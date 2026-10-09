#!/usr/bin/env bash
# Installs workshop tooling. Target: ready within 10 minutes (use Codespaces prebuild).
set -euo pipefail

echo "==> uv"
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

echo "==> GitHub Copilot CLI"
npm install -g @github/copilot

echo "==> spec-kit (specify CLI)"
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

echo "==> backend dependencies"
(cd backend && uv sync)

echo "==> frontend dependencies"
(cd frontend && if [ -f package-lock.json ]; then npm ci; else npm install; fi)

chmod +x scripts/*.sh

echo "==> done. Check: copilot --version / uv --version / node -v / specify --help"
