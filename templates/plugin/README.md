---
title: 팀 플러그인 골격
description: S5에서 저장소의 하네스를 Agent Plugins 1.0 형식의 팀 플러그인으로 묶을 때 쓰는 골격과 배치 규칙
---

Copilot CLI는 `plugin.json`에 `$schema`를 선언하면 Agent Plugins 1.0 형식으로 읽습니다.
스킬과 MCP 설정은 이식 가능한 표준 위치에, Copilot 전용 자산(에이전트, 훅)은 `com.github.copilot/` 아래에 둡니다.

## 만들어야 하는 구조

```text
plugins/ai-sw-factory-msft-ko/
├── plugin.json                       # Agent Plugins 1.0 manifest
├── README.md                         # 설치, 공유, 프로젝트별 맞춤 방법
├── skills/
│   ├── spec-driven-delivery/SKILL.md
│   ├── team-application-standards/     # SKILL.md와 references/를 함께 복사
│   ├── evidence-research/SKILL.md
│   ├── tdd/SKILL.md
│   ├── convergence-check/SKILL.md
│   └── pr-description/SKILL.md
├── mcp.json                          # templates/plugin/mcp.json 복사
├── mcp/sqlite-ro-server/             # templates/plugin/mcp/sqlite-ro-server 복사
└── com.github.copilot/
    ├── agents/
    │   ├── researcher.agent.md
    │   ├── planner.agent.md
    │   ├── test-writer.agent.md
    │   ├── implementer.agent.md
    │   ├── security-reviewer.agent.md
    │   └── convergence-reviewer.agent.md
    └── hooks/
        ├── hooks.json                # templates/plugin/hooks.json 복사
        ├── pre_tool_guard.py          # 이식 가능한 pre-tool 정책
        └── post_edit_check.py         # 프로젝트별 검증 연결
```

## 파일별 메모

| 파일 | 메모 |
|---|---|
| `plugin.json` | 허용 필드는 `$schema`, `name`, `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords`, `extensions` 뿐입니다. 그 밖의 필드는 무시됩니다 |
| `mcp.json` | stdio 서버의 `type`은 `stdio`입니다. `${PLUGIN_ROOT}`와 `${PLUGIN_DATA}`는 런타임이 확장합니다. SQLite를 쓰려면 `AI_SW_FACTORY_MSFT_KO_DB`를 지정합니다 |
| `hooks.json` | 훅 스크립트 경로는 `${PLUGIN_ROOT}` 기준입니다. 프로젝트별 검사는 `.ai-sw-factory-msft-ko/post-edit.py`가 담당합니다 |

`team-application-standards/references/application-profile.md`에는
기술 선택과 production 요구사항 결정표가 있습니다. 기존 stack과 작은 앱의
도메인 파일 구조를 유지하고 필요한 architecture 추출만 계획합니다.

Post-edit 스크립트가 없으면 hook은 `not configured`를, 있으면 설정된
검사의 성공/실패를 반환합니다. 설정 예제와 client 로딩 확인 절차는
[완성 plugin 안내](../../plugins/ai-sw-factory-msft-ko/README.md#프로젝트별-맞춤-검사)를
따릅니다. Hook context는 CI를 대체하는 강제 차단이 아닙니다.

## 설치와 확인

```bash
copilot plugin install ./plugins/ai-sw-factory-msft-ko   # 로컬 설치 (수정 후에는 다시 실행해 캐시 갱신)
copilot plugin list
```

Copilot CLI 세션에서 `/plugin list`, `/agent`, `/skills list`로 로드된 자산을 확인합니다.
