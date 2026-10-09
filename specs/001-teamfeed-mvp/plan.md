# 구현 계획: TeamFeed MVP

## 기술 스택

* 백엔드: Python 3.12, FastAPI, SQLAlchemy 2, SQLite, pytest
* 프론트엔드: React 18, Vite, TypeScript, Vitest
* 도구: uv, import-linter

## 디렉터리와 패키지

```text
backend/app/
  main.py            앱 진입점, 라우터 등록
  db.py              엔진과 세션
  errors.py          오류 응답 형식
  security.py        X-Member-Id 해석과 관리자 검사
  members/ posts/ follows/ feed/ reports/
    models.py repository.py service.py schemas.py routes.py api.py
backend/tests/<패키지>/
frontend/src/
```

## 경계 규칙

* 한 패키지는 다른 패키지의 `api.py`로만 접근합니다. 예: `feed`는 `follows.api`와 `posts.api`를 호출합니다.
* 이 규칙은 S2에서 import-linter 계약으로 강제합니다.

## 데이터 모델

데이터베이스 파일은 `scripts/seed-db.py`가 만든 것과 같은 스키마를 씁니다. 컬럼 이름은 추측하지 않고 실제 스키마를 확인합니다. 환경 변수 `TEAMFEED_DB`가 DB 경로이며 기본값은 `backend/teamfeed.db`입니다.

| 테이블 | 컬럼 |
|---|---|
| members | id, name (UNIQUE), role |
| posts | id, author_member_id, body, created_ts, is_hidden |
| follows | follower_member_id, followee_member_id |
| reports | id, post_id, reporter_member_id, reason, status, created_ts, UNIQUE(post_id, reporter_member_id) |

## 공개 API

| 메서드와 경로 | 설명 | 인증 |
|---|---|---|
| POST /api/members | 가입 | 없음 |
| GET /api/members | 회원 목록 | 없음 |
| POST /api/posts | 글 작성 | X-Member-Id |
| GET /api/posts | 글 목록 (`author_id` 선택) | 없음 |
| POST /api/follows, DELETE /api/follows/{id} | 팔로우, 해제 | X-Member-Id |
| GET /api/feed | 피드 (`limit`, `before`) | X-Member-Id |
| POST /api/reports | 신고 | X-Member-Id |
| GET /api/reports, PATCH /api/reports/{id} | 신고 목록, 처리 | 관리자 |

오류는 `{"error": {"code", "message"}}` 형식입니다.
