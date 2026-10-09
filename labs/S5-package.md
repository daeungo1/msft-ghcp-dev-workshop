---
title: S5 패키징 (30분)
description: 저장소에 쌓은 하네스를 팀 플러그인으로 묶어 다른 저장소에서 한 줄로 설치하고, 내 팀 규칙 1개를 더합니다
---

| 항목 | 내용 |
|---|---|
| 시간 | 30분 (패키징 10, 팀 규칙 10, 설치와 확인 8, 확인 2) |
| 도구 | Copilot CLI (`copilot plugin`) |
| 시작 상태 | S4 완료 (`s4-done`) |
| 완료 상태 | `s5-done` 브랜치와 같은 수준 |
| 통제 방식 | 배포와 재사용 |
| 막는 함정 | 하네스가 이 저장소 안에만 있어 다음 프로젝트에서 처음부터 다시 만듦 |

## 이 단계에서 배우는 것

* 하네스를 저장소 밖으로 꺼내면 팀의 BP가 됩니다. 플러그인이 그 배포 단위입니다.
* 플러그인은 스킬, 커스텀 에이전트, 훅, MCP 설정을 한 번에 설치합니다.
* 우리 팀만의 규칙 하나를 더하는 일이 "BP를 내 것으로 만드는" 마지막 단계입니다.

## 시작 전 확인

```bash
git status --short
scripts/checkpoint.sh S4      # S4를 건너뛰었다면 정답 상태에서 시작
```

## 추가 요건

[requirements/05-package.md](../requirements/05-package.md): 플러그인 구조 만들기, 다른 저장소에 설치, 팀 규칙 1개 추가, 버전 0.2.0.

## 1. 하네스 없이 시도 (건너뜀)

이 단계의 함정은 "다른 저장소에서 하네스가 사라진다"입니다. 먼저 확인해 보세요.

```bash
mkdir -p ../sandbox && cd ../sandbox && git init -q
copilot            # 세션에서 /skills list 와 /agent 를 실행해 tdd 스킬과 test-writer 에이전트가 없는지 확인
```

## 2. 플러그인 구조 만들기 (10분)

골격과 배치 규칙은 [templates/plugin/README.md](../templates/plugin/README.md)에 있습니다. 이 형식은 `plugin.json`에 `$schema`를 선언하는 **Agent Plugins 1.0**입니다.

```bash
P=plugins/teamfeed-harness
mkdir -p $P/skills $P/mcp $P/com.github.copilot/agents $P/com.github.copilot/hooks

cp templates/plugin/plugin.json $P/plugin.json
cp templates/plugin/mcp.json $P/mcp.json
cp templates/plugin/hooks.json $P/com.github.copilot/hooks/hooks.json

cp -r .github/skills/tdd $P/skills/tdd
cp .github/agents/*.agent.md $P/com.github.copilot/agents/
cp scripts/hooks/pre_tool_guard.sh scripts/hooks/post_edit_check.sh $P/com.github.copilot/hooks/
cp -r templates/mcp/sqlite-ro-server $P/mcp/sqlite-ro-server
```

`plugins/teamfeed-harness/plugin.json`의 `author`를 우리 팀 이름으로 바꿉니다. 이 시점의 버전은 `0.1.0`입니다.

## 3. 내 팀 규칙 1개 추가 (10분)

[templates/team-rule-template.md](../templates/team-rule-template.md)를 채웁니다.

1. 우리 팀에서 실제로 새는 상황 1~2개를 적습니다. 최근 리뷰나 장애에서 반복된 사례를 고릅니다.
2. 안내로 충분한지, 강제가 필요한지 고릅니다.
3. 결정에 따라 만듭니다.

| 결정 | 만들 것 | 위치 |
|---|---|---|
| 안내로 충분 | 스킬 | `plugins/teamfeed-harness/skills/<규칙-이름>/SKILL.md` |
| 강제가 필요 | 훅 규칙 추가 | `com.github.copilot/hooks/pre_tool_guard.sh`의 규칙 목록 |

4. `plugin.json`의 `version`을 `0.2.0`으로 올립니다.

> [!TIP]
> 규칙이 떠오르지 않으면 `bp-catalog`의 우리 BP 칸이나 [자가진단 카드](../templates/self-check-card.md)에서 가장 자주 새는 칸을 고르세요.

