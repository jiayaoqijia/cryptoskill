#!/bin/bash
# Validate an arb opportunity before execution
# Usage: ./validate-arb.sh <SYMBOL> <LONG_EX> <SHORT_EX> <SIZE_USD> [--leverage N]
# Performs: price check, liquidity check, balance check, risk check, dry-run via 'arb exec'
# Returns JSON validation report
# NOTE: For spot+perp arb, pass spot:<exch> as LONG_EX (e.g. spot:hl).

set -euo pipefail

# Auto-detect perp command (supports npx fallback for agents without install permissions)
if command -v perp &>/dev/null; then
  PERP="perp"
else
  PERP="npx -y perp-cli@latest"
fi

# perp exits 1 on {"ok":false} and prints exactly one JSON document: capture it as-is
# (never append a fallback document); empty output (crash / not installed) → {"ok":false}.
pj() { local out; out=$($PERP "$@" 2>/dev/null) || true; if [[ -n "$out" ]]; then printf '%s\n' "$out"; else echo '{"ok":false}'; fi; }
isok() { jq -e '.ok == true' >/dev/null 2>&1 <<<"$1"; }

SYM="${1:?Usage: validate-arb.sh <SYMBOL> <LONG_EX> <SHORT_EX> <SIZE_USD> [--leverage N]}"
LONG_EX="${2:?Usage: validate-arb.sh <SYMBOL> <LONG_EX> <SHORT_EX> <SIZE_USD>}"
SHORT_EX="${3:?Usage: validate-arb.sh <SYMBOL> <LONG_EX> <SHORT_EX> <SIZE_USD>}"
SIZE="${4:?Usage: validate-arb.sh <SYMBOL> <LONG_EX> <SHORT_EX> <SIZE_USD>}"
LEVERAGE=""

shift 4
while [[ $# -gt 0 ]]; do
  case "$1" in
    --leverage) LEVERAGE="$2"; shift 2 ;;
    *) shift ;;
  esac
done

checks=()
pass=true

add_result() {
  local name="$1" ok="$2" detail="$3"
  checks+=("{\"check\":\"$name\",\"ok\":$ok,\"detail\":\"$detail\"}")
  if [[ "$ok" == "false" ]]; then pass=false; fi
}

# Venue of the long leg (spot:<venue> → <venue>) for the per-venue reads below
LONG_VENUE="${LONG_EX#spot:}"
# portfolio -e accepts only full venue ids (no aliases)
venue_id() {
  case "$1" in
    pac) echo pacifica ;; hl) echo hyperliquid ;; lt) echo lighter ;; lrh|rh) echo lighter-rh ;;
    ast) echo aster ;; ondo-perps) echo ondo ;; qf) echo qfex ;; *) echo "$1" ;;
  esac
}

# 1. Price comparison — both exchanges must report similar prices
LONG_PRICE=$(pj --json -e "$LONG_VENUE" market mid "$SYM" | jq -r '.data.mid // "0"' 2>/dev/null || echo 0)
SHORT_PRICE=$(pj --json -e "$SHORT_EX" market mid "$SYM" | jq -r '.data.mid // "0"' 2>/dev/null || echo 0)

if [[ "$LONG_PRICE" == "0" || "$SHORT_PRICE" == "0" ]]; then
  add_result "price" "false" "Cannot fetch price: long=$LONG_PRICE short=$SHORT_PRICE"
else
  # Check deviation
  DEVIATION=$(echo "$LONG_PRICE $SHORT_PRICE" | awk '{d=($1-$2)/$2*100; print (d<0?-d:d)}')
  if (( $(echo "$DEVIATION > 5" | bc -l) )); then
    add_result "price" "false" "Price deviation ${DEVIATION}% > 5% — possible wrong token"
  else
    add_result "price" "true" "long=$LONG_PRICE short=$SHORT_PRICE dev=${DEVIATION}%"
  fi
fi

# 2. Balance check on both exchanges
LONG_BAL=$(pj --json portfolio -e "$(venue_id "$LONG_VENUE")" | jq -r '.data.exchanges[0].perp.available // .data.exchanges[0].perp.equity // "0"' 2>/dev/null || echo 0)
SHORT_BAL=$(pj --json portfolio -e "$(venue_id "$SHORT_EX")" | jq -r '.data.exchanges[0].perp.available // .data.exchanges[0].perp.equity // "0"' 2>/dev/null || echo 0)

NEEDED=$(echo "$SIZE" | awk '{print $1}')
if (( $(echo "$LONG_BAL < $NEEDED" | bc -l 2>/dev/null || echo 1) )); then
  add_result "balance_long" "false" "$LONG_EX balance $LONG_BAL < needed $NEEDED"
else
  add_result "balance_long" "true" "$LONG_EX balance=$LONG_BAL"
fi
if (( $(echo "$SHORT_BAL < $NEEDED" | bc -l 2>/dev/null || echo 1) )); then
  add_result "balance_short" "false" "$SHORT_EX balance $SHORT_BAL < needed $NEEDED"
else
  add_result "balance_short" "true" "$SHORT_EX balance=$SHORT_BAL"
fi

# 3. Market info (symbol availability)
LONG_INFO=$(pj --json -e "$LONG_VENUE" market info "$SYM")
SHORT_INFO=$(pj --json -e "$SHORT_EX" market info "$SYM")

if isok "$LONG_INFO" && isok "$SHORT_INFO"; then
  add_result "market_info" "true" "Both exchanges support $SYM"
else
  add_result "market_info" "false" "Symbol $SYM not available on one or both exchanges"
fi

# 4. Risk pre-check (risk check requires --leverage; default 1x when not given)
LEV_FLAG=""
[[ -n "$LEVERAGE" ]] && LEV_FLAG="--leverage $LEVERAGE"
RISK_CHECK=$(pj --json risk check --notional "$SIZE" --leverage "${LEVERAGE:-1}")
if isok "$RISK_CHECK" && [[ "$(jq -r '.data.allowed' <<<"$RISK_CHECK" 2>/dev/null || true)" == "true" ]]; then
  add_result "risk" "true" "Within risk limits"
else
  RISK_WHY=$(jq -r '.data.reason // .error.code // "unknown"' <<<"$RISK_CHECK" 2>/dev/null || echo unknown)
  add_result "risk" "false" "Risk check failed: $RISK_WHY"
fi

# 5. Dry-run
DRY_RUN=$(pj --json --dry-run arb exec "$SYM" "$LONG_EX" "$SHORT_EX" "$SIZE" $LEV_FLAG)
if isok "$DRY_RUN"; then
  add_result "dry_run" "true" "Dry-run succeeded"
else
  DRY_ERR=$(jq -r '.error.code // "unknown"' <<<"$DRY_RUN" 2>/dev/null || echo unknown)
  add_result "dry_run" "false" "Dry-run failed: $DRY_ERR"
fi

# Output
CHECKS_JSON=$(IFS=,; echo "${checks[*]}")
cat <<EOF
{
  "ok": true,
  "symbol": "$SYM",
  "longExchange": "$LONG_EX",
  "shortExchange": "$SHORT_EX",
  "sizeUsd": $SIZE,
  "allPassed": $pass,
  "checks": [$CHECKS_JSON]
}
EOF
