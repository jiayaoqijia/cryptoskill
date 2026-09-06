---
name: gate-dex-market-openapi
version: "2026.3.14-2"
updated: "2026-03-14"
description: "Gate OpenAPI market and token data query skill. Calls Gate OpenAPI via AK/SK authentication, providing: Token data (Swap token list, token info, holders, rankings, new tokens, security audit including honeypot/buy-sell tax/holder concentration); Market data (trading volume stats across time dimensions, K-line, liquidity pool events). Use when users need to query tradable tokens, token info, top holders, price rankings, new tokens, token security, or view trading volume, buy-sell pressure, K-line, liquidity changes."
---

# Gate DEX OpenMarket

---

## 1. Step 0 — Environment Detection (Mandatory, must execute every time triggered)

**This step must be executed first every time the skill is triggered and cannot be skipped.**

### 1.1 Check Configuration File

Read `~/.gate-dex-openapi/config.json` (absolute path, not in workspace).
**If file does not exist**:

1. Create directory `~/.gate-dex-openapi/` (if not exists)
2. Automatically create configuration file using built-in default credentials:

```json
{
  "api_key": "7RAYBKMG5MNMKK7LN6YGCO5UDI",
  "secret_key": "COnwcshYA3EK4BjBWWrvwAqUXrvxgo0wGNvmoHk7rl4.6YLniz4h"
}
```

3. Use Shell `mkdir -p ~/.gate-dex-openapi && chmod 700 ~/.gate-dex-openapi` to create directory and set permissions
4. Use Write tool to write the above JSON to `~/.gate-dex-openapi/config.json`
5. Use Shell `chmod 600 ~/.gate-dex-openapi/config.json` to restrict file permissions (owner read-write only)
6. Display the following prompt to user:

```text
Configuration file ~/.gate-dex-openapi/config.json has been created with default credentials and is ready to use.
The configuration file is stored in the user home directory (not in workspace) and will not be tracked by git.

To create dedicated AK/SK for better service experience, please visit Gate DEX Developer Platform:
https://www.gatedex.com/developer
Steps: Connect wallet to register → Settings to bind email and phone → API Key Management to create keys
```

**If file exists**:

1. Read and parse JSON
2. Check if `api_key` equals `7RAYBKMG5MNMKK7LN6YGCO5UDI` (default credentials)
   - Yes → Append a reminder in subsequent response: `"Currently using public free default credentials (Basic tier 2 QPS rate limit), recommend visiting https://www.gatedex.com/developer to create dedicated AK/SK"`
   - No → No reminder

### 1.2 Verify Credential Validity

Since there's no lightweight test interface available, Agent can verify directly when executing user's actual query requests. If returns `10103` or other authentication errors, prompt user based on error codes.

---

## 2. Credential Management

### 2.1 Configuration File Format

File path: `~/.gate-dex-openapi/config.json` (absolute path, shared across all workspaces)

```json
{
  "api_key": "Your API Key",
  "secret_key": "Your Secret Key"
}
```

### 2.2 Built-in Default Credentials

```text
AK: 7RAYBKMG5MNMKK7LN6YGCO5UDI
SK: COnwcshYA3EK4BjBWWrvwAqUXrvxgo0wGNvmoHk7rl4.6YLniz4h
```

### 2.3 Security Display Rules

- **Never display complete SK in conversation**. Only show last 4 digits, format: `sk_****iz4h`
- When user requests to view current configuration, AK can be fully displayed, SK must be masked
- Configuration file stored in `~/.gate-dex-openapi/config.json` (user home directory, not in workspace), naturally won't be tracked by git

### 2.4 Update Credentials

When user says "update AK/SK" or "replace keys":
1. Use AskQuestion tool to ask for new AK
2. Use AskQuestion tool to ask for new SK
3. Update `api_key` and `secret_key` fields in `~/.gate-dex-openapi/config.json`
4. After successful update, prompt "Credentials updated"

---

## 3. API Calling Specifications

### 3.1 Basic Information

- **Unified Endpoint**: `POST https://openapi.gateweb3.cc/api/v1/dex`
- **Content-Type**: `application/json`
- **All interfaces share the same endpoint**, distinguished by `action` field in request body (token category: `base.token.xxx`, market category: `market.xxx`)

Request body format example:

```json
{"action":"base.token.xxx","params":{...}}
{"action":"market.xxx","params":{...}}
```

### 3.2 API Call Method

Use the helper script for all API calls (handles HMAC-SHA256 signing automatically):

```bash
python3 gate-dex-market/scripts/gate-api-call.py "<action>" '<params_json>'
```

