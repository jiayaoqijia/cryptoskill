#!/usr/bin/env bash
# fast-limit-order.sh — End-to-end KyberSwap limit order: resolve tokens -> sign EIP-712 -> create order
#
# Usage: fast-limit-order.sh <amount> <makerAsset> <takerAsset> <targetPrice> <chain> <maker> [expiry_seconds] [wallet_method] [keystore_name]
# Output: JSON to stdout, progress to stderr
# Dependencies: curl, jq, cast (Foundry)
# Docs: https://docs.kyberswap.com/kyberswap-solutions/limit-order/developer-guides/create-limit-order

set -euo pipefail

# ── Configuration ───────────────────────────────────────────────────────────

LO_API="https://limit-order.kyberswap.com"
TOKEN_API="https://token-api.kyberswap.com/api/v1/public/tokens"
CLIENT_ID="ai-agent-skills"
NATIVE="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
DSLO_CONTRACT="0xcab2FA2eeab7065B45CBcF6E3936dDE2506b4f6C"
PASSWORD_FILE="${KEYSTORE_PASSWORD_FILE:-$HOME/.foundry/.password}"
# Fast-execution USD safety threshold (default $1,000). Override via env var.
# LIMITATION: price is fetched from the KyberSwap Token API on best-effort basis.
# If the token is exotic, newly-launched, or unlisted, the price may be unavailable
# and the check is SKIPPED with a warning — it is NOT a hard abort in that case.
# Always verify order value manually for exotic tokens.
# Set to 0 to disable entirely (use with care).
FAST_LIMIT_ORDER_MAX_USD="${FAST_LIMIT_ORDER_MAX_USD:-1000}"

# ── Helpers ─────────────────────────────────────────────────────────────────

log() { echo ":: $*" >&2; }

die() {
  local msg="$*"
  jq -nc --arg error "$msg" '{ok: false, error: $error}'
  exit 1
}

# URL-encode a string (requires jq)
urlencode() { printf '%s' "$1" | jq -sRr @uri; }

usage() {
  cat >&2 <<'EOF'
Usage: fast-limit-order.sh <amount> <makerAsset> <takerAsset> <targetPrice> <chain> <maker> [expiry_seconds] [wallet_method] [keystore_name]

  amount          Human-readable amount to sell (e.g. 1, 0.5, 100)
  makerAsset      Token to sell (e.g. ETH, USDC)
  takerAsset      Token to receive (e.g. USDC, ETH)
  targetPrice     Price per unit of makerAsset denominated in takerAsset
  chain           Chain slug (e.g. ethereum, arbitrum, polygon)
  maker           Maker wallet address (0x...)
  expiry_seconds  Order expiry in seconds (default: 604800 = 7 days)
  wallet_method   keystore | env | ledger | trezor (default: keystore)
  keystore_name   Keystore account name (default: mykey)
EOF
  exit 1
}

# Convert human-readable amount to wei (plain integer string, no decimals/sci notation)
to_wei() {
  local amount="$1" decimals="$2"
  local int_part dec_part dec_len pad_len result

  # Validate: must be a non-negative number (digits with optional single dot)
  if ! [[ "$amount" =~ ^[0-9]*\.?[0-9]+$ ]]; then
    die "Invalid amount for to_wei: '$amount'. Must be a non-negative number. No transaction was submitted."
  fi

  if [[ "$amount" == *.* ]]; then
    int_part="${amount%%.*}"
    dec_part="${amount#*.}"
  else
    int_part="$amount"
    dec_part=""
  fi

  [[ -z "$int_part" ]] && int_part="0"
  dec_len=${#dec_part}

  if (( dec_len >= decimals )); then
    # Truncate excess decimal places
    result="${int_part}${dec_part:0:$decimals}"
  else
    # Pad with trailing zeros
    pad_len=$((decimals - dec_len))
    result="${int_part}${dec_part}$(printf '%0*d' "$pad_len" 0)"
  fi

  # Strip leading zeros, keep at least "0"
  result="$(echo "$result" | sed 's/^0*//')"
  echo "${result:-0}"
}

# Convert wei to human-readable amount
from_wei() {
  local wei="$1" decimals="$2"
  local len int_part dec_part

  [[ -z "$wei" || "$wei" == "0" ]] && echo "0" && return

  # Strip leading zeros from input
  wei="$(echo "$wei" | sed 's/^0*//')"
  [[ -z "$wei" ]] && echo "0" && return

  len=${#wei}

  if (( decimals == 0 )); then
    echo "$wei"
  elif (( len <= decimals )); then
    local pad=$((decimals - len))
    if (( pad > 0 )); then
      dec_part="$(printf '%0*d' "$pad" 0)${wei}"
    else
      dec_part="$wei"
    fi
    dec_part="$(echo "$dec_part" | sed 's/0*$//')"
    [[ -z "$dec_part" ]] && echo "0" && return
    echo "0.${dec_part}"
  else
    int_part="${wei:0:$((len - decimals))}"
    dec_part="${wei:$((len - decimals))}"
    dec_part="$(echo "$dec_part" | sed 's/0*$//')"
    if [[ -z "$dec_part" ]]; then
      echo "$int_part"
    else
      echo "${int_part}.${dec_part}"
    fi
  fi
}

# Get chain ID from slug (17 chains — no megaeth for limit orders)
get_chain_id() {
  case "$1" in
    ethereum)   echo 1 ;;
    bsc)        echo 56 ;;
    arbitrum)   echo 42161 ;;
    polygon)    echo 137 ;;
    optimism)   echo 10 ;;
    base)       echo 8453 ;;
    avalanche)  echo 43114 ;;
    linea)      echo 59144 ;;
    mantle)     echo 5000 ;;
    sonic)      echo 146 ;;
    berachain)  echo 80094 ;;
    ronin)      echo 2020 ;;
    unichain)   echo 130 ;;
    hyperevm)   echo 999 ;;
    plasma)     echo 9745 ;;
    etherlink)  echo 42793 ;;
    monad)      echo 143 ;;
    *) return 1 ;;
  esac
}

