# Error Handling, Retries, and Stream Lifecycle

Complete reference for stream error states, retry behavior, lifecycle management, re-org handling, and rate limits.

## Retry Schedule

When a webhook delivery fails (non-2xx response or timeout), Moralis retries with exponential backoff:

| Attempt | Interval After Failure |
|---------|----------------------|
| 0 | 1 minute |
| 1 | 10 minutes |
| 2 | 1 hour |
| 3 | 2 hours |
| 4 | 6 hours |
| 5 | 12 hours |
| 6 | 24 hours |

After all retries are exhausted (7 attempts over ~45 hours), the webhook is marked as permanently failed.

## Webhook Success Rate

Each stream tracks a webhook success rate:

- **Starts at:** 100%
- **On failure:** -1% per failed delivery
- **On success:** +1% per successful delivery
- **Range:** Capped between 0% and 100%

## Stream States

### `active`

Normal operating state. The stream evaluates blocks and delivers webhooks.

### `paused`

Manually paused by the user. No blocks are evaluated, no webhooks sent. Resume by setting status to `active`.

### `error`

**Triggered automatically when:**
- Webhook success rate drops below **70%**, OR
- The event queue exceeds **10,000 pending events**

**Behavior in error state:**
- Webhook delivery is **paused**
- Blocks are still evaluated and events are queued
- The stream can recover if the webhook endpoint becomes healthy again

### `terminated`

**Triggered automatically after 24 hours in error state.**

**This is unrecoverable.** A terminated stream cannot be resumed, restarted, or recovered. You must create a new stream.

## Stream Lifecycle Diagram

```
active ──(success rate <70% or queue >10k)──> error
  ^                                              │
  │                                              │ (24 hours)
  │                                              v
  └──(manual)──> paused                      terminated
                   │                         (unrecoverable)
                   └──(manual)──> active
```

## Re-org Handling

Moralis automatically handles blockchain reorganizations (re-orgs):

1. **Detection**: Moralis monitors for chain re-orgs in real-time
2. **Invalidation**: Events from dropped blocks are invalidated
3. **Replacement**: New webhooks are sent with the correct data from the canonical chain
4. **Dual delivery**: You may receive `confirmed: false` for the original block and then updated data once the re-org resolves

**Best practice:** Always use the `confirmed: true` webhook as the source of truth. Design your handlers to gracefully handle re-delivered or invalidated events.

## Rate Limits

### Adding Addresses

- **Limit:** 5 requests per 5 minutes for adding addresses to a stream
- **Recommendation:** Use batch operations — send multiple addresses in a single `POST /streams/evm/{id}/address` call using the `addressToAdd` array
- **Maximum per batch:** 50,000 addresses per request

### Stream Reloads

When you update a stream configuration (ABI, topic0, filters, etc.), the stream reloads asynchronously. During reload:
- Existing webhook deliveries continue
- New configuration takes effect once reload completes
- No events are lost during reload

## Recovery from Failed Webhooks

If webhooks have failed and need to be replayed:

### 1. Find Failed Webhooks

```bash
curl "https://api.moralis-streams.com/history/logs?limit=100&deliveryStatus=failed" \
  -H "X-API-Key: $MORALIS_API_KEY"
```

### 2. Replay a Specific Block

```bash
curl -X POST "https://api.moralis-streams.com/streams/evm/{chainId}/block-to-webhook/{blockNumber}/{streamId}" \
  -H "X-API-Key: $MORALIS_API_KEY"
```

### 3. Replay from History

```bash
curl -X POST "https://api.moralis-streams.com/history/replay/{streamId}/{historyId}" \
  -H "X-API-Key: $MORALIS_API_KEY"
```

See [ReplayFailedWebhooks.md](ReplayFailedWebhooks.md) for complete replay procedures.

## Best Practices

1. **Return 200 quickly** — Process webhook data asynchronously. Return a 2xx response immediately to avoid timeouts.
2. **Monitor success rate** — Track the `retries` field in webhook payloads. If you see retries > 0 frequently, investigate your endpoint health.
3. **Set up health checks** — Ensure your webhook endpoint is highly available. A brief outage can cascade into error state.
4. **Use batch address operations** — Stay within rate limits by batching address additions.
5. **Have a recovery plan** — Know how to replay failed webhooks before you need to.
6. **Don't ignore terminated state** — If a stream terminates, you must create a new one. There is no way to recover it.
