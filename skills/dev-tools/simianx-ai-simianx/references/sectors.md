# Sector Watch

A sector is a curated list of US-listed stocks, the assets they own and the dated catalysts and first-hand events that
move them. Every event comes from one primary source (an SEC 8-K exhibit, a company press release, a regulator or
registry page), read once and classified: `event_type`, `severity` 1–4, `direction`, a one-paragraph `ai_summary`
and the source link. Only the `biopharma` sector is live today; `GET /v1/sectors` says which exist and what each one
tracks. Free, trial and Starter plans see events with a 30-minute delay (`delayed_seconds` in the answer, 0 on Plus
and Pro); the calendar, stocks and assets are never delayed. `title` is in the account's language when a translation
exists, `title_en` is always the English original. All sector endpoints need scope `data:read`; follows need
`automation:manage`.

## Sectors (0.2 points)

`GET /v1/sectors` → `items[]`: slug, name, tagline, description, is_live, calendar_kinds[], event_types[], stats.

## One sector (0.3 points)

`GET /v1/sectors/{sector}` → the same row with full `stats` (stocks, assets, scheduled items, events in the last days).

## Stocks (0.3 points per request)

`GET /v1/sectors/{sector}/stocks?q=&cap_tier=large&limit=50&offset=0`

- `q`: ticker or name prefix. `cap_tier`: `large` (≥ $10B), `mid` ($2B–$10B), `small` ($300M–$2B), `micro`
  ($50M–$300M), `nano` (< $50M), `unknown`. `limit` ≤ 200, `offset` for the next page; `total` in the answer.
- Items: ticker, name, market_cap, cap_tier, logo, id.

`GET /v1/sectors/{sector}/stocks/{ticker}` (0.3) → the stock with its assets, scheduled calendar items and recent events.

## Calendar (0.3 points; 0.05 when `since` is given and nothing changed)

`GET /v1/sectors/{sector}/calendar?from=2026-10-01&to=2026-12-31&status=scheduled&stock=NVDA&asset=<slug>&kind=pdufa&since=<iso>&limit=100`

- `from` / `to`: dates (inclusive). `status`: `scheduled` | `done` | `cancelled`. `kind`: one of the sector's
  `calendar_kinds` (biopharma: `pdufa`, `adcomm`, `readout`, `trial_completion`, `conference`). `stock`: ticker.
  `since`: ISO 8601, only items created or updated after it (poll with the `newest` value of the previous answer).
- Items: id, kind, date, date_precision (`day` | `month` | `quarter`), date_history[] (earlier dates when the item
  moved), title, title_en, status, outcome (`approved`, `crl`, `extended`, `positive`, `negative` or empty),
  confidence (`sourced` | `inferred` | `unsourced`), source_kind, source_url, stock{ticker, name, market_cap,
  cap_tier}, asset{slug, name}, payload, updated_at.
- A `quarter` or `month` precision means the company gave a window, not a day; do not present it as a date.

## Events (0.3 points; 0.05 when `since` is given and nothing is new)

`GET /v1/sectors/{sector}/events?min_severity=3&stock=NVDA&asset=<slug>&types=fda_approval,fda_crl&cursor=&since=<iso>&limit=50`

- `min_severity`: 1–4. `types`: comma list of `event_type`. `stock`: ticker; `asset`: slug.
- `since`: ISO 8601; return only newer rows (poll with the `newest` value of the previous answer).
- `cursor`: the `next_cursor` of the previous page for older rows. Newest first.
- Items: id, slug, event_type, severity, direction (`up` | `down` | `neutral`), title, title_en, ai_summary,
  source_kind, source_url, source_filed_at (when the source published it; `created_at` is when we saw it),
  confidence, stock{ticker, name, market_cap, cap_tier}, asset{slug, name}, calendar_item (id of the dated item it
  settles or creates), payload, escalations, created_at. `delayed_seconds` at the top level.

