---
name: require-an-idempotency-key-for-write-tools
description: Use when an agent may retry a write after a timeout or ambiguous failure. Send a stable idempotency key so a duplicate attempt cannot create a second record.
---

# Require an idempotency key for write tools

When a write times out you cannot tell whether it landed. Without a key, the safe-looking retry becomes a duplicate charge; with one, the retry is a no-op the server dedupes.

## Procedure

1. Derive the key deterministically from the logical operation, not from a random or time value: `sha256(f"{endpoint}:{account}:{ref}")`.
2. Reuse the same key across every retry of the same operation; a fresh key per attempt defeats the purpose.
3. Use a fresh key only when the logical operation changes — a new invoice, a new row, a new payment.
4. Send it in the header the API documents (`Idempotency-Key`) and record it in the action log beside the call.
5. On timeout, retry with the same key. On success, keep the key for the expected retention window (often 24h) before reuse.
6. Confirm the destination actually dedupes: a key field that is only stored and never checked is decoration.
7. For batch fan-out, key each item by its own identity, not by the batch, so a partial retry only re-sends the missing items.
8. Read back after a retry when the store cannot confirm dedupe, and reconcile by the key.

```bash
KEY=$(printf '%s' "invoice:$ACCT:$REF" | shasum -a 256 | cut -c1-32)
curl -sS -X POST "$API/invoices" -H "Idempotency-Key: $KEY" -d @"$BODY"
# a retry with the identical $KEY returns the original result rather than a second invoice
```

## Pitfalls

- Generating the key once per process and reusing it for unrelated writes, collapsing them into one.
- Adding a timestamp or nonce to the key, so every retry looks like a new operation.
- Assuming dedupe without testing it: fire the same key twice and confirm only one record exists.
- Retrying a non-idempotent endpoint that has no key support without a read-back reconciliation.
- Keying a batch as a whole, so one failed item forces re-sending the successful ones.
- Forgetting to persist the key, so a resumed run cannot reuse it after a crash.

## Verification

    for i in 1 2; do curl -sS -X POST "$API/invoices" -H "Idempotency-Key: $KEY" -d @"$BODY" >/dev/null; done; curl -sS "$API/invoices?ref=$REF" | jq 'length'   # must print 1

Report the key derivation, the number of attempts, and the destination record count confirmed at 1.
