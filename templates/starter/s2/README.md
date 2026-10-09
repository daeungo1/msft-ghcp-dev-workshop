---
title: S2 스타터
description: S2에서 훅과 경계 검사를 만들 때 쓰는 스타터 파일 사용법
---

이 디렉터리의 파일은 정답이 아니라 출발점입니다. 아래 순서로 복사해 사용합니다.

| 파일 | 복사 위치 | 하는 일 |
|---|---|---|
| `pre_tool_guard.skeleton.sh` | `scripts/hooks/pre_tool_guard.sh` | preToolUse 훅. 규칙 목록(TODO 2곳)만 채우면 됩니다 |
| `post_edit_check.sh` | `scripts/hooks/post_edit_check.sh` | postToolUse 훅. 편집 직후 import-linter와 해당 패키지 테스트를 실행합니다 (완성본) |
| `fixtures/*.json` | `scripts/hooks/fixtures/` | 훅 입력 예시. 도구 호출 JSON이 이렇게 생겼다는 것을 보여 줍니다 |
| `test_hooks.sh` | `scripts/hooks/test_hooks.sh` | fixture로 훅을 검사합니다. Copilot 없이 실행됩니다 |

## 복사 명령

```bash
mkdir -p scripts/hooks/fixtures .github/hooks
cp templates/starter/s2/pre_tool_guard.skeleton.sh scripts/hooks/pre_tool_guard.sh
cp templates/starter/s2/post_edit_check.sh scripts/hooks/post_edit_check.sh
cp templates/starter/s2/test_hooks.sh scripts/hooks/test_hooks.sh
cp templates/starter/s2/fixtures/*.json scripts/hooks/fixtures/
chmod +x scripts/hooks/*.sh
```

## 훅 설정 파일

`.github/hooks/guardrails.json`에 아래 내용을 저장합니다. Copilot CLI와 Copilot cloud agent가 읽습니다.

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": [
      { "type": "command", "bash": "./scripts/hooks/pre_tool_guard.sh", "cwd": ".", "timeoutSec": 15 }
    ],
    "postToolUse": [
      { "type": "command", "bash": "./scripts/hooks/post_edit_check.sh", "cwd": ".", "timeoutSec": 60 }
    ]
  }
}
```

## 훅 입출력 계약 (요약)

| 항목 | 내용 |
|---|---|
| 입력 | stdin으로 JSON 한 개. `toolName`, `toolArgs`, `cwd`, postToolUse는 `toolResult`도 포함 |
| preToolUse 출력 | stdout에 `{"permissionDecision": "allow\|deny", "permissionDecisionReason": "..."}` 한 개. deny에는 사유가 필요합니다 |
| postToolUse 출력 | `{}` 또는 `{"additionalContext": "에이전트에게 돌려줄 메시지"}` |
| 실패 처리 | 명령 훅이 비정상 종료하면 preToolUse는 도구 실행을 막고, 시간 초과는 통과시킵니다 |

## import-linter 계약 작성 힌트

`backend/pyproject.toml`의 `[tool.importlinter]`에 `root_package = "app"`을 두고, 다른 도메인 패키지의 `models`, `repository`, `service`, `schemas`, `routes`를 import하지 못하게 하는 `forbidden` 계약을 만듭니다.
다른 패키지가 쓸 수 있는 입구는 `app.<패키지>.api` 하나뿐입니다.
계약의 모듈 목록에는 **현재 존재하는 패키지만** 적습니다. 없는 모듈을 적으면 린터가 오류를 냅니다.
