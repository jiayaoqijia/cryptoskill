---
name: injective-official-mcp-server
description: "An [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that gives AI agents full trading capabilities on [Injective](https://injective.com) — perpetual futures, spot transfers, cross-chain bridging, and raw EVM transactions."
---

# injective-official-mcp-server

_Source: [github.com/InjectiveLabs/mcp-server](https://github.com/InjectiveLabs/mcp-server). The body below is the upstream README.md captured at the time of registration._

---

# Injective MCP Server

An [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that gives AI agents full trading capabilities on [Injective](https://injective.com) — perpetual futures, spot transfers, cross-chain bridging, and raw EVM transactions.

Connect it to Claude Desktop or Claude Code and trade with natural language.

---

## Tools

### Wallets
| Tool | Description |
|---|---|
| `wallet_generate` | Generate a new Injective wallet. Returns address + mnemonic (shown once). |
| `wallet_import` | Import a wallet from a hex private key. |
| `wallet_list` | List all wallets in the local keystore (addresses only — no keys). |
| `wallet_remove` | Permanently delete a wallet from the keystore. |

### Markets & Accounts
| Tool | Description |
|---|---|
| `market_list` | List all active perpetual futures markets. |
| `market_price` | Get the current oracle price for a market by symbol (e.g. `"BTC"`). |
| `account_balances` | Get bank + subaccount balances. Supports all token types. |
| `account_positions` | Get open perpetual positions with unrealized P&L. |
| `token_metadata` | Look up symbol, decimals, and type for any denom. |

### Perpetual Trading
| Tool | Description |
|---|---|
| `trade_open` | Open a position with a market order (Cosmos signing). |
| `trade_close` | Close an open position with a market order (Cosmos signing). |
| `trade_open_eip712` | Open a position using EIP-712 Ethereum signing (MetaMask-compatible keys). |
| `trade_close_eip712` | Close a position using EIP-712 Ethereum signing (MetaMask-compatible keys). |
| `trade_limit_open` | Open a limit order. |
| `trade_limit_orders` | List open limit orders. |
| `trade_limit_close` | Cancel a limit order by `orderHash`. |
| `trade_limit_states` | Query order states by order hash. |

### Transfers & Subaccounts
| Tool | Description |
|---|---|
| `transfer_send` | Send tokens to another Injective address. |
| `subaccount_deposit` | Deposit from bank balance into a trading subaccount. |
| `subaccount_withdraw` | Withdraw from a trading subaccount back to bank balance. |

### Bridging
| Tool | Description |
|---|---|
| `bridge_withdraw_to_eth` | Withdraw to Ethereum via the Peggy bridge (~30 min, fee applies). |
| `bridge_debridge_quote` | Get a deBridge DLN quote to any supported chain. Read-only. |
| `bridge_debridge_send` | Bridge tokens from Injective to another chain via deBridge DLN. |

### EVM
| Tool | Description |
|---|---|
| `evm_broadcast` | Broadcast a raw EVM transaction on Injective EVM. |

---

## Setup

```bash
npm install
npm run build
```

### Connect to Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "injective": {
      "command": "node",
      "args": ["/path/to/mcp-server/dist/mcp/server.js"],
      "env": {
        "INJECTIVE_NETWORK": "mainnet"
      }
    }
  }
}
```

### Connect to Claude Code

Add to `~/.claude/mcp.json` or your project's MCP config:

```json
{
  "mcpServers": {
    "injective": {
      "command": "node",
      "args": ["/path/to/mcp-server/dist/mcp/server.js"],
      "env": {
        "INJECTIVE_NETWORK": "mainnet"
      }
    }
  }
}
```

Set `INJECTIVE_NETWORK` to `"testnet"` to use the Injective testnet.

---

## Quickstart

Once connected, a typical session looks like:

```
> List all BTC and ETH perpetual markets
> What's the current price of BTC?
> Show my balances for inj1...
> Deposit 100 USDT into my trading subaccount
> Open a $50 long on BTC/USDT with 5x leverage
> Show my open positions
> Close my BTC position
```

For limit orders:

```
> Open a limit buy on ETH at $3200 for $100 notional, 3x leverage
> List my open limit orders
> Cancel order 0xabc...
```

For bridging:

```
> Get a deBridge quote to bridge 50 USDT from Injective to Base
> Bridge 50 USDT to 0x... on Base via deBridge
```

---

## Architecture

```
Claude (MCP client)
       │  tool calls over stdio
       ▼
MCP Server  (src/mcp/server.ts)
       │
       ├── config/       Network config (testnet / mainnet)
       ├── keystore/     AES-256-GCM encrypted key storage
       ├── wallets/      Wallet generation and management
       ├── markets/      Market data with in-memory caching
       ├── accounts/     Balances and positions
       ├── trading/      Perpetual market orders (Cosmos signing)
       ├── evm/eip712    Perpetual market orders (EIP-712 signing)
       ├── orders/       Perpetual limit order lifecycle
       ├── transfers/    Bank transfers and subaccount moves
       ├── bridges/      Peggy + deBridge cross-chain
       └── evm/          Generic Injective EVM tx broadcasting
              │
              ▼
     Injective Chain
     @injectivelabs/sdk-ts
```

---

## Security

- Private keys are **never stored in plaintext** — AES-256-GCM + scrypt at rest
- Keys live in `~/.injective-agent/keys/` with `0600` permissions
- Claude never sees raw private keys — only addresses and tx hashes
- Wallet passwords are passed as tool parameters and **may appear in MCP client logs** — avoid reusing passwords from other services

See [SECURITY.md](./SECURITY.md) for the full security model.

---

## Development

```bash
npm test                   # unit tests (no network required)
npm run test:integration   # integration tests against testnet
npm run typecheck          # TypeScript type check
```

---

## Token Support

All Injective denom formats are supported:

| Type | Format | Example |
|---|---|---|
| Native | `inj` | INJ |
| Peggy (bridged ERC-20) | `peggy0x...` | USDT |
| IBC | `ibc/...` | ATOM |
| TokenFactory | `factory/inj.../name` | — |
| MTS / Injective EVM ERC-20 | `erc20:0x...` | Injective EVM tokens |

Token metadata (symbol, decimals) is resolved automatically against on-chain registry and cached for the lifetime of the server process.

---

## Networks

| Network | `INJECTIVE_NETWORK` |
|---|---|
| Mainnet | `mainnet` |
| Testnet | `testnet` |

Testnet faucet: https://testnet.faucet.injective.network/
