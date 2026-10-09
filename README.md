---
title: GitHub Copilot 개발자 워크샵 Hands-on Lab
description: 빈 저장소에서 TeamFeed를 만들며 우리 팀 BP를 GitHub Copilot 하네스로 한 겹씩 쌓는 180분 핸즈온 실습 저장소
---

AI-DLC 개발자 워크샵 세션 3 「트렌드 Harness 워크샵 (GHCP 기반)」의 실습 저장소입니다.
혼자 읽고 따라 해도 끝까지 진행할 수 있도록, 각 단계의 요건, 프롬프트, 관찰 포인트, 완료 확인, 정답 위치를 모두 담았습니다.

## 이 워크샵을 한 문장으로

사내 미니 SNS **TeamFeed**를 GitHub Copilot으로 직접 만들면서, 기능을 하나 추가할 때마다 그 기능에서 실제로 터지는 문제를 막는 **하네스**를 한 겹씩 붙입니다.

하네스는 에이전트가 우리 팀의 방식대로 일하도록 감싸는 맥락(Context), 도구(Tools), 흐름 제어(Control Flow), 피드백(Feedback) 장치의 묶음입니다.
인스트럭션과 스킬은 확률적 안내이고, 훅, 테스트, CI, 리뷰 게이트는 결정적 강제입니다. 이 차이를 직접 눈으로 확인하는 것이 핵심입니다.

개념이 낯설다면 먼저 [docs/concepts.md](docs/concepts.md)(10분)를 읽으세요.

## 워크샵이 끝나면 남는 것

| 결과물 | 위치 | 내용 |
|---|---|---|
| 동작하는 앱 | `backend/`, `frontend/` | FastAPI 백엔드와 React 피드 화면 (회원, 게시글, 팔로우, 피드, 신고) |
| 팀 하네스 자산 | `.github/`, `.specify/`, `specs/`, `AGENTS.md` | constitution, 커스텀 인스트럭션, 스킬, 커스텀 에이전트, 훅, MCP 설정, CI |
| 팀 플러그인 | `plugins/teamfeed-harness/` | 내 팀 규칙 1개를 더한 BP 패키지. 다음 프로젝트에서 한 줄로 설치 |

## 학습 여정

```text
S0 Spec ──▶ S1 회원·게시글 ──▶ S2 팔로우 ──▶ (휴식) ──▶ S3 피드 ──▶ S4 신고 ──▶ S5 패키징 ──▶ 회고
 맥락        역할 분리           결정적 강제              도구 범위       독립 리뷰      배포·재사용      자가진단
```

| 단계 | 시간 | 추가 요건 | 붙이는 하네스 | 막는 함정 | 통제 방식 |
|---|---|---|---|---|---|
| [S0 Spec](labs/S0-spec.md) | 25분 | 앱 비전, MVP | constitution, copilot-instructions.md, AGENTS.md, spec/plan/tasks | 프롬프트마다 구조와 스타일이 달라짐 | 안내 |
| [S1 회원·게시글](labs/S1-member-post.md) | 30분 | 가입, 글 작성·목록, 피드 화면 뼈대 | `tdd` 스킬, `test-writer`·`implementer` 에이전트 | 테스트 없이 완료 보고 | 안내 + 역할 분리 |
| [S2 팔로우](labs/S2-follow.md) | 30분 | 팔로우, 언팔로우 | import-linter, pre·postToolUse 훅, PR CI | 저장소 코드 직접 import | 강제 |
| 휴식 | 15분 | | | | |
| [S3 피드](labs/S3-feed.md) | 15분 | 팔로우한 사람 글 모아 보기 | 읽기 전용 SQLite MCP, GitHub MCP | 스키마를 추측한 쿼리 | 도구 범위 제한 |
| [S4 신고](labs/S4-report.md) | 35분 | 신고, 관리자 처리 화면 | `security-reviewer` 에이전트, rubber duck, CodeQL, Copilot code review | 관리자 인가 누락 | 독립 리뷰 |
| [S5 패키징](labs/S5-package.md) | 30분 | 다음 프로젝트에서 재사용 | 팀 플러그인 + 내 팀 규칙 1개 | 하네스가 저장소에 갇힘 | 배포·재사용 |
| [회고·자가진단](labs/99-retro.md) | 15분 | | 함정 6개 회고표, 자가진단 카드 | | |

각 단계는 같은 6단계 루프로 진행합니다.

1. [requirements/](requirements/)에서 기능 요건과 Given/When/Then 수용 기준을 읽습니다.
2. 하네스 없이 Copilot에게 그대로 구현을 요청합니다.
3. 요건 속 함정이 실제로 재현되는지 관찰합니다.
4. 공식 기능으로 우리 BP 하네스를 추가합니다.
5. 같은 프롬프트로 다시 구현을 요청합니다.
6. `scripts/verify-step.sh S<n>`으로 완료를 확인합니다.

