#!/usr/bin/env bash
# Usage: scripts/verify-step.sh S0|S1|S2|S3|S4|S5|ALL|--check-main
# ALL runs every S0-S5 check cumulatively (used on the `final` branch before tagging v1.0).
# Prints ✅/❌ per check with a hint, then a pass count. Exits 1 on any failure.
# TODO(build): refine checks once s0-done … s5-done / final branches exist.
set -uo pipefail

cd "$(git rev-parse --show-toplevel)" || exit 1

PASS=0
FAIL=0

check() {
  local name="$1" hint="$2"
  shift 2
  if "$@" >/dev/null 2>&1; then
    echo "✅ ${name}"
    PASS=$((PASS + 1))
  else
    echo "❌ ${name}  →  ${hint}"
    FAIL=$((FAIL + 1))
  fi
}

exists() { [ -e "$1" ]; }
absent() { [ ! -e "$1" ]; }
contains() { grep -Eq "$2" "$1"; }
json_valid() { python3 -c "import json,sys; json.load(open(sys.argv[1]))" "$1"; }
json_has() { python3 -c "import json,sys; d=json.load(open(sys.argv[1])); sys.exit(0 if eval(sys.argv[2]) else 1)" "$1" "$2"; }
backend_tests() { (cd backend && uv run pytest -q); }
frontend_tests() { (cd frontend && npm test --silent); }

tests_before_impl() {
  local t a
  t=$(git log --reverse --format=%ct -- backend/tests/posts | head -n1)
  a=$(git log --reverse --format=%ct -- backend/app/posts | head -n1)
  [ -n "$t" ] && [ -n "$a" ] && [ "$t" -le "$a" ]
}

pre_hook_denies_fixture() {
  local out
  out=$(scripts/hooks/pre_tool_guard.sh < scripts/hooks/fixtures/forbidden-edit.json 2>&1)
  local rc=$?
  [ $rc -ne 0 ] || echo "$out" | grep -qi "deny"
}

reviewer_is_read_only() {
  local f=.github/agents/security-reviewer.agent.md
  [ -f "$f" ] && ! grep -Eiq '^\s*tools:.*\b(edit|write|create)\b' "$f"
}

no_string_built_sql() {
  ! grep -RnE '(f"|f'"'"').*(SELECT|LIKE|WHERE)|(SELECT|LIKE|WHERE).*"\s*\+|\.format\(' backend/app/reports
}

count_ge() { [ "$1" -ge "$2" ]; }

check_main() {
  for f in .github/copilot-instructions.md AGENTS.md .github/agents .github/skills .github/hooks .github/instructions .github/workflows Plan.md; do
    check "main has no ${f}" "harness files must live only on sN-done branches" absent "$f"
  done
}

check_s0() {
  check "constitution exists" "run /speckit-constitution" exists .specify/memory/constitution.md
  check "spec/plan/tasks exist" "run /speckit-specify, /speckit-plan, /speckit-tasks" \
    bash -c 'ls specs/*/spec.md specs/*/plan.md specs/*/tasks.md'
  check "constitution has >= 5 principles" "add at least 5 principles" \
    count_ge "$(grep -cE '^###? ' .specify/memory/constitution.md 2>/dev/null || echo 0)" 5
  check ".github/copilot-instructions.md exists" "write custom instructions" exists .github/copilot-instructions.md
  check "AGENTS.md includes test command" "add 'uv run pytest' to AGENTS.md" contains AGENTS.md 'pytest'
}

check_s1() {
  check "backend tests pass" "cd backend && uv run pytest" backend_tests
  check "frontend tests pass" "cd frontend && npm test" frontend_tests
  check "tdd skill exists" "create .github/skills/tdd/SKILL.md" exists .github/skills/tdd/SKILL.md
  check "test-writer agent exists" "create .github/agents/test-writer.agent.md" exists .github/agents/test-writer.agent.md
  check "implementer agent exists" "create .github/agents/implementer.agent.md" exists .github/agents/implementer.agent.md
  check "posts tests committed before implementation" "commit tests first (test-writer → implementer)" tests_before_impl
}

check_s2() {
  check "import contracts pass" "cd backend && uv run lint-imports" bash -c 'cd backend && uv run lint-imports'
  check "guardrails.json is valid JSON" "fix .github/hooks/guardrails.json" json_valid .github/hooks/guardrails.json
  check "hooks define preToolUse and postToolUse" "add both hook events" \
    json_has .github/hooks/guardrails.json '"preToolUse" in d.get("hooks",{}) and "postToolUse" in d.get("hooks",{})'
  check "pre hook denies forbidden edit fixture" "check scripts/hooks/pre_tool_guard.sh" pre_hook_denies_fixture
  check "CI workflow present" "cp templates/workflows/ci.yml .github/workflows/" exists .github/workflows/ci.yml
}

check_s3() {
  check ".vscode/mcp.json defines sqlite-ro and github" "cp templates/mcp/vscode-mcp.json .vscode/mcp.json" \
    json_has .vscode/mcp.json '"sqlite-ro" in d.get("servers",{}) and "github" in d.get("servers",{})'
  check "sqlite-ro server tests pass" "uv run --with pytest pytest templates/mcp/sqlite-ro-server" \
    uv run --with pytest pytest -q templates/mcp/sqlite-ro-server
  check "feed tests pass" "cd backend && uv run pytest tests/feed" bash -c 'cd backend && uv run pytest -q tests/feed'
}

check_s4() {
  check "security-reviewer agent is read-only" "remove edit tools from security-reviewer" reviewer_is_read_only
  check "403 test exists for reports" "add a non-admin PATCH → 403 test" bash -c 'grep -Rq "403" backend/tests/reports'
  check "backend tests pass" "cd backend && uv run pytest" backend_tests
  check "no string-built SQL in reports" "use SQLAlchemy bound parameters" no_string_built_sql
  check "CodeQL workflow present" "cp templates/workflows/codeql.yml .github/workflows/" exists .github/workflows/codeql.yml
}

check_s5() {
  P=plugins/teamfeed-harness
  check "plugin.json is valid JSON" "fix ${P}/plugin.json" json_valid "${P}/plugin.json"
  check "plugin.json has name/version/description" "add required fields" \
    json_has "${P}/plugin.json" 'all(k in d for k in ("name","version","description"))'
  check "plugin version bumped from 0.1.0" "set version to 0.2.0" json_has "${P}/plugin.json" 'd.get("version") != "0.1.0"'
  check "plugin has >= 2 skills" "add tdd + your team rule" count_ge "$(find "${P}" -name SKILL.md 2>/dev/null | wc -l)" 2
  check "plugin has 3 agents" "add test-writer, implementer, security-reviewer" count_ge "$(find "${P}" -name '*.agent.md' 2>/dev/null | wc -l)" 3
  check "plugin has hook config" "add hooks/guardrails.json" bash -c "find '${P}' -name 'guardrails.json' | grep -q ."
}

case "${1:-}" in
  --check-main) check_main ;;
  S0) check_s0 ;;
  S1) check_s1 ;;
  S2) check_s2 ;;
  S3) check_s3 ;;
  S4) check_s4 ;;
  S5) check_s5 ;;
  ALL)
    # Cumulative S0-S5 check for the final branch (tagged v1.0).
    check_s0
    check_s1
    check_s2
    check_s3
    check_s4
    check_s5
    ;;
  *)
    echo "Usage: $0 S0|S1|S2|S3|S4|S5|ALL|--check-main"
    exit 2
    ;;
esac

echo "----"
echo "passed: ${PASS}, failed: ${FAIL}"
[ "$FAIL" -eq 0 ]