| Severity | Meaning (biopharma) |
|---|---|
| 4 | decision-grade: approval, CRL, PDUFA extension, advisory committee scheduled or voted, Phase 3 topline |
| 3 | filing accepted, PDUFA date set, FDA inspection classification, EMA opinion, partnership or acquisition |
| 2 | designation (breakthrough, fast track, priority review), trial-registry change, label update, conference |
| 1 | anything else |

| `event_type` | Default severity | Direction | Creates / settles |
|---|---|---|---|
| `fda_approval` | 4 | up | pdufa |
| `fda_crl` | 4 | down | pdufa |
| `pdufa_extended` | 4 | down | pdufa |
| `pdufa_set` | 3 | neutral | pdufa |
| `adcomm_scheduled` · `adcomm_vote` | 4 | neutral | adcomm |
| `trial_topline` | 4 | neutral | readout |
| `bla_submitted` | 3 | up | — |
| `bla_accepted` | 3 | up | pdufa |
| `inspection` | 3 | down | — |
| `ema_opinion` | 3 | up | — |
| `partnership` | 3 | neutral | — |
| `designation` · `label_update` | 2 | up | — |
| `trial_change` | 2 | neutral | trial_completion |
| `conference` | 2 | neutral | conference |
| `other` | 1 | neutral | — |

Severity 3 and 4 events carry a `slug` (a permanent page on the site); lower ones have `slug: null`.

## One event (0.2 points)

`GET /v1/sectors/{sector}/events/{slug}` → the item plus `summary` (the source excerpt) and the full `payload`.

## Assets (0.3 points per request)

`GET /v1/sectors/{sector}/assets?stock=NVDA&q=&review_status=confirmed&limit=50&offset=0`

- `stock`: ticker of the owner; `q`: name or alias; `review_status`: `auto` | `confirmed` | `rejected` (`auto` rows
  were linked by the pipeline and not yet checked by a person; say so when you rely on one).
- Items: slug, name, kind, aliases[], indication, application_number, application_type, stock{ticker, name,
  market_cap, cap_tier}, readiness (checklist with `items[]`), review_status, updated_at.

`GET /v1/sectors/{sector}/assets/{slug}` (0.3) → the item plus `links[]` (role, review_status, evidence, stock or
external owner), `trials[]` (nct_id, title, phase, status, sponsor, primary_completion, enrollment, url), its
calendar items and events.

## Follows (free; scope `automation:manage`; Starter and above)

A follow is one thing the account watches on top of the sector feed: a stock, an asset, or one dated catalyst. The
first follow in a sector creates a subscription for the account with an email channel; from then on followed targets
push instant alerts for events of severity 2 and above and reminders before dated items. Ask the human before creating
one — it sends mail — and tell them channels and digests are managed on the sector page of the site.

- `GET /v1/sectors/{sector}/follows` → `follows[]` (id, type, key, reminder_offsets, stock | asset | calendar, created_at)
  and `subscription` (channels, min_severity, reminder_offsets, weekly_digest, timezone, send_time, is_active).
- `POST /v1/sectors/{sector}/follows` `{"type": "stock", "ticker": "NVDA"}` · `{"type": "asset", "slug": "<slug>"}`
  · `{"type": "calendar", "id": "<calendar item id>", "reminder_offsets": [7, 1, 0]}` (days before; omit to inherit
  the subscription's offsets). Idempotent per target: the same target twice returns the existing follow.
- `DELETE /v1/sectors/{sector}/follows/{id}` → removes it. The subscription stays; it is managed on the site.

## Poll loop

```bash
# new decision-grade events since the last check, then upcoming dated items for one stock
curl -s "$API/v1/sectors/biopharma/events?min_severity=3&since=$NEWEST" -H "Authorization: Bearer $SIMIANX_API_KEY"
curl -s "$API/v1/sectors/biopharma/calendar?stock=$TICKER&status=scheduled&from=$(date -u +%F)" -H "Authorization: Bearer $SIMIANX_API_KEY"
```

Keep `newest` from each answer and pass it as `since`; a poll that finds nothing costs 0.05. Relay `source_url` with
every event you report; the summary is a reading of one document, not a view on the stock.
