# Webhook Response Body

The body contains the data you are interested in. The `logs` array contains raw events and stream information such as `tag` and `streamId`. The body also contains a `chainId`, the block number, internal transactions, the ABIs, and a `confirmed` field that indicates if the block is confirmed.

## Common Fields

All webhook responses include these common fields:

| Field | Type | Description |
|-------|------|-------------|
| `confirmed` | boolean | `true` if block is confirmed, `false` for pending blocks |
| `chainId` | string | Hex chain ID (e.g., `"0x1"` for Ethereum) |
| `abi` | array | ABI definitions for the contracts being monitored |
| `streamId` | string | UUID of the stream that sent this webhook |
| `tag` | string | Custom tag for the stream |
| `retries` | number | Number of delivery retry attempts |
| `block` | object | Block information (number, hash, timestamp) |
| `logs` | array | Raw event logs |
| `txs` | array | Native transactions |
| `txsInternal` | array | Internal transactions |
| `erc20Transfers` | array | ERC20 transfer events (decoded) |
| `erc20Approvals` | array | ERC20 approval events (decoded) |
| `nftApprovals` | object | NFT approval events (ERC721, ERC1155) — nested format |
| `nftTokenApprovals` | array | NFT approval events (flat array, preferred over `nftApprovals`) |
| `nftTransfers` | array | NFT transfer events (decoded) |
| `nativeBalances` | array | Native token balances (when `getNativeBalances` is configured) |

## Response Types

### 1. Native Transactions

For native transactions, set `Native Transactions (txs)` in admin interface or `includeNativeTxs: true` via SDK.

```json
{
  "confirmed": false,
  "chainId": "0x1",
  "abi": [],
  "streamId": "c28d9e2e-ae9d-4fe6-9fc0-5fcde2dcdd17",
  "tag": "native_transactions",
  "retries": 0,
  "block": {
    "number": "15988759",
    "hash": "0x3aa07bd98e328db97ec273ce06b3a15fc645931fbd26337fe20c48b274277f76",
    "timestamp": "1668676247"
  },
  "logs": [],
  "txs": [
    {
      "hash": "0xd68700a0e2abd9c041eb236812e4194bf91c8182a2b03065887ab0f33d5c2958",
      "gas": "149200",
      "gasPrice": "13670412399",
      "nonce": "57995",
      "input": "0xf78dc253000000000000000000000000d9408f29...cfee7c08",
      "transactionIndex": "52",
      "fromAddress": "0x839d4641f97153b0ff26ab837860c479e2bd0242",
      "toAddress": "0x1111111254eeb25477b68fb85ed929f73a960582",
      "value": "0",
      "type": "2",
      "v": "1",
      "r": "46904304245026065492026869531757792493071866863221741878090753056388581469881",
      "s": "17075445080437932806356212399757328600893345374993510540712828450455909549452",
      "receiptCumulativeGasUsed": "3131649",
      "receiptGasUsed": "113816",
      "receiptContractAddress": null,
      "receiptRoot": null,
      "receiptStatus": "1"
    }
  ],
  "txsInternal": [],
  "erc20Transfers": [],
  "erc20Approvals": [],
  "nftApprovals": {
    "ERC1155": [],
    "ERC721": []
  },
  "nftTransfers": []
}
```

### 2. Native Transactions with Contract Logs

For native transactions + logs/events, select both `Native Transactions (txs)` and `Contract interactions (logs)` in admin interface, or set `includeContractLogs: true` and `includeNativeTxs: true` via SDK.

