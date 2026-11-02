---
title: Capability-Based Model Routing
description: TeamFeed v0.2에서 역할 역량, 비용, 독립성에 따라 모델을 선택하는 기준
ms.date: 2026-11-02
ms.topic: concept
---

## Principle

모델은 저장소 계약이 아니라 런타임 자원입니다. Agent 파일과 workflow는
역할의 입력, 출력, 검증 기준을 정의하고 특정 모델 이름을 요구하지 않습니다.

## Role matrix

| 역할 | 우선 역량 | 산출물 | 필수 검증 |
|---|---|---|---|
| Researcher | 긴 컨텍스트, 최신 자료, 출처 추적 | 근거와 미확인 가정 | 파일 경로와 공식 URL |
| Planner | 제약 통합, 작업 분해 | plan, tasks | 요구사항 추적성 |
| Test writer | 정밀한 수용 기준 해석 | 실패 테스트 | 예상 이유의 RED |
| Implementer | 저장소 이해, 타입 안전성 | 최소 구현 | targeted와 full GREEN |
| Reviewer | 독립 추론, 적대적 검토 | 증거 기반 findings | 작성자와 분리된 맥락 |
| Convergence reviewer | 전체 범위 대조 | 남은 tasks 또는 clean result | spec-to-code mapping |

## Multi-model rules

* 작성자와 리뷰어는 가능하면 다른 모델 또는 새 컨텍스트를 사용합니다.
* 빠른 모델은 파일 탐색과 반복 검증에 사용합니다.
* 긴 컨텍스트 모델은 여러 명세와 코드 경계를 동시에 대조할 때 사용합니다.
* 고추론 모델은 설계 trade-off, 보안 검토, 최종 수렴 판단에 우선합니다.
* 모델 변경 후에도 동일한 테스트와 품질 게이트를 실행합니다.

## Fusion and ensemble models

Fusion 또는 ensemble 모델은 여러 추론 경로를 결합할 수 있지만 저장소가
그 내부 동작을 검증할 수는 없습니다. 다음 조건에서 선택형으로 사용합니다.

* 클라이언트가 해당 모델 ID를 공식적으로 노출
* 조직 정책과 비용 한도에서 허용
* 실패와 fallback이 사용자에게 표시
* 같은 repository tests와 convergence gate를 통과

2026-11-02 조사에서는 "GitHub Copilot HydraFusion"을 공식 GitHub 또는
Microsoft 제품 계약으로 확인하지 못했습니다. 공개 검색의 HydraFusion은
동명의 센서 융합 연구 프로젝트를 가리킵니다.

따라서 HydraFusion이 현재 클라이언트에서 선택 가능하더라도 다음 위치에는
고정하지 않습니다.

* `.agent.md`의 필수 `model` frontmatter
* Spec Kit workflow와 bundle manifest
* CI와 acceptance criteria
* 테스트 기대값

## Failure handling

선택한 모델을 사용할 수 없으면 다음 순서를 따릅니다.

1. 모델 선택 실패를 명시적으로 보고합니다.
2. 같은 역할 계약을 만족하는 지원 모델을 선택합니다.
3. 독립 리뷰가 필요한 역할은 작성자와 다른 컨텍스트를 유지합니다.
4. 모든 검증 명령을 다시 실행합니다.

모델 fallback은 품질 게이트 fallback이 아닙니다.

