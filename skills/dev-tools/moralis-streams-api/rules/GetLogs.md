# Get logs

Get All logs.

## Method

GET

## Base URL

`https://api.moralis-streams.com`

## Path

`/history/logs`

## Query Params

| Name | Type | Required | Description | Example |
|------|------|----------|-------------|----------|
| limit | number | Yes | - | \`100\` |
| cursor | string | No | - | - |
| streamId | string | No | - | - |
| transactionHash | string | No | - | - |
| deliveryStatus | array | No | - | - |
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
      "streamId": "streamId_example",
      "chain": "chain_example",
      "webhookUrl": "webhookUrl_example",
      "tag": "tag_example",
      "retries": 0,
      "deliveryStatus": "deliveryStatus_example",
      "blockNumber": 0,
      "errorMessage": "errorMessage_example",
      "type": "type_example",
      "createdAt": "createdAt_example"
    }
  ],
  "cursor": "cursor_example",
  "total": 0
}
```

## Example (curl)

```bash
curl -X GET "https://api.moralis-streams.com/history/logs?limit=100" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY"
```
