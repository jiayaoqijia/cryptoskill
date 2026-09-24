# Metric Routing

## Core market metrics

- Total market cap trend -> Figure 1 skill (CMC global historical)
- Top asset monthly return -> Figure 2 skill (CoinGecko exact `market_chart/range`; universe is current market-cap snapshot and survivorship bias must be disclosed)
- DeFi share composition -> Figure 3 skill (DeFiLlama)
- NFT monthly volume -> Figure 4 skill (CryptoSlam web API; missing month fails, never writes zero)
- Outside top10 market-cap concentration -> Figure 6 skill (CMC + CoinGecko; not a standalone return-breadth proxy)

## Derivatives metrics

- Perp funding monthly history -> Deribit `public/get_funding_rate_history`
- Futures/options OI aggregate -> current snapshot only; include only within 48 hours of target month-end
- DVOL daily close trend -> Deribit monthly metrics skill

## Final synthesis

- Core narrative and appendix -> yuque monthly report script
- Orchestrator report -> integrates all outputs with benchmark-style sections
