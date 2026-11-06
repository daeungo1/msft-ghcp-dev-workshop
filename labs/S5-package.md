---
title: S5 멀티 하네스 패키징 (35분)
description: 하네스를 Spec Kit extension, workflow, bundle과 Copilot plugin으로 패키징합니다
---

| 항목 | 내용 |
|---|---|
| 시간 | 35분 (Spec Kit 구성 10, 플러그인 10, 팀 규칙 7, 설치와 확인 6, 확인 2) |
| 도구 | Specify CLI, Copilot CLI (`copilot plugin`) |
| 시작 상태 | S4 완료 (`s4-done`) |
| 완료 상태 | `s5-done` 브랜치와 같은 수준 |
| 통제 방식 | 배포와 재사용 |
| 막는 함정 | 하네스가 이 저장소 안에만 있어 다음 프로젝트에서 처음부터 다시 만듦 |

## 이 단계에서 배우는 것

* 하네스를 저장소 밖으로 꺼내면 팀의 BP가 됩니다. 플러그인이 그 배포 단위입니다.
* 플러그인은 스킬, 커스텀 에이전트, 훅, MCP 설정을 한 번에 설치합니다.
* 우리 팀만의 규칙 하나를 더하는 일이 "BP를 내 것으로 만드는" 마지막 단계입니다.

## v0.2 연결

v0.2는 두 배포 단위를 구분합니다.

* Spec Kit extension은 명령과 품질 게이트를 제공
* Spec Kit workflow는 명령과 human gate를 순서화
* Spec Kit bundle은 승인된 component 버전을 팀 구성으로 고정
* Copilot plugin은 agents, skills, hooks, MCP를 Copilot CLI에 배포

먼저 저장소에 포함된 로컬 구성 요소를 설치합니다.

```bash
specify extension add ./spec-kit/extensions/teamfeed-quality --dev --force
specify workflow add ./spec-kit/workflows/teamfeed-delivery --dev
specify bundle install ./spec-kit/bundles/teamfeed-multi-harness --offline
```

설치 결과를 확인합니다.

```bash
specify extension list --json
specify workflow list
specify bundle list
python scripts/validate-harness.py
```

## 시작 전 확인

```bash
git status --short
scripts/checkpoint.sh S4      # S4를 건너뛰었다면 정답 상태에서 시작
```

## 추가 요건

[requirements/05-package.md](../requirements/05-package.md): `ai-sw-factory-msft-ko`
구조 만들기, VS Code와 다른 저장소에 설치, 팀 규칙 추가, marketplace 등록.

## 1. 하네스 없이 시도 (건너뜀)

이 단계의 함정은 "다른 저장소에서 하네스가 사라진다"입니다. 먼저 확인해 보세요.

```bash
mkdir -p ../sandbox && cd ../sandbox && git init -q
copilot            # 세션에서 /skills list 와 /agent 를 실행해 tdd 스킬과 test-writer 에이전트가 없는지 확인
```

## 2. Copilot 플러그인 구조 만들기 (10분)

골격과 배치 규칙은 [templates/plugin/README.md](../templates/plugin/README.md)에 있습니다. 이 형식은 `plugin.json`에 `$schema`를 선언하는 **Agent Plugins 1.0**입니다.

```bash
P=plugins/ai-sw-factory-msft-ko
mkdir -p $P/skills $P/mcp $P/com.github.copilot/agents $P/com.github.copilot/hooks

cp templates/plugin/plugin.json $P/plugin.json
cp templates/plugin/mcp.json $P/mcp.json
cp templates/plugin/hooks.json $P/com.github.copilot/hooks/hooks.json

cp -r .github/skills/tdd .github/skills/evidence-research \
  .github/skills/convergence-check $P/skills/
cp -r templates/plugin/skills/* $P/skills/
cp .github/agents/*.agent.md $P/com.github.copilot/agents/
cp templates/plugin/pre_tool_guard.py templates/plugin/post_edit_check.py \
  $P/com.github.copilot/hooks/
cp -r templates/plugin/mcp/sqlite-ro-server $P/mcp/sqlite-ro-server
```

`plugins/ai-sw-factory-msft-ko/plugin.json`의 `author`를 우리 팀 이름으로 바꾸고,
완성 버전을 `2.0.0`로 지정합니다.

## 3. 내 팀 규칙 1개 추가 (10분)

[templates/team-rule-template.md](../templates/team-rule-template.md)를 채웁니다.

1. 우리 팀에서 실제로 새는 상황 1~2개를 적습니다. 최근 리뷰나 장애에서 반복된 사례를 고릅니다.
2. 안내로 충분한지, 강제가 필요한지 고릅니다.
3. 결정에 따라 만듭니다.

| 결정 | 만들 것 | 위치 |
|---|---|---|
| 안내로 충분 | 스킬 | `plugins/ai-sw-factory-msft-ko/skills/<규칙-이름>/SKILL.md` |
| 강제가 필요 | 훅 규칙 추가 | `com.github.copilot/hooks/pre_tool_guard.py`의 규칙 목록 |
| 프로젝트마다 명령이 다름 | 프로젝트 검증 스크립트 | `.ai-sw-factory-msft-ko/post-edit.py` |

