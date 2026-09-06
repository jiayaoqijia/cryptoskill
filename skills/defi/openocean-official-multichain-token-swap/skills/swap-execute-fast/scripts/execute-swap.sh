#!/bin/bash
# execute-swap.sh
# Builds and executes a swap in one step
# Usage: ./execute-swap.sh <chain> <tokenIn> <tokenOut> <amount> <sender> [slippageBps] [walletMethod] [keystoreName] [--enabled-dex-ids <csv>] [--disabled-dex-ids <csv>]

set -e  # Exit on error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FAST_SWAP_SCRIPT="$SCRIPT_DIR/fast-swap.sh"

# Validate arguments
if [ $# -lt 5 ]; then
    echo "Usage: $0 <chain> <tokenIn> <tokenOut> <amount> <sender> [slippageBps] [walletMethod] [keystoreName] [--enabled-dex-ids <csv>] [--disabled-dex-ids <csv>]"
    echo ""
    echo "Examples:"
    echo "  $0 ethereum ETH USDC 1 0x742d35Cc6634C0532925a3b844Bc9e90F1b6fB28 100"
    echo "  $0 arbitrum USDC ETH 100 0x742d35Cc6634C0532925a3b844Bc9e90F1b6fB28 100 ledger"
    echo "  $0 polygon MATIC USDC 10 0x742d35Cc6634C0532925a3b844Bc9e90F1b6fB28 100 keystore mykey"
    echo ""
    echo "Wallet Methods:"
    echo "  env      - Use ETH_RPC_URL and ETH_FROM env vars (default)"
    echo "  ledger   - Use Ledger hardware wallet"
    echo "  trezor   - Use Trezor hardware wallet"
    echo "  keystore - Use encrypted keystore file"
    exit 1
fi

CHAIN="$1"
TOKEN_IN="$2"
TOKEN_OUT="$3"
AMOUNT="$4"
SENDER="$5"
SLIPPAGE=${6:-100}
WALLET_METHOD=${7:-"env"}  # env, ledger, trezor, keystore
KEYSTORE_NAME=${8:-""}
ENABLED_DEX_IDS=""
DISABLED_DEX_IDS=""

# Parse optional flags after legacy positional args.
if [ $# -ge 9 ]; then
    shift 8
    while [ $# -gt 0 ]; do
        case "$1" in
            --enabled-dex-ids)
                if [ -z "${2:-}" ]; then
                    echo "Missing value for --enabled-dex-ids"
                    exit 1
                fi
                ENABLED_DEX_IDS="$2"
                shift 2
                ;;
            --disabled-dex-ids)
                if [ -z "${2:-}" ]; then
                    echo "Missing value for --disabled-dex-ids"
                    exit 1
                fi
                DISABLED_DEX_IDS="$2"
                shift 2
                ;;
            *)
                echo "Unknown argument: $1"
                exit 1
                ;;
        esac
    done
fi

if [ -n "$ENABLED_DEX_IDS" ] && [ -n "$DISABLED_DEX_IDS" ]; then
    echo "Specify only one of --enabled-dex-ids or --disabled-dex-ids"
    exit 1
fi

echo "OpenOcean Fast Swap Execution"
echo "========================================"
echo "WARNING: This will execute immediately without confirmation!"
echo "========================================"
echo ""
echo "Parameters:"
echo "  Chain:     $CHAIN"
echo "  Swap:      $AMOUNT $TOKEN_IN -> $TOKEN_OUT"
echo "  Sender:    $SENDER"
echo "  Slippage:  $SLIPPAGE bps"
echo "  Wallet:    $WALLET_METHOD"
if [ "$WALLET_METHOD" = "keystore" ] && [ -n "$KEYSTORE_NAME" ]; then
    echo "  Keystore:  $KEYSTORE_NAME"
fi
if [ -n "$ENABLED_DEX_IDS" ]; then echo "  enabledDexIds: $ENABLED_DEX_IDS"; fi
if [ -n "$DISABLED_DEX_IDS" ]; then echo "  disabledDexIds: $DISABLED_DEX_IDS"; fi
echo ""

# Check prerequisites
echo "Checking prerequisites..."
if ! command -v cast &> /dev/null; then
    echo "Foundry 'cast' command not found. Please install Foundry:"
    echo "   curl -L https://foundry.paradigm.xyz | bash"
    echo "   foundryup"
    exit 1
