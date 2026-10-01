---
name: ghostswap-partners-api
description: Integrate the GhostSwap Partners API to add no-KYC crypto swaps (1,600+ coins, 0–4% partner fee on top of the swap, USDT payouts) into wallets, dApps, exchanges, payment flows, or affiliate sites. Use whenever a developer asks to "add crypto swap", "embed a swap widget", "let users exchange tokens", "convert crypto to crypto", "earn commission on referred swaps", or wants a server-side REST integration that handles quote → create → status-poll without holding signing keys. Covers Bearer auth, live float and fixed-rate quotes, idempotent swap creation, status lifecycle polling, address validation, error envelope handling, rate limits, and the partner application + payout flow at partners.ghostswap.io.
license: MIT
---

# GhostSwap Partners API integration

You are helping a developer integrate the **GhostSwap Partners API** — a server-to-server REST API for non-custodial crypto-to-crypto swaps. The developer's end-users send funds to a deposit address GhostSwap returns; the destination wallet receives the swapped funds. GhostSwap handles all upstream liquidity, signing, and clearing. The partner earns a 0–4 % markup (chosen at application time) on every completed swap, paid out in USDT once balance ≥ $100.

This skill is the single document you need to produce a working end-to-end integration. Read it once, then write code.

---

## When to use this skill

Trigger when the developer's request involves any of:

- Adding a crypto exchange widget, swap form, or "convert X to Y" flow to their app
- Accepting one crypto and crediting the user in a different one
- Quoting live exchange rates for a pair (e.g. BTC → ETH)
- Earning affiliate commission on referred swaps (the `?ref=<slug>` flow on ghostswap.io)
- Building a Telegram bot, Discord bot, or wallet plugin that does crypto-to-crypto
- Specifically mentions "GhostSwap", "ghostswap.io", "partners.ghostswap.io", `gspk_live_*`, or `gssk_live_*`

Do **not** trigger for fiat on/off-ramps, custodial trading APIs, or self-custodial DEX SDKs — those are different products.

---

## Architecture, in one sentence

> Your server holds the bearer token; your server proxies every call to `https://partners-api.ghostswap.io`; your browser code talks only to your server.

The bearer **must never reach the browser**. Browser code calls `/api/quote`, `/api/swap`, etc. on the developer's own server; the server adds `Authorization: Bearer ${PUBLIC_KEY}:${SECRET}` and forwards to GhostSwap.

---

## Step 0 — Get a credential (one-time, by the developer)

The developer (not the agent) must do this once:

1. Sign in at <https://partners.ghostswap.io/sign-up>.
2. Submit the application form (org name, website, expected monthly volume, chosen partner fee 0–4 %).
3. Wait for admin approval (~24 h). Once status flips to `active`, an activation email lands in their inbox.
4. Open **/dashboard/api-credentials** → click **Create live credential** → copy both values:
   - `GHOSTSWAP_PUBLIC_KEY` — looks like `gspk_live_<32 hex>`, always recoverable from the dashboard.
   - `GHOSTSWAP_SECRET` — looks like `gssk_live_<48 hex>`, shown once at creation; can be revealed later via the audit-logged **Reveal secret** button.
5. Set both as environment variables on the developer's server. **Never paste them into code that ships to the browser.**

If the developer says "I haven't applied yet", direct them to that URL and pause the integration work — no API call works without a credential.

---

## The standard workflow (memorize this)

```
1. GET  /v1/currencies              → populate dropdowns
2. POST /v1/addresses/validate      → on blur, check the user's payout address
3. POST /v1/quotes                  → live quote on every amount/pair change
4. POST /v1/swaps                   → on confirm; MUST include Idempotency-Key
5. GET  /v1/swaps/{id}              → poll every 10 s while UI visible, 30 s when backgrounded
6. Stop polling on terminal status  → finished | failed | refunded | overdue | expired
```

That's the entire flow. Every well-built integration is some variant of these six steps.

---

## Authentication

Every `/v1/*` request needs exactly two headers:

```
Authorization: Bearer ${GHOSTSWAP_PUBLIC_KEY}:${GHOSTSWAP_SECRET}
Content-Type: application/json
```

The colon between public key and secret is part of the bearer string — there is no separate signing step. The server argon2id-verifies the secret against a hashed copy; partners never sign anything themselves.

