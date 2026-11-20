---
title: 05 하네스 패키징
description: S5 요건. 저장소에 쌓은 하네스를 팀 플러그인으로 묶어 재사용
---

## 배경

S0~S4에서 만든 하네스는 이 저장소 안에만 있습니다.
다음 프로젝트에서도 같은 개발 패턴이 동작하도록 `ai-sw-factory-msft-ko`
플러그인으로 묶고 VS Code와 Copilot CLI에서 설치할 수 있게 합니다.

## 기능 요건

1. `plugins/ai-sw-factory-msft-ko/`에 스킬, 커스텀 에이전트, 훅, MCP 설정을 Agent Plugins 1.0 구조(`plugin.json` + `skills/` + `mcp.json` + `com.github.copilot/`)로 옮깁니다. 구조는 `templates/plugin/README.md`를 따릅니다.
2. Spec Kit delivery, team application standards, 조사, TDD, 수렴 검사,
   PR 설명 skills와 역할 에이전트 6개를 포함합니다.
3. 다른 저장소(`sandbox`)와 VS Code의 Agent Customizations에서 플러그인을
   설치해 로드되는지 확인합니다.
4. `templates/team-rule-template.md`로 내 팀 규칙 1개를 skill, hook 또는
   프로젝트별 `.ai-sw-factory-msft-ko/post-edit.py`로 추가합니다.
5. `.github/plugin/marketplace.json`에 플러그인을 등록하고 버전을 `2.1.0`로
   맞춥니다.
6. TeamFeed의 stack과 도메인별 파일 구성을 유지하는 application profile,
   production 기술 요건 결정표를 포함합니다. 구체적인 운영 기능 추가는
   별도 명세와 구현 범위로 분리합니다.

## 수용 기준

* Given 플러그인을 만들었을 때 / When `plugin.json`을 검사하면 / Then 유효한 JSON이고 필수 필드가 있습니다
* Given 플러그인을 설치했을 때 / When VS Code 또는 CLI에서 구성 목록을 보면 / Then 6개 skills와 6개 역할 에이전트가 보입니다
* Given marketplace catalog를 검사할 때 / When plugin 항목을 찾으면 / Then 이름, 버전, source가 `plugin.json`과 일치합니다
* Given 프로젝트별 post-edit 검사를 추가했을 때 / When 검사가 실패하면 / Then Copilot에 실패 내용이 명시적으로 돌아갑니다
* Given 프로젝트별 post-edit 검사가 없을 때 / When 성공한 편집이 끝나면 / Then 미설정이며 검사를 실행하지 않았다고 명시합니다
* Given 프로젝트별 post-edit 검사가 있을 때 / When 검사가 통과하면 / Then 설정된 검사만 통과했음을 명시합니다
* Given 읽기 도구 또는 실패한 편집일 때 / When post-tool hook을 호출하면 / Then 프로젝트 검사를 실행하지 않습니다
* Given 앱의 기술을 계획할 때 / When team standards를 적용하면 / Then 기존 stack 유지/변경 근거, production 요구와 검증 방법, 미결정 blocker를 기록합니다

## 범위 밖

* Enterprise managed plugin 정책과 강제 설치
