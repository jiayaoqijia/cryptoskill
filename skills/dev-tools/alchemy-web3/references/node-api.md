# Node API Reference

Standard Ethereum JSON-RPC methods supported by Alchemy.

## Common Methods

### eth_getBalance
Get native token balance.

```json
{
  "method": "eth_getBalance",
  "params": ["0x...", "latest"]
}
```

### eth_getTransactionByHash
Get transaction details.

```json
{
  "method": "eth_getTransactionByHash",
  "params": ["0x...txhash"]
}
```

### eth_getTransactionReceipt
Get transaction receipt (status, logs, gas used).

```json
{
  "method": "eth_getTransactionReceipt",
  "params": ["0x...txhash"]
}
```

### eth_getBlockByNumber
Get block by number.

```json
{
  "method": "eth_getBlockByNumber",
  "params": ["latest", true]
}
```

### eth_call
Call contract function (read-only).

```json
{
  "method": "eth_call",
  "params": [{
    "to": "0x...",
    "data": "0x..."
  }, "latest"]
}
```

### eth_sendRawTransaction
Submit signed transaction.

```json
{
  "method": "eth_sendRawTransaction",
  "params": ["0x...signedTx"]
}
```

### eth_estimateGas
Estimate gas for transaction.

```json
{
  "method": "eth_estimateGas",
  "params": [{
    "from": "0x...",
    "to": "0x...",
    "data": "0x..."
  }]
}
```

### eth_gasPrice
Get current gas price.

```json
{
  "method": "eth_gasPrice",
  "params": []
}
```

### eth_getLogs
Get event logs.

```json
{
  "method": "eth_getLogs",
  "params": [{
    "address": "0x...",
    "topics": ["0x..."],
    "fromBlock": "0x...",
    "toBlock": "latest"
  }]
}
```

### eth_chainId
Get chain ID.

```json
{
  "method": "eth_chainId",
  "params": []
}
```

### eth_blockNumber
Get current block number.

```json
{
  "method": "eth_blockNumber",
  "params": []
}
```

## Alchemy-Enhanced Methods

### alchemy_getAssetTransfers
Get transaction history with decoded transfers.

```json
{
  "method": "alchemy_getAssetTransfers",
  "params": [{
    "fromBlock": "0x0",
    "toBlock": "latest",
    "toAddress": "0x...",
    "category": ["external", "erc20", "erc721", "erc1155"],
    "maxCount": "0x64"
  }]
}
```

### alchemy_getTokenBalances
Get all ERC-20 balances.

```json
{
  "method": "alchemy_getTokenBalances",
  "params": ["0x...", "erc20"]
}
```

### alchemy_getTokenMetadata
Get token info (name, symbol, decimals).

```json
{
  "method": "alchemy_getTokenMetadata",
  "params": ["0x...tokenAddress"]
}
```

### alchemy_simulateExecution
Simulate transaction execution.

```json
{
  "method": "alchemy_simulateExecution",
  "params": [{
    "from": "0x...",
    "to": "0x...",
    "data": "0x..."
  }]
}
```

## Debug/Trace Methods

### debug_traceTransaction
Full EVM trace of transaction.

```json
{
  "method": "debug_traceTransaction",
  "params": ["0x...txhash", {"tracer": "callTracer"}]
}
```

### trace_transaction
OpenEthereum-style trace.

```json
{
  "method": "trace_transaction",
  "params": ["0x...txhash"]
}
```

## WebSocket Subscriptions

Connect via:
```
wss://{chain}.g.alchemy.com/v2/{apiKey}
```

### eth_subscribe - newHeads
```json
{"method": "eth_subscribe", "params": ["newHeads"]}
```

### eth_subscribe - logs
```json
{"method": "eth_subscribe", "params": ["logs", {"address": "0x..."}]}
```

### eth_subscribe - pendingTransactions
```json
{"method": "eth_subscribe", "params": ["alchemy_pendingTransactions"]}
```
