# Gate DEX OpenMarket

Gate OpenAPI market and token data query skill (Cursor Agent Skill). Uses AK/SK authentication to call Gate DEX OpenAPI, providing token-dimension and market quote-dimension read-only queries, **no trading execution**.

## Feature Overview

| Category | Capabilities | Typical Scenarios |
|------|------|----------|
| **Token** | Swap token list, basic info, holders, rankings, new token discovery, security audit | Query tradeable tokens, token name/precision, whale holders, gainers/losers, newly listed, honeypot/buy-sell tax/holding concentration |
| **Market** | Volume stats, K-line, liquidity pool events | Buy/sell volume/pressure, K-line/candlestick, add/remove liquidity, market maker movements, Rug Pull alerts |

## Trigger Methods

Trigger this Skill in Cursor when user conversation shows the following intents:

- **Direct**: `OpenAPI`, `AK/SK`, `market API`, `token API`, `gate-dex-openmarket`
- **Token**: tradeable tokens, token basic info, holders, whale holdings, token rankings, new tokens, token security, honeypot, buy/sell tax
- **Market**: trading volume, buy/sell pressure, K-line, liquidity events, market maker behavior, add liquidity, remove liquidity

## Environment & Configuration

- **Config file**: `~/.gate-dex-openapi/config.json` (shared with Gate DEX Trade Skill)
- **Required fields**: `api_key`, `secret_key`
- **First use**: If file doesn't exist, Skill will auto-create config with built-in default credentials and prompt user; recommend visiting [Gate DEX Developer Platform](https://www.gatedex.com/developer) to create dedicated AK/SK for better rate limiting and experience.

## API Summary

- **Endpoint**: `POST https://openapi.gateweb3.cc/api/v1/dex`
- **Authentication**: HMAC-SHA256 signature (see Chapter 4 in `SKILL.md`)
- **Action count**: 9 (6 token-type `base.token.*` + 3 market-type `market.*`)

### Token Type (base.token.*)

| Action | Description |
|--------|------|
| `base.token.swap_list` | Swap token list for specified chain (supports search, favorites, recommendations) |
| `base.token.get_base_info` | Token name, symbol, LOGO, precision |
| `base.token.ranking` | Token rankings (sorted by gains/losses/volume etc.) |
| `base.token.range_by_created_at` | Discover new tokens by creation time |
| `base.token.risk_infos` | Security audit: risk items, buy/sell tax, holding concentration |
| `base.token.get_holder_topn` | Top N holders (wallets and holding amounts) |

### Market Type (market.*)

| Action | Description |
|--------|------|
| `market.volume_stats` | 5m/1h/4h/24h buy/sell volume, buy/sell amount, transaction count |
| `market.pair.liquidity.list` | Liquidity add/remove events (paginated) |
| `market.candles` | K-line data (multiple periods, max 1440 points per request) |

## Documentation & Specifications

- **Complete specification**: See [SKILL.md](./SKILL.md) in this directory, includes trigger scenarios, Step 0 environment detection, credential management, signature algorithm, each Action request/response and error codes, security rules.
- **Official API docs**: [Gate DEX API](https://gateweb3.gitbook.io/gate_dex_api)

## Version

Current release mainline: **2.0**. See [CHANGELOG.md](./CHANGELOG.md) for detailed release history.

## Related

- **Trade execution**: Swap quotes, authorization, building, signing, submission, status queries provided by [gate-dex-opentrade](../gate-dex-opentrade/); this Skill only handles market and token data queries.
- **Credentials**: Shares `~/.gate-dex-openapi/config.json` with Trade Skill, same AK/SK can be used for both market queries and trading capabilities.