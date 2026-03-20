# Useful Streams Options

Advanced configuration options for customizing webhook data when creating or updating streams.

## Overview

These options allow you to control what data is included in your webhook payloads, helping you reduce noise and focus on relevant blockchain events.

## Include Contract Logs

The `includeContractLogs` option includes all contract logs in the webhook.

```json
{
    "includeContractLogs": true
}
```

**Use cases:**

- Monitoring a specific contract
- Tracking wallet interactions with contracts

**Behavior:** When set to `true`, all contract logs are included. For wallet address monitoring, this enables you to also receive contract logs when the wallet interacts with a contract.

## Internal Transactions

Monitor all internal transactions happening on-chain by setting `includeInternalTxs` to `true`:

```json
{
    "includeInternalTxs": true
}
```

Internal transactions are transactions that are initiated by smart contracts rather than external accounts. These are useful for tracking complex DeFi interactions and contract-to-contract calls.

## Include Native Transactions

Control whether native (ETH, BNB, MATIC, etc.) transactions are included:

```json
{
    "includeNativeTxs": true
}
```

## Include All Transaction Logs

When `includeAllTxLogs` is enabled, it will include **all related logs** if any log or transaction matches your stream config.

```json
{
    "includeAllTxLogs": true
}
```

**Requirements:**

- Must be used together with `includeNativeTxs` or `includeContractLogs`
- Available on **Moralis Pro Plan & higher**

**Example:** Enabling `includeAllTxLogs` in a stream with `includeNativeTxs` enabled will return all logs related to the transaction sent in the webhook.

## Advanced Options

An array of advanced option objects that allow you to specify additional filters and conditions. Each object has the following **required** fields:

| Field              | Type    | Description                                                                                   |
| ------------------ | ------- | --------------------------------------------------------------------------------------------- |
| `topic0`           | string  | The event signature to listen to (e.g., `Transfer(address,address,uint256)`)                  |
| `filter`           | object  | Custom filter object with conditions data must meet (see [FilterStreams](./FilterStreams.md)) |
| `includeNativeTxs` | boolean | Whether to include native transactions in addition to contract logs                           |

### Use Case

Advanced Options are useful when you want to narrow down the data included in the stream to only include specific types of events or transactions. For example:

- Only listen to transfers of a certain amount
- Filter transfers from a particular address
- Track specific contract events with value thresholds

### Example Configuration

```json
{
    "topic0": "Transfer(address,address,uint256)",
    "filter": {
        "and": [
            {
                "eq": ["from", "0x283af0b28c62c092c9727f1ee09c02ca627eb7f5"]
            },
            {
                "gt": ["amount", "100000000000000000000"]
            }
        ]
    },
    "includeNativeTxs": false
}
```

**Explanation:**

- Listening to the ERC20 `Transfer(address,address,uint256)` event
- Filtering for transfers where `from` equals `0x283af0b28c62c092c9727f1ee09c02ca627eb7f5`
- Only including transfers where `amount` is greater than 100 tokens (in wei, assuming 18 decimals)
- Not including native transactions

## Get Native Balances

The `getNativeBalances` option enriches webhook payloads with native token balances (ETH, BNB, MATIC, etc.) of matched addresses at the time of the block.

> **Note:** Requires **Business plan** or higher.

### Configuration

```json
{
  "getNativeBalances": [
    {
      "selectors": ["$from", "$to"],
      "type": "erc20transfer"
    }
  ]
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| `selectors` | string[] | Dynamic selectors for addresses to query (`$from`, `$to`, `$contract`) |
| `type` | string | Event type that triggers balance lookup |

### Valid Types

| Type | Description |
|------|-------------|
| `tx` | Native transactions |
| `log` | Contract event logs |
| `erc20transfer` | ERC20 token transfers |
| `erc20approval` | ERC20 approvals |
| `nfttransfer` | NFT transfers |
| `internalTx` | Internal transactions |

### Example: Get Balances on ERC20 Transfers

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "webhookUrl": "https://your-server.com/webhook",
  "description": "ERC20 transfers with native balances",
  "tag": "erc20-native-balances",
  "chainIds": ["0x1"],
  "topic0": ["Transfer(address,address,uint256)"],
  "includeContractLogs": true,
  "abi": [
    {
      "anonymous": false,
      "inputs": [
        {"indexed": true, "name": "from", "type": "address"},
        {"indexed": true, "name": "to", "type": "address"},
        {"indexed": false, "name": "value", "type": "uint256"}
      ],
      "name": "Transfer",
      "type": "event"
    }
  ],
  "getNativeBalances": [
    {
      "selectors": ["$from", "$to"],
      "type": "erc20transfer"
    }
  ]
}'
```

### Resulting Webhook Payload

```json
{
  "nativeBalances": [
    {
      "address": "0x1234...",
      "balance": "1500000000000000000",
      "balanceWithDecimals": "1.5"
    },
    {
      "address": "0x5678...",
      "balance": "250000000000000000",
      "balanceWithDecimals": "0.25"
    }
  ]
}
```

## Filter Possible Spam Addresses

Set `filterPossibleSpamAddresses` to `true` to automatically exclude events from known spam token contracts. This prevents spam tokens from appearing in your webhook payloads.

```json
{
  "filterPossibleSpamAddresses": true
}
```

This is especially useful for wallet monitoring streams where spam token transfers are common. See also [FilterStreams.md](FilterStreams.md) for more filtering options.

## Combining Options

You can combine multiple options in a single stream configuration:

```json
{
    "webhookUrl": "https://your-server.com/webhook",
    "includeNativeTxs": true,
    "includeContractLogs": true,
    "includeInternalTxs": true,
    "includeAllTxLogs": true,
    "advancedOptions": [
        {
            "topic0": "Transfer(address,address,uint256)",
            "filter": {
                "gt": ["value", "1000000000000000000"]
            },
            "includeNativeTxs": false
        }
    ]
}
```

## References

- [Advanced Options Documentation](https://docs.moralis.com/streams-api/evm/streams-configuration/useful-streams-options)
- [CreateStream](./CreateStream.md) - For creating streams with these options
- [UpdateStream](./UpdateStream.md) - For updating existing stream options
- [FilterStreams](./FilterStreams.md) - For detailed filter syntax and examples
