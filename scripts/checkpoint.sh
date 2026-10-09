#!/usr/bin/env bash
# Usage: scripts/checkpoint.sh S<n>
# Moves you to the sN-done answer state on a new branch work/sN, so late participants can join the next step.
set -euo pipefail

STEP="${1:-}"
if ! [[ "$STEP" =~ ^S[0-5]$ ]]; then
  echo "Usage: $0 S0|S1|S2|S3|S4|S5"
  exit 2
fi

N="${STEP#S}"
BRANCH="s${N}-done"
WORK="work/s${N}"
UPSTREAM_URL="${WORKSHOP_UPSTREAM:-https://github.com/daeungo1/msft-ghcp-dev-workshop.git}"

if [ -n "$(git status --porcelain)" ]; then
  echo "==> stashing local changes"
  git stash push -u -m "checkpoint-before-${STEP}"
fi

if git show-ref --verify --quiet "refs/remotes/origin/${BRANCH}"; then
  REMOTE=origin
else
  if ! git remote get-url upstream >/dev/null 2>&1; then
    echo "==> adding upstream remote: ${UPSTREAM_URL}"
    git remote add upstream "$UPSTREAM_URL"
  fi
  REMOTE=upstream
fi

echo "==> fetching ${REMOTE}/${BRANCH}"
git fetch "$REMOTE" "$BRANCH"
git checkout -B "$WORK" "${REMOTE}/${BRANCH}"

echo "==> now on ${WORK} (${STEP} answer state). Continue with the next lab."
