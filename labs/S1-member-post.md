---
title: S1 회원·게시글 (30분)
description: 테스트가 구현보다 먼저 오고, 구현자가 테스트를 바꾸지 못하게 합니다
---

## 목표

테스트가 구현보다 먼저 오고, 구현자가 테스트를 바꾸지 못하게 합니다.

## 추가 요건

[requirements/01-member-post.md](../requirements/01-member-post.md): 회원 가입, 글 작성·목록, 피드 화면 뼈대.

## 1. 하네스 없이 시도 (5분)

```text
requirements/01-member-post.md 의 회원·게시글 기능 만들고 테스트 다 통과시켜줘.
```

## 2. 관찰

* 테스트 없이 "완료"를 보고했나요?
* 실패하던 테스트를 구현에 맞춰 고친 흔적이 있나요?

확인이 끝나면 변경을 버립니다.

## 3. 하네스 추가 (17분)

1. awesome-copilot에서 TDD 관련 에이전트·스킬을 찾아 출발점으로 복사합니다 (4분). `TODO(verify): 에셋 이름 확정`
2. `.github/skills/tdd/SKILL.md`를 작성합니다 (8분).
   * frontmatter: `name: tdd`, `description: 기능 구현 요청 시 실패하는 테스트부터 작성하는 절차`
   * 본문: RED → GREEN → REFACTOR, 테스트 위치(`backend/tests/<pkg>/test_*.py`), 커밋 순서, 테스트를 통과시키려고 테스트를 수정하지 않는다
3. 커스텀 에이전트 2개를 작성합니다 (5분).
   * `.github/agents/test-writer.agent.md`: 수용 기준을 pytest로 옮김. `backend/tests/**`, `frontend/src/**/*.test.tsx`만 수정
   * `.github/agents/implementer.agent.md`: 실패 테스트를 통과시키는 최소 구현. 테스트 수정 금지, 테스트가 틀렸다고 판단되면 멈추고 보고

## 4. 같은 요청 재실행 (8분)

`test-writer`로 테스트를 작성·커밋한 뒤 `implementer`로 구현·커밋합니다. 피드 화면 뼈대(회원 선택, 글쓰기, 글 목록)까지 만듭니다.

## 5. 완료 확인

```bash
scripts/verify-step.sh S1
```

## 막히면

`scripts/checkpoint.sh S0`으로 S0 정답에서 다시 시작합니다.

## 업계 공통 패턴

TDD 강제, 역할 분리. [bp-catalog](../bp-catalog/README.md) 참고.
