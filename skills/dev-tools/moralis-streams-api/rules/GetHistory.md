# Get history

Get all history

## Method

GET

## Base URL

`https://api.moralis-streams.com`

## Path

`/history`

## Query Params

| Name | Type | Required | Description | Example |
|------|------|----------|-------------|----------|
| limit | number | Yes | - | \`100\` |
| cursor | string | No | - | - |
| transactionHash | string | No | - | - |
| excludePayload | boolean | No | - | - |
| streamId | string | No | - | - |
| chainId | array | No | - | - |
| blockNumber | array | No | - | - |
| fromTimestamp | number | No | - | - |
| toTimestamp | number | No | - | - |

## Cursor/Pagination

- **limit**: Number of results per page
- **cursor**: Cursor for next page

The response includes a **cursor** field for pagination. Use this cursor in the next request to get the next page of results.

## Response Example

Status: 200

Ok

```json
{
  "result": [
    {
      "id": "id_example",
      "date": "date_example",
      "tinyPayload": {
        "chainId": "chainId_example",
        "confirmed": true,
        "block": "block_example",
        "records": 0,
        "retries": 0
      },
      "errorMessage": "errorMessage_example",
      "webhookUrl": "webhookUrl_example",
      "streamId": "streamId_example",
      "tag": "tag_example"
    }
  ],
  "cursor": "cursor_example",
  "total": 0
}
```

## Example (curl)

```bash
curl -X GET "https://api.moralis-streams.com/history?limit=100" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY"
```
