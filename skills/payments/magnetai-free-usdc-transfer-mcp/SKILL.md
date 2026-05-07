---
name: magnetai-free-usdc-transfer-mcp
description: "An MCP server implementation enabling free USDC transfers on **[Base](https://base.org)** with **[Coinbase CDP](https://docs.cdp.coinbase.com/)** MPC Wallet integration."
---

# magnetai-free-usdc-transfer-mcp

_Source: [github.com/magnetai/mcp-free-usdc-transfer](https://github.com/magnetai/mcp-free-usdc-transfer). The body below is the upstream README.md captured at the time of registration._

---

# Free USDC Transfer MCP Server

An MCP server implementation enabling free USDC transfers on **[Base](https://base.org)** with **[Coinbase CDP](https://docs.cdp.coinbase.com/)** MPC Wallet integration.

<img width="1374" alt="image" src="https://github.com/user-attachments/assets/3a58a720-8489-4f02-9075-19c8f264e3cc" />

## Features

- Free USDC Transfers: Send USDC to any address or ENS/BaseName domain on Base - no fees, just simple transfers
- Coinbase MPC Wallet: Create and manage your Coinbase MPC wallet for secure, feeless transactions
- Name Resolution: Automatic support for **ENS** and **BaseName** domains

## Functions

### `tranfer-usdc`
- Description: Analyze the value of the purchased items and transfer USDC to the recipient via the Base chain. Due to the uncertainty of blockchain transaction times, the transaction is only scheduled here and will not wait for the transaction to be completed.
- Inputs:
    - usdc_amount (number): USDC amount, greater than 0.
    - recipient (string): Recipient's on-chain address or ENS domain (e.g., example.eth).
- Behavior:
    - Verifies the recipient's address or resolves ENS domains.
    - Schedules a USDC transfer on the Base chain.
    - Provides a link to view transaction details on BaseScan.

### `create_coinbase_mpc_wallet`
- Description: Create a Coinbase MPC wallet address.
- Behavior:
    - Creates a new Coinbase MPC wallet and saves the seed to a secure file.
    - If a wallet already exists, returns the existing wallet address.
    - The seed file for Coinbase MPC wallets is stored in the Documents directory under the file name mpc_info.json.

## Configuration

### Getting an API Key
1. Sign up for a [Coinbase CDP account](https://portal.cdp.coinbase.com/)
2. Generate your API key from the developer dashboard

### Usage with Claude Desktop

1. Add this to your `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "free-usdc-transfer": {
      "command": "npx",
      "args": [
        "-y",
        "@magnetai/free-usdc-transfer"
      ],
      "env": {
        "COINBASE_CDP_API_KEY_NAME": "YOUR_COINBASE_CDP_API_KEY_NAME",
        "COINBASE_CDP_PRIVATE_KEY": "YOUR_COINBASE_CDP_PRIVATE_KEY"
      }
    }
  }
}
```

2. Or install the server with **[magnet-desktop](https://github.com/magnetai/magnet-desktop)**

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.

---

Crafted by [Magnet Labs](https://magnetlabs.xyz) with our vibrant AI & Crypto community
