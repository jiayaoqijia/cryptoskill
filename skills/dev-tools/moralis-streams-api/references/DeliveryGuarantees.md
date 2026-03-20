# Delivery Guarantees

Complete reference for webhook delivery semantics, idempotency, confirmation finality, test webhooks, and spam detection.

## At-Least-Once Delivery

Moralis Streams provides **at-least-once delivery**. This means:

- Every event will be delivered at least once
- Webhooks **may be retried**, so duplicates are possible
- There are **no ordering guarantees** — events may arrive out of sequence
- Your webhook handlers **must be idempotent** (processing the same event multiple times must be safe)

## Deduplication

Use the following composite key to deduplicate webhook events:

```
transactionHash + logIndex + confirmed
```

- `transactionHash` — unique per transaction
- `logIndex` — unique per event within a transaction
- `confirmed` — distinguishes unconfirmed vs confirmed deliveries

Store processed keys and skip any duplicates.

## Dual Webhook System

For every matching event, Moralis sends **two webhooks**:

1. **Unconfirmed** (`confirmed: false`) — sent immediately when the transaction is included in a block
2. **Confirmed** (`confirmed: true`) — sent once the block reaches finality (chain-specific confirmation depth)

**Important edge case:** The `confirmed: true` webhook may arrive **before** the `confirmed: false` webhook due to network timing. Design your handlers to accept either order.

**Billing:** Only `confirmed: true` webhooks are charged. Unconfirmed webhooks are free.

## Blocks Until Confirmed (Per Chain)

| Chain | Chain ID | Blocks Until Confirmed |
|-------|----------|----------------------|
| Ethereum | `0x1` | 12 |
| Polygon | `0x89` | 100 |
| BSC | `0x38` | 18 |
| Arbitrum | `0xa4b1` | 18 |
| Base | `0x2105` | 100 |
| Optimism | `0xa` | 500 |
| Avalanche | `0xa86a` | 100 |
| Fantom | `0xfa` | 100 |
| Linea | `0xe708` | 100 |
| Cronos | `0x19` | 100 |
| Gnosis | `0x64` | 100 |
| Chiliz | `0x15b38` | 100 |
| Flow | `0x2eb` | 100 |
| Ronin | `0x7e4` | 100 |
| Lisk | `0x46f` | 100 |
| Pulse | `0x171` | 100 |
| HyperEVM | `0x3e7` | 100 |
| Monad | `0x8f` | 100 |

## Test Webhooks

When you create or update a stream, Moralis sends a **test webhook** to verify your endpoint is reachable.

### Test Webhook Behavior

- Sent on every `PUT` (create) and `POST` (update) operation
- Your endpoint **must return 200** (or any 2xx status code)
- If the test webhook fails, the stream will not start
- Test webhooks are **not retried** and **not stored in history**

### Detecting Test Webhooks

Test webhooks have empty arrays for all data fields. Short-circuit processing when you detect this pattern:

```json
{
  "abi": [],
  "block": {
    "hash": "",
    "number": "",
    "timestamp": ""
  },
  "chainId": "",
  "confirmed": true,
  "erc20Approvals": [],
  "erc20Transfers": [],
  "logs": [],
  "nftApprovals": { "ERC721": [], "ERC1155": [] },
  "nftTransfers": [],
  "retries": 0,
  "streamId": "",
  "tag": "",
  "txs": [],
  "txsInternal": []
}
```

### Example Detection Logic

```javascript
app.post("/webhook", (req, res) => {
  // Detect test webhook — empty streamId or empty block hash
  if (!req.body.streamId || !req.body.block?.hash) {
    return res.status(200).json({ message: "Test webhook received" });
  }

  // Process real webhook...
  processWebhook(req.body);
  res.status(200).json({ message: "OK" });
});
```

## Spam Detection

Moralis flags known spam tokens on decoded transfer and approval events.

### `possibleSpam` Field

The `possibleSpam` boolean field appears on:
- `erc20Transfers` entries
- `erc20Approvals` entries
- `nftTransfers` entries

```json
{
  "erc20Transfers": [
    {
      "contract": "0xspamtoken...",
      "from": "0x...",
      "to": "0x...",
      "value": "999999999",
      "possibleSpam": true
    }
  ]
}
```

### Auto-Exclude Spam

Set `filterPossibleSpamAddresses: true` in your stream configuration to automatically exclude events from known spam contracts. This prevents spam tokens from appearing in your webhook payloads entirely.

```json
{
  "webhookUrl": "https://your-server.com/webhook",
  "chainIds": ["0x1"],
  "filterPossibleSpamAddresses": true,
  "topic0": ["Transfer(address,address,uint256)"]
}
```
