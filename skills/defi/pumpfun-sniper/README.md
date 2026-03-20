# pump.fun Sniper Scorer

Score any Solana token CA 0-100 for snipe safety before you buy.

## Scores 4 risk dimensions

- **Dev Wallet (30pts)** — SOL balance + prior launch history
- **Social Links (20pts)** — Twitter, Telegram, website, description
- **Liquidity (25pts)** — Liquidity USD, buy/sell ratio, 1h volume
- **Holder Concentration (25pts)** — Top 5 holder %, dev wallet %

## Verdict

| Score | Verdict |
|-------|---------|
| 70–100 | 🎯 SNIPE — low rug signals |
| 45–69 | ⚠️ CAUTION — mixed signals |
| 0–44 | 🚨 AVOID — high rug risk |

## Quick Start

```bash
pip install -r api/requirements.txt
python3 scripts/scorer.py <TOKEN_CA>
```

## Paid API

`https://pumpfun-sniper-production.up.railway.app/score?ca=<TOKEN_CA>`

$0.05 USDC per request via x402 on Base chain.

## License

MIT
