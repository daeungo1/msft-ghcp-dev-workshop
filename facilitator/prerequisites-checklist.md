---
title: 사전 준비 체크리스트
description: 참가자 계정, 조직 정책, 개발 환경, 안내 메일 문안, 리허설 점검 항목
---

## 참가자

* [ ] GitHub 계정
* [ ] Copilot Business 또는 Enterprise 라이선스
* [ ] GitHub Codespaces 사용 가능 또는 로컬 VS Code + Dev Containers
* [ ] 노트북에 터미널과 Git (Windows는 WSL 또는 Git Bash 사용을 권장)

## 조직 정책

* [ ] Copilot CLI 허용
* [ ] MCP 서버 허용
* [ ] 프리뷰 기능 허용
* [ ] Codespaces 사용과 할당량
* [ ] 참가자가 템플릿에서 저장소를 만들 수 있는 권한
* [ ] CodeQL: 공개 저장소이거나 GitHub Code Security(GHAS) 라이선스. 둘 다 아니면 강사 데모로 대체합니다

## 사전 점검 명령

```bash
copilot --version
uv --version
node -v
specify --help
```

## 안내 메일 (워크샵 1주 전)

제목: [GHCP 워크샵] 사전 준비 안내

본문:

> 안녕하세요. 이번 워크샵은 직접 코드를 작성하고 GitHub Copilot의 하네스(인스트럭션, 스킬, 에이전트, 훅, MCP, 플러그인)를 하나씩 붙여 보는 3시간 핸즈온입니다.
>
> 아래 두 가지만 미리 준비해 주세요.
>
> 1. https://github.com/daeungo1/msft-ghcp-dev-workshop 에서 "Use this template" 로 본인 계정에 저장소를 만들어 주세요.
> 2. 저장소에서 Code > Codespaces > Create codespace 로 환경을 한 번 열어 두세요. 첫 실행에 몇 분이 걸립니다.
>
> 로컬에서 진행하시려면 README의 "시작하기"를 참고해 주세요.
> Copilot 라이선스와 Copilot CLI 사용이 막혀 있으면 미리 알려 주세요.

## 리허설 점검 (강사, 워크샵 전)

이 항목은 개발 환경 밖에서 확인할 수 없어 리허설에서 실제로 해 봐야 합니다.

| 항목 | 확인 방법 | 안 되면 |
|---|---|---|
| CLI에서 훅 동작 | `scripts/hooks/test_hooks.sh` 통과 후 CLI 세션에서 위험 명령 요청 | 훅 JSON 필드 이름(`toolName`, `toolArgs`)을 CLI 로그와 대조 |
| 플러그인 설치 | 빈 sandbox 저장소에 `copilot plugin install ./plugins/teamfeed-harness` | `plugin.json`의 `$schema`와 필드 확인 |
| 플러그인 훅 경로 | 설치한 플러그인의 훅이 위험 명령을 거부하는지 확인 | 스크립트 경로가 풀리지 않으면 `.github/hooks`를 복사하는 방식으로 대체 |
| MCP 환경 변수 | `TEAMFEED_DB`를 설정한 셸에서 `sqlite-ro`가 연결되는지 | 절대 경로로 설정 |
| CodeQL | 템플릿에서 만든 저장소에서 워크플로 1회 실행 | 강사 데모 PR 화면으로 대체 |
| `uv sync` 시간 | Codespaces에서 첫 실행 시간 측정 | prebuild 설정 |
| 진단 5개 축 이름 | 자가진단 카드의 축 이름이 Innovation Hub 진단 기준과 같은지 확인 | `templates/self-check-card.md` 수정 |
| 덱 용어 | 덱의 "Agent Plugin v2"와 이 저장소의 "Agent Plugins 1.0" 표기 정합 | 덱 또는 문서 한쪽 수정 |
| 저장소 이름 | 덱의 `ghcp-harness-workshop` / `start` 표기와 이 저장소의 `msft-ghcp-dev-workshop` / `main` 정합 | 덱 슬라이드 24 수정 |
