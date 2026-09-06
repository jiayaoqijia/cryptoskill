# 8004-MCP - Agent Registry Protocol

Multi-chain MCP server for ERC-8004 Agent Registry. Query agents, reputation, and feedback across Solana + EVM chains.

---

## ⚡ First Time Setup (IMPORTANT)

### 1. Check System Health
```typescript
await client.callTool({ name: 'health_check', arguments: {} });
// Returns: { server: 'ok', chains: {...}, walletStore: 'not_initialized', ... }
```

### 2. Initialize Wallet Store (One-Time)
The wallet store encrypts all your wallets with a single master password.

```typescript
// ⚠️ SAVE THIS PASSWORD - Cannot be recovered if lost!
await client.callTool({ name: 'wallet_store_init', arguments: {
  password: 'YourSecureMasterPassword123!'
}});
// Returns: { initialized: true, message: 'Wallet store created' }
```

### 3. Create a Wallet
```typescript
await client.callTool({ name: 'wallet_create', arguments: {
  name: 'my-eth-wallet',
  chainType: 'evm'  // or 'solana'
}});
// Returns: { name: 'my-eth-wallet', address: '0x...', chainType: 'evm' }
```

### 4. Fund Your Wallet

Check the "Approximate Costs" section below for funding amounts.

```typescript
// Get faucet info (testnet) or ask owner (mainnet)
const funding = await client.callTool({ name: 'faucet_info', arguments: {
  chain: 'eth'  // or 'sol', 'base'
}});
// Returns faucet URLs and wallet address
```

**⚠️ Important for Agents:**
- See "Approximate Costs" section for funding amounts
- Faucets require captchas - you can't use them directly
- Ask your owner to fund your wallet
- On mainnet: no faucets, must ask owner for real funds

### 5. On New Sessions - Unlock Store
```typescript
await client.callTool({ name: 'wallet_store_unlock', arguments: {
  password: 'YourSecureMasterPassword123!'
}});
// Now all write operations work
```

### Common Issues

| Symptom | Cause | Solution |
|---------|-------|----------|
| `STORE_NOT_INITIALIZED` | First run | Call `wallet_store_init` |
| `STORE_LOCKED` | New session | Call `wallet_store_unlock` |
| `INVALID_PASSWORD` | Wrong password | Check password (no recovery!) |
| Timeout on wallet ops | Store locked | Unlock first |
| `INSUFFICIENT_BALANCE` | Empty wallet | Ask owner to fund (see below) |

### Requesting Funds from Owner

As an agent, you cannot use faucets directly (captchas). Ask your owner:

```typescript
// 1. Get your wallet address
const info = await client.callTool({ name: 'faucet_info', arguments: { chain: 'eth' }});

// 2. Ask owner to fund (see "Approximate Costs" section for amounts)
// Example: "Please fund my wallet 0x1234... with ~0.01 SOL or ~$0.50 in ETH"

// 3. Wait for owner to send funds, then proceed with agent_register
```

---

## Quick Start (MCP Client)

```typescript
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import { spawn } from 'child_process';

const server = spawn('npx', ['@quantulabs/8004-mcp'], {
  stdio: ['pipe', 'pipe', 'inherit'],
  env: { ...process.env, NETWORK_MODE: 'testnet' }
});

const client = new Client(
  { name: 'my-agent', version: '1.0.0' },
  { capabilities: {} }
);

await client.connect(new StdioClientTransport({
  reader: server.stdout,
  writer: server.stdin,
}));

// Ready - use client.callTool()
```

## Global ID Format

| Chain | Format | Example |
|-------|--------|---------|
| Solana | `sol:<pubkey>` | `sol:HHCVWcqs...` |
| Ethereum | `eth:<chainId>:<tokenId>` | `eth:11155111:738` |
| Base | `base:<chainId>:<tokenId>` | `base:84532:42` |

---

## Core Tools

### Read Operations (No wallet needed)

#### agent_search
Search agents across chains.
```typescript
await client.callTool({ name: 'agent_search', arguments: {
  query: 'trading bot',      // Search name/description
  chain: 'eth',              // Optional: sol, eth, base, arb, poly, op
  limit: 20,                 // Default: 20, max: 100
  offset: 0,                 // Pagination offset
  cursor: 'abc...',          // Cursor pagination (EVM only, faster)
  // Advanced filters (EVM only):
  hasMcp: true,              // Has MCP endpoint
  hasA2a: true,              // Has A2A endpoint
  active: true,              // Active agents only
  x402support: true,         // Supports x402 payments
  mcpTools: ['web-search'],  // Has specific MCP tools
  a2aSkills: ['translation'] // Has specific A2A skills
}});
// Returns: { results: IAgentSummary[], total, hasMore, cursor? }
```

