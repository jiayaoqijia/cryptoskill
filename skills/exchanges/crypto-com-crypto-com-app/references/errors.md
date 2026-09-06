# Error Reference

This document covers error scenarios, API error codes, and recovery guidance. The scripts return structured errors — use this reference when the compact table in [SKILL.md](../SKILL.md) needs more context.

Error format:
```json
{"ok": false, "error": "error_code", "error_message": "Human-readable message"}
```

---

## Script Error Codes

These are the `error` values returned by the TypeScript scripts when a problem is caught before or after the API call.

### MISSING_ENV

**Cause:** `CDC_API_KEY` or `CDC_API_SECRET` environment variable is not set.

**Recovery:** Tell the user to set both variables in their terminal:
```bash
export CDC_API_KEY="your-api-key"
export CDC_API_SECRET="your-api-secret"
```

### API_ERROR

**Cause:** The API returned a non-200 HTTP status or the response body has `ok: false`.

**Recovery:** Report the `error_message` to the user. If the message is vague, suggest checking API key validity and account status.

### INVALID_ARGS

**Cause:** The script received bad or missing command-line arguments (wrong scope, missing symbol, malformed JSON, unknown trade type).

**Recovery:** The `error_message` includes correct usage. Show it to the user or fix the command and retry.

### QUOTATION_FAILED

**Cause:** The quotation request was rejected by the API. See the API error tables below for specific codes.

**Recovery:** Report the `error_message`. Suggest the user adjust trade parameters and try again.

### EXECUTION_FAILED

**Cause:** The order confirmation failed after a successful quotation. See the API error tables below for specific codes.

**Recovery:** Report the error. Suggest: "Check order status with 'Show recent trades' to verify whether the order was partially processed."

### API_KEY_NOT_FOUND

**Cause:** The API key does not exist or has already been revoked.

**Recovery:** Inform the user: "API key not found — it may have already been revoked or does not exist." The key is already inactive.

### UNKNOWN

**Cause:** An unexpected error (network failure, JSON parse error, script crash).

**Recovery:** Report the raw `error_message`. If it's a network issue, suggest checking connectivity.

---

## API Error Codes — Quotation

These errors can appear when requesting a quotation via `trade.ts quote`. They apply across purchase, sale, and exchange operations unless noted otherwise.

### Balance & Eligibility

| `error` | `error_message` | Applies to | Recovery |
|---------|-----------------|------------|----------|
| `not_enough_balance` | (none) | All | Insufficient funds. Check balances and reduce trade amount. |
| `unauthorized` | (none) | All | User account not approved for trading. Contact support. |
| `restricted_feature` | varies | All | Account has a feature restriction. The `error_message` explains which feature. |
| `not_eligible_for_prime` | "user is not eligible for prime" | All | User is not eligible for Prime benefits. Proceed without Prime. |

### Currency & Pair

| `error` | `error_message` | Applies to | Recovery |
|---------|-----------------|------------|----------|
| `invalid_currency` | (none) | Exchange | Currency code not recognized. Verify spelling via coin search. |
| `existing_currency_order_error` | varies (from QRE) | Exchange | An existing order for this currency pair is in progress. Wait or cancel it first. |
| `failed_to_create_quotation` | "failed to create quotation" | All | Internal quotation engine error. Retry in a moment. |

### Feature Availability

| `error` | `error_message` | Applies to | Recovery |
|---------|-----------------|------------|----------|
| `viban_purchase_not_enabled` | (none) | Purchase | Fiat-to-crypto purchase is not enabled for this account. |
| `bank_transfer_not_enabled` | (none) | Purchase, Sale | Bank transfer feature is not enabled. |
| `crypto_viban_not_enabled` | (none) | Sale | Crypto-to-fiat sale is not enabled for this account. |

### Authentication

| `error` | `error_message` | Applies to | Recovery |
|---------|-----------------|------------|----------|
| `invalid_passcode` | (none) | All | Passcode verification failed. |
| `passcode_not_set` | (none) | All | User has not set a passcode. HTTP 400. |

---

## API Error Codes — Order Confirmation

These errors can appear when confirming an order via `trade.ts confirm`. They apply across purchase, sale, and exchange operations unless noted otherwise.

### Quotation Issues

| `error` | `error_message` | Applies to | Recovery |
|---------|-----------------|------------|----------|
| `invalid_quotation` | (none) | All | Quotation has expired or was already used. Request a new quote. |
| `missing_parameter` | (none) | All | `quotation_id` was not provided. This is a script bug — report it. |