```js
const AUTH = `Bearer ${process.env.GHOSTSWAP_PUBLIC_KEY}:${process.env.GHOSTSWAP_SECRET}`;
```

---

## Endpoint cheat sheet

Base URL: `https://partners-api.ghostswap.io`

| Method | Path | Purpose | Notes |
|---|---|---|---|
| GET | `/v1/currencies` | List enabled coins | `?lite=true` returns just tickers |
| GET | `/v1/pairs?from=btc&to=eth` | Min/max for a pair | Use `minAmountFloat`/`maxAmountFloat` for float, `…Fixed` for fixed-rate |
| POST | `/v1/addresses/validate` | Check a wallet address | `{ "currency": "eth", "address": "0x…" }` |
| POST | `/v1/quotes` | Get a live quote | `{ from, to, amountFrom }`. Add `mode: "fixed"` for a locked rate |
| POST | `/v1/swaps` | Create a swap | **Requires `Idempotency-Key` header.** Returns `payinAddress` + `id`. Pass `extraId` for memo/tag coins |
| GET | `/v1/swaps/{id}` | Get current status | Source of truth — poll this |
| GET | `/v1/swaps?limit=50&offset=0` | Paginated list | Scoped to the org, most-recent first |
| GET | `/v1/public/quote?from=btc&to=xmr&amount=0.05` | Public display quote | **No API key.** 60 req/min/IP, CORS-open — for price widgets & comparison sites, not for executing swaps |
| GET | `/health` | Liveness probe | Unmetered; safe at any frequency |

---

## Display rules (these are the user-visible parts)

Quote response shape:

```json
{
  "quote": {
    "from": "btc", "to": "eth",
    "amountFrom": "0.01",
    "amountTo": "0.1532",
    "networkFee": "0.0021",
    "amountUserReceives": "0.1511",
    "rate": "15.32",
    "fee": "0.001",
    "min": "0.0008", "max": "5.0",
    "mode": "float"
  }
}
```

**Show `amountUserReceives` to the user, not `amountTo`.** The subtraction (`amountTo - networkFee`) is already done. Also display `rate`, `min`, and `max`. Re-render on every change of `from`, `to`, or `amountFrom` — debounce ~400 ms so the user can type freely.

Swap response shape:

```json
{
  "swap": {
    "id": "htpi6bqnazl7hbjd",
    "status": "waiting",
    "from": "btc", "to": "eth",
    "amountFrom": "0.01",
    "amountExpectedFrom": "0.01",
    "amountExpectedTo": "0.1532",
    "amountActualFrom": null,
    "amountActualTo": null,
    "actualNetworkFee": null,
    "payinAddress": "bc1q…",
    "payoutAddress": "0x…",
    "refundAddress": "bc1q…",
    "payinHash": null,
    "payoutHash": null,
    "moneyReceivedAt": null,
    "moneySentAt": null,
    "amountAnomalyPct": null,
    "createdAt": "2026-04-29T12:00:00Z"
  }
}
```

**Display `payinAddress` prominently** — that's the deposit address the user should send `amountFrom` of `from` to. Render as a copyable string; a QR code is nice-to-have (use `qrcode` from npm). After the swap progresses, `amountActualFrom` is the actual on-chain amount received; use it for completed-state displays and accounting, especially if the user overpaid or underpaid.

The `id` is the canonical swap identifier in your records, GhostSwap's records, and the upstream provider's records. Use it for every follow-up call and store it on your order row.

---

## Idempotency — non-negotiable rule

`POST /v1/swaps` **requires** an `Idempotency-Key` header. Generate a UUID v4 **once per logical "Confirm" click** and reuse it across HTTP retries of THAT click. Do **not** generate a fresh UUID on retry — that creates a duplicate swap.

```js
import { randomUUID } from 'node:crypto';

// On the client: one UUID per Confirm button press; reset after success.
let confirmKey = null;
function onConfirmClick() {
  if (!confirmKey) confirmKey = crypto.randomUUID(); // browser-side
  // POST to your server with confirmKey in the body
}

// On the server: forward the key as a header to GhostSwap.
await fetch(`${BASE}/v1/swaps`, {
  method: 'POST',
  headers: {
    'Authorization': AUTH,
    'Content-Type': 'application/json',
    'Idempotency-Key': req.body.idempotencyKey,
  },
  body: JSON.stringify(swapBody),
});
```

