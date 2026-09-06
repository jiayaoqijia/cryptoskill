#!/bin/bash
# yield-scan.sh - Scan DeFi yield landscape via EmblemAI
# Usage: bash scripts/yield-scan.sh [chain]

set -e

CHAIN="${1:-Solana}"

echo "DeFi Yield Scan — $(date '+%Y-%m-%d %H:%M')"
echo "Chain: $CHAIN"
echo "=================================================="

if ! command -v emblemai &> /dev/null; then
    echo "Error: emblemai CLI not found"
    echo "Install with: npm install -g @emblemvault/agentwallet"
    exit 1
fi

echo ""
echo "1. Yield Opportunities"
echo "----------------------"
emblemai --agent --profile default -m "What are the best yield farming opportunities on $CHAIN right now? Include liquid staking, LP strategies, lending protocols, and estimated APYs. Use birdeyeTrendingTokens to check what tokens are trending."

echo ""
echo "2. Smart Money DeFi Activity"
echo "----------------------------"
emblemai --agent --profile default -m "Use nansen_smart_money_holdings to show what smart money is holding on ${CHAIN,,}. Focus on DeFi tokens, LSTs, and yield-bearing assets."

echo ""
echo "3. My Balances"
echo "--------------"
if [ "${CHAIN,,}" = "solana" ]; then
    emblemai --agent --profile default -m "Use solanaBalances to show my Solana token balances"
elif [ "${CHAIN,,}" = "ethereum" ]; then
    emblemai --agent --profile default -m "Use ethGetBalances to show my Ethereum token balances"
elif [ "${CHAIN,,}" = "base" ]; then
    emblemai --agent --profile default -m "Use baseGetBalances to show my Base token balances"
elif [ "${CHAIN,,}" = "bsc" ]; then
    emblemai --agent --profile default -m "Use bscGetBalances to show my BSC token balances"
elif [ "${CHAIN,,}" = "polygon" ]; then
    emblemai --agent --profile default -m "Use polygonGetBalances to show my Polygon token balances"
elif [ "${CHAIN,,}" = "hedera" ]; then
    emblemai --agent --profile default -m "Use hederaGetBalances to show my Hedera token balances"
else
    echo "Unknown chain: $CHAIN"
fi

echo ""
echo "=================================================="
echo "Scan complete. Run with a chain: bash scripts/yield-scan.sh Ethereum"
