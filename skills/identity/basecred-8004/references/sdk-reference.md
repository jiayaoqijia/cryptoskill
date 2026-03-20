# Agent0 SDK Reference (v1.5.2)

## Installation
```bash
npm install agent0-sdk@1.5.2
```

## SDK Initialization
```js
import { SDK } from 'agent0-sdk';

const sdk = new SDK({
  chainId: 1,                    // Required: 1, 137, 56
  rpcUrl: 'https://...',         // Optional: custom RPC
  privateKey: '0x...',           // Required for write operations
  ipfs: 'pinata',               // 'pinata' | 'filecoinPin' | 'node'
  pinataJwt: '...',              // Required if ipfs='pinata'
});
```

## Core Methods

### Create Agent
```js
const agent = sdk.createAgent(name, description, image);
```

### Register Agent
```js
// IPFS-based registration
const result = await agent.registerIPFS();

// HTTP-based registration
const result = await agent.registerHTTP(url);
```

### Load Existing Agent
```js
const agent = await sdk.loadAgent('chainId:agentId'); // e.g. '1:42'
```

### Search Agents
```js
const results = await sdk.searchAgents(
  { name: '...', active: true, skills: [...], tools: [...] },
  { chainId: 1 }
);
```

### Give Feedback
```js
await sdk.giveFeedback(agentId, value, tag1, tag2, endpoint, feedbackFile);
// value: 1-5
```

## Agent Properties
- `agent.name` — Agent name
- `agent.description` — Agent description
- `agent.image` — Image URL
- `agent.a2aUrl` — A2A endpoint
- `agent.mcpUrl` — MCP endpoint

## OASF Taxonomies
Skills and domains follow OASF taxonomy standards for interoperability.
