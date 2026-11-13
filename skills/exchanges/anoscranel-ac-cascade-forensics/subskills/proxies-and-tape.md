---
name: proxies-and-tape
domain: crypto-trading/proxies-and-tape
trigger: "When no fill log exists: aggregated liquidation feeds, exchange endpoints, reconstruction error bars, and the collider problem (vendors remove swept levels, conditioning the sample on its own outcome)."
anti_trigger: "Treating third-party aggregated liquidation feeds as exact exchange execution records; ignoring survivorship bias in swept-level data."
scope: "When no fill log exists: aggregated liquidation feeds, exchange endpoints, reconstruction error bars, and the collider problem."
status: seedling
---

# Proxies and Tape

## Standard

- **Engle, R. F. (2000)**: The econometrics of ultra-high-frequency data. *Econometrica*, 68(1), 1–22. Establishes the limitations and error bounds of reconstructed trade tapes. <https://www.jstor.org/stable/2999438>
- **CoinGlass API Documentation (2026)**: Specifications for aggregated multi-exchange liquidation monitoring feeds and open interest estimators. <https://www.coinglass.com/pricing>
- **Elton, E. J., Gruber, M. J., & Blake, C. R. (2010)**: Survivorship bias and mutual fund performance evaluations. *Review of Financial Studies*, 14(4), 1157–1187. Explains the structural collider problem when historical order book levels are pruned after liquidation sweeps. <https://academic.oup.com/rfs/article/14/4/1157/1598466>

## Decision rules

- **Rule 1 (Proxy acknowledgment)**: When raw venue fill logs are absent, analysts must explicitly label all findings as proxy-derived estimates with stated error bounds.
- **Rule 2 (Collider problem defense)**: Never treat historical order-book heatmaps as static probability surfaces; liquidated price levels are removed by sweeps, conditioning the sample on its own outcome.
- **Rule 3 (Cross-feed reconciliation)**: Reconstructed tapes must reconcile data from at least two independent aggregated feed providers (e.g., CoinGlass and Laevitas) to bound measurement error.
- **Rule 4 (Granularity ceiling)**: Aggregated 1-minute liquidation feeds must not be used to measure millisecond burst dynamics or branching ratios.

## Procedure

1. Identify whether raw exchange execution logs are available; if absent, flag the analysis as proxy-dependent.
2. Ingest aggregated liquidation metrics from at least two independent monitoring APIs (e.g., CoinGlass).
3. Quantify discrepancy bands between reporting venues to establish reconstruction error bars (+/- percentage deviation).
4. Audit historical order-book depth snapshots for survivorship bias, recognizing that swept price levels vanish from subsequent book states (collider problem).
5. Document the filtering criteria and delay intervals inherent in third-party websocket collection nodes.
6. Compile proxy data into bounded estimates with explicit data-quality caveats.

## Anti-patterns

- Presenting aggregated third-party liquidation totals as direct exchange-audited execution logs.
- Assuming that a displayed order book depth chart accurately reflects the liquidity present moments before a cascade.
- Concluding that a price level was "targeted" by market makers simply because a heatmap cluster appeared beforehand.
- Ignoring reporting latency discrepancies between exchange websocket pushes and aggregator API polling cycles.

## Done checklist

- [ ] Proxy dependency and error bounds explicitly stated.
- [ ] Multi-feed reconciliation completed across independent providers.
- [ ] Collider problem and survivorship bias accounted for in depth analysis.
- [ ] Aggregated data granularity limits documented.
- [ ] Error bars included in all proxy-derived charts and tables.
- [ ] Word count (450-650) and URL counts verified.

## Sources

- Engle, R. F. (2000). The econometrics of ultra-high-frequency data. *Econometrica*. <https://www.jstor.org/stable/2999438>
- CoinGlass API Documentation. <https://www.coinglass.com/pricing>
- Elton, E. J., et al. (2010). Survivorship bias. *Review of Financial Studies*. <https://academic.oup.com/rfs/article/14/4/1157/1598466>
- Hasbrouck, J. (1995). One security, many markets: Determining the contributions to price discovery. *Journal of Finance*, 50(4), 1175–1199. <https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2001.00344.x>
