---
name: convergence-check
description: "Use when: checking current code against constitution, spec, plan, tasks, and fresh verification evidence after implementation."
---

# Convergence Check

## 절차

1. constitution, spec, plan, tasks에서 검증 가능한 의도를 추출합니다.
2. 체크박스 상태가 아니라 현재 코드와 테스트 결과를 확인합니다.
3. 누락, 부분 구현, 명세 위반, 요청되지 않은 구현을 구분합니다.
4. 남은 차이를 추적 가능한 작업으로 기록합니다.
5. 저장소의 전체 품질 게이트를 실행합니다.

## 완료 기준

* 모든 수용 기준에 실행 증거가 있습니다.
* 남은 차이가 없거나 후속 작업으로 기록됐습니다.
* 특정 모델이 없어도 같은 계약으로 검증할 수 있습니다.
