# Get project stats by Stream ID

Get the stats for the streamId specified

## Method

GET

## Base URL

`https://api.moralis-streams.com`

## Path

`/stats/:streamId`

## Path Params

| Name | Type | Required | Description | Example |
|------|------|----------|-------------|----------|
| streamId | string | Yes | The id of the stream to get the stats | - |

## Response Example

Status: 200

Ok

```json
{
  "totalWebhooksDelivered": 0,
  "totalWebhooksFailed": 0,
  "totalLogsProcessed": 0,
  "totalTxsProcessed": 0,
  "totalTxsInternalProcessed": 0,
  "streams": [
    {
      "totalWebhooksDelivered": 0,
      "totalWebhooksFailed": 0,
      "totalLogsProcessed": 0,
      "totalTxsProcessed": 0,
      "totalTxsInternalProcessed": 0,
      "streamId": "streamId_example"
    }
  ],
  "createdAt": "createdAt_example",
  "updatedAt": "updatedAt_example"
}
```

## Example (curl)

```bash
curl -X GET "https://api.moralis-streams.com/stats/:streamId" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY"
```
