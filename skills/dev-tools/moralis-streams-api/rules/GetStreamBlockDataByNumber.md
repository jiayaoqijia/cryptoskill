# Get webhook data returned on the block number with provided stream config

Get webhook data returned on the block number with provided stream config.

## Method

POST

## Base URL

`https://api.moralis-streams.com`

## Path

`/streams/evm/:chainId/block/:blockNumber`

## Path Params

| Name | Type | Required | Description | Example |
|------|------|----------|-------------|----------|
| chainId | string | Yes | - | - |
| blockNumber | number | Yes | - | - |

## Body

| Name | Type | Required | Description | Example |
|------|------|----------|-------------|----------|
| tag | string | No | A user-provided tag that will be send along the webhook, the user can use this tag to identify the specific stream if multiple streams are present | \`string\` |
| topic0 | array | No | An Array of topic0's in string-signature format ex: ['FunctionName(address,uint256)'] | \`\` |
| allAddresses | boolean | No | Include events for all addresses (only applied when abi and topic0 is provided) | \`-\` |
| includeNativeTxs | boolean | No | Include or not native transactions defaults to false | \`-\` |
| includeContractLogs | boolean | No | Include or not logs of contract interactions defaults to false | \`-\` |
| includeInternalTxs | boolean | No | Include or not include internal transactions defaults to false | \`-\` |
| includeAllTxLogs | boolean | No | Include all logs if atleast one value in tx or log matches stream config | \`-\` |
| filterPossibleSpamAddresses | boolean | No | - | \`-\` |
| abi | - | No | - | \`string\` |
| advancedOptions | - | No | - | \`string\` |
| addresses | array | No | - | \`\` |

## Example (curl)

```bash
curl -X POST "https://api.moralis-streams.com/streams/evm/:chainId/block/:blockNumber" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "tag": "string",
  "topic0": [],
  "allAddresses": false,
  "includeNativeTxs": false,
  "includeContractLogs": false,
  "includeInternalTxs": false,
  "includeAllTxLogs": false,
  "filterPossibleSpamAddresses": false,
  "abi": "string",
  "advancedOptions": "string",
  "addresses": []
}'
```