```json
{
  "confirmed": true,
  "chainId": "0x1",
  "abi": [],
  "streamId": "c28d9e2e-ae9d-4fe6-9fc0-5fcde2dcdd17",
  "tag": "native_transactions_with_logs",
  "retries": 0,
  "block": {
    "number": "15988780",
    "hash": "0xf40d623518fa16c20614278656e426721820031913fd9c670330d4b2b751d50e",
    "timestamp": "1668676499"
  },
  "logs": [
    {
      "logIndex": "135",
      "transactionHash": "0x59cd370a41c699bdb77a020b3a27735bb7442ace68ec8313040b8b9ee2672244",
      "address": "0x96beaa1316f85fd679ec49e5a63dacc293b044be",
      "data": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
      "topic0": "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925",
      "topic1": "0x0000000000000000000000001748789703159580520cc2ce6d1ba01e7359c44c",
      "topic2": "0x0000000000000000000000001111111254eeb25477b68fb85ed929f73a960582",
      "topic3": null
    }
  ],
  "txs": [
    {
      "hash": "0x0bd4d05cfee0107ac69f7add8e21d66c3e4fd014b7aad595d6336910a6bfee39",
      "gas": "109803",
      "gasPrice": "13481860832",
      "nonce": "291",
      "input": "0x12aa3caf00000000000000000000000053222470...e26b9977",
      "transactionIndex": "92",
      "fromAddress": "0x3ec92c9d09403a76bda445ffdfaf6de59717219f",
      "toAddress": "0x1111111254eeb25477b68fb85ed929f73a960582",
      "value": "0",
      "type": "2",
      "v": "0",
      "r": "5776335037912114053229884461119750189570811705028494471955321961511802532800",
      "s": "50481622078880425443801093626517935308993319586804232237135731552994210947860",
      "receiptCumulativeGasUsed": "7225224",
      "receiptGasUsed": "70168",
      "receiptContractAddress": null,
      "receiptRoot": null,
      "receiptStatus": "1"
    }
  ],
  "txsInternal": [],
  "erc20Transfers": [],
  "erc20Approvals": [
    {
      "transactionHash": "0x59cd370a41c699bdb77a020b3a27735bb7442ace68ec8313040b8b9ee2672244",
      "logIndex": "135",
      "contract": "0x96beaa1316f85fd679ec49e5a63dacc293b044be",
      "owner": "0x1748789703159580520cc2ce6d1ba01e7359c44c",
      "spender": "0x1111111254eeb25477b68fb85ed929f73a960582",
      "value": "115792089237316195423570985008687907853269984665640564039457584007913129639935",
      "tokenName": "This Is Not Alpha",
      "tokenSymbol": "TINA",
      "tokenDecimals": "18",
      "valueWithDecimals": "1.15792089237316195423570985008687907853269984665640564039457584007913129639935e+59"
    }
  ],
  "nftApprovals": {
    "ERC1155": [],
    "ERC721": []
  },
  "nftTransfers": []
}
```

### 3. ERC20 Transfers

ERC20 transfer data is automatically decoded from logs and included at no additional record cost. Included in both `confirmed: false` and `confirmed: true` payloads.

```json
{
  "confirmed": false,
  "chainId": "0x5",
  "abi": [],
  "streamId": "c4cf9b1a-0cb3-4c79-9ca3-04f11856c555",
  "tag": "ChrisWallet",
  "retries": 0,
  "block": {
    "number": "8037952",
    "hash": "0x607ff512f17f890bf9ee6206e2029cd8530819ab72b2b9161f9b90d18ece8e03",
    "timestamp": "1669667244"
  },
  "logs": [
    {
      "logIndex": "132",
      "transactionHash": "0x1642a3b9b39e63d7fe571e7c22b80a5b059d2647fe4866d3f7105630f822d833",
      "address": "0x0041ebd11f598305d401cc1052df49219630ab79",
      "data": "0x0000000000000000000000000000000000000000000069e10006afc3291c0000",
      "topic0": "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
      "topic1": "0x0000000000000000000000000a46413965858a6ac4ed5184d7643dc055a4fea3",
      "topic2": "0x000000000000000000000000e496601436da37a045d8e88bbd6b2c2e17d8fe33",
      "topic3": null
    }
  ],
  "txs": [
    {
      "hash": "0x1642a3b9b39e63d7fe571e7c22b80a5b059d2647fe4866d3f7105630f822d833",
      "gas": "85359",
      "gasPrice": "6129141152",
      "nonce": "88",
      "input": "0xa9059cbb000000000000000000000000e496601436da37a045d8e88bbd6b2c2e17d8fe330000000000000000000000000000000000000000000069e10006afc3291c0000",
      "transactionIndex": "49",
      "fromAddress": "0x0a46413965858a6ac4ed5184d7643dc055a4fea3",
      "toAddress": "0x0041ebd11f598305d401cc1052df49219630ab79",
      "value": "0",
      "type": "2",
      "v": "1",
      "r": "86947778944630951418310264989677611886333891146913483133255814972120449355054",
      "s": "7019311275916215306620036726907048105130260362064080269753410507440852031640",
      "receiptCumulativeGasUsed": "11882265",
      "receiptGasUsed": "56906",
      "receiptContractAddress": null,
      "receiptRoot": null,
      "receiptStatus": "1"
    }
  ],
  "txsInternal": [],
  "erc20Transfers": [
    {
      "transactionHash": "0x1642a3b9b39e63d7fe571e7c22b80a5b059d2647fe4866d3f7105630f822d833",
      "logIndex": "132",
      "contract": "0x0041ebd11f598305d401cc1052df49219630ab79",
      "from": "0x0a46413965858a6ac4ed5184d7643dc055a4fea3",
      "to": "0xe496601436da37a045d8e88bbd6b2c2e17d8fe33",
      "value": "499999000000000000000000",
      "tokenName": "Example Token",
      "tokenSymbol": "Token",
      "tokenDecimals": "18",
      "valueWithDecimals": "499999"
    }
  ],
  "erc20Approvals": [],
  "nftApprovals": {
    "ERC1155": [],
    "ERC721": []
  },
  "nftTransfers": []
}
```

