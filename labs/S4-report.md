---
title: S4 신고 (35분)
description: 테스트가 통과해도 남는 결함을 작성자와 분리된 리뷰와 결정적 스캔으로 잡습니다
---

## 목표

테스트가 통과해도 남는 결함을 작성자와 분리된 리뷰와 결정적 스캔으로 잡습니다.

## 추가 요건

[requirements/04-report.md](../requirements/04-report.md): 신고, 관리자 처리 화면.

## 1. 하네스 없이 시도 (7분)

```text
requirements/04-report.md 의 신고 기능을 구현하고 테스트를 통과시켜줘.
```

## 2. 관찰

테스트는 통과합니다. 일반 회원으로 처리 API를 호출해 봅니다.

```bash
curl -i -X PATCH localhost:8000/api/reports/1 \
  -H "X-Member-Id: <일반 회원 id>" -H "Content-Type: application/json" \
  -d '{"status": "ACCEPTED"}'
```

* 200이 반환되나요? (관리자 인가 누락)
* `q` 키워드 검색이 문자열 결합 SQL로 작성되었나요?

## 3. 하네스 추가 (18분)

1. Copilot CLI plan 모드로 계획을 세우고 `/rubber-duck`으로 다른 모델 계열의 비평을 받아 계획을 수정합니다 (5분).
2. `.github/agents/security-reviewer.agent.md`를 작성하고 리뷰를 실행합니다 (8분). `TODO(verify): tools 값`
   * 도구: 읽기·검색만, 코드를 직접 수정하지 않음
   * 점검: 상태 변경 라우트의 인가 의존성, 403 테스트, 원시 SQL 결합, 오류 응답의 내부 정보 노출
   * 출력: `Critical / High / Medium` 표, 파일:라인, 근거, 수정 제안. 인가 누락은 항상 Critical
3. 수정합니다 (5분). `test-writer`로 403 테스트를 추가하고 `implementer`로 `require_admin`을 적용합니다.

## 4. CodeQL과 Copilot code review (10분)

```bash
cp templates/workflows/codeql.yml .github/workflows/
git push -u origin HEAD
```

PR을 만들고 Copilot code review를 요청한 뒤 CodeQL 결과를 확인합니다.

> [!NOTE]
> CodeQL은 인젝션 같은 알려진 취약 패턴을, 리뷰어 에이전트는 인가 누락 같은 비즈니스 로직 결함을 맡습니다.

## 5. 완료 확인

```bash
scripts/verify-step.sh S4
```

## 막히면

* `scripts/checkpoint.sh S3`
* CodeQL을 쓸 수 없는 환경이면 강사 화면의 데모 PR로 확인합니다.

## 업계 공통 패턴

작성자와 분리된 리뷰, 결정적 보안 스캔. [bp-catalog](../bp-catalog/README.md) 참고.
