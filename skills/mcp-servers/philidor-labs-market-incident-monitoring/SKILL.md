---
name: market-incident-monitoring
description: >
  Use this when the user wants lending-market monitoring, a market overview,
  recent market events, protocol incident history, or which vaults had a
  critical incident. Cite only identifiers and figures the Philidor tools return.
---

# Market and incident monitoring

Three different calls cover “the market”. Do not swap them.

| Question | Tool |
| --- | --- |
| Platform-wide vault TVL, vault count, risk mix, TVL by protocol | `get_market_overview` (no arguments) |
| A list of lending markets (Aave spoke, Morpho Blue pair, Kamino K-Lend, and similar) | `list_markets` |
| One market’s reserves, rates, utilization, tiers | `get_market` with `marketId` |
| Events on one market (incidents, bad debt, liquidation cascades) | `get_market_events` with `marketId` |
| Vaults with a critical incident in the last 365 days | `list_vaults_with_incidents` (no arguments) |
| One protocol’s audits and security history | `get_protocol_info` with `protocolId` |

The hosted server is `https://mcp.philidor.io/api/mcp`. Quote market ids, vault ids, and counts from the tool result. Never invent an incident, a date, or a TVL.

## Lending markets

1. Call `list_markets` with the filters the user named. `protocol` is `aave`, `spark`, `compound`, `morpho`, or `kamino`. `version` is `v3`, `v4`, or `klend`. Aave V4 is `protocol=aave` and `version=v4` (`aave-v4` is an accepted alias). `chain` is an integer id or a slug. `sortBy` is `total_supplied_usd`, `total_borrowed_usd`, `reserve_count`, or `name`. `limit` is 1–100, default 20.
2. Pass a `marketId` from that response into `get_market`. Spoke ids look like `aave-v4-1-main`. Composed Aave V4 hub parents look like `aave-v4-1-hub-global-dollar`. If `get_market` does not serve a hub id, open a spoke id returned under that hub. Do not invent a spoke id.
3. Call `get_market_events` for “what happened on this market”. `limit` is 1–100, default 20. Hub ids union the spoke feeds. This is not `get_market_overview`.

## Vault incidents and protocols

4. `list_vaults_with_incidents` lists vaults with a critical incident in the last 365 days (severity Critical, or `incident_severity` major), sorted by TVL descending, then by recency. It has no filters. Say that window in the answer. It is not a full lifetime history and not “every warning”.
5. For a protocol the user named, call `get_protocol_info`. Live protocol ids include `aave`, `morpho`, `spark`, `compound`, `yearn`, `beefy`, `uniswap`, `nest`, `maple`, and `kamino`. Aave V4 is under `aave`. Use an id the user named only if it matches this set or an id a previous tool returned. Otherwise say the id is not in the tool’s protocol list and read `philidor://supported-protocols`.
6. For one vault’s own events, use `get_vault` (see the vault due diligence skill). Do not claim a vault is clean because it is missing from the 365-day critical list.

## Done when

- The answer names which tool produced each block.
- Every market id and vault id is copied from a result.
- Empty event lists are reported as empty results, not as “no risk”.
