# Hyperliquid CLI Reference

Complete command reference for the Hyperliquid CLI.

## Global Options

These options can be used with any command:

| Option          | Description                         |
| --------------- | ----------------------------------- |
| `--json`        | Output in JSON format for scripting |
| `--testnet`     | Use testnet instead of mainnet      |
| `-V, --version` | Show version number                 |
| `-h, --help`    | Show help                           |

---

## Account Management

Commands for managing trading accounts stored locally in `~/.hyperliquid/accounts.db`.

### `hl account add`

Interactive wizard to add a new account.

**Process:**

1. Choose account type (API wallet for trading, read-only for monitoring)
2. Enter private key (for API wallet) or address (for read-only)
3. Set an alias for easy identification
4. Optionally set as default account

**Example:**

```bash
hl account add
# Follow interactive prompts
```

### `hl account ls`

List all configured accounts.

**Output columns:**

- Alias
- Address (truncated)
- Type (api-wallet or read-only)
- Default status

**Example:**

```bash
hl account ls
```

**JSON output:**

```json
[
  {
    "alias": "main",
    "address": "0x1234...abcd",
    "type": "api-wallet",
    "isDefault": true
  }
]
```

### `hl account set-default`

Interactively select which account to use by default.

```bash
hl account set-default
```

### `hl account remove`

Interactively remove an account from local storage.

```bash
hl account remove
```

---

## Position Monitoring

### `hl account positions`

View perpetual positions.

**Options:**
| Option | Description |
|--------|-------------|
| `-w, --watch` | Real-time updates via WebSocket |
| `--user <address>` | View positions for specific address |

**Output columns:**

- Coin
- Size (positive = long, negative = short)
- Entry Price
- Position Value
- Unrealized PnL (color-coded: green = profit, red = loss)
- Leverage
- Liquidation Price

**Examples:**

```bash
hl account positions
hl account positions -w
hl account positions --user 0x1234...
hl account positions --json
```

**JSON output:**

```json
{
  "positions": [
    {
      "coin": "BTC",
      "size": "0.1",
      "entryPx": "50000.0",
      "positionValue": "5000.0",
      "unrealizedPnl": "250.0",
      "leverage": "10",
      "liquidationPx": "45000.0"
    }
  ]
}
```

---

## Order Management

### `hl account orders`

View open orders.

**Options:**
| Option | Description |
|--------|-------------|
| `-w, --watch` | Real-time updates |
| `--user <address>` | View orders for specific address |

**Alias:** `hl order ls`

**Examples:**

```bash
hl account orders
hl account orders -w
hl account orders --json
```

**JSON output:**

```json
[
  {
    "oid": 12345,
    "coin": "BTC",
    "side": "buy",
    "size": "0.1",
    "price": "50000.0",
    "type": "limit",
    "tif": "Gtc"
  }
]
```

### `hl order limit <side> <size> <coin> <price>`

Place a limit order.

**Arguments:**
| Argument | Description |
|----------|-------------|
| `side` | `buy`, `sell`, `long`, or `short` |
| `size` | Order size |
| `coin` | Asset symbol (BTC, ETH, AAPL, GOLD, etc.) |
| `price` | Limit price |

**Options:**
| Option | Description |
|--------|-------------|
| `--tif <tif>` | Time-in-force: `Gtc` (default), `Ioc`, `Alo` |
| `--reduce-only` | Reduce-only order |

**Examples:**

```bash
# Buy 0.001 BTC at $50,000
hl order limit buy 0.001 BTC 50000

# Sell 0.1 ETH at $3,500 with Good-til-Cancelled
hl order limit sell 0.1 ETH 3500 --tif Gtc

# Reduce-only order
hl order limit sell 0.001 BTC 55000 --reduce-only

# Trade HIP3 assets
hl order limit buy 10 AAPL 200
hl order limit buy 1 GOLD 2500
```

**JSON output:**

```json
{
  "response": {
    "data": {
      "statuses": [{ "resting": { "oid": 12345 } }]
    }
  }
}
```

### `hl order market <side> <size> <coin>`

Place a market order.

**Arguments:**
| Argument | Description |
|----------|-------------|
| `side` | `buy`, `sell`, `long`, or `short` |
| `size` | Order size |
| `coin` | Asset symbol |

**Options:**
| Option | Description |
|--------|-------------|
| `--slippage <pct>` | Slippage percentage (default: 1%) |
| `--reduce-only` | Reduce-only order |

**Examples:**

```bash
hl order market buy 0.001 BTC
hl order market sell 0.1 ETH --slippage 0.5
hl order market buy 5 NVDA
```

### `hl order configure`

Configure order defaults.

**Options:**
| Option | Description |
|--------|-------------|
| `--slippage <pct>` | Set default slippage for market orders |

**Examples:**

```bash
# View current configuration
hl order configure

# Set default slippage to 0.5%
hl order configure --slippage 0.5
```

### `hl order cancel [oid]`

Cancel an order.

**Arguments:**
| Argument | Description |
|----------|-------------|
| `oid` | Order ID (optional - interactive if omitted) |

**Examples:**

```bash
# Interactive selection from open orders
hl order cancel

# Cancel specific order
hl order cancel 12345
```

### `hl order cancel-all`

Cancel all open orders.

**Options:**
| Option | Description |
|--------|-------------|
| `--coin <coin>` | Only cancel orders for specific coin |
| `-y, --yes` | Skip confirmation prompt |

**Examples:**

```bash
# Cancel all orders (with confirmation)
hl order cancel-all

# Cancel all BTC orders
hl order cancel-all --coin BTC

# Skip confirmation
hl order cancel-all -y
```

### `hl order set-leverage <coin> <leverage>`

