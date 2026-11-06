---
name: tdd
description: "Use when: implementing a feature or bug fix with a failing test first, minimal code, and fresh verification evidence."
---

# Test-Driven Development

## 절차

1. 수용 기준 하나를 실제 공개 동작을 검증하는 테스트 하나로 옮깁니다.
2. 테스트를 실행해 기대한 이유로 실패하는지 확인합니다.
3. 실패 증거를 남긴 뒤 통과시키는 최소 구현을 작성합니다.
4. 대상 테스트와 전체 테스트를 실행합니다.
5. 중복만 정리하고 전체 테스트를 다시 실행합니다.

## 금지

* 구현에 맞춰 기존 테스트의 기대값을 변경하는 일
* 실패를 확인하지 않은 테스트로 TDD를 완료했다고 보고하는 일
* 실행하지 않은 명령을 통과했다고 보고하는 일

## 완료 보고

RED 명령과 실패 이유, GREEN 명령과 통과 수, 변경 파일을 보고합니다.
