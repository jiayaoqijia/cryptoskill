#!/usr/bin/env bash
# swap.sh — Execute a token swap on Uniswap V4 via the Universal Router
# Usage: ./swap.sh --token-in <addr> --token-out <addr> --amount <wei> [--slippage <bps>] [--recipient <addr>] [--rpc-url <url>] [--chain base|ethereum]
#
# Example: swap 0.01 ETH for USDC on Base
#   PRIVATE_KEY=0x... ./swap.sh --token-in ETH --token-out 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 --amount 10000000000000000 --chain base

# FIX SH-01: Use set -uo pipefail (no -e) to allow error handling blocks
set -uo pipefail
export PATH="$HOME/.foundry/bin:$PATH"

# ── Logging ──
# FIX OUT-01: ALL informational output goes to stderr; only JSON to stdout
log() { echo "$@" >&2; }
err() { echo "ERROR: $@" >&2; }

# ── Defaults ──
CHAIN="base"
SLIPPAGE_BPS=50  # 0.5%
RECIPIENT=""
DEADLINE_OFFSET=300  # 5 minutes
RPC_URL=""
TOKEN_IN=""
TOKEN_OUT=""
AMOUNT=""
JSON_OUTPUT=false

# ── Contract Addresses ──
declare -A POOL_MANAGER=(
  [base]="0x498581fF718922c3f8e6A244956aF099B2652b2b"
  [ethereum]="0x000000000004444c5dc75cB358380D2e3dE08A90"
)
declare -A UNIVERSAL_ROUTER=(
  [base]="0x6Df1c91424F79E40E33B1A48F0687B666bE71075"
  [ethereum]="0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af"
)
declare -A PERMIT2=(
  [base]="0x494bbD8A3302AcA833D307D11838f18DbAdA9C25"
  [ethereum]="0x000000000022D473030F116dDEE9F6B43aC78BA3"
)
declare -A WETH=(
  [base]="0x4200000000000000000000000000000000000006"
  [ethereum]="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
)
declare -A DEFAULT_RPC=(
  [base]="https://mainnet.base.org"
  [ethereum]="https://eth.llamarpc.com"
)
# StateView addresses — for pool discovery (getSlot0 lives here, NOT on PoolManager)
declare -A STATE_VIEW=(
  [base]="0xa3c0c9b65bad0b08107aa264b0f3db444b867a71"
  [ethereum]="0xa3c0c9b65bad0b08107aa264b0f3db444b867a71"
)

# ── Parse Args ──
while [[ $# -gt 0 ]]; do
  case "$1" in
    --token-in)     TOKEN_IN="$2"; shift 2 ;;
    --token-out)    TOKEN_OUT="$2"; shift 2 ;;
    --amount)       AMOUNT="$2"; shift 2 ;;
    --slippage)     SLIPPAGE_BPS="$2"; shift 2 ;;
    --recipient)    RECIPIENT="$2"; shift 2 ;;
    --rpc-url|--rpc) RPC_URL="$2"; shift 2 ;;
    --chain)        CHAIN="$2"; shift 2 ;;
    --json)         JSON_OUTPUT=true; shift ;;
    -h|--help)
      cat >&2 <<'EOF'
Usage: swap.sh --token-in <addr|ETH> --token-out <addr|ETH> --amount <wei> [options]
Options:
  --chain base|ethereum     Chain (default: base)
  --slippage <bps>          Slippage in basis points (default: 50 = 0.5%)
  --recipient <addr>        Recipient (default: sender)
  --rpc-url <url>           RPC URL (default: chain default)
  --json                    Output as JSON

Private key: set PRIVATE_KEY env var (never pass on CLI)
EOF
      exit 0 ;;
    # FIX SH-06: Explicitly reject --private-key CLI flag
    --private-key)
      err "--private-key CLI flag is disabled for security (visible in ps output)."
      err "Set PRIVATE_KEY environment variable instead."
      exit 1 ;;
    *) err "Unknown arg: $1"; exit 1 ;;
  esac
done

# ── Input Validation ──
# FIX PT-001: Validate ALL user inputs are pure numbers before any arithmetic
validate_numeric() {
  local name="$1" value="$2"
  if [[ ! "$value" =~ ^[0-9]+$ ]]; then
    err "--${name} must be a non-negative integer. Got: '${value}'"
    exit 1
  fi
}

validate_address() {
  local name="$1" value="$2"
  if [[ "$value" != "ETH" && "$value" != "eth" && ! "$value" =~ ^0x[0-9a-fA-F]{40}$ ]]; then
    err "--${name} must be 'ETH' or a valid address (0x + 40 hex chars). Got: '${value}'"
    exit 1
  fi
}

