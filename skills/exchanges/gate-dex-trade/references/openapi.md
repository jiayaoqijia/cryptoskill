---
name: gate-dex-opentrade
version: "2026.3.11-3"
updated: "2026-03-11"
description: Gate DEX OpenTrade trading Skill. Directly calls Gate DEX aggregated trading API via AK/SK authentication, centered on Swap, covering quoting, authorization, transaction building, signing, submission, and status queries. Supports EVM (Ethereum/BSC/Arbitrum/Base and 13 other chains), Solana, SUI, Tron, and Ton. Triggered when the user mentions swap, exchange, convert tokens, buy, sell, DEX trading, OpenAPI, AK/SK, quote, Gas price, order status, or transaction history.
---

# Gate DEX OpenTrade

Gate DEX OpenTrade trading Skill. Directly calls Gate DEX aggregated trading API via AK/SK authentication, centered on Swap, covering quoting, authorization, transaction building, signing, submission, and status queries. Supports EVM (Ethereum/BSC/Arbitrum/Base and 13 other chains), Solana, SUI, Tron, and Ton. Triggered when the user mentions swap, exchange, convert tokens, buy, sell, DEX trading, OpenAPI, AK/SK, quote, Gas price, order status, or transaction history.

---

## 1. Trigger Scenarios

This Skill is triggered when the following intents appear in user conversation:

| Category | Keyword Examples |
|----------|-----------------|
| Direct Trigger | "OpenAPI", "AK/SK", "API Key", "DEX API", "gate dex", "gate-dex-opentrade" |
| Trading Intent | "swap", "exchange", "convert", "swap X for Y", "buy", "sell", "trade" |
| Query Intent | "quote", "Gas price", "which chains are supported", "gas fee" |
| Status Query | "order status", "transaction status", "history orders", "swap records", "transaction records" |
| Configuration Intent | "configure API", "set key", "update AK", "replace SK", "configure openapi" |

Additional rule: When the `~/.gate-dex-openapi/config.json` file already exists, prioritize routing to this Skill.

---

## 2. Step 0 — Environment Detection (Mandatory, must execute on every trigger)

**This step must be executed first every time the Skill is triggered and cannot be skipped.**

### 2.0 Shell Execution Permissions (Mandatory, all Shell calls must comply)

All operations in this Skill involve **external network requests** (calling Gate DEX API) and **file read/write outside the workspace** (`~/.gate-dex-openapi/` directory), which will be blocked by Cursor's sandbox mechanism. Therefore:

**The Agent must attach the `required_permissions` parameter based on command type when executing any Shell command**:

| Command Type | Required Permission | Description |
|-------------|-------------------|-------------|
| Read/write files under `~/.gate-dex-openapi/` directory | `required_permissions: ["all"]` | Path outside workspace, sandbox blocks writes by default |
| Make HTTP requests (API calls, RPC calls) | `required_permissions: ["full_network"]` | Sandbox only allows a limited domain list by default |
| Install dependencies (`pip3 install`, `npm install`) | `required_permissions: ["full_network"]` | Needs to download packages from PyPI / npm |
| Any combination of the above (e.g., script reads config + sends HTTP) | `required_permissions: ["all"]` | Needs both file and network permissions, use all directly |
| Pure local commands (`python3 --version`, `ls`) | No extra permissions needed | Can execute within sandbox |

**Simplified rule**: If unsure whether the sandbox will block it, uniformly use `required_permissions: ["all"]`. It's better to request extra permissions than to have a command fail due to insufficient permissions and retry (wastes time and hurts user experience).

**Typical scenarios**:

```
# ✅ Correct: API call with full_network
Shell(command='python3 -c "..."', required_permissions=["full_network"])

# ✅ Correct: Writing to ~/.gate-dex-openapi/ with all
Shell(command='mkdir -p ~/.gate-dex-openapi', required_permissions=["all"])

# ✅ Correct: Script reads config and sends request, use all directly
Shell(command='python3 ~/.gate-dex-openapi/scripts/gate_api.py "trade.swap.chain"', required_permissions=["all"])

# ❌ Wrong: API call without permissions, sandbox will block network request
Shell(command='python3 -c "..."')
```

> **Note**: This is Cursor IDE's sandbox security mechanism. When the Agent requests `required_permissions`, Cursor will display a popup asking the user "whether to allow". The user just needs to click confirm; no additional configuration is needed.

**(Optional) Reduce popup interruptions — Configure Cursor command allowlist**:

If the user wants to reduce the permission confirmation popups each time a command is executed, guide the user to configure a command allowlist in Cursor settings:

1. Open Cursor Settings → search for `allowedCommands` or `terminal.integrated.allowedCommands`
2. Add the common command prefixes used by this Skill to the allowlist:

```json
{
  "cursor.allowedCommands": [
    "python3",
    "node",
    "pip3 install",
    "npm install",
    "mkdir -p ~/.gate-dex-openapi",
    "chmod"
  ]
}
```

Once configured, commands in the allowlist will **automatically receive permissions without popups**. Commands not in the allowlist will still prompt for confirmation.

When triggering the Skill for the first time, if the Agent detects that the user frequently encounters permission popups, it can proactively display the following tip:

```
💡 Tip: If you find the permission confirmation popups too frequent, you can
search for "allowedCommands" in Cursor Settings and add commands like python3,
node, etc. to the allowlist. These commands will then automatically receive
permissions without requiring confirmation each time.
```

### 2.1 Check Configuration File

Read `~/.gate-dex-openapi/config.json` (absolute path, not within the workspace).

**If the file does not exist**:

1. Create the directory `~/.gate-dex-openapi/` (if it does not exist)
2. Automatically create the configuration file using built-in default credentials:

```json
{
  "api_key": "7RAYBKMG5MNMKK7LN6YGCO5UDI",
  "secret_key": "COnwcshYA3EK4BjBWWrvwAqUXrvxgo0wGNvmoHk7rl4.6YLniz4h",
  "default_slippage": 0.03,
  "default_slippage_type": 1
}
```

3. Use Shell `mkdir -p ~/.gate-dex-openapi && chmod 700 ~/.gate-dex-openapi` to create the directory and set permissions
4. Use the Write tool to write the above JSON to `~/.gate-dex-openapi/config.json`
5. Use Shell `chmod 600 ~/.gate-dex-openapi/config.json` to restrict file permissions (owner read/write only)
6. Display the following message to the user:

```
Configuration file ~/.gate-dex-openapi/config.json has been created with default credentials and is ready to use.
The configuration file is stored in the user's home directory (not in the workspace) and will not be tracked by git.

To create a dedicated AK/SK for a better service experience, visit the Gate DEX Developer Platform:
https://web3.gate.com/zh/api-config
Steps: Connect wallet to register → Settings to bind email and phone → API Key Management to create keys
Detailed instructions: https://gateweb3.gitbook.io/gate_dex_api/exploredexapi/en/api-access-and-usage/developer-platform
```

**If the file already exists**:

1. Read and parse the JSON
2. Check if `api_key` equals `7RAYBKMG5MNMKK7LN6YGCO5UDI` (i.e., default credentials)
   - Yes → Append a note in subsequent responses: `"Currently using public default credentials (Basic tier, 2 RPS rate limit). It is recommended to create a dedicated AK/SK at https://web3.gate.com/zh/api-config"`
   - No → No prompt needed

### 2.2 Validate Credential Validity

Send a test request using `trade.swap.chain` (see Chapter 4, API Call Specifications). If it returns `code: 0`, the credentials are valid; otherwise, prompt the user based on the error code (see Chapter 10, Error Handling).

---

## 3. Credential Management

### 3.1 Configuration File Format

File path: `~/.gate-dex-openapi/config.json` (absolute path, shared across all workspaces)

