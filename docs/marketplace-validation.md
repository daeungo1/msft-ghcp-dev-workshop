---
title: Marketplace Validation
description: ai-sw-factory-msft-ko marketplace와 Agent Plugin package의 model-free 검증 기준
ms.date: 2026-11-06
ms.topic: reference
---

## Validation levels

GitHub-hosted marketplace는 중앙 등록 심사를 기다리는 방식이 아닙니다.
사용자가 repository를 marketplace source로 추가하면 client가 catalog와
plugin package를 읽습니다.

이 repository는 publish 전에 세 수준으로 검증합니다.

| Level | Command or gate | What it proves |
|---|---|---|
| Schema and structure | `python scripts/validate-marketplace.py` | Catalog, Agent Plugins manifest, skills, agents, hooks, MCP 구조 |
| Behavior | unit tests and MCP tests | Hook decisions, stale-path fallback, read-only SQL guard |
| Client smoke | `copilot plugin marketplace add/browse/install` | Remote GitHub marketplace를 실제 Copilot client가 설치 가능 |

## Self-validator

```powershell
python scripts/validate-marketplace.py
python scripts/validate-marketplace.py --json
```

Validator는 다음 항목을 검사합니다.

* `.github/plugin/marketplace.json` 존재와 stable kebab-case name
* Plugin source가 repository 안에 있고 directory가 존재하는지
* Catalog name/version/source와 `plugin.json` 일치
* Vendored official Agent Plugins 1.0 `plugin.schema.json`
* Vendored official Agent Plugins 1.0 `mcp.schema.json`
* Unknown manifest fields와 invalid plugin names
* Skill directory와 frontmatter `name` 일치
* Agent name/description uniqueness
* Bash/PowerShell hooks와 missing-path no-op fallback
* Hook와 MCP가 참조하는 packaged file 존재
* Reserved MCP environment variable override 금지
* Plugin README와 self-tests 존재

Official schema snapshot은
`.github/plugin/schemas/`에 있으며 Apache-2.0 license와 NOTICE를 함께
보관합니다.

## Local release gate

```powershell
python -m unittest scripts/tests/test_validate_marketplace.py -v
python -m unittest plugins/ai-sw-factory-msft-ko/tests/test_hooks.py -v
uv run --with pytest pytest -q `
  plugins/ai-sw-factory-msft-ko/mcp/sqlite-ro-server
uv run --with pytest pytest -q `
  templates/plugin/mcp/sqlite-ro-server
python scripts/validate-harness.py
bash scripts/verify-step.sh S5
```

## CI

[`validate-marketplace.yml`](../.github/workflows/validate-marketplace.yml)은
pull request, `main` push, manual dispatch에서 실행됩니다.

Matrix:

* Ubuntu latest
* Windows latest
* macOS latest
* Python 3.12

모델 호출 없이 schema, structure, hooks, MCP tests를 실행합니다. Plugin
변경은 [`CODEOWNERS`](../.github/CODEOWNERS)의 maintainer review 대상입니다.

## Remote client smoke test

GitHub login과 Copilot entitlement가 필요한 client install은 CI에서
실행하지 않습니다. Release 후 사람이 다음 명령으로 확인합니다.

```powershell
copilot plugin marketplace add daeungo1/msft-ghcp-dev-workshop
copilot plugin marketplace browse ai-sw-factory-msft-ko-marketplace
copilot plugin install `
  ai-sw-factory-msft-ko@ai-sw-factory-msft-ko-marketplace
copilot plugin list
copilot skill list
copilot mcp list
```

Success criteria:

* Marketplace source가 GitHub repository로 표시
* Plugin version이 catalog version과 일치
* Plugin enabled
* 6 skills visible
* `sqlite-ro` MCP visible

## What this does not mean

Self-validation 통과는 `github/awesome-copilot` 같은 별도 curated catalog에
등록됐다는 뜻이 아닙니다. 현재 repository 자체가 GitHub-hosted marketplace
입니다. 다른 catalog에 포함하려면 해당 catalog의 별도 contribution과
review 절차를 따라야 합니다.
