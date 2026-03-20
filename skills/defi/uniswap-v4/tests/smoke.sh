#!/usr/bin/env bash
# Smoke test for Uniswap V4 skill
# Tests read operations live on Base mainnet
set -uo pipefail
export PATH="$HOME/.foundry/bin:$PATH"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PASS=0
FAIL=0

pass() { echo "  ✅ $1"; PASS=$((PASS+1)); }
fail() { echo "  ❌ $1"; FAIL=$((FAIL+1)); }

echo "[smoke] === Uniswap V4 Skill Smoke Test ==="
echo ""

# ── 0. Prerequisites ──
echo "[smoke] prerequisites"
command -v cast >/dev/null && pass "cast installed" || fail "cast not found"
command -v python3 >/dev/null && pass "python3 installed" || fail "python3 not found"
command -v jq >/dev/null && pass "jq installed" || fail "jq not found"

# ── 1. Pool Info (Base ETH/USDC) ──
echo "[smoke] pool-info ETH/USDC on Base"
USDC="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
POOL_JSON=$(./scripts/pool-info.sh --token0 ETH --token1 "$USDC" --chain base 2>/dev/null)
if echo "$POOL_JSON" | jq -e '.success == true' >/dev/null 2>&1; then
  pass "pool-info returns success"
  FEE=$(echo "$POOL_JSON" | jq -r '.fee')
  TICK=$(echo "$POOL_JSON" | jq -r '.tick')
  LIQ=$(echo "$POOL_JSON" | jq -r '.liquidity')
  echo "    Fee: $FEE | Tick: $TICK | Liquidity: $LIQ"
else
  fail "pool-info failed"
fi

# ── 2. Quote (find all pools) ──
echo "[smoke] quote ETH/USDC on Base"
QUOTE_JSON=$(./scripts/quote.sh --token0 ETH --token1 "$USDC" --chain base 2>/dev/null)
if echo "$QUOTE_JSON" | jq -e '.success == true' >/dev/null 2>&1; then
  POOL_COUNT=$(echo "$QUOTE_JSON" | jq '.pools | length')
  pass "quote found $POOL_COUNT pools"
else
  fail "quote failed"
fi

# ── 3. Input validation (PT-001) ──
echo "[smoke] input validation"
# Test that injection attempts are rejected
OUT=$(./scripts/swap.sh --token-in ETH --token-out "$USDC" --amount 'a[$(touch /tmp/pwned)]' --chain base --json 2>&1 || true)
if echo "$OUT" | grep -q "must be a non-negative integer" 2>/dev/null; then
  pass "arithmetic injection blocked"
else
  fail "arithmetic injection NOT blocked"
fi

# Test slippage injection
OUT=$(./scripts/swap.sh --token-in ETH --token-out "$USDC" --amount 1000 --slippage 'a[$(id)]' --chain base --json 2>&1 || true)
if echo "$OUT" | grep -q "must be a non-negative integer" 2>/dev/null; then
  pass "slippage injection blocked"
else
  fail "slippage injection NOT blocked"
fi

# Test --private-key rejection
OUT=$(./scripts/swap.sh --token-in ETH --token-out "$USDC" --amount 1000 --private-key 0xDEAD --chain base --json 2>&1 || true)
if echo "$OUT" | grep -q "disabled for security" 2>/dev/null; then
  pass "--private-key rejected"
else
  fail "--private-key NOT rejected"
fi

# Test address validation
OUT=$(./scripts/swap.sh --token-in ETH --token-out "foo;rm -rf /" --amount 1000 --chain base --json 2>&1 || true)
if echo "$OUT" | grep -q "valid address" 2>/dev/null; then
  pass "address injection blocked"
else
  fail "address injection NOT blocked"
fi

# ── 4. Invalid chain ──
echo "[smoke] invalid chain handling"
OUT=$(./scripts/pool-info.sh --token0 ETH --token1 "$USDC" --chain solana 2>&1 || true)
if [[ "$OUT" != *"Traceback"* ]]; then
  pass "invalid chain doesn't expose traceback"
else
  fail "invalid chain exposes Python traceback"
fi

# ── 5. JSON output cleanliness ──
echo "[smoke] JSON output format"
# pool-info should output valid JSON only on stdout
POOL_STDOUT=$(./scripts/pool-info.sh --token0 ETH --token1 "$USDC" --chain base 2>/dev/null)
if echo "$POOL_STDOUT" | jq . >/dev/null 2>&1; then
  pass "pool-info stdout is clean JSON"
else
  fail "pool-info stdout is NOT clean JSON"
fi

# ── Summary ──
echo ""
echo "[smoke] Results: $PASS passed, $FAIL failed"
if [[ $FAIL -gt 0 ]]; then
  echo "[smoke] ❌ FAIL"
  exit 1
else
  echo "[smoke] ✅ OK"
fi
