---
title: AI SW Factory MSFT KO Plugin
description: Spec Kit 기반 애플리케이션 개발 절차를 GitHub Copilot에 설치하는 Agent Plugins 1.0 패키지
ms.date: 2026-11-04
ms.topic: reference
---

## AI SW Factory MSFT KO

`ai-sw-factory-msft-ko`는 팀이나 프로젝트의 개발 패턴을 GitHub Copilot에서
반복할 수 있도록 묶은 Agent Plugins 1.0 패키지입니다.

TeamFeed 워크숍은 이 플러그인을 만드는 과정을 Spec Kit의 표준 애플리케이션
개발 단계로 설명합니다.

### Spec Kit composition

이 plugin은 Spec Kit fork가 아니라 team overlay입니다.

* Spec Kit core: constitution, specify, clarify, plan, tasks, implement, converge
* Plugin: team tech-stack, Clean Architecture, role agents, TDD, hooks, MCP
* Project: constitution, specs, instructions, `.ai-sw-factory-msft-ko/post-edit.py`

Target repository에 `.specify/`가 없으면 먼저 초기화합니다.

```bash
uv tool install specify-cli --force \
  --from git+https://github.com/github/spec-kit.git@v1.2.5
specify init --here --force --integration copilot
```

```text
constitution → specify → clarify → plan → tasks
       ↓
research → failing tests → implementation → independent review
       ↓
verify → converge → reusable plugin
```

### 포함 구성

| 유형 | 구성 |
|---|---|
| Skills | spec-driven-delivery, team-application-standards, evidence-research, tdd, convergence-check, pr-description |
| Agents | researcher, planner, test-writer, implementer, security-reviewer, convergence-reviewer |
| Hooks | 파괴적 명령 차단, 프로젝트별 post-edit 검증 연결 |
| MCP | 선택형 read-only SQLite 스키마 및 조회 도구 |

### 팀 기본 개발 패턴

`team-application-standards` skill은 다음 값을 구체적인 기본 계약으로
제공합니다.

* `Node.js >=22`, 신규 서비스는 승인된 최신 supported LTS 우선
* `Python >=3.12`, 신규 서비스는 승인된 latest bugfix-supported version 우선
* Business module/service 기준 분리
* `Adapters → Application Use Cases → Core` dependency direction
* Ports를 통한 DB, queue, external API 추상화
* One module/service or one use case 단위 incremental refactoring
* Legacy modernization의 Strangler Fig approach
* 여러 external resources를 위한 optional registry/adapter architecture shape
* Python import-linter와 TypeScript dependency boundary automation

### VS Code에 로컬 설치

1. Command Palette에서 **Chat: Install Plugin from Source**를 실행합니다.
2. 이 폴더의 절대 경로를 입력합니다.

```text
<repository>/plugins/ai-sw-factory-msft-ko
```

설치 후 **Agent Customizations → Plugins**에서 `ai-sw-factory-msft-ko`를 활성화합니다.

Copilot CLI를 사용하면 같은 사용자 plugin 저장소에 설치할 수 있습니다.

```bash
copilot plugin install ./plugins/ai-sw-factory-msft-ko
copilot plugin list
```

### GitHub 저장소에서 직접 설치

이 저장소가 원격 `main`에 공개된 뒤에는 Copilot CLI에서 repository
subdirectory를 직접 지정할 수 있습니다.

```bash
copilot plugin install \
  daeungo1/msft-ghcp-dev-workshop:plugins/ai-sw-factory-msft-ko
```

### Marketplace로 설치

```bash
copilot plugin marketplace add daeungo1/msft-ghcp-dev-workshop
copilot plugin marketplace browse ai-sw-factory-msft-ko-marketplace
copilot plugin install ai-sw-factory-msft-ko@ai-sw-factory-msft-ko-marketplace
```

VS Code에서는 **Chat: Manage Plugin Marketplaces**로 같은 저장소를 추가한 뒤
**Customize** 화면에서 `ai-sw-factory-msft-ko`를 검색해 설치할 수 있습니다.

### 프로젝트별 맞춤 검사

플러그인의 post-edit hook은 프로젝트 루트에 아래 스크립트가 있을 때만
실행합니다.

```text
.ai-sw-factory-msft-ko/post-edit.py
```

팀은 이 Python 스크립트에 자체 lint, test, architecture boundary 명령을
넣습니다.
종료 코드가 0이 아니면 Copilot에 실패 내용이 돌아가며 완료 보고 전에
수정하도록 요구합니다.

### 선택형 SQLite MCP

SQLite 조회가 필요한 프로젝트에서 DB 경로를 지정합니다.

```bash
export AI_SW_FACTORY_MSFT_KO_DB=/absolute/path/to/application.db
```

서버는 `list_tables`, `describe_table`, `query`를 제공하며 `SELECT`와
`WITH`만 허용합니다.

### 배포 전제

Marketplace 설치는 catalog와 plugin 폴더가 원격 기본 브랜치에 있어야
동작합니다. 현재 로컬 변경만으로는 다른 사용자가 설치할 수 없으므로
검증 후 저장소에 push하거나 별도 marketplace repository로 배포해야 합니다.

### Migration from the previous plugin ID

Plugin package identity가 변경됐으므로 in-place update가 아니라 재설치합니다.

```bash
copilot plugin list
# Marketplace install인 경우
copilot plugin uninstall ai-msft-harness@ai-msft-harness-marketplace
copilot plugin marketplace remove ai-msft-harness-marketplace --force
# Direct GitHub 또는 local-path install인 경우
copilot plugin uninstall ai-msft-harness

copilot plugin marketplace add daeungo1/msft-ghcp-dev-workshop
copilot plugin install \
  ai-sw-factory-msft-ko@ai-sw-factory-msft-ko-marketplace
```

`copilot plugin list`의 `marketplace` 값이 있으면 qualified ID를, 비어 있으면
unqualified old plugin ID를 제거합니다. 두 방식이 모두 설치되어 있으면 두
uninstall 명령을 모두 실행합니다.

기존 session은 uninstall 전 hook command를 메모리에 유지할 수 있습니다.
Migration 후 VS Code에서 **Developer: Reload Window**를 실행하고 새 Copilot
session을 시작합니다.

새 hook config는 plugin path가 이미 제거됐으면 `{}`를 반환해 normal
permission flow로 넘기므로 uninstall/rename 중 stale path가 작업을 차단하지
않습니다.
