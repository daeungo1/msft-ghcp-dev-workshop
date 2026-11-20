---
title: AI SW Factory MSFT KO Plugin
description: Spec Kit 기반 애플리케이션 개발 절차를 GitHub Copilot에 설치하는 Agent Plugins 1.0 패키지
ms.date: 2026-11-18
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

* 기존 stack과 요구사항으로 선택하는
  [application profile 결정표](skills/team-application-standards/references/application-profile.md)
* 인증, 데이터/migration, API, UX, 성능, 복구, 관측성, 배포, 비용 검토
* 작은 앱의 도메인별 파일 구조 유지와 필요한 use case만 선택적 추출
* `Node.js >=22`, 신규 서비스는 승인된 최신 supported LTS 우선
* `Python >=3.12`, 신규 서비스는 승인된 latest bugfix-supported version 우선
* Business module/service 기준 분리
* `Adapters → Application Use Cases → Core` dependency direction
* Ports를 통한 DB, queue, external API 추상화
* One module/service or one use case 단위 incremental refactoring
* Legacy modernization의 Strangler Fig approach
* 여러 external resources를 위한 optional registry/adapter architecture shape
* Python import-linter와 TypeScript dependency boundary automation

### 2.1.0 변경 사항

TeamFeed의 FastAPI, SQLAlchemy, SQLite, React, TypeScript, Vite를 유지하는
교육용 profile과 실제 배포 전 결정할 production 요구사항을 구분합니다.
`core/application/ports/adapters` tree는 모든 앱의 필수 scaffold가 아니라
필요한 use case를 분리할 때의 예제입니다.

새 앱에서 `/spec-driven-delivery` 또는 `team-application-standards`를 사용할
때는 대상 사용자, 데이터 민감도, 예상 부하와 배포 환경을 함께 전달하세요.
Plan에 기술 선택의 이유, 대안, 검증 방법과 미결정 release blocker를 남깁니다.
이 update가 앱에 OIDC, PostgreSQL, migration이나 운영 인프라를 구현하지는
않습니다.

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

Hooks는 Agent/Skill과 별도로 다음 위치에 포함됩니다. Agent Plugins 1.0의
`plugin.json`에 legacy `hooks` 필드를 추가하지 않습니다.

```text
com.github.copilot/hooks/
  hooks.json
  pre_tool_guard.py
  post_edit_check.py
```

`preToolUse`는 위험 명령과 보호 경로를 검사하고, `postToolUse`는 성공한
편집 뒤 프로젝트 루트의 아래 스크립트가 있을 때만 실행합니다.

```text
.ai-sw-factory-msft-ko/post-edit.py
```

프로젝트 소유자가 내용을 검토하고 직접 추가합니다. Hook이 보호하는 경로를
에이전트가 우회해서 수정하지 않습니다. TeamFeed에서 빠른 backend 경계
검사만 연결하는 예제입니다. `uv`와 backend dependencies가 준비돼 있어야 합니다.

```python
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
subprocess.run(
    ["uv", "run", "--no-sync", "lint-imports"],
    cwd=root / "backend",
    check=True,
    timeout=90,
)
```

다른 stack에서는 그 프로젝트의 확인된 빠른 명령으로 바꿉니다. Dependency
설치, 자동 수정, migration, 배포를 post-edit에 연결하지 않습니다. 전체
tests, frontend build, 보안 검사는 CI/release gate에 둡니다.

| 상태 | Copilot에 반환하는 내용 |
|---|---|
| 스크립트 없음 | `not configured`, `No project checks were run` |
| 종료 코드 0 | `passed (configured checks only)` |
| 종료 코드가 0이 아님 | 실패 메시지와 출력의 마지막 40줄 |
| 120초 초과 또는 실행 불가 | timeout 또는 실행 오류 |

Post hook의 context 메시지는 도구 실행을 취소하거나 release를 강제로
차단하지 않습니다. Pre hook의 deny와 구분하고 공유 차단은 CI에 둡니다.

### Hook 로딩 확인

Agent/Skill 목록에 보이는 것만으로 hook 실행을 확인할 수는 없습니다.
VS Code 1.146.0의 plugin 카드 요약은 기여 유형을 앞의 두 종류만 표시하므로
Agent와 Skill이 있으면 Hook은 카드에 나타나지 않습니다. 이는 패키지에
Hook이 없거나 실행되지 않는다는 증거가 아닙니다. 별도의 Hooks 화면에도
plugin Hook이 표시되지 않는 사례가
[보고돼 있습니다](https://github.com/microsoft/vscode/issues/347955).
카드 표시를 위해 같은 Hook을 workspace에 중복 등록하지 마세요.
Client별 지원은 [공식 plugin 문서](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/plugins-creating)와
[hooks reference](https://docs.github.com/en/copilot/reference/hooks-reference)를
확인하세요. Cloud agent의 repository hook 설정과 local plugin hook 설치를
동일하게 취급하지 않습니다.

1. Local source install은 변경 후 `copilot plugin install`을 다시 실행해
   cache를 갱신하고 새 session을 시작합니다.
2. 해당 session에서 안전한 일반 파일 편집 뒤 post-edit의
   미설정/성공/실패 context를 확인합니다.
3. 실제 파괴적 명령을 실행해 시험하지 말고 아래 hook tests로 deny를 검증합니다.
4. 메시지가 없으면 plugin enabled 상태, client 지원, workspace trust와
   hook-disable 정책을 확인합니다. 출력이 없다는 이유로 통과라고 보고하지 않습니다.

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

### Publish validation

Repository root에서 실행합니다.

```bash
python scripts/validate-marketplace.py
python -m unittest scripts/tests/test_validate_marketplace.py -v
python -m unittest plugins/ai-sw-factory-msft-ko/tests/test_hooks.py -v
uv run --with pytest pytest -q \
  plugins/ai-sw-factory-msft-ko/mcp/sqlite-ro-server
uv run --with pytest pytest -q \
  templates/plugin/mcp/sqlite-ro-server
bash scripts/verify-step.sh S5
```

Validator는 official Agent Plugins 1.0 plugin/MCP schema, marketplace와
manifest의 name/version/source 일치, skills, agents, hooks, MCP file
references를 검사합니다. Remote Copilot client install은 release 후 별도
smoke test로 확인합니다.

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
