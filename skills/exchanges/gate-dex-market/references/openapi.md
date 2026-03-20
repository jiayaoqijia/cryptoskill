---
name: gate-dex-openmarket
version: "2026.3.11-3"
updated: "2026-03-11"
description: |
  Gate OpenAPI market and token data query Skill. Calls Gate OpenAPI via AK/SK authentication, providing:
  - Token data: Swap token list, token basic info, holders, rankings, new token discovery, security audit (honeypot/buy-sell tax/holding concentration);
  - Market data: Volume statistics (multi-timeframe buy/sell volume/amount/tx count), candlestick (K-line), liquidity pool events (add/remove/market maker behavior).
  Use when users need to query tradable tokens, token info, top holders, gain/loss rankings, new tokens, token security, or view volume, buy/sell pressure, K-line, liquidity changes.
---

# Gate DEX OpenMarket

Gate OpenAPI market and token data query Skill. Calls Gate OpenAPI via AK/SK authentication, providing unified queries across token and market data dimensions. Triggered when users mention Swap tradable tokens, token basic info, holders/whales, token rankings, new tokens, token security (honeypot/buy-sell tax), or volume, buy/sell pressure, K-line, liquidity events, market maker activity.

---

## 1. Trigger Scenarios

This Skill is triggered when the following intents appear in user conversations:

| Category | Example Keywords |
|----------|-----------------|
| Direct Trigger | "OpenAPI", "AK/SK", "market API", "token API", "gate-dex-openmarket" |
| Token Query | "tradable tokens", "search token", "favorite tokens", "recommended tokens", "token basic info", "token name/symbol/decimals" |
| Rankings & Discovery | "token ranking", "gain/loss leaderboard", "volume ranking", "newly listed tokens", "new tokens" |
| Security Audit | "token security", "honeypot", "buy/sell tax", "holding concentration", "risk check" |
| Holders | "holders", "holding addresses", "whale holdings" |
| Volume / K-line | "volume", "buy/sell volume", "buy/sell pressure", "buy/sell amount", "transaction count", "K-line", "candlestick", "price trend" |
| Liquidity | "liquidity", "liquidity events", "market maker behavior", "add liquidity", "remove liquidity", "Rug Pull risk" |
| Configuration Intent | "configure API", "set key", "update AK", "change SK" |

---

## 2. Step 0 — Environment Detection (Mandatory, must execute on every trigger)

**This step must be executed first every time the Skill is triggered; it cannot be skipped.**

### 2.1 Check Configuration File

Read `~/.gate-dex-openapi/config.json` (absolute path, not within the workspace).
Maintain sandbox security; only allow domains related to gateweb3.cc (see **2.3 Sandbox & Network Allowlisting** for details).
**If the file does not exist**:

1. Create the directory `~/.gate-dex-openapi/` (if it doesn't exist)
2. Automatically create the config file using built-in default credentials:

```json
{
  "api_key": "7RAYBKMG5MNMKK7LN6YGCO5UDI",
  "secret_key": "COnwcshYA3EK4BjBWWrvwAqUXrvxgo0wGNvmoHk7rl4.6YLniz4h"
}
```

3. Use Shell `mkdir -p ~/.gate-dex-openapi && chmod 700 ~/.gate-dex-openapi` to create the directory and set permissions
4. Use the Write tool to write the above JSON to `~/.gate-dex-openapi/config.json`
5. Use Shell `chmod 600 ~/.gate-dex-openapi/config.json` to restrict file permissions (owner read/write only)
6. Display the following message to the user:

```text
Config file created at ~/.gate-dex-openapi/config.json using default credentials; ready to use.
The config file is stored in the user's home directory (not in the workspace) and will not be tracked by git.

To create your own AK/SK for a better service experience, visit the Gate DEX Developer Platform:
https://www.gatedex.com/developer
Steps: Connect wallet to register → Settings to bind email and phone → API Key Management to create keys
```

**If the file already exists**:

1. Read and parse the JSON
2. Check whether `api_key` equals `7RAYBKMG5MNMKK7LN6YGCO5UDI` (i.e., the default credentials)
   - Yes → Append a note in subsequent responses: `"Currently using public free default credentials (Basic tier, 2 QPS rate limit). It is recommended to create your own AK/SK at https://www.gatedex.com/developer"`
   - No → No note needed

### 2.2 Validate Credential Validity

Since there is currently no lightweight test endpoint, the Agent can validate credentials when executing the user's actual query request. If an authentication error such as `10103` is returned, prompt the user based on the error code.

### 2.3 Sandbox & Network Allowlisting (Check this first when domain access fails)

**Symptom**: `Tunnel connection failed: 403 Forbidden` or similar network unreachable errors when calling Gate OpenAPI.

**Cause**: The Cursor terminal sandbox uses an allowlist-only policy for outbound requests. Without a configured allowlist, requests to domains like `openapi.gateweb3.cc` are intercepted or proxied through a tunnel that returns 403, causing Gate API requests to fail.

**Solution**: While maintaining sandbox security, only allow Gate-related domains.

1. **Configure `sandbox.json`** (choose one):
   - **Current workspace**: Create or edit `.cursor/sandbox.json` in the project root directory
   - **All workspaces**: Create or edit `~/.cursor/sandbox.json` in the user's home directory

2. **Write the following content** (`default: "deny"` keeps the sandbox strict; only allows gateweb3.cc and its subdomains):

```json
{
  "networkPolicy": {
    "default": "deny",
    "allow": [
      "gateweb3.cc",
      "*.gateweb3.cc"
    ]
  }
}
```

3. **When making API requests**: Shell calls to Gate OpenAPI require requesting network permissions (e.g., set `required_permissions: ["network"]` in `run_terminal_cmd`), so the sandbox will allow access to `openapi.gateweb3.cc` etc. per the above allow list, while other domains remain blocked.

**Agent behavior**: If a user or log shows a Gate API request returning 403/network unreachable, first check whether `.cursor/sandbox.json` exists in the workspace or user directory and contains allowlist entries for `gateweb3.cc` / `*.gateweb3.cc`; if not, create or modify it per the steps above and prompt the user to retry the request.

---

## 3. Credential Management

### 3.1 Config File Format

File path: `~/.gate-dex-openapi/config.json` (absolute path, shared across all workspaces)

```json
{
  "api_key": "Your API Key",
  "secret_key": "Your Secret Key"
}
```

### 3.2 Built-in Default Credentials

```text
AK: 7RAYBKMG5MNMKK7LN6YGCO5UDI
SK: COnwcshYA3EK4BjBWWrvwAqUXrvxgo0wGNvmoHk7rl4.6YLniz4h
```

### 3.3 Security Display Rules

- **Never display the full SK in conversation.** Only show the last 4 characters, format: `sk_****iz4h`
- When users request to view the current configuration, AK may be shown in full; SK must be masked
- The config file is stored at `~/.gate-dex-openapi/config.json` (user's home directory, not in the workspace), so it is inherently not tracked by git

### 3.4 Updating Credentials

When the user says "update AK/SK" or "replace keys":
1. Use the AskQuestion tool to ask for the new AK
2. Use the AskQuestion tool to ask for the new SK
3. Update the `api_key` and `secret_key` fields in `~/.gate-dex-openapi/config.json`
4. After a successful update, confirm with "Credentials updated"

---

## 4. API Call Specifications

### 4.1 Basic Information

- **Unified endpoint**: `POST https://openapi.gateweb3.cc/api/v1/dex`
- **Content-Type**: `application/json`
- **All APIs share the same endpoint**; the `action` field in the request body differentiates between APIs (token-related: `base.token.xxx`, market-related: `market.xxx`)

Request body format example:

```json
{"action":"base.token.xxx","params":{...}}
{"action":"market.xxx","params":{...}}
```

### 4.2 HMAC-SHA256 Signature Algorithm

A signature must be computed for every API request. The algorithm is as follows:

**Step 1: Construct the prehash string**

```text
prehash = millisecond_timestamp + "/api/v1/dex" + raw_JSON_request_body
```

- Millisecond timestamp: 13-digit Unix millisecond timestamp, e.g., `1709812345678`
- The path is fixed as `/api/v1/dex` (regardless of the actual URL, the signing path is always this)
- The request body must be **compact JSON** (no extra whitespace); serialize with `separators=(',', ':')`

**Step 2: Compute HMAC-SHA256**

```text
signature = Base64Encode( HMAC-SHA256( key=SecretKey, message=prehash ) )
```

**Step 3: Set HTTP Headers**

| Header | Value | Description |
|--------|-------|-------------|
| Content-Type | `application/json` | Fixed value |
| X-API-Key | `api_key` from the config file | Identity identifier |
| X-Timestamp | The millisecond timestamp string used above | Must not deviate more than 30 seconds from the server |
| X-Signature | The Base64 signature computed above | Request integrity verification |
| X-Request-Id | Random UUIDv4 string | Idempotency key, unique per AK; not included in signature computation |

### 4.3 Signature Reference Implementation (Python pseudocode)

The following code shows the precise implementation of the signature algorithm for Agent reference. The Agent may implement equivalent logic in any language via a one-liner Shell command; **script files must not be created in the user's repository**.

```python
import hmac, hashlib, base64, time, json, uuid

ak = "api_key read from ~/.gate-dex-openapi/config.json"
sk = "secret_key read from ~/.gate-dex-openapi/config.json"

body = json.dumps({"action": "base.token.swap_list", "params": {"chain_id":"1"}}, separators=(',', ':'))

ts = str(int(time.time() * 1000))

prehash = ts + "/api/v1/dex" + body

signature = base64.b64encode(
    hmac.new(sk.encode('utf-8'), prehash.encode('utf-8'), hashlib.sha256).digest()
).decode('utf-8')

headers = {
    "Content-Type": "application/json",
    "X-API-Key": ak,
    "X-Timestamp": ts,
    "X-Signature": signature,
    "X-Request-Id": str(uuid.uuid4())
}
```

### 4.4 Key Notes

1. **JSON serialization must be compact**: `json.dumps(..., separators=(',', ':'))`; extra whitespace will cause signature mismatch
2. **Signing path is fixed**: Always `/api/v1/dex`
3. **X-Request-Id is not included in the signature**: It must be included in the request headers
4. **Timestamp must be millisecond-precision**: 13-digit numeric string
5. **The request body is used directly for signing**: The content sent must be exactly identical to the body used for signing

### 4.5 Common Response Format

All APIs return a unified format:

```json
{
  "code": 0,
  "msg": "success",
  "data": { ... }
}
```

- `code == 0` indicates success
- `code != 0` indicates an error; refer to the error handling section

---

## 5. Tool Specifications (9 Actions)

### 5.1 Token Category (base.token.*)

#### Action 1: base.token.swap_list

**Function**: Query the list of tokens available for Swap on a specified chain. Supports filtering by chain, keyword search, favorites list, system recommendations, and more.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | string | No | Chain ID, e.g., 1 (ETH), 501 (Solana). If omitted, queries all chains |
| tag | string | No | List type: empty for default list; `favorite` for favorites; `recommend` for system recommendations |
| wallet | string | No | User wallet address (comma-separated), used for favorites and balance display |
| account_id | string | No | User account ID, used only when wallet is empty |
| search | string | No | Search keyword (token symbol or contract address) |
| search_auth | string | No | Return only verified tokens when searching; pass `"true"` to enable |
| ignore_bridge | string | No | Ignore cross-chain bridge restrictions; pass `"true"` to enable (disabled by default) |
| web3_key | string | No | Chain web3_key identifier, used only when chain_id is empty |

**Request Example**:

```json
{"action":"base.token.swap_list","params":{"chain_id":"1","tag":"favorite","wallet":"0xAbC1234567890defAbC1234567890defAbC12345","search":"USDT","search_auth":"true","ignore_bridge":"false"}}
```

**Response Fields (partial)**:
- `tokens[].chain` / `chain_id`: Chain information
- `tokens[].address`: Token contract address
- `tokens[].name` / `symbol` / `decimal`: Token name, symbol, decimals
- `tokens[].current_price`: Current price
- `tokens[].token_balance`: Balance
- `favorites`: Total number of favorites

**Agent Behavior**: Display the basic token list by default; if the user has balances, highlight the balance information.

---

#### Action 2: base.token.get_base_info

**Function**: Retrieve basic information (name, symbol, logo, decimals) for a token on a specified chain. Used to display token details or as prerequisite information for other queries.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | string | Yes | Unique chain identifier, e.g., `1` (Ethereum); see [Supported Chains](https://gateweb3.gitbook.io/gate_dex_api) |
| token_address | string | Yes | Token contract address |

**Request Example**:

```json
{"action":"base.token.get_base_info","params":{"chain_id":"1","token_address":"0x382bb369d343125bfb2117af9c149795c6c65c52"}}
```

**Response Format**: `data` is an object containing `chain_id`, `token_name`, `token_symbol`, `token_logo`, `decimal`.

**Agent Behavior**: Ensure chain ID and token contract address are confirmed before calling; after calling, display the token name, symbol, decimals, and logo in a user-friendly format (if display capability exists).

**Reference Documentation**: [Token Basic Info](https://gateweb3.gitbook.io/gate_dex_api/market-api/hang-qing-api/dai-bi-ji-chu-xin-xi)

---

#### Action 3: base.token.ranking

**Function**: General-purpose token ranking query. Supports sorting by any trend field, filtering by chain, with paginated results.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | object | No | Chain ID filter; `{"eq": "56"}` or `{"in": ["1", "501"]}` |
| sort | object[] | Yes | Sort criteria, e.g., `[{"field": "trend_info.price_change_24h", "order": "desc"}]` |
| limit | int | Yes | Number of results to return, default 10 |
| cursor | string | No | Pagination cursor |

**Sort Fields (sort[].field)**: `trend_info.price_change_24h`, `trend_info.volume_24h`, `trend_info.tx_count_24h`, `liquidity`, `holder_count`, `total_supply`, etc.

**Request Example**:

```json
{"action":"base.token.ranking","params":{"chain_id":{"eq":"56"},"sort":[{"field":"trend_info.volume_24h","order":"desc"}],"limit":5,"cursor":""}}
```

**Agent Behavior**: Display sorted results as a ranked list showing symbol, price, price change, volume, etc.; if `next_cursor` exists, offer the user pagination.

---

#### Action 4: base.token.range_by_created_at

**Function**: Filter and discover new tokens by creation time range. Supports all chains, sorted by `created_at DESC`.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start | string | Yes | Creation time range start (RFC3339, e.g., `2025-03-01T00:00:00Z`) |
| end | string | Yes | Creation time range end (RFC3339) |
| chain_id | string | No | Chain ID filter; if omitted, queries all chains |
| limit | string | No | Number of results (1–100, default 20) |
| cursor | string | No | Pagination cursor |

**Request Example**:

```json
{"action":"base.token.range_by_created_at","params":{"start":"2025-03-01T00:00:00Z","end":"2025-03-07T00:00:00Z","chain_id":"501","limit":"10"}}
```

**Agent Behavior**: Ideal for "discover new tokens" scenarios; focus on displaying newly listed tokens' names, liquidity, and price changes.

---

#### Action 5: base.token.risk_infos

**Function**: Query detailed security audit information for a token, including risk item list, buy/sell tax rates, and holding concentration.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | string | Yes | Chain ID |
| address | string | Yes | Token contract address |
| lan | string | No | Language code (e.g., en, zh) |
| ignore | string | No | Set to `"true"` to hide empty risk items |

**Request Example**:

```json
{"action":"base.token.risk_infos","params":{"chain_id":"56","address":"0x55d398326f99059fF775485246999027B3197955","lan":"en","ignore":"true"}}
```

**Response Fields (partial)**: `high_risk_num` / `middle_risk_num` / `low_risk_num`; `all_analysis.{high,middle,low}_risk_list`; `tax_analysis.token_tax.buy_tax` / `sell_tax`; `data_analysis.top10_percent`.

**Agent Behavior**: When encountering high risk, high buy/sell tax (e.g., greater than 10% may indicate honeypot risk), or high token concentration, highlight warnings for the user.

---

#### Action 6: base.token.get_holder_topn

**Function**: Query the Top N holders of a token (wallet addresses and holding amounts). Used to analyze holding concentration, whale distribution, or cross-reference with holding data from security audits.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | string | Yes | Unique chain identifier, e.g., `1` (Ethereum) |
| token_address | string | Yes | Token contract address |

**Request Example**:

```json
{"action":"base.token.get_holder_topn","params":{"chain_id":"1","token_address":"0xdAC17F958D2ee523a2206206994597C13D831ec7"}}
```

**Response Format**: `data` is an object containing a `holders` array, where each item has `wallet` and `amount` (raw precision).

**Agent Behavior**: Display the holder list as a table; when showing amounts, convert to human-readable format based on the token's `decimal` (call `get_base_info` first if needed). Can be combined with `risk_infos` Top10 holding percentage to interpret concentration risk.

**Reference Documentation**: [Token Holder Info](https://gateweb3.gitbook.io/gate_dex_api/market-api/hang-qing-api/dai-bi-chi-you-ren-xin-xi)

---

### 5.2 Market Category (market.*)

#### Action 7: market.volume_stats

**Function**: Query volume statistics for a token. Returns buy/sell volume, buy/sell amount, and transaction count across four time dimensions: 5m, 1h, 4h, 24h. Used to analyze short-to-medium-term trading activity and capital flow for a token.

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

**Response Format**: `data` is a Map where keys are time periods (`5m` / `1h` / `4h` / `24h`), containing `timestamp`, `buyVolume`, `sellVolume`, `buyAmount`, `sellAmount`, `txCountBuy`, `txCountSell`.

**Agent Behavior**: Ensure chain ID and token contract address are confirmed before calling; after calling, display statistics across all 4 time dimensions in a user-friendly format, emphasizing buy/sell pressure comparison.

---

#### Action 8: market.pair.liquidity.list

**Function**: Query the list of add/remove events for a liquidity pool. Supports pagination; used for tracking market maker behavior, liquidity changes, or Rug Pull early warnings.

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

**Response Fields (Event list `data[]`)**: `chain`, `pair`, `maker`, `side` (add/remove), `total_volume_usd`, `token0_symbol`/`amount0`, `token1_symbol`/`amount1`, `dex`, `block_timestamp`, `txn_hash`.

**Agent Behavior**: Display the liquidity event list as a table; large `remove` operations must be highlighted, and the user should be warned about potential liquidity withdrawal risk.

---

#### Action 9: market.candles

**Function**: Retrieve candlestick (K-line) data for a specified token. Used to display price trends and draw market charts. Returns up to 1440 data points per query for the given token and period.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | int | Yes | Chain ID (e.g., 1=ETH, 56=BSC); see [Supported Chains](https://gateweb3.gitbook.io/gate_dex_api) |
| token_address | string | Yes | Token contract address. **For EVM chains, use all-lowercase addresses** |
| period | int | Yes | Time granularity (**in seconds**). E.g., for a 5-minute K-line, pass `300` (5×60) |
| start | int | No | Request K-line data **after** this timestamp (UTC+0, seconds) |
| end | int | No | Request K-line data **before** this timestamp (UTC+0, seconds) |
| limit | int | No | Number of results; max 300, default 100 if omitted |

**Supported period granularities (pass the corresponding seconds)**: 1s/5s/10s/30s/1m(60)/5m(300)/15m(900)/30m(1800)/1H(3600)/2H(7200)/4H(14400)/6H(21600)/8H(28800)/12H(43200)/1D(86400)/3D(259200)/5D(432000)/1W(604800)/1M

**Note**: Only the **most recent 1440 data points** for the given `token_address` and `period` are returned. If neither `start` nor `end` is provided, the most recent `limit` data points are returned.

**Request Example**:

```json
{"action":"market.candles","params":{"chain_id":56,"token_address":"0x9dd34e127e5198bcf4ebb400902e77fd41664444","period":300,"limit":100}}
```

**Response Format**: `data` is an array where each item contains `ts`, `o`, `h`, `l`, `c`, `vU`.

**Agent Behavior**: Confirm chain ID, token address (all lowercase for EVM), and period (e.g., 5m→300, 1h→3600, 1d→86400); after calling, display K-line data as a table or list; if charting capability exists, suggest the user can use this data to draw a candlestick chart.

**Reference Documentation**: [Get K-line](https://gateweb3.gitbook.io/gate_dex_api/market-api/hang-qing-api/huo-qu-k-xian)

---

## 6. Error Handling

When the API returns `code != 0`, it indicates an error. The Agent should **display the English msg as-is** and provide a description and suggestions.

### 6.1 Common & Authentication Errors

| Error Code | Agent Handling |
|------------|---------------|
| 10001~10005 | Suggest checking the API call implementation and verifying that all 4 required Headers are present. |
| 10008 | Signature mismatch; check whether the SK is correct. Possible causes: inconsistent JSON serialization format, or whether the signing path is `/api/v1/dex`. |
| 10101 | Timestamp exceeds the 30-second window; check whether the system clock is accurate. |
| 10103 | Signature verification failed; check whether the AK/SK are correct. Use the "update AK/SK" command to reconfigure. |
| 10122 | **Auto-retry**: Generate a new X-Request-Id and resend the request. |
| 10131~10133 | Request too frequent (rate limited). Default free credentials are Basic tier (2 QPS); wait 1 second then auto-retry. |

### 6.2 Business Errors (Market Category market.*)

| Error Code | Meaning | Agent Handling |
|------------|---------|---------------|
| 20001 | Missing parameter | Indicate that `chain_id` or `token_address` is empty; ask the user to provide the parameter. |
| 20002 | Parameter type error | Indicate that request parameter parsing failed. |
| 21001 | Unsupported chain | Indicate that the given `chain_id` is not currently supported. |
| 21002 | Data query failed | Server-side data retrieval error; suggest retrying later. |

### 6.3 Business Errors (Token Category base.token.*)

| Error Code | Meaning | Agent Handling |
|------------|---------|---------------|
| 41001 | Params error | Request parameter parsing failed, or a required parameter is empty. |
| 41002 | internal server error | System-level exception; suggest retrying later. |
| 41003 | This chain is not supported yet | The chain ID is not in the supported list. |
| 41102 | Token not found | For `risk_infos`, this means the token's security data has not been indexed. |

---

## 7. Security & Operational Rules

1. **Never display the Secret Key**: Never show the full SK in conversation.
2. **Config file security**: The credential file is stored at `~/.gate-dex-openapi/config.json`, which is inherently not tracked by git.
3. **Do not write to the workspace**: The Agent must not create, write, or modify any persistent script or log files in the user's workspace (repository) during the entire call flow. All API calls and signing operations must be completed in-memory via one-liner Shell inline commands (e.g., `python3 -c '...'`).
4. **Error transparency**: All API errors should be displayed as-is, accompanied by reasonable fix suggestions.