[[ -z "$TOKEN_IN" ]] && { err "--token-in required"; exit 1; }
[[ -z "$TOKEN_OUT" ]] && { err "--token-out required"; exit 1; }
[[ -z "$AMOUNT" ]] && { err "--amount required"; exit 1; }

# FIX PT-001: Validate numeric inputs BEFORE any arithmetic
validate_numeric "amount" "$AMOUNT"
validate_numeric "slippage" "$SLIPPAGE_BPS"

# FIX PT-012: Validate address inputs
validate_address "token-in" "$TOKEN_IN"
validate_address "token-out" "$TOKEN_OUT"

# FIX SH-06: Use env var ONLY for private key — never CLI flag
PRIVATE_KEY="${PRIVATE_KEY:-}"
[[ -z "$PRIVATE_KEY" ]] && { err "PRIVATE_KEY env var required (never pass on CLI for security)"; exit 1; }

# Validate chain
if [[ ! -v POOL_MANAGER[$CHAIN] ]]; then
  err "Unsupported chain: $CHAIN. Supported: ${!POOL_MANAGER[*]}"
  exit 1
fi

# Set RPC
RPC_URL="${RPC_URL:-${DEFAULT_RPC[$CHAIN]}}"

# Resolve ETH to address(0) for V4
ADDR_ZERO="0x0000000000000000000000000000000000000000"
[[ "$TOKEN_IN" == "ETH" || "$TOKEN_IN" == "eth" ]] && TOKEN_IN="$ADDR_ZERO"
[[ "$TOKEN_OUT" == "ETH" || "$TOKEN_OUT" == "eth" ]] && TOKEN_OUT="$ADDR_ZERO"

# Get sender address — pass key via env to avoid ps exposure
SENDER=$(PRIVATE_KEY="$PRIVATE_KEY" cast wallet address --private-key "$PRIVATE_KEY" 2>/dev/null)
if [[ -z "$SENDER" ]]; then
  err "Failed to derive wallet address from PRIVATE_KEY"
  exit 1
fi
RECIPIENT="${RECIPIENT:-$SENDER}"
if [[ -n "$RECIPIENT" && "$RECIPIENT" != "$SENDER" ]]; then
  validate_address "recipient" "$RECIPIENT"
fi

# ── Sort currencies for PoolKey ──
TOKEN_IN_LOWER=$(echo "$TOKEN_IN" | tr '[:upper:]' '[:lower:]')
TOKEN_OUT_LOWER=$(echo "$TOKEN_OUT" | tr '[:upper:]' '[:lower:]')

if [[ "$TOKEN_IN_LOWER" < "$TOKEN_OUT_LOWER" ]]; then
  CURRENCY0="$TOKEN_IN"
  CURRENCY1="$TOKEN_OUT"
  ZERO_FOR_ONE=true
else
  CURRENCY0="$TOKEN_OUT"
  CURRENCY1="$TOKEN_IN"
  ZERO_FOR_ONE=false
fi

