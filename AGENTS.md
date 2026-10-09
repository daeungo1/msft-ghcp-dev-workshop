# TeamFeed 작업 원칙

## 명령

| 목적 | 명령 |
|---|---|
| 백엔드 테스트 | `cd backend && uv run pytest` |
| 프론트엔드 테스트 | `cd frontend && npm test` |
| 경계 검사 | `cd backend && uv run lint-imports` |
| 개발 서버 | `scripts/dev.sh` |
| 단계 검증 | `scripts/verify-step.sh S<번호>` |

## 작업 원칙

* 구현 전에 가정이 있으면 먼저 말합니다. 요구가 모호하면 추측하지 않고 질문합니다.
* 요청받은 범위만 수정합니다. 관련 없는 파일은 건드리지 않습니다.
* 테스트를 먼저 작성하고, 실패하는 테스트는 구현을 고쳐서 통과시킵니다.
* 완료를 보고할 때는 실행한 명령과 결과를 함께 적습니다.
* 원칙의 전체 내용은 `.specify/memory/constitution.md`에 있습니다.

## 디렉터리

* `backend/app/<패키지>/`: members, posts, follows, feed, reports. 공용 모듈은 `db.py`, `errors.py`, `security.py`입니다.
* `backend/tests/<패키지>/`: 패키지별 테스트
* `frontend/src/`: 화면
* `specs/001-teamfeed-mvp/`: 명세, 계획, 작업 목록
* `requirements/`: 단계별 요건과 수용 기준