If the developer's code regenerates the UUID on every fetch, fix it. That single bug has produced duplicate swaps for real partners.

---

## Polling cadence

Poll `GET /v1/swaps/{id}` after creation:

| UI state | Interval |
|---|---|
| Browser tab visible, status non-terminal | **10 seconds** |
| Browser tab backgrounded or server-side worker | **30 seconds** |
| Status `hold` (AML/KYC review) | **5 minutes** — direct user to support@ghostswap.io |
| Status terminal | **Stop polling** |

Terminal statuses: `finished`, `failed`, `refunded`, `overdue`, `expired`.

GhostSwap refreshes upstream status every ~30 s, so polling faster than 10 s wastes the rate budget without giving the user fresher data. Polling slower than 60 s feels laggy while the user is watching the page.

---

## Float vs fixed-rate swaps

| | Float (default) | Fixed |
|---|---|---|
| Rate determined | At swap-finish time (whatever the market gives) | Locked at quote time |
| Body field | omit `mode` | `mode: "fixed"` + `rateId` from quote |
| `refundAddress` | optional but recommended | **required** |
| Time pressure on user | minutes (`waiting` window) | seconds (~60 s `payTill` window) |
| Best for | Most integrations | Receipts/invoices that need a guaranteed output |

Default to float unless the product specifically needs a locked rate. The fixed flow adds two failure modes: stale `rateId` (HTTP 409 `rate_expired` → re-quote with a **new `Idempotency-Key`**) and `expired` status (the user missed the `payTill` deadline).

---

## Error envelope

Every non-2xx body has this shape:

```json
{
  "error": {
    "type": "validation_error",
    "code": "amount_below_min",
    "message": "Minimum amountFrom is 0.0008",
    "param": "amountFrom"
  }
}
```

Surface `error.message` to the end-user (and `error.param` when present). Recovery by `type`:

| `type` | HTTP | What to do |
|---|---|---|
| `validation_error` | 400 | Show the message; user can fix |
| `authentication_error` | 401 | Bad bearer — check env vars on the server |
| `authorization_error` | 403 | Org not yet `active` — wait for admin approval |
| `not_found` | 404 | Wrong id, or id belongs to another org |
| `conflict` | 409 | `Idempotency-Key` reused with a different body, or fixed `rateId` expired — re-quote and retry with a **new** key |
| `unprocessable` (code `exchange_not_processable`) | 422 | We can't route this specific swap. **Do not retry.** Surface `message` verbatim |
| `rate_limit_error` | 429 | Read `Retry-After` (seconds), sleep, retry. If retrying `POST /v1/swaps`, reuse the same key |
| `upstream_error` | 502 / 503 | Transient. Backoff and retry once. On `POST /v1/swaps`, first call `GET /v1/swaps?limit=20` to check whether the swap was created before retrying |

Every response includes an `X-Request-Id` header. Log it. Forward it to support when escalating.

---

## Rate limits

- **Per credential: 30 RPS** — every `gspk_live_*` gets its own bucket.
- **Per source IP: 120 RPS** (pre-auth) — generous for partners on shared egress.
- Standard `RateLimit-Limit` / `RateLimit-Remaining` / `RateLimit-Reset` headers on every response. Self-throttle from `RateLimit-Remaining` before hitting 429.
- `/health` is unmetered.

---

## Minimal working example (Node.js + Express)

This is a complete server-side proxy you can deliver to the developer as a starting point. ~120 lines, no build step, no frameworks beyond Express.

