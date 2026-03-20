---
name: bitfinex-lending-monitor
description: Monitor Bitfinex lending (funding) performance via API. Use when the user asks to check Bitfinex funding收益/借贷利息, automate daily收益统计, or avoid opening the Bitfinex app for lending status.
---

# Bitfinex Lending Monitor

Use this skill to fetch and summarize Bitfinex funding收益 from API.

## What to collect

- Funding wallet balances from `v2/auth/r/wallets`
- Active funding credits from `v2/auth/r/funding/credits/{Symbol}`
- Ledger entries from `v2/auth/r/ledgers/{Currency}/hist` filtered by `wallet=funding`

## Run

1. Export API credentials:

```bash
export BITFINEX_API_KEY="your_api_key"
export BITFINEX_API_SECRET="your_api_secret"
```

2. Run summary:

```bash
python3 skills/bitfinex-lending-monitor/scripts/check_lending.py --currency USD --days 7
```

3. Optional JSON output:

```bash
python3 skills/bitfinex-lending-monitor/scripts/check_lending.py --currency USD --days 7 --json
```

## Notes

- Prefer read-only API permissions for safety.
- Timestamps are milliseconds since epoch.
- If no `--currency` is passed, script defaults to `USD` and symbol `fUSD`.
