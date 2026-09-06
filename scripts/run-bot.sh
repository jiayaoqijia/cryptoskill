#!/usr/bin/env bash
# Local and CI entry point. Publishing is a separate workflow step.
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHON_BIN="${CRYPTOSKILL_PYTHON:-python3}"
if [[ -z "${CRYPTOSKILL_PYTHON:-}" && -x .venv/bin/python ]]; then
  PYTHON_BIN=.venv/bin/python
fi
exec "$PYTHON_BIN" scripts/refresh-registry.py --fetch "$@"
