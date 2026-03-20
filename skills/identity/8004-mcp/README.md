# @quantulabs/8004-mcp

Multi-chain MCP server for the ERC-8004 Agent Registry Standard. Supports Solana and EVM chains (Ethereum, Base, Arbitrum, Polygon, Optimism).

## Requirements

- Node.js >= 20.0.0
- npm or pnpm

## Installation

```bash
npm install -g @quantulabs/8004-mcp
```

Or run directly without installing:

```bash
npx @quantulabs/8004-mcp
```

## Features

- **Multi-chain**: Solana + EVM (Base, Ethereum, Arbitrum, Polygon, Optimism)
- **Unified API**: Same tools work across chains with automatic routing
- **Wallet Management**: Encrypted local storage with auto-lock
- **Local Cache**: SQLite with FTS5 for fast agent search
- **ATOM Reputation**: Full integration with Solana's reputation system
- **IPFS Support**: Pinata, Filecoin, or custom node

## Configuration

The MCP automatically loads a `.env` file from the current directory.

```bash
cp .env.example .env
# Edit .env with your values
npx @quantulabs/8004-mcp
```

See [.env.example](./.env.example) for all available options.

## Usage with Claude Code

### Quick Start

```bash
claude mcp add 8004 npx @quantulabs/8004-mcp
```

Works on **Windows, Mac, and Linux**. No `cmd /c` or `--` needed.

With environment variables:

```bash
claude mcp add 8004 -e DEFAULT_CHAIN=sol -e NETWORK_MODE=testnet npx @quantulabs/8004-mcp
```

### Manual Configuration

Edit `~/.claude.json` (or `%USERPROFILE%\.claude.json` on Windows):

```json
{
  "mcpServers": {
    "8004": {
      "command": "npx",
      "args": ["@quantulabs/8004-mcp"],
      "env": {
        "DEFAULT_CHAIN": "sol",
        "NETWORK_MODE": "testnet"
      }
    }
  }
}
```

### Examples

#### Multi-chain agent search

Search across all blockchains without specifying a chain:

```
> Find the agent named "DataAnalyst Pro"

Found 2 agents named "DataAnalyst Pro" on Ethereum Sepolia:
- eth:11155111:461 - Owner: 0xfb49...
- eth:11155111:460 - Owner: 0x6fd8...
```

```
> Search for agents with "Yoda" in the name

Found 4 agents:
- eth:11155111:523 - "Yoda 27 Jan"
- eth:11155111:468 - "Yoda 3"
- eth:11155111:467 - "Yoda Dash 1"
- eth:11155111:465 - "Yoda PG 2 IPFS"
All owned by 0xad55...
```

#### Get agent details

```
> Show me details about agent eth:11155111:474

Agent: 8004 Test Agent
- Chain: Ethereum Sepolia
- Owner: 0x9ca4...
- Description: This is an explanation of my test agent
- Created: 2026-01-27
```

#### Check agent reputation (Solana only)

> Note: Trust tiers and ATOM reputation metrics are only available on Solana.

```
> What's the reputation of sol:6YMAwDYygQEo1BGDavNaKhhfy52yzZ6SoBsa2wdgXthJ?

Trust Tier: Unrated (0/4)
Quality Score: 2440
Total Feedbacks: 29
Average Score: 24.4
```

#### Top agents leaderboard (Solana only)

```
> Show me the top 5 agents by reputation

Top 5 Solana agents:
1. sol:9j7cTX... - Score: 5586 (34 feedbacks)
2. sol:5heKjG... - Score: 5544 (35 feedbacks)
3. sol:HnGRPf... - Score: 3364 (50 feedbacks)
4. sol:6YMAwD... - Score: 2440 (30 feedbacks)
5. sol:Arskmk... - Score: 2440 (30 feedbacks)
```

#### Submit feedback

```
> Give a score of 90 to agent sol:7xKXtG8vN2... with comment "Fast execution"

First I need to unlock a wallet...
Feedback submitted! Transaction: 4xR7m...
```

