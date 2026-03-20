#!/usr/bin/env bash
# KryptoGO Meme Trader — Full Analysis Dashboard
#
# Combines portfolio check, signal dashboard, trending tokens, and
# top candidate scoring into a single view. Useful for periodic scans
# or quick market assessment.
#
# Usage:
#   bash scripts/analysis.sh

set -euo pipefail

# Credentials must be pre-loaded in the environment (source ~/.openclaw/workspace/.env)
if [ -z "${KRYPTOGO_API_KEY:-}" ]; then
  echo "ERROR: Run 'source ~/.openclaw/workspace/.env' before running this script."
  exit 1
fi

BASE="https://wallet-data.kryptogo.app"
AUTH="Authorization: Bearer $KRYPTOGO_API_KEY"

echo "========================================="
echo "  KryptoGO Meme Trader - Full Analysis"
echo "========================================="
echo ""

# 1. Portfolio check
echo "=== PORTFOLIO ==="
curl -s "$BASE/agent/portfolio?wallet_address=$SOLANA_WALLET_ADDRESS" -H "$AUTH" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f\"Wallet: {d.get('wallet','?')}\")
print(f\"SOL Balance: {d.get('sol_balance','0')} SOL\")
print(f\"Realized PnL: {d.get('total_realized_pnl','0')}\")
print(f\"Unrealized PnL: {d.get('total_unrealized_pnl','0')}\")
tokens = d.get('tokens', [])
if tokens:
    print(f'Holdings: {len(tokens)} tokens')
    for t in tokens[:5]:
        print(f\"  - {t.get('symbol','?')}: {t.get('balance','?')} (PnL: {t.get('unrealized_pnl','?')})\")
else:
    print('Holdings: None (empty wallet)')
" 2>&1
echo ""

# 2. Signal Dashboard (Pro/Alpha tier — will 403 on Free tier)
echo "=== SIGNAL DASHBOARD (Accumulation Signals) ==="
curl -s "$BASE/signal-dashboard" -H "$AUTH" | python3 -c "
import sys, json
d = json.load(sys.stdin)
signals = d.get('signals', [])
print(f'Total signals: {len(signals)}')
print('')
for s in signals[:15]:
    sym = s.get('symbol', '?')
    chain = s.get('chain', '?')
    pct = s.get('price_change_percent', 0)
    max_pct = s.get('max_price_change_percent', 0)
    pattern = s.get('pattern', '?')
    cr_at = s.get('cluster_ratio_at_signal')
    cr_now = s.get('current_cluster_ratio')
    addr = s.get('contract_address', '?')
    direction = '+' if pct >= 0 else ''
    cr_str = f'CR: {cr_at:.1f}%→{cr_now:.1f}%' if cr_at and cr_now else 'CR: N/A'
    print(f'  {sym:12s} [{chain}] {pattern:12s} {direction}{pct:.0f}% (max {direction}{max_pct:.0f}%)  {cr_str}  {addr[:16]}...')
" 2>&1
echo ""

# 3. Trending tokens
echo "=== TRENDING TOKENS (by volume) ==="
curl -s "$BASE/agent/trending-tokens?chain_id=501&page_size=10&sort_by=volume" -H "$AUTH" | python3 -c "
import sys, json
d = json.load(sys.stdin)
tokens = d.get('tokens', d.get('data', []))
for i, t in enumerate(tokens[:10]):
    sym = t.get('symbol', '?')
    mc = float(t.get('market_cap', 0) or 0)
    vol = float(t.get('volume_24h', t.get('volume', 0)) or 0)
    addr = t.get('contract_address', t.get('token_mint', '?'))
    print(f'{i+1:2d}. {sym:12s} mc=\${mc/1e6:.1f}M  vol24h=\${vol/1e6:.1f}M  {addr}')
" 2>&1
echo ""

# 4. Top candidates from signals (scored by cluster ratio growth)
echo "=== TOP CANDIDATES FOR ANALYSIS ==="
curl -s "$BASE/signal-dashboard" -H "$AUTH" | python3 -c "
import sys, json
d = json.load(sys.stdin)
signals = d.get('signals', [])

candidates = []
for s in signals:
    pct = s.get('price_change_percent', 0)
    max_pct = s.get('max_price_change_percent', 0)
    cr_at = s.get('cluster_ratio_at_signal')
    cr_now = s.get('current_cluster_ratio')

    cr_growth = (cr_now - cr_at) if cr_at and cr_now and cr_now > cr_at else 0

    candidates.append({
        'symbol': s.get('symbol', '?'),
        'address': s.get('contract_address', '?'),
        'chain': s.get('chain', '?'),
        'pct': pct,
        'max_pct': max_pct,
        'cr_at': cr_at,
        'cr_now': cr_now,
        'cr_growth': cr_growth,
        'pattern': s.get('pattern', '?'),
    })

candidates.sort(key=lambda x: x['cr_growth'], reverse=True)

print('Top 5 by cluster ratio growth (strongest accumulation):')
for i, c in enumerate(candidates[:5]):
    cr_str = f'CR: {c[\"cr_at\"]:.1f}%→{c[\"cr_now\"]:.1f}% (+{c[\"cr_growth\"]:.1f}pp)' if c['cr_at'] and c['cr_now'] else 'CR: N/A'
    print(f'  {i+1}. {c[\"symbol\"]:12s} [{c[\"chain\"]}] price: {c[\"pct\"]:+.0f}% (max: +{c[\"max_pct\"]:.0f}%)  {cr_str}  {c[\"address\"]}')
print()

# Early-stage tokens (price near signal, CR growing)
early = [c for c in candidates if -20 < c['pct'] < 50 and c['cr_growth'] > 0]
early.sort(key=lambda x: x['cr_growth'], reverse=True)
if early:
    print('Early stage (price near signal entry, CR still growing):')
    for i, c in enumerate(early[:5]):
        cr_str = f'CR: {c[\"cr_at\"]:.1f}%→{c[\"cr_now\"]:.1f}% (+{c[\"cr_growth\"]:.1f}pp)' if c['cr_at'] and c['cr_now'] else 'CR: N/A'
        print(f'  {i+1}. {c[\"symbol\"]:12s} [{c[\"chain\"]}] price: {c[\"pct\"]:+.0f}%  {cr_str}  {c[\"address\"]}')
" 2>&1
echo ""

echo "=== DONE ==="
