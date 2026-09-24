# Source Access Matrix (for JPG Template)

Based on the table in the JPG and current validation state.

## Market structure

- CoinMarketCap: partially available on current plan
  - Available now: global latest, listings, quotes, categories
  - Paid needed for your missing part: global historical and some market-pairs/history endpoints
- CoinGecko Demo: available for global snapshot, categories, top markets, trending
  - Paid needed for your missing part: `global/market_cap_chart` (Pro)

## Derivatives

- Deribit: public endpoints available (no API key needed for public market data)
- Coinglass: API key required; production use is paid-tier oriented

## On-chain funds

- Glassnode: API key required, free tier exists with limited metrics/history
- Nansen: paid-oriented API access

## Sentiment

- Alternative.me Fear & Greed: free/no-key API
- Santiment: key-based API, paid-plan oriented for full metric usage

## Narrative hot sectors

- CoinGecko Categories: available with Demo/public base

## Environment variable map

- `CMC_API_KEY`
- `COINGECKO_API_KEY`
- `COINGLASS_API_KEY`
- `GLASSNODE_API_KEY`
- `NANSEN_API_KEY`
- `NANSEN_BASE_URL`
- `SANTIMENT_API_KEY`
- `ALTERNATIVE_ME_BASE_URL` (optional override)
