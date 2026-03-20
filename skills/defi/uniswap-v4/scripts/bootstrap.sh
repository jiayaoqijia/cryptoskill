#!/usr/bin/env bash
# bootstrap.sh — Check prerequisites for Uniswap V4 skill
set -euo pipefail

MISSING=0

check() {
  if command -v "$1" >/dev/null 2>&1; then
    echo "  ✅ $1 found: $(command -v "$1")"
  else
    echo "  ❌ $1 NOT found"
    echo "     Install: $2"
    MISSING=$((MISSING+1))
  fi
}

echo "[bootstrap] Checking Uniswap V4 skill prerequisites..."

# Foundry (cast)
export PATH="$HOME/.foundry/bin:$PATH"
check "cast" "curl -L https://foundry.paradigm.xyz | bash && foundryup"

# Python 3
check "python3" "apt install python3  (or brew install python3)"

# jq
check "jq" "apt install jq  (or brew install jq)"

if [[ $MISSING -gt 0 ]]; then
  echo ""
  echo "[bootstrap] ❌ Missing $MISSING prerequisite(s). Please install and re-run."
  exit 1
else
  echo ""
  echo "[bootstrap] ✅ All prerequisites met."
fi
