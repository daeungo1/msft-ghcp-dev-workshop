#!/usr/bin/env bash
# Usage: scripts/verify-step.sh S0|S1|S2|S3|S4|S5|ALL|--check-main
# 단계 완료 여부를 자동으로 확인합니다. 항목마다 ✅/❌ 와 힌트를 출력하고, 하나라도 실패하면 종료 코드 1을 반환합니다.
# ALL은 S0~S5 검사를 누적 실행합니다 (final 브랜치, 태그 v1.0 기준).
# 오프라인 환경에서는 VERIFY_UV_RUN="" 로 실행하면 `uv run` 없이 현재 PATH의 python 도구를 사용합니다.
set -uo pipefail

cd "$(git rev-parse --show-toplevel)" || exit 1

UVR="${VERIFY_UV_RUN-uv run}"
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
count_ge() { [ "$1" -ge "$2" ]; }

backend_tests() { (cd backend && $UVR pytest -q "$@"); }
frontend_tests() { (cd frontend && npm test --silent); }
import_contracts() { (cd backend && $UVR lint-imports); }
mcp_server_tests() {
  if [ -n "$UVR" ]; then uv run --with pytest pytest -q templates/mcp/sqlite-ro-server; else pytest -q templates/mcp/sqlite-ro-server; fi
}

# S1: posts 테스트 커밋이 posts 구현 커밋보다 먼저(또는 같은 시각)여야 합니다.
tests_before_impl() {
  local t a
  t=$(git log --reverse --format=%ct -- backend/tests/posts | head -n1)
  a=$(git log --reverse --format=%ct -- backend/app/posts | head -n1)
  [ -n "$t" ] && [ -n "$a" ] && [ "$t" -le "$a" ]
}

# 훅 스크립트에 fixture를 넣어 결정(permissionDecision)을 확인합니다.
hook_decision() {
  scripts/hooks/pre_tool_guard.sh < "$1" 2>/dev/null | python3 -c "
import json, sys
print(json.load(sys.stdin).get('permissionDecision', 'allow'))"
}
pre_hook_denies_forbidden() { [ "$(hook_decision scripts/hooks/fixtures/forbidden-edit.json)" = "deny" ]; }
pre_hook_allows_normal() { [ "$(hook_decision scripts/hooks/fixtures/allowed-edit.json)" = "allow" ]; }

reviewer_is_read_only() {
  local f=.github/agents/security-reviewer.agent.md
  [ -f "$f" ] && ! grep -Eiq '^\s*tools:.*\b(edit|write|create)\b' "$f"
}

no_string_built_sql() {
  ! grep -RnE '(f"|f'"'"').*(SELECT|LIKE|WHERE)|(SELECT|LIKE|WHERE).*"\s*\+|\.format\(' backend/app/reports
}

plugin_count() { find "$1" -name "$2" 2>/dev/null | wc -l; }

check_main() {
  for f in .github/copilot-instructions.md AGENTS.md .github/agents .github/skills .github/hooks .github/instructions .github/workflows .mcp.json .vscode/mcp.json Plan.md; do
    check "main has no ${f}" "하네스 파일은 sN-done 브랜치에만 있어야 합니다" absent "$f"
  done
}

check_s0() {
  check "constitution exists" "/speckit-constitution 을 실행하세요" exists .specify/memory/constitution.md
  check "spec/plan/tasks exist" "/speckit-specify, /speckit-plan, /speckit-tasks 를 실행하세요" \
    bash -c 'ls specs/*/spec.md specs/*/plan.md specs/*/tasks.md'
  check "constitution has >= 5 principles" "원칙을 5개 이상 적으세요 (## 또는 ### 제목 기준)" \
    count_ge "$(grep -cE '^###? ' .specify/memory/constitution.md 2>/dev/null || echo 0)" 5
  check ".github/copilot-instructions.md exists" "커스텀 인스트럭션을 작성하세요" exists .github/copilot-instructions.md
  check "AGENTS.md includes test command" "AGENTS.md 에 'uv run pytest' 를 적으세요" contains AGENTS.md 'pytest'
}