#### cache_search
Fast fuzzy search (FTS5). Use for partial name matches.
```typescript
await client.callTool({ name: 'cache_search', arguments: {
  query: 'Upsense',  // Partial match works
  chain: 'all',
  limit: 20
}});
```

#### agent_get
Get agent details by ID.
```typescript
await client.callTool({ name: 'agent_get', arguments: {
  id: 'eth:11155111:738'  // Global ID
}});
// Returns: IAgent with name, description, owner, endpoints, metadata
```

#### agent_exists
Check if agent exists.
```typescript
await client.callTool({ name: 'agent_exists', arguments: {
  id: 'sol:HHCVWcqs...'
}});
// Returns: { exists: boolean }
```

#### reputation_get
Get reputation summary.
```typescript
await client.callTool({ name: 'reputation_get', arguments: {
  id: 'sol:HHCVWcqs...'
}});
// Returns: { averageScore, totalFeedbacks, trustTier (Solana only) }
```

#### feedback_list
List feedbacks for an agent.
```typescript
await client.callTool({ name: 'feedback_list', arguments: {
  id: 'sol:HHCVWcqs...',
  limit: 20,
  minScore: 50  // Optional filter
}});
```

#### leaderboard_get
Top agents by reputation.
```typescript
await client.callTool({ name: 'leaderboard_get', arguments: {
  chain: 'sol',
  limit: 10
}});
```

#### solana_atom_stats_get
ATOM reputation metrics (Solana only).
```typescript
await client.callTool({ name: 'solana_atom_stats_get', arguments: {
  asset: 'HHCVWcqs...'  // Solana pubkey (no sol: prefix)
}});
// Returns: { qualityScore, trustTier, uniqueClients, fastEma, slowEma }
```

#### solana_integrity_verify
Verify indexer data integrity (Solana only).
```typescript
await client.callTool({ name: 'solana_integrity_verify', arguments: {
  asset: 'HHCVWcqs...'
}});
// Returns: { status: 'valid' | 'syncing' | 'corrupted' }
```

### Write Operations (Wallet required)

#### Wallet Store Setup (Master Password)
```typescript
// 1. Initialize store (one-time) - SAVE THE MASTER PASSWORD!
await client.callTool({ name: 'wallet_store_init', arguments: {
  password: 'MySecureMaster123!'
}});

// 2. Create wallets (stored in encrypted store)
await client.callTool({ name: 'wallet_create', arguments: {
  name: 'my-solana',
  chainType: 'solana'  // or 'evm'
}});

// 3. On new session, unlock store with master password
await client.callTool({ name: 'wallet_store_unlock', arguments: {
  password: 'MySecureMaster123!'
}});

// 4. Now write operations work (all wallets unlocked)
```

#### feedback_give
Submit feedback for an agent.
```typescript
await client.callTool({ name: 'feedback_give', arguments: {
  id: 'sol:HHCVWcqs...',
  value: 85,              // Score 0-100
  tag1: 'uptime',         // Category tag
  tag2: 'day',            // Period tag
  comment: 'Great agent', // Optional
  skipSend: false         // true = dry-run (returns unsigned tx)
}});
```

#### agent_register
Register new agent on-chain. See "Approximate Costs" section for funding.

```typescript
await client.callTool({ name: 'agent_register', arguments: {
  chain: 'eth',  // or 'sol', 'base', etc.
  name: 'My Agent',
  description: 'Does cool stuff',
  tokenUri: 'https://example.com/agent.json',  // Optional: your hosted metadata
  // If no tokenUri: SDK uploads to IPFS automatically
}});
```

---

## Approximate Costs

### Solana (Devnet/Mainnet)

| Operation | Cost | Notes |
|-----------|------|-------|
| `agent_register` | ~0.01 SOL | Includes ATOM stats account |
| `feedback_give` | ~0.0005 SOL | Event-based, low rent |
| `feedback_response_append` | ~0.0005 SOL | Event-based |
| `agent_uri_update` | ~0.00005 SOL | Tx fee only |

### EVM - L2 Chains (Base, Arbitrum, Optimism)

**Recommended for lowest costs.**

| Operation | Gas | Typical Cost |
|-----------|-----|--------------|
| `agent_register` | 150-200k | $0.01-0.50 |
| `feedback_give` | 100k | $0.01-0.30 |
| `feedback_response_append` | 60k | $0.01-0.20 |
| `agent_uri_update` | 50k | $0.01-0.15 |

