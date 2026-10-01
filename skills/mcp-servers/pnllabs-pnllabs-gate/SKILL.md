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

Order: Wallet before copying → Token before buying → Trade for your size. All must pass.

Hard stops:
- Wallet: UNTRUSTED, INSUFFICIENT, UNVERIFIABLE, UNKNOWN, or flag known_sniper_bot → do not copy
- Token: HIGH_RISK, CRITICAL, UNKNOWN → do not buy
- Trade: HIGH_COST, UNTRADEABLE, NO_POOL, UNKNOWN → do not buy at that size
- Funder: flag fresh_wallet → do not copy; UNKNOWN_ORIGIN, UNVERIFIABLE_ORIGIN, UNKNOWN → no conclusion
- HTTP 402 / PaymentRequired, errors and timeouts are not verdicts → no trade

Proceed only on: Wallet TRUSTED (NEUTRAL = no proven edge, never size up), Token LOW_RISK
(ELEVATED = reduced size), Trade ACCEPTABLE_COST (ELEVATED_COST = reduce toward
recommended_max_size_sol). UNKNOWN / UNVERIFIABLE → say so, do not invent edge.

Never use leaderboard PnL or peak-gain screenshots as proof.
Quote verdict + first reason code before acting (headers X-Verdict, X-Reason).
Full table: https://pnllabs.com/GATE.md

Payment: 5 free checks per IP per UTC day (header `X-RateLimit-Remaining`).
After that HTTP 402 — pay per call via x402 (USDC on Solana; header PAYMENT-SIGNATURE)
or send a prepaid `X-API-Key` (top up: https://api.pnllabs.com/credits).
