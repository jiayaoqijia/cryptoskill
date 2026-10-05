---
name: ucash-sell
description: Monetize an AI agent with agents.u.cash - get an API key, set receive wallets, create priced 402 resources, verify settlement webhooks, and test the buyer flow end to end. Use when the user wants to charge for access to an agent/API/content, sell something per-call, or accept crypto payments non-custodially.
---

# Sell access with agents.u.cash (402 Online)

Non-custodial: buyers pay the seller's own wallet address on-chain; the platform only issues the
HTTP 402 challenge, detects the payment, and settles. Works instantly at $0.

## Flow (do these in order, stop and show the user each result)

### 1. Key (skip if UXC_API_KEY is already exported)

```bash
curl -s -X POST https://agents.u.cash/v1/signup -H 'Content-Type: application/json' \
  -d '{"username":"my-agent","password":"long-random-pass"}'
# -> response.api_key  (never print the full key back; first6/last4 max)
```

Store it: `export UXC_API_KEY=...`. Email verification (~$5 credit) is optional and later.

### 2. Receive wallet (where funds land)

```bash
curl -s -X POST https://agents.u.cash/v1/wallets -H "X-Api-Key: $UXC_API_KEY" \
  -H 'Content-Type: application/json' -d '{"asset":"btc","address":"bc1q..."}'
```

One call per coin (`eth`, `usdc`, `sol`, `trx`, ...). Custom ERC-20/TRC-20/SPL/TON tokens:
`POST /v1/custom-tokens`. No wallet yet? Create a `test:true` resource (step 3) to try the flow at $0.

### 3. Create the priced resource

```bash
curl -s -X POST https://agents.u.cash/v1/resources -H "X-Api-Key: $UXC_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"amount":0.05,"currency":"USD"}'
# -> response.res_id + response.checkout_url (the buyer door)
```

Options: `accepted_assets:["btc","eth"]` to restrict coins; `test:true` = sandbox (settles at $0,
excluded from earnings); `webhook_url` = settlement callback (HMAC-signed, secret shown once).

### 4. Show the buyer side (what a payer sees)

- Human: open `https://agents.u.cash/r/{res_id}` (or the checkout_url).
- Agent: `GET https://agents.u.cash/r/{res_id}` with `Accept: application/json` → HTTP 402 +
  `accepts[]` (per-coin address + exact amount) or via the hosted keyless MCP
  (`https://mcp.u.cash/`, tool `uxc_view_door`).
- Optional per-caller spend cap: `PUT /v1/resources?res_id=... {"max_per_caller":{"amount":10,"window_hours":24}}`.

### 5. Webhook verification (when a webhook_url is set)

Verify `X-Webhook-Signature` (`t=<unix>,v1=<hex>`) as HMAC-SHA256 of `"<t>.<raw_body>"` with the
secret from step 3. Use the EXACT raw body bytes; reject age > 300s; dedupe by event_id. The MCP
tool `uxc_verify_webhook_signature` (local, no network) does this check for you.

### 6. Watch settlement

```bash
curl -s "https://agents.u.cash/r/{res_id}?status=1"          # settled:true/false
curl -s https://agents.u.cash/v1/settlements -H "X-Api-Key: $UXC_API_KEY"   # earnings log
```

## Sandbox test loop (proves the whole rail at $0)

Create with `{"amount":0.01,"test":true,"test_confirmations":2}` → view the door for a
`challengeId` → `POST /v1/simulate-payment {"challengeId":"...","confirmations":1}` (pending) →
`POST /v1/verify {"challengeId":"...","hash":"<from simulate>"}` (settles) → `?status=1` shows
`settled:true`.

## Mounting the full 86-tool surface

`claude mcp add agents --env UXC_API_KEY=... -- php <repo>/mcp/server.php` (repo:
github.com/UdotCash/agents; Docker: `ghcr.io/udotcash/agents-u-cash-mcp`). Full catalog:
https://agents.u.cash/mcp
