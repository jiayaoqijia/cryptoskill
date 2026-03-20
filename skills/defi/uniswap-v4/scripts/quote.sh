#!/usr/bin/env bash
# quote.sh — Find all Uniswap V4 pools for a token pair (read-only, no gas)
# Usage: ./quote.sh --token0 <addr|ETH> --token1 <addr|ETH> [--chain base|ethereum]
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="$HOME/.foundry/bin:$PATH"

exec python3 "$SKILL_DIR/scripts/v4_read.py" find-pool "$@"