```js
// server.js
import 'dotenv/config';
import express from 'express';
import { randomUUID } from 'node:crypto';

const { GHOSTSWAP_PUBLIC_KEY, GHOSTSWAP_SECRET, PORT = 3000 } = process.env;
if (!GHOSTSWAP_PUBLIC_KEY || !GHOSTSWAP_SECRET) {
  console.error('Set GHOSTSWAP_PUBLIC_KEY and GHOSTSWAP_SECRET in your env.');
  process.exit(1);
}

const BASE = 'https://partners-api.ghostswap.io';
const AUTH = `Bearer ${GHOSTSWAP_PUBLIC_KEY}:${GHOSTSWAP_SECRET}`;

async function gs(method, path, { body, idempotencyKey } = {}) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: {
      'Authorization': AUTH,
      'Content-Type': 'application/json',
      ...(idempotencyKey ? { 'Idempotency-Key': idempotencyKey } : {}),
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = data?.error ?? { message: `HTTP ${res.status}` };
    const e = new Error(err.message);
    Object.assign(e, { status: res.status, ...err });
    e.retryAfter = res.headers.get('Retry-After');
    e.requestId = res.headers.get('X-Request-Id');
    throw e;
  }
  return data;
}

const app = express();
app.use(express.json({ limit: '10kb' }));

// Browser-safe proxy routes. Bearer never leaves the server.
const route = (fn) => async (req, res) => {
  try { res.json(await fn(req)); }
  catch (e) {
    if (e.retryAfter) res.setHeader('Retry-After', e.retryAfter);
    res.status(e.status || 502).json({
      error: { type: e.type, code: e.code, message: e.message, param: e.param },
    });
  }
};

app.get('/api/currencies', route(() => gs('GET', '/v1/currencies')));
app.post('/api/quote', route((r) => gs('POST', '/v1/quotes', { body: r.body })));
app.post('/api/validate', route((r) => gs('POST', '/v1/addresses/validate', { body: r.body })));
app.post('/api/swap', route((r) => {
  // The browser MUST send its own idempotencyKey (one UUID per Confirm
  // click, reused on retries). Refuse silent server-side generation —
  // that hides client bugs and risks duplicate swaps.
  const { idempotencyKey, ...body } = r.body;
  if (!idempotencyKey) {
    const e = new Error('idempotencyKey is required');
    e.status = 400; e.code = 'missing_idempotency_key'; e.type = 'validation_error';
    throw e;
  }
  return gs('POST', '/v1/swaps', { body, idempotencyKey });
}));
app.get('/api/swap/:id', route((r) => gs('GET', `/v1/swaps/${encodeURIComponent(r.params.id)}`)));

app.listen(PORT, () => console.log(`http://localhost:${PORT}`));
```

The matching browser code reads `crypto.randomUUID()` on first Confirm click, stores it in a variable, sends it to `/api/swap`, and resets it only after success. See the full reference implementation (HTML + browser JS, ~200 lines) in the [end-to-end guide](https://partners.ghostswap.io/docs/guides/end-to-end-swap).

---

## Critical rules — never violate

1. **Server-side only.** The bearer must never reach the browser. All browser → API calls go through the developer's own server.
2. **Bearer format is `${PUBLIC_KEY}:${SECRET}` with a single colon.** Both values from env vars.
3. **`Idempotency-Key` is required on `POST /v1/swaps`.** UUID v4, one per Confirm click, reused on retries.
4. **Display `amountUserReceives`, not `amountTo`.** The network-fee subtraction is already done for you.
5. **Refund address is optional on float, required on fixed.** Send `undefined` (or omit the key) when the user can't provide one — never send an empty string.
6. **Stop polling on terminal status.** Don't keep hitting `/v1/swaps/{id}` forever.
7. **On 429, read `Retry-After` and sleep.** Don't hammer.
8. **On `upstream_error` (5xx) after `POST /v1/swaps`, do not auto-retry.** First call `GET /v1/swaps?limit=20` and look for your `partnerReferenceId` — the swap may already exist.
9. **Disable the Confirm button until a quote has loaded AND the payout address validated.** Eager-enabled buttons let users submit blindly.
10. **Never put the secret in browser code, in git, or in client-side env files.** Server env vars or a secret manager only.
11. **Collect a memo / destination tag for tag coins.** When the `to` currency has `requiresExtraId: true` on `GET /v1/currencies` (XRP, XLM, ATOM, HBAR, TON and others), render an input labelled with its `extraIdName` and send it as `extraId`. Omitting it returns 400 `missing_extra_id` and no swap is created. Only if the user confirms their wallet genuinely has no tag, send `extraIdNotRequired: true`. Send `refundExtraId` alongside `refundAddress` when the `from` coin uses tags.

---

## Anti-patterns to refuse

If the developer asks for any of these, push back and explain why:

- ❌ **"Put the API key in the React app for simplicity"** — leaks credentials in page source. The fix is a server proxy.
- ❌ **"Generate a new idempotency key on each retry"** — creates duplicate swaps. Reuse the same UUID for the same logical click.
- ❌ **"Skip the quote panel; users just want to confirm"** — biggest failure mode of bad integrations. Users have no idea how much they'll receive. Show `amountUserReceives` before Confirm enables.
- ❌ **"Poll every second so it feels real-time"** — wastes the 30-RPS budget and gives no fresher data (upstream refresh is ~30 s). 10 s while visible is the right number.
- ❌ **"Skip the memo field — nobody uses tags"** — payouts to an exchange deposit address on XRP, XLM, ATOM etc. can't be credited without the tag. Honour `requiresExtraId`.
- ❌ **"Catch errors silently"** — always surface `error.message` and `error.param`. Silent failures lose users.
- ❌ **"Hard-code the base URL"** — read `GHOSTSWAP_API_BASE` from env so staging can point elsewhere.

---

## Affiliate referral links (optional, no integration code)

Every approved partner also gets a referral link: `https://ghostswap.io/?ref=<their-slug>`. End-users who click that URL get a 30-day cookie attribution; any swap they complete on ghostswap.io credits the partner 1 % of the volume. No code on the partner's end — they just share the URL. The partner claims their slug from the dashboard overview page.

