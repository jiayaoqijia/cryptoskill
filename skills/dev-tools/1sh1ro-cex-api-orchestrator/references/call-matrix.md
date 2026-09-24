# API Call Matrix

## Capability-first calls

- CoinGecko Pro check: `GET https://pro-api.coingecko.com/api/v3/key`
- CoinGecko Demo check: `GET https://api.coingecko.com/api/v3/global`
- CMC plan check: `GET https://pro-api.coinmarketcap.com/v1/key/info`
- Deribit health check: JSON-RPC `public/ticker`
- Coinglass check: endpoint probe with `CG-API-KEY`
- Glassnode check: `/v1/metrics/*` probe with `api_key`
- Nansen check: endpoint probe with `NANSEN_API_KEY`
- Santiment check: GraphQL probe with `SANTIMENT_API_KEY`
- Alternative.me check: `GET https://api.alternative.me/fng/`

## Metric routing

- Global market cap snapshot:
  - Primary: CMC `/global-metrics/quotes/latest`
  - Secondary: CoinGecko `/global`
- Global market cap history:
  - Primary: CoinGecko Pro `/global/market_cap_chart`
  - Fallback: per-coin proxy from `/coins/{id}/market_chart`
- BTC dominance:
  - Primary: CMC global latest field `btc_dominance`
  - Secondary: CoinGecko global field `market_cap_percentage.btc`
- Top narratives:
  - Primary: CoinGecko `/coins/categories`
  - Secondary: CoinGecko `/search/trending`
- Derivatives pulse:
  - Primary: Deribit `public/get_volatility_index_data`
  - Primary: Deribit `public/ticker`
  - Optional paid extension: Coinglass OI/funding/liquidations
- On-chain funds:
  - Primary paid: Glassnode exchange/supply metrics
  - Secondary paid: Nansen wallet/flow analytics
- Sentiment:
  - Primary free: Alternative.me `/fng/`
  - Secondary paid: Santiment GraphQL metrics

## Normalized output keys

- `market.total_market_cap`
- `market.total_volume_24h`
- `market.btc_dominance`
- `derivatives.btc_perp_funding`
- `derivatives.eth_perp_funding`
- `derivatives.dvol_btc`
- `derivatives.dvol_eth`
- `narratives.categories_top10`
- `narratives.trending`
- `derivatives.coinglass_open_interest`
- `derivatives.coinglass_funding_rate`
- `derivatives.coinglass_liquidations_24h`
- `onchain.glassnode_exchange_netflow`
- `onchain.glassnode_stablecoin_supply`
- `onchain.nansen_smart_money_flow`
- `sentiment.fear_greed_index`
- `sentiment.santiment_social_dominance`
