---
name: pnllabs-gate
description: Before copying a Solana wallet or buying a mint, call PnL Labs and obey the verdict.
---

# PnL Labs Gate

MCP: https://api.pnllabs.com/mcp

HTTP:
- GET https://api.pnllabs.com/check/wallet/{address}
- GET https://api.pnllabs.com/check/token/{mint}
- GET https://api.pnllabs.com/check/trade/{mint}?size_sol={size}
- GET https://api.pnllabs.com/check/funder/{address}

Hard stops:
- UNTRUSTED or INSUFFICIENT → do not copy
- HIGH_RISK or CRITICAL → do not buy
- UNTRADEABLE or HIGH_COST → do not buy at that size
- UNVERIFIABLE or UNKNOWN → say so, do not invent edge

Never use leaderboard PnL or peak-gain screenshots as proof.
Quote verdict + first reason code before acting.

Payment: 5 free checks per IP per UTC day (header `X-RateLimit-Remaining`).
After that HTTP 402 — pay per call via x402 (USDC on Solana) or send a prepaid
`X-API-Key` (top up: https://api.pnllabs.com/credits). A 402 is not a verdict:
no verdict, no trade.