4. `plugin.json`과 `.github/plugin/marketplace.json`의 버전을 함께
   `2.0.0`로 올립니다.

> [!TIP]
> 규칙이 떠오르지 않으면 `bp-catalog`의 우리 BP 칸이나 [자가진단 카드](../templates/self-check-card.md)에서 가장 자주 새는 칸을 고르세요.

## 4. 설치와 확인 (8분)

```bash
copilot plugin install ./plugins/ai-sw-factory-msft-ko   # 수정 후에는 다시 실행해 캐시를 갱신합니다
copilot plugin list
```

sandbox 저장소에서 확인합니다.

```bash
cd ../sandbox
export AI_SW_FACTORY_MSFT_KO_DB=/workspaces/<저장소-이름>/backend/teamfeed.db
copilot
```

세션에서 다음을 확인합니다.

| 명령 | 기대하는 결과 |
|---|---|
| `/plugin list` | `ai-sw-factory-msft-ko` |
| `/skills list` | `tdd`와 내 팀 규칙 |
| `/agent` | `test-writer`, `implementer`, `security-reviewer` |
| `rm -rf /tmp/x 를 실행해줘` | 플러그인 훅이 거부합니다 |

> [!NOTE]
> 플러그인 훅은 설치 환경에 따라 스크립트 경로가 풀리지 않을 수 있습니다. 그 경우 훅은 조용히 건너뛰도록 만들어져 있습니다.
> 훅이 거부하지 않으면 스킬, 에이전트, MCP 확인까지만 하고 강사에게 알려 주세요.

설치한 플러그인을 지우려면 `copilot plugin uninstall ai-sw-factory-msft-ko`를 실행합니다.

> [!NOTE]
> 로컬 경로 직접 설치는 실습용으로 가장 빠르지만 CLI가 `deprecated` 경고를 출력합니다. 앞으로는 `plugin@marketplace` 방식만 지원될 예정이므로, 팀 배포는 아래 marketplace 방식을 기준으로 합니다.

### 사내 marketplace는 어떻게 되나요 (강사 데모)

여러 저장소에 배포하려면 플러그인 목록 파일(`.github/plugin/marketplace.json`)을 저장소에 두고 등록합니다.

```bash
copilot plugin marketplace add OWNER/REPO
copilot plugin install ai-sw-factory-msft-ko@ai-sw-factory-msft-ko-marketplace
```

현재 `main`의 `.github/plugin/marketplace.json`이 완성 예시입니다. 저장소
루트에서 `copilot plugin marketplace add .`로 로컬 marketplace를 등록한
뒤 `copilot plugin install ai-sw-factory-msft-ko@ai-sw-factory-msft-ko-marketplace`로
설치할 수 있습니다. 원격에 push한 뒤에는 다른 사용자가
`copilot plugin marketplace add daeungo1/msft-ghcp-dev-workshop`로 같은
marketplace를 추가할 수 있습니다.

## 5. 완료 확인 (2분)

```bash
cd <실습 저장소>
scripts/verify-step.sh S5
```

| 확인 항목 | 안 되면 |
|---|---|
| `plugin.json` 유효하고 `$schema`, `name`, `version`, `description` 포함 | 템플릿 복사 후 필드 확인 |
| plugin과 marketplace 버전이 일치 | 둘 다 `2.0.0`로 변경 |
| `skills/` 아래 `SKILL.md` 6개 이상 | delivery, team standards, research, TDD, convergence, PR |
| `com.github.copilot/agents/` 에이전트 6개 | 조사, 계획, 테스트, 구현, 보안, 수렴 |
| `com.github.copilot/hooks/hooks.json` 유효, `version` 1 | 템플릿 복사 |
| 루트 `mcp.json` 유효 | 템플릿 복사 |

## 정리

* 하네스를 재사용 가능한 자산으로 만드는 것이 팀 BP의 시작입니다.
* Spec Kit bundle은 프로세스 구성을, Copilot plugin은 런타임 사용자화를
  배포합니다.
* 두 패키지의 버전은 독립적으로 올리고 변경 근거를 기록합니다.

## 막히면

* 설치가 안 되면 `copilot plugin install ./plugins/ai-sw-factory-msft-ko`를 저장소 루트에서 다시 실행하고, 오류 메시지의 첫 줄을 확인합니다.
* 목록에 보이지 않으면 `plugin.json`의 JSON 오류와 `$schema` 문자열을 확인합니다.
* 시간이 부족하면 `scripts/checkpoint.sh S5`로 정답 상태에서 설치 확인만 합니다.

## 정답 보기

```bash
git diff s4-done..s5-done --stat
git show main:plugins/ai-sw-factory-msft-ko/plugin.json
git ls-tree -r --name-only main plugins/ai-sw-factory-msft-ko
```

## 업계 공통 패턴

팀 자산 배포. [bp-catalog](../bp-catalog/README.md)를 참고합니다.