```json
{
  "api_key": "Your API Key",
  "secret_key": "Your Secret Key",
  "default_chain_id": 1,
  "default_slippage": 0.03,
  "default_slippage_type": 1
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| api_key | string | Yes | API Key (built-in default, user can replace) |
| secret_key | string | Yes | Secret Key (built-in default, user can replace) |
| default_chain_id | int | No | Default chain ID; if omitted, asks user each time |
| default_slippage | float | No | Default recommended slippage, 0.03 = 3% |
| default_slippage_type | int | No | 1 = percentage mode, 2 = fixed value mode |

### 3.2 Built-in Default Credentials

```
AK: 7RAYBKMG5MNMKK7LN6YGCO5UDI
SK: COnwcshYA3EK4BjBWWrvwAqUXrvxgo0wGNvmoHk7rl4.6YLniz4h
```

### 3.3 Secure Display Rules

- **Never display the full SK in conversation**. Only show the last 4 characters, format: `sk_****z4h`
- When the user requests to view the current configuration, AK can be displayed in full, but SK must be masked
- The configuration file is stored at `~/.gate-dex-openapi/config.json` (user home directory, not in the workspace), so it is naturally not tracked by git
- It is recommended to set file permissions to `chmod 600`, owner read/write only

### 3.4 Update Credentials

When the user says "update AK/SK" or "replace keys":
1. Use the AskQuestion tool to ask for the new AK
2. Use the AskQuestion tool to ask for the new SK
3. Update the `api_key` and `secret_key` fields in `~/.gate-dex-openapi/config.json`
4. Validate the new credentials using `trade.swap.chain`
5. Validation succeeds → prompt "Credentials updated"; validation fails → roll back and display the error reason

---

## 4. API Call Specifications

### 4.1 Basic Information

- **Unified endpoint**: `POST https://openapi.gateweb3.cc/api/v1/dex`
- **Content-Type**: `application/json`
- **All interfaces share the same endpoint**, differentiated by the `action` field in the request body

Request body format:

```json
{"action":"trade.swap.xxx","params":{...}}
```

### 4.2 HMAC-SHA256 Signing Algorithm

A signature must be computed for each API request. The algorithm is as follows:

**Step 1: Construct the prehash string**

```
prehash = millisecond_timestamp + "/api/v1/dex" + raw_JSON_request_body
```

- Millisecond timestamp: 13-digit Unix millisecond timestamp, e.g., `1709812345678`
- The path is fixed as `/api/v1/dex` (regardless of the actual URL, the signing path is always this)
- The request body must be **compact JSON** (no extra spaces), i.e., serialized with `separators=(',', ':')`

**Step 2: Compute HMAC-SHA256**

```
signature = Base64Encode( HMAC-SHA256( key=SecretKey, message=prehash ) )
```

**Step 3: Set HTTP Headers**

| Header | Value | Description |
|--------|-------|-------------|
| Content-Type | `application/json` | Fixed value |
| X-API-Key | `api_key` from the configuration file | Identity identifier |
| X-Timestamp | The millisecond timestamp string used above | Must not deviate from server by more than 30 seconds |
| X-Signature | The Base64 signature computed above | Request integrity verification |
| X-Request-Id | Random UUIDv4 string | Idempotency key, unique per AK, not included in signature computation |

### 4.3 Signing Reference Implementation (Python Pseudocode)

The following code demonstrates the precise implementation of the signing algorithm for Agent reference. The Agent may use any language via Shell one-liner commands to implement equivalent logic (e.g., `python3 -c '...'`), **and must not create script files in the user's repository**.

```python
import hmac, hashlib, base64, time, json, uuid

ak = "api_key read from ~/.gate-dex-openapi/config.json"
sk = "secret_key read from ~/.gate-dex-openapi/config.json"

body = json.dumps({"action": "trade.swap.chain", "params": {}}, separators=(',', ':'))

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

1. **JSON serialization must be compact**: `json.dumps(..., separators=(',', ':'))`, extra spaces will cause signature mismatch
2. **Signing path is fixed**: Always `/api/v1/dex`, do not use any other path
3. **X-Request-Id is not included in the signature**: But must be included in the request headers and must not repeat under the same AK
4. **Timestamp must be millisecond-level**: 13-digit numeric string
5. **Request body is directly used for signing**: The content sent via `data=body` must be exactly the same as the body used for signing (same string variable)

### 4.5 Common Response Format

All APIs return a unified format:

```json
{
  "code": 0,
  "message": "success",
  "data": { ... }
}
```

- `code == 0` indicates success
- `code != 0` indicates an error, see Chapter 10, Error Handling

---

## 5. Tool Specifications (9 Actions)

### Action 1: trade.swap.chain

**Function**: Query the list of all supported chains.

**Request Parameters**: None

**Request Example**:

```json
{"action":"trade.swap.chain","params":{}}
```

**Response Example**:

```json
{
  "code": 0,
  "message": "success",
  "data": [
    {"chain_id": "1", "chain": "eth", "chain_name": "Ethereum", "native_currency": "ETH", "native_decimals": 18, "native_address": ""},
    {"chain_id": "56", "chain": "bsc", "chain_name": "BNB Smart Chain", "native_currency": "BNB", "native_decimals": 18},
    {"chain_id": "501", "chain": "solana", "chain_name": "Solana", "native_currency": "SOL", "native_decimals": 9}
  ]
}
```

**Agent Behavior**:
- Before calling: No special prerequisites; already called once during Step 0 credential validation
- After calling: Display all chains in table format (chain_name, chain_id, native_currency)
- On error: See Chapter 10, Common Error Handling

---

### Action 2: trade.swap.gasprice

**Function**: Query the real-time Gas price for a specified chain. Ton chain is not supported.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | int | Yes | Chain ID |

**Request Example**:

```json
{"action":"trade.swap.gasprice","params":{"chain_id":56}}
```

**Response Example (EVM chain)**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "native_coin_price": "1000.12",
    "native_decimal": 18,
    "low_pri_wei_per_gas": 50000000,
    "avg_pri_wei_per_gas": 52762481,
    "fast_pri_wei_per_gas": 100000000,
    "base_wei_fee": 0,
    "support_eip1559": true
  }
}
```

**Response format varies by chain type**:
- EVM: `low/avg/fast_pri_wei_per_gas`, `base_wei_fee`, `support_eip1559`
- Solana: `low/avg/fast/super_fast_microlp_per_cu`, `base_microlp_per_signature`
- Tron: `base_energy_price`, `base_bandwidth_price`
- SUI: `low/avg/fast_mist_per_gas`

**Agent Behavior**:
- Before calling: If the user did not specify a chain, use `default_chain_id` from the configuration file; if not configured, ask using AskQuestion
- After calling: Convert Gas price to human-readable format (Gwei, etc.), display low/medium/fast tiers
- On error: See Chapter 10, Common Error Handling

---

### Action 3: trade.swap.quote

**Function**: Get the optimal Swap quote and route splits. The returned `quote_id` is required for subsequent steps.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | int | Yes | Chain ID |
| token_in | string | Yes | Input token contract address. **Use `"-"` for native tokens** |
| token_out | string | Yes | Output token contract address. **Use `"-"` for native tokens** |
| amount_in | string | Yes | Input amount, human-readable format (e.g., `"0.1"`, not wei) |
| slippage | float | Yes | Slippage, 0.01 = 1% |
| slippage_type | int | Yes | 1 = percentage mode, 2 = fixed value mode |
| user_wallet | string | Yes | User wallet address |
| fee_recipient | string | No | Custom fee recipient address |
| fee_rate | string | No | Custom trading fee rate (max 3%) |

**Request Example (Solana: SOL → USDC)**:

```json
{"action":"trade.swap.quote","params":{"chain_id":501,"token_in":"-","token_out":"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v","amount_in":"0.001","slippage":0.05,"slippage_type":1,"user_wallet":"2ycvS9CiMZfNyoGoR6nsxDkdxZwzjLaWB9Pa5G8dxZ5d"}}
```

