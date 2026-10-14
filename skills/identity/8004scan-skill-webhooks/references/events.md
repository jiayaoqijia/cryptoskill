# Webhook Event Types

## Event Overview

| Event | Description |
|-------|-------------|
| `validation.requested` | A validation request is submitted for an agent |
| `validation.completed` | A validator submits their attestation response |
| `feedback.received` | New feedback is submitted for an agent |
| `feedback.revoked` | Existing feedback is revoked by its submitter |
| `star.received` | An agent receives a star rating (tag: "starred") |
| `star.removed` | A star rating is removed |

## Payload Schemas

### validation.requested

Triggered when someone requests a third-party validation for an agent.

```json
{
  "event": "validation.requested",
  "timestamp": "2026-03-16T12:00:00Z",
  "data": {
    "chainId": 8453,
    "tokenId": 17,
    "agentId": "8453:17",
    "requester": "0x1234...abcd",
    "validator": "0x5678...ef01",
    "transactionHash": "0x..."
  }
}
```

### validation.completed

Triggered when a validator submits their attestation response.

```json
{
  "event": "validation.completed",
  "timestamp": "2026-03-16T12:05:00Z",
  "data": {
    "chainId": 8453,
    "tokenId": 17,
    "agentId": "8453:17",
    "validator": "0x5678...ef01",
    "score": 85,
    "proof": "0x...",
    "transactionHash": "0x..."
  }
}
```

### feedback.received

Triggered when new feedback is submitted for an agent.

```json
{
  "event": "feedback.received",
  "timestamp": "2026-03-16T12:10:00Z",
  "data": {
    "chainId": 8453,
    "tokenId": 17,
    "agentId": "8453:17",
    "feedbackId": 42,
    "submitter": "0xabcd...1234",
    "value": 80,
    "decimals": 0,
    "tag": "starred",
    "payload": "",
    "transactionHash": "0x..."
  }
}
```

### feedback.revoked

Triggered when feedback is revoked by the original submitter.

```json
{
  "event": "feedback.revoked",
  "timestamp": "2026-03-16T12:15:00Z",
  "data": {
    "chainId": 8453,
    "tokenId": 17,
    "agentId": "8453:17",
    "feedbackId": 42,
    "submitter": "0xabcd...1234",
    "transactionHash": "0x..."
  }
}
```

### star.received

Triggered when an agent receives a star rating (feedback with tag "starred" and positive value).

```json
{
  "event": "star.received",
  "timestamp": "2026-03-16T12:20:00Z",
  "data": {
    "chainId": 8453,
    "tokenId": 17,
    "agentId": "8453:17",
    "submitter": "0xabcd...1234",
    "value": 100,
    "transactionHash": "0x..."
  }
}
```

### star.removed

Triggered when a star rating is removed (revocation of a "starred" feedback).

```json
{
  "event": "star.removed",
  "timestamp": "2026-03-16T12:25:00Z",
  "data": {
    "chainId": 8453,
    "tokenId": 17,
    "agentId": "8453:17",
    "submitter": "0xabcd...1234",
    "transactionHash": "0x..."
  }
}
```

## Common Fields

All event payloads share these fields:

| Field | Type | Description |
|-------|------|-------------|
| `event` | string | Event type identifier |
| `timestamp` | string | ISO 8601 timestamp of event |
| `data.chainId` | number | Blockchain network ID |
| `data.tokenId` | number | Agent token ID |
| `data.agentId` | string | Formatted as `{chainId}:{tokenId}` |
| `data.transactionHash` | string | On-chain transaction hash |

## Subscribing to Events

When registering a webhook, specify which events to receive:

```bash
# Subscribe to all feedback events
curl -s -X POST "https://8004scan.io/api/v1/webhooks/register" \
  -H "X-Access-Token: $EIGHTSCAN_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "webhook_url": "https://myserver.com/hook",
    "events": ["feedback.received", "feedback.revoked"]
  }' | jq .
```

To receive all events, list them all:

```json
{
  "events": [
    "validation.requested",
    "validation.completed",
    "feedback.received",
    "feedback.revoked",
    "star.received",
    "star.removed"
  ]
}
```
