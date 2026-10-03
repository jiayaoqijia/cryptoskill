---
name: gdex-token-risk
description: GDEX token screen on 12 chains: price, liquidity, volume plus honeypot, taxes, LP lock, holder concentration. Deterministic NDJSON; missing security data never means safe.
---

# GDEX: Token Risk Screen

The GDEX trending board for each chain, with market context and GDEX's back-end security
assessment. One JSON object per token.

## Run it

```bash
python3 scripts/token_risk.py                    # every supported chain
python3 scripts/token_risk.py --chain-id 1 8453  # GDEX chain ids
python3 scripts/token_risk.py --list-chains
```

Standard library only. Non-zero exit means a read failed.

## Rules for agents

1. **Report numbers exactly as the script prints them.** Never estimate or compute new figures.
2. **Absent is unknown, never safe.** Security fields are omitted when GDEX has no value — on a
   typical run `is_honeypot` is present for only about a quarter of tokens. A token with no
   `is_honeypot` field has *not been checked*; say so rather than calling it clean.
3. The board carries junk and scam tokens by design (it ranks trending, not quality). Treat
   market figures as observations — a token can show a huge market cap on trivial liquidity.

## Fields

Security (percent fields are 0–100): `is_honeypot`, `buy_tax_pct`, `sell_tax_pct`,
`lp_lock_pct`, `top_holders_pct`, `is_contract_verified`, and — on Solana — `can_mint`,
`can_freeze`. Market: `price_usd`, `market_cap_usd`, `liquidity_usd`, `volume_24h_usd`,
`change_1h_pct`, `change_24h_pct`. `upstream_updated_source` names which clock stamped the row;
`fetch_time_fallback` means GDEX had no timestamp, so the row's age is unknown.

Solana and Sui addresses are case-sensitive and kept exactly; Sui type tags (`0x…::mod::TYPE`)
appear with `::` replaced by `.` in `gemach_id` only.
