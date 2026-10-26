#!/bin/bash
# Validate an arb opportunity before execution
# Usage: ./validate-arb.sh <SYMBOL> <LONG_EX> <SHORT_EX> <SIZE_USD> [--leverage N]
# Performs: price check, liquidity check, balance check, risk check, dry-run via 'arb exec'
# Returns JSON validation report
# NOTE: For spot+perp arb, pass spot:<exch> as LONG_EX (e.g. spot:hl) — only for a scan row with
#       direction == "long-spot-short-perp" (arb exec spot: always buys spot + shorts the perp).

set -euo pipefail

# perp must be installed (no npx / auto-install path: the user decides what gets installed).
if ! command -v perp &>/dev/null; then
  echo "perp not found — ask the user to install perp-cli >= 0.16.0" >&2
  echo '{"ok":false,"error":{"code":"PERP_NOT_FOUND","message":"perp not found — ask the user to install perp-cli >= 0.16.0"}}'
  exit 1
fi
PERP="perp"

# perp exits 1 on {"ok":false} and prints exactly one JSON document: capture it as-is
# (never append a fallback document); empty output (crash) → an explicit NO_OUTPUT error document.
pj() { local out; out=$($PERP "$@" 2>/dev/null) || true; if [[ -n "$out" ]]; then printf '%s\n' "$out"; else echo '{"ok":false,"error":{"code":"NO_OUTPUT","message":"perp printed nothing (crashed?)"}}'; fi; }
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

# Venue of the long leg (spot:<venue> → <venue>) for the per-venue reads below.
# Aliases (hl, pac, lt, lrh, ast, …) are accepted everywhere, portfolio included.
LONG_VENUE="${LONG_EX#spot:}"
SPOT_MODE=false
[[ "$LONG_EX" == spot:* ]] && SPOT_MODE=true

# 1. Price comparison — both exchanges must report similar prices.
#    `market mid` reads the PERP book; there is no spot price read — in spot mode the long price
#    is the spot venue's perp mid (arb exec itself compares the spot and perp books and refuses
#    an empty book or a > 5% gap).
LONG_MID=$(pj --json -e "$LONG_VENUE" market mid "$SYM")
SHORT_MID=$(pj --json -e "$SHORT_EX" market mid "$SYM")
if ! isok "$LONG_MID" || ! isok "$SHORT_MID"; then
  add_result "price" "false" "Cannot fetch mid: long=$(jq -r '.error.code // .data.mid' <<<"$LONG_MID") short=$(jq -r '.error.code // .data.mid' <<<"$SHORT_MID")"
else
  LONG_PRICE=$(jq -r '.data.mid' <<<"$LONG_MID")
  SHORT_PRICE=$(jq -r '.data.mid' <<<"$SHORT_MID")
  DEVIATION=$(echo "$LONG_PRICE $SHORT_PRICE" | awk '{d=($1-$2)/$2*100; print (d<0?-d:d)}')
  if (( $(echo "$DEVIATION > 5" | bc -l) )); then
    add_result "price" "false" "Price deviation ${DEVIATION}% > 5% — possible wrong token"
  else
    add_result "price" "true" "long=$LONG_PRICE short=$SHORT_PRICE dev=${DEVIATION}%"
  fi
fi

# 2. Balances. Perp legs: portfolio .perp.available only (missing / unreadable = fail, never 0 or equity).
#    The comparison against the full SIZE is conservative (arb exec needs notional / leverage × buffer).
perp_available() {
  local out; out=$(pj --json portfolio -e "$1")
  if ! isok "$out"; then echo "ERROR:$(jq -r '.error.code' <<<"$out")"; return; fi
  jq -r '.data.exchanges[0].perp.available // "MISSING"' <<<"$out"
}
check_perp_balance() {
  local name="$1" venue="$2" bal; bal=$(perp_available "$venue")
  if [[ "$bal" == ERROR:* || "$bal" == "MISSING" ]]; then
    add_result "$name" "false" "$venue perp available unreadable ($bal)"
  elif (( $(echo "$bal < $SIZE" | bc -l) )); then
    add_result "$name" "false" "$venue perp available $bal < $SIZE"
  else
    add_result "$name" "true" "$venue perp available=$bal"
  fi
}
if $SPOT_MODE; then
  # Spot leg: needs spot quote balance (or perp funds the CLI transfers perp→spot on that venue).
  # The exact rule (shared vs separate spot margin, transfer shortfall) is enforced by the arb exec
  # dry-run below; here the spot balances are read so a read failure is surfaced.
  SPOT_BAL=$(pj --json -e "$LONG_VENUE" trade spot-balance)
  if isok "$SPOT_BAL"; then
    add_result "balance_spot" "true" "$LONG_VENUE spot balances: $(jq -c '[.data.balances[] | {token, available}]' <<<"$SPOT_BAL" | tr -d '"') — sufficiency checked by the dry-run"
  else
    add_result "balance_spot" "false" "$LONG_VENUE spot balance unreadable ($(jq -r '.error.code' <<<"$SPOT_BAL"))"
  fi
else
  check_perp_balance "balance_long" "$LONG_VENUE"
fi
check_perp_balance "balance_short" "$SHORT_EX"

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
  if isok "$RISK_CHECK"; then RISK_WHY=$(jq -r '.data.reason' <<<"$RISK_CHECK"); else RISK_WHY=$(jq -r '.error.code' <<<"$RISK_CHECK"); fi
  add_result "risk" "false" "Risk check failed: $RISK_WHY"
fi

# 5. Dry-run
DRY_RUN=$(pj --json --dry-run arb exec "$SYM" "$LONG_EX" "$SHORT_EX" "$SIZE" $LEV_FLAG)
if isok "$DRY_RUN"; then
  add_result "dry_run" "true" "Dry-run succeeded"
else
  DRY_ERR=$(jq -r '"\(.error.code): \(.error.message)"' <<<"$DRY_RUN" | tr -d '"\\')
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
