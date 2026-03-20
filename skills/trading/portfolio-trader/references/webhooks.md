# SnapTrade Webhooks (docs.snaptrade.com/docs/webhooks)

Source: https://docs.snaptrade.com/docs/webhooks

## Key points
- Configure webhook listener in SnapTrade Dashboard.
- Verify authenticity via **Signature** header (HMAC SHA256 using client secret).
- Webhook secret is deprecated.
- Undeliverable webhooks retry with exponential backoff (up to 3 tries).

## Common event types
- USER_REGISTERED / USER_DELETED
- CONNECTION_ATTEMPTED / ADDED / DELETED / BROKEN / FIXED / UPDATED / FAILED
- NEW_ACCOUNT_AVAILABLE
- ACCOUNT_TRANSACTIONS_INITIAL_UPDATE / UPDATED
- ACCOUNT_REMOVED
- ACCOUNT_HOLDINGS_UPDATED

Refer to the official doc for full payload examples.