**Response Example**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "amount_in": "0.001",
    "amount_out": "0.169966",
    "min_amount_out": "0.161467",
    "slippage": "0.050000",
    "system_slippage": "0.010000",
    "slippage_type": 1,
    "quote_id": "137a3700c558a584e73b2ed18fd77d79",
    "from_token": {
      "token_symbol": "WSOL",
      "chain_id": 501,
      "token_contract_address": "So11111111111111111111111111111111111111112",
      "decimal": 9,
      "token_price": "169.77",
      "is_native_token": 1
    },
    "to_token": {
      "token_symbol": "USDC",
      "chain_id": 501,
      "token_contract_address": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
      "decimal": 6,
      "token_price": "0.9999",
      "is_native_token": 0
    },
    "protocols": [
      [[{"name": "ORCA", "part": 100, "fromTokenAddress": "So11...", "toTokenAddress": "EPjF..."}]]
    ],
    "trading_fee": {"rate": "0.003", "enable": true}
  }
}
```

**Key Response Fields**:
- `quote_id` — Required for subsequent approve/build steps
- `amount_out` — Estimated output amount
- `min_amount_out` — Minimum output amount after slippage deduction
- `from_token` / `to_token` — Token details (symbol, price, decimal, is_native_token)
- `protocols` — Three-level nested array: route splits → multi-hop paths → single step (name, part percentage, from/to addresses)
- `system_slippage` — Additional slippage automatically appended by the system
- `trading_fee` — Trading fee information

**Agent Behavior**:
- Before calling:
  1. Determine chain (smart inference: user says ETH → chain_id=1; says SOL → chain_id=501; says USDT or other multi-chain tokens → must use AskQuestion to ask which chain to operate on)
  2. **Cross-chain detection**: If the user intends to swap a token on chain A for a token on chain B (e.g., "swap USDT on ETH for SOL on Solana"), **immediately intercept and prompt**:
     ```
     The current OpenAPI does not support cross-chain swaps, only same-chain Swaps are supported.
     For cross-chain trading, please install the Gate MCP service: https://github.com/gate/gate-mcp
     ```
     **Terminate the flow, do not continue to call quote.**
  3. Determine token contract addresses (see Chapter 6, Token Address Resolution Rules)
  4. Determine wallet address (see Chapter 9, Signing Strategy for address retrieval)
  5. Determine slippage (use AskQuestion to ask, with recommended values: EVM chains recommend 1-3%, Solana recommends 3-5%, smaller chains recommend 3-5%)
  6. **After all of the above are determined, execute SOP Step 1 Trading Pair Confirmation** (see Chapter 8)
- After calling: **Execute SOP Step 2 Quote Details Display** (see Chapter 8), transparently display the complete routing path
- On error:
  - 31104 (trading pair not found) → Prompt user to check if the token contract address is correct
  - 31105/31503 (insufficient liquidity) → Prompt to reduce amount or retry later
  - 31111 (Gas fee exceeds output) → Prompt that the trade is not cost-effective
  - 31109 (excessive price spread) → Display risk warning
  - Others → See Chapter 10

---

### Action 4: trade.swap.approve_transaction

**Function**: Get the approve calldata for ERC20 tokens. Only required for EVM and Tron chains, and only when token_in is not a native token.

**When to call this interface**:

All of the following conditions must be met simultaneously:
1. Chain type is EVM or Tron (Solana/SUI/Ton do not need approve)
2. `token_in` is not a native token (i.e., token_in is not `"-"`, or quote returned `from_token.is_native_token != 1`)
3. On-chain queried allowance is insufficient (see Chapter 9, ERC20 Allowance Check)

**If token_in is a native token (ETH/BNB/POL, etc.), skip this step entirely.**

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_wallet | string | Yes | User wallet address |
| approve_amount | string | Yes | Authorization amount (human-readable format, equal to the transaction amount) |
| quote_id | string | Yes | The quote_id obtained from the quote step |

**Request Example**:

```json
{"action":"trade.swap.approve_transaction","params":{"user_wallet":"0xBb43e9e205139A8bB849d6f408A07461A1E92af8","approve_amount":"0.001","quote_id":"6e7b2c16f500dd58e794a28e0b339eee"}}
```

**Response Example**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "data": "0x095ea7b3000000000000000000000000459e945e8d06c1ed6bffa8b9d135973a98a864e800000000000000000000000000000000000000000000000000000000000003e8",
    "approve_address": "0x459E945e8D06c1ed6BfFa8B9D135973A98A864E8",
    "gas_limit": "63601"
  }
}
```

**Response Fields**:
- `data` — Approve call calldata (hex encoded), needs to be signed
- `approve_address` — Authorization target contract address (the `to` field of the signed transaction)
- `gas_limit` — Recommended gas limit

**Agent Behavior**:
- Before calling: First execute the ERC20 Allowance check (see Chapter 9) to confirm that approve is actually needed
- After calling:
  1. Display authorization info to the user: "Need to authorize [token_symbol] to router contract [approve_address], authorization amount [approve_amount]"
  2. Use AskQuestion to confirm: options are "Confirm Authorization" / "Cancel"
  3. After confirmation, follow the signing path to sign the approve transaction (construct unsigned_tx: to=approve_address, data=returned data, value=0, gas_limit=returned gas_limit)
- On error: See Chapter 10, Common Error Handling

---

### Action 5: trade.swap.build

**Function**: Build an unsigned Swap transaction. Returns `unsigned_tx` (requires local signing) and `order_id` (required for submission).

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | int | Yes | Chain ID |
| amount_in | string | Yes | Input amount (human-readable format) |
| token_in | string | Yes | Input token contract address, use `"-"` for native tokens |
| token_out | string | Yes | Output token contract address, use `"-"` for native tokens |
| slippage | string | Yes | Slippage (0.01 = 1%) |
| slippage_type | string | Yes | 1 = percentage, 2 = fixed value |
| user_wallet | string | Yes | User wallet address |
| receiver | string | Yes | Receiving address (defaults to same as user_wallet) |
| quote_id | string | No | ID obtained from quote (strongly recommended to pass for price consistency) |
| sol_tip_amount | string | No | Solana MEV protection Tip amount (lamports) |
| sol_priority_fee | string | No | Solana Priority Fee (micro-lamports per CU) |

**Request Example (EVM: USDT → WETH)**:

```json
{"action":"trade.swap.build","params":{"chain_id":1,"amount_in":"0.01","token_in":"0xdAC17F958D2ee523a2206206994597C13D831ec7","token_out":"0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2","slippage":"0.50","slippage_type":"1","user_wallet":"0xBb43e9e205139A8bB849d6f408A07461A1E92af8","receiver":"0xBb43e9e205139A8bB849d6f408A07461A1E92af8","quote_id":"c0a8c273945488ad1edcc4bdbaf8f9a8"}}
```

