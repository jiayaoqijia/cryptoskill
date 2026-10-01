# PnL Labs gate — verdict → agent action

No verdict, no trade. One table for every check. SKILL.md and the MCP instructions follow it.

| Check (MCP tool · HTTP) | Proceed | Proceed with limits | Abort |
|---|---|---|---|
| **Wallet** · `check_wallet_trust` · `GET /check/wallet/{address}` | `TRUSTED` — copying allowed; still run Token + Trade for every trade | `NEUTRAL` — no proven edge: never size up because of it | `UNTRUSTED`, `INSUFFICIENT`, `UNVERIFIABLE`, `UNKNOWN`; flag `known_sniper_bot` |
| **Token** · `check_token_safety` · `GET /check/token/{mint}` | `LOW_RISK` | `ELEVATED` — reduced size, read the reasons | `HIGH_RISK`, `CRITICAL`, `UNKNOWN` |
| **Trade** · `check_trade_cost` · `GET /check/trade/{mint}?size_sol=` | `ACCEPTABLE_COST` | `ELEVATED_COST` — reduce toward `recommended_max_size_sol` | `HIGH_COST` (at that size), `UNTRADEABLE`, `NO_POOL`, `UNKNOWN` |
| **Funder** · `check_wallet_forensics` · `GET /check/funder/{address}` | never on its own — context for the wallet decision | `CEX_FUNDED`, `WALLET_FUNDED` — informational (`WALLET_FUNDED` = possible cluster link) | flag `fresh_wallet` → do not copy; `UNKNOWN_ORIGIN`, `UNVERIFIABLE_ORIGIN`, `UNKNOWN` → no conclusion, never treat as clean |

## Order for a copy trade

1. **Wallet** before copying anyone. Abort → stop here.
2. **Token** before buying the mint. Abort → skip this trade.
3. **Trade** for your size. `HIGH_COST` → retry with a smaller size, never force it.

All three must pass. A failed call, a timeout, or **HTTP 402 / `PaymentRequired` is not a verdict → no trade.**

## Rules

- `UNKNOWN` and `UNVERIFIABLE` mean "we could not tell". Say so. Do not invent an edge.
- Never use leaderboard PnL or peak-gain screenshots as proof.
- Before acting, quote the verdict and the first reason code (response header `X-Verdict` and `X-Reason`).
- Verdicts are computed on a recent window, not a lifetime. Re-check before each copy.
