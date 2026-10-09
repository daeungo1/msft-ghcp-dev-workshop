---
title: S1 회원·게시글 (30분)
description: 테스트 없이 완료를 보고하는 에이전트에게 테스트 먼저 규칙과 역할 분리를 붙입니다
---

| 항목 | 내용 |
|---|---|
| 시간 | 30분 (시도 5, 관찰 3, 하네스 추가 10, 재실행 10, 확인 2) |
| 도구 | Copilot CLI 또는 VS Code Copilot Chat (커스텀 에이전트 선택 가능) |
| 시작 상태 | S0 완료 (`s0-done`) |
| 완료 상태 | `s1-done` 브랜치와 같은 수준 |
| 통제 방식 | 안내 + 역할 분리 |
| 막는 함정 | 테스트 없이 구현만 하고 "완료"라고 보고 |

## 이 단계에서 배우는 것

* 같은 모델이라도 "테스트를 쓰는 역할"과 "구현하는 역할"을 나누면, 테스트를 구현에 맞춰 고치는 일이 줄어듭니다.
* 스킬은 필요할 때 불러오는 절차이고, 커스텀 에이전트는 역할과 도구 범위를 가진 전문가입니다.

## 시작 전 확인

```bash
git status --short            # 비어 있어야 합니다. 남은 변경이 있으면 commit 하거나 stash
scripts/checkpoint.sh S0      # S0를 건너뛰었다면 정답 상태에서 시작
```

## 추가 요건

[requirements/01-member-post.md](../requirements/01-member-post.md): 회원 가입, 게시글 작성·목록, 화면 뼈대. 수용 기준 5개를 읽어 둡니다.

## 1. 하네스 없이 시도 (5분)

```text
requirements/01-member-post.md 의 요건을 백엔드와 프론트엔드 모두 구현해줘.
```

## 2. 관찰 (3분)

* 에이전트가 테스트를 작성했나요? 구현보다 먼저였나요?
* "완료했습니다"라고 보고하면서 테스트를 실제로 실행했나요?
* `cd backend && uv run pytest`를 직접 실행해 보세요. 수용 기준 5개를 모두 검증하나요?
* 커밋 이력에서 테스트와 구현의 순서는 어땠나요?

확인이 끝나면 변경을 보관합니다.

```bash
git stash push -u -m "s1-no-harness"
```

## 3. 하네스 추가 (10분)

[templates/starter/s1/](../templates/starter/s1/)의 스타터 세 개를 복사해 TODO를 채웁니다.

| 자산 | 복사 위치 | 핵심 내용 |
|---|---|---|
| `tdd` 스킬 | `.github/skills/tdd/SKILL.md` | 수용 기준을 테스트로 옮기고, 실패를 확인하고, 최소 구현을 하는 절차. 테스트를 약하게 만들어 통과시키는 것을 금지 |
| `test-writer` 에이전트 | `.github/agents/test-writer.agent.md` | 요건의 수용 기준을 `backend/tests/<패키지>/`의 실패하는 테스트로 옮김. 구현 코드는 쓰지 않음 |
| `implementer` 에이전트 | `.github/agents/implementer.agent.md` | 이미 커밋된 실패 테스트를 통과시키는 최소 구현. 테스트 파일은 수정하지 않음 |

```bash
mkdir -p .github/skills/tdd .github/agents
cp templates/starter/s1/tdd-skill.starter.md .github/skills/tdd/SKILL.md
cp templates/starter/s1/test-writer.agent.starter.md .github/agents/test-writer.agent.md
cp templates/starter/s1/implementer.agent.starter.md .github/agents/implementer.agent.md
```

채울 때 지킬 점은 다음과 같습니다.

* 스킬과 에이전트 모두 frontmatter의 `description`이 가장 중요합니다. 에이전트는 이 문장을 보고 선택하고 불러옵니다.
* 에이전트 파일은 `name`(선택), `description`(필수), `tools`(선택)를 씁니다. `tools`에는 `read`, `search`, `edit`, `execute` 같은 별칭을 사용합니다.
* 힌트가 필요하면 Copilot에게 직접 물어도 됩니다. 예: `이 스타터의 TODO를 우리 프로젝트에 맞게 채워줘. 테스트 위치는 backend/tests/<패키지>/`.

## 4. 같은 요청 재실행 (10분)

역할을 나눠 순서대로 실행합니다. Copilot CLI에서는 `/agent`로 에이전트를 고르고, VS Code에서는 채팅의 에이전트 선택기를 씁니다.

1. `test-writer`를 선택합니다.

   ```text
   requirements/01-member-post.md 의 수용 기준을 backend/tests/members, backend/tests/posts 의 실패하는 테스트로 옮겨줘.
   ```

   실행해서 **실패하는지** 확인하고, 테스트를 먼저 커밋합니다.

   ```bash
   cd backend && uv run pytest -q ; cd ..
   git add backend/tests && git commit -m "test(backend): add members and posts API tests"
   ```

2. `implementer`를 선택합니다.

   ```text
   커밋된 테스트를 모두 통과시키는 구현을 backend/app/members, backend/app/posts 에 작성하고, 프론트엔드 화면(회원 선택, 글쓰기 폼, 글 목록)도 구현해줘.
   ```

   ```bash
   cd backend && uv run pytest -q ; cd ..
   git add -A && git commit -m "feat: implement members and posts"
   ```

3. 에이전트가 테스트 파일을 건드렸는지 확인합니다.

   ```bash
   git diff HEAD~1 --stat -- backend/tests
   ```

   변경이 있다면 "테스트를 고쳐서 통과시킨" 것입니다. `implementer` 지침의 해당 부분을 강화하세요.

화면은 `scripts/dev.sh`로 실행해 포트 5173에서 직접 확인합니다.

## 5. 완료 확인 (2분)

```bash
scripts/verify-step.sh S1
```

| 확인 항목 | 안 되면 |
|---|---|
| 백엔드와 프론트엔드 테스트 통과 | 실패 메시지를 `implementer`에게 전달 |
| `tdd` 스킬, 두 에이전트 파일 존재 | 3 표의 복사 위치 확인 |
| `backend/tests/posts` 커밋이 `backend/app/posts` 커밋보다 먼저 | 테스트를 먼저 커밋하세요. 순서가 뒤집혔다면 `git rebase -i`로 정리하거나 정답에서 합류 |

> [!NOTE]
> 마지막 항목은 패키지 경로가 `backend/app/posts`, `backend/tests/posts`일 때만 검사됩니다. S0에서 정한 도메인 패키지 구조가 그대로인지 확인하세요.

## 정리

* 안내를 더 길게 쓰는 것보다 역할을 나누는 편이 테스트 우선 규칙을 지키게 하는 데 효과적입니다.
* 그래도 에이전트가 규칙을 어길 수 있습니다. 어겨서는 안 되는 규칙은 S2에서 강제로 올립니다.

## 막히면

* 에이전트 목록에 보이지 않으면 파일 이름이 `*.agent.md`인지, 위치가 `.github/agents/`인지 확인하고 세션을 다시 시작합니다.
* 시간이 부족하면 `scripts/checkpoint.sh S1`로 정답 상태에서 합류합니다.

## 정답 보기

```bash
git diff s0-done..s1-done --stat
git show s1-done:.github/skills/tdd/SKILL.md
git show s1-done:.github/agents/test-writer.agent.md
```

## 업계 공통 패턴

TDD 강제를 위한 스킬과 역할 분리. [bp-catalog](../bp-catalog/README.md)를 참고합니다.
