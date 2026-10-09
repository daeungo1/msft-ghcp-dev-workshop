---
applyTo: "backend/tests/**"
---

# 테스트 파일 규칙

* 수용 기준 하나에 테스트 하나를 만들고, 테스트 이름에 기준을 담습니다. 예: `test_follow_self_returns_422`
* 요청에는 `tests/conftest.py`의 `client`, `h(member_id)`, `make_member(role)`를 씁니다. 헤더나 회원을 직접 조립하지 않습니다.
* 인증이 필요한 호출은 `X-Member-Id` 헤더를 넣고, 오류 응답은 상태 코드와 `error.code`를 함께 확인합니다.
* 테스트는 `backend/tests/<패키지>/` 아래에 둡니다. 구현 파일은 이 규칙이 붙은 작업에서 수정하지 않습니다.