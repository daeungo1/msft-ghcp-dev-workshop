---
title: AI MSFT Harness Workshop
description: Spec Kit 표준 개발 단계로 팀 맞춤형 GitHub Copilot 하네스를 만들고 TeamFeed 예제로 검증하는 개발자 워크숍
ms.date: 2026-11-04
ms.topic: tutorial
---

## AI MSFT Harness Workshop

이 워크숍의 목표는 **Spec Kit 표준 애플리케이션 개발 단계를 따라가며
팀과 프로젝트의 개발 패턴을 GitHub Copilot용 `ai-msft-harness` plugin으로
만드는 것**입니다.

TeamFeed는 하네스가 실제 애플리케이션 개발에서 어떻게 작동하는지 보여주는
reference application입니다. 회원, 게시글, 팔로우, 피드, 신고 기능을
단계적으로 구현하면서 각 하네스 계층의 필요성과 효과를 검증합니다.

> [!IMPORTANT]
> **최종 산출물: [`plugins/ai-msft-harness/`](plugins/ai-msft-harness/)**
>
> S0-S6에서 만든 역할 에이전트, skills, hooks, MCP를 Agent Plugins 1.0
> 패키지로 제공합니다. VS Code에서는 **Chat: Install Plugin from Source**,
> CLI에서는 `copilot plugin install ./plugins/ai-msft-harness`로 설치합니다.

![Spec Kit 개발 단계에서 재사용 가능한 ai-msft-harness까지 이어지는 워크숍 개요](docs/images/workshop-overview.svg)

완성된 하네스는 이 저장소에만 머물지 않습니다. 다른 사용자도 GitHub
Copilot의 marketplace에서 `ai-msft-harness`를 설치해 같은 skills, agents,
hooks, MCP를 사용할 수 있습니다.

```powershell
copilot plugin marketplace add daeungo1/msft-ghcp-dev-workshop
copilot plugin install ai-msft-harness@ai-msft-harness-marketplace
```

VS Code에서는 **Chat: Manage Plugin Marketplaces**에서
`daeungo1/msft-ghcp-dev-workshop`를 추가한 뒤 **Customize → Plugins**에서
`ai-msft-harness`를 설치합니다.

이 워크숍은 각 팀이 자신의 애플리케이션 개발 패턴을 설치 가능한 plugin으로
만드는 과정을 Spec Kit 단계에 맞춰 설명합니다.

### 이 워크숍에서 만드는 것

| 결과물 | 핵심 학습 |
|---|---|
| Reference application | FastAPI + React TeamFeed로 하네스 동작 검증 |
| Spec Kit 1.2.5 개발 흐름 | constitution, spec, plan, tasks, implement, converge |
| 역할별 Copilot 에이전트 | 조사, 계획, 테스트, 구현, 보안 리뷰, 수렴 리뷰 |
| 다층 하네스 | instructions, skills, agents, hooks, MCP, CI |
| 최종 설치 패키지 | [`ai-msft-harness`](plugins/ai-msft-harness/) Agent Plugin |
| 프로세스 패키지 | Spec Kit extension, workflow, bundle |

### 빠른 길찾기

