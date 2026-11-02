---
title: S6 수렴과 최종 검증 (20분)
description: 구현을 명세와 다시 대조하고 남은 작업이 없을 때만 완료로 판정합니다
---

| 항목 | 내용 |
|---|---|
| 시간 | 20분 (검증 5, converge 8, 재구현 5, 확인 2) |
| 도구 | Spec Kit 1.2.5, Copilot, 저장소 검증 명령 |
| 시작 상태 | S5 완료 |
| 완료 상태 | v0.2 baseline |
| 통제 방식 | 독립 수렴 검증 + human gate |
| 막는 함정 | 작업 체크박스와 테스트 일부만 보고 전체 완료로 판단 |

## 이 단계에서 배우는 것

* 테스트 통과는 작성된 테스트에 대해서만 사실입니다.
* `speckit-converge`는 spec, plan, tasks, constitution을 현재 코드와 다시
  대조합니다.
* 남은 차이는 기존 작업을 다시 쓰지 않고 convergence phase에 append합니다.
* 사람 승인은 검증과 수렴 결과를 읽은 뒤에만 수행합니다.

## 1. 전체 품질 게이트 실행

```bash
python scripts/validate-harness.py
cd backend && uv run pytest && uv run lint-imports
cd ../frontend && npm test && npm run build
cd ..
bash scripts/hooks/test_hooks.sh
```

도구가 없거나 실행이 차단되면 성공으로 간주하지 않습니다. blocked gate와
필요한 환경을 기록하고 지원 환경에서 다시 실행합니다.

## 2. 독립 리뷰

`convergence-reviewer`를 새 세션에서 선택합니다.

```text
현재 TeamFeed 구현을 spec.md, plan.md, tasks.md, constitution과 대조해줘.
체크박스를 믿지 말고 코드와 테스트 증거를 확인해줘.
```

작성자와 같은 모델을 사용하더라도 새 컨텍스트에서 실행합니다. 가능하면
다른 고추론 모델을 사용해 독립성을 높입니다.

## 3. Spec Kit convergence

Copilot 세션에서 실행합니다.

```text
/speckit-converge
```

결과를 두 가지로 나눕니다.

* `Converged`: `tasks.md`가 변경되지 않고 남은 차이가 없음
* Remaining work: 새 convergence phase와 추적 가능한 tasks가 append됨

남은 작업이 있으면 `/speckit-implement`를 실행하고 품질 게이트와 converge를
다시 수행합니다.

## 4. Delivery workflow

전체 과정을 새 기능에 반복할 때는 로컬 workflow를 사용합니다.

```bash
specify workflow run ./spec-kit/workflows/teamfeed-delivery \
  --input spec="Add the next TeamFeed capability"
```

Spec, plan, test contract, final acceptance gate에서 사람이 결과를 검토합니다.

## 5. 완료 확인

```bash
bash scripts/verify-step.sh S6
```

| 확인 항목 | 안 되면 |
|---|---|
| 하네스 구조 검증 통과 | `python scripts/validate-harness.py` 오류 확인 |
| `speckit-converge` skill 존재 | Spec Kit Copilot integration 재설치 |
| quality extension과 delivery workflow 설치 | S5 설치 명령 재실행 |
| 모델 이름이 필수 계약에 없음 | agent와 workflow의 `model` 고정 제거 |
| 전체 테스트와 경계 검사 통과 | 실패한 gate부터 수정 |

## 정리

* 완료는 구현자의 선언이 아니라 반복 가능한 검증 결과입니다.
* 모델을 바꿔도 spec, tests, boundaries, convergence 계약은 유지됩니다.
* extension, workflow, bundle은 팀의 검증 방법을 다른 저장소에 재사용하게
  합니다.