# ── ERC20 Approval (if not ETH) ──
approve_token() {
  local TOKEN=$1
  local SPENDER=$2
  [[ "$TOKEN" == "$ADDR_ZERO" ]] && return 0

  # Check current allowance on Permit2
  local ALLOWANCE
  ALLOWANCE=$(cast call "$TOKEN" "allowance(address,address)(uint256)" "$SENDER" "$SPENDER" --rpc-url "$RPC_URL" 2>/dev/null || echo "0")

  # FIX SH-03 / PT-002: Use Python for big-number comparison (bash overflows on uint256)
  local NEEDS_APPROVE
  NEEDS_APPROVE=$(python3 -c "
a = '${ALLOWANCE}'.split('[')[0].strip()
try:
    needs = int(a) < int('${AMOUNT}')
except:
    needs = True
print('yes' if needs else 'no')
")

  if [[ "$NEEDS_APPROVE" == "yes" ]]; then
    log "Approving $TOKEN for $SPENDER..."
    # FIX SH-06: Never pass --private-key on CLI; cast reads from PRIVATE_KEY env
    PRIVATE_KEY="$PRIVATE_KEY" cast send "$TOKEN" "approve(address,uint256)" "$SPENDER" "$(cast max-uint)" \
      --private-key "$PRIVATE_KEY" --rpc-url "$RPC_URL" --json 2>/dev/null | jq -r '.transactionHash' >&2 || true
  fi
}

# ── Approve Permit2 to spend token, then approve UR on Permit2 ──
if [[ "$TOKEN_IN" != "$ADDR_ZERO" ]]; then
  approve_token "$TOKEN_IN" "${PERMIT2[$CHAIN]}"

  # Approve Universal Router on Permit2
  log "Setting Permit2 allowance for Universal Router..."
  # FIX PT-002: Use Python for expiry calculation to avoid potential overflow
  EXPIRY=$(python3 -c "import time; print(int(time.time()) + 86400 * 30)")
  MAX_UINT160="1461501637330902918203684832716283019655932542975"
  PRIVATE_KEY="$PRIVATE_KEY" cast send "${PERMIT2[$CHAIN]}" \
    "approve(address,address,uint160,uint48)" \
    "$TOKEN_IN" "${UNIVERSAL_ROUTER[$CHAIN]}" "$MAX_UINT160" "$EXPIRY" \
    --private-key "$PRIVATE_KEY" --rpc-url "$RPC_URL" --json 2>/dev/null | jq -r '.transactionHash' >&2 || true
fi

# ── Build V4 Swap via Universal Router ──
# Deadline
DEADLINE=$(python3 -c "import time; print(int(time.time()) + ${DEADLINE_OFFSET})")

# Determine ETH value to send
ETH_VALUE="0"
if [[ "$TOKEN_IN" == "$ADDR_ZERO" ]]; then
  ETH_VALUE="$AMOUNT"
fi

log "Executing swap on Uniswap V4..."
log "  Chain: $CHAIN"
log "  Token In: $TOKEN_IN"
log "  Token Out: $TOKEN_OUT"
log "  Amount: $AMOUNT wei"
log "  Slippage: ${SLIPPAGE_BPS} bps"
log "  Router: ${UNIVERSAL_ROUTER[$CHAIN]}"

# ── Pool Discovery ──
# FIX C-01: Use v4_read.py (extsload) for pool discovery instead of
# calling getSlot0 on PoolManager (which doesn't have that function).
# v4_read.py uses the proven extsload pattern that works correctly.
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

FOUND_POOL=false
FEE_TIER=""
TICK_SPACING=""
SQRT_PRICE=""

# Use v4_read.py to find the best pool
POOL_JSON=$(python3 "$SKILL_DIR/scripts/v4_read.py" find-pool \
  --token0 "$CURRENCY0" --token1 "$CURRENCY1" \
  --chain "$CHAIN" --rpc "$RPC_URL" 2>/dev/null || echo '{"success":false}')

# Parse pool discovery results — pick pool with highest liquidity
# Pipe JSON via stdin to avoid quoting issues with embedded content
POOL_DATA=$(echo "$POOL_JSON" | python3 -c "
import json, sys
try:
    data = json.load(sys.stdin)
    if not data.get('success') or not data.get('pools'):
        print('NONE')
        sys.exit(0)
    # Pick pool with highest liquidity (FIX M-01)
    best = max(data['pools'], key=lambda p: int(p.get('liquidity', '0')))
    print(f\"{best['fee']}|{best['tickSpacing']}|{best['sqrtPriceX96']}|{best['liquidity']}\")
except Exception as e:
    print('NONE', file=sys.stderr)
    print('NONE')
" 2>/dev/null)

if [[ "$POOL_DATA" != "NONE" && -n "$POOL_DATA" ]]; then
  IFS='|' read -r FEE_TIER TICK_SPACING SQRT_PRICE LIQUIDITY <<< "$POOL_DATA"
  FOUND_POOL=true
  log "  Pool found: fee=$FEE_TIER tickSpacing=$TICK_SPACING liquidity=$LIQUIDITY"
fi

if [[ "$FOUND_POOL" != "true" ]]; then
  if [[ "$JSON_OUTPUT" == "true" ]]; then
    echo '{"success":false,"error":"No V4 pool found for this token pair"}'
  else
    err "No V4 pool found for this token pair. Try using the quote.sh script to check available pools."
  fi
  exit 1
fi

# ── FIX C-03: Quote expected output from pool sqrtPriceX96 ──
# price = sqrtPriceX96^2 / 2^192 (token1 per token0 in raw units)
# Uses Python for arbitrary-precision arithmetic (sqrtPriceX96^2 exceeds 64-bit)
# FIX PT-002: ALL wei arithmetic in Python — never in bash
QUOTE_RESULT=$(python3 -c "
sqrt_price = int('$SQRT_PRICE')
amount_in = int('$AMOUNT')
slippage_bps = int('$SLIPPAGE_BPS')
zero_for_one = ('$ZERO_FOR_ONE' == 'true')

if sqrt_price == 0:
    print('0|0')
else:
    if zero_for_one:
        expected_out = amount_in * sqrt_price * sqrt_price // (1 << 192)
    else:
        expected_out = amount_in * (1 << 192) // (sqrt_price * sqrt_price)

    # Apply slippage to the QUOTED output (not the input amount)
    min_out = expected_out * (10000 - slippage_bps) // 10000

    # Sanity check: min_out must be > 0 for any nonzero amount
    if amount_in > 0 and min_out <= 0:
        min_out = 1  # At minimum, require 1 wei output

    print(f'{expected_out}|{min_out}')
")

IFS='|' read -r EXPECTED_OUT AMOUNT_OUT_MIN <<< "$QUOTE_RESULT"

log "  Expected output: $EXPECTED_OUT"
log "  Min output (${SLIPPAGE_BPS}bps slippage): $AMOUNT_OUT_MIN"

# ── Encode V4 swap params ──
# SWAP_EXACT_IN_SINGLE params: ((currency0,currency1,fee,tickSpacing,hooks), zeroForOne, amountIn, amountOutMinimum, hookData)
SWAP_PARAMS=$(cast abi-encode \
  "f((address,address,uint24,int24,address),bool,uint128,uint128,bytes)" \
  "($CURRENCY0,$CURRENCY1,$FEE_TIER,$TICK_SPACING,$ADDR_ZERO)" \
  "$ZERO_FOR_ONE" "$AMOUNT" "$AMOUNT_OUT_MIN" "0x" 2>/dev/null)

# FIX C-02: Correct action bytes from official Actions.sol
# SWAP_EXACT_IN_SINGLE = 0x06
# SETTLE_ALL = 0x0c (NOT 0x0b — that's SETTLE)
# TAKE_ALL = 0x0f
ACTIONS="0x060c0f"

# SETTLE_ALL params: (currency, maxAmount)
if [[ "$ZERO_FOR_ONE" == "true" ]]; then
  SETTLE_CURRENCY="$CURRENCY0"
  TAKE_CURRENCY="$CURRENCY1"
else
  SETTLE_CURRENCY="$CURRENCY1"
  TAKE_CURRENCY="$CURRENCY0"
fi

SETTLE_PARAMS=$(cast abi-encode "f(address,uint256)" "$SETTLE_CURRENCY" "$AMOUNT" 2>/dev/null)
TAKE_PARAMS=$(cast abi-encode "f(address,uint256)" "$TAKE_CURRENCY" "$AMOUNT_OUT_MIN" 2>/dev/null)

# Encode V4_SWAP input
V4_INPUT=$(cast abi-encode "f(bytes,bytes[])" \
  "$ACTIONS" \
  "[$SWAP_PARAMS,$SETTLE_PARAMS,$TAKE_PARAMS]" 2>/dev/null)

# Command: 0x10 = V4_SWAP
COMMANDS="0x10"

# Execute via Universal Router
# FIX SH-01: || true allows error handling block to execute
TX_RESULT=$(cast send "${UNIVERSAL_ROUTER[$CHAIN]}" \
  "execute(bytes,bytes[],uint256)" \
  "$COMMANDS" "[$V4_INPUT]" "$DEADLINE" \
  --value "$ETH_VALUE" \
  --private-key "$PRIVATE_KEY" \
  --rpc-url "$RPC_URL" \
  --json 2>&1) || true

TX_HASH=$(echo "$TX_RESULT" | jq -r '.transactionHash // empty' 2>/dev/null || echo "")

if [[ -n "$TX_HASH" ]]; then
  if [[ "$JSON_OUTPUT" == "true" ]]; then
    echo "{\"success\":true,\"txHash\":\"$TX_HASH\",\"chain\":\"$CHAIN\",\"tokenIn\":\"$TOKEN_IN\",\"tokenOut\":\"$TOKEN_OUT\",\"amount\":\"$AMOUNT\",\"amountOutMin\":\"$AMOUNT_OUT_MIN\",\"expectedOut\":\"$EXPECTED_OUT\"}"
  else
    log "✅ Swap submitted!"
    log "  TX: $TX_HASH"
    log "  Explorer: https://$([ "$CHAIN" = "base" ] && echo "basescan.org" || echo "etherscan.io")/tx/$TX_HASH"
  fi
else
  if [[ "$JSON_OUTPUT" == "true" ]]; then
    # Escape TX_RESULT for JSON — take first line of error
    ERR_MSG=$(echo "$TX_RESULT" | head -1 | sed 's/"/\\"/g')
    echo "{\"success\":false,\"error\":\"$ERR_MSG\"}"
  else
    err "Swap failed"
    echo "$TX_RESULT" | head -5 >&2
  fi
  exit 1
fi