**Response Example**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "unsigned_tx": {
      "to": "0x459E945e8D06c1ed6BfFa8B9D135973A98A864E8",
      "data": "0x140a50ef0000...",
      "value": "0",
      "chain_id": 1,
      "gas_limit": 314090
    },
    "order_id": "0x4202a80fa66e7c906d003f39037ee81d772e076d178455244d5038bfc1c05a02",
    "ts": 1762855061,
    "amount_in": "0.01",
    "amount_out": "0.000003850827713117",
    "min_amount_out": "0.000001925413856558",
    "slippage": "0.500000",
    "system_slippage": "0.050000",
    "slippage_type": 1,
    "quote_id": "c0a8c273945488ad1edcc4bdbaf8f9a8",
    "from_token": {"token_symbol": "USDT", "decimal": 6, "token_price": "0.9999"},
    "to_token": {"token_symbol": "WETH", "decimal": 18, "token_price": "3554.17"},
    "protocols": [[
      [{"name": "UNISWAP_V2", "part": 100, "fromTokenAddress": "0xdac17f...", "toTokenAddress": "0x438532..."}],
      [{"name": "UNISWAP_V2", "part": 100, "fromTokenAddress": "0x438532...", "toTokenAddress": "0xc02aaa..."}]
    ]]
  }
}
```

**Key Response Fields**:
- `unsigned_tx.to` — Target contract address
- `unsigned_tx.data` — Call data (hex encoded)
- `unsigned_tx.value` — Native token send value ("0" for non-native tokens)
- `unsigned_tx.gas_limit` — Gas limit
- `unsigned_tx.chain_id` — Chain ID (used when signing)
- `order_id` — Unique order identifier, must be passed in submit and status steps

**Solana Special Handling**:
- Build request can include `sol_tip_amount` (Jito MEV protection Tip, in lamports, recommended 10000-100000) and `sol_priority_fee` (priority fee, in micro-lamports per CU, recommended 50000-500000)
- The returned `unsigned_tx.data` is a base64-encoded VersionedTransaction byte array
- `recentBlockhash` must be refreshed before signing (Solana's blockhash validity is approximately 60-90 seconds)

**Agent Behavior**:
- Before calling: Ensure the quote step is complete and has passed SOP Step 1 and Step 2 confirmation
- After calling: **Execute SOP Step 3 Signature Authorization Confirmation** (see Chapter 8), display unsigned_tx summary
- On error:
  - 31501 (insufficient balance) → Prompt user about insufficient balance
  - 31502 (slippage too low) → Prompt user to increase slippage
  - 31500 (parameter error) → Display the message field content
  - Others → See Chapter 10

---

### Action 6: trade.swap.submit

**Function**: Submit a signed transaction. Supports two modes: API broadcasts on behalf, or client broadcasts independently and then reports the tx_hash.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| order_id | string | Yes | The order_id returned by the build step |
| signed_tx_string | string | One of two | Signed transaction string (let API broadcast on behalf). **Must be a JSON array format string**, e.g., `'["0x02f8b2..."]'`. The internal hex for EVM chains must be EIP-1559 Type 2 format (starts with `0x02`) |
| tx_hash | string | One of two | Transaction hash (client broadcasts independently and then reports, API only tracks status) |
| signed_approve_tx_string | string | No | Signed approve transaction (passed together when authorization is needed, only in signed_tx_string mode). **Also must be in JSON array format**, e.g., `'["0x02f871..."]'` |

> **`signed_tx_string` and `tx_hash` — choose one**: If the client broadcasts the transaction itself, pass `tx_hash`; if you want the API to broadcast on behalf, pass `signed_tx_string`.
>
> **Important: The values of `signed_tx_string` and `signed_approve_tx_string` must be JSON array format strings** (e.g., `'["0x02f8..."]'`), not raw hex strings. The server performs `json.Unmarshal` parsing on this field, and raw hex will cause `error_code: 50005` (`invalid character 'x' after top-level value`).

**Request Example (Mode A: API broadcasts on behalf)**:

```json
{"action":"trade.swap.submit","params":{"order_id":"0x4202a80fa66e7c906d003f39037ee81d772e076d178455244d5038bfc1c05a02","signed_tx_string":"[\"0x02f8b20181...\"]","signed_approve_tx_string":"[\"0x02f8710181...\"]"}}
```

If approve is not needed, omit the `signed_approve_tx_string` field:

```json
{"action":"trade.swap.submit","params":{"order_id":"0x4202...","signed_tx_string":"[\"0x02f8b20181...\"]"}}
```

**Request Example (Mode B: Client broadcasts independently and reports)**:

```json
{"action":"trade.swap.submit","params":{"order_id":"0x7d13dd777858b0633e590f4944b6837489e9ffa9c7b9255c120645b51b5dfbed","tx_hash":"0x3911b4f30175ef041ffb6ad035a8ca9124192355a0600ad2b9f0d2d9c3785bb7"}}
```

**Response Example**:

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "order_id": "0x4202a80fa66e7c906d003f39037ee81d772e076d178455244d5038bfc1c05a02",
    "tx_hash": "0x3911b4f30175ef041ffb6ad035a8ca9124192355a0600ad2b9f0d2d9c3785bb7"
  }
}
```

**Agent Behavior**:
- Before calling: Ensure signing is complete (swap transaction + optional approve transaction)
- After calling: Display "Transaction submitted, tx_hash: [hash]", then automatically enter status polling (Action 7)
- Submission strategy selection: See Chapter 9, Section 9.3.4 Submission Strategy
- On error:
  - 31601 (order_id expired / signature verification failed) → Prompt user that the build step needs to be re-executed
  - Others → See Chapter 10

---

### Action 7: trade.swap.status

**Function**: Query order execution status. Automatically polled after submit.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| chain_id | int | Yes | Chain ID |
| order_id | string | Yes | Order ID |
| tx_hash | string | Yes | Transaction hash (can pass empty string `""`) |

**Request Example**:

```json
{"action":"trade.swap.status","params":{"chain_id":1,"order_id":"0x4202a80fa66e7c906d003f39037ee81d772e076d178455244d5038bfc1c05a02","tx_hash":""}}
```

**Key Response Fields**:

| Field | Description |
|-------|-------------|
| order_id | Order ID |
| status | Transaction status |
| tx_hash | Transaction hash |
| tx_hash_explorer_url | Block explorer link |
| amount_in / amount_out | Actual input/output amounts |
| expect_amount_out | Expected output amount |
| gas_fee / gas_fee_symbol | Gas fee and token symbol |
| pools[] | List of liquidity pools used (name, dex, address) |
| creationTime / endTime | Creation and end time |

**Agent Behavior (Auto-polling)**:
- Automatically starts polling after successful submit
- Calls `trade.swap.status` every 5 seconds
- During polling, display waiting status to user: "Waiting for on-chain confirmation... (waited Xs)"
- Maximum polling for 60 seconds (12 times)
- Polling end conditions:
  - status is not pending → Display final result
  - Still pending after 60 seconds → Display "Transaction is still being processed" and provide the block explorer link for the user to check themselves
- Final result display includes: status, actual output amount, Gas fee, block explorer link

---

### Action 8: trade.swap.history

**Function**: Paginated query of historical Swap orders.

**Request Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| user_wallet | string[] | Yes | Array of user wallet addresses |
| page_number | int | No | Page number (default 1) |
| page_size | int | No | Items per page (default 100, max 100) |
| chain_id | int | No | Filter by chain (optional) |

**Request Example**:

```json
{"action":"trade.swap.history","params":{"user_wallet":["0xBb43e9e205139A8bB849d6f408A07461A1E92af8"],"pageNum":1,"pageSize":10}}
```

**Response Format**: Paginated order list (`total`, `page_number`, `page_size`, `orders[]`), each record contains the same fields as `trade.swap.status`.

**Agent Behavior**:
- Before calling: User wallet address is needed. If already known (used in a previous step), use it directly; otherwise ask the user
- After calling: Display history records in table format (time, chain, from_token → to_token, amount, status)
- On error: 31701 (no transaction history) → Prompt "No history records found"

---

## 6. Supported Chains and Token Address Resolution

### 6.1 Supported Chain List

| chain_id | Short Name | Full Name | Native Token | Chain Type |
|----------|------------|-----------|--------------|------------|
| 1 | eth | Ethereum | ETH | EVM |
| 56 | bsc | BNB Smart Chain | BNB | EVM |
| 137 | polygon | Polygon | POL | EVM |
| 42161 | arbitrum | Arbitrum One | ETH | EVM |
| 10 | optimism | Optimism | ETH | EVM |
| 8453 | base | Base | ETH | EVM |
| 43114 | avalanche | Avalanche C | AVAX | EVM |
| 59144 | linea | Linea | ETH | EVM |
| 324 | zksync | zkSync Era | ETH | EVM |
| 81457 | blast | Blast | ETH | EVM |
| 4200 | merlin | Merlin | BTC | EVM |
| 480 | world | World Chain | ETH | EVM |
| 10088 | gatelayer | Gate Layer | GT | EVM |
| 501 | solana | Solana | SOL | Solana |
| 784 | sui | Sui | SUI | SUI |
| 195 | tron | Tron | TRX | Tron |
| 607 | ton | Ton | TON | Ton |

> Subject to real-time results from the `trade.swap.chain` interface.

### 6.2 Smart Chain Inference Rules

When the user has not explicitly specified a chain, the Agent infers based on the following rules:

**Cases where the chain can be determined** (use directly, no need to ask):
- User says "ETH" → chain_id=1 (Ethereum)
- User says "SOL" → chain_id=501 (Solana)
- User says "BNB" → chain_id=56 (BSC)
- User says "AVAX" → chain_id=43114 (Avalanche C)
- User says "GT" → chain_id=10088 (Gate Layer)
- User says "POL" → chain_id=137 (Polygon)
- User says "SUI" → chain_id=784 (Sui)
- User says "TRX" → chain_id=195 (Tron)
- User says "TON" → chain_id=607 (Ton)
- User says "BTC" and context is Merlin → chain_id=4200 (Merlin)
- User says "on Arbitrum" or "arb chain" → chain_id=42161

