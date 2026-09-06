#!/bin/bash
# memecoin-scan.sh - Scan trending memecoins via EmblemAI
# Usage: bash scripts/memecoin-scan.sh [platform]
# Platforms: pumpfun (default), launchlab, clanker, hedera

set -e

PLATFORM="${1:-pumpfun}"

echo "Memecoin Scout — $(date '+%Y-%m-%d %H:%M')"
echo "Platform: $PLATFORM"
echo "=================================================="

if ! command -v emblemai &> /dev/null; then
    echo "Error: emblemai CLI not found"
    echo "Install with: npm install -g @emblemvault/agentwallet"
    exit 1
fi

echo ""
echo "1. New Launches"
echo "----------------"
if [ "$PLATFORM" = "pumpfun" ]; then
    emblemai --agent --profile default -m "Use getPumpFunTokens with type about_to_graduate to show tokens about to graduate with holder data, dev hold %, and volume"
elif [ "$PLATFORM" = "launchlab" ]; then
    emblemai --agent --profile default -m "Use discoverLaunchLabTokens to show newest LaunchLab token launches with curve data"
elif [ "$PLATFORM" = "clanker" ]; then
    emblemai --agent --profile default -m "Use baseFindClankerTokens to show new Clanker tokens on Base with market cap and creator info"
elif [ "$PLATFORM" = "hedera" ]; then
    emblemai --agent --profile default -m "Use hederaFindMemeCoins to show trending memecoins on Hedera with market cap and socials"
else
    echo "Unknown platform: $PLATFORM"
    echo "Available: pumpfun, launchlab, clanker, hedera"
    exit 1
fi

echo ""
echo "2. Trending Gems (Solana)"
echo "--------------------------"
emblemai --agent --profile default -m "Use findSolanaGems with sortBy trending to show top trending tokens with organic score and holder count"

echo ""
echo "3. Smart Money Memecoin Activity"
echo "---------------------------------"
emblemai --agent --profile default -m "Use nansen_smart_money_trades to show what smart money is trading on solana right now"

echo ""
echo "=================================================="
echo "Scan complete. Platforms: pumpfun, launchlab, clanker, hedera"
