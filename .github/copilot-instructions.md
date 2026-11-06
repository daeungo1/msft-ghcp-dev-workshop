# Copilot 인스트럭션

TeamFeed 저장소 전체에 적용되는 규칙입니다. 작업 원칙과 명령은 `AGENTS.md`를 따릅니다.

## 스타일

* Python은 타입 힌트를 쓰고 함수는 한 가지 일만 합니다.
* TypeScript는 `any`를 쓰지 않습니다.
* 도메인 패키지는 `routes.py`(HTTP), `service.py`(규칙), `repository.py`(DB), `api.py`(다른 패키지에 공개하는 함수)로 나눕니다.

## 에러 응답

모든 오류는 `{"error": {"code": "NOT_FOUND", "message": "..."}}` 형식으로 응답합니다. 직접 `HTTPException`을 던지지 않고 `app.errors`의 예외를 씁니다.

## 테스트

* 수용 기준 하나에 테스트 하나를 만들고, 테스트 이름에 기준을 담습니다.
* 새 기능은 실패하는 테스트를 먼저 만듭니다.
* 테스트를 고쳐서 통과시키지 않습니다.

## 보안

* 관리자 엔드포인트는 서버에서 역할을 검사합니다.
* SQL은 바인딩 파라미터만 씁니다. 문자열로 쿼리를 조립하지 않습니다.

## DB

* 스키마를 추측하지 않고 `models.py`나 DB 조회 도구로 확인합니다.
* 쓰기는 `repository.py`를 통해서만 합니다.

## 하네스 계층

* Spec Kit 산출물은 요구사항과 작업 범위의 기준입니다.
* instructions는 지속 규칙, skills는 반복 절차, agents는 역할 경계,
  hooks는 빠른 차단, MCP는 외부 컨텍스트, CI는 공유 검증을 담당합니다.
* 같은 규칙을 여러 계층에 복사하지 않고 가장 좁은 책임에 둡니다.
* 구현 후 `speckit-converge`와 저장소 검증 명령으로 명세와 코드의 차이를
  확인합니다.

## 모델 선택

* 저장소는 특정 모델을 필수로 요구하지 않습니다.
* 워크숍 runtime default는 Copilot Fusion Standard입니다. S4 security
  review와 S6 convergence는 Fusion High, final audit은 필요할 때만 Fusion
  Max를 사용합니다.
* Agent frontmatter에는 Fusion이나 개별 model을 고정하지 않습니다.
* 조사, 계획, 테스트, 구현, 리뷰 역할에 필요한 역량을 기준으로 런타임에서
  모델을 선택합니다.
* 선택형 모델을 사용할 수 없으면 오류를 숨기지 말고 지원되는 모델로 역할을
  다시 배정합니다.