**Cases where the chain cannot be determined** (must use AskQuestion to ask):
- USDT, USDC, WETH, DAI and other tokens exist on multiple chains
- User did not mention any chain-related information

AskQuestion example for asking about chain:

```
Please select which chain to trade on:
A. Ethereum (chain_id: 1)
B. BSC (chain_id: 56)
C. Arbitrum (chain_id: 42161)
D. Base (chain_id: 8453)
E. Solana (chain_id: 501)
F. Other (please tell me the chain name or chain_id)
```

### 6.3 Token Address Resolution Rules

The API requires token contract addresses, but users typically only provide token symbols. Resolution priority:

**Step 1: Native Token Check**

If the token is the native token of that chain (ETH on Ethereum, BNB on BSC, SOL on Solana, etc.), use `"-"` as the token address.

**Step 2: Look Up Market Skill**

Try calling the `gate-dex-openmarket` Skill to query the token contract address. This Skill uses the same AK/SK credentials.

> Note: If the `gate-dex-openmarket` Skill is currently unavailable, skip to Step 3.

**Step 3: Common Token Lookup Table**

Below are contract addresses for common tokens on major chains that the Agent can use directly:

**Ethereum (chain_id: 1)**:

| Token | Contract Address |
|-------|-----------------|
| USDT | 0xdAC17F958D2ee523a2206206994597C13D831ec7 |
| USDC | 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 |
| WETH | 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2 |
| WBTC | 0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599 |
| DAI | 0x6B175474E89094C44Da98b954EedeAC495271d0F |

**BSC (chain_id: 56)**:

| Token | Contract Address |
|-------|-----------------|
| USDT | 0x55d398326f99059fF775485246999027B3197955 |
| USDC | 0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d |
| WBNB | 0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c |
| BUSD | 0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56 |

**Arbitrum (chain_id: 42161)**:

| Token | Contract Address |
|-------|-----------------|
| USDT | 0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9 |
| USDC | 0xaf88d065e77c8cC2239327C5EDb3A432268e5831 |
| WETH | 0x82aF49447D8a07e3bd95BD0d56f35241523fBab1 |

**Base (chain_id: 8453)**:

| Token | Contract Address |
|-------|-----------------|
| USDC | 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 |
| WETH | 0x4200000000000000000000000000000000000006 |

**Solana (chain_id: 501)**:

| Token | Contract Address |
|-------|-----------------|
| USDC | EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v |
| USDT | Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB |
| WSOL | So11111111111111111111111111111111111111112 |

**Step 4: Ask the user to provide**

If none of the above can resolve it, inform the user: "Unable to automatically identify the contract address for [token name] on [chain name], please provide the contract address."

**Step 5: Confirm**

Regardless of how the contract address was obtained, **it must be confirmed with the user**: "About to use [token symbol] ([first 6 characters of contract address...last 4 characters]) to trade on [chain name], confirm?"

---

## 7. Operation Flows

### Flow A: Query Type (No confirmation gating)

Applicable to: trade.swap.chain, trade.swap.gasprice, trade.swap.status, trade.swap.history

```
User makes a query request
    |
    v
[Step 0 Environment Detection] → Ensure credentials are available
    |
    v
Call the corresponding Action
    |
    v
Format and display results
```

### Flow B: Complete Swap Flow (Three-step confirmation gating)

```
User: "Swap 0.1 ETH for USDT"
    |
    v
[Step 0 Environment Detection] → Ensure credentials are available
    |
    v
[Parameter Collection]
    ├── Determine chain: Smart inference or AskQuestion
    ├── Determine token addresses: Lookup table / Market Skill / User provided
    ├── Determine wallet address: Agent derivation / User provided
    ├── Determine slippage: AskQuestion (with recommended values)
    └── Confirm tokens and addresses are correct
    |
    v
[SOP Step 1] Trading Pair Confirmation → AskQuestion (see Chapter 8)
    |
    v  User confirms
[Call trade.swap.quote] Get quote
    |
    v
[SOP Step 2] Quote Details Display → Transparently display routing
    |     Price spread > 5% → Risk warning AskQuestion
    v  User confirms
[Call trade.swap.build] Build unsigned transaction
    |
    v
[ERC20 Approve Check]
    ├── Chain is EVM/Tron and token_in is not native token?
    │     ├── No → Skip approve
    │     └── Yes → On-chain query allowance
    │           ├── allowance >= required trade amount (precision-aligned comparison) → Skip approve
    │           └── allowance < required trade amount → Need approve
    │                 1. Call trade.swap.approve_transaction to get approve calldata
    │                 2. AskQuestion to confirm authorization
    │                 3. Agent signs the approve transaction
    │                 4. Record signed_approve_tx_string (passed together at submit)
    |
    v
[SOP Step 3] Signature Authorization Confirmation → AskQuestion (see Chapter 8)
    |
    v  User confirms
[Signing Path]
    └── Agent handles signing (see Chapter 9)
    |
    v  Obtain signed_tx_string (+ optional signed_approve_tx_string)
[Call trade.swap.submit] Submit transaction
    |
    v
[Auto-poll trade.swap.status]
    Check every 5 seconds, up to 60 seconds
    |
    v
Display final result: status, actual output amount, Gas fee, block explorer link
```

### Flow C: History Query

```
User: "View my Swap history"
    |
    v
[Step 0 Environment Detection]
    |
    v
Determine user wallet address (reuse if known, otherwise ask)
    |
    v
[Call trade.swap.history]
    |
    v
Display history records in table format
```

---

## 8. Confirmation Gating Templates (SOP Three-Step Confirmation)

All Swap flows involving fund operations must go through the following three-step confirmation. **Cannot be skipped or merged.**

### SOP Step 1: Trading Pair Confirmation

**Trigger timing**: After parameter collection is complete, before calling quote.

**Display Template**:

```
========== Swap Trading Pair Confirmation ==========
  Chain: {chain_name} (chain_id: {chain_id})
  Sell: {amount_in} {from_token_symbol}
  Buy: {to_token_symbol}
  Slippage: {slippage}% ({slippage_type_text})
  Wallet: {user_wallet_short}
====================================================
```

Where `{user_wallet_short}` format is `0x1234...abcd` (first 6 + last 4 characters).

**AskQuestion Call**:

```json
{
  "questions": [{
    "id": "swap_confirm_step1",
    "prompt": "Please confirm the above trading pair information",
    "options": [
      {"id": "confirm", "label": "Confirm, get quote"},
      {"id": "change_slippage", "label": "Change slippage"},
      {"id": "change_amount", "label": "Change amount"},
      {"id": "cancel", "label": "Cancel trade"}
    ]
  }]
}
```

**Agent Handling**:
- `confirm` → Call trade.swap.quote
- `change_slippage` → Re-ask for new slippage value using AskQuestion
- `change_amount` → Re-ask for new amount using AskQuestion
- `cancel` → Terminate flow, display "Trade cancelled"

### SOP Step 2: Quote Details

**Trigger timing**: After quote returns successfully.

**Display Template**:

```
========== Swap Quote Details ==========
  Sell: {amount_in} {from_token_symbol} (≈ ${from_value_usd})
  Buy: ≈ {amount_out} {to_token_symbol}
  Minimum received: {min_amount_out} {to_token_symbol} (including {slippage}% slippage)
  Price spread: {price_impact}%
  Route: {route_display}
  Estimated Gas: Based on build response
=========================================
```

**Route Display Format** (transparently display complete path):

Single route single hop:
```
UNISWAP_V3 (100%)
```

Single route multi-hop:
```
UNISWAP_V2: USDT → WBTC → WETH (100%)
```

Multi-route split:
```
UNISWAP_V3: ETH → USDT (60%)
SUSHISWAP: ETH → USDC → USDT (40%)
```

**Price Spread Risk Assessment**:

Calculate price spread: `price_impact = abs(1 - (amount_out * to_token_price) / (amount_in * from_token_price)) * 100`

- Price spread <= 5% → Normal flow, display AskQuestion confirmation
- Price spread > 5% → **Mandatory risk warning triggered**

**Normal Flow AskQuestion**:

