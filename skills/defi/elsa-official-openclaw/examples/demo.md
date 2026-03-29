# Elsa x402 OpenClaw Demo

This document demonstrates typical usage patterns for the Elsa x402 OpenClaw skill-pack.

## 1. Token Search

Search for tokens across supported blockchains:

```bash
npx tsx scripts/index.ts elsa_search_token '{"query": "USDC", "limit": 5}'
```

Expected output:
```json
{
  "ok": true,
  "data": {
    "tokens": [
      {
        "name": "USD Coin",
        "symbol": "USDC",
        "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "chain": "base",
        "decimals": 6
      }
    ]
  },
  "billing": {
    "estimated_cost_usd": 0.001,
    "payment_required": true,
    "receipt": null,
    "protocol": "x402-v1-compat"
  },
  "meta": {
    "latency_ms": 245,
    "endpoint": "/api/search_token",
    "timestamp": "2024-01-15T10:30:00.000Z"
  }
}
```

## 2. Portfolio Analysis

Get portfolio overview for a wallet:

```bash
npx tsx scripts/index.ts elsa_get_portfolio '{"wallet_address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"}'
```

## 3. Budget Status Check

Check how much budget remains:

```bash
npx tsx scripts/index.ts elsa_budget_status '{}'
```

Expected output:
```json
{
  "ok": true,
  "data": {
    "spent_today_usd": 0.012,
    "remaining_today_usd": 1.988,
    "calls_last_minute": 3,
    "last_calls": []
  }
}
```

## 4. Swap Quote

Get a quote before executing:

```bash
npx tsx scripts/index.ts elsa_get_swap_quote '{
  "from_chain": "base",
  "from_token": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "from_amount": "100",
  "to_chain": "base",
  "to_token": "0x4200000000000000000000000000000000000006",
  "wallet_address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "slippage": 0.5
}'
```

## 5. Safe Swap Execution Flow

### Step 1: Dry Run (Always Do This First!)

```bash
npx tsx scripts/index.ts elsa_execute_swap_dry_run '{
  "from_chain": "base",
  "from_token": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "from_amount": "100",
  "to_chain": "base",
  "to_token": "0x4200000000000000000000000000000000000006",
  "wallet_address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "slippage": 0.5
}'
```

Response includes `confirmation_token`:
```json
{
  "ok": true,
  "data": {
    "pipeline_id": "pip_abc123",
    "status": "dry_run_complete"
  },
  "confirmation_token": "abc123xyz...",
  "confirmation_expires_in_seconds": 600
}
```

### Step 2: Review and Confirm (Requires ELSA_ENABLE_EXECUTION_TOOLS=true)

```bash
npx tsx scripts/index.ts elsa_execute_swap_confirmed '{
  "from_chain": "base",
  "from_token": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  "from_amount": "100",
  "to_chain": "base",
  "to_token": "0x4200000000000000000000000000000000000006",
  "wallet_address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "slippage": 0.5,
  "confirmation_token": "abc123xyz..."
}'
```

### Step 3: Complete Pipeline (If Needed)

```bash
npx tsx scripts/index.ts elsa_pipeline_run_and_wait '{
  "pipeline_id": "pip_123456789",
  "timeout_seconds": 120,
  "mode": "local_signer"
}'
```

## Error Handling

All errors return structured JSON:

```json
{
  "ok": false,
  "error": {
    "code": "BUDGET_EXCEEDED",
    "message": "Daily budget limit reached. Spent: $2.00, Limit: $2.00",
    "details": {
      "limit": 2.00,
      "requested": 0.02,
      "spent": 2.00
    }
  }
}
```

## Common Error Codes

| Code | Description |
|------|-------------|
| `BUDGET_EXCEEDED` | Per-call or daily budget limit reached |
| `RATE_LIMIT_EXCEEDED` | Too many calls in the last minute |
| `EXECUTION_DISABLED` | Execution tools not enabled |
| `CONFIRMATION_REQUIRED` | Need to run dry-run first |
| `CONFIRMATION_INVALID` | Token expired, not found, or params mismatch |
| `UPSTREAM_HTTP_ERROR` | Elsa API returned an error |
| `PIPELINE_TIMEOUT` | Pipeline execution timed out |
| `PIPELINE_TASK_ERROR` | A pipeline task failed |
| `VALIDATION_ERROR` | Invalid input parameters |
