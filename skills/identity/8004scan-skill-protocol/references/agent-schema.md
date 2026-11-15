# Agent Schema — Registration File & Data Structures

## Registration File

The `agentURI` on the Identity Registry resolves to a JSON registration file. This is the primary metadata document describing an agent.

```json
{
  "name": "My Agent",
  "description": "A detailed description of what this agent does",
  "image": "ipfs://Qm.../avatar.png",
  "active": true,
  "services": [
    { "name": "MCP", "endpoint": "https://agent.example.com/mcp", "version": "2025-06-18" },
    { "name": "A2A", "endpoint": "https://agent.example.com/a2a", "version": "0.3.0" },
    { "name": "OASF", "endpoint": "https://agent.example.com/oasf", "skills": ["code-review"], "domains": ["software-engineering"] },
    { "name": "agentWallet", "endpoint": "eip155:8453:0x1234567890123456789012345678901234567890" },
    { "name": "ENS", "endpoint": "myagent.eth" },
    { "name": "DID", "endpoint": "did:example:123" }
  ],
  "registrations": [
    {
      "agentRegistry": "eip155:8453:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432",
      "agentId": 17
    }
  ],
  "supportedTrusts": ["reputation", "crypto-economic", "tee-attestation", "social-graph"],
  "x402support": false
}
```

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Agent display name |
| `description` | string | What the agent does |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `image` | string | Avatar URL (IPFS or HTTP) |
| `active` | boolean | Whether agent is currently operational (default: true) |
| `services` | array | Endpoint definitions (MCP, A2A, OASF, agentWallet, ENS, DID, custom) |
| `registrations` | array | On-chain registrations in `{ agentRegistry, agentId }` form |
| `supportedTrusts` | string[] | Trust mechanisms: reputation, crypto-economic, tee-attestation, social-graph |
| `x402support` | boolean | Whether agent supports x402 payments |

## AgentSummary (Indexed View)

The subgraph/8004scan indexes on-chain data into a lighter `AgentSummary`:

```typescript
interface AgentSummary {
  agentId: string;           // "{chainId}:{tokenId}"
  chainId: number;
  tokenId: number;
  name: string;
  description: string;
  image?: string;
  active: boolean;
  owner: string;             // Wallet address
  agentURI: string;          // Token URI
  services: Array<{ name: string; endpoint: string; version?: string }>;
  skills: string[];
  domains: string[];
  x402support: boolean;
  wallet?: string;           // Registered agent wallet
  feedbackCount: number;
  averageValue: number;
  registeredAt: number;      // Block timestamp
  updatedAt: number;
}
```

## Feedback Data (Off-chain Payload)

When feedback includes an IPFS `payloadCID`, it resolves to:

```json
{
  "text": "Detailed review of the agent interaction",
  "mcp": {
    "tool": "code-review",
    "prompt": "Review my PR",
    "resource": "github://repo/pr/123"
  },
  "a2a": {
    "skills": ["code-review"],
    "contextId": "ctx-abc",
    "taskId": "task-123"
  },
  "oasf": {
    "skills": ["code-review", "testing"],
    "domains": ["software-engineering"]
  },
  "proofOfPayment": {
    "txHash": "0x...",
    "amount": "0.01",
    "currency": "ETH"
  }
}
```

## OASF Taxonomy

Skills and domains follow the Open Agent Skill Framework (OASF) from [agntcy/oasf](https://github.com/agntcy/oasf):

- **Skills**: Specific capabilities (code-review, translation, summarization)
- **Domains**: Broad categories (software-engineering, finance, healthcare)

Use `--validate-oasf true` during registration to validate against the official taxonomy.
