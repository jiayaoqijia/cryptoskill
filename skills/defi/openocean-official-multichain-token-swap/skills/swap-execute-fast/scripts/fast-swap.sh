#!/bin/bash
# fast-swap.sh
# Builds swap transaction without confirmation
# Usage: ./fast-swap.sh <chain> <tokenIn> <tokenOut> <amount> <sender> [slippageBps] [--enabled-dex-ids <csv>] [--disabled-dex-ids <csv>]
# Slippage in basis points (100 = 1%). API expects percentage; script converts automatically.
# All progress output goes to stderr; only JSON is printed to stdout for piping.

set -e  # Exit on error

# Configuration
API_BASE="https://open-api.openocean.finance/v4"
NATIVE_TOKEN_ADDRESS="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"

# Default values: slippage in basis points (100 bps = 1%). API expects percentage (1 = 1%), so we convert.
SLIPPAGE_API_NUMERIC=""

# Python command fallback for environments where python3 is unavailable.
if command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_BIN="python"
else
    echo "Python is required but neither 'python3' nor 'python' was found." >&2
    exit 1
fi

# Validate arguments
if [ $# -lt 5 ]; then
    echo "Usage: $0 <chain> <tokenIn> <tokenOut> <amount> <sender> [slippageBps] [--enabled-dex-ids <csv>] [--disabled-dex-ids <csv>]" >&2
    echo "Example: $0 ethereum ETH USDC 1 0x742d35Cc6634C0532925a3b844Bc9e90F1b6fB28 100" >&2
    exit 1
fi

CHAIN="$1"
TOKEN_IN="$2"
TOKEN_OUT="$3"
AMOUNT="$4"
SENDER="$5"
SLIPPAGE_BPS=${6:-100}
ENABLED_DEX_IDS=""
DISABLED_DEX_IDS=""

# Parse optional arguments with backward compatibility:
# - 6th positional arg as slippageBps
# - flags: --enabled-dex-ids, --disabled-dex-ids
shift 5
if [ $# -gt 0 ] && [[ ! "$1" =~ ^-- ]]; then
    SLIPPAGE_BPS="$1"
    shift
fi
while [ $# -gt 0 ]; do
    case "$1" in
        --enabled-dex-ids)
            if [ -z "${2:-}" ]; then
                echo "Missing value for --enabled-dex-ids" >&2
                exit 1
            fi
            ENABLED_DEX_IDS="$2"
            shift 2
            ;;
        --disabled-dex-ids)
            if [ -z "${2:-}" ]; then
                echo "Missing value for --disabled-dex-ids" >&2
                exit 1
            fi
            DISABLED_DEX_IDS="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1" >&2
            exit 1
            ;;
    esac
done

# Must not set both enabled and disabled lists at the same time.
if [ -n "$ENABLED_DEX_IDS" ] && [ -n "$DISABLED_DEX_IDS" ]; then
    echo "Specify only one of --enabled-dex-ids or --disabled-dex-ids" >&2
    exit 1
fi

normalize_chain() {
    local chain_raw="$1"
    local c
    c=$(echo "$chain_raw" | tr '[:upper:]' '[:lower:]')
    case "$c" in
        # If already chain ID, pass through.
        ''|*[!0-9]*)
            ;;
        *)
            echo "$c"
            return 0
            ;;
    esac
    case "$c" in
        ethereum|mainnet) echo "eth" ;;
        eth) echo "eth" ;;
        binance-smart-chain|binance|bnb|bsc) echo "bsc" ;;
        polygon|matic) echo "polygon" ;;
        arbitrum|arbitrum-one) echo "arbitrum" ;;
        optimism|op) echo "optimism" ;;
        avalanche|avax) echo "avax" ;;
        base) echo "base" ;;
        fantom|ftm) echo "fantom" ;;
        gnosis|xdai) echo "xdai" ;;
        zksync|zksync-era) echo "zksync" ;;
        polygon-zkevm|polygon_zkevm) echo "polygon_zkevm" ;;
        *)
            # Unknown slug: pass through and let API validate.
            echo "$c"
            ;;
    esac
}

CHAIN_NORMALIZED=$(normalize_chain "$CHAIN")