### EVM - Ethereum Mainnet

**High variability - gas spikes during congestion.**

| Operation | Gas | Cost (25-100 gwei) |
|-----------|-----|--------------------|
| `agent_register` | 150-200k | $10-60 |
| `feedback_give` | 100k | $7-30 |
| `feedback_response_append` | 60k | $4-18 |
| `agent_uri_update` | 50k | $3-15 |

**Tip:** Use L2 chains (Base, Arbitrum) for 10-100x lower costs than Ethereum mainnet.

---

## Dry-Run Mode (skipSend)

Test write operations without funds or broadcasting:

```typescript
// Returns unsigned transaction, no funds needed
const preview = await client.callTool({ name: 'feedback_give', arguments: {
  id: 'sol:HHCVWcqs...',
  value: 85,
  tag1: 'uptime',
  skipSend: true  // Dry-run
}});
// preview.content[0].text contains: { unsigned: true, transaction: "base64...", message: "..." }
```

Supported on: `feedback_give`, `agent_register`, `agent_transfer`, `agent_uri_update`, `feedback_revoke`, `solana_validation_request`, `solana_validation_respond`

---

## Network Configuration

```typescript
// Check current network
await client.callTool({ name: 'network_get', arguments: {} });

// Switch to mainnet
await client.callTool({ name: 'network_set', arguments: { mode: 'mainnet' } });

// Switch to testnet (default)
await client.callTool({ name: 'network_set', arguments: { mode: 'testnet' } });
```

| Network | Solana | Ethereum | Base |
|---------|--------|----------|------|
| testnet | devnet | Sepolia (11155111) | Base Sepolia (84532) |
| mainnet | mainnet-beta | Mainnet (1) | Base (8453) |

---

## x402 Protocol

Payment-linked reputation.

```typescript
// 1. Build identity for 402 response
const identity = await client.callTool({ name: 'x402_identity_build', arguments: {
  agentId: 'sol:HHCVWcqs...'
}});

// 2. Parse payment proof from response header
const proof = await client.callTool({ name: 'x402_proof_parse', arguments: {
  paymentResponse: 'base64-encoded-header...'
}});

// 3. Submit feedback with proof
await client.callTool({ name: 'x402_feedback_submit', arguments: {
  agentId: 'sol:HHCVWcqs...',
  value: 90,
  tag1: 'x402-resource-delivered',
  tag2: 'exact-svm',
  proofOfPayment: proof.proofOfPayment
}});
```

---

## Error Codes

| Error | Cause | Solution |
|-------|-------|----------|
| `STORE_LOCKED` | Write op without unlock | Call `wallet_store_unlock` with master password |
| `STORE_NOT_INITIALIZED` | No wallet store | Call `wallet_store_init` first |
| `INVALID_PASSWORD` | Wrong master password | Check password (cannot recover if lost) |
| `AGENT_NOT_FOUND` | Invalid ID | Verify global ID format |
| `INSUFFICIENT_BALANCE` | Wallet empty | Fund wallet address |
| `PROVIDER_NOT_AVAILABLE` | Chain not initialized | Check `network_get` |

---

## OASF Standards

```typescript
// List valid skill slugs
await client.callTool({ name: 'oasf_list_skills', arguments: {} });

// List valid domain slugs
await client.callTool({ name: 'oasf_list_domains', arguments: {} });

// List feedback tags
await client.callTool({ name: 'oasf_list_tags', arguments: {} });
```

---

## All Tools Reference

### Agent Operations
- `agent_get` - Get agent by ID
- `agent_exists` - Check existence
- `agent_search` - Search with filters
- `agent_list_by_owner` - List by owner address
- `agent_register` - Register new agent (write)
- `agent_transfer` - Transfer ownership (write)
- `agent_uri_update` - Update metadata URI (write)
- `agent_metadata_set` - Set on-chain metadata (Solana, write)

### Feedback Operations
- `feedback_give` - Submit feedback (write)
- `feedback_read` - Read single feedback
- `feedback_list` - List feedbacks
- `feedback_revoke` - Revoke feedback (write)
- `feedback_response_append` - Respond to feedback (write)

### Reputation Operations
- `reputation_get` - Get summary
- `leaderboard_get` - Top agents

### Collection Operations
- `collection_get` - Get collection details
- `collection_list` - List collections
- `collection_agents` - List agents in collection
- `collection_base_get` - Get base registry
- `collection_create` - Create collection (Solana, write)
- `collection_uri_update` - Update collection URI (Solana, write)