### 4. NFT Transfers

NFT transfer data is automatically decoded from logs and included at no additional record cost, similar to ERC20 transfers. Included in both `confirmed: false` and `confirmed: true` payloads.

**NFT Transfer Fields:**

| Field | Description |
|-------|-------------|
| `tokenName` | Name of the NFT |
| `tokenSymbol` | Symbol of the NFT (only for ERC721) |
| `tokenContractType` | Type of NFT (`ERC721` or `ERC1155`) |
| `to` | Receiver address |
| `from` | Sender address |
| `amount` | Amount transferred (`1` for ERC721) |
| `transactionHash` | Transaction hash |
| `tokenId` | Token ID of the NFT |
| `operator` | Third party address approved to manage NFTs (EIP1155) |
| `contract` | Contract address |

```json
{
  "confirmed": false,
  "chainId": "0x13881",
  "abi": [],
  "streamId": "c4cf9b1a-0cb3-4c79-9ca3-04f11856c555",
  "tag": "ChrisWallet",
  "retries": 0,
  "block": {
    "number": "29381772",
    "hash": "0xdd64099df718e2a439a9805d25a3ab88e943a8c713f2259d9777460d7051572c",
    "timestamp": "1669640635"
  },
  "logs": [
    {
      "logIndex": "72",
      "transactionHash": "0x5ecd6b57593ab2f4f3e39fbb3318a3933e2cf9fdcf5b7ca671fb0fc2ce9dc4b5",
      "address": "0x26b4e79bca1a550ab26a8e533be97c40973b2671",
      "data": "0x",
      "topic0": "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef",
      "topic1": "0x00000000000000000000000074f64bebb1a9615fc7c2ead9c894b6ffd1803582",
      "topic2": "0x000000000000000000000000e496601436da37a045d8e88bbd6b2c2e17d8fe33",
      "topic3": "0x0000000000000000000000000000000000000000000000000000000000000000"
    }
  ],
  "txs": [],
  "txsInternal": [],
  "erc20Transfers": [],
  "erc20Approvals": [],
  "nftApprovals": {
    "ERC1155": [],
    "ERC721": []
  },
  "nftTransfers": [
    {
      "operator": null,
      "from": "0x74f64bebb1a9615fc7c2ead9c894b6ffd1803582",
      "to": "0xe496601436da37a045d8e88bbd6b2c2e17d8fe33",
      "tokenId": "0",
      "amount": "1",
      "transactionHash": "0x5ecd6b57593ab2f4f3e39fbb3318a3933e2cf9fdcf5b7ca671fb0fc2ce9dc4b5",
      "logIndex": "72",
      "contract": "0x26b4e79bca1a550ab26a8e533be97c40973b2671",
      "tokenName": "Test",
      "tokenSymbol": "SYMBOL",
      "tokenContractType": "ERC721"
    }
  ]
}
```

