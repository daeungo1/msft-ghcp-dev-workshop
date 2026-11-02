---
title: GitHub Copilot and Spec Kit Multi-Harness Workshop
description: TeamFeed를 구현하며 Spec Kit 1.2.5, 멀티 에이전트, 다층 하네스, 수렴 검증을 익히는 개발자 워크숍
ms.date: 2026-11-02
ms.topic: tutorial
---

## TeamFeed Multi-Harness Workshop

TeamFeed는 GitHub Copilot과 Spec Kit으로 사내 미니 SNS를 구현하며,
재현 가능한 에이전트 개발 하네스를 설계하는 워크숍입니다.

v0.2는 Spec Kit 1.2.5의 공식 Copilot integration을 사용합니다. 명세에서
구현으로 끝내지 않고 extension, workflow, bundle, human gate,
`speckit-converge`까지 연결합니다.

> [!IMPORTANT]
> `main-v0.1`은 기존 완성 워크숍의 보존 브랜치입니다. 기존 `s0-done`부터
> `s5-done`, `final` 브랜치도 변경하지 않습니다. 새 `main`은 v0.2 기준선이며,
> 새 체크포인트 브랜치는 전체 경로 검증 후 배포합니다.

## 수료 목표

워크숍을 마치면 다음을 수행할 수 있습니다.

* constitution, spec, plan, tasks로 구현 의도와 검증 기준 연결
* 조사, 계획, 테스트, 구현, 리뷰 역할을 독립 에이전트로 분리
* instructions, skills, agents, hooks, MCP, CI의 책임 구분
* 모델 이름이 아니라 역할 역량과 검증 계약으로 모델 선택
* Spec Kit extension과 workflow를 bundle로 패키징
* 테스트와 `speckit-converge`로 코드와 명세의 차이 확인

## 전체 흐름

![S0에서 Spec Kit 기준선을 만들고 S6에서 수렴을 검증하는 워크숍 흐름](docs/images/workshop-workflow.svg)

```text
요청
  |
  v
constitution -> specify -> clarify -> plan -> tasks
  |
  v
researcher -> test-writer -> implementer -> independent reviewers
  |
  v
instructions -> skills -> agents -> hooks -> MCP -> CI
  |
  v
tests -> package boundaries -> security -> converge
  |
  v
extension + workflow + bundle
```

## 시작하기

### 권장 환경

* GitHub Codespaces 또는 VS Code Dev Containers
* Python 3.12
* Node.js 22
* uv
* GitHub Copilot CLI 또는 VS Code Copilot Chat
* Spec Kit 1.2.5

Windows PowerShell 단독 환경보다 제공된 개발 컨테이너를 권장합니다. Bash
hooks, Node.js, Python 도구 버전이 워크숍 검증 환경과 일치합니다.

### 설치

```bash
git clone https://github.com/daeungo1/msft-ghcp-dev-workshop.git
cd msft-ghcp-dev-workshop
git switch main

uv tool install specify-cli --force \
  --from git+https://github.com/github/spec-kit.git@v1.2.5
uv sync --directory backend
npm --prefix frontend install
```

설치 상태를 확인합니다.

```bash
specify --version
specify integration status --json
python scripts/validate-harness.py
```

## Spec Kit 기본 흐름

Copilot 세션에서 다음 skills를 순서대로 실행합니다.

```text
/speckit-constitution
/speckit-specify
/speckit-clarify
/speckit-plan
/speckit-tasks
/speckit-implement
/speckit-converge
```

`speckit-converge`가 남은 작업을 찾으면 `tasks.md`에 추가된 작업을 구현하고
다시 수렴 검사를 실행합니다.

## 실습 지도

| 단계 | 앱 기능 | 하네스 목표 | 핵심 자산 |
|---|---|---|---|
| S0 | 범위 정의 | Spec Kit 1.2.5 SDD 기준선 | constitution, spec, plan, tasks |
| S1 | 회원과 게시글 | 조사, 테스트, 구현 역할 분리 | skills, custom agents |
| S2 | 팔로우 | 결정적 경계와 위험 명령 차단 | import-linter, hooks, CI |
| S3 | 피드 | 최소 권한 컨텍스트 접근 | read-only SQLite MCP |
| S4 | 신고와 관리자 처리 | 독립 보안 리뷰와 모델 교차 검증 | reviewer agents, CodeQL |
| S5 | 팀 배포 | extension, workflow, bundle 패키징 | `spec-kit/` component sources |
| S6 | 완성도 확인 | 명세와 구현 수렴 | verification, converge, human gate |

상세 가이드는 [`labs/`](labs)에서 확인합니다.

