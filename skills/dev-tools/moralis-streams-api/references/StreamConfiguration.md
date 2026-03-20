# Stream Configuration Reference

Complete reference for stream configuration when working with Moralis Streams API.

## Table of Contents

- [Stream ID Format](#stream-id-format)
- [Chain IDs](#chain-ids)
- [Topic0 (Event Signature) Format](#topic0-event-signature-format)
- [Stream Status Values](#stream-status-values)
- [Common Stream Field Mappings](#common-stream-field-mappings)
- [Stream Types](#stream-types)
- [Advanced Options](#advanced-options)
- [Address Monitoring](#address-monitoring)
- [Best Practices](#best-practices)

---

## Stream ID Format

**ALWAYS UUID, never hex:**

```typescript
// ❌ WRONG - Hex format
"0x1234567890abcdef"

// ✅ CORRECT - UUID format
"a1b2c3d4-e5f6-7890-abcd-ef1234567890"
```

### UUID Format Validation

```typescript
function isValidUUID(uuid: string): boolean {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(uuid);
}

// Usage
const streamId = 'a1b2c3d4-e5f6-7890-abcd-ef1234567890';
if (!isValidUUID(streamId)) {
  throw new Error('Invalid stream ID format. Must be UUID.');
}
```

### Stream ID Sources

- **Created by API:** When you call `CreateStream`, the response includes the `id` field
- **From GetStreams:** List all streams to get their IDs
- **From dashboard:** Manually copy from Moralis Streams dashboard

## Chain IDs

**ALWAYS hex strings:**

```typescript
// Common chain IDs (EVM chains)
"0x1"     // Ethereum
"0x89"    // Polygon
"0x38"    // BSC (Binance Smart Chain)
"0xa4b1"  // Arbitrum
"0xa"     // Optimism
"0x2105"  // Base
"0xa86a"  // Avalanche
"0xfa"     // Fantom
"0x19"     // Cronos
"0x64"     // Gnosis
"0xe708"  // Linea
```

### Complete Chain ID Reference

| Chain          | Hex ID      | String Name |
| --------------- | ----------- | ----------- |
| Ethereum       | `0x1`      | `eth`       |
| Ethereum Sepolia | `0xaa36a7`  | `sepolia`   |
| Ethereum Holesky | `0x4268` | `holesky`   |
| Polygon        | `0x89`     | `polygon`    |
| Polygon Amoy   | `0x13882`  | `amoy`      |
| BSC            | `0x38`     | `bsc`        |
| BSC Testnet   | `0x61`     | `bsc testnet` |
| Arbitrum      | `0xa4b1`   | `arbitrum`   |
| Arbitrum Sepolia | `0x66eee` | `arbitrum sepolia` |
| Optimism      | `0xa`      | `optimism`   |
| Optimism Sepolia | `0xaa37dc` | `optimism sepolia` |
| Base           | `0x2105`   | `base`       |
| Base Sepolia   | `0x14a34`  | `base sepolia` |
| Avalanche      | `0xa86a`   | `avalanche`  |
| Fantom         | `0xfa`     | `fantom`     |
| Fantom Testnet | `0xfa2`    | `fantom testnet` |
| Cronos         | `0x19`     | `cronos`     |
| Gnosis         | `0x64`     | `gnosis`     |
| Gnosis Chiado  | `0x27d8`   | `gnosis chiado` |
| Linea          | `0xe708`   | `linea`      |
| Linea Sepolia | `0xe705`   | `linea sepolia` |
| Moonbeam       | `0x504`    | `moonbeam`   |
| Moonriver      | `0x505`    | `moonriver`  |
| Flow           | `0x2eb`    | `flow`       |
| Flow Testnet   | `0x221`    | `flow testnet` |
| Ronin          | `0x7e4`    | `ronin`      |
| Ronin Saigon   | `0x7e5`    | `ronin saigon` |
| Lisk           | `0x46f`    | `lisk`       |
| Lisk Sepolia  | `0x106a`   | `lisk sepolia` |
| Pulse          | `0x171`    | `pulse`      |
| Sei            | `0x531`    | `sei`        |
| Sei Testnet   | `0x530`    | `sei testnet` |
| Monad          | `0x8f`     | `monad`     |
| HyperEVM       | `0x3e7`    | `hyperevm`  |
| Chiliz         | `0x15b38`  | `chiliz`    |
| Chiliz Testnet | `0x15b32`  | `chiliz testnet` |
| Moonbase       | `0x507`    | `moonbase`  |

### Chains NOT Supported by Streams

The following chains are supported by the Moralis Data API but **do not support Streams**:

- zkSync (`0x144`)
- Blast (`0x13e31`)
- Mantle (`0x1388`)
- opBNB (`0xcc`)
- Polygon zkEVM (`0x44d`)
- Zetachain (`0x1b59`)

### Chain ID Validation

```typescript
function isValidChainId(chainId: string): boolean {
  // Must be hex string
  if (!/^0x[a-fA-F0-9]+$/.test(chainId)) {
    return false;
  }
  // Check if it's a known chain (optional)
  const knownChains = [
    '0x1', '0x89', '0x38', '0xa4b1', '0xa', '0x2105',
    '0xa86a', '0xfa', '0x19', '0x64', '0xe708'
  ];
  return knownChains.includes(chainId) || chainId.length === 10; // Allow custom chains
}
```

## Topic0 (Event Signature) Format

**Must be exact Solidity event signature:**

### Standard Event Signatures

```typescript
// ERC20 Transfer
"Transfer(address,address,uint256)"

// ERC20 Approval
"Approval(address,address,uint256)"

// NFT Transfer (both ERC721 and ERC1155)
"Transfer(address,address,uint256)"

// ERC721 Approval
"Approval(address,address,uint256)"

// ERC1155 Transfer Batch
"TransferBatch(address,address,uint256[])"
```

### Custom Event Signatures

```typescript
// Custom event
"MyEvent(address,uint256,bytes)"

// Multiple indexed params
"Swap(address,address,uint256,uint256)"

// Struct param
"TokenDetails(string name,uint256 amount,address[] holders)"
```

### Finding Event Signatures

1. **Check contract ABI** - Look for the event definition
2. **Use block explorer** - Look at the contract's events tab
3. **Use ethers.js** - Parse the interface:

```typescript
import { Interface } from 'ethers';

const abi = [
  "event Transfer(address indexed from, address indexed to, uint256 value)"
];
const iface = new Interface(abi);
const fragment = iface.getEvent('Transfer');
console.log(fragment.format); // "Transfer(address,address,uint256)"
```

## Stream Status Values

**Lowercase only:**

```typescript
// ✅ CORRECT
"active"
"paused"
"error"
"terminated"

// ❌ WRONG
"ACTIVE"
"PAUSED"
"Active"
"Paused"
```

### Status Descriptions

| Status | Description |
|--------|-------------|
| `active` | Normal operating state. Blocks are evaluated and webhooks are delivered. |
| `paused` | Manually paused. No blocks evaluated, no webhooks sent. Resume by setting to `active`. |
| `error` | Auto-triggered when webhook success rate drops below 70% or event queue exceeds 10,000. Delivery paused, blocks still evaluated. |
| `terminated` | Auto-triggered after 24 hours in `error` state. **Unrecoverable** — must create a new stream. |

See [ErrorHandling.md](ErrorHandling.md) for complete error lifecycle details.

### Status Transitions

```typescript
type StreamStatus = 'active' | 'paused' | 'error' | 'terminated';

async function pauseStream(streamId: string): Promise<void> {
  const response = await fetch(`/streams/evm/${streamId}/status`, {
    method: 'POST',
    body: JSON.stringify({ status: 'paused' })
  });
}

async function resumeStream(streamId: string): Promise<void> {
  const response = await fetch(`/streams/evm/${streamId}/status`, {
    method: 'POST',
    body: JSON.stringify({ status: 'active' })
  });
}
```

### Status Validation

```typescript
function isValidStreamStatus(status: string): boolean {
  const validStatuses = ['active', 'paused', 'error', 'terminated'];
  return validStatuses.includes(status.toLowerCase());
}
```

## Common Stream Field Mappings

### API Response → TypeScript Interface

```typescript
// API response → TypeScript interface
{
  webhook_url: string;
  chain_ids: string[];
  topic0: string[];
  all_addresses: boolean;
  include_native_hash: boolean;
  description: string;
  tag: string;
  include_native_txs: boolean;
  include_contract_logs: boolean;
  include_internal_txs: boolean;
  include_all_tx_logs: boolean;
  get_native_balances: Array<{...}>;
  abi: string;
  advanced_options: Array<{...}>;
  triggers: Array<{...}>;
}
→ {
  webhookUrl: string;
  chainIds: string[];
  topic0: string[];
  allAddresses: boolean;
  includeNativeHash: boolean;
  description: string;
  tag: string;
  includeNativeTxs: boolean;
  includeContractLogs: boolean;
  includeInternalTxs: boolean;
  includeAllTxLogs: boolean;
  getNativeBalances: Array<{...}>;
  abi: string;
  advancedOptions: Array<{...}>;
  triggers: Array<{...}>;
}
```

### Field-by-Field Mapping

```typescript
// Common snake_case → camelCase conversions
webhook_url           → webhookUrl
chain_ids             → chainIds
topic0                → topic0
all_addresses         → allAddresses
include_native_hash   → includeNativeHash
include_native_txs    → includeNativeTxs
include_contract_logs → includeContractLogs
include_internal_txs  → includeInternalTxs
include_all_tx_logs  → includeAllTxLogs
get_native_balances   → getNativeBalances
advanced_options      → advancedOptions
```

### Automatic Conversion Function

```typescript
function toCamelCase(str: string): string {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

// Example: toCamelCase('webhook_url') → 'webhookUrl'
```

## Stream Types

Streams can monitor different types of blockchain events:

### Native Transactions (tx)

Monitors all native ETH token transfers.

```typescript
{
  "include_native_txs": true
}
```

### Contract Logs (logs)

Monitors contract event logs based on `topic0`.

```typescript
{
  "include_contract_logs": true,
  "topic0": ["Transfer(address,address,uint256)"]
}
```

### ERC20 Transfers (erc20transfer)

Monitors ERC20 token transfer events.

```typescript
{
  "topic0": ["Transfer(address,address,uint256)"]
}
```

### ERC20 Approvals (erc20approval)

Monitors ERC20 approval events.

```typescript
{
  "topic0": ["Approval(address,address,uint256)"]
}
```

### NFT Transfers (nfttransfer)

Monitors NFT transfer events.

```typescript
{
  "topic0": ["Transfer(address,address,uint256)"]
}
```

### Internal Transactions (internalTx)

Monitors internal ETH transfers within contract execution.

```typescript
{
  "include_internal_txs": true
}
```

### Multiple Stream Types

A single stream can monitor multiple event types:

```typescript
{
  "include_native_txs": true,
  "include_contract_logs": true,
  "include_internal_txs": true,
  "topic0": [
    "Transfer(address,address,uint256)",
    "Approval(address,address,uint256)"
  ]
}
```

## Advanced Options

Some stream features require advanced options configuration.

### Including Native Hash

```typescript
{
  "advanced_options": [
    {
      "topic0": "Transfer(address,address,uint256)",
      "include_native_hash": true
    }
  ]
}
```

### Custom Triggers

```typescript
{
  "triggers": [
    {
      "type": "contract",
      "contractAddress": "0x...",
      "inputs": [
        { "type": "address", "name": "from" },
        { "type": "uint256", "name": "amount" }
      ],
      "functionAbi": {
        "inputs": [...],
        "name": "transfer",
        "type": "function"
      }
    }
  ]
}
```

## Address Monitoring

### Specific Addresses

```typescript
{
  "all_addresses": false,
  // Addresses added via AddAddressToStream endpoint
}
```

### All Addresses on Chain

```typescript
{
  "all_addresses": true,  // ⚠️ Resource-intensive
  "chain_ids": ["0x1", "0x89"]
}
```

### Address Limits

| Plan Type      | Address Limit |
| -------------- | -------------- |
| Starter Plan   | 10,000 addresses |
| Pro / Business | 50,000 addresses |
| Enterprise     | Up to 100M addresses |

## Project Settings Region

When configuring project settings via `SetSettings`, you can specify a region:

| Region | Value |
|--------|-------|
| US East | `us-east-1` |
| US West | `us-west-2` |
| EU Central | `eu-central-1` |
| Asia Pacific | `ap-southeast-1` |

```bash
curl -X POST "https://api.moralis-streams.com/settings" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"region": "eu-central-1"}'
```

## Best Practices

1. **Always use hex chain IDs** - More efficient than string names
2. **Verify stream ID format** - Must be UUID, never hex
3. **Use lowercase status values** - `"active"`, `"paused"`, `"error"`, or `"terminated"`
4. **Start with specific addresses** - Use `all_addresses: false` to test
5. **Enable only needed event types** - Don't monitor everything unnecessarily
6. **Set appropriate chainIds** - Monitor only chains you actually need
7. **Use advanced options sparingly** - Only when necessary for your use case
8. **Verify webhook URL** - Must be publicly accessible from internet
9. **Test with sample data** - Create test stream before production deployment
10. **Monitor webhook failures** - Use retry logic for unreliable webhooks
