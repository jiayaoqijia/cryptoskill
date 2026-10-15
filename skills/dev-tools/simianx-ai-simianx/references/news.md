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

## Stream (Plus and above; 3 points per connection hour, metered by the minute)

`GET /v1/news/stream?symbols=BTC,ETH&min_value=medium` with `Accept: text/event-stream`.

- `event: news` with the article as data; `id:` is the cursor. Reconnect with `?after=<id>` (or `Last-Event-ID`) to resume.
- `event: reconnect` after ~55 minutes: open a new connection with the last id.
- `event: paused_budget` when the account cannot cover the next minute: the stream closes; fix the points and reconnect.
- One stream per Plus account, three per Pro (`news_stream_connections`); 429 `news_stream_limit` beyond that.