fi

if ! command -v jq &> /dev/null; then
    echo "'jq' command not found. Please install jq:"
    echo "   sudo apt-get install jq   # Ubuntu/Debian"
    echo "   brew install jq           # macOS"
    exit 1
fi

if [ -z "$ETH_RPC_URL" ]; then
    echo "ETH_RPC_URL environment variable not set"
    echo "   export ETH_RPC_URL=https://rpc.example.com"
    exit 1
fi

echo "Prerequisites satisfied"

# Step 1: Build swap transaction
echo ""
echo "Building swap transaction..."
FAST_SWAP_ARGS=("$CHAIN" "$TOKEN_IN" "$TOKEN_OUT" "$AMOUNT" "$SENDER" "$SLIPPAGE")
if [ -n "$ENABLED_DEX_IDS" ]; then
    FAST_SWAP_ARGS+=("--enabled-dex-ids" "$ENABLED_DEX_IDS")
fi
if [ -n "$DISABLED_DEX_IDS" ]; then
    FAST_SWAP_ARGS+=("--disabled-dex-ids" "$DISABLED_DEX_IDS")
fi

if ! TX_JSON=$("$FAST_SWAP_SCRIPT" "${FAST_SWAP_ARGS[@]}"); then
    echo "Failed to build swap transaction."
    exit 1
fi
if [ -z "$TX_JSON" ]; then
    echo "Failed to build swap transaction: empty response."
    exit 1
fi

# Validate JSON before parsing
if ! echo "$TX_JSON" | jq -e . >/dev/null 2>&1; then
    echo "Invalid JSON from build step. Check network and API."
    exit 1
fi

# Parse JSON output
FROM=$(echo "$TX_JSON" | jq -r '.from')
TO=$(echo "$TX_JSON" | jq -r '.to')
VALUE=$(echo "$TX_JSON" | jq -r '.value')
DATA=$(echo "$TX_JSON" | jq -r '.data')
GAS=$(echo "$TX_JSON" | jq -r '.gas')
GAS_PRICE=$(echo "$TX_JSON" | jq -r '.gasPrice')
CHAIN_ID=$(echo "$TX_JSON" | jq -r '.chainId')
GAS_PRICE_GWEI=$(echo "$TX_JSON" | jq -r '.gasPriceGwei // empty')
GAS_FEE_ETH=$(echo "$TX_JSON" | jq -r '.gasFeeEth // empty')

echo "Transaction built:"
echo "   From:    $FROM"
echo "   To:      $TO"
echo "   Value:   $VALUE wei"
echo "   Gas:     $GAS"
echo "   Gas Price: $GAS_PRICE wei${GAS_PRICE_GWEI:+ ($GAS_PRICE_GWEI Gwei)}"
if [ -n "$GAS_FEE_ETH" ] && [ "$GAS_FEE_ETH" != "null" ]; then
    echo "   Est. gas fee: $GAS_FEE_ETH ETH"
fi
echo "   Chain ID: $CHAIN_ID"

# Step 2: Execute transaction
echo ""
echo "Executing transaction..."

# Build wallet-specific auth args first, then reuse for estimate + send.
case "$WALLET_METHOD" in
    env)
        if [ -z "$ETH_FROM" ]; then
            echo "ETH_FROM environment variable not set"
            echo "   export ETH_FROM=0xYourAddress"
            exit 1
        fi
        AUTH_ARGS=(--from "$ETH_FROM")
        ;;
    
    ledger)
        AUTH_ARGS=(--ledger)
        ;;
    
    trezor)
        AUTH_ARGS=(--trezor)
        ;;
    
    keystore)
        if [ -z "$KEYSTORE_NAME" ]; then
            echo "Keystore name required for keystore method"
            echo "   Usage: $0 ... keystore <name>"
            exit 1
        fi
        
        # Look for keystore file
        KEYSTORE_FILE="$HOME/.foundry/keystores/$KEYSTORE_NAME"
        if [ ! -f "$KEYSTORE_FILE" ]; then
            # Try alternative location
            KEYSTORE_FILE="$HOME/.ethereum/keystore/$KEYSTORE_NAME"
        fi
        
        if [ ! -f "$KEYSTORE_FILE" ]; then
            echo "Keystore file not found: $KEYSTORE_NAME"
            echo "   Expected locations:"
            echo "     ~/.foundry/keystores/$KEYSTORE_NAME"
            echo "     ~/.ethereum/keystore/$KEYSTORE_NAME"
            exit 1
        fi
        AUTH_ARGS=(--keystore "$KEYSTORE_FILE")
        ;;
    
    *)
        echo "Unknown wallet method: $WALLET_METHOD"
        echo "   Supported: env, ledger, trezor, keystore"
        exit 1
        ;;