Set leverage for a coin.

**Arguments:**
| Argument | Description |
|----------|-------------|
| `coin` | Asset symbol |
| `leverage` | Leverage value (1-50 depending on asset) |

**Options:**
| Option | Description |
|--------|-------------|
| `--isolated` | Use isolated margin |
| `--cross` | Use cross margin (default) |

**Examples:**

```bash
# Set 10x cross margin leverage for BTC
hl order set-leverage BTC 10

# Set 5x isolated margin leverage
hl order set-leverage ETH 5 --isolated
```

---

## Balance & Portfolio

### `hl account balances`

View account balances (spot + perpetuals).

**Options:**
| Option | Description |
|--------|-------------|
| `-w, --watch` | Real-time updates |
| `--user <address>` | View balances for specific address |

**Examples:**

```bash
hl account balances
hl account balances -w
hl account balances --json
```

**JSON output:**

```json
{
  "spot": [{ "token": "USDC", "total": "10000.0", "hold": "500.0", "available": "9500.0" }],
  "perp": {
    "accountValue": "10000.0",
    "marginUsed": "2000.0",
    "available": "8000.0"
  }
}
```

### `hl account portfolio`

Combined view of positions and balances.

**Options:**
| Option | Description |
|--------|-------------|
| `-w, --watch` | Real-time updates |
| `--user <address>` | View portfolio for specific address |

**Examples:**

```bash
hl account portfolio
hl account portfolio -w
```

---

## Market Information

### `hl markets ls`

List all available markets (perpetual and spot).

**Examples:**

```bash
hl markets ls
hl markets ls --json
```

**Output includes:**

- Market name
- Type (perp/spot)
- Max leverage
- Price decimals
- Size decimals

---

## Asset Information

### `hl asset price <coin>`

Get current price for an asset.

**Options:**
| Option | Description |
|--------|-------------|
| `-w, --watch` | Real-time price updates |

**Examples:**

```bash
hl asset price BTC
hl asset price ETH -w
hl asset price AAPL --json

# HIP3 assets
hl asset price NVDA
hl asset price GOLD
```

**JSON output:**

```json
{
  "coin": "BTC",
  "price": "50000.0"
}
```

### `hl asset book <coin>`

View order book for an asset.

**Options:**
| Option | Description |
|--------|-------------|
| `-w, --watch` | Real-time order book updates |

**Examples:**

```bash
hl asset book BTC
hl asset book ETH -w
hl asset book AAPL --json
```

**Output includes:**

- Top bid/ask levels
- Cumulative depth visualization
- Spread calculation

### `hl asset leverage <coin>`

Get leverage and margin info for a specific asset.

**Arguments:**
| Argument | Description |
|----------|-------------|
| `coin` | Coin symbol (e.g., BTC, ETH, xyz:AAPL) |

**Options:**
| Option | Description |
|--------|-------------|
| `-w, --watch` | Real-time updates via WebSocket |
| `--user <address>` | View leverage info for specific address |

**Examples:**

```bash
hl asset leverage BTC
hl asset leverage ETH -w
hl asset leverage BTC --user 0x1234...
hl asset leverage BTC --json
```

**Output includes:**

- Current leverage value and type (cross/isolated)
- Maximum leverage for the asset
- Mark price
- Max trade sizes and available to trade (short/long capacity)
- Current position size and value (if any)
- Account value, margin used, and available margin

**JSON output:**

```json
{
  "coin": "BTC",
  "leverage": { "value": 10, "type": "cross" },
  "maxLeverage": 50,
  "markPx": "85000.0",
  "maxTradeSzs": ["0", "1.5"],
  "availableToTrade": ["0", "1.2"],
  "position": { "size": "0.01", "value": "850.00" },
  "margin": {
    "accountValue": "10000.00",
    "totalMarginUsed": "850.00",
    "availableMargin": "9150.00"
  }
}
```

---

## Background Server

### `hl server start`

Start the background caching server.

**Benefits:**

- Persistent WebSocket connections
- In-memory market data cache
- ~20-50x faster queries
- Sub-5ms latency

**Example:**

```bash
hl server start
```

### `hl server stop`

Stop the background server.

**Example:**

```bash
hl server stop
```

### `hl server status`

Check server status.

**Output includes:**

- Running state
- WebSocket connection status
- Uptime
- Cache statistics

**Example:**

```bash
hl server status
```

---

## Error Handling

Common errors and their meanings:

| Error                 | Cause                 | Solution                                |
| --------------------- | --------------------- | --------------------------------------- |
| `No default account`  | No account configured | Run `hl account add`                    |
| `Invalid private key` | Malformed private key | Ensure key starts with `0x`             |
| `Insufficient margin` | Not enough balance    | Reduce position size or add funds       |
| `Invalid asset`       | Unknown coin symbol   | Check `hl markets ls` for valid symbols |
| `Rate limited`        | Too many requests     | Start server with `hl server start`     |

---

## Exit Codes

| Code | Meaning       |
| ---- | ------------- |
| 0    | Success       |
| 1    | General error |

---

## Environment Variables

| Variable                     | Description                                                        |
| ---------------------------- | ------------------------------------------------------------------ |
| `HYPERLIQUID_PRIVATE_KEY`    | Private key for trading (required if not using account management) |
| `HYPERLIQUID_WALLET_ADDRESS` | Explicit wallet address (optional, derived from key)               |

---

## Local Storage

| Path                               | Description                                  |
| ---------------------------------- | -------------------------------------------- |
| `~/.hyperliquid/accounts.db`       | SQLite database for account management       |
| `~/.hyperliquid/order-config.json` | Order configuration (default slippage, etc.) |
| `~/.hyperliquid/server.pid`        | Background server PID file                   |
