# Agent Schema — Registration File & Data Structures

## Registration File

The `agentURI` on the Identity Registry resolves to a JSON registration file. This is the primary metadata document describing an agent.

```json
{
  "name": "My Agent",
  "description": "A detailed description of what this agent does",
  "image": "ipfs://Qm.../avatar.png",
  "active": true,
  "services": {
    "mcp": { "url": "https://agent.example.com/mcp" },
    "a2a": { "url": "https://agent.example.com/a2a" },
    "ens": { "name": "myagent.eth" },
    "did": { "id": "did:example:123" },
    "email": { "address": "agent@example.com" },
    "web": { "url": "https://agent.example.com" }
  },
  "supportedTrust": ["reputation", "crypto-economic", "tee-attestation"],
  "skills": ["code-review", "testing", "deployment"],
  "domains": ["software-engineering", "devops"],
  "x402": false,
  "metadata": {
    "version": "1.0",
    "customField": "value"
  }
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
| `services` | object | Endpoint definitions (MCP, A2A, ENS, DID, email, web) |
| `supportedTrust` | string[] | Trust mechanisms supported: reputation, crypto-economic, tee-attestation |
| `skills` | string[] | OASF skill identifiers |
| `domains` | string[] | OASF domain identifiers |
| `x402` | boolean | Whether agent supports x402 payments |
| `metadata` | object | Arbitrary key-value pairs |

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
  mcpEndpoint?: string;
  a2aEndpoint?: string;
  ensName?: string;
  skills: string[];
  domains: string[];
  x402: boolean;
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
