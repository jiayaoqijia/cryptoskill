# Streams API FAQ

Frequently asked questions about the Moralis Streams API, covering production status, pricing, configurations, and usage details.

## Is Streams API in production?

Yes, the Streams API is in production.

## How are Streams priced?

Streams consume Compute Units similar to other Moralis APIs. Charges are based on **records**:

- A **record** = 1 transaction (`txs`) + 1 log (`logs`) + 1 internal transaction (`txsInternal`)
- Charge: **50 Compute Units per record**
- **Only confirmed webhooks are charged** (unconfirmed requests are free)
- Check the `x-records-charged` header in webhook responses to see how many records were charged

```javascript
// Example webhook headers
headers: {
  'x-region': 'us-west-2',
  'x-queue-size': '0',
  'x-records-charged': '20',  // 20 records = 1000 Compute Units
  'x-signature': '0x...'
}
```

## Can I disable unconfirmed webhook requests?

No, you cannot disable unconfirmed webhook requests. However, **you are not charged for unconfirmed requests** — only confirmed webhooks incur charges.

## Why do I receive two requests for the same transaction?

You receive two requests:
1. **Unconfirmed transaction** — sent immediately when transaction is detected
2. **Confirmed transaction** — sent after the required number of confirmations

You are **only charged for the confirmed transaction**.

## After how many blocks is a transaction considered confirmed?

Confirmation depth varies by chain:

| Chain | Chain ID | Blocks Until Confirmed |
|-------|----------|----------------------|
| Ethereum | `0x1` | 12 |
| Polygon | `0x89` | 100 |
| BSC | `0x38` | 18 |
| Arbitrum | `0xa4b1` | 18 |
| Base | `0x2105` | 100 |
| Optimism | `0xa` | 500 |
| Avalanche | `0xa86a` | 100 |
| Fantom | `0xfa` | 100 |

For a complete per-chain table, see [DeliveryGuarantees.md](DeliveryGuarantees.md).

## How many addresses can I add to a stream?

| Plan | Address Limit |
|------|---------------|
| Starter Plan | Up to 10,000 addresses |
| Pro / Business | Up to 50,000 addresses |
| Enterprise | Fully customized (up to 100M addresses) |

Contact `hello@moralis.io` to increase your limit.

## How many separate streams can I create?

| Plan | Stream Limit |
|------|--------------|
| Free Plan | 1 active stream |
| Paid Plans | Up to 200 active streams |

Each stream can support listening to millions of addresses in a single configuration. Contact `hello@moralis.io` if you need more streams.

## Are events lost when updating a stream or its filters?

**No**, no events are lost when a stream or its filters are updated.

## Is there a limit on how many filters I can add to a stream?

**No**, there is no limit on the number of filters you can add to a stream.

## Does filter complexity affect delivery speed?

**No**, the complexity of filters (even with 500k+ address filters) does **not** affect stream delivery speed.

## Why is the ABI required to listen to events?

The ABI ensures you receive data for the **exact event** you want to listen to. For example:

- ERC20 Transfer: `Transfer(address from, address to, uint256 value)`
- ERC721 Transfer: `Transfer(address from, address to, uint256 tokenId)`

Both have the same signature `Transfer(address,address,uint256)` but represent different events. Without the ABI, we cannot distinguish between them.

The ABI also accounts for differences in `indexed` parameters across contracts.

## Why don't I see all the internal transactions from my transaction?

If you're listening to a "Wallet Transfer" stream:

1. We only provide internal transactions where there is a **transfer of value**
2. We only provide internal transactions that mention the **addresses you're watching**

Ensure you have selected to receive Internal Transactions (`txsInternal`) in your Stream configuration.

## Why don't I see all the logs from my transaction?

Logs are filtered based on your Stream configuration. For a "Wallet Transfer" stream:

- We only provide logs where your address is mentioned in the **Topics** or **Data**

Ensure you have selected to receive Contract Interactions (`logs`) in your Stream configuration.

## What is a record?

A **record** is the basic unit for calculating Streams usage:

- 1 record = 1 transaction OR 1 log OR 1 internal transaction
- Total records = `txs + logs + txsInternal` in the webhook response
- Cost: **50 Compute Units per record**
- Only confirmed blocks are charged (unconfirmed has `x-records-charged: 0`)

## What happens if my webhook endpoint is down?

Moralis retries with exponential backoff (1 min → 10 min → 1 hour → 2 hours → 6 hours → 12 hours → 24 hours). If the webhook success rate drops below **70%** or the event queue exceeds **10,000**, the stream enters `error` state and delivery is paused.

If the stream remains in `error` state for **24 hours**, it becomes `terminated` and is unrecoverable. See [ErrorHandling.md](ErrorHandling.md) for complete details.

## Can a terminated stream be resumed?

**No.** A terminated stream cannot be resumed, restarted, or recovered. You must create a new stream. This is why monitoring webhook health is critical — see [ErrorHandling.md](ErrorHandling.md) for best practices.

## What is the rate limit for adding addresses to a stream?

**5 requests per 5 minutes** for address addition endpoints. To stay within limits, use batch operations — send multiple addresses in a single request using the `addressToAdd` array (up to 50,000 addresses per batch).

```bash
curl -X POST "https://api.moralis-streams.com/streams/evm/STREAM_ID/address" \
  -H "X-API-Key: $MORALIS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"addressToAdd": ["0x1234...", "0x5678...", "0x9abc..."]}'
```

## Need More Help?

- Slack channel for enterprise customers
- Community forum: https://forum.moralis.io/
- Email: hello@moralis.io
