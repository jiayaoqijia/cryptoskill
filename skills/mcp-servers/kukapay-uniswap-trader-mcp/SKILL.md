---
name: kukapay-uniswap-trader-mcp
description: "[![smithery badge](https://smithery.ai/badge/@kukapay/uniswap-trader-mcp)](https://smithery.ai/server/@kukapay/uniswap-trader-mcp)"
---

# kukapay-uniswap-trader-mcp

_Source: [github.com/kukapay/uniswap-trader-mcp](https://github.com/kukapay/uniswap-trader-mcp). The body below is the upstream README.md captured at the time of registration._

---

# Uniswap Trader MCP
[![smithery badge](https://smithery.ai/badge/@kukapay/uniswap-trader-mcp)](https://smithery.ai/server/@kukapay/uniswap-trader-mcp)

An MCP server for AI agents to automate token swaps on Uniswap DEX across multiple blockchains.

## Features
- **Price Quotes**: Get real-time price quotes for token swaps with multi-hop route optimization.
- **Swap Execution**: Execute swaps on Uniswap V3 with configurable slippage tolerance and deadlines.
- **Swap Suggestions**: Generate trading suggestions based on liquidity, fees, and optimal paths.
- **Multi-Chain Support**: Compatible with Ethereum, Optimism, Polygon, Arbitrum, Celo, BNB Chain, Avalanche, and Base.

## Prerequisites
- **Node.js**: Version 14.x or higher.
- **npm**: For package management.
- **Wallet**: A funded wallet with a private key for executing swaps.
- **RPC Endpoints**: Access to blockchain RPC URLs (e.g., Infura, Alchemy) for supported chains.

## Installation

### Installing via Smithery

To install Uniswap Trader MCP for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@kukapay/uniswap-trader-mcp):

```bash
npx -y @smithery/cli install @kukapay/uniswap-trader-mcp --client claude
```

### Manual Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/kukapay/uniswap-trader-mcp.git
   cd uniswap-trader-mcp
   ```

2. **Install Dependencies**:
   ```bash
   npm install
   ```

## Configuration

```json
{
  "mcpServers": {
    "Uniswap-Trader-MCP": {
      "command": "node",
      "args": ["path/to/uniswap-trader-mcp/server/index.js"],
      "env": {
        "INFURA_KEY": "your infura key",
        "WALLET_PRIVATE_KEY": "your private key"
      }
    }
  }
}
```
## Usage

### Supported Chains
The following blockchains are supported. Ensure each chain is configured in `chainConfigs.js` with a valid RPC URL, WETH address, and SwapRouter address.

| Chain ID | Name         | Notes                                      |
|----------|--------------|--------------------------------------------|
| 1        | Ethereum     | Mainnet, widely used for Uniswap trades   |
| 10       | Optimism     | Layer 2, requires Optimism RPC            |
| 137      | Polygon      | Fast and low-cost, uses MATIC as native   |
| 42161    | Arbitrum     | Layer 2, Arbitrum One network             |
| 42220    | Celo         | Mobile-first blockchain, uses CELO        |
| 56       | BNB Chain    | Binance Smart Chain, uses BNB             |
| 43114    | Avalanche    | High-throughput, uses AVAX                |
| 8453     | Base         | Coinbase’s Layer 2, built on Optimism     |


### Tools and Prompts

#### 1. `getPrice`
Fetches a price quote for a Uniswap swap.

**Schema**:
- `chainId`: Number (default: 1)
- `tokenIn`: String (e.g., `"NATIVE"` or token address)
- `tokenOut`: String (e.g., `"NATIVE"` or token address)
- `amountIn`: String (optional, required for `"exactIn"`)
- `amountOut`: String (optional, required for `"exactOut"`)
- `tradeType`: `"exactIn"` or `"exactOut"` (default: `"exactIn"`)

Example prompt:

```
Get me a price quote for swapping 1 ETH to DAI on Ethereum.
```

Output:

```
{
  "chainId": 1,
  "tradeType": "exactIn",
  "price": "3000.50",
  "inputAmount": "1.000000",
  "outputAmount": "3000.50",
  "minimumReceived": "2985.50",
  "maximumInput": "1.005000",
  "route": [
    {
      "tokenIn": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
      "tokenOut": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
      "fee": 3000
    }
  ],
  "estimatedGas": "150000"
}
```

#### 2. `executeSwap`
Executes a swap on Uniswap.

**Schema**:
- `chainId`: Number (default: 1)
- `tokenIn`: String
- `tokenOut`: String
- `amountIn`: String (optional, required for `"exactIn"`)
- `amountOut`: String (optional, required for `"exactOut"`)
- `tradeType`: `"exactIn"` or `"exactOut"` (default: `"exactIn"`)
- `slippageTolerance`: Number (default: 0.5, in percentage)
- `deadline`: Number (default: 20, in minutes)

Example prompt:

```
Swap 1 ETH for DAI on Ethereum with a 0.5% slippage tolerance and a 20-minute deadline.
```

Output:

```
{
  "chainId": 1,
  "txHash": "0x1234...abcd",
  "tradeType": "exactIn",
  "amountIn": "1.000000",
  "outputAmount": "2990.75",
  "minimumReceived": "2985.50",
  "maximumInput": "1.005000",
  "fromToken": "NATIVE",
  "toToken": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
  "route": [
    {
      "tokenIn": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
      "tokenOut": "0x6B175474E89094C44Da98b954EedeAC495271d0F",
      "fee": 3000
    }
  ],
  "gasUsed": "145000"
}
```

## License
MIT License. See [LICENSE](LICENSE) for details.
