#!/bin/bash
# swap-helper.sh - Token swap walkthrough via EmblemAI
# Usage: bash scripts/swap-helper.sh

set -e

echo "Token Swap Helper"
echo "=================================================="

if ! command -v emblemai &> /dev/null; then
    echo "Error: emblemai CLI not found"
    echo "Install with: npm install -g @emblemvault/agentwallet"
    exit 1
fi

echo ""
echo "Step 1: Current Balances"
echo "------------------------"
emblemai --agent --profile default -m "Show my balances with USD values. Use solanaBalances, ethGetBalances, baseGetBalances, bscGetBalances, polygonGetBalances, hederaGetBalances, getBTCBalances"

echo ""
echo "Step 2: Swap Commands by Chain"
echo "------------------------------"
echo ""
echo "  Solana:     emblemai --agent --profile default -m 'Use splBuyIntent to swap 5 SOL for USDC'"
echo "  Ethereum:   emblemai --agent --profile default -m 'Use ethSwap to swap 0.01 ETH for USDC'"
echo "  Base:       emblemai --agent --profile default -m 'Use baseSwap to swap 0.005 ETH for USDC'"
echo "  BSC:        emblemai --agent --profile default -m 'Use bscSwap to swap 0.1 BNB for USDT'"
echo "  Polygon:    emblemai --agent --profile default -m 'Use polygonSwap to swap 10 POL for USDC'"
echo "  Hedera:     emblemai --agent --profile default -m 'Use hederaTokensSwap to swap 100 HBAR for USDC'"
echo "  Bridge:     emblemai --agent --profile default -m 'Use getChangeNowSwapQuote to bridge 0.05 ETH to SOL'"
echo ""
echo "Tips:"
echo "  - Name the exact tool for reliable routing"
echo "  - Safe mode will ask for confirmation before executing"
echo "  - Solana splBuyIntent supports \$USD, SOL, or token amounts"
echo ""
echo "=================================================="