> [!TIP]
> 관찰 포인트는 "인스트럭션은 가끔 지켜지고, 훅과 리뷰어는 반드시 막는다"는 차이입니다 (S2, S4).
> 함정이 재현되지 않아도 괜찮습니다. 재현되지 않았다는 사실도 모델과 프롬프트에 따라 결과가 달라진다는 증거입니다.

## 하네스 네 계층과 단계의 대응

| 계층 | 하는 일 | 이 워크샵에서 만드는 자산 | 단계 |
|---|---|---|---|
| Context | 에이전트가 읽는 규칙과 명세 | constitution, copilot-instructions.md, AGENTS.md, spec/plan/tasks, 스킬 | S0, S1 |
| Tools | 에이전트가 쓸 수 있는 도구와 그 범위 | 커스텀 에이전트(tools 제한), 읽기 전용 SQLite MCP, GitHub MCP | S1, S3, S4 |
| Control Flow | 작업 순서와 경계를 강제 | 역할 분리(테스트 먼저), 훅, import-linter | S1, S2 |
| Feedback | 결과를 검증하고 되돌려 줌 | pytest, postToolUse 훅, CI, CodeQL, 리뷰어 에이전트 | S2, S4 |

여기에 S5에서 이 모두를 플러그인으로 묶어 저장소 밖으로 꺼냅니다.

## 시작하기

1. 이 저장소 상단의 **Use this template**을 눌러 내 계정에 저장소를 만듭니다. **Include all branches**를 반드시 체크합니다.
   템플릿을 쓸 수 없다면 `git clone` 후 `scripts/checkpoint.sh`가 정답 브랜치를 알아서 가져옵니다.
2. 내 저장소에서 **Code > Codespaces > Create codespace on main**으로 개발 환경을 엽니다. 첫 빌드는 약 10분입니다.
3. 터미널에서 사전 점검 명령을 실행합니다.

   ```bash
   copilot --version
   uv --version
   node -v
   specify --help
   ```

4. Copilot CLI에 로그인합니다. `copilot`을 실행하고 안내에 따라 `/login`을 진행합니다.
5. [labs/S0-spec.md](labs/S0-spec.md)부터 순서대로 진행합니다.

> [!IMPORTANT]
> `main` 브랜치에는 하네스 파일(`.github/copilot-instructions.md`, `AGENTS.md`, `.github/agents`, `.github/skills`, `.github/hooks`, `.mcp.json`)이 의도적으로 없습니다.
> "하네스 없이 시도"에서 함정을 재현하기 위해서입니다. 직접 만들기 전에 `final` 브랜치를 열어 보지 않는 편이 학습에 좋습니다.

## 막혔거나 늦었을 때

단계마다 정답 상태가 `s0-done` … `s5-done` 브랜치에 있습니다.
단계 시간의 70%가 지났다면 직전 단계 정답으로 이동해 다음 단계에 합류합니다.

```bash
scripts/checkpoint.sh S2          # s2-done 상태로 work/s2 브랜치 생성 (로컬 변경은 자동 stash)
git diff main..s2-done --stat     # 정답이 main과 어떻게 다른지 파일 단위로 보기
git show s2-done:.github/hooks/guardrails.json   # 정답 파일 하나만 읽기
```

| 브랜치 | 내용 |
|---|---|
| `main` | 참가자 진입점. 앱 골격, 요건, 가이드, 템플릿만 포함 |
| `s0-done` … `s5-done` | 해당 단계를 마친 시점의 정답 앱과 누적 하네스 |
| `final` | 모든 단계가 끝난 최종 완성본. 회고표 예시, 팀 규칙 3개, marketplace 등록까지 끝난 플러그인 `v1.0.0` 포함. 태그 `v1.0` |
| `authoring` | 저장소 구축 계획(Plan.md). 참가자는 볼 필요 없음 |

각 `sN-done` 브랜치는 `scripts/verify-step.sh S<N>`을 통과하는 상태입니다.

## 저장소 구조

```text
msft-ghcp-dev-workshop/
├── .devcontainer/      # Python 3.12, uv, Node 22, GitHub CLI, Copilot CLI, spec-kit
├── backend/            # FastAPI 골격 (의존성과 테스트 설정만)
├── frontend/           # React + Vite 골격 (의존성만)
├── requirements/       # 단계별 요건과 수용 기준 (00 비전 ~ 05 패키징)
├── labs/               # 단계 가이드 S0~S5, 회고
├── docs/               # concepts.md 개념 정리, after-workshop.md 워크샵 이후
├── bp-catalog/         # 업계 공통 패턴, 우리 BP, GHCP 기능 매핑
├── templates/          # 사전 제공 자산 (워크플로, MCP, 플러그인 골격, 스타터, 팀 규칙, 자가진단 카드)
├── scripts/            # verify-step.sh, checkpoint.sh, seed-db.py, dev.sh
└── facilitator/        # 강사용 진행표, 사전 준비, 트러블슈팅, 함정 재현 기록
```

