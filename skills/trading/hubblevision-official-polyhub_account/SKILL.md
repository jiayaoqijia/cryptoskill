---
name: polyhub_account
description: View portfolio stats on Polyhub using an API key.
---

# Polyhub Account Skill

Version: v0.3.8

## When to use

Use this skill when the user asks about:

- Portfolio overview or stats
- Selling a position by token ID

## Requirements

- `POLYHUB_API_BASE_URL` is fixed to `https://polyhub.skill-test.bedev.hubble-rpc.xyz`.
- `POLYHUB_API_KEY` — API key (must start with `phub_`)
- `curl` must be available in the runtime environment.
- `jq` is strongly recommended for building JSON payloads safely.

If `POLYHUB_API_KEY` is missing, guide the user to register and apply for one first at `https://polyhub.hubble.xyz/`.
Recommended guidance:

1. Open Polyhub Web: `https://polyhub.hubble.xyz/`
2. Click the avatar menu.
3. Open `Skills API Key`.
4. Click `申请 API Key`.
5. Set both `POLYHUB_API_BASE_URL` and `POLYHUB_API_KEY`.

Suggested wording:

```text
API key is not configured yet, so I can't check your account details for now.

Please register first on PolyHub:
https://polyhub.hubble.xyz/

After registration, click your avatar in the top-right corner and open `Skills API Key` to apply.

Send me the generated key and I'll continue right away.
```

## Safety rules

- Never print `POLYHUB_API_KEY` in the output.
- Prefer building JSON with `jq -n` instead of interpolating raw shell strings.
- For sell actions (`POST /api/v1/positions/sell`), repeat the token ID and confirm with the user before calling the API.

## Tools

Use the `bash` tool to call the API with `curl`.

## Fast Path

For common intents, map user requests like this:

- “看资产统计” -> `GET /api/v1/portfolio/stats`
- “卖出这个仓位” / “sell this position” -> `POST /api/v1/positions/sell`

### Curl base setup

```bash
BASE="https://polyhub.skill-test.bedev.hubble-rpc.xyz"
AUTH=(-H "Authorization: Bearer $POLYHUB_API_KEY" -H "Content-Type: application/json")
```

---

## Portfolio

### Action: Get portfolio stats

- `GET /api/v1/portfolio/stats`

Returns aggregated portfolio statistics for the authenticated user.

Current field semantics:

- `positionsValue`: official Polymarket positions value
- `availableBalance`: official USDC balance minus `unsettledFees`
- `totalPnL`: official Polymarket total PnL
- `unsettledFees`: unsettled Polyhub fees in USDC
- `investedCapital`: Polyhub-calculated invested capital for copy-task history

Current UI alignment in `poly_copy`:

- Portfolio page top stats use this endpoint
- Avatar dropdown `USDC Balance` uses `availableBalance`
- Avatar dropdown `Account Value` uses `availableBalance + positionsValue`

```bash
curl -sS --fail-with-body "${AUTH[@]}" "$BASE/api/v1/portfolio/stats"
```

---

## Sell Position

### Action: Sell position by token ID

- `POST /api/v1/positions/sell`
- Sells the **entire** position for the specified token. Partial sell is not supported.

Required field: `TokenId` (the Polymarket token ID of the position to sell)

Before calling: repeat the token ID to the user and confirm. This action is irreversible.

Minimum fields to ask:

- Always ask: `TokenId`

```bash
PAYLOAD="$(jq -n \
  --arg TokenId "..." \
  '{TokenId: $TokenId}')"

curl -sS --fail-with-body "${AUTH[@]}" -X POST "$BASE/api/v1/positions/sell" \
  -d "$PAYLOAD"
```

Response contains:

- `success`: whether the sell completed
- `totalAmount`: total USDC amount received
- `soldPositions`: array of sold positions, each with:
  - `marketTitle`, `outcome`: which market and side was sold
  - `amount`: shares sold
  - `price`: execution price
  - `currentPrice`: market price at time of sale
  - `pnl`, `realizedPnl`, `unrealizedPnl`, `totalPnl`: PnL breakdown
  - `value`: USDC value of the sold position
  - `marketUrl`: link to the market on Polymarket
- `skippedPositions`: array of positions that could not be sold, each with:
  - `marketTitle`, `outcome`, `amount`: what was skipped
  - `reason`: why it was skipped

Present results clearly:

```
✅ 卖出成功
总金额: ${totalAmount} USDC

已卖出:
  - {marketTitle} ({outcome}): {amount} shares @ {price}, PnL ${totalPnl}

跳过:
  - {marketTitle} ({outcome}): {reason}
```

### Difference from copy-task sell

| | `POST /api/v1/positions/sell` | `POST /api/v1/copy-tasks/{taskId}/sell` |
|---|---|---|
| Scope | Account-level, by token ID | Task-level, by task + market |
| Partial sell | No (sells all) | Yes (`amount` field) |
| Required params | `TokenId` | `taskId` + `marketId` or `conditionId` |
| PnL in response | Yes (detailed breakdown) | No |
| When to use | User wants to sell a specific position directly | User wants to manage positions within a copy task |

Guidance:

- If the user says "卖掉这个仓位" or provides a token ID, use `/positions/sell`.
- If the user says "卖掉这个任务的某个持仓" or references a copy task, use `/copy-tasks/{taskId}/sell`.
- If the user wants to sell ALL positions in a task, use `/copy-tasks/{taskId}/sell-all`.

---

## Error handling

- `401`: API key missing/invalid/expired/disabled. Ask user to check or regenerate key.
- `400`: Invalid request payload. Check required fields.
- `404`: Delegated access not registered for the given `organizationId`.
- `405`: Wrong HTTP method.
- `5xx`: Server error. Retry once with backoff; if still failing, report response body.
