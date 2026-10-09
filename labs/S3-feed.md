---
title: S3 피드 (15분)
description: 에이전트가 스키마를 추측하지 않고 필요한 만큼만 DB를 보게 하는 읽기 전용 MCP를 붙입니다
---

| 항목 | 내용 |
|---|---|
| 시간 | 15분 (시도 3, 관찰 1, 하네스 추가 4, 재실행 5, GitHub MCP 1, 확인 1) |
| 도구 | Copilot CLI 또는 VS Code (MCP 설정 파일이 다릅니다) |
| 시작 상태 | S2 완료 (`s2-done`) |
| 완료 상태 | `s3-done` 브랜치와 같은 수준 |
| 통제 방식 | 도구 범위 제한 |
| 막는 함정 | 실제 스키마를 보지 않고 컬럼 이름을 추측한 쿼리 |

## 이 단계에서 배우는 것

* 에이전트에게 "DB를 보여 주지 않으면 추측하고, 쓰기 권한을 주면 위험"합니다. 읽기 전용 도구로 필요한 만큼만 보여 줍니다.
* MCP는 에이전트에 도구를 연결하는 표준입니다. 서버 코드는 [templates/mcp/sqlite-ro-server/](../templates/mcp/sqlite-ro-server/)에 이미 있고, 우리는 연결 설정만 합니다.

## 시작 전 확인

```bash
git status --short
scripts/checkpoint.sh S2      # S2를 건너뛰었다면 정답 상태에서 시작
```

## 추가 요건

[requirements/03-feed.md](../requirements/03-feed.md): 팔로우한 사람과 내 글을 모아 보는 피드.

운영 중인 DB가 이미 있다고 가정합니다. 시드 스크립트로 같은 모양의 데이터(회원 20, 글 200, 팔로우 60)를 만듭니다.

```bash
uv run --directory backend python ../scripts/seed-db.py
```

## 1. 하네스 없이 시도 (3분)

```text
requirements/03-feed.md 의 피드 API를 구현해줘. 쿼리는 backend/teamfeed.db 의 데이터로 확인해.
```

## 2. 관찰 (1분)

* 에이전트가 실제와 다른 컬럼 이름(`content`, `created_at`, `author_id` 등)을 추측했나요?
* DB 파일을 직접 열어 수정하거나 `sqlite3` 명령을 임의로 실행했나요?

확인이 끝나면 변경을 보관합니다.

```bash
git stash push -u -m "s3-no-harness"
```

## 3. 하네스 추가 (4분)

`sqlite-ro` 서버는 세 가지 도구를 제공하고 DB를 읽기 전용으로 엽니다.

| 도구 | 하는 일 |
|---|---|
| `list_tables` | 테이블 목록 |
| `describe_table` | 컬럼 이름과 타입 |
| `query` | SELECT만 허용 |

사용하는 도구에 맞는 설정 파일을 복사합니다. 둘 다 해도 됩니다.

```bash
# VS Code
mkdir -p .vscode && cp templates/mcp/vscode-mcp.json .vscode/mcp.json

# Copilot CLI (저장소 루트에서 실행해야 상대 경로가 맞습니다)
cp templates/mcp/copilot-cli-mcp.json .mcp.json
```

| 도구 | 설정 파일 | 비고 |
|---|---|---|
| VS Code | `.vscode/mcp.json` (키 이름 `servers`) | `github` HTTP 서버도 함께 정의되어 있습니다 |
| Copilot CLI | `.mcp.json` 또는 `.github/mcp.json` (키 이름 `mcpServers`) | 프로젝트 MCP 서버는 폴더 신뢰를 확인한 뒤 로드됩니다. GitHub MCP 서버는 기본 내장입니다 |

Copilot CLI는 `copilot`을 다시 시작한 뒤 `/mcp`로 `sqlite-ro`가 보이는지 확인합니다. VS Code는 `.vscode/mcp.json` 파일 상단의 **Start** 링크로 서버를 시작합니다.

## 4. 같은 요청 재실행 (5분)

```text
sqlite-ro MCP의 list_tables, describe_table 로 실제 스키마를 먼저 확인한 뒤, requirements/03-feed.md 의 피드 API와 피드 화면을 구현해줘.
```

* 에이전트가 `describe_table` 결과로 실제 컬럼 이름(`body`, `created_ts`, `author_member_id` 등)을 썼는지 확인합니다.
* 쓰기 쿼리(`UPDATE`, `DELETE`)를 시도하면 서버가 거부하는지 직접 확인해 봅니다.

  ```text
  sqlite-ro 의 query 도구로 posts 테이블의 첫 번째 글을 삭제해줘.
  ```

## 5. GitHub MCP로 이슈 연결 (1분)

```text
GitHub MCP로 "피드 페이지네이션 개선" 이슈를 만들고, 이번 커밋 메시지에 이슈 번호를 연결해줘.
```

> [!NOTE]
> 실습 저장소에서 이슈 기능이 꺼져 있거나 권한이 없으면 건너뜁니다. 핵심은 "도구가 추가되면 에이전트가 할 수 있는 일이 넓어진다"는 점을 보는 것입니다.

## 6. 완료 확인 (1분)

```bash
scripts/verify-step.sh S3
```

| 확인 항목 | 안 되면 |
|---|---|
| `.vscode/mcp.json`에 `sqlite-ro`, `github` 정의 | 3의 복사 명령 |
| `.mcp.json`에 `sqlite-ro` 정의 | 3의 복사 명령 |
| sqlite-ro 서버 테스트 통과 | 서버 파일을 수정하지 않았는지 확인 |
| `backend/tests/feed` 통과 | 피드 테스트 실패 메시지를 에이전트에게 전달 |

## 정리

* 하네스의 Tools 계층은 "무엇을 할 수 있게 하느냐"보다 "어디까지만 할 수 있게 하느냐"가 중요합니다.
* 읽기 전용 도구는 필요한 만큼의 사실을 주고 위험은 막는, 최소 권한 접근입니다.

## 막히면

* 서버가 시작되지 않으면 `TEAMFEED_DB` 경로와 `scripts/seed-db.py` 실행 여부를 확인합니다.
* Copilot CLI에서 서버가 안 보이면 폴더 신뢰를 허용했는지, `copilot`을 저장소 루트에서 실행했는지 확인합니다.
* 시간이 부족하면 `scripts/checkpoint.sh S3`로 정답 상태에서 합류합니다.

## 정답 보기

```bash
git diff s2-done..s3-done --stat
git show s3-done:.mcp.json
```

## 업계 공통 패턴

최소 권한 도구 접근. [bp-catalog](../bp-catalog/README.md)를 참고합니다.