# Validate numeric amount format early.
if ! [[ "$AMOUNT" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
    echo "Invalid amount format: $AMOUNT" >&2
    echo "Amount must be a positive decimal string, e.g. 1 or 0.5" >&2
    exit 1
fi

if [ "$AMOUNT" = "0" ] || [ "$AMOUNT" = "0.0" ]; then
    echo "Amount must be greater than 0" >&2
    exit 1
fi

# Convert bps -> API slippage percent and validate API bounds [0.05, 50].
SLIPPAGE_API=$("$PYTHON_BIN" -c "
from decimal import Decimal, InvalidOperation
import sys
try:
    bps = Decimal('$SLIPPAGE_BPS')
except InvalidOperation:
    print('INVALID')
    sys.exit(0)
v = bps / Decimal('100')
if v < Decimal('0.05') or v > Decimal('50'):
    print('OUT_OF_RANGE:' + format(v, 'f'))
    sys.exit(0)
s = format(v.normalize(), 'f')
if '.' in s:
    s = s.rstrip('0').rstrip('.')
print(s)
" 2>/dev/null || echo "INVALID")

if [ "$SLIPPAGE_API" = "INVALID" ]; then
    echo "Invalid slippage bps: $SLIPPAGE_BPS" >&2
    exit 1
fi

if [[ "$SLIPPAGE_API" == OUT_OF_RANGE:* ]]; then
    SLIPPAGE_API_NUMERIC="${SLIPPAGE_API#OUT_OF_RANGE:}"
    echo "Slippage out of range after conversion: ${SLIPPAGE_BPS}bps -> ${SLIPPAGE_API_NUMERIC}%" >&2
    echo "OpenOcean API v4 requires slippage between 0.05 and 50 (percent)." >&2
    exit 1
fi

echo "[*] Building swap: $AMOUNT $TOKEN_IN -> $TOKEN_OUT on $CHAIN" >&2
echo "   Chain normalized for API: $CHAIN_NORMALIZED" >&2
echo "   Sender: $SENDER" >&2
echo "   Slippage: $SLIPPAGE_BPS bps (= ${SLIPPAGE_API}% for API)" >&2
if [ -n "$ENABLED_DEX_IDS" ]; then echo "   enabledDexIds: $ENABLED_DEX_IDS" >&2; fi
if [ -n "$DISABLED_DEX_IDS" ]; then echo "   disabledDexIds: $DISABLED_DEX_IDS" >&2; fi

validate_dex_ids_format() {
    local ids="$1"
    local label="$2"
    if ! [[ "$ids" =~ ^[0-9]+(,[0-9]+)*$ ]]; then
        echo "Invalid $label format: $ids (expected csv integers like 1,2,3)" >&2
        exit 1
    fi
}

if [ -n "$ENABLED_DEX_IDS" ]; then validate_dex_ids_format "$ENABLED_DEX_IDS" "enabledDexIds"; fi
if [ -n "$DISABLED_DEX_IDS" ]; then validate_dex_ids_format "$DISABLED_DEX_IDS" "disabledDexIds"; fi

validate_dex_ids_against_chain() {
    local chain="$1"
    local ids_csv="$2"
    local label="$3"
    [ -z "$ids_csv" ] && return 0

    local dex_resp dex_indexes
    if ! dex_resp=$(curl -s "$API_BASE/$chain/dexList"); then
        echo "Failed to query dexList for chain $chain" >&2
        exit 1
    fi
    if [ "$(echo "$dex_resp" | jq -r '.code // 0')" != "200" ]; then
        echo "dexList API returned non-200 for chain $chain" >&2
        exit 1
    fi
    dex_indexes=$(echo "$dex_resp" | jq -r '.data[]?.index' | tr '\n' ' ')
    local missing=""
    IFS=',' read -r -a req_ids <<< "$ids_csv"
    for id in "${req_ids[@]}"; do
        if ! echo " $dex_indexes " | grep -q " $id "; then
            missing="$missing $id"
        fi
    done
    if [ -n "$missing" ]; then
        echo "$label contains unsupported dex indexes for chain $chain:$missing" >&2
        echo "Use /v4/$chain/dexList to choose valid indexes." >&2
        exit 1
    fi
}

validate_dex_ids_against_chain "$CHAIN_NORMALIZED" "$ENABLED_DEX_IDS" "enabledDexIds"
validate_dex_ids_against_chain "$CHAIN_NORMALIZED" "$DISABLED_DEX_IDS" "disabledDexIds"

# Step 1: Resolve token addresses
resolve_token_address() {
    local symbol="$1"
    local chain="$2"
    
    local symbol_lower=$(echo "$symbol" | tr '[:upper:]' '[:lower:]')
    
    case "$symbol_lower" in
        eth|ether|ethereum)
            echo "$NATIVE_TOKEN_ADDRESS"
            echo "18"
            return 0
            ;;
        usdc)
            case "$chain" in
                ethereum|1)
                    echo "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
                    echo "6"
                    ;;
                bsc|56)
                    echo "0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d"
                    echo "18"
                    ;;
                polygon|137)
                    echo "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174"
                    echo "6"
                    ;;
                arbitrum|42161)
                    echo "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8"
                    echo "6"
                    ;;
                *)
                    query_token_api "$symbol" "$chain"
                    ;;
            esac
            return 0
            ;;
        usdt)
            case "$chain" in
                ethereum|1)
                    echo "0xdAC17F958D2ee523a2206206994597C13D831ec7"
                    echo "6"
                    ;;
                bsc|56)
                    echo "0x55d398326f99059fF775485246999027B3197955"
                    echo "18"
                    ;;
                *)
                    query_token_api "$symbol" "$chain"
                    ;;
            esac
            return 0
            ;;
        *)
            query_token_api "$symbol" "$chain"
            ;;
    esac
}

