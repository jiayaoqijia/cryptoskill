# For developers calling the API from code

The same endpoints serve AI agents and programs. The fields written for an agent to speak (`say`, `ask`,
`notify_user`) are additions you may ignore; the machine fields (`kind`, `data`, `id`, `cursor`, `next_run_at`) are
stable and in the OpenAPI document (`https://service.simianx.ai/v1/openapi.json`). Points are reported to code in
full: `X-Points-Charged` and `X-Points-Remaining` on every paid response, `POST /v1/analysis/quote` for a price before
a call, `GET /v1/me` for the balance and `reset_type` (`daily` for free and VIP, `monthly` for period plans).

## Keys

Create keys by hand at https://www.simianx.ai/#api or let a CLI sign the user in with the browser link
(`references/auth.md`). Keys carry scopes, daily / monthly budgets, a per-call cap, an expiry and an IP allowlist
(`references/billing.md`).

## Safe retries: `Idempotency-Key`

Send `Idempotency-Key: <your unique string>` on any `POST`, `PATCH` or `DELETE`. For 24 hours the same key on the
same endpoint from the same API key returns the stored answer (`X-Idempotent-Replay: true`) without running the call
again: a retry after a network cut cannot start a second session, a second deep run or a second charge. A replayed
key-creation answer never repeats the token (it was shown once). Use one Idempotency-Key per logical operation: the
same key sent with a different method, path or body answers `422 idempotency_mismatch` rather than the other call's result.

## Delivery: four ways to the same updates

Every event a run produces for your key is one **update** row (`references/following.md`): `{id, kind, notify_user,
say, ask, data, next_run_at, source, event_id, created_at}`. The same `id` reaches you by whichever path you pick;
acking it on one path acks it everywhere.

| Path | How | Ack |
|---|---|---|
| **Webhook** (recommended for servers) | `POST /v1/webhooks` with your URL; every update is POSTed to it | a 2xx answer within 10 s is the ack (when the webhook was created with `acks: true` **and** `this_key_only: true`; an account-wide hook never acks, so sibling keys polling the feed keep their rows; default `false` leaves the row for the feed) |
| **WebSocket** | the live session socket (`references/live.md`), frames carry `id`/`cursor` | send `{"ack": <id>}`; a reconnect to the same `ws_url` replays unacked rows (`data.replay: true`) |
| **SSE** | `GET …/events?stream=1` on deep runs and autopilots, `GET /v1/news/stream` | `Last-Event-ID` on reconnect; ack through the feed when you need exactly-once |
| **Polling** | `GET /v1/updates?ack=<id>&wait=30` | `ack` on the next request |

### Webhooks

```
POST /v1/webhooks
{"url": "https://example.com/simianx", "events": ["decision", "position.changed", "news"], "secret": "<16-128 chars>",
 "acks": true, "this_key_only": false}
→ 201 {"webhook": {"id", "url", "events", "active", "acks", …}, "secret": "<only when generated for you>",
        "signature_header": "X-SimianX-Signature: t=<unix seconds>,v1=<hex hmac_sha256(secret, '<t>.<body>')>"}
GET /v1/webhooks · GET /v1/webhooks/{id} · PATCH /v1/webhooks/{id} {url?, events?, acks?, active?} · DELETE /v1/webhooks/{id}
POST /v1/webhooks/{id}/test        → one signed "test" event to your URL now
GET  /v1/webhooks/{id}/failures    → the dead letters: update id, attempt, response status, error
```

- `events`: update kinds (`references/following.md`), or `["*"]` (default) for every kind. Plans: Free none,
  Starter 2 endpoints, Plus 5, Pro 10 (`webhook_endpoints` in `GET /v1/me` limits); 403 `plan_required` / 409
  `webhook_limit`.
- Request: `POST`, `Content-Type: application/json`, `User-Agent: SimianX-Webhooks/1.0`, headers `X-SimianX-Event-Id`
  (the update id) and `X-SimianX-Signature: t=<unix seconds>,v1=<hex>` where `hex = HMAC-SHA256(secret, f"{t}.{raw body}")`.
  Body = the update object plus `"event": "update"` and `"hook_id"` (`"event": "test"` for the test call).
- Answer 2xx within 10 s. Anything else, or a timeout, is retried after 1 min, 5 min, 30 min, 2 h and 12 h (five
  retries); then the attempt is a dead letter under `/failures`, and after repeated failures the hook is disabled
  (`active: false`, `disabled_reason`); `PATCH {"active": true}` re-enables it.