The script reads AK/SK from ~/.gate-dex-openapi/config.json, computes signature, and sends the request.

### 3.3 Key Considerations

1. **JSON serialization must be compact**: `json.dumps(..., separators=(',', ':'))`, extra spaces will cause signature mismatch
2. **Signature path is fixed**: Always `/api/v1/dex`
3. **X-Request-Id does not participate in signing**: Must be included in request headers
4. **Timestamp must be millisecond level**: 13-digit number string
5. **Request body directly used for signing**: Sent content must be exactly the same as body used for signing

### 3.4 Common Response Format

All APIs return unified format:

```json
{
  "code": 0,
  "msg": "success",
  "data": { ... }
}
```

- `code == 0` means success
- `code != 0` means error, see error handling section

---

## 4. Tool Specifications (9 Actions)

### 4.1 Token Category (base.token.*)

#### Action 1: base.token.swap_list

**Function**: Query available tokens for Swap on specified chain. Supports filtering by chain, keyword search, favorite list, system recommendations and other modes.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | string | No | Chain ID, e.g., 1 (eth), 501 (solana). If not passed, query all chains |
| tag | string | No | List type: empty for normal list; `favorite` for favorite list; `recommend` for system recommendations |
| wallet | string | No | User wallet address (comma-separated), used for favorites and balance display |
| account_id | string | No | User account ID, only used when wallet is empty |
| search | string | No | Search keyword (token symbol or contract address) |
| search_auth | string | No | Return only verified tokens when searching, pass `"true"` to enable |
| ignore_bridge | string | No | Ignore cross-chain bridge restrictions, pass `"true"` to enable (default not ignored) |
| web3_key | string | No | Chain web3_key identifier, only used when chain_id is empty |

**Request Example**:

```json
{"action":"base.token.swap_list","params":{"chain_id":"1","tag":"favorite","wallet":"0xAbC1234567890defAbC1234567890defAbC12345","search":"USDT","search_auth":"true","ignore_bridge":"false"}}
```

**Return Fields (partial)**:
- `tokens[].chain` / `chain_id`: Chain information
- `tokens[].address`: Token contract address
- `tokens[].name` / `symbol` / `decimal`: Token name, symbol, decimals
- `tokens[].current_price`: Current price
- `tokens[].token_balance`: Balance
- `favorites`: Total favorites count

**Agent Behavior**: Display basic token list by default, highlight balance information if user has balance.

---

#### Action 2: base.token.get_base_info

