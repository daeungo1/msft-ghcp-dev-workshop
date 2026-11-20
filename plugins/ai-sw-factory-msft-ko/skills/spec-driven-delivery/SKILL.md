---
name: spec-driven-delivery
description: "Use when: taking an application feature from constitution and specification through planning, TDD implementation, independent review, and convergence."
---

# Spec-Driven Application Delivery

## Prerequisite

이 plugin은 Spec Kit core를 복사하지 않고 team policy를 overlay합니다.
Repository에 `.specify/`와 Copilot의 `speckit-*` skills가 없으면 구현을
시작하지 않고 다음 초기화 명령을 안내합니다.

```bash
uv tool install specify-cli --force \
  --from git+https://github.com/github/spec-kit.git@v1.2.5
specify init --here --force --integration copilot
```

## 단계

1. Constitution: 프로젝트 전반의 품질, 보안, 경계 원칙을 확인합니다.
2. Specify: 사용자 시나리오, 수용 기준, 비목표를 작성합니다.
3. Clarify: 구현 방향을 바꾸는 모호함을 해소하고 교육용/production 목표,
   데이터 민감도, 사용자 규모, 운영 환경을 구분합니다.
4. Plan: `team-application-standards`와 그 application profile 결정표를 적용해
   기존 stack 유지/변경 근거, runtime lifecycle, module/service boundary,
   필요한 architecture 추출 범위, 인증/데이터/운영 요구와 검증 전략을
   기록합니다. 미결정 production 요건은 release blocker로 남깁니다.
5. Tasks: 실패 테스트, 최소 구현, 독립 리뷰 순서로 작업을 분해합니다.
6. Implement: one module/service or one use case 단위로 TDD를 실행합니다.
7. Verify: 테스트, lint, build, 보안과 경계 검사를 실행합니다. Hook이 실제
   로딩됐는지, 프로젝트 post-edit 검사가 설정됐는지 따로 확인합니다.
   빠른 hook 검사와 전체 CI/release gate의 증거를 구분합니다.
8. Converge: 명세와 현재 코드의 차이를 확인하고 남은 작업을 반복합니다.
9. Package: 반복 가능한 규칙과 절차를 plugin 자산으로 추출합니다.

## Human gates

Spec 승인, plan 승인, 테스트 계약 승인, 최종 수렴 승인에서는 사람이
산출물을 검토합니다. 자동화는 이 승인 단계를 성공으로 가정하지 않습니다.