- Verify the signature before trusting a body (reject timestamps older than 300 s):

```python
import hashlib, hmac, time

def verify(secret: str, header: str, body: str, tolerance: int = 300) -> bool:
    try:
        parts = dict(p.split("=", 1) for p in header.split(","))
        ts, given = int(parts["t"]), parts["v1"]
    except (ValueError, KeyError):
        return False
    if abs(int(time.time()) - ts) > tolerance:
        return False
    expected = hmac.new(secret.encode(), f"{ts}.{body}".encode(), hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, given)
```

`examples/webhook_verify.py` is the same function as a script; `examples/python_client.py` and
`examples/js_client.mjs` are complete minimal clients.

## The decision, for an execution system

A `decision` update's `data` is what a broker or exchange integration reads (never the `say` text):

| field | meaning |
|---|---|
| `action` | `open`, `close`, `hold` |
| `side` | `long`, `short` (stocks: long only) |
| `entry_low`, `entry_high`, `entry_type` | the entry zone and `market` / `limit` / `stop` |
| `stop`, `target` | protective stop and target |
| `confidence` | 1–10 |
| `invalidation` | what would void the call |
| `timeframe`, `expires_at` | the candle the call is for and when it is stale |
| `market`, `symbol`, `analysis_id`, `rationale` | identity and the one-paragraph reasoning |

Act only while `now < expires_at`. SimianX supplies analysis and events; your system places and manages the real
orders in the user's own account and is the source of truth for fills. Positions recorded inside SimianX (autopilot
paper books, `/autopilots/{id}/actions`) are simulated.

## Conventions

- Envelope `{"code", "notify", "data"}`; errors add `data.reason` (`references/billing.md` for 402 / 429 / 426).
- `429` carries `Retry-After`; paginated lists return `next_cursor`; every time is ISO 8601 UTC.
- Breaking changes never edit a path in place: a new path or field is added, the old one gets `Deprecation`, `Sunset`
  and `Link: <…>; rel="successor-version"` headers and a `deprecations` entry in `GET /v1/skill`.
- Send `X-SimianX-Skill: 1.0.6` (or your client's own version string) so `_skill_update` and `426` work as designed;
  a client that never sends it is never refused.

## Minimal clients

Python (`pip install requests websockets`):

```python
import asyncio, json, os, requests, websockets

API = "https://service.simianx.ai"; KEY = os.environ["SIMIANX_API_KEY"]
H = {"Authorization": f"Bearer {KEY}", "X-SimianX-Skill": "1.0.6", "Content-Type": "application/json"}

s = requests.post(f"{API}/v1/live/sessions", headers={**H, "Idempotency-Key": "live-btc-15m-1"},
                  json={"asset": "crypto", "symbol": "BTC", "timeframe": "15m"}).json()["data"]

async def follow():
    async with websockets.connect(s["ws_url"], additional_headers={"Authorization": H["Authorization"]}) as ws:
        async for raw in ws:
            f = json.loads(raw)
            if not f.get("notify_user"):
                continue                      # heartbeat / tick
            if f["kind"] == "decision":
                place_order(f["data"])        # your broker / exchange code
            await ws.send(json.dumps({"ack": f["id"]}))
            if f["kind"] == "session_end":
                break

asyncio.run(follow())
```

JavaScript (Node 18+, `npm i ws`):

```js
import WebSocket from "ws";
const API = "https://service.simianx.ai", KEY = process.env.SIMIANX_API_KEY;
const H = { Authorization: `Bearer ${KEY}`, "X-SimianX-Skill": "1.0.6", "Content-Type": "application/json" };

const { data: s } = await (await fetch(`${API}/v1/live/sessions`, { method: "POST",
  headers: { ...H, "Idempotency-Key": "live-btc-15m-1" },
  body: JSON.stringify({ asset: "crypto", symbol: "BTC", timeframe: "15m" }) })).json();

const ws = new WebSocket(s.ws_url, { headers: { Authorization: H.Authorization } });
ws.on("message", (raw) => {
  const f = JSON.parse(raw);
  if (!f.notify_user) return;                        // heartbeat / tick
  if (f.kind === "decision") placeOrder(f.data);     // your broker / exchange code
  ws.send(JSON.stringify({ ack: f.id }));
  if (f.kind === "session_end") ws.close();
});
```

Polling instead of a socket: `GET /v1/updates?ack=<last>&wait=30` in a loop; `scripts/follow_run.py` is a reference
implementation of that loop with the exit codes agents use.
