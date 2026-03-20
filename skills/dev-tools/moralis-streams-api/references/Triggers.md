# Triggers (Read-Only Contract Call Enrichment)

Triggers allow you to enrich webhook data with on-chain read calls. When a stream event fires, Moralis executes a read-only (`view`/`pure`) smart contract function and attaches the result to the webhook payload.

## Trigger Interface

Each trigger object has the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `type` | string | Yes | Event type that activates this trigger |
| `contractAddress` | string | Yes | Contract to call (use `$contract` for dynamic) |
| `functionAbi` | object | Yes | ABI of the `view`/`pure` function to call |
| `inputs` | array | Yes | Function input values (supports dynamic selectors) |
| `topic0` | string | No | Filter to specific event signature |
| `callFrom` | string | No | Address to use as `msg.sender` for the call |

## Valid Trigger Types

| Type | Fires On |
|------|----------|
| `tx` | Native transactions |
| `log` | Contract event logs |
| `erc20transfer` | ERC20 token transfers |
| `erc20approval` | ERC20 approvals |
| `nfttransfer` | NFT transfers |

## Dynamic Selectors

Instead of hardcoding addresses or values, use selectors that reference fields from the webhook event data:

| Selector | Resolves To |
|----------|-------------|
| `$contract` | Contract address that emitted the event |
| `$from` | Sender address |
| `$to` | Receiver address |
| `$value` | Transfer value |

## Constraint

Only functions with `stateMutability: "view"` or `"pure"` are allowed. State-modifying functions (`nonpayable`, `payable`) will be rejected.

## Example: balanceOf Enrichment for ERC-20 Transfers

Get the sender and receiver token balances whenever an ERC-20 transfer occurs:

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "webhookUrl": "https://your-server.com/webhook",
  "description": "ERC20 transfers with balance enrichment",
  "tag": "erc20-balances",
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
  "triggers": [
    {
      "type": "erc20transfer",
      "contractAddress": "$contract",
      "functionAbi": {
        "constant": true,
        "inputs": [{"name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
      },
      "inputs": ["$from"]
    },
    {
      "type": "erc20transfer",
      "contractAddress": "$contract",
      "functionAbi": {
        "constant": true,
        "inputs": [{"name": "owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
      },
      "inputs": ["$to"]
    }
  ]
}'
```

## Trigger Results in Webhook

When triggers are configured, each matching event (tx, log, transfer, etc.) includes a `triggers` array in the webhook payload:

```json
{
  "erc20Transfers": [
    {
      "transactionHash": "0xabc...",
      "from": "0x1234...",
      "to": "0x5678...",
      "value": "1000000000000000000",
      "triggers": [
        {
          "name": "balanceOf",
          "value": "5000000000000000000"
        },
        {
          "name": "balanceOf",
          "value": "2000000000000000000"
        }
      ]
    }
  ]
}
```

The `triggers` array contains one entry per trigger defined on the stream, in the same order. Each entry has:

| Field | Description |
|-------|-------------|
| `name` | Function name from `functionAbi` |
| `value` | Return value from the contract call (as string) |

## Use Cases

- **Balance tracking**: Get token balances of sender/receiver on every transfer
- **Price feeds**: Call oracle contracts to get current prices alongside swap events
- **Allowance checks**: Read `allowance()` when approval events fire
- **NFT metadata**: Call `tokenURI()` or `ownerOf()` on NFT transfer events
- **Pool state**: Read DEX pair reserves alongside swap events