The partner's API-integration earnings and referral earnings combine into one payable USDT balance, paid out once balance ≥ $100.

If the developer's primary use case is "I just want a share link, not an integration" — they don't need any of this skill's code. Direct them to <https://partners.ghostswap.io/sign-up>, tell them to apply, and after approval the **Pick your referral code** card on /dashboard handles everything else. No more steps.

---

## Pre-flight checklist before declaring done

Before handing the integration back to the developer, walk through this:

1. ☐ `GHOSTSWAP_PUBLIC_KEY` and `GHOSTSWAP_SECRET` are server-side env vars, **not** in browser code or git.
2. ☐ All `/v1/*` calls go through the developer's own server (not directly from browser).
3. ☐ `Idempotency-Key` is a UUID generated **once per Confirm click**, reused on retries.
4. ☐ The UI shows `amountUserReceives`, `rate`, `min`, `max` **before** the Confirm button is enabled.
5. ☐ Confirm button is disabled until (a) a quote has loaded, (b) payout address validated, (c) refund address either empty or validated.
6. ☐ Address validation runs on blur via `POST /v1/addresses/validate`, with visible ✓ or error.
7. ☐ After Confirm, the deposit address (`payinAddress`) is prominently displayed.
8. ☐ Polling runs at 10 s while visible / 30 s when backgrounded / 5 min on `hold` / never when terminal.
9. ☐ Error display surfaces `error.message` and `error.param` — never silent.
10. ☐ `partnerReferenceId` is set to the developer's own order id so they can correlate swaps with their DB.

If any item fails, fix it before shipping. Partial integrations leak money.

---

## Reference docs (load these when you need depth)

- Full integration brief (a complete one-prompt walkthrough): <https://partners.ghostswap.io/llms-full.txt>
- Quickstart: <https://partners.ghostswap.io/docs/quickstart>
- End-to-end swap (the reference HTML+JS implementation, ~200 lines of UI code): <https://partners.ghostswap.io/docs/guides/end-to-end-swap>
- Authentication: <https://partners.ghostswap.io/docs/auth>
- Idempotency: <https://partners.ghostswap.io/docs/concepts/idempotency>
- Status lifecycle (all 10 states): <https://partners.ghostswap.io/docs/concepts/status-lifecycle>
- Errors: <https://partners.ghostswap.io/docs/concepts/errors>
- Rate limits: <https://partners.ghostswap.io/docs/concepts/rate-limits>
- Troubleshooting (real failure modes integrators have hit): <https://partners.ghostswap.io/docs/guides/troubleshooting>
- Security: <https://partners.ghostswap.io/docs/guides/security>
- Roadmap: <https://partners.ghostswap.io/docs/roadmap>

---

## Support

- Telegram: <https://t.me/ghostswap1>
- Email: <support@ghostswap.io>
- AML/KYC review (user-facing): direct end-users to <support@ghostswap.io> when status is `hold`

Always include the swap `id` and the `X-Request-Id` of the relevant response when escalating. Both make support's lookup hop trivial.
