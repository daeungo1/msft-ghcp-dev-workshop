---
description: Run TeamFeed harness, backend, frontend, boundary, and hook checks without hiding failures
---

# TeamFeed Verification

Run each gate from the repository root. Stop at the first failed gate, report
the command, exit code, and actionable error, then leave remaining gates
unreported rather than presenting a partial run as success.

## Gates

1. Run `python scripts/validate-harness.py`.
2. Run `cd backend && uv run pytest`.
3. Run `cd backend && uv run lint-imports`.
4. Run `cd frontend && npm test`.
5. Run `cd frontend && npm run build`.
6. Run `bash scripts/hooks/test_hooks.sh`.

## Completion report

Report every command that ran and its result. If the runtime lacks Python,
Node.js, uv, npm, or Bash, report the missing prerequisite as a blocked gate.
Do not replace a blocked result with a success-shaped fallback.