# Get RPC URL for chain (needed for allowance check)
get_rpc_url() {
  local chain="$1"
  case "$chain" in
    ethereum)   echo "https://ethereum-rpc.publicnode.com" ;;
    arbitrum)   echo "https://arb1.arbitrum.io/rpc" ;;
    polygon)    echo "https://polygon-rpc.com" ;;
    optimism)   echo "https://mainnet.optimism.io" ;;
    base)       echo "https://mainnet.base.org" ;;
    bsc)        echo "https://bsc-dataseed.binance.org" ;;
    avalanche)  echo "https://api.avax.network/ext/bc/C/rpc" ;;
    linea)      echo "https://rpc.linea.build" ;;
    mantle)     echo "https://rpc.mantle.xyz" ;;
    sonic)      echo "https://rpc.soniclabs.com" ;;
    berachain)  echo "https://rpc.berachain.com" ;;
    ronin)      echo "https://api.roninchain.com/rpc" ;;
    unichain)   echo "https://rpc.unichain.org" ;;
    hyperevm)   echo "https://rpc.hyperliquid.xyz/evm" ;;
    plasma)     echo "https://plasma.drpc.org" ;;
    etherlink)  echo "https://node.mainnet.etherlink.com" ;;
    monad)      echo "https://rpc.monad.xyz" ;;
    *)          echo "" ;;
  esac
}

# Look up token in built-in registry. Outputs: "address decimals"
lookup_token() {
  local chain="$1" sym
  sym=$(echo "$2" | tr '[:lower:]' '[:upper:]')

  case "$chain:$sym" in
    # ── Native tokens ──
    ethereum:ETH|arbitrum:ETH|optimism:ETH|base:ETH|linea:ETH|unichain:ETH)
      echo "$NATIVE 18" ;;
    bsc:BNB)                    echo "$NATIVE 18" ;;
    polygon:POL|polygon:MATIC)  echo "$NATIVE 18" ;;
    avalanche:AVAX)             echo "$NATIVE 18" ;;
    mantle:MNT)                 echo "$NATIVE 18" ;;
    sonic:S)                    echo "$NATIVE 18" ;;
    berachain:BERA)             echo "$NATIVE 18" ;;
    ronin:RON)                  echo "$NATIVE 18" ;;
    etherlink:XTZ)              echo "$NATIVE 18" ;;
    monad:MON)                  echo "$NATIVE 18" ;;

    # ── Stablecoins: Ethereum ──
    ethereum:USDC) echo "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 6" ;;
    ethereum:USDT) echo "0xdAC17F958D2ee523a2206206994597C13D831ec7 6" ;;

    # ── Stablecoins: BSC ──
    bsc:USDC)      echo "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d 18" ;;
    bsc:USDT)      echo "0x55d398326f99059fF775485246999027B3197955 18" ;;

    # ── Stablecoins: Arbitrum ──
    arbitrum:USDC) echo "0xaf88d065e77c8cC2239327C5EDb3A432268e5831 6" ;;
    arbitrum:USDT) echo "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9 6" ;;

    # ── Stablecoins: Polygon ──
    polygon:USDC)  echo "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359 6" ;;
    polygon:USDT)  echo "0xc2132D05D31c914a87C6611C10748AEb04B58e8F 6" ;;

    # ── Stablecoins: Optimism ──
    optimism:USDC) echo "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85 6" ;;
    optimism:USDT) echo "0x94b008aA00579c1307B0EF2c499aD98a8ce58e58 6" ;;

    # ── Stablecoins: Base ──
    base:USDC)     echo "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 6" ;;

    # ── Stablecoins: Avalanche ──
    avalanche:USDC) echo "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E 6" ;;
    avalanche:USDT) echo "0x9702230A8Ea53601f5cD2dc00fDBc13d4dF4A8c7 6" ;;

    # ── Stablecoins: Linea ──
    linea:USDC)    echo "0x176211869cA2b568f2A7D4EE941E073a821EE1ff 6" ;;
    linea:USDT)    echo "0xA219439258ca9da29E9Cc4cE5596924745e12B93 6" ;;

    # ── Stablecoins: Sonic ──
    sonic:USDC.E|sonic:USDC) echo "0x29219dd400f2Bf60E5a23d13Be72B486D4038894 6" ;;

    # ── Stablecoins: Mantle ──
    mantle:USDC) echo "0x09Bc4E0D864854c6aFB6eB9A9cdF58aC190D0dF9 6" ;;

    *) return 1 ;;
  esac
}

# Resolve token via KyberSwap Token API (fallback). Outputs: "address decimals"
resolve_token_api() {
  local chain_id="$1" symbol="$2"
  local resp match

  log "Looking up $symbol via Token API (chain $chain_id)..."

  local encoded_symbol
  encoded_symbol=$(urlencode "$symbol")

  # Try symbol search first (exact match, most reliable)
  resp=$(curl -s --connect-timeout 10 --max-time 30 "${TOKEN_API}?chainIds=${chain_id}&symbol=${encoded_symbol}&isWhitelisted=true" \
    -H "X-Client-Id: ${CLIENT_ID}" 2>/dev/null) || true

  if [[ -n "$resp" ]]; then
    match=$(echo "$resp" | jq -r --arg s "$symbol" \
      '[.data.tokens[] | select(.symbol | ascii_downcase == ($s | ascii_downcase))] | sort_by(-(.marketCap // 0)) | first // empty | "\(.address) \(.decimals)"' 2>/dev/null) || true

    if [[ -n "$match" && "$match" != " " ]]; then
      echo "$match"
      return 0
    fi
  fi

  # Fall back to unfiltered symbol search (for non-whitelisted tokens)
  resp=$(curl -s --connect-timeout 10 --max-time 30 "${TOKEN_API}?chainIds=${chain_id}&symbol=${encoded_symbol}" \
    -H "X-Client-Id: ${CLIENT_ID}" 2>/dev/null) || true

  if [[ -n "$resp" ]]; then
    match=$(echo "$resp" | jq -r --arg s "$symbol" \
      '[.data.tokens[] | select(.symbol | ascii_downcase == ($s | ascii_downcase)) | select(.isVerified == true or (.marketCap // 0) > 0)] | sort_by(-(.marketCap // 0)) | first // empty | "\(.address) \(.decimals)"' 2>/dev/null) || true

    if [[ -n "$match" && "$match" != " " ]]; then
      echo "$match"
      return 0
    fi
  fi

  # Fall back to name search (substring match on token name)
  resp=$(curl -s --connect-timeout 10 --max-time 30 "${TOKEN_API}?chainIds=${chain_id}&name=${encoded_symbol}&isWhitelisted=true" \
    -H "X-Client-Id: ${CLIENT_ID}" 2>/dev/null) || true

  if [[ -n "$resp" ]]; then
    match=$(echo "$resp" | jq -r --arg s "$symbol" \
      '[.data.tokens[] | select(.symbol | ascii_downcase == ($s | ascii_downcase))] | sort_by(-(.marketCap // 0)) | first // empty | "\(.address) \(.decimals)"' 2>/dev/null) || true

    if [[ -n "$match" && "$match" != " " ]]; then
      echo "$match"
      return 0
    fi
  fi

  # Fall back to browsing by market cap
  local page
  for page in 1 2 3; do
    resp=$(curl -s --connect-timeout 10 --max-time 30 "${TOKEN_API}?chainIds=${chain_id}&page=${page}&pageSize=100" \
      -H "X-Client-Id: ${CLIENT_ID}" 2>/dev/null) || continue

    match=$(echo "$resp" | jq -r --arg s "$symbol" \
      '[.data.tokens[] | select(.symbol | ascii_downcase == ($s | ascii_downcase)) | select(.isVerified == true or (.marketCap // 0) > 0)] | sort_by(-(.marketCap // 0)) | first // empty | "\(.address) \(.decimals)"' 2>/dev/null) || continue

    if [[ -n "$match" && "$match" != " " ]]; then
      echo "$match"
      return 0
    fi
  done

  return 1
}

