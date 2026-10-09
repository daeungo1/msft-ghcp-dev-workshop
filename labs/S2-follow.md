---
title: S2 팔로우 (30분)
description: 문장 규칙이 아니라 결정적 장치로 모듈 경계와 위험 행동을 막습니다
---

> [!IMPORTANT]
> VS Code의 훅 지원은 프리뷰입니다. S2는 Copilot CLI로 진행합니다.

## 목표

문장 규칙이 아니라 결정적 장치로 모듈 경계와 위험 행동을 막습니다.

## 추가 요건

[requirements/02-follow.md](../requirements/02-follow.md): 팔로우, 언팔로우, 팔로잉 목록.

## 1. 하네스 없이 시도 (5분)

```text
requirements/02-follow.md 의 팔로우 기능을 구현해줘.
```

## 2. 관찰

* `follows` 패키지가 `members.repository`나 `members.models`를 직접 import하나요?
* constitution에 경계 규칙이 있는데도 위반이 생겼나요?

## 3. 하네스 추가 (18분)

1. `backend/pyproject.toml`에 import-linter 계약을 추가하고 `uv run lint-imports`로 위반을 확인합니다 (5분).

   ```toml
   [tool.importlinter]
   root_package = "app"

   [[tool.importlinter.contracts]]
   name = "domain packages import each other only via api"
   type = "forbidden"
   source_modules = ["app.follows", "app.posts", "app.feed", "app.reports"]
   forbidden_modules = ["app.members.repository", "app.members.models"]
   ```

2. `.github/hooks/guardrails.json`과 훅 스크립트 2개를 작성합니다 (10분). `TODO(verify): 훅 필드명과 입출력 형식`
   * `scripts/hooks/pre_tool_guard.sh`: `rm -rf`, `git push --force`, `git reset --hard`, 범위 밖 경로 편집, `.env`·`*.db` 편집을 거부
   * `scripts/hooks/post_edit_check.sh`: 편집된 패키지의 pytest와 `lint-imports`를 실행하고 실패 결과를 에이전트에 반환
3. CI 워크플로를 복사합니다 (3분).

   ```bash
   mkdir -p .github/workflows && cp templates/workflows/ci.yml .github/workflows/
   ```

## 4. 같은 요청 재실행 (7분)

Copilot CLI로 1번 프롬프트를 다시 실행합니다. 위반 시도가 훅에서 차단되고 `members/api.py`에 공개 함수를 추가하는 방향으로 수정되는지 확인합니다.

## 5. 완료 확인

```bash
scripts/verify-step.sh S2
```

## 막히면

* `scripts/checkpoint.sh S1`
* 훅이 동작하지 않으면 실행 권한(`chmod +x scripts/hooks/*.sh`)을 확인합니다.

## 업계 공통 패턴

위험 명령 차단, 결정적 경계 검사. [bp-catalog](../bp-catalog/README.md) 참고.
