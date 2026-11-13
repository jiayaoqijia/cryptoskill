---
name: survivorship-and-universe
domain: crypto-trading/survivorship-and-universe
trigger: "Point-in-time universe: the instruments and venues that existed THEN, not now; delisting and renaming; why survivorship bias kills cascade studies."
anti_trigger: "Not for the analysis itself, not for the trade record or risk budget."
scope: "Point-in-time universe: the instruments and venues that existed THEN, not now; delisting and renaming; why survivorship bias kills cascade studies."
status: seedling
---

# Survivorship and Universe

## Standard
Empirical studies of exchange liquidations, perpetual funding rates, and market crashes must evaluate the exact point-in-time universe of instruments that existed at each historical moment, rather than the surviving subset available today. Survivorship bias severely skews aggregate metrics by omitting assets that suffered catastrophic crashes, liquidations, or delistings. Collectors must record complete venue rosters continuously.

Primary sources for the claims in this step: <https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api> and <https://binance-docs.github.io/apidocs/futures/en/>.

## Decision rules
- **Point-in-time fidelity:** Every analytical query must reference the exact set of active trading pairs, margin tiers, and contract specifications valid at the specific historical timestamp in question.
- **Delisted asset retention:** Historical data for delisted tokens, liquidated contracts, and defunct trading pairs must remain permanently queryable in storage.
- **Symbol renaming tracking:** Instrument ticker changes and contract migrations (e.g., token swaps or ticker rebranding) must be mapped via immutable symbol version tables.
- **Venue boundary enforcement:** Universe definitions must explicitly bound scope to specific exchange venues (e.g., Binance Futures, Hyperliquid, Bybit) without cross-venue contamination.

## Procedure
1. Configure universe discovery collectors to query active exchange instrument metadata (`/fapi/v1/exchangeInfo` or equivalent) on a daily schedule.
2. Store daily instrument metadata snapshots in an append-only registry tracking listing dates, contract types, and base/quote assets.
3. Cross-reference historical market data queries against the instrument registry valid for the query timestamp.
4. Flag any active data stream whose underlying instrument was delisted or migrated during the study window.
5. Compile comprehensive inclusion and exclusion logs detailing every instrument considered in the empirical sample.
6. Verify that aggregate market statistics incorporate failing or delisted assets up to the exact moment of their cessation.

## Anti-patterns
- **Current-universe backtesting:** Applying today's active trading pair list retroactively across multi-year historical datasets, omitting failed assets.
- **Dropping delisted symbols:** Purging data directories of instruments that ceased trading to save storage space.
- **Ignoring contract specs:** Assuming contract multipliers, leverage caps, and tick sizes remained constant throughout an asset's trading history.
- **Implicit venue aggregation:** Blending spot and perpetual contract pricing or mixing liquidation statistics across disparate venue clearing houses without normalization.

## Done checklist
- [ ] Daily exchange instrument metadata snapshots are collected and stored immutably.
- [ ] Historical queries successfully resolve point-in-time instrument universes.
- [ ] Delisted and rebranded assets are fully retained in storage and analysis samples.
- [ ] Survivorship bias audits verify inclusion of failed assets prior to delisting dates.

## Sources
- Center for Research in Security Prices (CRSP). (2026). Survivorship bias principles and historical database standards. Retrieved from https://www.crsp.org/
- Binance API Documentation. (2026). Exchange information endpoints and symbol lifecycle management. Retrieved from https://binance-docs.github.io/apidocs/futures/en/
- Hyperliquid API Documentation. (2026). Asset metadata and perpetual contract specifications. Retrieved from https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api
- CoinMarketCap. (2026). Historical cryptocurrency listing and delisting tracking methodologies. Retrieved from https://coinmarketcap.com/api/
