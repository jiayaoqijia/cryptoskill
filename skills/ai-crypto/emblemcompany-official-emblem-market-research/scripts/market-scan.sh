#!/bin/bash
# market-scan.sh - Daily crypto market scan via EmblemAI
# Usage: bash scripts/market-scan.sh [chain]

set -e

CHAIN="${1:-solana}"

echo "Market Scan — $(date '+%Y-%m-%d %H:%M')"
echo "Chain: $CHAIN"
echo "=================================================="

if ! command -v emblemai &> /dev/null; then
    echo "Error: emblemai CLI not found"
    echo "Install with: npm install -g @emblemvault/agentwallet"
    exit 1
fi

echo ""
echo "1. Trending Tokens (CoinGecko)"
echo "-------------------------------"
emblemai --agent --profile default -m "Use getTrendingCoins to show what's trending globally with prices and 24h change"

echo ""
echo "2. Trending on $CHAIN (Birdeye)"
echo "--------------------------------"
emblemai --agent --profile default -m "Use birdeyeTrendingTokens on $CHAIN to show top trending tokens by volume"

echo ""
echo "3. Smart Money Activity (Nansen)"
echo "---------------------------------"
emblemai --agent --profile default -m "Use nansen_smart_money_flows to show token net flows on $CHAIN in the last 24h"

echo ""
echo "4. Derivatives (CoinGlass)"
echo "---------------------------"
emblemai --agent --profile default -m "Use getCoinglassOpenInterestHistory to show BTC open interest, and getCoinglassHyperliquidWhaleAlert for whale positions"

echo ""
echo "=================================================="
echo "Scan complete. Run with a chain: bash scripts/market-scan.sh base"
