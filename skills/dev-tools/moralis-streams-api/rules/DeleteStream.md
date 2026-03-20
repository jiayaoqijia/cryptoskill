# Delete stream

Delete a specific evm stream.

## Method

DELETE

## Base URL

`https://api.moralis-streams.com`

## Path

`/streams/evm/:id`

## Path Params

| Name | Type | Required | Description | Example |
|------|------|----------|-------------|----------|
| id | string | Yes | The id of the stream to delete | - |

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
curl -X DELETE "https://api.moralis-streams.com/streams/evm/:id" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY"
```
