#!/usr/bin/env bash
# KryptoGO Meme Trader — Portfolio Check
#
# Shows wallet balance, token holdings, and PnL summary.
#
# Usage:
#   bash scripts/portfolio.sh                    # Uses SOLANA_WALLET_ADDRESS from .env
#   bash scripts/portfolio.sh <wallet_address>   # Check a specific wallet

set -euo pipefail

# Credentials must be pre-loaded in the environment (source ~/.openclaw/workspace/.env)
if [ -z "${KRYPTOGO_API_KEY:-}" ]; then
  echo "ERROR: Run 'source ~/.openclaw/workspace/.env' before running this script."
  exit 1
fi

BASE="https://wallet-data.kryptogo.app"
AUTH="Authorization: Bearer $KRYPTOGO_API_KEY"
WALLET="${1:-$SOLANA_WALLET_ADDRESS}"

curl -s "$BASE/agent/portfolio?wallet_address=$WALLET" -H "$AUTH" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f\"Wallet: {d.get('wallet', '?')}\")
print(f\"SOL Balance: {d.get('sol_balance', '0')} SOL\")
print(f\"Realized PnL: {d.get('total_realized_pnl', '0')}\")
print(f\"Unrealized PnL: {d.get('total_unrealized_pnl', '0')}\")
tokens = d.get('tokens', [])
if tokens:
    print(f'Holdings: {len(tokens)} tokens')
    for t in tokens[:10]:
        sym = t.get('symbol', '?')
        bal = t.get('balance', '?')
        pnl = t.get('unrealized_pnl', '?')
        print(f'  - {sym}: {bal} (PnL: {pnl})')
else:
    print('Holdings: None (empty wallet)')
"
