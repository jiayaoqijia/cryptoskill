# PnL Labs — MCP server & x402 API

> **PnL Labs gate — no verdict, no trade.** MCP: `https://api.pnllabs.com/mcp`
> Hard stops: `UNTRUSTED`/`INSUFFICIENT` → do not copy · `HIGH_RISK`/`CRITICAL` → do not buy ·
> `UNTRADEABLE`/`HIGH_COST` → not at that size · `UNVERIFIABLE`/`UNKNOWN` → say so, do not invent edge.
> Rule file: [SKILL.md](SKILL.md) · Measured examples: [docs/VERDICTS.md](docs/VERDICTS.md)

**Trust & risk verdicts for AI trading agents on Solana.** Proof of *real* PnL,
not peak scores. Pay-per-call via [x402](https://www.x402.org) (USDC on Solana) —
no signup, no API key, no account.

🌐 **[pnllabs.com](https://pnllabs.com)** · 🔌 **`https://api.pnllabs.com`** · 🐦 **[@pnllabs](https://x.com/pnllabs)**

---

## Connect in 10 seconds (hosted MCP — no install)

The server is hosted. Add it to any MCP-capable assistant with one URL:

```
https://api.pnllabs.com/mcp
```

- **Claude** (all plans): Settings → Connectors → *Add custom connector*
- **Grok**: [grok.com/connectors](https://grok.com/connectors) → *Custom*
- **ChatGPT / Gemini**: custom MCP connector → same URL
- Also listed in the [official MCP Registry](https://registry.modelcontextprotocol.io) (`io.github.PnLlabs/pnllabs`) and on Smithery.

Free tier per IP/day — when it runs out, the tools reply with structured
x402 payment instructions (pay-per-call, USDC on Solana).

---

## Why

Every "smart money" score you've seen ranks wallets by **peak or paper gains**.
Peaks lie. A wallet can 100x on paper, dump into no liquidity, and walk away red —
while its score still says genius.

PnL Labs recomputes what actually hit the wallet — realized SOL, in vs out — and
returns a conservative, machine-readable verdict. When the numbers can't be
reconstructed reliably, it says `UNVERIFIABLE` instead of guessing.

## The four checks

| Endpoint | Question | Verdicts |
|---|---|---|
| `GET /check/wallet/{address}` | Is this wallet worth copying? (real realized PnL) | `TRUSTED` · `NEUTRAL` · `UNTRUSTED` · `INSUFFICIENT` · `UNVERIFIABLE` |
| `GET /check/funder/{address}` | Where did this wallet's money come from? (funding origin / cluster links) | `CEX_FUNDED` · `WALLET_FUNDED` · `UNKNOWN_ORIGIN` · `UNVERIFIABLE_ORIGIN` |
| `GET /check/token/{mint}` | Is this token structurally safe? | `LOW_RISK` · `ELEVATED` · `HIGH_RISK` · `CRITICAL` · `UNKNOWN` |
| `GET /check/trade/{mint}?size_sol=1` | What will this trade really cost? (real slippage) | `ACCEPTABLE_COST` · `ELEVATED_COST` · `HIGH_COST` · `UNTRADEABLE` · `NO_POOL` |

Every response carries a stable `verdict` enum, machine-readable `reasons` (code +
message), `confidence`, `flags`, and `schema_version`. Built to be parsed by agents,
not read by humans. Interactive docs: `https://api.pnllabs.com/docs`.

## Quick example

```bash
curl https://api.pnllabs.com/check/wallet/57hECCDVNmP7jCY6XX6FxP31DQuKiwQhv2g3nxGPLPmV
```

```json
{
  "schema_version": 1,
  "verdict": "UNTRUSTED",
  "confidence": "high",
  "trust": 15,
  "reasons": [
    { "code": "NEGATIVE_REALIZED_PNL", "message": "Genuinely NEGATIVE: -47.1 SOL net realized" },
    { "code": "LOW_WIN_RATE", "message": "Only 27% of coins were profitable" }
  ]
}
```

## MCP server

This repo ships an [MCP](https://modelcontextprotocol.io) server exposing the four
checks as tools (`check_wallet_trust`, `check_wallet_forensics`, `check_token_safety`,
`check_trade_cost`). It calls the hosted API — no RPC keys or local setup needed.

**Add to an MCP client** (e.g. Claude Desktop / Claude Code):

```json
{
  "mcpServers": {
    "pnllabs": {
      "command": "python3",
      "args": ["/path/to/pnllabs_mcp.py"]
    }
  }
}
```

Runs on the Python standard library — no dependencies for the free/beta tier.

## Payment (x402)

Calls are priced per request and paid in USDC on Solana via the x402 protocol
(HTTP 402). Your agent pays a few cents, gets an on-chain receipt — no accounts,
no keys stored anywhere. Prices: wallet `0.10`, funder `0.05`, token/trade `0.02` USDC.
Any x402-capable client (or the official x402 SDKs) can pay automatically.

## Honest scope

- **Wallet trust & forensics** are the core edge — realized-PnL truth and funding
  origin, which peak-based scores and EVM-only tools don't provide on Solana.
- **Token safety** flags structural red flags with zero noise. Behavioral rugs
  (an operator selling into his own hype) are invisible to *all* structural
  checkers — for those, check the wallets involved.
- We sell **risk/trust verdicts, not alpha.** Never "when to buy."

## License

MIT — see [LICENSE](LICENSE).
