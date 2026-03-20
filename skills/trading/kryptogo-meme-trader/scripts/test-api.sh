#!/usr/bin/env bash
# KryptoGO Meme Trader — API Connectivity Test
#
# Tests key API endpoints to verify authentication and connectivity.
#
# Usage:
#   bash scripts/test-api.sh

set -euo pipefail

# Credentials must be pre-loaded in the environment (source ~/.openclaw/workspace/.env)
if [ -z "${KRYPTOGO_API_KEY:-}" ]; then
  echo "ERROR: Run 'source ~/.openclaw/workspace/.env' before running this script."
  exit 1
fi

BASE="https://wallet-data.kryptogo.app"
AUTH="Authorization: Bearer $KRYPTOGO_API_KEY"
PASS=0
FAIL=0

test_endpoint() {
    local name="$1"
    local url="$2"
    local code
    code=$(curl -s -o /dev/null -w "%{http_code}" "$url" -H "$AUTH")
    if [ "$code" = "200" ]; then
        echo "  ✓ $name (HTTP $code)"
        PASS=$((PASS + 1))
    else
        echo "  ✗ $name (HTTP $code)"
        FAIL=$((FAIL + 1))
    fi
}

echo "=== KryptoGO API Connectivity Test ==="
echo ""

test_endpoint "Account & Tier"     "$BASE/agent/account"
test_endpoint "Trending Tokens"    "$BASE/agent/trending-tokens?chain_id=501&page_size=1&sort_by=volume"
test_endpoint "Portfolio"          "$BASE/agent/portfolio?wallet_address=$SOLANA_WALLET_ADDRESS"
test_endpoint "Signal Dashboard"   "$BASE/signal-dashboard"

echo ""
echo "Results: $PASS passed, $FAIL failed"
