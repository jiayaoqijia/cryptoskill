---
name: macro-data-query
description: Answer questions about macro and market indicators (liquidity, inflation, yield curve, VIX, crypto dominance, stablecoin supply, gold) from the local, health-checked SQLite dataset built by this repo. Use when asked for the latest value of an indicator, what was known on a past date, how an indicator has moved, or which regime inputs are available. Always runs the health check first and only reports point-in-time values.
---

# Macro data query

You are answering from a documented dataset, not from memory and not from live web
calls. The dataset is a SQLite file built by this repo's pipeline. Its contract is in
`docs/three-clocks.md` (time semantics) and `docs/data-sources.md` (series, units,
caveats).

Paths below are relative to the repo root. The database defaults to `data/macro.db`;
use `data/sample.db` if that is what exists (it is SYNTHETIC, so say so in the answer).

## Step 1: check health before answering

```bash
python pipeline/check_health.py --db-path data/macro.db --json
```

- If `all_checks_passed` is `true`, continue.
- If any check fails, do not present numbers as reliable. Report which check failed
  and the failing rows (they are in the JSON), then answer only for series not named in
  the failing rows, and say that you did so.
- `not_stale` failures mean the data is old. Give the value with its date and say it is
  stale. Do not refresh data yourself unless the user asks; if they do, run
  `python pipeline/run_pipeline.py` (needs network; FRED needs `FRED_API_KEY`).

## Step 2: map the question to series

The catalog is `config/series_catalog.yaml`. Indicator codes map to series:

- Liquidity: L1 M2, L2 Fed net liquidity (WALCL - WTREGEN - RRPONTSYD, all in
  millions USD), L3 dollar index, L4 HY spreads, L5 Fed funds
- Inflation: I1 CPI, I2 10Y real yield, I3 copper / copper-gold, I4 oil
- Transition: T1 10Y-2Y curve, T2 ISM PMI, T3 VIX
- Crypto: C1 BTC dominance, C2 stablecoin supply (USDT + USDC)
- Precious metals: P1 gold/silver ratio, P2 central-bank gold purchases

## Step 3: query point-in-time only

```bash
# What is known today (or on any past date)
python pipeline/query_as_of.py --as-of YYYY-MM-DD --indicator L2 --json

# One or more series, with the last N known values
python pipeline/query_as_of.py --as-of YYYY-MM-DD --series FRED:CPIAUCSL --history 4 --json
```

Rules:

- Never query `raw_observations` without `available_at <= as_of`. If you write your
  own SQL, start from `sql/point_in_time.sql`.
- "Latest" means latest *available* as of today, not the latest `observation_date`.
- For a question about a past date ("what did we know on 2025-03-15?"), set `--as-of`
  to that date. Do not use later data to describe it.

## Step 4: answer with provenance

For every number, give:

- the value and units (from the catalog),
- `series_id`, `observation_date` (period it describes) and `available_at` (when it
  became known),
- a caveat when `coverage_status` is `proxy`,
- "SYNTHETIC sample data" when the database is `data/sample.db`.

Do not make investment recommendations. This dataset is research tooling.

## Example

User: "What's the latest CPI print and when did it come out?"

1. `check_health.py` -> `all_checks_passed: true`
2. `query_as_of.py --as-of <today> --series FRED:CPIAUCSL --history 2 --json`
3. Answer: "CPI (CPIAUCSL, index) for August 2025 is 323.4, available from
   2025-09-14 under the catalog's 14-day release lag. The previous print (July) was
   322.1." (Values illustrative.)
