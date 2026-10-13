#!/usr/bin/env bash
# 훅 스크립트를 fixture로 검사합니다. Copilot 없이 로컬에서 바로 실행할 수 있습니다.
# Usage: scripts/hooks/test_hooks.sh
set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || exit 1

# Python 실행체 자동 감지 (실제 동작 여부 검증)
PYTHON_BIN=""
if command -v python3 >/dev/null 2>&1 && python3 -c "import sys" >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1 && python -c "import sys" >/dev/null 2>&1; then
  PYTHON_BIN="python"
elif command -v py >/dev/null 2>&1 && py -c "import sys" >/dev/null 2>&1; then
  PYTHON_BIN="py"
else
  echo "Error: Python 인터프리터를 찾을 수 없습니다." >&2
  exit 1
fi

# 훅 스크립트 및 fixtures 경로 감지
HOOK_SCRIPT="scripts/hooks/pre_tool_guard.sh"
if [ ! -f "$HOOK_SCRIPT" ] && [ -f "templates/starter/s2/pre_tool_guard.skeleton.sh" ]; then
  HOOK_SCRIPT="templates/starter/s2/pre_tool_guard.skeleton.sh"
fi

FIXTURES_DIR="scripts/hooks/fixtures"
if [ ! -d "$FIXTURES_DIR" ] && [ -d "templates/starter/s2/fixtures" ]; then
  FIXTURES_DIR="templates/starter/s2/fixtures"
fi

PASS=0
FAIL=0

expect() {
  local fixture="$1" want="$2" got
  got=$("$HOOK_SCRIPT" < "${FIXTURES_DIR}/${fixture}" | "$PYTHON_BIN" -c "
import json, sys
if hasattr(sys.stdout, 'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
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
