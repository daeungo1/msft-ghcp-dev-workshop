---
title: 하네스 개념 정리
description: 실습 전에 읽는 10분 개념 문서. 하네스 네 계층, 안내와 강제의 차이, GitHub Copilot 기능 매핑, 용어집
---

## 왜 하네스인가

AI 코딩 에이전트를 도입해도 개발 속도가 기대만큼 오르지 않는 가장 큰 이유는 에이전트가 우리 팀의 방식을 모르거나, 알아도 가끔 어기기 때문입니다.
코드는 빨라졌지만 리뷰, 테스트, 보안 검토에서 사람이 다시 걸러내야 하니 병목이 뒤로 옮겨갑니다.

하네스는 이 문제를 에이전트 바깥에서 푸는 접근입니다. 모델을 바꾸는 대신 모델이 일하는 환경을 설계합니다.

## 하네스 네 계층

| 계층 | 질문 | GitHub Copilot 기능 |
|---|---|---|
| Context | 에이전트가 무엇을 읽고 일하나 | `.github/copilot-instructions.md`, `AGENTS.md`, `.github/instructions/*.instructions.md`, 스킬(`.github/skills/*/SKILL.md`), spec-kit의 constitution과 spec |
| Tools | 에이전트가 무엇을 할 수 있나 | 커스텀 에이전트(`.github/agents/*.agent.md`의 `tools`), MCP 서버 |
| Control Flow | 어떤 순서로, 어디까지 하나 | 역할 분리 에이전트, 훅(`.github/hooks/*.json`), 계획 후 구현 흐름 |
| Feedback | 잘했는지 누가 확인하나 | 테스트, 린터, import-linter, CI, CodeQL, 리뷰어 에이전트, Copilot code review |

## 안내와 강제

같은 규칙이라도 어디에 두느냐에 따라 지켜지는 확률이 달라집니다.

| 구분 | 예 | 성격 | 새는 경우 |
|---|---|---|---|
| 안내 | 인스트럭션, 스킬, 에이전트 설명 | 확률적. 모델이 읽고 따르기를 기대 | 컨텍스트가 길어지거나 다른 지시와 충돌하면 무시됨 |
| 강제 | 훅, 테스트, import-linter, CI, 리뷰 게이트 | 결정적. 위반하면 실행이 거부되거나 실패 | 규칙 자체를 안 만든 경우뿐 |

경험칙은 다음과 같습니다.

* 어겨도 리뷰에서 잡히면 안내(스킬, 인스트럭션)로 충분합니다.
* 한 번 새면 비용이 큰 규칙(경계 위반, 비밀 유출, 파괴적 명령, 인가 누락)은 강제로 올립니다.
* 강제는 사람이 아니라 스크립트가 판정합니다. 에이전트가 우회할 수 없는 위치(루프 경계)에 둡니다.

## 하네스 자산 한눈에 보기

| 자산 | 파일 위치 | 한 줄 설명 | 실습 |
|---|---|---|---|
| constitution | `.specify/memory/constitution.md` | 프로젝트가 지킬 원칙. spec-kit이 모든 단계에서 참조 | S0 |
| 커스텀 인스트럭션 | `.github/copilot-instructions.md` | 모든 요청에 자동으로 붙는 저장소 전체 규칙 | S0 |
| AGENTS.md | 저장소 루트 | 에이전트용 README. 빌드, 테스트 명령과 작업 원칙 | S0 |
| 스킬 | `.github/skills/<name>/SKILL.md` | 필요할 때 불러오는 절차와 체크리스트 | S1 |
| 커스텀 에이전트 | `.github/agents/<name>.agent.md` | 역할, 도구 범위, 지침을 가진 전문 에이전트 | S1, S4 |
| 훅 | `.github/hooks/*.json` + 스크립트 | 도구 실행 전후에 끼어드는 결정적 검사 | S2 |
| MCP 서버 | `.vscode/mcp.json`, `.mcp.json` | 에이전트에 외부 도구를 연결 | S3 |
| 플러그인 | `plugins/<name>/plugin.json` | 위 자산을 묶어 다른 저장소에 설치 | S5 |

