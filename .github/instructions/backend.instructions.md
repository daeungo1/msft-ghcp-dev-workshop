---
description: TeamFeed 백엔드의 도메인 경계, 오류, 데이터 접근 규칙
applyTo: "backend/**/*.py"
---

# 백엔드 규칙

* 도메인 패키지는 `routes.py`, `service.py`, `repository.py`, `api.py`로
  책임을 분리합니다.
* 다른 도메인은 공개 `api.py`만 import합니다.
* HTTP 오류는 `app.errors`의 예외로 표현하고 공통 오류 응답 형식을
  유지합니다.
* 데이터베이스 쓰기는 `repository.py`에서만 수행합니다.
* SQLAlchemy 모델과 실제 스키마를 확인한 뒤 컬럼을 사용합니다.
* 모든 함수에 타입 힌트를 추가하고 한 함수는 한 책임만 가집니다.

