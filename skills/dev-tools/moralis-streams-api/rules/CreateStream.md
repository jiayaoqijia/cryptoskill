# Create stream

Creates a new evm stream.

## Method

PUT

## Base URL

`https://api.moralis-streams.com`

## Path

`/streams/evm`

## Body

| Name | Type | Required | Description | Example |
|------|------|----------|-------------|----------|
| webhookUrl | string | No | Webhook URL where moralis will send the POST request. | \`string\` |
| description | string | No | A description for this stream | \`string\` |
| tag | string | No | A user-provided tag that will be send along the webhook, the user can use this tag to identify the specific stream if multiple streams are present | \`string\` |
| topic0 | array | No | An Array of topic0's in string-signature format ex: ['FunctionName(address,uint256)'] | \`\` |
| allAddresses | boolean | No | Include events for all addresses (only applied when abi and topic0 is provided) | \`-\` |
| includeNativeTxs | boolean | No | Include or not native transactions defaults to false | \`-\` |
| includeContractLogs | boolean | No | Include or not logs of contract interactions defaults to false | \`-\` |
| includeInternalTxs | boolean | No | Include or not include internal transactions defaults to false | \`-\` |
| includeAllTxLogs | boolean | No | Include all logs if atleast one value in tx or log matches stream config | \`-\` |
| getNativeBalances | array | No | Include native balances for each address in the webhook | \`\` |
| abi | - | No | - | \`string\` |
| advancedOptions | - | No | - | \`string\` |
| chainIds | array | No | The ids of the chains for this stream in hex Ex: ["0x1","0x38"] | \`\` |
| filterPossibleSpamAddresses | boolean | No | Indicator if it is a demo stream | \`-\` |
| demo | boolean | No | Filter possible spam addresses | \`-\` |
| triggers | array | No | triggers | \`\` |

## Response Example

Status: 200

Ok

```json
{
  "webhookUrl": "webhookUrl_example",
  "description": "description_example",
  "tag": "tag_example",
  "topic0": [],
  "allAddresses": true,
  "includeNativeTxs": true,
  "includeContractLogs": true,
  "includeInternalTxs": true,
  "includeAllTxLogs": true,
  "getNativeBalances": [
    {
      "selectors": [],
      "type": "type_example"
    }
  ],
  "chainIds": [],
  "filterPossibleSpamAddresses": true,
  "demo": true,
  "triggers": [
    {
      "type": "type_example",
      "contractAddress": "contractAddress_example",
      "inputs": [],
      "functionAbi": {},
      "topic0": "topic0_example",
      "callFrom": "callFrom_example"
    }
  ],
  "id": "id_example",
  "status": {},
  "statusMessage": "statusMessage_example",
  "updatedAt": "updatedAt_example",
  "amountOfAddresses": 0
}
```

## Example (curl)

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
  "webhookUrl": "string",
  "description": "string",
  "tag": "string",
  "topic0": [],
  "allAddresses": false,
  "includeNativeTxs": false,
  "includeContractLogs": false,
  "includeInternalTxs": false,
  "includeAllTxLogs": false,
  "getNativeBalances": [],
  "abi": "string",
  "advancedOptions": "string",
  "chainIds": [],
  "filterPossibleSpamAddresses": false,
  "demo": false,
  "triggers": []
}'
```
