# Per-coin news (from the project's own sources) + community sentiment

Built and verified 2026-10-05 for a 5-token portfolio (ONDO/TAO/WLD/VIRTUAL/BOME) feeding a
risk dashboard. Two asks, one recipe: *"news yang ada kok kek lama bgt — ambil dari X asli koin
tersebut"* and *"tambahin sentimen masyarakat, bullish or bearish brp persen"*.

## The diagnosis that matters

When the user says the news is stale, check **who gets covered**, not whether the feed runs:

> the news DB refreshed hourly (newest item 22:09 the same day) — but tier-1 media (CoinTelegraph,
> Decrypt, The Block) never write about mid-caps, so per-coin the newest rows were 10–26 days old and
> two tokens had **zero** rows. The feed was alive; the coverage was empty.

Fix = add the coin's own sources instead of blaming/patching the aggregator. Say this out loud in the
report — it reframes "broken" into "no coverage", which is the honest answer.

## Source 1 — official X posts without the X API (keyless)

X's API timeline read is locked/paid. The endpoint that actually worked, first try, every time:

```
https://news.google.com/rss/search?q=site:x.com/<handle>&hl=en-US&gl=US&ceid=US:en
```

Parse `<item>` → `title`, `link`, `pubDate`. Works for `@opendensor`-style handles, for the project's
own site/blog (`q=<coin name> (site:ondo.finance OR site:blog.ondo.finance)`), and for material media
(`q="<SYMBOL>" (partnership OR launch OR unlock OR listing OR ETF …)`).

Do **not** burn time re-testing these — all returned 429/403/blocked/no-render on 5 Oct 2026:
`api.fxtwitter.com`, `nitter.poast.org|tiekoetter.com|lightbrd.com`, `rsshub.app`,
`syndication.twitter.com/srv/timeline-profile/…`, `cdn.syndication.twimg.com/…`, `xcancel.com`.
Browsing `https://x.com/<handle>` without login also yields no timeline article text.

Honesty label for the UI: `X resmi @handle` = post indexed under that account URL;
`X soal @handle` = something indexed mentioning the handle (could be a third party). Author-verified
timelines require a paid X API tier — say the price and that you did not enable it.

## Source 2 — community sentiment % (keyless, rate-limited)

```
GET https://api.coingecko.com/api/v3/coins/<cg_id>?localization=false&tickers=false
    &community_data=false&developer_data=false&sparkline=false
→ sentiment_votes_up_percentage   (down = 100 - up)
```

- `/coins/{id}` also gives `twitter_followers`-class fields only if you ask `community_data=true`
  (we turn it off to stay light); it is `sentiment_votes_up_percentage` at the TOP level that we want.
- **429 after ~2 back-to-back calls** on this host (shared IP). Rules that made it reliable:
  cache each coin's votes for 6 h in `porto_sentiment_cache.json`, `time.sleep(3.5)` between coins,
  2 retries with ~8 s backoff, and on failure just skip — never block the build.
- Values seen: ONDO 92, TAO 72, WLD 64, ASTER 100 (small samples — hundreds of voters at most).

## Sentiment = votes + tone, and say which

```
bull = 0.5 * cg_up_pct + 0.5 * (bull_hits / (bull_hits + bear_hits) * 100)   # text half needs ≥3 hits
src  = "vote CoinGecko 72% + teks X/media 42%"   # always rendered next to the number
conf = tinggi  if votes present AND ≥15 posts
       sedang  if ≥8 posts OR votes present
       rendah  otherwise
```

- Keyword halves live in two tuples (bullish/buy/partnership/listing/buyback/… vs
  bearish/dump/hack/lawsuit/delist/dilution/…), matched on lowercased headline text.
- If only the text half survives, say so in the source string, and add the disclosure the user needs:
  **the tone half is biased bullish** — project posts are marketing. Never print a bare percentage.
- Market-wide context (separate, one call, cache): `https://api.alternative.me/fng/?limit=1` → value+label
  ("Sentimen pasar: 70 — Greed"). Do not confuse it with the per-coin figure.

## Storage + cadence (reuse infrastructure, don't build a second pipeline)

- One table in the DB that already exists — `crypto_impact.db.token_news`
  (`sym, kind('x'|'x_mention'), level, tier('terverifikasi'|'perlu_dicek'), pub_utc, title, link, source`).
- Verification tiers: **terverifikasi** = official X / official site-blog, or tier-1 media with a clear
  event, or ≥2 sources; **perlu_dicek** = official source but impact unclear. Social chatter and
  price-prediction articles are dropped, not demoted.
- Filters that keep it clean: minimum title length, a noise regex (`to watch|weekly gainers|market
  update|convert <n> <SYM> to …`), strip the ` - <source>` suffix before dedup, and require the coin to
  be actually mentioned for media rows.
- Silent fetch cron every 30 min (`no_agent`, stdout empty on success → no chat spam). **Push only
  material events** (partnership/launch/burn/unlock/listing/upgrade/ETF/hack keyword gate) — daily
  tweets stay in the dashboard. Same delta-only discipline as every other alert lane.

## Reporting shape that landed

Verdict first, then a per-coin table (bullish %, bearish %, source, confidence), then the honest caveat
paragraph, then the visual proof (dashboard screenshots). Close on the actionable item already in the
queue (the over-weight position whose sentiment was MOST euphoric — 41% of the book at 94% bullish is a
warning, not a green light).