query_token_api() {
    local symbol="$1"
    local chain="$2"
    local symbol_lower
    symbol_lower=$(echo "$symbol" | tr '[:upper:]' '[:lower:]')

    echo "   Querying OpenOcean token API for $symbol on $chain..." >&2
    
    if ! TOKEN_LIST_RESPONSE=$(curl -s "$API_BASE/$chain/tokenList"); then
        echo "Failed to query token API" >&2
        exit 1
    fi

    TOKEN_DATA=$(echo "$TOKEN_LIST_RESPONSE" | jq -r --arg symbol "$symbol_lower" '.data[] | select((.symbol | ascii_downcase) == $symbol) | [.address, .decimals] | @tsv' | head -1)

    if [ -z "$TOKEN_DATA" ]; then
        echo "Token $symbol not found on $chain" >&2
        exit 1
    fi
    
    TOKEN_ADDR=$(echo "$TOKEN_DATA" | cut -f1)
    TOKEN_DECIMALS=$(echo "$TOKEN_DATA" | cut -f2)
    
    echo "$TOKEN_ADDR"
    echo "$TOKEN_DECIMALS"
}

echo "   Resolving $TOKEN_IN address..." >&2
TOKEN_IN_DATA=$(resolve_token_address "$TOKEN_IN" "$CHAIN_NORMALIZED")
TOKEN_IN_ADDR=$(echo "$TOKEN_IN_DATA" | head -1)
TOKEN_IN_DECIMALS=$(echo "$TOKEN_IN_DATA" | tail -1)

echo "   Resolving $TOKEN_OUT address..." >&2
TOKEN_OUT_DATA=$(resolve_token_address "$TOKEN_OUT" "$CHAIN_NORMALIZED")
TOKEN_OUT_ADDR=$(echo "$TOKEN_OUT_DATA" | head -1)
TOKEN_OUT_DECIMALS=$(echo "$TOKEN_OUT_DATA" | tail -1)

echo "Token addresses resolved:" >&2
echo "   $TOKEN_IN: $TOKEN_IN_ADDR (decimals: $TOKEN_IN_DECIMALS)" >&2
echo "   $TOKEN_OUT: $TOKEN_OUT_ADDR (decimals: $TOKEN_OUT_DECIMALS)" >&2

echo "Fetching gas price..." >&2
if ! GAS_PRICE_RESPONSE=$(curl -s "$API_BASE/$CHAIN_NORMALIZED/gasPrice"); then
    echo "Failed to fetch gas price" >&2
    exit 1
fi

# Per OpenOcean API v4: Ethereum returns data.standard.legacyGasPrice / data.base (wei);
# other EVM chains may return data.standard as a number (wei). All values in wei.
GAS_PRICE=$(echo "$GAS_PRICE_RESPONSE" | jq -r '.data.standard.legacyGasPrice // .data.standard // .data.base')
if [ "$GAS_PRICE" = "null" ] || [ -z "$GAS_PRICE" ]; then
    echo "Could not extract gas price from response" >&2
    exit 1
fi

echo "Gas price: $GAS_PRICE wei" >&2

