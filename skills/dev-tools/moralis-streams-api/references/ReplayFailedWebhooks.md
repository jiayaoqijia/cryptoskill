# Replay Failed Webhooks

Replay blockchain events for blocks that failed webhook delivery.

## Concept

When webhook deliveries fail (network issues, server downtime, etc.), you can replay those specific blocks using the block-to-webhook endpoint. This involves:

1. **Query failed logs** - Get all failed delivery attempts
2. **Extract block numbers** - From the failed logs response
3. **Replay each block** - Send webhook for each failed block

## Step 1: Get Failed Logs

```bash
curl -X GET \
  "https://api.moralis-streams.com/history/logs?limit=100&streamId=YOUR_STREAM_ID&deliveryStatus=failed" \
  -H "X-API-Key: $MORALIS_API_KEY"
```

**Query Parameters:**

- `streamId` - Your stream ID (UUID format)
- `deliveryStatus=failed` - Filter for failed deliveries only
- `limit` - Max results (up to 100)
- `cursor` - For pagination (from response)

**Response contains:**

- `blockNumber` - The block that failed
- `chain` - Chain identifier (e.g., "0x1" for Ethereum)
- `errorMessage` - Why delivery failed

## Step 2: Replay Each Failed Block

For each failed block from the response:

```bash
curl -X POST \
  "https://api.moralis-streams.com/streams/evm/0x1/block-to-webhook/12345678/YOUR_STREAM_ID" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json"
```

**Path Parameters:**

- `0x1` - Chain ID (replace with actual chain from failed log)
- `12345678` - Block number (from failed log response)
- `YOUR_STREAM_ID` - Your stream ID

**No request body needed** - Uses your existing stream configuration.

## Complete Example

```bash
# 1. Get all failed logs for a stream
curl -X GET \
  "https://api.moralis-streams.com/history/logs?limit=100&streamId=a1b2c3d4-e5f6-7890-abcd-ef1234567890&deliveryStatus=failed" \
  -H "X-API-Key: $MORALIS_API_KEY"

# 2. For each failed block in response, replay it
# Example: Block 12345678 on Ethereum (0x1)
curl -X POST \
  "https://api.moralis-streams.com/streams/evm/0x1/block-to-webhook/12345678/a1b2c3d4-e5f6-7890-abcd-ef1234567890" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json"
```

## Response Status Codes

| Code | Meaning                                |
| ---- | -------------------------------------- |
| 200  | Webhook sent successfully              |
| 204  | Success (no content)                   |
| 500  | Internal server error - retry later    |
| 504  | Gateway timeout - may succeed on retry |

## Related Endpoints

- [GetLogs](GetLogs.md) - Full logs endpoint with all filters
- [GetStreamBlockDataToWebhookByNumber](GetStreamBlockDataToWebhookByNumber.md) - Block replay endpoint
