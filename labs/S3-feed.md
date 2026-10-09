---
title: S3 피드 (15분)
description: 에이전트가 스키마를 추측하지 않고 필요한 만큼만 DB를 보게 합니다
---

## 목표

에이전트가 스키마를 추측하지 않고, 필요한 만큼만 DB를 볼 수 있게 합니다.

## 추가 요건

[requirements/03-feed.md](../requirements/03-feed.md): 팔로우한 사람과 내 글을 모아 보는 피드.

## 1. 하네스 없이 시도 (3분)

```bash
uv run --directory backend python ../scripts/seed-db.py
```

```text
requirements/03-feed.md 의 피드 API를 구현해줘.
```

## 2. 관찰

* 에이전트가 실제와 다른 컬럼명(`content`, `created_at` 등)을 추측했나요?
* DB를 직접 수정하려고 시도했나요?

## 3. 하네스 추가 (4분)

MCP 설정 템플릿을 복사합니다. 서버 정의는 이미 준비되어 있습니다.

```bash
cp templates/mcp/vscode-mcp.json .vscode/mcp.json
```

* Copilot CLI는 `/mcp add` 또는 `templates/mcp/copilot-cli-mcp-config.json`을 참고합니다. `TODO(verify): CLI 설정 파일 위치`
* `sqlite-ro` 서버는 `list_tables`, `describe_table`, `query`(SELECT만) 도구를 제공하고 DB를 읽기 전용으로 엽니다.

## 4. 같은 요청 재실행 (6분)

1번 프롬프트를 다시 실행합니다. 에이전트가 `describe_table` 결과로 쿼리를 작성하고 피드 화면을 완성하는지 확인합니다.

## 5. GitHub MCP로 이슈 연결 (2분)

```text
GitHub MCP로 "피드 페이지네이션 개선" 이슈를 만들고, 이번 커밋 메시지에 이슈 번호를 연결해줘.
```

## 6. 완료 확인

```bash
scripts/verify-step.sh S3
```

## 막히면

* `scripts/checkpoint.sh S2`
* MCP 연결 실패 시 `TEAMFEED_DB` 경로를 확인합니다.

## 업계 공통 패턴

최소 권한 도구 접근. [bp-catalog](../bp-catalog/README.md) 참고.
