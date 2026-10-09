---
title: S5 패키징 + 내 팀 규칙 (30분)
description: 저장소에 갇힌 하네스를 팀 플러그인으로 묶어 다른 저장소에 설치하고 내 팀 규칙 하나를 더합니다
---

## 목표

저장소에 갇힌 하네스를 플러그인으로 묶어 다른 저장소에 설치하고, 자기 팀 규칙 하나를 더합니다.

## 추가 요건

[requirements/05-package.md](../requirements/05-package.md): 팀 플러그인 패키징과 내 팀 규칙 1개.

## 1. 플러그인 구성 (8분)

```bash
mkdir -p plugins && cp -r templates/plugin plugins/teamfeed-harness
```

스킬, 에이전트, 훅, MCP 설정을 플러그인 구조로 옮깁니다. `TODO(verify): Agent Plugins 스키마`

```text
plugins/teamfeed-harness/
├── plugin.json
├── skills/tdd/SKILL.md
├── skills/<my-team-rule>/SKILL.md
├── agents/            # test-writer, implementer, security-reviewer
├── hooks/             # guardrails.json + 스크립트
└── mcp.json           # sqlite-ro (경로는 환경변수)
```

## 2. 다른 저장소에 설치 (5분)

내 계정에 빈 `sandbox` 저장소를 만들고 플러그인을 설치한 뒤 스킬이 로드되는지 확인합니다. `TODO(verify): 로컬 경로 설치 지원 여부`

```bash
copilot plugin install <plugin source>
```

## 3. 내 팀 규칙 1개 추가 (15분)

[templates/team-rule-template.md](../templates/team-rule-template.md)를 채워 스킬(안내) 또는 훅(강제)으로 작성합니다. 플러그인 버전을 0.2.0으로 올립니다.

## 4. 사내 배포 흐름 (2분, 강사 데모)

사내 marketplace와 조직 정책으로 검증된 플러그인만 배포하는 흐름을 확인합니다.

## 5. 완료 확인

```bash
scripts/verify-step.sh S5
```

## 막히면

`scripts/checkpoint.sh S4`
