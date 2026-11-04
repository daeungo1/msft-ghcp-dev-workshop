---
name: spec-driven-delivery
description: "Use when: taking an application feature from constitution and specification through planning, TDD implementation, independent review, and convergence."
---

# Spec-Driven Application Delivery

## 단계

1. Constitution: 프로젝트 전반의 품질, 보안, 경계 원칙을 확인합니다.
2. Specify: 사용자 시나리오, 수용 기준, 비목표를 작성합니다.
3. Clarify: 구현 방향을 바꾸는 모호함을 해소합니다.
4. Plan: `team-application-standards`를 적용해 runtime lifecycle, module/service
   boundary, Core/Application Use Cases/Ports/Adapters, migration seam,
   검증 전략을 기록합니다.
5. Tasks: 실패 테스트, 최소 구현, 독립 리뷰 순서로 작업을 분해합니다.
6. Implement: one module/service or one use case 단위로 TDD를 실행합니다.
7. Verify: 테스트, lint, build, 보안과 경계 검사를 실행합니다.
8. Converge: 명세와 현재 코드의 차이를 확인하고 남은 작업을 반복합니다.
9. Package: 반복 가능한 규칙과 절차를 plugin 자산으로 추출합니다.

## Human gates

Spec 승인, plan 승인, 테스트 계약 승인, 최종 수렴 승인에서는 사람이
산출물을 검토합니다. 자동화는 이 승인 단계를 성공으로 가정하지 않습니다.