# Resolve token: built-in registry first, then Token API fallback
resolve_token() {
  local chain="$1" symbol="$2" chain_id="$3"
  local result

  if result=$(lookup_token "$chain" "$symbol"); then
    echo "$result"
    return 0
  fi

  if result=$(resolve_token_api "$chain_id" "$symbol"); then
    echo "$result"
    return 0
  fi

  return 1
}

# Convert native token sentinel to wrapped ERC-20 equivalent for limit orders.
# The Limit Order API requires ERC-20 tokens; native token addresses are rejected.
# Outputs: "address decimals" or returns 1 if no mapping exists.
native_to_wrapped() {
  local chain="$1" chain_id="$2"
  case "$chain" in
    ethereum)   echo "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 18" ;;
    arbitrum)   echo "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1 18" ;;
    optimism)   echo "0x4200000000000000000000000000000000000006 18" ;;
    base)       echo "0x4200000000000000000000000000000000000006 18" ;;
    linea)      echo "0xe5D7C2a44FfDDf6b295A15c148167daaAf5Cf34f 18" ;;
    polygon)    echo "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270 18" ;;
    bsc)        echo "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c 18" ;;
    avalanche)  echo "0xB31f66AA3C1e785363F0875A1B74E27b85FD66c7 18" ;;
    # Chains where the wrapped address must be looked up via Token API
    unichain|mantle|sonic|berachain|ronin|etherlink|monad)
      local wrapped_sym
      case "$chain" in
        unichain)   wrapped_sym="WETH" ;;
        mantle)     wrapped_sym="WMNT" ;;
        sonic)      wrapped_sym="WS" ;;
        berachain)  wrapped_sym="WBERA" ;;
        ronin)      wrapped_sym="WRON" ;;
        etherlink)  wrapped_sym="WXTZ" ;;
        monad)      wrapped_sym="WMON" ;;
      esac
      local result
      if result=$(resolve_token_api "$chain_id" "$wrapped_sym"); then
        echo "$result"
        return 0
      fi
      return 1
      ;;
    *) return 1 ;;
  esac
}

# ── Main ────────────────────────────────────────────────────────────────────

