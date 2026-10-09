---
title: S0 Spec (25분)
description: 앱의 원칙과 범위를 먼저 정해 이후 모든 요청의 구조와 스타일을 고정합니다
---

| 항목 | 내용 |
|---|---|
| 시간 | 25분 (시도 5, 관찰 2, 하네스 추가 13, 재실행 3, 확인 2) |
| 도구 | Copilot CLI 또는 VS Code Copilot Chat, spec-kit |
| 시작 상태 | `main` |
| 완료 상태 | `s0-done` 브랜치와 같은 수준 |
| 통제 방식 | 안내 (확률적) |
| 막는 함정 | 같은 요청이라도 문장이 달라지면 구조와 스타일이 달라짐 |

## 이 단계에서 배우는 것

* 코드를 쓰기 전에 원칙(constitution)과 명세(spec, plan, tasks)를 먼저 두면 이후 모든 요청이 같은 틀에서 시작합니다.
* 인스트럭션과 AGENTS.md는 모든 요청에 자동으로 붙는 맥락입니다. 다만 안내일 뿐이라는 점을 S2에서 확인합니다.

## 시작 전 확인

* Codespaces 또는 Dev Container가 열려 있고 사전 점검 명령이 통과합니다 ([README](../README.md#시작하기)).
* [requirements/00-vision.md](../requirements/00-vision.md)를 한 번 읽었습니다.

## 1. 하네스 없이 시도 (5분)

같은 기능을 서로 다른 문장으로 두 번 요청합니다. 각 요청은 새 세션(Copilot CLI는 `/clear`, VS Code는 새 채팅)에서 합니다.

```text
회원 가입 API 만들어줘.
```

```text
FastAPI로 회원 등록 엔드포인트를 추가해줘.
```

## 2. 관찰 (2분)

두 결과를 비교합니다. 코드를 읽지 말고 파일 목록과 응답 형태만 봅니다.

* 패키지 구조와 파일 이름이 같은가요? (`backend/app/` 아래 어디에 무엇이 생겼나)
* 오류 응답 형식이 같은가요? (409, 422가 어떤 JSON으로 나가나)
* 테스트가 함께 만들어졌나요? 어느 디렉터리에?
* 요청마다 이전에 정한 적 없는 결정을 에이전트가 혼자 내렸나요?

확인이 끝나면 변경을 보관합니다. 지우지 않고 보관해 두면 나중에 비교할 수 있습니다.

```bash
git stash push -u -m "s0-no-harness"
```

> [!NOTE]
> 두 결과가 우연히 비슷했다면 한 번 더 다른 문장으로 시도하세요. 어느 쪽이든 "문장에 따라 달라질 수 있다"는 사실이 이 단계의 출발점입니다.

## 3. 하네스 추가 (13분)

### 3-1. spec-kit으로 원칙과 명세 만들기 (8분)

spec-kit은 명세에서 구현까지 이어지는 스펙 주도 개발 도구입니다. 이미 있는 저장소에는 `--here`로 초기화합니다.

```bash
git add -A && git commit -m "chore: before spec-kit init"   # 초기화 전에는 변경을 커밋하거나 stash 합니다
specify init --here --force --integration copilot
```

초기화가 끝나면 Copilot 세션에서 아래 명령을 차례로 실행합니다. 자세한 입력 예시는 [templates/starter/s0/README.md](../templates/starter/s0/README.md)에 있습니다.

| 순서 | 명령 | 결과 파일 |
|---|---|---|
| 1 | `/speckit-constitution` | `.specify/memory/constitution.md` |
| 2 | `/speckit-specify` + [00-vision.md](../requirements/00-vision.md) 내용 | `specs/<번호>-<이름>/spec.md` |
| 3 | `/speckit-plan` | `specs/<번호>-<이름>/plan.md` |
| 4 | `/speckit-tasks` | `specs/<번호>-<이름>/tasks.md` |

constitution에는 다음 다섯 가지를 반드시 담습니다. 각 원칙에는 "무엇으로 검증하는가"를 한 줄 적습니다.

1. 테스트 우선
2. 패키지 경계: 도메인 패키지끼리는 `api` 모듈로만 접근
3. 작은 변경: 요청 범위만 수정
4. 에러 응답 형식 통일
5. 보안 기본값: 인가와 입력 검증

plan에는 도메인 패키지 구성을 명시합니다. 이후 단계 검사가 이 구조를 전제로 합니다.

```text
backend/app/<도메인>/    members, posts, follows, feed, reports (각 패키지에 models, repository, service, schemas, api, routes)
backend/tests/<도메인>/  도메인별 테스트
```

> [!WARNING]
> `/speckit-implement`는 지금 실행하지 않습니다. 구현은 기능별로 S1부터 합니다.

### 3-2. 인스트럭션과 AGENTS.md 작성 (5분)

두 파일을 직접 만듭니다. 길게 쓰지 말고 지킬 수 있는 규칙 몇 개만 적습니다.

* `.github/copilot-instructions.md`: 저장소 전체에 자동 적용되는 규칙. 스타일, 에러 형식, 테스트 규칙
* `AGENTS.md`: 에이전트용 README. 개발 명령(`cd backend && uv run pytest`, `cd frontend && npm test`)과 작업 원칙(가정은 먼저 말하기, 요청 범위만 수정)

예시는 아래와 같습니다. 그대로 쓰지 말고 우리 팀 방식으로 바꾸세요.

```markdown
## 작업 원칙
* 요구에 모호함이 있으면 가정을 먼저 한 문장으로 말하고 진행한다.
* 요청 범위의 파일만 수정한다.
* 완료 보고에는 실행한 테스트 명령과 결과를 포함한다.

## 개발 명령
* 백엔드 테스트: `cd backend && uv run pytest`
* 프론트엔드 테스트: `cd frontend && npm test`
```

## 4. 같은 요청 재실행 (3분)

1번의 두 문장을 다시, 새 세션에서 실행합니다.

* 두 결과가 이번에는 같은 구조와 에러 형식으로 나오는지 확인합니다.
* constitution의 원칙(`api` 모듈 경계, 테스트 위치)이 반영되었는지 확인합니다.

확인이 끝나면 다시 변경을 보관합니다.

```bash
git stash push -u -m "s0-with-harness"
```

> [!NOTE]
> 구조가 많이 가까워졌더라도 100% 같아지지는 않습니다. 인스트럭션은 "안내"이기 때문입니다. S2에서 이 한계를 강제 장치로 보완합니다.

## 5. 완료 확인 (2분)

```bash
git add -A && git commit -m "docs: add constitution, spec, instructions"
scripts/verify-step.sh S0
```

| 확인 항목 | 안 되면 |
|---|---|
| constitution 존재 | `/speckit-constitution` 실행 |
| spec, plan, tasks 존재 | 3-1 표의 2~4번 실행 |
| constitution 원칙 5개 이상 | 원칙마다 `##` 또는 `###` 제목을 사용 |
| copilot-instructions.md, AGENTS.md 존재, AGENTS.md에 `pytest` 포함 | 3-2 참고 |

## 정리

* 하네스 첫 층은 맥락입니다. 코드를 쓰기 전에 원칙과 명세를 파일로 남깁니다.
* 그러나 이것은 안내입니다. 에이전트가 어길 수 있다는 점을 S2에서 다시 만납니다.

## 막히면

* `specify`가 없다고 나오면 `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git`을 실행합니다.
* `/speckit-*` 명령이 보이지 않으면 `specify init --here --force --integration copilot`을 다시 실행하고 세션을 새로 시작합니다.
* 시간이 부족하면 `scripts/checkpoint.sh S0`으로 정답 상태에서 시작합니다.

## 정답 보기

```bash
git diff main..s0-done --stat
git show s0-done:.specify/memory/constitution.md
```

## 업계 공통 패턴

에이전트 행동 원칙, 스펙 주도 개발. [bp-catalog](../bp-catalog/README.md)를 참고합니다.
