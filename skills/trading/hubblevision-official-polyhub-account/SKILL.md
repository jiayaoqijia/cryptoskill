---
name: polyhub-account
description: View Polyhub portfolio stats, fee history, and place manual orders with explicit confirmation and field validation.
---

# Polyhub Account

Version: v0.3.8

Use this skill when the user wants account-level data or manual trading actions on Polyhub.

## Requirements

- `POLYHUB_API_BASE_URL` is fixed to `https://polyhub.skill-test.bedev.hubble-rpc.xyz`.
- `POLYHUB_API_KEY` is set and starts with `phub_`.
- `curl` is available.
- `jq` is recommended.

If `POLYHUB_API_KEY` is missing, guide the user to register and apply for one first at `https://polyhub.hubble.xyz/`.
Recommended guidance:

1. Open Polyhub Web: `https://polyhub.hubble.xyz/`
2. Click the avatar menu.
3. Open `Skills API Key`.
4. Click `申请 API Key`.
5. Set:
   - `POLYHUB_API_BASE_URL`
   - `POLYHUB_API_KEY`

Suggested wording:

```text
API key is not configured yet, so I can't check your account details for now.

Please register first on PolyHub:
https://polyhub.hubble.xyz/

After registration, click your avatar in the top-right corner and open `Skills API Key` to apply.

Send me the generated key and I'll continue right away.
```

## Safety Rules

- Never print `POLYHUB_API_KEY`.
- For `place-order`, repeat the full order summary and wait for explicit confirmation before calling the API.
- Do not accept arbitrary JSON for order placement. Ask for minimal required fields first.
- Prefer `jq -n` for payload construction.

## Base Setup

```bash
BASE="https://polyhub.skill-test.bedev.hubble-rpc.xyz"
AUTH=(-H "Authorization: Bearer $POLYHUB_API_KEY" -H "Content-Type: application/json")
```

## Intent Mapping

- Portfolio overview: `GET /api/v1/portfolio/stats`
- Fee history: `GET /api/v1/user/fees`
- Sell position by token ID: `POST /api/v1/positions/sell`
- Manual order placement: `POST /api/v1/place-order`

## Common Calls

### Portfolio stats

Field semantics:

- `positionsValue`: official Polymarket positions value
- `availableBalance`: official USDC balance minus `unsettledFees`
- `totalPnL`: official Polymarket total PnL
- `unsettledFees`: unsettled Polyhub fees in USDC
- `investedCapital`: Polyhub-calculated invested capital for copy-task history

UI alignment:

- `poly_copy` portfolio header uses this endpoint
- avatar dropdown `USDC Balance` uses `availableBalance`
- avatar dropdown `Account Value` uses `availableBalance + positionsValue`

```bash
curl -sS --fail-with-body "${AUTH[@]}" \
  "$BASE/api/v1/portfolio/stats"
```

### Fee history

Validation:

- `limit` must be positive.
- `offset` must be zero or greater.

```bash
curl -sS --fail-with-body "${AUTH[@]}" \
  "$BASE/api/v1/user/fees?limit=20&offset=0"
```

### Place order

Always ask for:

- `tokenId`
- `size`
- `side`
- `apiKey`
- `apiSecret`
- `apiPassphrase`

Always confirm:

- `organizationId`
- `signWith`
- `safeAddress`

Decision rules:

- If the user does not specify a price, prefer `isMarketOrder=true`.
- If the user specifies a target price, send a limit order with `price` and `isMarketOrder=false`.
- Normalize `side` to uppercase.

```bash
PAYLOAD="$(jq -n \
  --arg organizationId "..." \
  --arg signWith "..." \
  --arg safeAddress "0x..." \
  --arg tokenId "..." \
  --arg side "BUY" \
  --arg apiKey "..." \
  --arg apiSecret "..." \
  --arg apiPassphrase "..." \
  --argjson size 10 \
  --argjson isMarketOrder true \
  '{
    organizationId: $organizationId,
    signWith: $signWith,
    safeAddress: $safeAddress,
    tokenId: $tokenId,
    size: $size,
    side: $side,
    isMarketOrder: $isMarketOrder,
    apiKey: $apiKey,
    apiSecret: $apiSecret,
    apiPassphrase: $apiPassphrase
  }')"

curl -sS --fail-with-body "${AUTH[@]}" \
  -X POST "$BASE/api/v1/place-order" \
  -d "$PAYLOAD"
```

## Sell Position

Sell the entire position for a given token ID. Partial sell is not supported.

Required field: `TokenId`

Before calling: confirm with the user. This action is irreversible.

```bash
PAYLOAD="$(jq -n \
  --arg TokenId "..." \
  '{TokenId: $TokenId}')"

curl -sS --fail-with-body "${AUTH[@]}" \
  -X POST "$BASE/api/v1/positions/sell" \
  -d "$PAYLOAD"
```

Response: `success`, `totalAmount`, `soldPositions[]` (with `marketTitle`, `outcome`, `amount`, `price`, `totalPnl`, `marketUrl`), `skippedPositions[]` (with `reason`).

Use `/positions/sell` when the user wants to sell a specific position directly by token ID. Use `/copy-tasks/{taskId}/sell` when managing positions within a copy task.

## Error Handling

- `400`: invalid payload
- `401`: missing or invalid API key
- `404`: delegated access not registered
- `5xx`: server error