### Wallet Store (Master Password)
- `wallet_store_init` - Initialize store with master password
- `wallet_store_unlock` - Unlock all wallets with master password
- `wallet_store_lock` - Lock store (secure wipe)
- `wallet_store_status` - Get store status
- `wallet_store_change_password` - Change master password
- `wallet_store_migrate` - Migrate legacy wallets

### Wallet Operations
- `wallet_list` - List wallets in store
- `wallet_info` - Wallet details
- `wallet_create` - Create new wallet (requires unlocked store)
- `wallet_import` - Import private key (requires unlocked store)
- `wallet_delete` - Delete wallet (requires unlocked store)
- `wallet_security` - Configure auto-lock timeout

### Cache Operations
- `cache_search` - Fast FTS5 search
- `cache_refresh` - Force refresh
- `cache_stats` - Cache statistics
- `cache_sync_status` - Sync status

### Solana-Specific
- `solana_atom_stats_get` - ATOM metrics
- `solana_atom_stats_initialize` - Init ATOM account (write)
- `solana_trust_tier_get` - Trust tier
- `solana_enriched_summary_get` - Combined metrics
- `solana_agent_wallet_get` - Get operational wallet
- `solana_sign` - Sign with agent wallet
- `solana_verify` - Verify signature
- `solana_validation_request` - Request validation (write)
- `solana_validation_respond` - Respond to validation (write)
- `solana_validation_read` - Read validation
- `solana_validation_wait` - Wait for response
- `solana_validation_pending_get` - Pending validations
- `solana_integrity_verify` - O(1) integrity check
- `solana_integrity_verify_deep` - Deep verification

### EVM-Specific
- `evm_agent_wallet_set` - Set operational wallet (write)
- `evm_agent_wallet_unset` - Remove operational wallet (write)

### x402 Protocol
- `x402_identity_build` - Build agent identity
- `x402_proof_parse` - Parse payment proof
- `x402_feedback_build` - Build feedback file
- `x402_feedback_submit` - Submit with proof (write)

### Configuration & Health
- `config_get` - Current config
- `config_set` - Update config
- `config_reset` - Reset to defaults
- `network_get` - Network status
- `network_set` - Switch network
- `health_check` - System health (server, chains, wallet store, cache)
- `faucet_info` - Testnet faucet URLs and funding info

### OASF Standards
- `oasf_list_skills` - Valid skill slugs
- `oasf_list_domains` - Valid domain slugs
- `oasf_list_tags` - Feedback tags
- `oasf_validate_skill` - Validate skill
- `oasf_validate_domain` - Validate domain
- `oasf_validate_tag` - Validate tag

### Crawler
- `crawler_fetch_mcp` - Fetch MCP capabilities
- `crawler_fetch_a2a` - Fetch A2A agent card
- `crawler_is_alive` - Health check

### IPFS (Configured by default)
- `ipfs_configure` - Override default IPFS/Pinata settings (optional)
- `ipfs_add_json` - Store JSON (max 1MB)
- `ipfs_add_registration` - Store registration file
- `ipfs_get_registration` - Retrieve registration

> Note: IPFS is pre-configured with a shared Pinata account. No setup required for basic usage.

---

## Claude Code Integration

> This section is for Claude Code / AI assistants using 8004-MCP tools.

### Intent Mapping

| User Says | Tool | Notes |
|-----------|------|-------|
| "find agents", "search for X" | `agent_search` or `cache_search` | Use `cache_search` for partial names |
| "agent details", "info on X" | `agent_get` | Pass global ID |
| "is X reliable?", "reputation" | `reputation_get` | Returns score + trust tier |
| "top agents", "best agents" | `leaderboard_get` | Chain optional |
| "reviews for X", "feedback" | `feedback_list` | |
| "my wallets" | `wallet_list` | |
| "switch to mainnet" | `network_set` | `mode: 'mainnet'` |
| "OASF skills/domains/tags" | `oasf_list_*` | |

### DO NOT use web search for:
- Agent registry queries (use 8004 tools)
- Reputation/feedback lookups
- OASF standards
- x402 protocol

### Search Strategy
1. **Exact name known** → `agent_search` with `nameQuery`
2. **Partial name** → `cache_search` (fuzzy FTS5)
3. **By capabilities** → `agent_search` with `hasMcp`, `hasA2a`, `mcpTools`, etc.
4. **By owner** → `agent_search` with `owner`

### Write Operation Flow
1. Check `wallet_store_status` - is store initialized and unlocked?
2. If not initialized: `wallet_store_init` (save master password!)
3. If locked: `wallet_store_unlock` with master password
4. If no wallet: `wallet_create` for needed chain
5. Execute write operation
6. Report transaction hash on success
