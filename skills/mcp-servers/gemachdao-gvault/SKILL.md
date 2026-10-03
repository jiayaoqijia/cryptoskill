---
name: gvault
description: GVault (GMACL, Gemach's Enzyme vault on Ethereum) — NAV, share price, holdings and return both cumulative and annualised, read from Enzyme's own accounting by a deterministic script.
---

# GVault

Read-only state of GVault (ticker GMACL, "Gemach LP"), an Enzyme vault on Ethereum
denominated in USDC.

## Run it

```bash
python3 scripts/gvault.py      # one JSON object on stdout
```

Standard library only. Every value is read at one Ethereum block (`observed_block`).

## Rules for agents

1. **Report numbers exactly as the script prints them.**
2. **Always quote return with its horizon.** `all_time_return_pct` is cumulative since
   inception (2022-07-31); `annualised_return_pct` is the same over `age_years`. Quoting the
   cumulative figure alone invites it to be read as a one-year rate. Say both, or say the
   annualised one.
3. NAV comes from Enzyme's `calcGav()`, not from token balances — do not "check" it by summing
   balances; the vault holds stETH as well as USDC.

## Fields

`nav_usd`, `share_price_usd`, `shares_outstanding`, `tracked_assets`,
`all_time_return_pct`, `annualised_return_pct`, `age_years`, `inception_date`,
`denomination_symbol`, `observed_block`.
