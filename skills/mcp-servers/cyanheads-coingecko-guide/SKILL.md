---
name: coingecko-guide
description: Use coingecko_* tools to verify token identities by chain and contract, turn a named category into a market list, or compare paginated price histories. Check coverage before interpreting missing coins, quotes, or chart points.
license: Apache-2.0
metadata:
  author: "cyanheads"
  version: "1.0"
---

## Scope

Use this workflow for CoinGecko token comparisons, category research, and historical analysis. For a current quote or profile with a known coin ID, call the corresponding tool directly. Keep the CoinGecko attribution with reported data.

## Identifiers

- A coin `id` comes from `coingecko_search_coins` or an existing market row. Use it to join prices, profiles, and history.
- Use `coingecko_get_coin` platform details to check a candidate's network and contract. For an exact contract lookup, use the [CoinGecko asset platform catalog](https://docs.coingecko.com/reference/asset-platforms) to resolve the network name to a platform ID if needed. Pass the address with its original casing to `coingecko_search_coins`.
- A `categoryId` comes from `coingecko_list_categories`. A coin profile's category names are display labels. Resolve them in the category catalog before filtering markets.

## Gates

- Resolve ticker collisions before pulling prices or charts. Use the named network and exact contract when available. If several candidates still fit, ask which asset the user means before calculating a result.
- Before treating a price batch as complete, check `missing` and `skippedIds`. Re-resolve missing IDs and send skipped IDs in a separate batch. When a resolved asset lacks a numeric quote in the requested currency, report the quote as unavailable and keep its value unknown.
- Before declaring a category absent, check the category catalog. The aggregate ranking can omit valid categories, and its filters and pagination can also hide them.
- Before comparing chart series, check observed cadence and match observations by timestamp. A range's bounds use Unix seconds, and chart points use Unix milliseconds. Follow `nextPointOffset` with the same range and interval, and check for gaps or overlaps across pages because each page is a fresh upstream read.

## Workflows

- **Compare tokens.** Batch current quotes with `coingecko_get_prices`, or use `coingecko_list_markets` with the resolved IDs for ranked market rows. Check `notReturnedIds` when the market tool provides it. A full page or a later page leaves absence unresolved.
- **Compare categories and constituents.** Discover the category in catalog mode, or start in market-data mode for aggregate comparisons. Every normalized query token must match the start of a name word. If a name search is empty, try a distinctive word prefix. Pass the selected category ID to `coingecko_list_markets` to inspect members. Category aggregates are in USD, so use USD for member comparisons that depend on the same currency.
- **Compare history across assets.** Give `coingecko_get_market_chart` fixed bounds and the same quote currency for every asset. If upstream refuses the requested history window, report that coverage gap before using a shorter period.
