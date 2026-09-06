#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

if ! command -v bun >/dev/null 2>&1; then
  echo "[ERROR] bun is required. Install bun first: https://bun.sh"
  exit 1
fi

bun run bootstrap -- "$@"