## 하네스 계층

![TeamFeed 앱과 Spec Kit, Copilot 하네스 계층](docs/images/teamfeed-architecture.svg)

| 계층 | 책임 | 실패할 때의 방어선 |
|---|---|---|
| Constitution과 specs | 의도, 범위, 수용 기준 | clarify, analyze |
| Instructions | 저장소와 경로별 지속 규칙 | 리뷰 |
| Skills | 반복 가능한 작업 절차 | 역할 에이전트 |
| Agents | 조사, 계획, 테스트, 구현, 리뷰 경계 | 읽기/쓰기 도구 제한 |
| Hooks | 도구 실행 전후의 빠른 차단 | fixture tests |
| MCP | 외부 시스템과 실제 데이터 컨텍스트 | 최소 권한, read-only |
| CI | 모든 기여자에게 동일한 공유 게이트 | PR 차단 |
| Convergence | 명세와 현재 코드의 차이 | 후속 tasks |

구체적인 관계는
[`docs/multi-harness-architecture.md`](docs/multi-harness-architecture.md)를
참고하세요.

## 멀티 모델 원칙

저장소는 특정 모델을 필수로 지정하지 않습니다. 조사에는 긴 컨텍스트와
출처 추적, 계획에는 제약 통합, 구현에는 코드 정확성, 리뷰에는 독립적
추론을 우선합니다.

HydraFusion은 현재 공식 GitHub Copilot 제품 또는 공개 저장소 계약으로
확인되지 않았습니다. 클라이언트에서 제공되면 계획과 리뷰의 선택형 실험
모델로 사용할 수 있지만 agent frontmatter, workflow, CI에는 고정하지
않습니다.

자세한 기준은 [`docs/model-routing.md`](docs/model-routing.md)를 참고하세요.

## 저장소 구조

```text
backend/                    FastAPI, SQLAlchemy, SQLite
frontend/                   React, TypeScript, Vite
requirements/               단계별 수용 기준
specs/001-teamfeed-mvp/     TeamFeed 기능 명세, 계획, 작업
.specify/                   Spec Kit 1.2.5 관리 파일과 설치 상태
.github/agents/             역할별 custom agents
.github/skills/             Spec Kit과 TeamFeed skills
.github/instructions/       경로별 규칙
.github/hooks/              Copilot hook 설정
spec-kit/extensions/        TeamFeed 품질 extension source
spec-kit/workflows/         사람 승인을 포함한 delivery workflow source
spec-kit/bundles/           팀 배포 bundle source
labs/                       S0-S6 실습
scripts/                    개발, hook, 구조 검증
```

## 실행과 검증

```bash
# 하네스 구조
python scripts/validate-harness.py

# 백엔드
cd backend
uv run pytest
uv run lint-imports

# 프론트엔드
cd ../frontend
npm test
npm run build

# hooks
cd ..
bash scripts/hooks/test_hooks.sh

# 전체 워크숍
bash scripts/verify-step.sh ALL
```

개발 서버는 `scripts/dev.sh`로 실행합니다.

## 로컬 Spec Kit 구성

[`spec-kit/README.md`](spec-kit/README.md)의 순서대로 quality extension과
delivery workflow를 설치한 뒤 multi-harness bundle을 적용합니다.

```bash
specify workflow run teamfeed-delivery \
  --input spec="Build the next TeamFeed capability"
```

## 브랜치 정책

![v0.1 보존 브랜치와 v0.2 main 관계](docs/images/branch-map.svg)

* `main-v0.1`: v0.1 완성 상태 보존
* `s0-done`부터 `s5-done`: v0.1 단계별 체크포인트 보존
* `final`: v0.1 완성 브랜치 보존
* `main`: v0.2 기준선
* 새 v0.2 체크포인트: S0-S6 전체 검증 후 생성

원격 기록을 force-push하거나 기존 체크포인트를 재작성하지 않습니다.

## 공식 기준

* [GitHub Spec Kit](https://github.com/github/spec-kit)
* [Spec Kit v1.2.5](https://github.com/github/spec-kit/releases/tag/v1.2.5)
* [Spec Kit extensions](https://github.github.io/spec-kit/reference/extensions.html)
* [Spec Kit workflows](https://github.github.io/spec-kit/reference/workflows.html)
* [Spec Kit bundles](https://github.github.io/spec-kit/reference/bundles.html)
* [GitHub Copilot agent skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills)
* [GitHub Copilot MCP](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/customize-copilot/extend-copilot-with-tools-and-context/extend-copilot-chat-with-mcp)

## 라이선스

이 저장소는 [MIT License](LICENSE)를 따릅니다.