echo "Converting amount to wei..." >&2
AMOUNT_IN_WEI=$("$PYTHON_BIN" -c "
from decimal import Decimal, ROUND_DOWN
amount = Decimal('$AMOUNT')
decimals = int('$TOKEN_IN_DECIMALS')
scale = Decimal(10) ** decimals
result = (amount * scale).to_integral_value(rounding=ROUND_DOWN)
print(result)
")

echo "Amount in wei: $AMOUNT_IN_WEI" >&2

echo "Getting swap quote with calldata..." >&2
SWAP_URL="$API_BASE/$CHAIN_NORMALIZED/swap?inTokenAddress=$TOKEN_IN_ADDR&outTokenAddress=$TOKEN_OUT_ADDR&amountDecimals=$AMOUNT_IN_WEI&gasPriceDecimals=$GAS_PRICE&slippage=$SLIPPAGE_API&account=$SENDER"
if [ -n "$ENABLED_DEX_IDS" ]; then
    SWAP_URL="$SWAP_URL&enabledDexIds=$ENABLED_DEX_IDS"
fi
if [ -n "$DISABLED_DEX_IDS" ]; then
    SWAP_URL="$SWAP_URL&disabledDexIds=$DISABLED_DEX_IDS"
fi

if ! SWAP_RESPONSE=$(curl -s "$SWAP_URL"); then
    echo "Failed to call swap API" >&2
    exit 1
fi

RESPONSE_CODE=$(echo "$SWAP_RESPONSE" | jq -r '.code')
if [ "$RESPONSE_CODE" != "200" ]; then
    ERROR_MSG=$(echo "$SWAP_RESPONSE" | jq -r '.message // "Unknown error"')
    echo "API error $RESPONSE_CODE: $ERROR_MSG" >&2
    exit 1
fi

FROM=$(echo "$SWAP_RESPONSE" | jq -r '.data.from')
TO=$(echo "$SWAP_RESPONSE" | jq -r '.data.to')
VALUE=$(echo "$SWAP_RESPONSE" | jq -r '.data.value')
DATA=$(echo "$SWAP_RESPONSE" | jq -r '.data.data')
GAS=$(echo "$SWAP_RESPONSE" | jq -r '.data.estimatedGas')
CHAIN_ID=$(echo "$SWAP_RESPONSE" | jq -r '.data.chainId')
# Use gas price from swap response so the transaction matches the quote (OpenOcean API v4).
SWAP_GAS_PRICE=$(echo "$SWAP_RESPONSE" | jq -r '.data.gasPrice')
if [ -z "$SWAP_GAS_PRICE" ] || [ "$SWAP_GAS_PRICE" = "null" ]; then
    SWAP_GAS_PRICE="$GAS_PRICE"
fi

if [ -z "$DATA" ] || [ "$DATA" = "null" ]; then
    echo "No calldata in response" >&2
    exit 1
fi

# Gas fee in wei = gas limit * gas price (both from swap response). All units per API v4: wei.
GAS_FEE_WEI=$("$PYTHON_BIN" -c "
gas = int($GAS)
price = int('$SWAP_GAS_PRICE')
print(gas * price)
" 2>/dev/null || echo "0")
GAS_FEE_ETH=$("$PYTHON_BIN" -c "print(int('$GAS_FEE_WEI') / 1e18)" 2>/dev/null || echo "0")
GAS_PRICE_GWEI=$("$PYTHON_BIN" -c "print(int('$SWAP_GAS_PRICE') / 1e9)" 2>/dev/null || echo "0")

echo "Swap transaction built successfully" >&2
echo "   From: $FROM | To: $TO | Value: $VALUE wei | Gas: $GAS | Gas price: $SWAP_GAS_PRICE wei ($GAS_PRICE_GWEI Gwei) | Chain: $CHAIN_ID" >&2
echo "   Est. gas fee: $GAS_FEE_ETH ETH ($GAS_FEE_WEI wei)" >&2

# Only JSON to stdout for execute-swap.sh
# gasPrice is in wei (per OpenOcean API v4). gasPriceGwei and gasFeeEth prevent unit confusion downstream.
cat <<EOF
{
  "from": "$FROM",
  "to": "$TO",
  "value": "$VALUE",
  "data": "$DATA",
  "gas": "$GAS",
  "gasPrice": "$SWAP_GAS_PRICE",
  "gasPriceGwei": "$GAS_PRICE_GWEI",
  "gasFeeWei": "$GAS_FEE_WEI",
  "gasFeeEth": "$GAS_FEE_ETH",
  "chainId": "$CHAIN_ID",
  "tokenIn": "$TOKEN_IN",
  "tokenOut": "$TOKEN_OUT",
  "amount": "$AMOUNT",
  "slippage": "$SLIPPAGE_BPS",
  "enabledDexIds": "$ENABLED_DEX_IDS",
  "disabledDexIds": "$DISABLED_DEX_IDS"
  ,"chainInput": "$CHAIN"
  ,"chainNormalized": "$CHAIN_NORMALIZED"
}
EOF
