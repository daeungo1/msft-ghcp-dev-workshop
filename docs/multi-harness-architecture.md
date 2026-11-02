---
title: TeamFeed Multi-Harness Architecture
description: TeamFeed v0.2의 Spec Kit, Copilot customization, MCP, hooks, CI 책임 경계
ms.date: 2026-11-02
ms.topic: concept
---

## Architecture

TeamFeed v0.2는 하나의 긴 프롬프트 대신 서로 다른 실패 모드를 담당하는
하네스 계층을 조합합니다.

```text
Intent       constitution, spec, plan, tasks
Procedure    skills
Role         agents
Policy       instructions
Guard        hooks
Context      MCP
Shared gate  CI
Closure      converge
Distribution extension, workflow, bundle
```

## Responsibility boundaries

### Spec Kit artifacts

Constitution은 모든 기능에 적용되는 원칙을 정의합니다. Feature spec은
사용자 시나리오와 수용 기준, plan은 기술 선택과 경계, tasks는 실행 순서를
담습니다.

Spec Kit 관리 파일과 프로젝트 소유 파일을 구분합니다.

* `.specify/integrations/`와 `.github/skills/speckit-*`는 integration이 관리
* `.specify/memory/constitution.md`와 `specs/`는 프로젝트가 소유
* integration upgrade는 프로젝트 소유 파일을 덮어쓰지 않음

### Instructions

Repository instruction은 모든 작업에 필요한 규칙만 담습니다. Backend,
frontend, tests처럼 범위가 좁은 규칙은 path-specific instruction에 둡니다.
같은 규칙을 global instruction과 skill에 복사하지 않습니다.

### Skills

Skill은 TDD, 조사, 수렴 검사처럼 반복 가능한 절차입니다. Skill은 역할을
선택하지 않고 선택된 역할이 어떻게 작업할지를 정의합니다.

### Agents

Agent는 조사, 계획, 테스트, 구현, 리뷰의 쓰기 권한을 분리합니다.

* researcher와 reviewer는 제품 코드를 수정하지 않음
* test-writer는 테스트만 수정
* implementer는 커밋된 실패 테스트를 변경하지 않음
* planner는 plan과 tasks를 작성하지만 구현하지 않음

### Hooks and CI

Hook은 파괴적 명령과 범위 밖 편집을 빠르게 차단합니다. CI는 동일한 테스트,
경계 검사, 보안 검사를 모든 기여자에게 적용합니다. Hook 성공은 CI 성공을
대체하지 않습니다.

### MCP

MCP는 에이전트에 컨텍스트와 도구를 제공합니다. SQLite 서버는 스키마와
데이터를 읽을 수 있지만 쓰기 쿼리를 거부합니다. GitHub MCP 권한은 실습에
필요한 작업만 허용합니다.

### Convergence

`speckit-converge`는 체크박스를 신뢰하지 않고 spec, plan, tasks,
constitution을 현재 코드와 대조합니다. 남은 차이는 append-only convergence
tasks로 기록하고 다시 구현합니다.

## Distribution

TeamFeed 품질 검사는 extension command로 제공됩니다. Delivery workflow는
Spec Kit core commands, human gates, 품질 extension, convergence를 순서대로
실행합니다. Bundle은 승인된 component 버전을 하나의 팀 구성으로 고정합니다.

Source와 installed state를 모두 둡니다.

* `spec-kit/`은 검토하고 배포하는 source
* `.specify/extensions/`와 `.specify/workflows/`는 현재 프로젝트 설치 상태
* `.github/skills/speckit-teamfeed-quality-verify/`는 Copilot invocation

## Failure visibility

모든 계층은 실패를 명시적으로 보고합니다.

* 없는 도구를 성공으로 간주하지 않음
* 실행하지 않은 테스트를 통과로 보고하지 않음
* 선택형 모델 부재를 조용히 대체하지 않음
* MCP 쓰기 거부를 빈 성공 응답으로 바꾸지 않음
* partial workflow run을 전체 성공으로 표시하지 않음

