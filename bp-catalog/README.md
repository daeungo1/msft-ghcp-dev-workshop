---
title: BP 카탈로그
description: 업계 공통 하네스 패턴을 우리 팀 BP로 바꾸고 GitHub Copilot 기능으로 구현하는 매핑
---

## 원칙

트렌드 하네스는 설치하지 않고 패턴만 선별합니다. 선별한 패턴을 우리 팀 BP로 바꾸고, GitHub Copilot 위에서 강제되는 장치로 구현합니다.

| 업계 공통 패턴 | 우리 BP로 바꾼 규칙 | GHCP 구현 | 단계 | 출처 |
|---|---|---|---|---|
| 에이전트 행동 원칙 | 가정 말하기, 범위만 수정 | AGENTS.md | S0 | [^1] |
| 스펙 주도 개발 | constitution + spec/plan/tasks | spec-kit | S0 | [^2] |
| TDD 강제 | 테스트 커밋 먼저, 테스트 수정 금지 | 스킬 + 역할 분리 에이전트 | S1 | [^3] |
| 위험 명령 차단 | 파괴적 명령, 범위 밖 편집 거부 | preToolUse 훅 | S2 | [^4] |
| 결정적 경계 검사 | api.py 경유 import | import-linter + postToolUse 훅 + CI | S2 | [^4] |
| 최소 권한 도구 | DB는 읽기 전용 MCP로만 | 커스텀 MCP 서버 | S3 | [^5] |
| 작성자와 분리된 리뷰 | 인가 누락 = Critical | 읽기 전용 리뷰어 + rubber duck | S4 | [^6] |
| 결정적 보안 스캔 | 원시 SQL 금지 | CodeQL | S4 | [^7] |
| 팀 자산 배포 | 검증된 것만 배포 | Agent Plugins + 사내 marketplace | S5 | [^8] |

## 하네스를 들이는 세 가지 방법

1. 공식 하네스 설치: spec-kit (S0)
2. 카탈로그에서 골라 고치기: awesome-copilot의 에이전트·스킬을 우리 규칙으로 수정 (S1, S4, S5)
3. 업계 패턴은 원칙만 흡수: constitution, 훅, 리뷰어 에이전트로 이전 (설치 없음)

[^1]: 커뮤니티 에이전트 행동 원칙 모음
[^2]: [github/spec-kit](https://github.com/github/spec-kit)
[^3]: 여러 TDD 스킬 하네스, [github/awesome-copilot](https://github.com/github/awesome-copilot)
[^4]: 훅 기반 가드레일 하네스, [GitHub Docs: Hooks](https://docs.github.com/en/copilot/concepts/agents/hooks)
[^5]: MCP 보안 권고
[^6]: 2축 리뷰 패턴, [microsoft/hve-core](https://github.com/microsoft/hve-core)
[^7]: GitHub Code Security
[^8]: [GitHub Docs: Plugins](https://docs.github.com/en/copilot/concepts/agents/about-plugins)
