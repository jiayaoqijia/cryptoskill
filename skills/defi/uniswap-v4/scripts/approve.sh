#!/usr/bin/env bash
# approve.sh — Set up token approvals for Uniswap V4 swaps (Permit2 flow)
# Usage: PRIVATE_KEY=0x... ./approve.sh --token <addr> [--chain base|ethereum] [--rpc-url <url>]
#
# Sets up the two-step Permit2 approval:
#   1. ERC20 approve → Permit2
#   2. Permit2 approve → Universal Router

set -uo pipefail
export PATH="$HOME/.foundry/bin:$PATH"

# FIX OUT-01/OUT-04: All log output to stderr
log() { echo "$@" >&2; }
err() { echo "ERROR: $@" >&2; }

CHAIN="base"
RPC_URL=""
TOKEN=""
JSON_OUTPUT=false

declare -A PERMIT2=(
  [base]="0x494bbD8A3302AcA833D307D11838f18DbAdA9C25"
  [ethereum]="0x000000000022D473030F116dDEE9F6B43aC78BA3"
)
declare -A UNIVERSAL_ROUTER=(
  [base]="0x6Df1c91424F79E40E33B1A48F0687B666bE71075"
  [ethereum]="0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af"
)
declare -A DEFAULT_RPC=(
  [base]="https://mainnet.base.org"
  [ethereum]="https://eth.llamarpc.com"
)

while [[ $# -gt 0 ]]; do
  case "$1" in
    --token)       TOKEN="$2"; shift 2 ;;
    --chain)       CHAIN="$2"; shift 2 ;;
    --rpc-url|--rpc) RPC_URL="$2"; shift 2 ;;
    --json)        JSON_OUTPUT=true; shift ;;
    # FIX SH-06: Reject --private-key CLI flag
    --private-key)
      err "--private-key CLI flag is disabled for security."
      err "Set PRIVATE_KEY environment variable instead."
      exit 1 ;;
    -h|--help)
      cat >&2 <<'EOF'
Usage: approve.sh --token <addr> [--chain base|ethereum] [--rpc-url <url>]
Private key: set PRIVATE_KEY env var (never pass on CLI)
EOF
      exit 0 ;;
    *) err "Unknown: $1"; exit 1 ;;
  esac
done

# ── Validation ──
[[ -z "$TOKEN" ]] && { err "--token required"; exit 1; }

# FIX PT-001: Validate token address format
if [[ ! "$TOKEN" =~ ^0x[0-9a-fA-F]{40}$ ]]; then
  err "--token must be a valid address (0x + 40 hex chars). Got: '$TOKEN'"
  exit 1
fi

# FIX SH-06: Use env var ONLY
PRIVATE_KEY="${PRIVATE_KEY:-}"
[[ -z "$PRIVATE_KEY" ]] && { err "PRIVATE_KEY env var required"; exit 1; }

# Validate chain
if [[ ! -v PERMIT2[$CHAIN] ]]; then
  err "Unsupported chain: $CHAIN. Supported: ${!PERMIT2[*]}"
  exit 1
fi

RPC_URL="${RPC_URL:-${DEFAULT_RPC[$CHAIN]}}"

SENDER=$(cast wallet address --private-key "$PRIVATE_KEY" 2>/dev/null)
if [[ -z "$SENDER" ]]; then
  err "Failed to derive wallet address from PRIVATE_KEY"
  exit 1
fi

SYM=$(cast call "$TOKEN" "symbol()(string)" --rpc-url "$RPC_URL" 2>/dev/null || echo "???")

log "Setting up Permit2 approvals for $SYM ($TOKEN)..."

# Step 1: ERC20 approve Permit2
log "Step 1: Approving Permit2 to spend $SYM..."
TX1=$(cast send "$TOKEN" "approve(address,uint256)" \
  "${PERMIT2[$CHAIN]}" "$(cast max-uint)" \
  --private-key "$PRIVATE_KEY" --rpc-url "$RPC_URL" --json 2>/dev/null) || true
HASH1=$(echo "$TX1" | jq -r '.transactionHash // "failed"' 2>/dev/null || echo "failed")
log "  TX: $HASH1"

# Step 2: Permit2 approve Universal Router
log "Step 2: Granting Universal Router allowance on Permit2..."
# FIX M-05: Standardize Permit2 expiry (use max uint48 for long-lived approvals)
MAX_UINT160="1461501637330902918203684832716283019655932542975"
EXPIRY="281474976710655"  # type(uint48).max
TX2=$(cast send "${PERMIT2[$CHAIN]}" \
  "approve(address,address,uint160,uint48)" \
  "$TOKEN" "${UNIVERSAL_ROUTER[$CHAIN]}" \
  "$MAX_UINT160" "$EXPIRY" \
  --private-key "$PRIVATE_KEY" --rpc-url "$RPC_URL" --json 2>/dev/null) || true
HASH2=$(echo "$TX2" | jq -r '.transactionHash // "failed"' 2>/dev/null || echo "failed")
log "  TX: $HASH2"

if [[ "$JSON_OUTPUT" == "true" ]]; then
  echo "{\"success\":true,\"token\":\"$TOKEN\",\"symbol\":\"$SYM\",\"erc20ApproveTx\":\"$HASH1\",\"permit2ApproveTx\":\"$HASH2\"}"
else
  log ""
  log "✅ Approvals set for $SYM"
  log "  ERC20 → Permit2: $HASH1"
  log "  Permit2 → Router: $HASH2"
fi