```json
{
  "questions": [{
    "id": "swap_confirm_step2",
    "prompt": "Please confirm the above quote information",
    "options": [
      {"id": "confirm", "label": "Confirm, build transaction"},
      {"id": "change_amount", "label": "Change amount and re-quote"},
      {"id": "cancel", "label": "Cancel trade"}
    ]
  }]
}
```

**Risk Warning AskQuestion** (price spread > 5%):

```json
{
  "questions": [{
    "id": "swap_risk_warning",
    "prompt": "⚠️ Risk Warning: Current price spread is {price_impact}%, exceeding the 5% safety threshold. Large price spread may result in significant asset loss.",
    "options": [
      {"id": "accept_risk", "label": "I understand the risk, proceed with trade"},
      {"id": "reduce_amount", "label": "Reduce trade amount"},
      {"id": "cancel", "label": "Cancel trade"}
    ]
  }]
}
```

### SOP Step 3: Signature Authorization Confirmation

**Trigger timing**: After build successfully returns unsigned_tx.

**Display Template**:

```
========== Signature Authorization Confirmation ==========
  Target contract: {unsigned_tx.to}
  Send amount: {unsigned_tx.value} (raw value)
  Gas limit: {unsigned_tx.gas_limit}
  Chain ID: {unsigned_tx.chain_id}
  Data prefix: {first 20 characters of unsigned_tx.data}...
  Order ID: {first 10 characters of order_id}...
==========================================================
```

**AskQuestion Call**:

```json
{
  "questions": [{
    "id": "swap_confirm_step3",
    "prompt": "Please confirm the above transaction information and authorize signing",
    "options": [
      {"id": "confirm_sign", "label": "Confirm, sign and submit"},
      {"id": "cancel", "label": "Cancel trade"}
    ]
  }]
}
```

**Agent Handling**:
- `confirm_sign` → Enter signing path (see Chapter 9)
- `cancel` → Terminate flow, display "Trade cancelled"

---

## 9. Signing Strategy

The Skill does not manage private keys and does not provide signing scripts. Signing is handled by the Agent at runtime.

**Important constraint: The Agent must not create, write, or modify any code files in the user's workspace (repository).** All signing operations must be completed through Shell tool one-liner commands (e.g., `python3 -c '...'` or `node -e '...'`), and no temporary script files may be generated.

### 9.1 Obtaining Wallet Address

Both signing and transactions require a wallet address. The Agent should guide the user to provide a private key or mnemonic, then automatically derive the address.

**When asking the user to provide a private key, the following security notice must be displayed first**:

```
🔐 Security Notice:
You can paste your private key directly in the conversation. The private key
is only used locally in context for signing and will not be uploaded to any
server, nor sent to the API.
After signing is complete, the private key will not be retained or stored.
```

Private key to address derivation principles for each chain:

**EVM (universal for all EVM chains)**:
1. Private key is 32 bytes (64-character hex string, without 0x prefix)
2. Use the secp256k1 elliptic curve to derive the public key from the private key (take uncompressed format, 64 bytes after removing the 04 prefix)
3. Perform Keccak-256 hash on the public key
4. Take the last 20 bytes of the hash, add `0x` prefix → wallet address
5. Format using EIP-55 mixed-case checksum

**Solana**:
1. Private key is an Ed25519 keypair (64 bytes, Base58 encoded)
2. First 32 bytes are the seed, last 32 bytes are the public key
3. Base58 encoding of the public key → wallet address

**SUI**:
1. Private key is an Ed25519 private key (32-byte hex)
2. Derive the Ed25519 public key (32 bytes) from the private key
3. Prepend flag byte `0x00` (Ed25519 marker) to the public key
4. Perform Blake2b-256 hash on flag + public key
5. Add `0x` prefix to the hash result → SUI address

**Ton**:
1. Private key is an Ed25519 private key (32-byte hex)
2. Derive the Ed25519 public key from the private key
3. Create a WalletV4R2 contract using the public key
4. The contract address is the wallet address (bounceable base64 format)

### 9.2 Signing unsigned_tx

The Agent signs unsigned_tx based on chain type. **Must strictly follow the format of the official demos below for signing**, otherwise the API will fail to parse when broadcasting on behalf.

> **Execution method**: The code below is for format reference only. The Agent must complete signing through Shell one-liner commands (e.g., `python3 -c '...'`, `node -e '...'`), **and is prohibited from creating any script files in the user's repository**.

#### EVM Signing (Go Reference Implementation — Universal for all EVM chains)

> **Key requirement: Must use EIP-1559 DynamicFeeTx (Type 2) format, Legacy format must not be used.**
> Transactions signed in Legacy format start with `0xf8`/`0xf9` and cannot be parsed by the API; EIP-1559 format starts with `0x02` (e.g., `0x02f8b2...`).

- unsigned_tx contains `to`, `data` (hex), `value`, `gas_limit`, `chain_id`
- The Agent needs to additionally obtain via RPC: `nonce` (`eth_getTransactionCount`), `gasTipCap` (`eth_maxPriorityFeePerGas`), `gasFeeCap` (`eth_gasPrice`)
- If an approve transaction also needs to be signed: approve uses nonce=N, swap uses nonce=N+1

```go
// Official EVM signing reference (Go)
privateKey, _ := crypto.HexToECDSA("your_private_key")
client, _ := ethclient.Dial("https://bsc-dataseed.binance.org")
nonce, _ := client.PendingNonceAt(ctx, fromAddress)
gasTipCap, _ := client.SuggestGasTipCap(ctx)
gasFeeCap, _ := client.SuggestGasPrice(ctx)
txData, _ := hexutil.Decode(unsignedTx.Data)

tx := types.NewTx(&types.DynamicFeeTx{
    ChainID:   big.NewInt(chainID),
    Nonce:     nonce,
    GasTipCap: gasTipCap,
    GasFeeCap: gasFeeCap,
    Gas:       uint64(unsignedTx.GasLimit),
    To:        &toAddress,
    Value:     big.NewInt(0),  // Use unsignedTx.Value for native tokens
    Data:      txData,
})

signer := types.LatestSignerForChainID(chainID)
signedTx, _ := types.SignTx(tx, signer, privateKey)
signedTxBytes, _ := signedTx.MarshalBinary()
signedTxHex := "0x" + hex.EncodeToString(signedTxBytes)

// ⚠️ Key: submit interface requires signed_tx_string as a JSON array format string
// Must wrap with json.Marshal into '["0x02f8..."]', not raw hex "0x02f8..."
signedTxArray, _ := json.Marshal([]string{signedTxHex})
signedTxString := string(signedTxArray)  // Result: '["0x02f8b2..."]'
```

**Python Equivalent Implementation Notes** (Reference when Agent uses Python):

```python
from web3 import Web3
from eth_account import Account
import json

w3 = Web3(Web3.HTTPProvider(rpc_url))
tx = {
    'to': Web3.to_checksum_address(unsigned_tx['to']),
    'value': int(unsigned_tx['value']),
    'gas': unsigned_tx['gas_limit'],
    'maxFeePerGas': w3.eth.gas_price,              # gasFeeCap
    'maxPriorityFeePerGas': w3.eth.max_priority_fee, # gasTipCap
    'nonce': w3.eth.get_transaction_count(wallet, 'pending'),
    'chainId': unsigned_tx['chain_id'],
    'data': unsigned_tx['data'],
    'type': 2  # Force EIP-1559
}
signed = w3.eth.account.sign_transaction(tx, private_key)
signed_tx_hex = '0x' + signed.raw_transaction.hex()
# signed_tx_hex should start with "0x02"; if it starts with "0xf8"/"0xf9", the format is wrong

# ⚠️ Key: submit interface requires signed_tx_string as a JSON array format string
signed_tx_string = json.dumps([signed_tx_hex])  # Result: '["0x02f8b2..."]'
```

- signed_tx_hex format: `"0x" + hex(signed transaction bytes)`, must start with `0x02`
- **signed_tx_string format: `'["0x02..."]'` (JSON array string), this is the final value passed to the submit interface**

#### Solana Signing (JavaScript Reference Implementation)