#### Register a new agent

```
> Register a new agent called "MyBot" with MCP endpoint https://mybot.com/mcp

1. Uploading registration to IPFS...
2. Registering on-chain...

Agent registered!
- ID: sol:NewAgentPubkey...
- Name: MyBot
- Transaction: 5tY8n...
```

#### Manage wallets

```
> Create a new Solana wallet called "trading-wallet"

Wallet created:
- Name: trading-wallet
- Address: 8xM2k...
- Chain: Solana

Fund this address to start using it for transactions.
```

#### Switch networks

```
> Switch to mainnet

Using network_set with mode "mainnet"...

Switched to mainnet. Active chains:
- Solana: mainnet-beta
- Base: mainnet (chainId: 8453)
- Ethereum: mainnet (chainId: 1)
```

## Cost Reference

Use `estimateCost: true` with `agent_register` to get real-time prices.

### Solana (SOL @ $150)

| Operation | Cost Range | USD |
|-----------|------------|-----|
| `agent_register` | 0.008-0.01 SOL | ~$1.20-1.50 |
| `feedback_give` | 0.0001-0.0005 SOL | ~$0.02-0.08 |
| `feedback_response_append` | 0.0001-0.0005 SOL | ~$0.02-0.08 |
| `agent_uri_update` | 0.00005 SOL | ~$0.01 |

### EVM - Base L2 (Recommended)

| Operation | Gas | @ 0.01 gwei | @ 1 gwei |
|-----------|-----|-------------|----------|
| `agent_register` | 150-200k | ~$0.005-0.006 | ~$0.45-0.60 |
| `feedback_give` | 100k | ~$0.003 | ~$0.30 |
| `feedback_response_append` | 60k | ~$0.002 | ~$0.18 |
| `agent_uri_update` | 50k | ~$0.002 | ~$0.15 |

### EVM - Ethereum Mainnet

| Operation | Gas | @ 25 gwei | @ 50 gwei |
|-----------|-----|-----------|-----------|
| `agent_register` | 150-200k | ~$11-15 | ~$22-30 |
| `feedback_give` | 100k | ~$7.50 | ~$15 |
| `feedback_response_append` | 60k | ~$4.50 | ~$9 |
| `agent_uri_update` | 50k | ~$3.75 | ~$7.50 |

**Tip:** Use L2 chains (Base, Arbitrum, Optimism) for 10-100x lower costs than Ethereum mainnet.

## Usage for Autonomous Agents

For programmatic access from autonomous agents, AI frameworks, or custom applications:

### Quick Start

```javascript
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { spawn } from 'child_process';

// Start the MCP server
const server = spawn('npx', ['@quantulabs/8004-mcp'], {
  stdio: ['pipe', 'pipe', 'inherit'],
  env: { ...process.env, NETWORK_MODE: 'testnet' },
});

const transport = new StdioClientTransport({
  reader: server.stdout,
  writer: server.stdin,
});

const client = new Client(
  { name: 'my-agent', version: '1.0.0' },
  { capabilities: {} }
);

await client.connect(transport);

// List available tools
const tools = await client.listTools();
console.log(`${tools.tools.length} tools available`);

// Search agents
const result = await client.callTool({
  name: 'agent_search',
  arguments: { chain: 'eth', limit: 5 }
});
console.log(result.content[0].text);

// Get agent details
const agent = await client.callTool({
  name: 'agent_get',
  arguments: { id: 'eth:11155111:738' }
});
console.log(agent.content[0].text);
```

### Testing Without Funds (Dry Run)

Use `skipSend: true` to get unsigned transactions without broadcasting:

