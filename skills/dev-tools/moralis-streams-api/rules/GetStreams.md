# Get streams

Get all the evm streams for the current project based on the project api-key .

## Method

GET

## Base URL

`https://api.moralis-streams.com`

## Path

`/streams/evm`

## Query Params

| Name | Type | Required | Description | Example |
|------|------|----------|-------------|----------|
| limit | number | Yes | Limit response results max value 100 | \`100\` |
| cursor | string | No | Cursor for fetching next page | - |
| status | string | No | - | - |

## Cursor/Pagination

- **limit**: Limit response results max value 100
- **cursor**: Cursor for fetching next page

The response includes a **cursor** field for pagination. Use this cursor in the next request to get the next page of results.

## Response Example

Status: 200

Ok

```json
{
  "result": [
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
  ],
  "cursor": "cursor_example",
  "total": 0
}
```

## Example (curl)

```bash
curl -X GET "https://api.moralis-streams.com/streams/evm?limit=100" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY"
```
