# dYdX indexer API — documented gotchas (found by our watchdog)

Five non-obvious behaviors of indexer.dydx.trade that make naive
clients lie (each caught on live data and covered by gateway tests):

1. **Candles and historical-pnl arrive newest-first** (newest entries
   first). A consumer expecting chronology inverts the sign of
   ΔOI/Δprice and the TA trend. Our API layer normalizes this (sorting
   by startedAt). Example damage: a signal reading "OI shrank −8.9%"
   was in fact +9.7% growth.

2. **`netTransfers` in historical-pnl is a flow for the period between
   points, NOT cumulative.** A running sum is required. Without it, the
   deposit-adjusted drawdown of a reference market maker looks like
   79.5% instead of the real 11.9% (a 67 pp phantom gap).

3. **`priceChange24H` in perpetualMarkets does not match the actual 24h
   price change** (verified against ETH/BTC candles). Compute it
   yourself: close[-1]/close[-25] over 1H candles.

4. **The price subticks field is called `subticksPerTick`** (not
   subticksPerBase): price_subticks = price / tickSize × subticksPerTick.
   For ETH (tick 0.1, spt 100000) — price×10^6.

5. **There is no public liquidations feed** (several candidate paths
   return 404). Cascades are caught by a candle signature: |Δprice|↑
   together with OI↓ (2 stages: fresh_2h on 5-min candles,
   confirmed_6h on hourly).

Plus: **extreme funding on markets with OI < $100k is noise**
(example: CRO "+2967% annualized" at $4.5k OI). Always filter by OI.

Current version: reports/data-quality-2026-08.md in the gateway repo.