## 발표 자료와의 대응

발표 자료 「Github Copilot 개발자 워크샵」의 3번 Agenda(슬라이드 15~25)와 이 저장소의 대응입니다.

| 슬라이드 | 내용 | 이 저장소에서 |
|---|---|---|
| 16 | 공식 자산과 업계 패턴에서 우리 팀 BP로 | [bp-catalog/](bp-catalog/README.md) |
| 17 | 실습 앱 TeamFeed | [requirements/00-vision.md](requirements/00-vision.md) |
| 18 | 시도, 관찰, 하네스 추가, 재실행 | 위의 6단계 루프, 각 [labs/](labs/) |
| 19 | 기능이 늘수록 하네스가 쌓임 | 위의 하네스 네 계층 표 |
| 20 | S0~S2 문제와 하네스 | [S0](labs/S0-spec.md), [S1](labs/S1-member-post.md), [S2](labs/S2-follow.md) |
| 21 | S3~S5 문제와 하네스 | [S3](labs/S3-feed.md), [S4](labs/S4-report.md), [S5](labs/S5-package.md) |
| 22, 23 | 업계 트렌드 하네스와 도입 방법 세 가지 | [bp-catalog/](bp-catalog/README.md), [docs/concepts.md](docs/concepts.md) |
| 24 | 실습 저장소와 사전 준비 | 이 문서의 "시작하기", [facilitator/prerequisites-checklist.md](facilitator/prerequisites-checklist.md) |
| 25 | 회고와 자가진단 | [labs/99-retro.md](labs/99-retro.md), [templates/self-check-card.md](templates/self-check-card.md) |
| 26~29 | 워크샵 이후 | [docs/after-workshop.md](docs/after-workshop.md) |

## 자주 묻는 질문

### 테스트가 실패하는데 어디부터 봐야 하나요?

`scripts/verify-step.sh S<n>`의 ❌ 줄 뒤 화살표(→)가 힌트입니다. 그래도 막히면 `scripts/checkpoint.sh`로 정답에서 합류합니다.

### Copilot이 제 프롬프트와 다른 결과를 내요.

정상입니다. 같은 프롬프트라도 모델과 시점에 따라 결과가 다릅니다. 이 차이가 안내와 강제의 차이를 보여 주는 재료입니다.

### Windows에서도 되나요?

Codespaces나 Dev Container(WSL2 포함)를 권장합니다. 훅 스크립트는 bash로 작성되어 있습니다.

### Copilot CLI와 VS Code 중 무엇을 쓰나요?

둘 다 씁니다. 훅(S2)과 플러그인(S5)은 Copilot CLI에서 확인하고, 나머지는 어느 쪽이든 가능합니다. 각 단계 가이드에 명시되어 있습니다.

### 발표 자료에는 `ghcp-harness-workshop`, `start` 브랜치라고 적혀 있는데요.

실제 저장소 이름은 `msft-ghcp-dev-workshop`이고 시작 브랜치는 `main`입니다.

## 사전 준비

* GitHub 계정과 Copilot Business 또는 Enterprise 라이선스
* 조직 정책에서 Copilot CLI, MCP 서버, 프리뷰 기능 사용 허용
* GitHub Codespaces 또는 VS Code + Dev Containers
* CodeQL 실습은 공개 저장소이거나 GitHub Code Security 라이선스가 필요합니다. 없으면 강사 데모로 대체합니다

자세한 내용은 [facilitator/prerequisites-checklist.md](facilitator/prerequisites-checklist.md)를 참고합니다.

## 참고 자료

* [GitHub Docs: Copilot customization cheat sheet](https://docs.github.com/en/copilot/reference/customization-cheat-sheet)
* [GitHub Docs: Hooks](https://docs.github.com/en/copilot/concepts/agents/hooks)
* [GitHub Docs: Plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
* [GitHub Docs: Copilot CLI rubber duck](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/rubber-duck)
* [github/spec-kit](https://github.com/github/spec-kit)
* [github/awesome-copilot](https://github.com/github/awesome-copilot)
* [microsoft/hve-core](https://github.com/microsoft/hve-core)
* [HakjunMIN/ai-native-harness](https://github.com/HakjunMIN/ai-native-harness) (레퍼런스 구현, 워크샵 이후 단계)