### 5. Smart Contract Events Only

For smart contract events (logs), select `Contract interactions (logs)` and `Event Emittance` in admin interface. Provide an ABI and select at least one topic. Via SDK: set `includeContractLogs: true` and provide ABI and topic.

```json
{
  "confirmed": false,
  "chainId": "0x1",
  "abi": [
    {
      "anonymous": false,
      "inputs": [
        {
          "indexed": false,
          "name": "reserve0",
          "type": "uint112"
        },
        {
          "indexed": false,
          "name": "reserve1",
          "type": "uint112"
        }
      ],
      "name": "Sync",
      "type": "event"
    }
  ],
  "streamId": "6378fe38-54c7-4816-8d61-fca8e128e260",
  "tag": "test_events",
  "retries": 1,
  "block": {
    "number": "15984246",
    "hash": "0x7f8d8285b572a60f6a14d5f1dcbd40e487ccffd9ec78f8dfbccb49aa191fbb95",
    "timestamp": "1668621827"
  },
  "logs": [
    {
      "logIndex": "320",
      "transactionHash": "0xf1682fa49b83689093b467ac6937785102895fc3ba418624c28d04f9af6e5e2b",
      "address": "0x4cd36d6f32586177e36179a810595a33163a20bf",
      "data": "0x00000000000000000000000000000000000000000000944ad388817e590ab6070000000000000000000000000000000000000000000000000000008a602de18e",
      "topic0": "0x1c411e9a96e071241c2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1",
      "topic1": null,
      "topic2": null,
      "topic3": null
    }
  ],
  "txs": [],
  "txsInternal": [],
  "erc20Transfers": [],
  "erc20Approvals": [],
  "nftApprovals": {
    "ERC1155": [],
    "ERC721": []
  },
  "nftTransfers": []
}
```

### 6. Internal Transactions

For internal transactions, select `Internal Transactions (txsInternal)` in admin interface or set `includeInternalTxs: true` via SDK.

```json
{
  "confirmed": false,
  "chainId": "0x1",
  "abi": [],
  "streamId": "c28d9e2e-ae9d-4fe6-9fc0-5fcde2dcdd17",
  "tag": "internal transactions",
  "retries": 0,
  "block": {
    "number": "15988462",
    "hash": "0xa4520ca85758374d05c31f6e6869f081997daa6e6b18449d49cfac4558f9e7f8",
    "timestamp": "1668672659"
  },
  "logs": [],
  "txs": [],
  "txsInternal": [
    {
      "from": "0x1111111254eeb25477b68fb85ed929f73a960582",
      "to": "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
      "value": "11000000000000000",
      "gas": "117885",
      "transactionHash": "0x0e5c3114c0ee7d29cca17aa0b8e790c4d7d25b4789bd14150f113956b5ce94de"
    }
  ],
  "erc20Transfers": [],
  "erc20Approvals": [],
  "nftApprovals": {
    "ERC1155": [],
    "ERC721": []
  },
  "nftTransfers": []
}
```

### 7. Native Balances

When `getNativeBalances` is configured on your stream, the webhook includes a `nativeBalances` array with the native token balance of matched addresses at the time of the block.

```json
{
  "confirmed": true,
  "chainId": "0x1",
  "nativeBalances": [
    {
      "address": "0x839d4641f97153b0ff26ab837860c479e2bd0242",
      "balance": "1234567890000000000",
      "balanceWithDecimals": "1.23456789"
    }
  ]
}
```

| Field | Description |
|-------|-------------|
| `address` | Wallet address |
| `balance` | Native balance in wei (as string) |
| `balanceWithDecimals` | Human-readable balance with decimals |

See [UsefulStreamOptions.md](UsefulStreamOptions.md) for `getNativeBalances` configuration.

### 8. NFT Token Approvals (Flat Array)

The `nftTokenApprovals` field provides NFT approval events as a flat array (preferred over the nested `nftApprovals` object):

