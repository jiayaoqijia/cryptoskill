#!/usr/bin/env bash
# Install crypto-skill Python package into the current project's venv
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -q httpx pydantic

# Install the package from the skill's bundled source
pip install -q -e "$SCRIPT_DIR"

echo "crypto-skill installed. Set APIFY_API_TOKEN env var to use."
