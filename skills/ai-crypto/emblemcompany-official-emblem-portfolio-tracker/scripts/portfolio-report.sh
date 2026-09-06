#!/bin/bash
# portfolio-report.sh - Generate a cross-chain portfolio report via EmblemAI
# Usage: bash scripts/portfolio-report.sh

set -e

echo "Portfolio Report — $(date '+%Y-%m-%d %H:%M')"
echo "=================================================="

if ! command -v emblemai &> /dev/null; then
    echo "Error: emblemai CLI not found"
    echo "Install with: npm install -g @emblemvault/agentwallet"
    exit 1
fi

echo ""
echo "1. Wallet Addresses"
echo "-------------------"
emblemai --agent --profile default -m "Use wallet to list all my wallet addresses across every chain"

echo ""
echo "2. Balance Snapshot"
echo "-------------------"
emblemai --agent --profile default -m "Show my balances with USD values across all chains. Use these tools: solanaBalances, ethGetBalances, baseGetBalances, bscGetBalances, polygonGetBalances, hederaGetBalances, getBTCBalances"

echo ""
echo "3. Trade Positions"
echo "-------------------"
emblemai --agent --profile default -m "Use getAllPositions to show my conditional trade positions with realized P&L"

echo ""
echo "=================================================="
echo "Report complete."
