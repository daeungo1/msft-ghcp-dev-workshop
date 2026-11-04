---
title: AI MSFT Harness Plugin
description: Spec Kit 기반 애플리케이션 개발 절차를 GitHub Copilot에 설치하는 Agent Plugins 1.0 패키지
ms.date: 2026-11-04
ms.topic: reference
---

## AI MSFT Harness

`ai-msft-harness`는 팀이나 프로젝트의 개발 패턴을 GitHub Copilot에서
반복할 수 있도록 묶은 Agent Plugins 1.0 패키지입니다.

TeamFeed 워크숍은 이 플러그인을 만드는 과정을 Spec Kit의 표준 애플리케이션
개발 단계로 설명합니다.

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
* Manifest-driven resource registry와 HTTP/MCP/Database adapters
* Python import-linter와 TypeScript dependency boundary automation

### VS Code에 로컬 설치

1. Command Palette에서 **Chat: Install Plugin from Source**를 실행합니다.
2. 이 폴더의 절대 경로를 입력합니다.

```text
<repository>/plugins/ai-msft-harness
```

설치 후 **Agent Customizations → Plugins**에서 `ai-msft-harness`를 활성화합니다.

Copilot CLI를 사용하면 같은 사용자 plugin 저장소에 설치할 수 있습니다.

```bash
copilot plugin install ./plugins/ai-msft-harness
copilot plugin list
```

### GitHub 저장소에서 직접 설치

이 저장소가 원격 `main`에 공개된 뒤에는 Copilot CLI에서 repository
subdirectory를 직접 지정할 수 있습니다.

```bash
copilot plugin install \
  daeungo1/msft-ghcp-dev-workshop:plugins/ai-msft-harness
```

### Marketplace로 설치

```bash
copilot plugin marketplace add daeungo1/msft-ghcp-dev-workshop
copilot plugin marketplace browse ai-msft-harness-marketplace
copilot plugin install ai-msft-harness@ai-msft-harness-marketplace
```

VS Code에서는 **Chat: Manage Plugin Marketplaces**로 같은 저장소를 추가한 뒤
**Customize** 화면에서 `ai-msft-harness`를 검색해 설치할 수 있습니다.

### 프로젝트별 맞춤 검사

플러그인의 post-edit hook은 프로젝트 루트에 아래 스크립트가 있을 때만
실행합니다.

```text
.ai-msft-harness/post-edit.py
```

팀은 이 Python 스크립트에 자체 lint, test, architecture boundary 명령을
넣습니다.
종료 코드가 0이 아니면 Copilot에 실패 내용이 돌아가며 완료 보고 전에
수정하도록 요구합니다.

### 선택형 SQLite MCP

SQLite 조회가 필요한 프로젝트에서 DB 경로를 지정합니다.

```bash
export AI_MSFT_HARNESS_DB=/absolute/path/to/application.db
```

서버는 `list_tables`, `describe_table`, `query`를 제공하며 `SELECT`와
`WITH`만 허용합니다.

### 배포 전제

Marketplace 설치는 catalog와 plugin 폴더가 원격 기본 브랜치에 있어야
동작합니다. 현재 로컬 변경만으로는 다른 사용자가 설치할 수 없으므로
검증 후 저장소에 push하거나 별도 marketplace repository로 배포해야 합니다.