```javascript
// Create a wallet first
await client.callTool({
  name: 'wallet_create',
  arguments: {
    name: 'test-wallet',
    chainType: 'solana',
    password: 'my-secure-password'
  }
});

// Register agent (dry run - returns unsigned tx)
const result = await client.callTool({
  name: 'agent_register',
  arguments: {
    name: 'My Test Agent',
    description: 'A test agent',
    chain: 'sol',
    skipSend: true  // Returns unsigned tx, no funds needed
  }
});
// Returns: { unsigned: true, transaction: "base64...", message: "..." }

// Give feedback (dry run)
const feedback = await client.callTool({
  name: 'feedback_give',
  arguments: {
    id: 'sol:AgentPubkey...',
    value: 85,
    tag1: 'uptime',
    tag2: 'day',
    skipSend: true
  }
});
```

### Dependencies

```bash
npm install @modelcontextprotocol/sdk
```

## Documentation

- [TOOLS.md](./TOOLS.md) - Complete tool reference (86+ tools)
- [skill.md](./skill.md) - AI agent integration guide (search tips, workflows, write ops)

## Global ID Format

Agents are identified using global IDs that include chain info:

| Chain | Format | Example |
|-------|--------|---------|
| Solana | `sol:<pubkey>` | `sol:7xKXtG8vN2mPQr...` |
| Ethereum | `eth:<chainId>:<tokenId>` | `eth:11155111:738` (Sepolia) |
| Base | `base:<chainId>:<tokenId>` | `base:84532:42` (Sepolia) |
| Arbitrum | `arb:<chainId>:<tokenId>` | `arb:421614:123` |
| Polygon | `poly:<chainId>:<tokenId>` | `poly:80002:456` |
| Optimism | `op:<chainId>:<tokenId>` | `op:11155420:789` |

**Note:** When using `agent_get`, you can pass either:
- Full globalId: `eth:11155111:738`
- Raw tokenId with chain param: `{ id: "738", chain: "eth" }`

## x402 Protocol Integration

The MCP supports the x402 payment protocol extension for reputation (`8004-reputation`). This allows linking feedback to actual payment transactions, creating verifiable proof-of-payment reputation.

### How it works

1. **Server announces identity**: When returning 402 Payment Required, include agent identity in CAIP-2 format
2. **Client pays**: Standard x402 payment flow
3. **Feedback with proof**: Both parties can submit feedback linked to the payment transaction

### Example: Connecting to 8004-mcp

```javascript
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { spawn } from 'child_process';

// Start the MCP server
const server = spawn('npx', ['@quantulabs/8004-mcp'], {
  stdio: ['pipe', 'pipe', 'inherit'],
});

const transport = new StdioClientTransport({
  reader: server.stdout,
  writer: server.stdin,
});

const mcpClient = new Client(
  { name: 'my-app', version: '1.0.0' },
  { capabilities: {} }
);

await mcpClient.connect(transport);
```

### Example: Server-side (announcing identity)

```javascript
// Build identity for PaymentRequired response
const result = await mcpClient.callTool({
  name: 'x402_identity_build',
  arguments: { agentId: 'sol:AgentPubkey...' }
});

const identity = JSON.parse(result.content[0].text);
// Returns: { identity: { agentRegistry: "solana:EtWTRA...:HHCVWc...", agentId: "..." } }

// Add to PaymentRequired headers
const paymentRequired = {
  ...standardX402Fields,
  extensions: {
    '8004-reputation': identity.identity
  }
};
```

### Example: Client-side (submitting feedback)

```javascript
// After receiving PaymentResponse, parse the proof
const proofResult = await mcpClient.callTool({
  name: 'x402_proof_parse',
  arguments: { paymentResponse: base64EncodedPaymentResponse }
});

const proof = JSON.parse(proofResult.content[0].text);

// Option A: Auto-store on IPFS (requires ipfs_configure first)
await mcpClient.callTool({
  name: 'x402_feedback_submit',
  arguments: {
    agentId: 'sol:AgentPubkey...',
    score: 85,
    tag1: 'x402-resource-delivered',
    tag2: 'exact-svm',
    endpoint: 'https://agent.example.com/api',
    proofOfPayment: proof.proofOfPayment,
    storeOnIpfs: true
  }
});

// Option B: Manual storage - build file first, store yourself
const buildResult = await mcpClient.callTool({
  name: 'x402_feedback_build',
  arguments: {
    agentId: 'base:84532:123',
    score: 90,
    tag1: 'x402-resource-delivered',
    proofOfPayment: proof.proofOfPayment
  }
});
// Store buildResult.feedbackFile on Arweave, your IPFS, etc.
const myUri = 'ar://abc123...';

// Then submit with your URI
await mcpClient.callTool({
  name: 'x402_feedback_submit',
  arguments: {
    agentId: 'base:84532:123',
    score: 90,
    tag1: 'x402-resource-delivered',
    proofOfPayment: proof.proofOfPayment,
    feedbackUri: myUri,
    storeOnIpfs: false
  }
});
```