esac

# Re-estimate gas from RPC and apply 25% safety buffer (per OpenOcean v4 integration guidance).
echo "Re-estimating gas with RPC..."
ESTIMATE_ARGS=(estimate --rpc-url "$ETH_RPC_URL" "${AUTH_ARGS[@]}" --value "$VALUE" "$TO" "$DATA")
EST_GAS_RAW=$(cast "${ESTIMATE_ARGS[@]}" 2>/dev/null || true)
EST_GAS=$(echo "$EST_GAS_RAW" | tr -d '[:space:]')
if [[ "$EST_GAS" =~ ^[0-9]+$ ]]; then
    GAS=$(( (EST_GAS * 125 + 99) / 100 ))
    echo "   Estimated gas: $EST_GAS, using buffered gas: $GAS"
else
    echo "   Gas estimation failed, fallback to swap response gas: $GAS"
fi

CAST_ARGS=(send --rpc-url "$ETH_RPC_URL" "${AUTH_ARGS[@]}" --value "$VALUE" --gas "$GAS" --gas-price "$GAS_PRICE" --chain "$CHAIN_ID" "$TO" "$DATA")

echo "   Command: cast send --rpc-url <redacted> ... --gas $GAS --gas-price $GAS_PRICE --chain $CHAIN_ID ..."
echo ""

# Execute the command
echo "Broadcasting transaction..."
set +e
TX_RESULT=$(cast "${CAST_ARGS[@]}" 2>&1)
CAST_EXIT_CODE=$?
set -e

if [ $CAST_EXIT_CODE -eq 0 ]; then
    # Extract transaction hash from cast output
    TX_HASH=$(echo "$TX_RESULT" | grep -o '0x[0-9a-fA-F]\{64\}' | head -1)
    
    if [ -n "$TX_HASH" ]; then
        echo ""
        echo "Transaction broadcast successfully."
        echo "   Transaction Hash: $TX_HASH"
        
        # Generate block explorer URL based on chain
        case "$CHAIN" in
            ethereum|1)
                EXPLORER_URL="https://etherscan.io/tx/$TX_HASH"
                ;;
            sepolia|11155111)
                EXPLORER_URL="https://sepolia.etherscan.io/tx/$TX_HASH"
                ;;
            bsc|56)
                EXPLORER_URL="https://bscscan.com/tx/$TX_HASH"
                ;;
            arbitrum|42161)
                EXPLORER_URL="https://arbiscan.io/tx/$TX_HASH"
                ;;
            polygon|137)
                EXPLORER_URL="https://polygonscan.com/tx/$TX_HASH"
                ;;
            base|8453)
                EXPLORER_URL="https://basescan.org/tx/$TX_HASH"
                ;;
            *)
                EXPLORER_URL="Transaction hash: $TX_HASH"
                ;;
        esac
        
        echo "   Explorer: $EXPLORER_URL"
        echo ""
        echo "Transaction Details:"
        echo "$TX_RESULT"
    else
        echo "Transaction broadcast successfully."
        echo "$TX_RESULT"
    fi
else
    echo "Transaction failed."
    echo ""
    echo "Error output:"
    echo "$TX_RESULT"
    echo ""
    echo "Troubleshooting:"
    echo "1. Check wallet balance and allowances"
    echo "2. Verify RPC endpoint is working"
    echo "3. Ensure wallet is properly connected/unlocked"
    echo "4. Try with higher slippage or gas price"
    exit 1
fi

echo ""
echo "========================================"
echo "REMINDER: This executed without confirmation!"
echo "   Always verify transaction on block explorer."
echo "========================================"
