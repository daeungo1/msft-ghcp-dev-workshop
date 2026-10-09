---
title: S0 Spec (25분)
description: 앱의 원칙과 범위를 먼저 정해 이후 모든 요청의 구조와 스타일을 고정합니다
---

## 목표

앱의 원칙과 범위를 먼저 정해, 이후 모든 요청의 구조·스타일을 고정합니다.

## 추가 요건

[requirements/00-vision.md](../requirements/00-vision.md): TeamFeed 비전, 기술 스택, MVP 4개 기능.

## 1. 하네스 없이 시도 (3분)

같은 기능을 두 번, 서로 다른 문장으로 요청합니다.

```text
회원 가입 API 만들어줘.
```

```text
FastAPI로 회원 등록 엔드포인트를 추가해줘.
```

## 2. 관찰

* 패키지 구조, 파일 이름, 오류 응답 형식이 두 번의 결과에서 같은가요?
* 테스트가 함께 만들어졌나요?

확인이 끝나면 변경을 버립니다.

```bash
git restore . && git clean -fd
```

## 3. 하네스 추가 (19분)

1. spec-kit 초기화 (4분) `TODO(verify): --here 지원 여부와 생성 위치`

   ```bash
   specify init --here --integration copilot
   ```

2. `/speckit-constitution`으로 우리 BP를 작성합니다 (8분). 최소 5개 원칙을 넣습니다.
   * 패키지 경계: 다른 패키지는 `app.<pkg>.api`만 import
   * 테스트 먼저: 구현 전에 실패하는 테스트를 커밋
   * 인가: 상태를 바꾸는 API는 인가 의존성을 명시하고 403 테스트로 확인
   * DB 접근: 스키마는 추측하지 말고 도구로 확인, 쓰기는 repository를 통해서만
   * 범위: 요청 범위 밖 파일은 수정하지 않고 먼저 제안
   * 응답 형식: 오류는 `{"error": {"code", "message"}}`
3. `/speckit-specify` → `/speckit-plan` → `/speckit-tasks`로 MVP 범위를 정의합니다 (7분). 구현은 S1부터 합니다.
4. `.github/copilot-instructions.md`와 `AGENTS.md`를 작성합니다.
   * copilot-instructions.md: 스택, 실행·테스트 명령, 패키지 경계 요약, 코드 스타일
   * AGENTS.md: 에이전트 행동 원칙 4개(가정은 말하고 시작, 가장 단순한 해법, 요청 범위만 수정, 검증 기준 먼저)와 테스트 명령

## 4. 같은 요청 재실행 (3분)

1번 프롬프트를 그대로 다시 실행하고 구조가 일관되는지 확인한 뒤 변경을 버립니다.

## 5. 완료 확인

```bash
scripts/verify-step.sh S0
```

## 막히면

* `scripts/checkpoint.sh S0`으로 정답 상태에서 다음 단계를 시작합니다.
* spec-kit 명령이 보이지 않으면 [troubleshooting](../facilitator/troubleshooting.md)을 확인합니다.

## 업계 공통 패턴

에이전트 행동 원칙, 스펙 주도 개발. [bp-catalog](../bp-catalog/README.md) 참고.
