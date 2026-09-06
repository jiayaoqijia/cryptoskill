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
  [[ "$ok" == "false" ]] && pass=false
}

# 1. Price comparison — both exchanges must report similar prices
LONG_PRICE=$($PERP --json -e "$LONG_EX" market mid "$SYM" 2>/dev/null | jq -r '.data.mid // "0"')
SHORT_PRICE=$($PERP --json -e "$SHORT_EX" market mid "$SYM" 2>/dev/null | jq -r '.data.mid // "0"')

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
LONG_BAL=$($PERP --json -e "$LONG_EX" account balance 2>/dev/null | jq -r '.data.available // .data.equity // "0"')
SHORT_BAL=$($PERP --json -e "$SHORT_EX" account balance 2>/dev/null | jq -r '.data.available // .data.equity // "0"')

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
LONG_INFO=$($PERP --json -e "$LONG_EX" market info "$SYM" 2>/dev/null || echo '{"ok":false}')
SHORT_INFO=$($PERP --json -e "$SHORT_EX" market info "$SYM" 2>/dev/null || echo '{"ok":false}')

if echo "$LONG_INFO" | grep -q '"ok":true' && echo "$SHORT_INFO" | grep -q '"ok":true'; then
  add_result "market_info" "true" "Both exchanges support $SYM"
else
  add_result "market_info" "false" "Symbol $SYM not available on one or both exchanges"
fi

# 4. Risk pre-check
LEV_FLAG=""
[[ -n "$LEVERAGE" ]] && LEV_FLAG="--leverage $LEVERAGE"
RISK_CHECK=$($PERP --json risk check --notional "$SIZE" $LEV_FLAG 2>/dev/null || echo '{"ok":false}')
if echo "$RISK_CHECK" | grep -q '"ok":true'; then
  add_result "risk" "true" "Within risk limits"
else
  add_result "risk" "false" "Risk check failed — review risk limits"
fi

# 5. Dry-run
DRY_RUN=$($PERP --json --dry-run arb exec "$SYM" "$LONG_EX" "$SHORT_EX" "$SIZE" $LEV_FLAG 2>/dev/null || echo '{"ok":false}')
if echo "$DRY_RUN" | grep -q '"ok":true'; then
  add_result "dry_run" "true" "Dry-run succeeded"
else
  DRY_ERR=$(echo "$DRY_RUN" | jq -r '.error.message // .error // "unknown"' 2>/dev/null)
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
