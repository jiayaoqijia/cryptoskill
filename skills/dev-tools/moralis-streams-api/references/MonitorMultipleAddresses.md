# Monitor Multiple Addresses

Best practices for handling multiple addresses in your streams.

## Overview

You do not have to create a separate stream for each address. Instead, you can attach multiple addresses to the same stream. The best practice is to create as few streams as possible and instead attach addresses to existing streams whenever it makes sense. You can attach any number of addresses to a stream.

> If you really need more streams, update to a paid plan or contact support (hello@moralis.io) if you are already a paying client.

## Add Multiple Addresses to a Stream

Add multiple addresses to an existing stream using the `AddAddressToStream` endpoint.

### Request

```bash
curl -X POST "https://api.moralis-streams.com/streams/evm/{streamId}/address" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "address": [
      "0xCFDF6Aaae9f6B927E3736FBD327853B622c5060E",
      "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B"
    ]
  }'
```

### Add a Single Address

```bash
curl -X POST "https://api.moralis-streams.com/streams/evm/{streamId}/address" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0xCFDF6Aaae9f6B927E3736FBD327853B622c5060E"
  }'
```

### Response

```json
{
  "addresses": [
    "0xCFDF6Aaae9f6B927E3736FBD327853B622c5060E",
    "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B"
  ],
  "streamId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

## Delete an Address from a Stream

Remove one or more addresses from a stream using the `DeleteAddressFromStream` endpoint.

### Delete a Single Address

```bash
curl -X DELETE "https://api.moralis-streams.com/streams/evm/{streamId}/address" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0xCFDF6Aaae9f6B927E3736FBD327853B622c5060E"
  }'
```

### Delete Multiple Addresses

```bash
curl -X DELETE "https://api.moralis-streams.com/streams/evm/{streamId}/address" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "address": [
      "0xCFDF6Aaae9f6B927E3736FBD327853B622c5060E",
      "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B"
    ]
  }'
```

### Response

```json
{
  "addresses": [
    "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B"
  ],
  "streamId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

## Replace Addresses in a Stream

Replace addresses in a stream using the `ReplaceAddressFromStream` endpoint.

```bash
curl -X PATCH "https://api.moralis-streams.com/streams/evm/{streamId}/address" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
  }'
```

## Get All Addresses from a Stream

Retrieve all addresses associated with a specific stream using the `GetAddresses` endpoint.

### Request

```bash
curl -X GET "https://api.moralis-streams.com/streams/evm/{streamId}/address?limit=100" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY"
```

### Response

```json
{
  "result": [
    "0xCFDF6Aaae9f6B927E3736FBD327853B622c5060E",
    "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
    "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
  ],
  "cursor": "<cursor_value>",
  "total": 3
}
```

### Pagination

When the stream has many addresses, use the `cursor` from the response to fetch the next page:

```bash
curl -X GET "https://api.moralis-streams.com/streams/evm/{streamId}/address?limit=100&cursor={cursor}" \
  -H "accept: application/json" \
  -H "X-API-Key: $MORALIS_API_KEY"
```

## Best Practices

### 1. Minimize Stream Count

Create as few streams as possible and attach addresses to existing streams. This reduces complexity and improves manageability.

**Example:** Instead of creating separate streams for monitoring wallets on Ethereum and Polygon, create one stream with multiple chain IDs:

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "webhookUrl": "https://your-server.com/webhook",
    "description": "Monitor multiple wallets across chains",
    "chainIds": ["0x1", "0x89"],
    "includeNativeTxs": true,
    "includeContractLogs": true
  }'
```

Then add addresses:

```bash
curl -X POST "https://api.moralis-streams.com/streams/evm/{streamId}/address" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "address": [
      "0xCFDF6Aaae9f6B927E3736FBD327853B622c5060E",
      "0xAb5801a7D398351b8bE11C439e05C5B3259aeC9B",
      "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
    ]
  }'
```

### 2. Batch Address Operations

When managing many addresses, batch add/remove operations in a single request rather than making multiple individual requests.

### 3. Use Descriptive Tags

When creating streams that will hold multiple addresses, use descriptive tags to identify them:

```bash
curl -X PUT "https://api.moralis-streams.com/streams/evm" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "webhookUrl": "https://your-server.com/webhook",
    "description": "High-value whale wallet monitoring",
    "tag": "whale-monitoring",
    "chainIds": ["0x1"]
  }'
```

The tag will be included in webhook payloads, making it easier to identify which stream triggered the webhook.

## References

- [Monitor Multiple Addresses Documentation](https://docs.moralis.com/streams-api/evm/monitor-multiple-addresses)
- [AddAddressToStream](./AddAddressToStream.md) - Add addresses to a stream
- [DeleteAddressFromStream](./DeleteAddressFromStream.md) - Remove addresses from a stream
- [ReplaceAddressFromStream](./ReplaceAddressFromStream.md) - Replace addresses in a stream
- [GetAddresses](./GetAddresses.md) - Get all addresses for a stream
- [CreateStream](./CreateStream.md) - Create a new stream