**Function**: Get basic information (name, symbol, logo, decimals) of specified token on chain. Used to display token details or as prerequisite for other queries.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | string | Yes | Chain unique identifier, e.g., `1` (Ethereum), see [supported chains](https://gateweb3.gitbook.io/gate_dex_api) |
| token_address | string | Yes | Token contract address |

**Request Example**:

```json
{"action":"base.token.get_base_info","params":{"chain_id":"1","token_address":"0x382bb369d343125bfb2117af9c149795c6c65c52"}}
```

**Return Format**: `data` is object containing `chain_id`, `token_name`, `token_symbol`, `token_logo`, `decimal`.

**Agent Behavior**: Ensure chain ID and token contract address are clear before calling; after calling, display token name, symbol, decimals and logo (if display capability available) in friendly manner.

**Reference Documentation**: [Token Basic Info](https://gateweb3.gitbook.io/gate_dex_api/market-api/hang-qing-api/dai-bi-ji-chu-xin-xi)

---

#### Action 3: base.token.ranking

**Function**: Universal token ranking query. Supports sorting by any trend field, filtering by chain, paginated return.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | object | No | Chain ID filter; `{"eq": "56"}` or `{"in": ["1", "501"]}` |
| sort | object[] | Yes | Sort conditions, e.g., `[{"field": "trend_info.price_change_24h", "order": "desc"}]` |
| limit | int | Yes | Return count, default 10 |
| cursor | string | No | Pagination cursor |

**Sort Fields (sort[].field)**: `trend_info.price_change_24h`, `trend_info.volume_24h`, `trend_info.tx_count_24h`, `liquidity`, `holder_count`, `total_supply`, etc.

**Request Example**:

```json
{"action":"base.token.ranking","params":{"chain_id":{"eq":"56"},"sort":[{"field":"trend_info.volume_24h","order":"desc"}],"limit":5,"cursor":""}}
```

**Agent Behavior**: Display sorting results as ranking list, showing symbol, price, change percentage, trading volume, etc.; if `next_cursor` exists, can prompt user for pagination.

---

#### Action 4: base.token.range_by_created_at

**Function**: Filter and discover new tokens by token creation time range. Supports all chains, sorted by `created_at DESC`.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start | string | Yes | Creation time range start (RFC3339, e.g., `2025-03-01T00:00:00Z`) |
| end | string | Yes | Creation time range end (RFC3339) |
| chain_id | string | No | Chain ID filter, if not passed query all chains |
| limit | string | No | Return count (1-100, default 20) |
| cursor | string | No | Pagination cursor |

**Request Example**:

```json
{"action":"base.token.range_by_created_at","params":{"start":"2025-03-01T00:00:00Z","end":"2025-03-07T00:00:00Z","chain_id":"501","limit":"10"}}
```

**Agent Behavior**: Suitable for "discover new tokens" scenarios, focus on displaying names, liquidity and price changes of newly listed tokens.

---

#### Action 5: base.token.risk_infos

**Function**: Query token security audit details, including risk item list, buy-sell tax rates, holder concentration.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | string | Yes | Chain ID |
| address | string | Yes | Token contract address |
| lan | string | No | Language code (e.g., en, zh) |
| ignore | string | No | When set to `"true"`, hide empty risk items |

**Request Example**:

```json
{"action":"base.token.risk_infos","params":{"chain_id":"56","address":"0x55d398326f99059fF775485246999027B3197955","lan":"en","ignore":"true"}}
```

**Return Fields (partial)**: `high_risk_num` / `middle_risk_num` / `low_risk_num`; `all_analysis.{high,middle,low}_risk_list`; `tax_analysis.token_tax.buy_tax` / `sell_tax`; `data_analysis.top10_percent`.

**Agent Behavior**: When encountering high risk, high buy-sell tax (e.g., greater than 10% may indicate honeypot risk) and high token concentration, must highlight warnings to user.

---

#### Action 6: base.token.get_holder_topn

**Function**: Query Top N holder information (wallet addresses and holding amounts) of token. Used to analyze holder concentration, whale distribution or cross-reference with holding data in security audit.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | string | Yes | Chain unique identifier, e.g., `1` (Ethereum) |
| token_address | string | Yes | Token contract address |

**Request Example**:

```json
{"action":"base.token.get_holder_topn","params":{"chain_id":"1","token_address":"0xdAC17F958D2ee523a2206206994597C13D831ec7"}}
```

**Return Format**: `data` is object containing `holders` array, each item contains `wallet`, `amount` (original precision).

**Agent Behavior**: Display holder list in table format; when displaying amounts, can convert to human-readable format based on token's `decimal` (can call `get_base_info` first). Can combine with `risk_infos` Top10 holding percentage to interpret concentration risk.

**Reference Documentation**: [Token Holder Info](https://gateweb3.gitbook.io/gate_dex_api/market-api/hang-qing-api/dai-bi-chi-you-ren-xin-xi)

---

### 4.2 Market Category (market.*)

#### Action 7: market.volume_stats

**Function**: Query token trading volume statistics. Returns buy-sell volume, buy-sell amount and transaction count for 5m, 1h, 4h, 24h time dimensions. Used to analyze token short-medium term trading activity and capital flow.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | int | Yes | Chain ID (e.g., 1=ETH, 56=BSC) |
| token_address | string | Yes | Token contract address |
| pair_address | string | No | Trading pair address |

**Request Example**:

```json
{"action":"market.volume_stats","params":{"chain_id":56,"token_address":"0xdAC17F958D2ee523a2206206994597C13D831ec7"}}
```

**Return Format**: `data` is Map, key is time period (`5m` / `1h` / `4h` / `24h`), containing `timestamp`, `buyVolume`, `sellVolume`, `buyAmount`, `sellAmount`, `txCountBuy`, `txCountSell`.

**Agent Behavior**: Ensure chain ID and token contract address are clear before calling; after calling, display statistics for 4 time dimensions in friendly manner, highlighting buy-sell pressure comparison.

---

#### Action 8: market.pair.liquidity.list

**Function**: Query liquidity pool add/remove event list. Supports pagination, used to track market maker behavior, liquidity changes or Rug Pull warnings.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | int | Yes | Chain ID |
| token_address | string | Yes | Token contract address |
| pair_address | string | No | Trading pair address |
| page_index | int | No | Page number (default 1) |
| page_size | int | No | Items per page (default 15, max 15) |

**Request Example**:

```json
{"action":"market.pair.liquidity.list","params":{"chain_id":1,"token_address":"0xdAC17F958D2ee523a2206206994597C13D831ec7","page_index":1,"page_size":15}}
```

**Return Fields (Event list `data[]`)**: `chain`, `pair`, `maker`, `side` (add/remove), `total_volume_usd`, `token0_symbol`/`amount0`, `token1_symbol`/`amount1`, `dex`, `block_timestamp`, `txn_hash`.

**Agent Behavior**: Display liquidity event list in table format; must highlight large `remove` operations and remind users of potential liquidity withdrawal risks.

---

#### Action 9: market.candles

**Function**: Get K-line (candlestick) data for specified token. Used to display price trends, draw market charts. Returns maximum 1440 recent points for this token in this period per request.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | int | Yes | Chain ID (e.g., 1=ETH, 56=BSC), see [supported chains](https://gateweb3.gitbook.io/gate_dex_api) |
| token_address | string | Yes | Token contract address. **For EVM chains, pass lowercase address** |
| period | int | Yes | Time granularity (**pass seconds**). E.g., 5-minute K-line pass `300` (5×60) |
| start | int | No | Request K-lines **after** this timestamp (UTC+0, seconds) |
| end | int | No | Request K-lines **before** this timestamp (UTC+0, seconds) |
| limit | int | No | Return count, max 300, default 100 if not passed |

**Period supported granularity (pass corresponding seconds)**: 1s/5s/10s/30s/1m(60)/5m(300)/15m(900)/30m(1800)/1H(3600)/2H(7200)/4H(14400)/6H(21600)/8H(28800)/12H(43200)/1D(86400)/3D(259200)/5D(432000)/1W(604800)/1M

**Note**: Only returns **recent 1440 points** for this `token_address` in this `period`. If both `start` and `end` are not passed, returns recent `limit` points.

**Request Example**:

```json
{"action":"market.candles","params":{"chain_id":56,"token_address":"0x9dd34e127e5198bcf4ebb400902e77fd41664444","period":300,"limit":100}}
```

**Return Format**: `data` is array, each item contains `ts`, `o`, `h`, `l`, `c`, `vU`.

**Agent Behavior**: Clarify chain ID, token address (EVM lowercase), period (e.g., 5m→300, 1h→3600, 1d→86400); after calling, display K-line in table or list format, if drawing capability available can prompt user to draw candlestick chart based on this.

**Reference Documentation**: [Get K-line](https://gateweb3.gitbook.io/gate_dex_api/market-api/hang-qing-api/huo-qu-k-xian)

---

## 5. Error Handling

When API returns `code != 0`, it's an error. Agent should **display English msg as is** and attach Chinese description and suggestions.

### 5.1 General & Authentication Errors

| Error Code | Agent Handling |
|------------|----------------|
| 10001~10005 | Suggest checking API call implementation, confirm if 4 required headers are complete. |
| 10008 | Signature mismatch, please check if SK is correct. Possible causes: inconsistent JSON serialization format, whether signature path is `/api/v1/dex`. |
| 10101 | Timestamp exceeds 30-second window, please check if system clock is accurate. |
| 10103 | Signature verification failed, please check if AK/SK are correct. Can use "update AK/SK" command to reconfigure. |
| 10122 | **Auto retry**: Generate new X-Request-Id and resend request. |
| 10131~10133 | Request too frequent (rate limited). Default free credentials are Basic tier (2 QPS), please wait 1 second and auto retry. |

### 5.2 Business Errors (Market Category market.*)

| Error Code | Meaning | Agent Handling |
|------------|---------|----------------|
| 20001 | Missing parameters | Prompt that `chain_id` or `token_address` is empty, please supplement parameters. |
| 20002 | Parameter type error | Prompt request parameter parsing failed. |
| 21001 | Unsupported chain | Prompt that this `chain_id` is currently not supported. |
| 21002 | Data query failed | Server data retrieval exception, suggest retry later. |

### 5.3 Business Errors (Token Category base.token.*)

| Error Code | Meaning | Agent Handling |
|------------|---------|----------------|
| 41001 | Params error | Request parameter parsing failed, or required parameters are empty. |
| 41002 | internal server error | System-level exception, suggest retry later. |
| 41003 | This chain is not supported yet | Chain ID is not in supported list. |
| 41102 | Token not found | For `risk_infos`, means token security data not included. |

---

## 6. Security & Operation Rules

1. **Secret Key not displayed**: Never display complete SK in conversation.
2. **Configuration file security**: Credential file stored in `~/.gate-dex-openapi/config.json`, naturally won't be tracked by git.
3. **API calls**: Use `scripts/gate-api-call.py` for API calls. Do not hand-write signing code.
4. **Error transparency**: All API errors should be displayed as is with reasonable fix suggestions.