check_s1() {
  check "backend tests pass" "cd backend && uv run pytest" backend_tests
  check "frontend tests pass" "cd frontend && npm test" frontend_tests
  check "tdd skill exists" ".github/skills/tdd/SKILL.md 를 만드세요" exists .github/skills/tdd/SKILL.md
  check "test-writer agent exists" ".github/agents/test-writer.agent.md 를 만드세요" exists .github/agents/test-writer.agent.md
  check "implementer agent exists" ".github/agents/implementer.agent.md 를 만드세요" exists .github/agents/implementer.agent.md
  check "posts tests committed before implementation" "테스트를 먼저 커밋하세요 (test-writer → implementer)" tests_before_impl
}

check_s2() {
  check "import contracts pass" "cd backend && uv run lint-imports" import_contracts
  check "guardrails.json is valid JSON" ".github/hooks/guardrails.json 을 고치세요" json_valid .github/hooks/guardrails.json
  check "hooks use schema version 1" '"version": 1 을 추가하세요' json_has .github/hooks/guardrails.json 'd.get("version") == 1'
  check "hooks define preToolUse and postToolUse" "두 이벤트를 모두 추가하세요" \
    json_has .github/hooks/guardrails.json '"preToolUse" in d.get("hooks",{}) and "postToolUse" in d.get("hooks",{})'
  check "pre hook denies forbidden-edit fixture" "scripts/hooks/pre_tool_guard.sh 가 deny 를 출력해야 합니다" pre_hook_denies_forbidden
  check "pre hook allows allowed-edit fixture" "정상 편집까지 막으면 안 됩니다" pre_hook_allows_normal
  check "CI workflow present" "cp templates/workflows/ci.yml .github/workflows/" exists .github/workflows/ci.yml
}

check_s3() {
  check ".vscode/mcp.json defines sqlite-ro and github" "cp templates/mcp/vscode-mcp.json .vscode/mcp.json" \
    json_has .vscode/mcp.json '"sqlite-ro" in d.get("servers",{}) and "github" in d.get("servers",{})'
  check ".mcp.json defines sqlite-ro (Copilot CLI)" "cp templates/mcp/copilot-cli-mcp.json .mcp.json" \
    json_has .mcp.json '"sqlite-ro" in d.get("mcpServers",{})'
  check "sqlite-ro server tests pass" "uv run --with pytest pytest templates/mcp/sqlite-ro-server" mcp_server_tests
  check "feed tests pass" "cd backend && uv run pytest tests/feed" backend_tests tests/feed
}

check_s4() {
  check "security-reviewer agent is read-only" "security-reviewer 의 tools 에서 edit 계열을 빼세요" reviewer_is_read_only
  check "403 test exists for reports" "일반 회원의 PATCH → 403 테스트를 추가하세요" bash -c 'grep -Rq "403" backend/tests/reports'
  check "backend tests pass" "cd backend && uv run pytest" backend_tests
  check "no string-built SQL in reports" "SQLAlchemy 바인딩 파라미터를 쓰세요" no_string_built_sql
  check "CodeQL workflow present" "cp templates/workflows/codeql.yml .github/workflows/" exists .github/workflows/codeql.yml
}

check_s5() {
  local P=plugins/teamfeed-harness
  check "plugin.json is valid JSON" "${P}/plugin.json 을 고치세요" json_valid "${P}/plugin.json"
  check "plugin.json has \$schema/name/version/description" "필수 필드를 추가하세요" \
    json_has "${P}/plugin.json" 'all(k in d for k in ("$schema","name","version","description"))'
  check "plugin version bumped from 0.1.0" "version 을 0.2.0 으로 올리세요" json_has "${P}/plugin.json" 'd.get("version") != "0.1.0"'
  check "plugin has >= 2 skills" "tdd 와 내 팀 규칙 스킬을 넣으세요" count_ge "$(plugin_count "${P}/skills" SKILL.md)" 2
  check "plugin has 3 agents" "com.github.copilot/agents 에 3개를 넣으세요" count_ge "$(plugin_count "${P}/com.github.copilot/agents" '*.agent.md')" 3
  check "plugin has hooks.json (version 1)" "com.github.copilot/hooks/hooks.json 을 만드세요" \
    json_has "${P}/com.github.copilot/hooks/hooks.json" 'd.get("version") == 1 and "preToolUse" in d.get("hooks",{})'
  check "plugin has mcp.json" "${P}/mcp.json 을 만드세요" json_valid "${P}/mcp.json"
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
