# Transactions

Execute transactions with agent wallets.

## Endpoint

```bash
POST /v1/wallets/{wallet_id}/rpc
```

## Ethereum Transactions

### Send ETH

```json
{
  "method": "eth_sendTransaction",
  "caip2": "eip155:1",
  "params": {
    "transaction": {
      "to": "0x...",
      "value": "1000000000000000"
    }
  }
}
```

### Send on Base (Chain ID 8453)

```json
{
  "method": "eth_sendTransaction",
  "caip2": "eip155:8453",
  "params": {
    "transaction": {
      "to": "0x...",
      "value": "1000000000000000"
    }
  }
}
```

### Contract Interaction (with data)

```json
{
  "method": "eth_sendTransaction",
  "caip2": "eip155:8453",
  "params": {
    "transaction": {
      "to": "0x...",
      "data": "0x...",
      "value": "0"
    }
  }
}
```

### Response

```json
{
  "method": "eth_sendTransaction",
  "data": {
    "hash": "0x...",
    "caip2": "eip155:8453"
  }
}
```

## Sign Message (Personal Sign)

```json
{
  "method": "personal_sign",
  "params": {
    "message": "0x..."
  }
}
```

## Sign Typed Data (EIP-712)

```json
{
  "method": "eth_signTypedData_v4",
  "params": {
    "typed_data": {
      "types": {...},
      "primaryType": "...",
      "domain": {...},
      "message": {...}
    }
  }
}
```

## Solana Transactions

### Sign and Send Transaction

```json
{
  "method": "signAndSendTransaction",
  "caip2": "solana:mainnet",
  "params": {
    "transaction": "<base64-encoded-transaction>"
  }
}
```

### Sign Transaction Only

```json
{
  "method": "signTransaction",
  "caip2": "solana:mainnet",
  "params": {
    "transaction": "<base64-encoded-transaction>"
  }
}
```

### Sign Message

```json
{
  "method": "signMessage",
  "params": {
    "message": "<base64-encoded-message>"
  }
}
```

## CAIP-2 Chain Identifiers

| Chain | CAIP-2 |
|-------|--------|
| Ethereum Mainnet | `eip155:1` |
| Goerli Testnet | `eip155:5` |
| Sepolia Testnet | `eip155:11155111` |
| Base | `eip155:8453` |
| Base Sepolia | `eip155:84532` |
| Polygon | `eip155:137` |
| Arbitrum One | `eip155:42161` |
| Optimism | `eip155:10` |
| Avalanche C-Chain | `eip155:43114` |
| BNB Chain | `eip155:56` |
| Solana Mainnet | `solana:mainnet` |
| Solana Devnet | `solana:devnet` |

## Transaction Options

### Gas Sponsorship

Add `"sponsor": true` to have Privy sponsor gas fees:

```json
{
  "method": "eth_sendTransaction",
  "caip2": "eip155:8453",
  "sponsor": true,
  "params": {
    "transaction": {
      "to": "0x...",
      "value": "0"
    }
  }
}
```

### Custom Gas Settings

```json
{
  "method": "eth_sendTransaction",
  "caip2": "eip155:1",
  "params": {
    "transaction": {
      "to": "0x...",
      "value": "1000000000000000",
      "gas_limit": "21000",
      "max_fee_per_gas": "50000000000",
      "max_priority_fee_per_gas": "2000000000"
    }
  }
}
```

## Error Handling

Policy violations return an error:

```json
{
  "error": {
    "code": "POLICY_VIOLATION",
    "message": "Transaction exceeds maximum allowed value"
  }
}
```

Common errors:
- `POLICY_VIOLATION` — Transaction blocked by policy
- `INSUFFICIENT_FUNDS` — Wallet lacks funds for transaction
- `INVALID_TRANSACTION` — Malformed transaction data
