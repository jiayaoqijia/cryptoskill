#!/usr/bin/env bash
# pool-info.sh — Read Uniswap V4 pool state (price, tick, liquidity, fees)
# Usage: ./pool-info.sh --token0 <addr|ETH> --token1 <addr|ETH> [--fee <bps>] [--tick-spacing <int>] [--chain base|ethereum]
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
export PATH="$HOME/.foundry/bin:$PATH"

# Pass all args to Python reader
exec python3 "$SKILL_DIR/scripts/v4_read.py" pool-info "$@"
