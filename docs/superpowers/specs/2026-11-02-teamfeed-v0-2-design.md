---
title: TeamFeed Workshop v0.2 Design
description: Spec Kit 1.2.5 기반 멀티 에이전트와 다층 하네스 워크숍 재구성 설계
ms.date: 2026-11-02
ms.topic: concept
---

# TeamFeed Workshop v0.2 Design

## Intent

TeamFeed v0.2는 기존 애플리케이션 도메인을 유지하면서 워크숍의 중심을
"기능을 단계별로 구현하기"에서 "명세부터 검증과 패키징까지 재현 가능한
에이전트 개발 하네스를 설계하기"로 옮긴다.

완성된 v0.1은 `main-v0.1` 브랜치에 보존한다. 새 `main`은 Spec Kit 1.2.5의
공식 Copilot integration과 extension, preset, workflow, bundle, converge
개념을 반영한 v0.2 기준선이 된다.

## Goals

* Spec Kit 1.2.5의 공식 SDD 흐름을 저장소의 기본 개발 흐름으로 사용한다.
* 역할이 분리된 에이전트가 명세, 테스트, 구현, 리뷰를 독립적으로 수행한다.
* instructions, skills, agents, hooks, MCP, CI를 서로 다른 하네스 계층으로
  설명하고 검증한다.
* 팀 구성을 Spec Kit bundle과 workflow로 재사용할 수 있는 소스로 제공한다.
* 모델 이름보다 역할과 검증 계약을 우선하는 멀티 모델 전략을 제시한다.
* 기존 TeamFeed 테스트와 패키지 경계 규칙을 유지한다.

## Non-goals

* 비공개 또는 문서화되지 않은 모델을 필수 런타임으로 요구하지 않는다.
* 하나의 모델이 항상 특정 역할을 수행한다고 가정하지 않는다.
* Spec Kit upstream 소스를 저장소 안에 복제하지 않는다.
* TeamFeed의 실제 인증, 운영 배포, 이미지 업로드 범위를 추가하지 않는다.
* v0.1의 단계별 브랜치 기록을 재작성하지 않는다.

## Anti-goals

* 프롬프트 파일만 많이 추가하고 각 파일의 책임과 검증 기준이 겹치는 구성
* 모델 선택 실패를 숨기거나 다른 모델로 조용히 대체하는 구성
* MCP 서버에 불필요한 쓰기 권한을 부여하는 구성
* 생성된 Spec Kit 파일과 프로젝트 소유 파일을 구분하지 않는 구성
* 문서에서만 동작하고 자동 검증할 수 없는 워크숍

## Research baseline

2026-11-02 기준 공식 `github/spec-kit` 최신 릴리스는 `v1.2.5`다. 공식
문서는 다음 기능을 핵심 구성 요소로 설명한다.

* Copilot을 포함한 coding agent integrations
* 명령과 품질 게이트를 추가하는 extensions
* 템플릿과 방법론을 조정하는 presets
* 조건, 반복, fan-out과 fan-in, 사람 승인을 지원하는 workflows
* 팀 구성을 배포하는 bundles
* 설치 파일의 출처를 확인하는 artifact inventory
* 구현과 명세의 수렴 여부를 확인하는 `speckit-converge`

공식 GitHub와 Microsoft 자료에서는 "GitHub Copilot HydraFusion"을 제품이나
공개 모델 계약으로 확인할 수 없었다. 공개 검색 결과의 HydraFusion은
센서 융합 연구 프로젝트를 가리킨다. 따라서 HydraFusion을 실험적으로 사용할
수는 있지만 저장소의 필수 frontmatter, CI, 검증 명령에는 포함하지 않는다.

## Approaches

### In-place tool upgrade

기존 S0-S5 교육 흐름을 유지하고 Spec Kit 생성 파일만 1.2.5로 갱신한다.
변경 위험은 낮지만 extension, workflow, bundle, converge를 실습의 핵심으로
만들기 어렵다.

### Full replacement