### Feedback File Storage

Feedback files **must** be stored for the x402 protocol. Two options:

1. **Auto IPFS** (`storeOnIpfs: true`): Configure IPFS first with `ipfs_configure`, then feedback is automatically stored
2. **Manual storage** (`feedbackUri`): Use `x402_feedback_build` to get the file, store it yourself (Arweave, your IPFS, HTTP), then pass the URI

Supported URI schemes: `ipfs://`, `ar://`, `https://`, `http://`

Example feedback file structure:

```json
{
  "agentRegistry": "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1:HHCVWcqs...",
  "agentId": "AgentPubkey...",
  "clientAddress": "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1:ClientPubkey...",
  "createdAt": "2026-01-23T12:00:00Z",
  "score": 85,
  "tag1": "x402-resource-delivered",
  "tag2": "exact-svm",
  "endpoint": "https://agent.example.com/api",
  "proofOfPayment": {
    "fromAddress": "ClientPubkey...",
    "toAddress": "AgentPubkey...",
    "chainId": "EtWTRABZaYq6iMfeYKouRu166VU2xqa1",
    "txHash": "5xR7mN2k..."
  }
}
```

See [TOOLS.md](./TOOLS.md#x402-protocol-integration) for more details on x402 tools.

## Troubleshooting

### Windows: "Failed to connect" or `cmd C:/` error

If you see `cmd C:/` instead of `cmd /c`, the command was parsed incorrectly.

**Wrong** (causes Windows parsing bug):
```bash
claude mcp add 8004 -- cmd /c npx @quantulabs/8004-mcp
```

**Correct**:
```bash
claude mcp add 8004 npx @quantulabs/8004-mcp
```

### Server not starting

1. Check logs: `claude mcp logs 8004`
2. Verify installation: `npx @quantulabs/8004-mcp --help`
3. Restart Claude Code after adding the server

## Development

```bash
git clone https://github.com/QuantuLabs/8004-mcp.git
cd 8004-mcp
npm install
npm run build
npm test
```

## Adding Your Registry

> **Note:** Registries supported by the [8004-solana SDK](https://github.com/QuantuLabs/8004-solana) and [agent0-ts SDK](https://github.com/agent0lab/agent0-ts) are automatically included in this MCP. No action needed for those chains.

Want to add your own ERC-8004 compatible registry to the MCP? [Open an issue on GitHub](https://github.com/QuantuLabs/8004-mcp/issues/new?template=registry-request.md) with the following requirements:

### Requirements

1. **Open Source**: Your registry must be public and open source
   - Provide link to your GitHub repository

2. **Indexer**: Provide an open source indexer or equivalent data access method
   - We need a way to query agents efficiently
   - Subgraph, REST API, or RPC-based indexing supported

3. **Documentation**: Complete API documentation including:
   - All contract methods and events
   - Data structures and types
   - Example requests/responses

4. **API Compatibility**: We recommend following the [8004-solana SDK](https://github.com/QuantuLabs/8004-solana) API patterns:
   - `getAgent(id)` - Get agent details
   - `agentExists(id)` - Check existence
   - `searchAgents(params)` - Search with filters
   - `giveFeedback(input)` - Submit feedback
   - `getFeedback(agentId, client, index)` - Read feedback
   - `listFeedbacks(query)` - List feedbacks
   - `getReputationSummary(id)` - Get reputation

## License

MIT
