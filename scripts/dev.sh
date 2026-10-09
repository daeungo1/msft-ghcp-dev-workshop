#!/usr/bin/env bash
# 백엔드(8000)와 프론트엔드(5173)를 함께 실행합니다. 종료는 Ctrl+C.
# Usage: scripts/dev.sh
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

if [ ! -f backend/app/main.py ]; then
  echo "backend/app/main.py 가 아직 없습니다. S1에서 회원·게시글 API를 구현한 뒤 실행하세요." >&2
  exit 1
fi

trap 'kill 0' EXIT
(cd backend && uv run fastapi dev app/main.py --port 8000) &
(cd frontend && npm run dev -- --host) &
wait
