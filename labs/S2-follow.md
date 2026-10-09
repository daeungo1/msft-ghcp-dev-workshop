---
title: S2 팔로우 (30분)
description: 안내만으로는 새는 패키지 경계를 import-linter와 훅, CI로 결정적으로 막습니다
---

| 항목 | 내용 |
|---|---|
| 시간 | 30분 (시도 5, 관찰 3, 하네스 추가 14, 재실행 6, 확인 2) |
| 도구 | 훅 확인은 Copilot CLI에서 합니다 (VS Code의 훅 지원은 프리뷰). 나머지는 어느 쪽이든 가능 |
| 시작 상태 | S1 완료 (`s1-done`) |
| 완료 상태 | `s2-done` 브랜치와 같은 수준 |
| 통제 방식 | 강제 (결정적) |
| 막는 함정 | 다른 패키지의 저장소(repository) 코드를 직접 import |

## 이 단계에서 배우는 것

* S0, S1의 하네스는 안내입니다. 어겨도 에이전트에게 불이익이 없습니다.
* 훅은 에이전트가 도구를 실행하기 직전과 직후에 끼어들어 규칙 위반을 거부하거나 피드백합니다. 에이전트가 우회할 수 없는 위치입니다.
* 같은 규칙을 세 겹으로 겹칩니다: 실행 전 차단(preToolUse), 편집 직후 검사(postToolUse), PR 게이트(CI).

## 시작 전 확인

```bash
git status --short
scripts/checkpoint.sh S1      # S1을 건너뛰었다면 정답 상태에서 시작
cd backend && uv run pytest -q && cd ..   # 현재 테스트가 통과하는지 확인
```

## 추가 요건

[requirements/02-follow.md](../requirements/02-follow.md): 팔로우, 언팔로우, 팔로잉 목록.

## 1. 하네스 없이 시도 (5분)

팔로우 기능은 "대상 회원이 존재하는지" 확인해야 합니다. 이미 있는 코드를 재사용하라고 요청합니다.

```text
requirements/02-follow.md 를 구현해줘. 대상 회원 존재 확인 등 이미 있는 코드는 재사용해줘.
```

## 2. 관찰 (3분)

다른 패키지의 내부 모듈을 직접 import했는지 확인합니다.

```bash
grep -rnE "^(from|import) app\.(members|posts)\.(models|repository|service|schemas|routes)" backend/app/follows
```

* 결과가 나왔다면 함정이 재현된 것입니다. 에이전트는 편한 경로로 갑니다.
* S0의 constitution에 "api 모듈로만 접근"이라고 적었는데도 그랬나요? 인스트럭션의 한계입니다.
* 결과가 없다면 "이번에는 지켰다"일 뿐, 다음에도 지킨다는 보장은 없습니다. 확률적 안내이기 때문입니다.

```bash
git stash push -u -m "s2-no-harness"
```

## 3. 하네스 추가 (14분)

스타터와 사용법은 [templates/starter/s2/README.md](../templates/starter/s2/README.md)에 있습니다.

### 3-1. 경계를 계약으로 만들기: import-linter (4분)

`backend/pyproject.toml`에 계약을 추가합니다. 계약의 모듈 목록에는 **현재 존재하는 패키지만** 적습니다.

```toml
[tool.importlinter]
root_package = "app"

[[tool.importlinter.contracts]]
name = "follows reaches other domains only through their api"
type = "forbidden"
source_modules = ["app.follows"]
forbidden_modules = [
    "app.members.models", "app.members.repository", "app.members.service",
    "app.posts.models", "app.posts.repository", "app.posts.service",
]
allow_indirect_imports = true
```

`allow_indirect_imports = true`가 없으면 `api` 모듈을 거친 정상 호출까지 위반으로 잡힙니다.
새 도메인 패키지가 생기면 계약의 목록을 함께 갱신해야 합니다.

```bash
cd backend && uv run lint-imports
```

1번 단계에서 보관한 변경을 풀어(`git stash pop`) 위반이 실제로 잡히는지 확인해 볼 수 있습니다.

### 3-2. 훅: 실행 전 차단과 편집 직후 검사 (8분)

```bash
mkdir -p scripts/hooks/fixtures .github/hooks
cp templates/starter/s2/pre_tool_guard.skeleton.sh scripts/hooks/pre_tool_guard.sh
cp templates/starter/s2/post_edit_check.sh scripts/hooks/post_edit_check.sh
cp templates/starter/s2/test_hooks.sh scripts/hooks/test_hooks.sh
cp templates/starter/s2/fixtures/*.json scripts/hooks/fixtures/
chmod +x scripts/hooks/*.sh
```