main() {
  # Check dependencies
  for cmd in curl jq cast; do
    command -v "$cmd" &>/dev/null || die "Required command not found: ${cmd}. Install it and try again. No transaction was submitted."
  done

  # Parse arguments
  case "${1:-}" in -h|--help) usage ;; esac
  [[ $# -lt 6 ]] && usage

  local amount="$1"
  local maker_asset_sym="$2"
  local taker_asset_sym="$3"
  local target_price="$4"
  local chain="$5"
  local maker="$6"
  local expiry_seconds="${7:-604800}"
  local wallet_method="${8:-keystore}"
  local keystore_name="${9:-mykey}"

  # ── Input validation ────────────────────────────────────────────────────

  # Validate amount
  if ! [[ "$amount" =~ ^[0-9]*\.?[0-9]+$ ]]; then
    die "Invalid amount: '$amount'. Must be a non-negative number (e.g. 1, 0.5, 100). No transaction was submitted."
  fi
  # Reject zero amount
  if [[ "$(echo "$amount" | sed 's/[0.]//g')" == "" ]]; then
    die "Amount must be greater than zero. No transaction was submitted."
  fi

  # Validate target price
  if ! [[ "$target_price" =~ ^[0-9]*\.?[0-9]+$ ]]; then
    die "Invalid target price: '$target_price'. Must be a non-negative number. No transaction was submitted."
  fi
  # Reject zero target price
  if [[ "$(echo "$target_price" | sed 's/[0.]//g')" == "" ]]; then
    die "Target price must be greater than zero. No transaction was submitted."
  fi

  # Validate token inputs: either a symbol or pre-resolved address:decimals
  if [[ "$maker_asset_sym" =~ ^0x[a-fA-F0-9]{40}:[0-9]+$ ]]; then
    :  # Pre-resolved address:decimals
  elif [[ "$maker_asset_sym" =~ ^[a-zA-Z0-9.]+$ ]]; then
    :  # Symbol
  else
    die "Invalid makerAsset: $maker_asset_sym. Must be a symbol (e.g. ETH) or address:decimals (e.g. 0xA0b8...:6). No transaction was submitted."
  fi
  if [[ "$taker_asset_sym" =~ ^0x[a-fA-F0-9]{40}:[0-9]+$ ]]; then
    :  # Pre-resolved address:decimals
  elif [[ "$taker_asset_sym" =~ ^[a-zA-Z0-9.]+$ ]]; then
    :  # Symbol
  else
    die "Invalid takerAsset: $taker_asset_sym. Must be a symbol (e.g. USDC) or address:decimals (e.g. 0xA0b8...:6). No transaction was submitted."
  fi

  # Validate maker address
  [[ "$maker" =~ ^0x[a-fA-F0-9]{40}$ ]] || die "Invalid maker address: $maker. No transaction was submitted."
  local maker_lower
  maker_lower=$(echo "$maker" | tr '[:upper:]' '[:lower:]')
  if [[ "$maker_lower" == "0x0000000000000000000000000000000000000000" ]]; then
    die "Cannot use zero address as maker. Please provide your actual wallet address. No transaction was submitted."
  fi
  if [[ "$maker_lower" == "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee" ]]; then
    die "Cannot use the native token sentinel address as maker. Please provide your actual wallet address. No transaction was submitted."
  fi

  # Validate expiry_seconds
  if ! [[ "$expiry_seconds" =~ ^[0-9]+$ ]]; then
    die "Invalid expiry_seconds: '$expiry_seconds'. Must be a positive integer (seconds). No transaction was submitted."
  fi
  if (( expiry_seconds < 60 )); then
    die "Expiry too short: ${expiry_seconds}s. Minimum is 60 seconds. No transaction was submitted."
  fi
  if (( expiry_seconds > 31536000 )); then
    die "Expiry too long: ${expiry_seconds}s. Maximum is 31536000 seconds (365 days). No transaction was submitted."
  fi

  # Validate wallet_method
  case "$wallet_method" in
    keystore|env|ledger|trezor) ;;
    *) die "Unknown wallet method '$wallet_method'. Use: keystore, env, ledger, trezor. No transaction was submitted." ;;
  esac

  # Validate keystore_name
  if [[ -n "$keystore_name" ]] && ! [[ "$keystore_name" =~ ^[a-zA-Z0-9_.-]+$ ]]; then
    die "Invalid keystore name '$keystore_name'. Must contain only letters, digits, underscores, dots, and hyphens. No transaction was submitted."
  fi

  # Validate chain
  local chain_id
  chain_id=$(get_chain_id "$chain") || \
    die "Unsupported chain for limit orders: ${chain}. Supported: ethereum, bsc, arbitrum, polygon, optimism, avalanche, base, linea, mantle, sonic, berachain, ronin, unichain, hyperevm, plasma, etherlink, monad. No transaction was submitted."

  log "Creating limit order: sell ${amount} ${maker_asset_sym} for ${taker_asset_sym} at ${target_price} on ${chain}"
  log "Maker: $maker"
  log "Expiry: ${expiry_seconds}s"

  # ── Step 1: Resolve tokens ──────────────────────────────────────────────

  local maker_addr maker_dec taker_addr taker_dec

  # Resolve makerAsset
  if [[ "$maker_asset_sym" =~ ^0x[a-fA-F0-9]{40}:[0-9]+$ ]]; then
    maker_addr="${maker_asset_sym%%:*}"
    maker_dec="${maker_asset_sym##*:}"
    log "Using pre-resolved makerAsset: ${maker_addr} (${maker_dec} decimals)"
  else
    log "Resolving ${maker_asset_sym} on ${chain}..."
    local maker_info
    maker_info=$(resolve_token "$chain" "$maker_asset_sym" "$chain_id") || \
      die "Token '${maker_asset_sym}' not found on ${chain}. Verify the symbol or provide a contract address. No transaction was submitted."
    maker_addr=$(echo "$maker_info" | awk '{print $1}')
    maker_dec=$(echo "$maker_info" | awk '{print $2}')
    [[ "$maker_addr" =~ ^0x[a-fA-F0-9]{40}$ ]] || die "Invalid token address for $maker_asset_sym: $maker_addr. No transaction was submitted."
    log "  ${maker_asset_sym} = ${maker_addr} (${maker_dec} decimals)"
  fi

  # Resolve takerAsset
  if [[ "$taker_asset_sym" =~ ^0x[a-fA-F0-9]{40}:[0-9]+$ ]]; then
    taker_addr="${taker_asset_sym%%:*}"
    taker_dec="${taker_asset_sym##*:}"
    log "Using pre-resolved takerAsset: ${taker_addr} (${taker_dec} decimals)"
  else
    log "Resolving ${taker_asset_sym} on ${chain}..."
    local taker_info
    taker_info=$(resolve_token "$chain" "$taker_asset_sym" "$chain_id") || \
      die "Token '${taker_asset_sym}' not found on ${chain}. Verify the symbol or provide a contract address. No transaction was submitted."
    taker_addr=$(echo "$taker_info" | awk '{print $1}')
    taker_dec=$(echo "$taker_info" | awk '{print $2}')
    [[ "$taker_addr" =~ ^0x[a-fA-F0-9]{40}$ ]] || die "Invalid token address for $taker_asset_sym: $taker_addr. No transaction was submitted."
    log "  ${taker_asset_sym} = ${taker_addr} (${taker_dec} decimals)"
  fi

  # ── Auto-wrap native tokens for limit orders ──────────────────────────
  # The Limit Order API requires ERC-20 tokens only. If either asset resolved
  # to the native sentinel address, convert it to the wrapped ERC-20 equivalent.

  if [[ "$maker_addr" == "$NATIVE" ]]; then
    local wrapped_maker
    wrapped_maker=$(native_to_wrapped "$chain" "$chain_id") || \
      die "Cannot auto-wrap native token on ${chain}: no wrapped token mapping found. No transaction was submitted."
    maker_addr=$(echo "$wrapped_maker" | awk '{print $1}')
    maker_dec=$(echo "$wrapped_maker" | awk '{print $2}')
    local maker_sym_upper
    maker_sym_upper=$(echo "$maker_asset_sym" | tr '[:lower:]' '[:upper:]')
    log "Native ${maker_sym_upper} converted to W${maker_sym_upper} for limit orders"
    log "  W${maker_sym_upper} = ${maker_addr} (${maker_dec} decimals)"
  fi

  if [[ "$taker_addr" == "$NATIVE" ]]; then
    local wrapped_taker
    wrapped_taker=$(native_to_wrapped "$chain" "$chain_id") || \
      die "Cannot auto-wrap native token on ${chain}: no wrapped token mapping found. No transaction was submitted."
    taker_addr=$(echo "$wrapped_taker" | awk '{print $1}')
    taker_dec=$(echo "$wrapped_taker" | awk '{print $2}')
    local taker_sym_upper
    taker_sym_upper=$(echo "$taker_asset_sym" | tr '[:lower:]' '[:upper:]')
    log "Native ${taker_sym_upper} converted to W${taker_sym_upper} for limit orders"
    log "  W${taker_sym_upper} = ${taker_addr} (${taker_dec} decimals)"
  fi

  local maker_is_native="false" taker_is_native="false"
  [[ "$maker_addr" == "$NATIVE" ]] && maker_is_native="true"
  [[ "$taker_addr" == "$NATIVE" ]] && taker_is_native="true"

  # ── Step 1b: Honeypot / FOT check ────────────────────────────────────

  check_honeypot() {
    local addr="$1" symbol="$2" is_native="$3"
    [[ "$is_native" == "true" ]] && return 0

    # Validate address format before using in API URL
    [[ "$addr" =~ ^0x[a-fA-F0-9]{40}$ ]] || return 1

    local resp hp fot tax
    resp=$(curl -s --connect-timeout 10 --max-time 30 "${TOKEN_API}/honeypot-fot-info?chainId=${chain_id}&address=${addr}" \
      -H "X-Client-Id: ${CLIENT_ID}" 2>/dev/null) || { log "WARNING: Token safety API unreachable for ${symbol}. Proceeding without honeypot/FOT check."; return 0; }

    hp=$(echo "$resp" | jq -r '.data.isHoneypot // false' 2>/dev/null) || { log "WARNING: Could not parse safety data for ${symbol}."; return 0; }
    fot=$(echo "$resp" | jq -r '.data.isFOT // false' 2>/dev/null) || { log "WARNING: Could not parse FOT data for ${symbol}."; return 0; }
    tax=$(echo "$resp" | jq -r '.data.tax // 0' 2>/dev/null) || return 0

    if [[ "$hp" == "true" ]]; then
      die "HONEYPOT DETECTED: ${symbol} (${addr}) is flagged as a honeypot. You will not be able to sell this token. Order creation aborted. No transaction was submitted."
    fi

    if [[ "$fot" == "true" ]]; then
      log "WARNING: ${symbol} has a fee-on-transfer (tax: ${tax}%). The actual received amount when the order is filled will be less than expected."
    fi
  }

  log "Checking token safety..."
  check_honeypot "$maker_addr" "$maker_asset_sym" "$maker_is_native"
  check_honeypot "$taker_addr" "$taker_asset_sym" "$taker_is_native"

  # ── Step 2: Convert amounts to wei ──────────────────────────────────────

  local making_amount_wei
  making_amount_wei=$(to_wei "$amount" "$maker_dec")
  if [[ "$making_amount_wei" == "0" ]]; then
    die "Making amount converts to 0 wei (amount too small for token decimals). No transaction was submitted."
  fi
  log "Making amount: ${amount} ${maker_asset_sym} = ${making_amount_wei} wei"

  # Calculate takingAmount = makingAmount * targetPrice
  # Use bc for precision with arbitrary-precision decimals
  command -v bc &>/dev/null || die "bc is required for price calculation. Install it and try again. No transaction was submitted."

  # Validate target_price is numeric before bc call (injection guard)
  if ! [[ "$target_price" =~ ^[0-9]*\.?[0-9]+$ ]]; then
    die "Invalid target price for calculation: '$target_price'. No transaction was submitted."
  fi
  if ! [[ "$amount" =~ ^[0-9]*\.?[0-9]+$ ]]; then
    die "Invalid amount for calculation: '$amount'. No transaction was submitted."
  fi

  local taking_amount
  taking_amount=$(echo "scale=18; $amount * $target_price" | bc -l 2>/dev/null) || \
    die "Failed to calculate taking amount. Verify amount and target price are valid numbers. No transaction was submitted."

  # Strip trailing zeros and possible leading dot
  taking_amount=$(echo "$taking_amount" | sed 's/0*$//; s/\.$//')
  # Handle bc output that starts with "." (e.g. ".5")
  [[ "$taking_amount" == .* ]] && taking_amount="0${taking_amount}"
  [[ -z "$taking_amount" || "$taking_amount" == "0" ]] && die "Calculated taking amount is zero. Verify target price is positive. No transaction was submitted."

  local taking_amount_wei
  taking_amount_wei=$(to_wei "$taking_amount" "$taker_dec")
  log "Taking amount: ${taking_amount} ${taker_asset_sym} = ${taking_amount_wei} wei"
  log "Target price: 1 ${maker_asset_sym} = ${target_price} ${taker_asset_sym}"

  # ── Step 2b: USD value threshold check ──────────────────────────────────
  # Abort if order value exceeds FAST_LIMIT_ORDER_MAX_USD (default $1,000).
  # Override: FAST_LIMIT_ORDER_MAX_USD=<n>  |  set to 0 to disable.
  # LIMITATION: price is sourced from the KyberSwap Token API on best-effort
  # basis. If the token is exotic, newly-launched, or the API is unreachable,
  # the check is SKIPPED with a warning (not aborted). Always verify order
  # value manually for exotic tokens before using this fast-execution path.
  local max_usd="$FAST_LIMIT_ORDER_MAX_USD"
  if ! [[ "$max_usd" =~ ^[0-9]+$ ]]; then max_usd=1000; fi
  if [[ "$max_usd" -eq 0 ]]; then
    log "USD threshold check DISABLED (FAST_LIMIT_ORDER_MAX_USD=0)"
  else
    log "Checking order USD value against \$${max_usd} threshold..."
    local price_resp token_price="0"
    price_resp=$(curl -s --connect-timeout 10 --max-time 15 \
      "${TOKEN_API}?chainIds=${chain_id}&address=${maker_addr}" \
      -H "X-Client-Id: ${CLIENT_ID}" 2>/dev/null) || true
    token_price=$(echo "$price_resp" | jq -r \
      '[.data.tokens[]? | (.price // 0)] | first // 0' 2>/dev/null || echo "0")
    [[ "$token_price" =~ ^[0-9]*\.?[0-9]+$ ]] || token_price="0"

    if [[ "$token_price" == "0" ]]; then
      log "WARNING: USD price for '${maker_asset_sym}' unavailable (exotic/unlisted token or API unreachable)."
      log "         USD threshold check SKIPPED — verify order value manually."
      log "         To suppress this warning: FAST_LIMIT_ORDER_MAX_USD=0"
    elif command -v bc &>/dev/null; then
      local usd_value
      usd_value=$(echo "scale=2; $amount * $token_price" | bc -l 2>/dev/null || echo "0")
      usd_value=$(echo "$usd_value" | sed 's/0*$//; s/\.$//')
      [[ "$usd_value" == .* ]] && usd_value="0${usd_value}"
      [[ -z "$usd_value" ]] && usd_value="0"
      log "Estimated order value: \$${usd_value} USD (${amount} × \$${token_price})"
      if (( $(echo "$usd_value > $max_usd" | bc -l 2>/dev/null || echo 0) )); then
        die "Order value \$${usd_value} USD exceeds fast-execution safety limit of \$${max_usd} USD. Use /limit-order for large orders. To raise the limit: FAST_LIMIT_ORDER_MAX_USD=<new_limit>. No transaction was submitted."
      fi
    fi
  fi

  # ── Step 3: Get DSLOProtocol contract address ───────────────────────────

  log "Fetching DSLOProtocol contract address..."
  local contract_resp contract_addr
  contract_resp=$(curl -s --connect-timeout 10 --max-time 30 \
    "${LO_API}/read-ks/api/v1/configs/contract-address?chainId=${chain_id}" \
    -H "X-Client-Id: ${CLIENT_ID}" 2>/dev/null) || \
    die "Network error: failed to reach KyberSwap limit order config API. No transaction was submitted."

  contract_addr=$(echo "$contract_resp" | jq -r '.data.contractAddress // empty' 2>/dev/null)

  if [[ -z "$contract_addr" || "$contract_addr" == "null" ]]; then
    log "WARNING: Could not fetch contract address from API, using default: ${DSLO_CONTRACT}"
    contract_addr="$DSLO_CONTRACT"
  fi

  [[ "$contract_addr" =~ ^0x[a-fA-F0-9]{40}$ ]] || die "Invalid DSLOProtocol contract address: $contract_addr. No transaction was submitted."

  # Cross-check API-returned address against known-good (defense against compromised API)
  local expected_contract="${CONTRACT_ADDR_OVERRIDE:-$DSLO_CONTRACT}"
  local contract_lower expected_lower
  contract_lower=$(echo "$contract_addr" | tr '[:upper:]' '[:lower:]')
  expected_lower=$(echo "$expected_contract" | tr '[:upper:]' '[:lower:]')
  if [[ "$contract_lower" != "$expected_lower" ]]; then
    if [[ -n "${CONTRACT_ADDR_OVERRIDE:-}" ]]; then
      log "WARNING: Using CONTRACT_ADDR_OVERRIDE: $contract_addr"
    else
      die "Unexpected DSLOProtocol address: $contract_addr (expected: $DSLO_CONTRACT). This may indicate a new contract deployment or a compromised API response. Set CONTRACT_ADDR_OVERRIDE=<address> to proceed with the new address. No transaction was submitted."
    fi
  fi
  log "DSLOProtocol contract: ${contract_addr}"

  # ── Step 3b: Validate wallet and set up flags ──────────────────────────
  # Wallet setup is needed early for auto-approval before signing.

  # Register cleanup trap BEFORE any key export or temp file creation.
  local tmp_dir
  trap 'rm -rf "${tmp_dir:-}"; unset ETH_PRIVATE_KEY PRIVATE_KEY 2>/dev/null' EXIT INT TERM

  log "Validating wallet configuration..."
  local wallet_flags=()
  case "$wallet_method" in
    keystore)
      if [[ ! -f "$PASSWORD_FILE" ]]; then
        die "Password file not found: $PASSWORD_FILE. Create it or set KEYSTORE_PASSWORD_FILE. No transaction was submitted."
      fi
      local pw_perms
      if [[ "$(uname)" == "Darwin" ]]; then
        pw_perms=$(stat -f '%Lp' "$PASSWORD_FILE" 2>/dev/null || echo "unknown")
      else
        pw_perms=$(stat -c '%a' "$PASSWORD_FILE" 2>/dev/null || echo "unknown")
      fi
      if [[ "$pw_perms" != "600" && "$pw_perms" != "unknown" ]]; then
        die "Password file $PASSWORD_FILE has insecure permissions ($pw_perms). Required: 600. Fix with: chmod 600 $PASSWORD_FILE. No transaction was submitted."
      fi
      local keystore_dir="${HOME}/.foundry/keystores"
      if [[ ! -f "${keystore_dir}/${keystore_name}" ]]; then
        die "Keystore '${keystore_name}' not found in ${keystore_dir}. List keystores with: cast wallet list. No transaction was submitted."
      fi
      wallet_flags=(--account "$keystore_name" --password-file "$PASSWORD_FILE")
      log "Using keystore: $keystore_name"
      ;;
    env)
      if [[ -z "${PRIVATE_KEY:-}" ]]; then
        die "PRIVATE_KEY environment variable not set. No transaction was submitted."
      fi
      export ETH_PRIVATE_KEY="$PRIVATE_KEY"
      wallet_flags=()
      log "Using private key from env (via ETH_PRIVATE_KEY)"
      log "WARNING: env method is less secure than keystore. Private key is in process environment."
      ;;
    ledger)
      wallet_flags=(--ledger)
      log "Using Ledger (confirm on device)"
      ;;
    trezor)
      wallet_flags=(--trezor)
      log "Using Trezor (confirm on device)"
      ;;
  esac

  # ── Step 3c: Check balance, allowance, and auto-approve if needed ──────
  # The KyberSwap create order API requires sufficient balance AND allowance
  # before accepting an order. Check both and auto-approve if needed.

  local allowance_status="unknown" allowance_dec="0"
  local rpc_url="${RPC_URL_OVERRIDE:-$(get_rpc_url "$chain")}"

  if [[ "$maker_is_native" != "true" ]] && [[ -n "$rpc_url" ]]; then
    # Check maker's token balance first
    log "Checking ${maker_asset_sym} balance..."
    local balance_hex balance_dec="0"
    balance_hex=$(FOUNDRY_DISABLE_NIGHTLY_WARNING=1 cast call \
      --rpc-url "$rpc_url" \
      "$maker_addr" \
      "balanceOf(address)(uint256)" \
      "$maker" 2>/dev/null || echo "0")

    if [[ "$balance_hex" == 0x* ]]; then
      balance_dec=$(printf "%d" "$balance_hex" 2>/dev/null || echo "0")
    else
      balance_dec="${balance_hex%%[^0-9]*}"
      balance_dec="${balance_dec:-0}"
    fi

    if [[ "$balance_dec" =~ ^[0-9]+$ ]] && [[ "$making_amount_wei" =~ ^[0-9]+$ ]] && command -v bc &>/dev/null; then
      if (( $(echo "$balance_dec < $making_amount_wei" | bc -l 2>/dev/null || echo 0) )); then
        local balance_human
        balance_human=$(from_wei "$balance_dec" "$maker_dec")
        die "Insufficient ${maker_asset_sym} balance: ${balance_human} ${maker_asset_sym} available, but order requires ${amount} ${maker_asset_sym}. No transaction was submitted."
      fi
      log "Balance OK: $(from_wei "$balance_dec" "$maker_dec") ${maker_asset_sym}"
    fi

    log "Checking ERC-20 allowance for ${maker_asset_sym}..."

    local allowance_hex
    allowance_hex=$(FOUNDRY_DISABLE_NIGHTLY_WARNING=1 cast call \
      --rpc-url "$rpc_url" \
      "$maker_addr" \
      "allowance(address,address)(uint256)" \
      "$maker" \
      "$contract_addr" 2>/dev/null || echo "0")

    if [[ "$allowance_hex" == 0x* ]]; then
      allowance_dec=$(printf "%d" "$allowance_hex" 2>/dev/null || echo "0")
    else
      allowance_dec="${allowance_hex%%[^0-9]*}"
      allowance_dec="${allowance_dec:-0}"
    fi

    if [[ "$allowance_dec" =~ ^[0-9]+$ ]] && [[ "$making_amount_wei" =~ ^[0-9]+$ ]] && command -v bc &>/dev/null; then
      if (( $(echo "$allowance_dec >= $making_amount_wei" | bc -l 2>/dev/null || echo 0) )); then
        allowance_status="sufficient"
        log "Allowance OK: ${allowance_dec} >= ${making_amount_wei}"
      else
        log "Insufficient allowance: ${allowance_dec} < ${making_amount_wei}. Auto-approving..."

        local approve_output approve_exit_code=0
        approve_output=$(FOUNDRY_DISABLE_NIGHTLY_WARNING=1 cast send \
          --rpc-url "$rpc_url" \
          --timeout 120 \
          "${wallet_flags[@]}" \
          "$maker_addr" \
          "approve(address,uint256)" \
          "$contract_addr" \
          "$making_amount_wei" 2>&1) || approve_exit_code=$?

        if [[ $approve_exit_code -ne 0 ]]; then
          local safe_approve_output
          safe_approve_output=$(echo "$approve_output" | tail -3 | sed -E \
            -e 's/--private-key [^ ]*/--private-key [REDACTED]/g' \
            -e 's/"private[Kk]ey"[[:space:]]*:[[:space:]]*"[^"]*"/"privateKey": "[REDACTED]"/g' \
            -e 's/ETH_PRIVATE_KEY=[^ ]*/ETH_PRIVATE_KEY=[REDACTED]/g' \
            -e 's/PRIVATE_KEY=[^ ]*/PRIVATE_KEY=[REDACTED]/g' \
            -e 's/0x[a-fA-F0-9]{64}/[REDACTED_HEX]/g')
          die "Token approval transaction failed. Cannot create limit order without approval. Transaction was broadcast. Error: ${safe_approve_output}"
        fi

        local approve_status
        approve_status=$(echo "$approve_output" | grep -i '^status' | awk '{print $2}')
        if [[ "$approve_status" != "1" && "$approve_status" != "1 (success)" ]]; then
          die "Token approval transaction reverted (status: ${approve_status}). Check token contract or gas. Transaction was broadcast."
        fi

        local approve_hash
        approve_hash=$(echo "$approve_output" | grep -i '^transactionHash' | awk '{print $2}' | head -1)
        log "Approval tx confirmed: ${approve_hash:-unknown}"

        allowance_status="approved"
        allowance_dec="$making_amount_wei"
        log "Approved ${amount} ${maker_asset_sym} for DSLOProtocol contract"
      fi
    fi
  fi

  # ── Step 4: Compute expiry timestamp ────────────────────────────────────

  local expiry_ts
  expiry_ts=$(($(date +%s) + expiry_seconds))
  log "Order expires at: ${expiry_ts} ($(date -r "$expiry_ts" 2>/dev/null || date -d "@$expiry_ts" 2>/dev/null || echo "timestamp: $expiry_ts"))"

  # ── Step 5: Call sign-message API ───────────────────────────────────────

  log "Requesting EIP-712 sign message..."
  local sign_body sign_resp

  sign_body=$(jq -nc \
    --arg chainId "$chain_id" \
    --arg makerAsset "$maker_addr" \
    --arg takerAsset "$taker_addr" \
    --arg maker "$maker" \
    --argjson allowedSenders '["0x0000000000000000000000000000000000000000"]' \
    --arg makingAmount "$making_amount_wei" \
    --arg takingAmount "$taking_amount_wei" \
    --argjson expiredAt "$expiry_ts" \
    '{
      chainId: $chainId,
      makerAsset: $makerAsset,
      takerAsset: $takerAsset,
      maker: $maker,
      allowedSenders: $allowedSenders,
      makingAmount: $makingAmount,
      takingAmount: $takingAmount,
      expiredAt: $expiredAt
    }')

  sign_resp=$(curl -s --connect-timeout 10 --max-time 30 \
    -X POST "${LO_API}/write/api/v1/orders/sign-message" \
    -H "Content-Type: application/json" \
    -H "X-Client-Id: ${CLIENT_ID}" \
    -d "$sign_body" 2>/dev/null) || \
    die "Network error: failed to reach KyberSwap sign-message API."

  # Validate response
  local sign_data
  sign_data=$(echo "$sign_resp" | jq -c '.data // empty' 2>/dev/null)
  if [[ -z "$sign_data" || "$sign_data" == "null" || "$sign_data" == "" ]]; then
    local sign_error
    sign_error=$(echo "$sign_resp" | jq -r '.message // .error // "Unknown error"' 2>/dev/null || echo "Invalid response")
    die "Sign-message API error: ${sign_error}"
  fi

  # Extract EIP-712 typed data for signing
  local eip712_data salt interactions
  eip712_data=$(echo "$sign_resp" | jq -c '.data' 2>/dev/null) || \
    die "Failed to extract EIP-712 data from sign-message response."

  salt=$(echo "$sign_resp" | jq -r '.data.message.salt // .data.salt // empty' 2>/dev/null)
  interactions=$(echo "$sign_resp" | jq -r '.data.message.interaction // .data.message.interactions // .data.interactions // empty' 2>/dev/null)

  log "EIP-712 message received"

  # ── Step 6: Sign the EIP-712 message ────────────────────────────────────

  log "Signing EIP-712 message with cast wallet sign..."

  # Write typed data to temp file to avoid shell escaping issues
  local typed_data_file
  tmp_dir=$(mktemp -d)
  chmod 700 "$tmp_dir"
  typed_data_file=$(mktemp "${tmp_dir}/eip712-XXXXXX.json")
  chmod 600 "$typed_data_file"

  echo "$eip712_data" > "$typed_data_file"

  local signature sign_exit_code=0
  signature=$(FOUNDRY_DISABLE_NIGHTLY_WARNING=1 cast wallet sign \
    "${wallet_flags[@]}" \
    --data \
    "$(cat "$typed_data_file")" 2>&1) || sign_exit_code=$?

  rm -f "$typed_data_file"

  if [[ $sign_exit_code -ne 0 ]]; then
    # Sanitize output to prevent private key leakage
    local safe_output
    safe_output=$(echo "$signature" | sed -E \
      -e 's/--private-key [^ ]*/--private-key [REDACTED]/g' \
      -e 's/"private[Kk]ey"[[:space:]]*:[[:space:]]*"[^"]*"/"privateKey": "[REDACTED]"/g' \
      -e 's/ETH_PRIVATE_KEY=[^ ]*/ETH_PRIVATE_KEY=[REDACTED]/g' \
      -e 's/PRIVATE_KEY=[^ ]*/PRIVATE_KEY=[REDACTED]/g' \
      -e 's/0x[a-fA-F0-9]{64}/[REDACTED_HEX]/g')
    die "EIP-712 signing failed: ${safe_output}"
  fi

  # Validate signature format (0x-prefixed hex, 130 or 132 chars for 65 bytes)
  signature=$(echo "$signature" | tr -d '[:space:]')
  if ! [[ "$signature" =~ ^0x[a-fA-F0-9]{130}$ ]]; then
    die "Invalid signature format. Expected 0x-prefixed 65-byte hex string (132 chars total). Got: ${signature:0:20}..."
  fi

  log "EIP-712 message signed successfully"

  # ── Step 7: Create the order ────────────────────────────────────────────

  log "Submitting limit order..."
  local order_body order_resp

  order_body=$(jq -nc \
    --arg chainId "$chain_id" \
    --arg makerAsset "$maker_addr" \
    --arg takerAsset "$taker_addr" \
    --arg maker "$maker" \
    --argjson allowedSenders '["0x0000000000000000000000000000000000000000"]' \
    --arg makingAmount "$making_amount_wei" \
    --arg takingAmount "$taking_amount_wei" \
    --argjson expiredAt "$expiry_ts" \
    --arg signature "$signature" \
    --arg salt "$salt" \
    --arg interactions "$interactions" \
    '{
      chainId: $chainId,
      makerAsset: $makerAsset,
      takerAsset: $takerAsset,
      maker: $maker,
      allowedSenders: $allowedSenders,
      makingAmount: $makingAmount,
      takingAmount: $takingAmount,
      expiredAt: $expiredAt,
      signature: $signature,
      salt: $salt,
      interactions: $interactions
    }')


  order_resp=$(curl -s --connect-timeout 10 --max-time 30 \
    -X POST "${LO_API}/write/api/v1/orders" \
    -H "Content-Type: application/json" \
    -H "X-Client-Id: ${CLIENT_ID}" \
    -d "$order_body" 2>/dev/null) || \
    die "Network error: failed to reach KyberSwap create order API."


  # Check for API errors
  local order_id
  order_id=$(echo "$order_resp" | jq -r '.data.id // .data.orderId // empty' 2>/dev/null)

  if [[ -z "$order_id" || "$order_id" == "null" ]]; then
    local order_error order_code
    order_error=$(echo "$order_resp" | jq -r '.message // .error // "Unknown error"' 2>/dev/null || echo "Invalid response")
    order_code=$(echo "$order_resp" | jq -r '.code // 0' 2>/dev/null || echo "0")

    # Provide actionable context for known error patterns
    if [[ "$order_error" == *"out of range: makingAmount"* ]]; then
      die "Create order API error: ${order_error}. This means the maker's token balance or allowance is insufficient for the requested makingAmount. Check balance and allowance on-chain."
    fi

    die "Create order API error: ${order_error}"
  fi

  log "Order created: ${order_id}"

  # Allowance was already checked and auto-approved in Step 3c.
  # allowance_status and allowance_dec are set from that step.

  # ── Step 9: Output JSON ─────────────────────────────────────────────────

  jq -n \
    --argjson ok true \
    --arg chain "$chain" \
    --arg chainId "$chain_id" \
    --arg orderId "$order_id" \
    --arg maker "$maker" \
    --arg makerAssetSymbol "$maker_asset_sym" \
    --arg makerAssetAddress "$maker_addr" \
    --argjson makerAssetDecimals "$maker_dec" \
    --argjson makerAssetIsNative "$maker_is_native" \
    --arg takerAssetSymbol "$taker_asset_sym" \
    --arg takerAssetAddress "$taker_addr" \
    --argjson takerAssetDecimals "$taker_dec" \
    --argjson takerAssetIsNative "$taker_is_native" \
    --arg makingAmount "$amount" \
    --arg makingAmountWei "$making_amount_wei" \
    --arg takingAmount "$taking_amount" \
    --arg takingAmountWei "$taking_amount_wei" \
    --arg targetPrice "$target_price" \
    --argjson expiredAt "$expiry_ts" \
    --arg contractAddress "$contract_addr" \
    --arg allowanceStatus "$allowance_status" \
    --arg allowance "$allowance_dec" \
    --arg walletMethod "$wallet_method" \
    '{
      ok: $ok,
      chain: $chain,
      chainId: $chainId,
      orderId: $orderId,
      maker: $maker,
      makerAsset: {
        symbol: $makerAssetSymbol,
        address: $makerAssetAddress,
        decimals: $makerAssetDecimals,
        isNative: $makerAssetIsNative
      },
      takerAsset: {
        symbol: $takerAssetSymbol,
        address: $takerAssetAddress,
        decimals: $takerAssetDecimals,
        isNative: $takerAssetIsNative
      },
      order: {
        makingAmount: $makingAmount,
        makingAmountWei: $makingAmountWei,
        takingAmount: $takingAmount,
        takingAmountWei: $takingAmountWei,
        targetPrice: $targetPrice,
        expiredAt: $expiredAt
      },
      contract: $contractAddress,
      allowanceStatus: $allowanceStatus,
      allowance: $allowance,
      walletMethod: $walletMethod
    }'
}

main "$@"