| 지금 필요한 것 | 이동할 곳 |
|---|---|
| 바로 환경을 준비하고 싶음 | [빠른 시작](#빠른-시작) |
| 전체 실습 순서를 보고 싶음 | [S0-S6 학습 흐름](#s0-s6-학습-흐름) |
| 하네스 계층을 이해하고 싶음 | [멀티 하네스 구조](#멀티-하네스-구조) |
| Spec Kit 명령 순서가 궁금함 | [Spec Kit 실행 흐름](#spec-kit-실행-흐름) |
| 전체 검증 명령이 필요함 | [실행과 검증](#실행과-검증) |
| 과거 v0.1 브랜치를 찾고 있음 | [버전과 브랜치](#버전과-브랜치) |

> [!IMPORTANT]
> 현재 `main`은 v0.2 기준선입니다. 기존 워크숍 완성본은 `main-v0.1`과
> `final`, 단계별 정답은 `s0-done`부터 `s5-done`에 보존되어 있습니다.

## 수료 목표

워크숍을 마치면 다음을 설명하고 재현할 수 있습니다.

* 요구사항을 명세, 계획, 작업, 테스트로 추적
* 조사자와 작성자, 구현자와 리뷰어의 역할 분리
* 안내 규칙과 결정적 차단 장치의 차이
* 읽기 전용 MCP를 이용한 최소 권한 컨텍스트 제공
* 모델과 무관하게 유지되는 테스트와 검증 계약
* 구현 후 명세와 코드의 차이를 찾는 convergence 반복
* 팀 하네스를 다른 저장소에 배포하는 패키징 방식

## S0-S6 학습 흐름

S0-S6는 `ai-msft-harness`를 만드는 주 과정이고, TeamFeed 기능은 각 단계의
하네스를 검증하기 위한 실습 시나리오입니다.

![S0 명세에서 S6 수렴 검증까지 TeamFeed 예제로 하네스를 단계적으로 추가하는 흐름](docs/images/workshop-workflow.svg)

| 단계 | 앱 기능 | 하네스 목표 | 주요 산출물 |
|---|---|---|---|
| [S0](labs/S0-spec.md) | 범위 정의 | 개발 기준 고정 | constitution, spec, plan, tasks |
| [S1](labs/S1-member-post.md) | 회원과 게시글 | 역할과 TDD 분리 | researcher, planner, test-writer, implementer |
| [S2](labs/S2-follow.md) | 팔로우 | 규칙 위반의 결정적 차단 | import-linter, hooks, CI |
| [S3](labs/S3-feed.md) | 피드 | 실제 스키마를 최소 권한으로 조회 | read-only SQLite MCP |
| [S4](labs/S4-report.md) | 신고와 관리자 처리 | 작성자와 독립된 보안 검토 | security reviewer, CodeQL |
| [S5](labs/S5-package.md) | 팀 배포 | 하네스의 버전 관리와 재사용 | `ai-msft-harness`, marketplace |
| [S6](labs/S6-converge.md) | 완성도 확인 | 명세와 코드의 차이 제거 | verification, converge, human gate |

각 단계는 같은 패턴을 반복합니다.

```text
요건 읽기 → 하네스 없이 시도 → 실패 관찰 → 하네스 추가 → 재실행 → 검증
```

## 멀티 하네스 구조

![Reference application TeamFeed와 Spec Kit, 역할 에이전트, 품질 게이트의 관계](docs/images/teamfeed-architecture.svg)

하네스는 하나의 거대한 프롬프트가 아닙니다. 각 계층은 서로 다른 실패를
막습니다.

| 계층 | 책임 | 저장 위치 |
|---|---|---|
| Spec Kit artifacts | 의도, 범위, 수용 기준, 구현 작업 | `.specify/`, `specs/` |
| Instructions | 저장소 전체 또는 경로별 지속 규칙 | `.github/copilot-instructions.md`, `.github/instructions/` |
| Skills | 반복 가능한 작업 절차 | `.github/skills/` |
| Agents | 조사, 계획, 테스트, 구현, 리뷰의 역할 경계 | `.github/agents/` |
| Hooks | 위험 명령과 범위 밖 편집의 즉시 차단 | `.github/hooks/`, `scripts/hooks/` |
| MCP | DB와 GitHub 같은 외부 컨텍스트의 최소 권한 접근 | `.mcp.json`, `.vscode/mcp.json` |
| CI | 모든 기여자에게 동일한 공유 검증 | `.github/workflows/` |
| Convergence | 명세와 현재 구현의 남은 차이 탐지 | `speckit-converge` |

더 자세한 책임 경계는
[Multi-Harness Architecture](docs/multi-harness-architecture.md)를 참고하세요.

## Spec Kit 실행 흐름

Spec Kit은 요구사항을 코드로 바로 넘기지 않습니다. 사람이 검토할 수 있는
산출물을 단계별로 만들고, 구현 후 다시 수렴 여부를 확인합니다.

```text
constitution
    ↓
specify → clarify
    ↓
plan → tasks
    ↓
test-writer → implementer
    ↓
verify → independent review
    ↓
converge ── 남은 작업 있음 ──┐
    ↑                         │
    └──────── implement ──────┘
```

Copilot 세션에서 사용하는 기본 순서는 다음과 같습니다.

```text
/speckit-constitution
/speckit-specify
/speckit-clarify
/speckit-plan
/speckit-tasks
/speckit-implement
/speckit-converge
```

전체 과정을 human gate와 함께 실행하려면 설치된 workflow를 사용합니다.

```bash
specify workflow run teamfeed-delivery \
  --input spec="Build the next TeamFeed capability"
```

## 빠른 시작

### 1. 권장 환경

* GitHub Codespaces 또는 VS Code Dev Containers
* Python 3.12
* Node.js 22
* uv
* GitHub Copilot CLI 또는 VS Code Copilot Chat
* Spec Kit 1.2.5

Windows에서는 Bash hooks와 도구 버전 차이를 줄이기 위해 제공된 Dev
Container를 권장합니다.

### 2. 설치

```bash
git clone https://github.com/daeungo1/msft-ghcp-dev-workshop.git
cd msft-ghcp-dev-workshop
git switch main

uv tool install specify-cli --force \
  --from git+https://github.com/github/spec-kit.git@v1.2.5
uv sync --directory backend
npm --prefix frontend install
```

### 3. 준비 상태 확인

```bash
specify --version
specify integration status --json
python scripts/validate-harness.py
```

### 4. 앱 실행

```bash
bash scripts/dev.sh
```

* Frontend: `http://localhost:5173`
* Backend API: `http://localhost:8000`

> [!NOTE]
> `X-Member-Id`는 교육용 인증 방식입니다. 실제 계정이나 민감 데이터를
> 넣지 마세요.

## 역할과 모델 선택

저장소는 특정 모델을 필수로 지정하지 않습니다. 역할에 필요한 역량과
검증 비용을 기준으로 런타임에서 모델을 선택합니다.

| 역할 | 우선 역량 | 결과 검증 |
|---|---|---|
| Researcher | 긴 컨텍스트와 출처 추적 | 파일 경로와 공식 URL |
| Planner | 제약 통합과 작업 분해 | 요구사항과 작업의 추적성 |
| Test writer | 수용 기준의 정밀한 해석 | 예상 이유로 실패하는 테스트 |
| Implementer | 저장소 이해와 타입 안전성 | targeted와 full test |
| Reviewer | 독립 추론과 적대적 검토 | 파일과 줄 근거가 있는 findings |

작성자와 리뷰어는 가능하면 다른 모델 또는 최소한 새 컨텍스트를 사용합니다.
모델이 달라도 같은 테스트, 경계 검사, 보안 규칙, convergence gate를
통과해야 합니다.

> [!NOTE]
> HydraFusion은 이 저장소의 필수 기술이나 공식 지원 계약이 아닙니다.
> 멀티 모델 또는 fusion 접근을 설명할 때 참고 사례로만 다룹니다.

세부 기준은 [Capability-Based Model Routing](docs/model-routing.md)을
참고하세요.

## 저장소 구조

```text
backend/                    FastAPI, SQLAlchemy, SQLite
frontend/                   React, TypeScript, Vite
requirements/               단계별 요건과 수용 기준
specs/001-teamfeed-mvp/     기능 명세, 계획, 작업
.specify/                   Spec Kit 관리 파일과 설치 상태
.github/agents/             역할별 custom agents
.github/skills/             Spec Kit과 TeamFeed skills
.github/instructions/       저장소 및 경로별 규칙
.github/hooks/              Copilot hook 설정
spec-kit/extensions/        TeamFeed 품질 extension source
spec-kit/workflows/         human gate를 포함한 workflow source
spec-kit/bundles/           팀 배포 bundle source
plugins/ai-msft-harness/    VS Code와 Copilot CLI 설치용 최종 plugin
labs/                       S0-S6 실습
scripts/                    개발, hook, 구조 검증
```

## 실행과 검증

| 목적 | 명령 |
|---|---|
| 하네스 구조 | `python scripts/validate-harness.py` |
| 백엔드 테스트 | `cd backend && uv run pytest` |
| 패키지 경계 | `cd backend && uv run lint-imports` |
| 프론트엔드 테스트 | `cd frontend && npm test` |
| 프론트엔드 빌드 | `cd frontend && npm run build` |
| Hook fixtures | `bash scripts/hooks/test_hooks.sh` |
| 전체 워크숍 | `bash scripts/verify-step.sh ALL` |

품질 extension은 같은 검증 순서를
`/speckit-teamfeed-quality-verify` skill로 제공합니다. 로컬 Spec Kit 구성
설치 방법은 [Spec Kit Components](spec-kit/README.md)를 참고하세요.

## 플러그인 설치와 공유

### 현재 VS Code에 설치

Command Palette에서 **Chat: Install Plugin from Source**를 실행한 뒤
[`plugins/ai-msft-harness/`](plugins/ai-msft-harness/)의 절대 경로를
입력합니다. 설치 결과는 **Agent Customizations → Plugins**에서 확인합니다.

Copilot CLI 설치도 같은 사용자 plugin 저장소를 사용합니다.

```bash
copilot plugin install ./plugins/ai-msft-harness
copilot plugin list
```

### 다른 사용자에게 공유

현재 저장소는 marketplace catalog까지 포함합니다.

```bash
copilot plugin marketplace add daeungo1/msft-ghcp-dev-workshop
copilot plugin marketplace browse ai-msft-harness-marketplace
copilot plugin install ai-msft-harness@ai-msft-harness-marketplace
```

직접 설치도 가능합니다.

```bash
copilot plugin install \
  daeungo1/msft-ghcp-dev-workshop:plugins/ai-msft-harness
```

> [!NOTE]
> 다른 사용자가 설치하려면 [`marketplace.json`](.github/plugin/marketplace.json)과
> plugin 폴더가 원격 기본 브랜치에 push되어 있어야 합니다. 공개 저장소는
> 누구나 추가할 수 있고, 비공개 저장소는 사용자가 해당 저장소의 읽기
> 권한과 GitHub 로그인을 가져야 합니다.

## 버전과 브랜치

![v0.1 보존 브랜치와 현재 v0.2 main의 관계](docs/images/branch-map.svg)

* `main`: 현재 v0.2 기준선
* `main-v0.1`: 기존 v0.1 완성 상태 보존
* `s0-done`부터 `s5-done`: v0.1 단계별 정답
* `final`: v0.1 회고와 데모용 완성본
* `authoring`: 강사용 구성 이력

기존 체크포인트를 재작성하거나 force-push하지 않습니다. v0.2 단계별
체크포인트는 S0-S6 경로가 확정된 뒤 별도로 배포합니다.

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
