#!/usr/bin/env bash
# KryptoGO Meme Trader — Trending Token Scanner
#
# Lists top trending tokens by 24h volume on Solana.
#
# Usage:
#   bash scripts/trending.sh           # Default: top 10 by volume on Solana
#   bash scripts/trending.sh 20        # Top 20
#   bash scripts/trending.sh 10 56     # Top 10 on BSC (chain_id=56)

set -euo pipefail

# Credentials must be pre-loaded in the environment (source ~/.openclaw/workspace/.env)
if [ -z "${KRYPTOGO_API_KEY:-}" ]; then
  echo "ERROR: Run 'source ~/.openclaw/workspace/.env' before running this script."
  exit 1
fi

BASE="https://wallet-data.kryptogo.app"
AUTH="Authorization: Bearer $KRYPTOGO_API_KEY"
PAGE_SIZE="${1:-10}"
CHAIN_ID="${2:-501}"

curl -s "$BASE/agent/trending-tokens?chain_id=$CHAIN_ID&page_size=$PAGE_SIZE&sort_by=volume" -H "$AUTH" | python3 -c "
import sys, json
d = json.load(sys.stdin)
tokens = d.get('tokens', d.get('data', []))
for i, t in enumerate(tokens):
    sym = t.get('symbol', '?')
    mc = float(t.get('market_cap', 0) or 0)
    vol = float(t.get('volume_24h', t.get('volume', 0)) or 0)
    addr = t.get('contract_address', t.get('token_mint', '?'))
    print(f'{i+1:2d}. {sym:12s} mc=\${mc/1e6:.1f}M  vol24h=\${vol/1e6:.1f}M  {addr}')
"
