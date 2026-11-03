# Spectra REST API (fallback when the MCP server is not connected)

Base URL: `https://api.spectra.finance` · OpenAPI: `https://api.spectra.finance/api-docs` · No key required.

Network slugs: `mainnet, arbitrum, optimism, base, sonic, hemi, avalanche, bsc, katana, flare, hyperevm, monad, sei` (+ `stellar` via `/v1/stellar/...`).

| Need | Call |
| --- | --- |
| All PT markets on a network | `GET /v1/{network}/pools` |
| One market by pool | `GET /v1/{network}/pools/{pool}` |
| Implied APY history | `GET /v1/{network}/pools/{pool}/implied-apy` |
| Volume windows | `GET /v1/{network}/pools/{pool}/stats` |
| MetaVaults (all chains) | `GET /v2/metavaults` |
| Wallet positions (EVM, all chains) | `GET /v1/portfolio/{address}` |
| MetaVault positions | `GET /v2/metavaults/portfolio/{address}` |
| Stellar markets | `GET /v1/stellar/pools` |

## Reading `/v1/{network}/pools`

The response is an array of PTs (futures). Per PT: `symbol`, `maturity` (unix seconds), `underlying`, `ibt` (with `apr.total` = variable APY in percent), `tvl.usd`, `tags` (`stable`, `eth`, `stock`…) and `pools[]`. Per pool: `address`, `ptApy` (fixed APY, percent), `impliedApy`, `lpApy.total`, `liquidity.usd`, `ytLeverage`, `ptPrice.underlying`.

- APYs are percent. Treat values above ~200% or pools with under ~$10k liquidity as unreliable.
- Each pool carries `quality`: `{status: "ok" | "anomalous", reasons: [...]}` (`implausible_apy`, `pt_rate_impaired`, `ibt_depleted_pool`). Do not recommend anomalous pools; `GET /v1/{network}/pools?quality=ok` drops them (the `X-Spectra-Quality-Omitted` header counts them).
- Skip `tags` containing `stock` for persons in US, GB, CA, AU, SG.
- Check the `X-Spectra-Catalog-Status` header: `fresh`, `stale` or `partial`.

App link for a market: `https://app.spectra.finance/fixed-rate/{app-slug}:{pool}` where app-slug is the network slug except `mainnet→eth`, `arbitrum→arb`, `optimism→op`, `avalanche→avax`.

```bash
curl -s https://api.spectra.finance/v1/base/pools | jq '[.[] | {pt: .symbol, maturity: (.maturity|todate), fixed: .pools[0].ptApy, liquidity: .pools[0].liquidity.usd}]'
```
