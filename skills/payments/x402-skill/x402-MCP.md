# 🔌 x402 MCP Server Integration

> **Bridge paid APIs to Claude Desktop and MCP-compatible clients using the x402 payment protocol**

Model Context Protocol (MCP) is a protocol for passing context between LLMs and AI agents. This guide shows how to integrate x402 payment capabilities with MCP servers, enabling Claude Desktop and other MCP clients to autonomously discover and pay for API services.

---

## 📖 Table of Contents

- [What is this Integration?](#what-is-this-integration)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Implementation](#implementation)
- [How It Works](#how-it-works)
- [Multi-Network Support](#multi-network-support)
- [Response Handling](#response-handling)
- [Architecture](#architecture)
- [Dependencies](#dependencies)
- [Examples](#examples)

---

## What is this Integration?

This guide walks you through running an **MCP server** that can access paid APIs using the x402 protocol. The MCP server acts as a bridge between Claude Desktop (or any MCP-compatible client) and paid APIs discovered through the x402 Bazaar.

When Claude (or another agent) calls a tool, the MCP server will:

1. **Detect** if the API requires payment (via HTTP 402 with `PAYMENT-REQUIRED` header)
2. **Parse** payment requirements from the response
3. **Execute** payment using your wallet via the registered x402 scheme
4. **Retry** the request with payment proof
5. **Return** the paid data to the client (e.g., Claude)

This lets you (or your agent) access paid APIs programmatically, with **no manual payment steps**.

---

## Prerequisites

- **Node.js v20+** (install via [nvm](https://github.com/nvm-sh/nvm))
- **pnpm v10+** (install via [pnpm.io/installation](https://pnpm.io/installation))
- An x402-compatible server to connect to (sample weather API or any x402 Bazaar service)
- **Ethereum wallet with USDC** (on Base Sepolia or Base Mainnet) and/or
- **Solana wallet with USDC** (on Devnet or Mainnet)
- **Claude Desktop** with MCP support

---

## Quick Start

### 1. Install and Build

```bash
# Clone the x402 repository
git clone https://github.com/coinbase/x402.git
cd x402/examples/typescript

# Install dependencies and build packages
pnpm install && pnpm build

# Navigate to the MCP client example
cd clients/mcp
```

### 2. Configure Claude Desktop

Add the MCP server to your Claude Desktop configuration file:

**macOS/Linux:** `~/.config/claude/claude_desktop_config.json`  
**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "x402-bazaar": {
      "command": "pnpm",
      "args": [
        "--silent",
        "-C",
        "<absolute path to x402 repo>/examples/typescript/clients/mcp",
        "dev"
      ],
      "env": {
        "EVM_PRIVATE_KEY": "<private key of wallet with USDC on Base Sepolia>",
        "SVM_PRIVATE_KEY": "<base58-encoded private key of Solana wallet with USDC>",
        "RESOURCE_SERVER_URL": "http://localhost:4021",
        "ENDPOINT_PATH": "/weather"
      }
    }
  }
}
```

### 3. Start an x402 Server

Make sure your x402-compatible server is running at the URL specified in `RESOURCE_SERVER_URL`:

```bash
# In another terminal, from the examples/typescript directory
cd servers/express
pnpm dev
```

This starts the sample weather API server at `http://localhost:4021`

### 4. Restart Claude Desktop

Restart Claude Desktop to load the new MCP server, then ask:

> "Use the get-data-from-resource-server tool to get weather data"

Claude will automatically handle the payment and return the weather data!

---

## Implementation

The MCP server uses `@x402/axios` to wrap axios with automatic payment handling:

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import axios from "axios";
import { x402Client, wrapAxiosWithPayment } from "@x402/axios";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { ExactSvmScheme } from "@x402/svm/exact/client";
import { privateKeyToAccount } from "viem/accounts";
import { createKeyPairSignerFromBytes } from "@solana/kit";
import { base58 } from "@scure/base";
import { config } from "dotenv";

config();

const evmPrivateKey = process.env.EVM_PRIVATE_KEY as `0x${string}`;
const svmPrivateKey = process.env.SVM_PRIVATE_KEY as string;
const baseURL = process.env.RESOURCE_SERVER_URL || "http://localhost:4021";
const endpointPath = process.env.ENDPOINT_PATH || "/weather";

if (!evmPrivateKey && !svmPrivateKey) {
  throw new Error("At least one of EVM_PRIVATE_KEY or SVM_PRIVATE_KEY must be provided");
}

/**
 * Creates an axios client configured with x402 payment support for EVM and/or SVM.
 */
async function createClient() {
  const client = new x402Client();

  // Register EVM scheme if private key is provided
  if (evmPrivateKey) {
    const evmSigner = privateKeyToAccount(evmPrivateKey);
    client.register("eip155:*", new ExactEvmScheme(evmSigner));
  }

  // Register SVM scheme if private key is provided
  if (svmPrivateKey) {
    const svmSigner = await createKeyPairSignerFromBytes(base58.decode(svmPrivateKey));
    client.register("solana:*", new ExactSvmScheme(svmSigner));
  }

  return wrapAxiosWithPayment(axios.create({ baseURL }), client);
}

async function main() {
  const api = await createClient();

  // Create an MCP server
  const server = new McpServer({
    name: "x402 MCP Client Demo",
    version: "2.0.0",
  });

  // Add a tool that calls the paid API
  server.tool(
    "get-data-from-resource-server",
    "Get data from the resource server (in this example, the weather)",
    {},
    async () => {
      const res = await api.get(endpointPath);
      return {
        content: [{ type: "text", text: JSON.stringify(res.data) }],
      };
    },
  );

  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(error => {
  console.error(error);
  process.exit(1);
});
```

---

## How It Works

The MCP server exposes a tool that, when called, fetches data from a paid API endpoint. If the endpoint requires payment, the x402 axios wrapper automatically handles the payment handshake:

### Payment Flow

1. **402 Response:** The server returns HTTP 402 with `PAYMENT-REQUIRED` header
2. **Parse Requirements:** The wrapper extracts payment requirements from the header
3. **Create Payment:** Uses the registered scheme (EVM or SVM) to create a payment payload
4. **Retry Request:** Sends the original request with the `PAYMENT-SIGNATURE` header
5. **Return Data:** Once payment is verified, the data is returned to Claude

### v2 API Response Shape

The x402 v2 API returns discovery responses in this format:

```json
{
  "x402Version": 2,
  "items": [
    {
      "url": "https://api.example.com/weather",
      "type": "http",
      "accepts": [
        {
          "network": "eip155:8453",
          "token": "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",
          "maxAmountRequired": "1000"
        }
      ]
    }
  ],
  "pagination": {
    "nextCursor": "abc123",
    "hasMore": true
  }
}
```

**Key differences from v1:**
- Wrapped response with `x402Version` and `items` (not flat list)
- Uses `maxAmountRequired` instead of `amount`
- MCP tool uniqueness is `(resource_url, tool_name)` not just URL
- Supports `bazaarResourceServerExtension` and `declareDiscoveryExtension()`

---

## Multi-Network Support

The example supports both **EVM** (Base, Ethereum) and **Solana** networks. The x402 client automatically selects the appropriate scheme based on the payment requirements:

```typescript
import { x402Client, wrapAxiosWithPayment } from "@x402/axios";
import { ExactEvmScheme } from "@x402/evm/exact/client";
import { ExactSvmScheme } from "@x402/svm/exact/client";

const client = new x402Client();

// Register EVM scheme for Base/Ethereum payments
client.register("eip155:*", new ExactEvmScheme(evmSigner));

// Register SVM scheme for Solana payments
client.register("solana:*", new ExactSvmScheme(svmSigner));

// Now handles both EVM and Solana networks automatically
const httpClient = wrapAxiosWithPayment(axios.create({ baseURL }), client);
```

When the server returns a 402 response, the client checks the `network` field in the payment requirements:

- `eip155:*` networks use the **EVM scheme**
- `solana:*` networks use the **SVM scheme**

---

## Response Handling

### Payment Required (402)

When a payment is required, the client receives:

```http
HTTP/1.1 402 Payment Required
PAYMENT-REQUIRED: <base64-encoded JSON>
```

The wrapper automatically:
1. Parses the payment requirements
2. Creates and signs a payment using the appropriate scheme
3. Retries the request with the `PAYMENT-SIGNATURE` header

### Successful Response

After payment is processed, the MCP server returns:

```json
{
  "content": [
    {
      "type": "text",
      "text": "{\"report\":{\"weather\":\"sunny\",\"temperature\":70}}"
    }
  ]
}
```

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Claude Desktop │────▶│   MCP Server    │────▶│  x402 API       │
│                 │     │  (x402 client)  │     │  (paid endpoint)│
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        │  1. Call tool         │  2. GET /weather      │
        │                       │                       │
        │                       │  3. 402 + requirements│
        │                       │◀──────────────────────│
        │                       │                       │
        │                       │  4. Sign payment      │
        │                       │                       │
        │                       │  5. Retry with payment│
        │                       │──────────────────────▶│
        │                       │                       │
        │                       │  6. 200 + data        │
        │                       │◀──────────────────────│
        │                       │                       │
        │  7. Return response   │                       │
        │◀──────────────────────│                       │
```

### How the Pieces Fit Together

1. **x402-compatible server:** Hosts the paid API (e.g., weather data). Responds with HTTP 402 and `PAYMENT-REQUIRED` header if payment is required.

2. **MCP server (this implementation):** Acts as a bridge, handling payment via `@x402/axios` and exposing tools to MCP clients.

3. **Claude Desktop:** Calls the MCP tool, receives the paid data, and displays it to the user.

---

## Dependencies

The example uses these x402 v2 packages:

```json
{
  "dependencies": {
    "@modelcontextprotocol/sdk": "^1.9.0",
    "@x402/axios": "workspace:*",
    "@x402/evm": "workspace:*",
    "@x402/svm": "workspace:*",
    "axios": "^1.13.2",
    "viem": "^2.39.0",
    "@solana/kit": "^2.1.1",
    "@scure/base": "^1.2.6",
    "dotenv": "^16.0.0"
  }
}
```

---

## Examples

### Example 1: Weather Data via MCP

**Ask Claude:**
> "Get the weather using the x402 tool"

**What happens:**
1. Claude calls `get-data-from-resource-server` tool
2. MCP server makes GET request to `/weather`
3. Server returns 402 with payment requirements
4. MCP server pays 0.001 USDC on Base
5. Server returns weather data
6. Claude displays: *"The weather is sunny with a temperature of 70°F"*

### Example 2: Multiple Services

You can configure multiple x402 services in Claude Desktop:

```json
{
  "mcpServers": {
    "x402-weather": {
      "command": "node",
      "args": ["mcp-server.js"],
      "env": {
        "RESOURCE_SERVER_URL": "https://api.weather-x402.com",
        "ENDPOINT_PATH": "/current",
        "EVM_PRIVATE_KEY": "0x..."
      }
    },
    "x402-sentiment": {
      "command": "node",
      "args": ["mcp-server.js"],
      "env": {
        "RESOURCE_SERVER_URL": "https://api.sentiment-x402.com",
        "ENDPOINT_PATH": "/analyze",
        "EVM_PRIVATE_KEY": "0x..."
      }
    }
  }
}
```

Now Claude can autonomously choose which service to use!

### Example 3: Solana Network

Use Solana USDC instead of Base:

```json
{
  "env": {
    "SVM_PRIVATE_KEY": "base58-encoded-private-key",
    "RESOURCE_SERVER_URL": "https://api.x402network.com",
    "ENDPOINT_PATH": "/llm/llama"
  }
}
```

The MCP server automatically detects the `solana:*` network and uses the SVM scheme.

---

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `EVM_PRIVATE_KEY` | Your EVM wallet's private key (0x prefixed) | One of EVM or SVM required |
| `SVM_PRIVATE_KEY` | Your Solana wallet's private key (base58 encoded) | One of EVM or SVM required |
| `RESOURCE_SERVER_URL` | The base URL of the paid API | Yes |
| `ENDPOINT_PATH` | The specific endpoint path (e.g., `/weather`) | Yes |

---

## Setup for OpenClaw Integration

If you're using this with the OpenClaw x402 Bazaar skill:

```bash
# Copy skill to clawd skills directory
cp -r . ~/.openclaw/skills/x402-bazaar/

# Copy and configure environment
cp ~/.openclaw/skills/x402-bazaar/.env.example ~/.openclaw/skills/x402-bazaar/.env

# Edit .env - add EVM_PRIVATE_KEY only if you want to make paid calls
nano ~/.openclaw/skills/x402-bazaar/.env
```

**Note:** Browse-only mode (service discovery) requires **no private keys at all**!

---

## Troubleshooting

### MCP Server Not Showing in Claude

1. Check Claude Desktop config file location
2. Ensure absolute paths are used (not `~` or relative)
3. Restart Claude Desktop completely (quit, not just close window)
4. Check Claude Desktop logs: Help → Developer Tools → Console

### Payment Failing

1. Verify wallet has sufficient USDC balance
2. Check network matches (Base Sepolia vs Mainnet)
3. Ensure private key is correctly formatted:
   - EVM: `0x` prefix, 64 hex characters
   - Solana: base58-encoded, no prefix

### Connection Refused

1. Ensure x402 server is running (`pnpm dev`)
2. Check `RESOURCE_SERVER_URL` is correct
3. Verify port is not blocked by firewall

---

## Resources

- [x402 GitHub Repository](https://github.com/coinbase/x402)
- [x402 Protocol Documentation](https://docs.cdp.coinbase.com/x402)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io)
- [Claude Desktop MCP Guide](https://docs.anthropic.com/claude/docs/model-context-protocol)
- [Base Network](https://base.org)

---

## Next Steps

1. **Explore the Bazaar:** Use the Python skill to discover available x402 services
2. **Create MCP tools:** Expose multiple x402 services through different MCP tools
3. **Automate workflows:** Chain multiple paid API calls together
4. **Build your own:** Create x402-compatible APIs and list them on the Bazaar

---

<div align="center">

**Made with ❤️ by the OpenClaw & x402 Communities**

[← Back to Main README](README.md) • [View on GitHub](https://github.com/coinvest518/openclaw-x402-skill)

</div>
