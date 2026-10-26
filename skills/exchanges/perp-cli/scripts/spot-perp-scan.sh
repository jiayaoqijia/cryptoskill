#!/bin/bash
# Scan spot+perp (and perp-perp) funding rate arbitrage opportunities
# Usage: ./spot-perp-scan.sh [--json] [--mode all|spot-perp|perp-perp] [--min 10] [-n mainnet|testnet] [--no-portfolio]
# Combines the scan with balances (portfolio) and venue health (perp health).
# --no-portfolio: skip the balance read (no wallet needed); the output says it was skipped.
# Spot-perp rows: only direction == "long-spot-short-perp" is executable with `arb exec <SYM> spot:<venue> <perp>`.
# Testnet funding / spreads are not meaningful — use mainnet (the default) for yield analysis.

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

JSON_MODE=false
MODE="all"
MIN_SPREAD=10
NETWORK="mainnet"
WITH_PORTFOLIO=true
while [[ $# -gt 0 ]]; do
  case "$1" in
    --json) JSON_MODE=true; shift ;;
    --mode) MODE="$2"; shift 2 ;;
    --min) MIN_SPREAD="$2"; shift 2 ;;
    -n|--network) NETWORK="$2"; shift 2 ;;
    --no-portfolio) WITH_PORTFOLIO=false; shift ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done
PERP="perp -n $NETWORK"

# 1. Portfolio (balances). Explicitly skipped with --no-portfolio; a failed read aborts.
if $WITH_PORTFOLIO; then
  PORTFOLIO=$(pj --json portfolio)
  if ! isok "$PORTFOLIO"; then
    if $JSON_MODE; then
      jq -c '{ok:false, error:{code:.error.code, message:.error.message, source:"perp --json portfolio", remediation:"Check the wallet setup, or rerun with --no-portfolio to scan without balances"}}' <<<"$PORTFOLIO"
    else
      echo "ERROR: portfolio failed ($(jq -r '.error.code' <<<"$PORTFOLIO")). Check the wallet setup, or rerun with --no-portfolio." >&2
    fi
    exit 1
  fi
else
  PORTFOLIO='{"skipped":true,"reason":"--no-portfolio"}'
fi

# 2. Run appropriate scan
SCAN_RESULT=$(pj --json arb scan --mode "$MODE" --min "$MIN_SPREAD")

# 3. Venue health (data.healthy = every official-API venue is up)
HEALTH=$(pj --json health)

if $JSON_MODE; then
  cat <<EOF
{
  "ok": true,
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "network": "$NETWORK",
  "mode": "$MODE",
  "minSpread": $MIN_SPREAD,
  "portfolio": $PORTFOLIO,
  "scan": $SCAN_RESULT,
  "health": $HEALTH
}
EOF
else
  echo "=== Spot+Perp Arb Scanner ==="
  echo "Network: $NETWORK | Mode: $MODE | Min spread: ${MIN_SPREAD}% annual"
  echo ""

  echo "--- Balances ---"
  if $WITH_PORTFOLIO; then
    jq -r '.data.exchanges[] | "  \(.name): equity $\(.perp.equity) available $\(.perp.available)"' <<<"$PORTFOLIO"
  else
    echo "  (skipped: --no-portfolio)"
  fi
  echo ""

  echo "--- Opportunities ---"
  if isok "$SCAN_RESULT"; then
    jq -r '.data[] |
      if .mode == "spot-perp" then
        "  \(.symbol) | spot-perp | net \(.netSpread)%/yr | \(.direction) spot:\(.spotExchanges | join("/")) perp:\(.perpExchange)"
        + (if .direction == "long-spot-short-perp" then "" else "  [NOT executable with arb exec]" end)
      else
        "  \(.symbol) | perp-perp | net \(.netSpread)%/yr | long \(.longExch) / short \(.shortExch)"
      end' <<<"$SCAN_RESULT"
  else
    echo "  ERROR: arb scan failed: $(jq -r '"\(.error.code): \(.error.message)"' <<<"$SCAN_RESULT")"
  fi

  echo ""
  echo "--- Venue Health ---"
  if isok "$HEALTH"; then
    jq -r '"  healthy (official venues): \(.data.healthy)", (.data.exchanges[] | "  \(.exchange): \(.status)")' <<<"$HEALTH"
  else
    echo "  ERROR: perp health failed: $(jq -r '.error.code' <<<"$HEALTH")"
  fi
fi
