---
title: 완성본 둘러보기
description: final 브랜치에 쌓인 하네스 구조, 단계별 자산, 막은 함정, 마켓플레이스 등록, 채워 둔 자가진단 카드 예시
---

이 문서는 `final` 브랜치(태그 `v1.0`) 기준입니다. 실습 중에는 막혔을 때 정답 확인용으로, 실습 후에는 복사해 가져갈 목록으로 씁니다.

## 하네스 구조

```text
.
├─ AGENTS.md                         # 맥락: 에이전트용 README (S0)
├─ .specify/memory/constitution.md   # 맥락: 원칙 6개 (S0)
├─ specs/001-teamfeed-mvp/           # 맥락: spec, plan, tasks (S0)
├─ .github/
│  ├─ copilot-instructions.md        # 맥락: 저장소 전체 규칙 (S0)
│  ├─ instructions/                  # 맥락: 경로별 규칙 (S1 python-tests, S4 security)
│  ├─ skills/tdd/                    # 도구: 테스트 먼저 절차 (S1)
│  ├─ agents/                        # 흐름: test-writer, implementer (S1), security-reviewer (S4)
│  ├─ hooks/guardrails.json          # 피드백/강제: pre·postToolUse 훅 (S2)
│  └─ workflows/                     # 피드백/강제: ci.yml (S2), codeql.yml (S4)
├─ scripts/hooks/                    # 훅 본체와 테스트 (S2)
├─ backend/pyproject.toml            # 강제: import-linter 계약 (S2~S4)
├─ .vscode/mcp.json, .mcp.json       # 도구: 읽기 전용 SQLite MCP (S3)
├─ plugins/teamfeed-harness/         # 배포: 위 자산을 묶은 플러그인 (S5)
└─ .github/plugin/marketplace.json   # 배포: 플러그인 마켓플레이스 (S5)
```

## 단계별 하네스 목록

| 단계 | 추가된 자산 | 통제 방식 |
|---|---|---|
| S0 | constitution, copilot-instructions.md, AGENTS.md, spec/plan/tasks | 안내 |
| S1 | `tdd` 스킬, `test-writer`·`implementer` 에이전트, `python-tests` 인스트럭션 | 안내 + 역할 분리 |
| S2 | import-linter 계약, `guardrails.json` 훅, CI | 강제 |
| S3 | 읽기 전용 SQLite MCP, 피드 계약 | 도구 범위 제한 |
| S4 | `security-reviewer` 에이전트, `security` 인스트럭션, CodeQL | 독립 리뷰 |
| S5 | `teamfeed-harness` 플러그인, 팀 규칙 스킬 | 재사용 |

## 막은 함정 요약

| 단계 | 함정 | 막은 장치 | 확인 방법 |
|---|---|---|---|
| S1 | 테스트 없이 완료 보고 | `tdd` 스킬, 에이전트 역할 분리 | 테스트 커밋이 구현 커밋보다 앞섬 |
| S2 | 팔로우 구현이 `members.repository`를 직접 import | import-linter 계약, CI | `cd backend && uv run lint-imports` |
| S2 | 위험한 명령과 보호 파일 편집 | preToolUse 훅 | `scripts/hooks/test_hooks.sh` |
| S3 | 스키마를 추측한 쿼리 | 읽기 전용 SQLite MCP | MCP로 스키마를 조회한 뒤 쿼리 |
| S4 | 관리자 신고 처리에 인가 누락 | `security-reviewer`, 관리자가 아닌 회원으로 호출하는 403 테스트 | 권한 없는 호출이 403 |

## 마켓플레이스에서 설치

이 저장소는 로컬 마켓플레이스입니다. 저장소 루트에서 실행합니다.

```bash
copilot plugin marketplace add .
copilot plugin install teamfeed-harness@teamfeed-marketplace
copilot plugin list
```

팀 공용으로 쓰려면 플러그인 디렉터리를 별도 저장소로 옮기고, `.github/plugin/marketplace.json`을 가진 마켓플레이스 저장소를 `copilot plugin marketplace add <owner>/<repo>`로 등록합니다.

## 자가진단 카드 작성 예시

| 축 | 우리 팀에서 가장 자주 새는 곳 | 그 자리에 둘 강제 1개 |
|---|---|---|
| 요구·명세 | 모호한 요구를 에이전트가 가정만 하고 구현 | spec의 수용 기준을 테스트로 옮기는 `tdd` 스킬과 PR 체크리스트 |
| 설계·경계 | 다른 패키지의 repository 직접 import | import-linter 계약 + CI 게이트 |
| 테스트·검증 | 테스트를 약하게 고쳐 통과시킴 | `tdd` 스킬의 테스트 선커밋 규칙과 CI |
| 보안·리뷰 | 관리자 기능의 서버 인가 누락 | 읽기 전용 `security-reviewer` + CodeQL + Copilot code review |
| 배포·운영 | `rm -rf`, force push | preToolUse 훅 |

빈 카드는 [templates/self-check-card.md](../templates/self-check-card.md)에 있습니다.