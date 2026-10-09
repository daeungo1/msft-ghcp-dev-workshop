#!/usr/bin/env bash
# 훅 스크립트를 fixture로 검사합니다. Copilot 없이 로컬에서 바로 실행할 수 있습니다.
# Usage: scripts/hooks/test_hooks.sh
set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || exit 1

PASS=0
FAIL=0

expect() {
  local fixture="$1" want="$2" got
  got=$(scripts/hooks/pre_tool_guard.sh < "scripts/hooks/fixtures/${fixture}" | python3 -c "
import json, sys
print(json.load(sys.stdin).get('permissionDecision', 'allow'))")
  if [ "$got" = "$want" ]; then
    echo "✅ ${fixture} → ${got}"
    PASS=$((PASS + 1))
  else
    echo "❌ ${fixture}: expected ${want}, got ${got:-<no output>}"
    FAIL=$((FAIL + 1))
  fi
}

expect forbidden-edit.json deny
expect allowed-edit.json allow
expect dangerous-bash.json deny
expect force-push.json deny
expect safe-bash.json allow
expect outside-repo-edit.json deny

echo "----"
echo "passed: ${PASS}, failed: ${FAIL}"
[ "$FAIL" -eq 0 ]