### Balance & Eligibility

| `error` | `error_message` | Applies to | Recovery |
|---------|-----------------|------------|----------|
| `not_enough_balance` | (none) | Exchange | Balance changed between quote and confirm. Check balances and re-quote. |
| `unauthorized` | (none) | Exchange | User account not approved. Contact support. |

### Transaction Failures

| `error` | `error_message` | Applies to | Recovery |
|---------|-----------------|------------|----------|
| `failed_to_create_transaction` | (none) | Sale | Internal error creating the transaction. Retry or contact support. |
| `failed_to_activate_prime_account` | "failed to activate prime account" | All | Prime account activation failed during order. Retry without Prime. |

### Feature Availability

| `error` | `error_message` | Applies to | Recovery |
|---------|-----------------|------------|----------|
| `bank_transfer_not_enabled` | (none) | Purchase | Bank transfer feature is not enabled for this account. |
| `restricted_feature` | varies | Exchange | Account has a feature restriction. The `error_message` explains which feature. |

---

## API Error Codes — API Keys

These errors can appear when interacting with API key endpoints (`trading-limit`, `revoke-key`). The `/v1/api-keys` path may return errors in either `{"ok": false, "error": "..."}` or `{"code": "...", "message": "..."}` format — the scripts handle both.

| `error` / `code` | `error_message` / `message` | Meaning | Recovery |
|-------------------|----------------------------|---------|----------|
| `key_not_active` | (none) | API key has been revoked or expired | Generate a new API key and update env vars |
| `api_key_not_found` | "not found" | Key doesn't exist or belongs to another user | Verify the correct API key is set in `CDC_API_KEY` |
| `invalid_scope` | (none) | One or more scopes in the request don't exist | Verify the API key has the required scopes |
| `invalid_expiration` | (none) | `expires_at` is in the past or more than 1 year out | Use a valid expiration date |
| `invalid_public_key` | (none) | Not a valid PEM-encoded Ed25519 public key | Provide a valid Ed25519 public key |
| `passcode_required` | (none) | Sensitive fields changed but no passcode provided | N/A for API-key-based trading |

**Note:** The `key_not_active` and `api_key_not_found` errors are the most relevant for this skill. If either appears during `trading-limit` or any other operation, the API key is no longer valid — the user must generate a new one.

---

## Dynamic Error Codes

Some API errors return dynamic codes and messages from internal subsystems. These will not match the exact strings above but follow the same `{"ok": false, "error": "...", "error_message": "..."}` format. Common categories:

| Pattern | Meaning |
|---------|---------|
| Limit / exceeded errors | Trade amount exceeds a limit (weekly, per-trade, or per-currency). Reduce amount or check `trading-limit`. |
| Currency disabled errors | The specific currency is temporarily disabled for trading. Try a different currency or wait. |
| Cooling-off / trade restriction | Account is in a cooling-off period after a security event. Wait for the period to end. |
| Finalized / cancelling errors | The order is already finalized or being cancelled. No action needed. |
| Risk / payment rejected | The transaction was rejected by risk assessment. Contact support if recurring. |
| Account inactive / not accessible | The target account is inactive. Verify account status. |
| Unsupported strategy / payout | The requested trade strategy or payout method is not supported. Use a different method. |

When the agent encounters a dynamic error code not listed above, report the `error` and `error_message` directly to the user.

---

## API HTTP Status Codes

The scripts handle these internally, but for reference:

| Status | Meaning |
|--------|---------|
| 200 | Success (must also check `ok: true` in body) |
| 400 | Bad request — invalid parameters |
| 401 | Unauthorized — invalid or missing API key |
| 403 | Forbidden — API key lacks required permissions |
| 404 | Endpoint not found |
| 429 | Rate limited — too many requests |
| 500 | Internal server error |
| 503 | Service unavailable — maintenance |

---

## Troubleshooting Checklist

If a command fails unexpectedly:

1. **Check env vars** — `echo $CDC_API_KEY` should return a value (not empty)
2. **Check API key status** — run `npx tsx ./scripts/account.ts trading-limit` (from the skill directory). If it returns successfully, the key is valid.
3. **Check network** — can the machine reach `https://wapi.crypto.com`?
4. **Check Node version** — `node --version` should be 18+
5. **Check timestamps** — system clock must be accurate for HMAC signing to work