TeamFeed와 기존 교육 자료를 모두 제거하고 새로운 멀티 에이전트 예제로
시작한다. 최신 기능을 자유롭게 구성할 수 있지만 검증된 도메인, 테스트,
강의 자료를 잃는다.

### Versioned rebuild

완성된 v0.1을 보존하고 TeamFeed를 안정된 실습 도메인으로 재사용한다. 새
버전은 Spec Kit 1.2.5와 다층 하네스를 중심으로 워크숍을 다시 구성한다.
기존 테스트가 회귀 기준으로 남고, 새 교육 목표를 충분히 반영할 수 있다.

선택한 방식은 versioned rebuild다.

## Target architecture

```text
Participant request
        |
        v
Spec Kit SDD
constitution -> specify -> clarify -> plan -> tasks
        |
        v
Role routing
researcher -> test-writer -> implementer -> reviewer
        |
        v
Harness layers
instructions -> skills -> agents -> hooks -> MCP -> CI
        |
        v
Convergence
tests + boundaries + security + speckit-converge
        |
        v
Distribution
extension + workflow + bundle
```

## Harness boundaries

Repository instructions contain stable contributor-wide rules. Path-specific
instructions narrow those rules for Python tests, backend code, frontend code,
and security-sensitive code.

Skills provide repeatable task procedures. Agents own bounded roles and may
load skills, but do not duplicate their contents.

Hooks enforce fast local guardrails. They block destructive Git commands and
run targeted checks after edits. CI remains the authoritative shared gate.

MCP is context access, not an authority bypass. The SQLite server remains
read-only. GitHub access uses the minimum operation set needed by the exercise.

Spec Kit workflow files orchestrate steps and human gates. Bundle manifests
package approved extensions, presets, workflows, and steps without embedding
model-specific behavior.

## Model routing

The default configuration stays model-neutral. Participants choose models at
runtime according to role requirements:

| Role | Required capability | Primary verification |
|---|---|---|
| Research | Long context and source citation | Source links and evidence log |
| Planning | Constraint synthesis and decomposition | Requirement-to-task mapping |
| Test writing | Precise acceptance-criteria translation | Expected failing test |
| Implementation | Repository-aware code generation | Targeted and full tests |
| Review | Independent reasoning and adversarial checks | Findings with file evidence |

Experimental fusion or ensemble models can be selected for planning and review
when the client exposes them. The workflow must still succeed with any supported
Copilot model that satisfies the role capability.

## Version and branch policy

* `main-v0.1` points to the completed v0.1 `final` commit.
* Existing `s0-done` through `s5-done` branches remain unchanged.
* `main` becomes the v0.2 development line.
* No remote branches are rewritten or force-pushed.
* A future v0.2 release can introduce new checkpoint branches after the new
  learning path is validated end to end.

## Validation

The repository is ready when all of the following hold:

* Spec Kit reports the Copilot integration and installed component inventory.
* Every custom agent and skill has valid frontmatter and a unique responsibility.
* Harness validation detects missing required layers and undocumented hardcoded
  model names.
* Backend tests and import boundary checks pass.
* Frontend tests and production build pass.
* Hook tests pass.
* The workshop verification script passes for the v0.2 baseline.

## Sources

* [Spec Kit repository](https://github.com/github/spec-kit)
* [Spec Kit v1.2.5 release](https://github.com/github/spec-kit/releases/tag/v1.2.5)
* [Spec Kit README](https://github.com/github/spec-kit/blob/v1.2.5/README.md)
* [Spec Kit upgrade guide](https://github.github.io/spec-kit/upgrade.html)
* [Spec Kit extensions](https://github.github.io/spec-kit/reference/extensions.html)
* [Spec Kit workflows](https://github.github.io/spec-kit/reference/workflows.html)
* [Spec Kit bundles](https://github.github.io/spec-kit/reference/bundles.html)
* [GitHub Copilot agent skills](https://docs.github.com/en/copilot/concepts/customizations/agent-skills)
* [GitHub Copilot MCP configuration](https://docs.github.com/en/copilot/how-tos/copilot-in-your-ide/customize-copilot/extend-copilot-with-tools-and-context/extend-copilot-chat-with-mcp)

