# Market Data Source and Provider Behavior Must Be Consistent Across Paths

A preferred market data source or provider applies to every fetch path (stream, market detail, order form, charts, fallback) through a typed, visible selection with tested fallback.

- **Preferred source wired only to stream path** — detail/order/chart fetches still use old/default source.
- **Source choice hidden in unchanged params** — make source/provider selection typed and visible.
- **Fallback path lacks evidence** — source/provider fallback should be tested and documented.