## 4. 설치와 확인 (8분)

```bash
copilot plugin install ./plugins/teamfeed-harness   # 수정 후에는 다시 실행해 캐시를 갱신합니다
copilot plugin list
```

sandbox 저장소에서 확인합니다.

```bash
cd ../sandbox
export TEAMFEED_DB=/workspaces/<저장소-이름>/backend/teamfeed.db   # sqlite-ro MCP 서버가 읽을 DB 경로
copilot
```

세션에서 다음을 확인합니다.

| 명령 | 기대하는 결과 |
|---|---|
| `/plugin list` | `teamfeed-harness` 0.2.0 |
| `/skills list` | `tdd`와 내 팀 규칙 |
| `/agent` | `test-writer`, `implementer`, `security-reviewer` |
| `rm -rf /tmp/x 를 실행해줘` | 플러그인 훅이 거부합니다 |

> [!NOTE]
> 플러그인 훅은 설치 환경에 따라 스크립트 경로가 풀리지 않을 수 있습니다. 그 경우 훅은 조용히 건너뛰도록 만들어져 있습니다.
> 훅이 거부하지 않으면 스킬, 에이전트, MCP 확인까지만 하고 강사에게 알려 주세요.

설치한 플러그인을 지우려면 `copilot plugin uninstall teamfeed-harness`를 실행합니다.

> [!NOTE]
> 로컬 경로 직접 설치는 실습용으로 가장 빠르지만 CLI가 `deprecated` 경고를 출력합니다. 앞으로는 `plugin@marketplace` 방식만 지원될 예정이므로, 팀 배포는 아래 marketplace 방식을 기준으로 합니다.

### 사내 marketplace는 어떻게 되나요 (강사 데모)

여러 저장소에 배포하려면 플러그인 목록 파일(`.github/plugin/marketplace.json`)을 저장소에 두고 등록합니다.

```bash
copilot plugin marketplace add OWNER/REPO
copilot plugin install teamfeed-harness@<marketplace-이름>
```

`final` 브랜치의 `.github/plugin/marketplace.json`이 예시입니다. `final`에서 `copilot plugin marketplace add .`로 저장소를 로컬 marketplace로 등록한 뒤 `copilot plugin install teamfeed-harness@teamfeed-marketplace`로 설치해 볼 수 있습니다 (사용 후 `copilot plugin marketplace remove teamfeed-marketplace`). 조직 정책(허용할 marketplace 지정)은 이 실습의 범위 밖입니다.

## 5. 완료 확인 (2분)

```bash
cd <실습 저장소>
scripts/verify-step.sh S5
```

| 확인 항목 | 안 되면 |
|---|---|
| `plugin.json` 유효하고 `$schema`, `name`, `version`, `description` 포함 | 템플릿 복사 후 필드 확인 |
| 버전이 `0.1.0`이 아님 | `0.2.0`으로 변경 |
| `skills/` 아래 `SKILL.md` 2개 이상 | `tdd`와 내 팀 규칙 |
| `com.github.copilot/agents/` 에이전트 3개 | 2번 복사 명령 확인 |
| `com.github.copilot/hooks/hooks.json` 유효, `version` 1 | 템플릿 복사 |
| 루트 `mcp.json` 유효 | 템플릿 복사 |

## 정리

* 하네스를 재사용 가능한 자산으로 만드는 것이 팀 BP의 시작입니다.
* 플러그인 버전은 팀 BP의 버전입니다. 규칙을 더하면 올립니다.

## 막히면

* 설치가 안 되면 `copilot plugin install ./plugins/teamfeed-harness`를 저장소 루트에서 다시 실행하고, 오류 메시지의 첫 줄을 확인합니다.
* 목록에 보이지 않으면 `plugin.json`의 JSON 오류와 `$schema` 문자열을 확인합니다.
* 시간이 부족하면 `scripts/checkpoint.sh S5`로 정답 상태에서 설치 확인만 합니다.

## 정답 보기

```bash
git diff s4-done..s5-done --stat
git show s5-done:plugins/teamfeed-harness/plugin.json
git ls-tree -r --name-only s5-done plugins/teamfeed-harness
```

## 업계 공통 패턴

팀 자산 배포. [bp-catalog](../bp-catalog/README.md)를 참고합니다.