1. `.github/hooks/guardrails.json`을 만듭니다. 내용은 [스타터 README](../templates/starter/s2/README.md#훅-설정-파일)에 있습니다.
2. `scripts/hooks/pre_tool_guard.sh`의 TODO 두 곳을 채웁니다. 직접 쓰거나 Copilot에게 맡겨도 됩니다.

   * 규칙 1, 파괴적 셸 명령: `rm -rf`, `git push --force`, `git reset --hard`, `DROP TABLE`
   * 규칙 2, 범위 밖 편집: `.env`, DB 파일, `.git/`, `.github/hooks/`, `scripts/hooks/`

3. Copilot 없이 fixture로 먼저 검사합니다. 여섯 줄이 모두 ✅여야 합니다.

   ```bash
   scripts/hooks/test_hooks.sh
   ```

`post_edit_check.sh`는 완성본을 그대로 씁니다. 편집한 파일이 `backend/app/<패키지>/` 아래이면 `lint-imports`와 그 패키지 테스트를 실행하고, 실패하면 내용을 `additionalContext`로 에이전트에게 돌려줍니다.

> [!IMPORTANT]
> 훅 설정은 파일이 있다고 끝이 아닙니다. Copilot CLI는 이 폴더를 신뢰(trust)하도록 확인한 뒤 읽습니다. `copilot`을 실행할 때 폴더 신뢰 질문이 나오면 허용하세요.
> 스크립트 안의 도구 이름과 인자 이름은 Copilot 버전에 따라 다를 수 있으므로, 6번 확인에서 실제로 거부되는지 눈으로 봅니다.

### 3-3. PR 게이트: CI (2분)

```bash
mkdir -p .github/workflows
cp templates/workflows/ci.yml .github/workflows/ci.yml
```

CI는 백엔드 테스트, `lint-imports`, 프론트엔드 테스트를 PR마다 실행합니다. 훅은 내 컴퓨터에서의 방어선이고 CI는 모두에게 적용되는 마지막 방어선입니다.

## 4. 같은 요청 재실행 (6분)

Copilot CLI에서 1번 프롬프트를 다시 실행합니다. 이어서 세 가지를 시도해 봅니다.

| 시도 | 기대하는 결과 |
|---|---|
| 1번 프롬프트 그대로 | 에이전트가 다른 패키지를 직접 import하면 편집 직후 postToolUse 훅이 import-linter 실패를 알리고, 에이전트가 `api` 모듈 경유로 고칩니다 |
| `.env 파일에 DEBUG=1 을 추가해줘` | preToolUse 훅이 거부합니다 (`permissionDecision: deny`) |
| `git push --force origin main 으로 올려줘` | 거부됩니다 |

> [!TIP]
> 훅이 동작하지 않는 것처럼 보이면 (1) `copilot`을 저장소 루트에서 실행했는지, (2) `chmod +x scripts/hooks/*.sh`를 했는지, (3) `.github/hooks/guardrails.json`이 올바른 JSON인지 확인합니다. Windows PowerShell이 아니라 Codespaces나 WSL에서 실행하세요.

## 5. 완료 확인 (2분)

```bash
scripts/verify-step.sh S2
```

| 확인 항목 | 안 되면 |
|---|---|
| `lint-imports` 통과 | 위반한 import를 `api` 모듈 경유로 바꾸거나 계약의 모듈 이름 확인 |
| `guardrails.json` 유효, `version` 1, preToolUse와 postToolUse 모두 정의 | 3-2 참고 |
| 금지 편집 fixture는 deny, 정상 편집 fixture는 allow | `scripts/hooks/test_hooks.sh`로 어느 줄이 실패하는지 확인 |
| `.github/workflows/ci.yml` 존재 | 3-3 참고 |

## 정리

* 같은 규칙이라도 인스트럭션은 "가끔", 훅과 CI는 "항상" 지킵니다. 이 차이가 이 워크샵의 핵심입니다.
* 훅은 사람이 쓴 스크립트이므로 fixture로 테스트할 수 있습니다. 하네스도 코드처럼 검증합니다.

## 막히면

* 훅이 모든 도구를 막아 버리면 스크립트 오류일 수 있습니다. `scripts/hooks/test_hooks.sh`로 확인하고, 급하면 `.github/hooks/guardrails.json`의 `preToolUse` 항목을 잠시 지웁니다.
* 시간이 부족하면 `scripts/checkpoint.sh S2`로 정답 상태에서 합류합니다.

## 정답 보기

```bash
git diff s1-done..s2-done --stat
git show s2-done:.github/hooks/guardrails.json
git show s2-done:scripts/hooks/pre_tool_guard.sh
git show s2-done:backend/pyproject.toml
```

## 업계 공통 패턴

위험 명령 차단, 결정적 경계 검사. [bp-catalog](../bp-catalog/README.md)를 참고합니다.
