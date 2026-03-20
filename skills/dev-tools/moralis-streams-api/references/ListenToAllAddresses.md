# Listen to All Addresses

Monitor specific events across **every contract on a chain** without adding individual addresses. Useful for tracking all ERC20 transfers, NFT mints, or any event signature network-wide.

## How It Works

Set `allAddresses: true` in your stream configuration along with a `topic0` event signature and an `abi`. The stream will match that event on every contract, not just addresses you've explicitly added.

**Requirements:**
- `allAddresses` must be `true`
- `topic0` must be provided (event signature to filter)
- `abi` must be provided (defines the event structure for decoding)
- `webhookUrl` must be set (where to receive events)

Without all three (`allAddresses`, `topic0`, `abi`), the stream won't work correctly.

## Plan Availability

This feature is **not available on all plans**. Check your Moralis plan tier before relying on it. Higher-tier plans support more compute units for all-address streams.

---

## Create Stream: All ERC20 Transfers

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "webhookUrl": "https://your-server.com/webhook",
    "description": "All ERC20 transfers on Ethereum",
    "tag": "all-erc20-transfers",
    "topic0": ["Transfer(address,address,uint256)"],
    "allAddresses": true,
    "includeContractLogs": true,
    "abi": [
      {
        "anonymous": false,
        "inputs": [
          { "indexed": true, "name": "from", "type": "address" },
          { "indexed": true, "name": "to", "type": "address" },
          { "indexed": false, "name": "value", "type": "uint256" }
        ],
        "name": "Transfer",
        "type": "event"
      }
    ],
    "chainIds": ["0x1"]
  }'
```

## Create Stream: All NFT Transfers

NFT transfers share the same `Transfer(address,address,uint256)` signature as ERC20. The difference is the third parameter represents a `tokenId` instead of a `value`. To capture NFT transfers specifically, use the NFT ABI variant:

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "webhookUrl": "https://your-server.com/webhook",
    "description": "All NFT transfers on Ethereum",
    "tag": "all-nft-transfers",
    "topic0": ["Transfer(address,address,uint256)"],
    "allAddresses": true,
    "includeContractLogs": true,
    "abi": [
      {
        "anonymous": false,
        "inputs": [
          { "indexed": true, "name": "from", "type": "address" },
          { "indexed": true, "name": "to", "type": "address" },
          { "indexed": true, "name": "tokenId", "type": "uint256" }
        ],
        "name": "Transfer",
        "type": "event"
      }
    ],
    "chainIds": ["0x1"]
  }'
```

**Important:** ERC20 and ERC721 Transfer events produce the same `topic0` hash because the function signature is identical. The difference is whether the third parameter is `indexed`. This means an all-address stream for one will also capture events from the other. Filter by checking whether the log has 3 or 4 topics (ERC721 transfers have 4 topics since `tokenId` is indexed; ERC20 transfers have 3).

## Create Stream: All Approval Events

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "webhookUrl": "https://your-server.com/webhook",
    "description": "All ERC20 approvals on Ethereum",
    "tag": "all-approvals",
    "topic0": ["Approval(address,address,uint256)"],
    "allAddresses": true,
    "includeContractLogs": true,
    "abi": [
      {
        "anonymous": false,
        "inputs": [
          { "indexed": true, "name": "owner", "type": "address" },
          { "indexed": true, "name": "spender", "type": "address" },
          { "indexed": false, "name": "value", "type": "uint256" }
        ],
        "name": "Approval",
        "type": "event"
      }
    ],
    "chainIds": ["0x1"]
  }'
```

---

## Key Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `allAddresses` | boolean | Yes | Must be `true` to listen on all addresses |
| `topic0` | string[] | Yes | Event signatures to filter (e.g., `["Transfer(address,address,uint256)"]`) |
| `abi` | object[] | Yes | ABI definition of the events to decode |
| `includeContractLogs` | boolean | Recommended | Set `true` to include contract event logs |
| `chainIds` | string[] | Yes | Hex chain IDs (e.g., `["0x1", "0x89"]`) |
| `webhookUrl` | string | Yes | URL to receive webhook events |
| `tag` | string | Yes | Identifier for the stream |
| `advancedOptions` | object[] | No | Per-topic options like `includeNativeHash` |

---

## Warnings and Best Practices

**Resource intensive:** All-address streams generate significantly more webhook calls than address-specific streams. This can exhaust your compute quota quickly on lower-tier plans.

**Prefer specific addresses when possible:**
```json
// Only use allAddresses when you truly need every contract
{
  "allAddresses": true,   // Monitors ALL contracts on chain
  "topic0": ["Transfer(address,address,uint256)"]
}

// For known contracts, add addresses explicitly instead
{
  "allAddresses": false,  // Then use AddAddressToStream endpoint
  "topic0": ["Transfer(address,address,uint256)"]
}
```

**Multi-chain considerations:** Adding multiple `chainIds` with `allAddresses: true` multiplies the event volume. Start with a single chain and scale up.

**ABI collision:** Different contracts may emit events with identical `topic0` signatures but different semantics (e.g., ERC20 vs ERC721 `Transfer`). Your webhook handler should validate the decoded data matches your expected format.

**Test with block replay first:** Use the `GetStreamBlockDataByNumber` endpoint to test your stream configuration against a specific block before going live. This lets you verify your `topic0` and `abi` are correct without receiving live webhooks.
