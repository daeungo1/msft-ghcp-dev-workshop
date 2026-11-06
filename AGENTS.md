# TeamFeed 작업 원칙

## 명령

| 목적 | 명령 |
|---|---|
| 백엔드 테스트 | `cd backend && uv run pytest` |
| 프론트엔드 테스트 | `cd frontend && npm test` |
| 경계 검사 | `cd backend && uv run lint-imports` |
| 하네스 검사 | `python scripts/validate-harness.py` |
| Marketplace 검사 | `python scripts/validate-marketplace.py` |
| 개발 서버 | `scripts/dev.sh` |
| 단계 검증 | `scripts/verify-step.sh S<번호>` |
| Spec Kit 상태 | `specify integration status --json` |

## 작업 원칙

* 구현 전에 가정이 있으면 먼저 말합니다. 요구가 모호하면 추측하지 않고 질문합니다.
* 가장 단순한 해법을 택합니다. 요청하지 않은 추상화와 기능을 넣지 않습니다.
* 요청받은 범위만 수정합니다. 관련 없는 파일은 건드리지 않습니다.
* 시작하기 전에 검증 기준(테스트나 명령)을 먼저 정합니다.
* 테스트를 먼저 작성하고, 실패하는 테스트는 구현을 고쳐서 통과시킵니다.
* 완료를 보고할 때는 실행한 명령과 결과를 함께 적습니다.
* 조사, 계획, 테스트, 구현, 리뷰 역할을 분리하고 모델 이름을 필수 계약에 고정하지 않습니다.
* 구현 후 `speckit-converge`로 명세와 현재 코드의 차이를 확인합니다.
* 원칙의 전체 내용은 `.specify/memory/constitution.md`에 있습니다.

## 디렉터리

* `backend/app/<패키지>/`: members, posts, follows, feed, reports. 공용 모듈은 `db.py`, `errors.py`, `security.py`입니다.
* `backend/tests/<패키지>/`: 패키지별 테스트
* `frontend/src/`: 화면
* `specs/001-teamfeed-mvp/`: 명세, 계획, 작업 목록
* `requirements/`: 단계별 요건과 수용 기준
* `spec-kit/`: TeamFeed extension, workflow, bundle source
* `.github/agents/`, `.github/skills/`: 역할과 반복 절차
* `docs/multi-harness-architecture.md`: 하네스 계층 책임
* `docs/model-routing.md`: 역할 역량 기반 모델 선택