## 하네스를 들이는 세 가지 방법

1. 공식 하네스를 설치합니다. spec-kit이 대표적입니다 (S0).
2. 카탈로그에서 고르고 우리 규칙으로 고칩니다. awesome-copilot의 에이전트와 스킬이 출발점입니다 (S1, S4, S5).
3. 업계 패턴은 원칙만 흡수합니다. 설치하지 않고 constitution, 훅, 리뷰어 에이전트로 옮깁니다.

업계 공통 패턴과 우리 BP, GitHub Copilot 구현의 매핑은 [bp-catalog](../bp-catalog/README.md)에 있습니다.

## 계획, 리서치, 구현을 나누는 이유 (세션 1~2 연결)

hve-core의 핵심은 AI는 규칙을 따르고 사람은 판단하는 단계 분리입니다. 이 워크샵에서는 다음과 같이 대응합니다.

| 분리된 단계 | 하는 일 | 이 워크샵 |
|---|---|---|
| 명세 | 무엇을 만들지 정함 | S0 `/speckit-specify` |
| 계획 | 어떻게 만들지 정함 | S0 `/speckit-plan`, `/speckit-tasks` |
| 구현 | 테스트 먼저, 그다음 코드 | S1 `test-writer`, `implementer` |
| 검증 | 작성자와 다른 눈으로 확인 | S4 `security-reviewer`, rubber duck |

## 공식 문서 기준 사실 확인 메모

이 저장소의 명령과 파일 형식은 GitHub Docs와 spec-kit 공식 저장소를 기준으로 작성했습니다. 기능이 빠르게 바뀌므로 어긋나면 문서를 우선하세요.

* 훅 설정은 `.github/hooks/*.json`에 `"version": 1`과 이벤트별 배열로 둡니다. 스크립트는 stdin으로 JSON을 받고, `preToolUse`는 stdout으로 `permissionDecision`을 돌려줍니다.
* 플러그인은 `plugin.json`에 `$schema`를 선언하는 Agent Plugins 1.0 형식으로 만듭니다. 발표 자료의 "Agent Plugin v2"와 같은 대상을 가리킵니다.
* Copilot CLI의 프로젝트 MCP 설정은 저장소 루트의 `.mcp.json` 또는 `.github/mcp.json`입니다. VS Code는 `.vscode/mcp.json`을 씁니다.

## 용어집

| 용어 | 뜻 |
|---|---|
| 하네스 | 에이전트를 감싸는 맥락, 도구, 흐름 제어, 피드백 장치의 묶음 |
| 인스트럭션 | 요청에 자동으로 붙는 규칙 문서 |
| 스킬 | 필요할 때 에이전트가 불러 쓰는 절차 묶음 (SKILL.md와 보조 파일) |
| 커스텀 에이전트 | 역할, 도구, 지침이 정해진 전문 에이전트 (`*.agent.md`) |
| 훅 | 에이전트가 도구를 실행하기 전후에 호출되는 사용자 스크립트 |
| MCP | 에이전트에 외부 도구와 데이터를 연결하는 표준 프로토콜 |
| spec-kit | 명세에서 계획, 작업, 구현까지 이어지는 스펙 주도 개발 도구 |
| constitution | spec-kit에서 프로젝트 원칙을 적는 문서 |
| import-linter | 파이썬 패키지 간 import 경계를 계약으로 검사하는 도구 |
| rubber duck | Copilot CLI에 내장된, 다른 모델의 눈으로 계획과 구현을 비평하는 에이전트 |
| 플러그인 | 스킬, 에이전트, 훅, MCP 설정을 묶어 설치하는 배포 단위 |
| marketplace | 플러그인 목록을 모아 두는 저장소. `copilot plugin marketplace add`로 등록 |
