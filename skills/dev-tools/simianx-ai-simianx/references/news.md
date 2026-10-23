# News

Every article from ~150 sources is classified: the symbols it concerns, a `value_score` (very_low | low | medium | high),
a `sentiment` (bullish | bearish | neutral), `is_global`. Free, trial and Starter plans see the list with a 30-minute
delay (free also without value and sentiment); Plus and above are live and may open the stream.

## List (0.5 points per request; 0.1 when `since` is given and nothing is new)

`GET /v1/news?symbols=BTC,NVDA&asset=crypto&min_value=medium&sentiment=bullish&since=<iso>&limit=50`

- `symbols`: comma list (an article matches when it names one of them or is global).
- `since`: ISO 8601; return only rows that became readable after it, oldest first (poll with the `newest` value of the previous answer; a story can repeat, dedupe by `id`).
- `cursor`: the `next_cursor` of the previous page for older rows.
- Items: id, title, summary, url, source, asset, image_url, published_at, symbols[], is_global, value_score, sentiment.

## One article (0.2 points)

`GET /v1/news/{id}` → the item plus `text` when the full text was captured.

## Translate titles (1 point per call, ≤ 20 titles)

`POST /v1/news/translate {"titles": ["…"], "language": "ja"}`

## News watch (server side; keeps matching while you are away)

When the user says "tell me when there is news on NVDA and BTC", "帮我盯 NVDA 的新闻": create a watch. The server
matches every new story against it, offline or not, and writes an update per story to `GET /v1/updates`.

```
POST /v1/news/watches
{"symbols": ["NVDA", "BTC"], "min_value": "medium", "sentiment": null, "asset": null, "language": "en",
 "include_pulse": false, "quiet_hours": {"start": "23:00", "end": "07:00", "tz": "America/Los_Angeles"}}
→ 201 {"watch": {"id": "…", "symbols": [...], "min_value": "medium", "active": true, …}, "next_step": "…"}
GET /v1/news/watches                 → the key's watches (symbols, when the last match was, how many)
DELETE /v1/news/watches/{id}         → stop
```

- `min_value` (default `medium`): `low` / `medium` / `high`. `sentiment` filters one side. `symbols: []` = global
  stories only. `include_pulse` is accepted and stored for a coming release; today a watch delivers news only.
- `quiet_hours`: inside the window only `high` stories pass.
- Each match is one update, kind `news`:
  `say` = "[important · bullish] NVDA: <title> — <one-line summary> (Reuters, 3 min ago)" + the link in `data.url`;
  `data`: `id`, `symbols`, `value_score`, `sentiment`, `published_at`, `url`, `source`, `story_key`, `also_reported_by`.
  On `high` value the row carries an `ask`: "Shall I run a quick read on NVDA for this story?" — put it to the user
  and, on a yes, `POST /v1/analysis/quick`.
- One story, many sources: the same event from several outlets is one update (`story_key`); later outlets are
  appended as `also_reported_by`, not sent again.
- Bursts: more than 5 stories for one watch within 10 s become one `news.burst` update ("6 stories on NVDA in the
  last moments: …"); `high` stories are still sent on their own.
- Plans below Plus: the first update of a watch says once that news on this plan runs about 30 minutes behind
  (no price, no plan pitch); do not repeat it.
- Follow the feed as in `references/following.md`; a watch runs until it is deleted.

## Stream (Plus and above; 3 points per connection hour, metered by the minute)

For an agent that holds a connection and wants every story as it lands, now:

`GET /v1/news/stream?symbols=BTC,ETH&min_value=medium` with `Accept: text/event-stream`.

- `event: news` with the article as data; `id:` is the cursor. Reconnect with `?after=<id>` (or `Last-Event-ID`) to resume.
- `event: reconnect` after ~55 minutes: open a new connection with the last id.
- `event: paused_budget` when the account cannot cover the next minute: the stream closes; this is a 402 case, say
  so once and give the links.
- One stream per Plus account, three per Pro (`news_stream_connections`); 429 `news_stream_limit` beyond that.

A watch and a stream can run together on the same symbols: the watch is what survives you leaving.