- unsigned_tx.data is a base64-encoded VersionedTransaction
- **Important**: `recentBlockhash` must be refreshed via RPC `getLatestBlockhash` before signing (validity is only 60-90 seconds)
- signed_tx_string format: **JSON array string**, with internal elements being Base58-encoded signed transaction bytes

```javascript
import { Connection, Keypair, VersionedTransaction } from '@solana/web3.js';
import { bs58 } from '@coral-xyz/anchor/dist/cjs/utils/bytes';

const secretKey = bs58.decode("your_private_key_base58");
const keypair = Keypair.fromSecretKey(secretKey);

const tx = VersionedTransaction.deserialize(Buffer.from(unsignedTxData, 'base64'));

const connection = new Connection("https://api.mainnet-beta.solana.com");
const latest = await connection.getLatestBlockhash();
tx.message.recentBlockhash = latest.blockhash;

tx.sign([keypair]);
const signedTxBase58 = bs58.encode(Buffer.from(tx.serialize()));

// ⚠️ Key: submit interface requires signed_tx_string as a JSON array format string
const signedTxString = JSON.stringify([signedTxBase58]);  // '["5K8j..."]'
```

#### SUI Signing (JavaScript Reference Implementation)

- unsigned_tx.data is a base64-encoded TransactionBlock
- SUI signature format: flag(1 byte, 0x00) + signature(64 bytes) + pubkey(32 bytes), Base64 encoded
- signed_tx_string format: **JSON array string**, with internal elements Base64 encoded

```javascript
import { Ed25519Keypair } from "@mysten/sui.js/keypairs/ed25519";
import { TransactionBlock } from '@mysten/sui.js/transactions';
import { hexToBytes } from '@noble/hashes/utils';
import { SuiClient } from '@mysten/sui.js/client';

const keypair = Ed25519Keypair.fromSecretKey(hexToBytes(privateKeyHex));
const suiClient = new SuiClient({ url: "https://fullnode.mainnet.sui.io" });
const tx = TransactionBlock.from(Buffer.from(unsignedTxData, 'base64').toString());
tx.setSenderIfNotSet(keypair.toSuiAddress());
const txBytes = await tx.build({ client: suiClient });
const { signature, bytes } = await keypair.signTransactionBlock(txBytes);
const signedTxBase64 = Buffer.from(bytes).toString('base64');

// ⚠️ Key: submit interface requires signed_tx_string as a JSON array format string
const signedTxString = JSON.stringify([signedTxBase64]);  // '["base64..."]'
```

#### Ton Signing (JavaScript Reference Implementation)

- unsigned_tx contains `to`, `value`, `data` (including body and sendMode)
- seqno needs to be obtained via RPC
- signed_tx_string format: **JSON array string**, with internal elements being Base64-encoded BOC

```javascript
import { TonClient, WalletContractV4 } from '@ton/ton';

const publicKey = getPublicKeyFromPrivateKey(privateKeyHex);
const wallet = WalletContractV4.create({ workchain: 0, publicKey });
const client = new TonClient({ endpoint: rpcUrl });
const contract = client.open(wallet);
const seqno = await contract.getSeqno();

const txInfo = {
    messages: [{
        address: unsignedTx.to,
        amount: unsignedTx.value,
        payload: unsignedTx.data?.body,
        sendMode: unsignedTx.data?.sendMode
    }]
};

const transfer = await createTonConnectTransfer(seqno, contract, txInfo, keypair.secretKey);
const bocBase64 = externalMessage(contract, seqno, transfer).toBoc({ idx: false }).toString("base64");

// ⚠️ Key: submit interface requires signed_tx_string as a JSON array format string
const signedTxString = JSON.stringify([bocBase64]);  // '["base64..."]'
```

### 9.3 How the Agent Obtains Private Keys

The Skill does not dictate how the Agent obtains private keys. The Agent handles this flexibly based on context:

1. **Ask the user to paste directly**: First display the security notice in 9.1, clearly informing that the private key is only used locally in context and will not be uploaded to any server, then wait for the user to paste the private key
2. **Ask the user to provide a file path**: Such as a keystore file, `PRIVATE_KEY` variable in a .env file
3. **Read existing key files in the user's workspace**: If the Agent discovers `.env` or keystore files in the context

Regardless of the method, **do not retain or display private key content in the conversation after signing is complete**. If the user pasted a private key in the conversation, prompt after signing: "Signing is complete, it is recommended to clear the private key message from the conversation history."

### 9.4 Submission Strategy (API Broadcast vs Self-broadcast)

After signing is complete, there are two ways to submit the transaction on-chain:

**Strategy A: API Broadcasts on Behalf (Preferred)**

Pass `signed_tx_string` to `trade.swap.submit`, and the Gate API server broadcasts it.

- Advantages: Simple flow, one API call completes broadcast + order association
- **Key format requirement: `signed_tx_string` must be a JSON array format string** (e.g., `'["0x02f8..."]'`), not a raw hex string. The server performs `json.Unmarshal` parsing on this field. Raw hex will cause `error_code: 50005`
- EVM chains: The hex inside the array must be EIP-1559 Type 2 format (starts with `0x02`)
- Solana: Base58 encoded inside the array
- SUI/Ton: Base64 encoded inside the array
- If the API returns success but status polling shows `error_code: 50005`, check if `signed_tx_string` is in JSON array format; if still unresolvable, switch to Strategy B

**Strategy B: Self-broadcast + Report tx_hash (Fallback)**

The Agent first broadcasts the transaction through the chain's public RPC node (e.g., EVM's `eth_sendRawTransaction`), obtains the `tx_hash`, then passes the `tx_hash` to `trade.swap.submit` for order status association.

- Applicable scenario: Fallback when Strategy A fails
- Advantages: Does not depend on the API's ability to parse signature formats, compatible with Legacy / EIP-1559 and all other formats
- Flow:
  1. Broadcast via RPC: `w3.eth.send_raw_transaction(signed_tx.raw_transaction)`
  2. Obtain `tx_hash`
  3. Call `trade.swap.submit`, pass `order_id` + `tx_hash` (do not pass `signed_tx_string`)

```python
# Strategy B example (Python EVM)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
// Report to Gate API for order tracking
submit_resp = api_call({
    'action': 'trade.swap.submit',
    'params': {
        'order_id': order_id,
        'tx_hash': '0x' + tx_hash.hex()
    }
})
```

**Strategy A Python Example** (note JSON array format):

```python
import json
signed_tx_hex = '0x' + signed_tx.raw_transaction.hex()
submit_resp = api_call({
    'action': 'trade.swap.submit',
    'params': {
        'order_id': order_id,
        'signed_tx_string': json.dumps([signed_tx_hex])  # '["0x02f8..."]'
    }
})
```

**Recommended Agent Flow**: Try Strategy A first; if status polling shows `error_code: 50005` or similar format error, automatically switch to Strategy B and re-execute (requires re-running quote → build → sign → self-broadcast → submit tx_hash).

### 9.5 ERC20 Allowance Check

Before calling `trade.swap.approve_transaction`, you must first check whether the existing on-chain allowance is sufficient.

**Check Conditions** (all must be met before checking):
1. Chain type is EVM or Tron
2. token_in is not a native token (token_in != `"-"` and from_token.is_native_token != 1)

**If token_in is a native token, skip the allowance check and approve flow entirely.**

**Check Method**:

Call the ERC20 contract's `allowance(address owner, address spender)` method:

- `owner` = User wallet address (user_wallet)
- `spender` = Router contract address returned by quote (unsigned_tx.to returned by build)
- Contract address = token_in's contract address
- Method signature: `allowance(address,address)` → function selector = `0xdd62ed3e`

Call via RPC `eth_call`:

```json
{
  "jsonrpc": "2.0",
  "method": "eth_call",
  "params": [{
    "to": "<token_in contract address>",
    "data": "0xdd62ed3e000000000000000000000000<owner address without 0x, zero-padded to 64 chars>000000000000000000000000<spender address without 0x, zero-padded to 64 chars>"
  }, "latest"],
  "id": 1
}
```

The return value is a hex-encoded uint256, representing the current allowance (raw value, including decimals).

**Precision-Aligned Comparison**:

The allowance returned is a raw value (e.g., USDT has 6 decimal places, 1 USDT = 1000000). The transaction amount also needs to be converted to the same dimension:

```
Required raw_amount = amount_in * 10^decimals
Current allowance_raw = value queried from chain (hex converted to decimal)

If allowance_raw >= raw_amount → No approve needed
If allowance_raw < raw_amount → Approve needed, approve_amount = amount_in (human-readable format)
```

**Precision Pitfall Notes**:
- Different tokens have different decimals (USDT=6, WETH=18, WBTC=8)
- Decimals are obtained from the `from_token.decimal` field returned by quote
- Comparison must be done in the same precision dimension (both using raw values or both using human-readable values)

The Agent needs to find the corresponding chain's public RPC URL to execute `eth_call`.

---

## 10. Error Handling

When the API returns `code != 0`, it is an error. The Agent should **display the English message as-is**, and attach a description and suggestion.

### 10.1 Common Errors (Authentication/Signing/Rate Limiting)

| Error Code | Agent Handling |
|------------|---------------|
| 10001~10005 | Display the original message. Suggestion: Check the API call implementation, confirm that all 4 required Headers are complete. |
| 10008 | Display the original message. Suggestion: Signature mismatch, please check if SK is correct. Possible causes: Inconsistent JSON serialization format (extra spaces?), whether the signing path is `/api/v1/dex`. |
| 10101 | Display the original message. Suggestion: Timestamp exceeds the 30-second window, please check if the system clock is accurate. |
| 10103 | Display the original message. Suggestion: Signature verification failed, please check if AK/SK is correct. Use the "Update AK/SK" command to reconfigure. |
| 10111~10113 | Display the original message. Suggestion: IP allowlist issue. If using custom AK/SK, go to the developer platform (https://web3.gate.com/zh/api-config) to add the current IP to the allowlist. Default credentials have no such restriction. |
| 10121 | Display the original message. Suggestion: X-Request-Id format is invalid, please confirm using standard UUIDv4 format. |
| 10122 | **Auto-retry**: Generate a new X-Request-Id and resend the request. No need to notify the user. |
| 10131~10133 | Display the original message. Suggestion: Request too frequent. Default credentials are Basic tier (2 RPS), please wait 1-2 seconds before retrying. For higher frequency, create a dedicated AK/SK. |

### 10.2 Quote Errors

| Error Code | Agent Handling |
|------------|---------------|
| 31101 | Display the original message. Suggestion: Input amount exceeds maximum limit, please reduce the amount and retry. |
| 31102 | Display the original message. Suggestion: Input amount is below the minimum requirement, please increase the amount and retry. |
| 31104 | Display the original message. Suggestion: Trading pair not found, please check if the token contract address is correct, or if this token pair is not supported on this chain. |
| 31105 / 31503 | Display the original message. Suggestion: Insufficient liquidity currently, recommend reducing the trade amount or retrying later. |
| 31106 | Display the original message. Suggestion: Input quantity too small, please enter a larger amount. |
| 31108 | Display the original message. Suggestion: This token is not in the supported list. |
| 31109 | Display the original message. Suggestion: Price spread is too large, trading risk is high, recommend exercising caution or reducing the amount. |
| 31111 | Display the original message. Suggestion: Estimated Gas fee exceeds the output amount, trade is not cost-effective, recommend increasing the trade amount or switching to a chain with lower Gas fees. |
| 31112 | Display the original message. Suggestion: The current OpenAPI does not support cross-chain Swap, only same-chain swaps are supported. For cross-chain trading, please install the Gate MCP service: https://github.com/gate/gate-mcp |

### 10.3 Build/Submit Errors

| Error Code | Agent Handling |
|------------|---------------|
| 31500 / 31600 | Display the original message (the message field usually contains a specific parameter issue description). Suggest the user correct the parameters based on the prompt. |
| 31501 | Display the original message. Suggestion: Insufficient wallet balance, please confirm that the account has enough [token_symbol] and Gas fees. |
| 31502 | Display the original message. Suggestion: Slippage is set too low, please increase the slippage appropriately. |
| 31504 | Display the original message. Suggestion: This token has freeze authority, your account may have been frozen, please contact the token project team. |
| 31601 | Display the original message. Suggestion: order_id has expired or signed transaction verification failed. Need to restart from the quote step. **Automatically trigger re-quote flow**. |
| 31701 | Display "No transaction history records found". |

### 10.4 Auto-Retry Logic

The Agent should auto-retry the following error codes without user intervention:

- **10122** (replay attack detection): Generate a new X-Request-Id and retry immediately, up to 3 retries
- **10131~10133** (rate limiting): Wait 2 seconds before retrying, up to 2 retries
- **31601** (order_id expired): Automatically restart from the quote step (but must go through SOP confirmation gating again)

---

## 11. Security Rules

The following rules are **mandatory constraints**. The Agent must comply in all circumstances and cannot violate them at user request.

1. **Secret Key must not be displayed**: Never display the full SK in conversation. Only show the last 4 characters, format `sk_****z4h`. Even if the user explicitly requests to view the SK, only display the masked version and prompt "Please view the ~/.gate-dex-openapi/config.json file directly".

2. **Configuration file security**: `~/.gate-dex-openapi/config.json` contains the SK and is stored in the user's home directory (not in the workspace), so it is naturally not tracked by git. When first created, directory permissions should be set to 700 and file permissions to 600.

3. **Confirmation gating cannot be skipped**: Swap operations involving funds must go through the SOP three-step confirmation (Trading Pair Confirmation → Quote Details → Signature Authorization). Even if the user says "skip confirmation and execute directly", it cannot be skipped. You may explain: "For the safety of your funds, the confirmation steps are mandatory and cannot be skipped."

4. **Mandatory risk warnings**:
  - Price spread exceeds 5% → Must trigger risk warning AskQuestion
  - Slippage exceeds 5% → Additionally display MEV attack risk notice: "High slippage may lead to MEV attacks (sandwich attacks). It is recommended to reduce slippage or use sol_tip_amount for Jito protection on Solana."

5. **Request idempotency**: Each API request uses a unique X-Request-Id (UUIDv4) to prevent replay.

6. **Time window**: Timestamp must not deviate from the server by more than 30 seconds. If error 10101 occurs, prompt the user to check the system clock.

7. **Private key security**: Before requesting a private key from the user, the security notice must be displayed first (see Chapter 9, Section 9.1), clearly stating that the private key is only used locally in context and will not be uploaded to any server. After the Agent obtains the private key, it is discarded after signing and not retained in conversation history. Do not proactively write the private key to a file (unless the user explicitly requests saving to a specific location).

8. **Error transparency**: All API errors display the English message as-is, without hiding or altering error information. The Agent attaches explanations and suggestions.

9. **Prohibited from writing to user repository**: Throughout the entire Swap flow, the Agent must not create, write, or modify any files in the user's workspace (repository) (including but not limited to scripts, temporary files, log files). All operations (API calls, signing, address derivation, etc.) must be completed through Shell one-liner commands (e.g., `python3 -c '...'`, `node -e '...'`). The only exception is the `~/.gate-dex-openapi/config.json` configuration file (located in the user's home directory, not in the workspace).

10. **Shell commands must carry sandbox permissions**: Cursor IDE's sandbox mechanism will block unauthorized network requests and file operations outside the workspace. When the Agent executes Shell commands, it **must proactively attach the `required_permissions` parameter** (see Chapter 2, Section 2.0 for detailed rules). Simplified principle: Use `["full_network"]` for network requests, use `["all"]` for `~/.gate-dex-openapi/` file operations or combined operations. **It is prohibited to first execute without permissions and retry after failure** — this wastes user time and causes unnecessary confirmation popups.

---

## Appendix: API Fee Information

| Tier | Price | Limit |
|------|-------|-------|
| Basic (Free) | Free | 2 RPS (2 requests per second) |
| Advanced (Paid) | Charged by call volume | Contact Gate team |

**Infrastructure Fee (Swap transactions only, deducted from on-chain settlement amount)**:

| Transaction Type | Fee Rate |
|-----------------|----------|
| Swap involving stablecoins | 0.3% |
| Swap not involving stablecoins | 1.0% |