```json
{
  "nftTokenApprovals": [
    {
      "transactionHash": "0xabc...",
      "logIndex": "42",
      "contract": "0x1234...",
      "account": "0x5678...",
      "operator": "0x9abc...",
      "approvedAll": true,
      "tokenContractType": "ERC721",
      "tokenName": "BoredApeYachtClub",
      "tokenSymbol": "BAYC"
    }
  ]
}
```

## Enrichment Fields

Decoded transfer and approval events include additional enrichment fields:

| Field | Type | Description |
|-------|------|-------------|
| `logo` | string | URL to the token logo image |
| `thumbnail` | string | URL to a smaller token logo thumbnail |
| `possibleSpam` | boolean | `true` if the token is flagged as potential spam |
| `verifiedCollection` | boolean | `true` if the NFT collection is verified |

These fields appear on `erc20Transfers`, `erc20Approvals`, and `nftTransfers` entries.

## Trigger Results

When [Triggers](Triggers.md) are configured on a stream, matching events include a `triggers` array and a `triggered_by` field:

```json
{
  "erc20Transfers": [
    {
      "transactionHash": "0xabc...",
      "from": "0x1234...",
      "to": "0x5678...",
      "value": "1000000000000000000",
      "triggered_by": "erc20transfer",
      "triggers": [
        {
          "name": "balanceOf",
          "value": "5000000000000000000"
        }
      ]
    }
  ]
}
```

| Field | Description |
|-------|-------------|
| `triggered_by` | The event type that activated the trigger |
| `triggers` | Array of trigger results with `name` (function name) and `value` (return value) |

## Block Object

The `block` object contains:

```json
{
  "number": "15988759",
  "hash": "0x3aa07bd98e328db97ec273ce06b3a15fc645931fbd26337fe20c48b274277f76",
  "timestamp": "1668676247"
}
```

| Field | Description |
|-------|-------------|
| `number` | Block number (as string) |
| `hash` | Block hash |
| `timestamp` | Unix timestamp |

## Log Entry Object

Each log entry in the `logs` array contains:

```json
{
  "logIndex": "135",
  "transactionHash": "0x59cd370a41c699bdb77a020b3a27735bb7442ace68ec8313040b8b9ee2672244",
  "address": "0x96beaa1316f85fd679ec49e5a63dacc293b044be",
  "data": "0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
  "topic0": "0x8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b925",
  "topic1": "0x0000000000000000000000001748789703159580520cc2ce6d1ba01e7359c44c",
  "topic2": "0x0000000000000000000000001111111254eeb25477b68fb85ed929f73a960582",
  "topic3": null
}
```

## Transaction Object

Each transaction in the `txs` array contains:

```json
{
  "hash": "0xd68700a0e2abd9c041eb236812e4194bf91c8182a2b03065887ab0f33d5c2958",
  "gas": "149200",
  "gasPrice": "13670412399",
  "nonce": "57995",
  "input": "0xf78dc253...",
  "transactionIndex": "52",
  "fromAddress": "0x839d4641f97153b0ff26ab837860c479e2bd0242",
  "toAddress": "0x1111111254eeb25477b68fb85ed929f73a960582",
  "value": "0",
  "type": "2",
  "v": "1",
  "r": "4690430424502606549...",
  "s": "17075445080437932806...",
  "receiptCumulativeGasUsed": "3131649",
  "receiptGasUsed": "113816",
  "receiptContractAddress": null,
  "receiptRoot": null,
  "receiptStatus": "1"
}
```

## Stream Configuration Reference

To enable different data types in webhooks, configure your stream:

| Data Type | Admin Interface Selection | SDK Parameter |
|-----------|---------------------------|---------------|
| Native transactions | `Native Transactions (txs)` | `includeNativeTxs: true` |
| Contract logs | `Contract interactions (logs)` | `includeContractLogs: true` |
| Internal transactions | `Internal Transactions (txsInternal)` | `includeInternalTxs: true` |

## See Also

- [WebhookSecurity.md](WebhookSecurity.md) - Verify webhook signatures
- [CreateStream.md](CreateStream.md) - Create streams with specific configurations
