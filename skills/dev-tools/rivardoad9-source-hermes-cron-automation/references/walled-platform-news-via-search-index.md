# Per-entity news when the platform is walled — read the search index, not the API

Problem shape (5 Oct 2026): "the news column in the risk dashboard is stale — pull it from each
coin's **official X account**, and push an entry whenever there's a real development." The feed
itself was fine (items landing every hour); the *per-entity* view was stale because tier-1 crypto
press rarely writes about small tokens. Before blaming a collector, check the **post-filter** view
per entity — `select sym, max(pub_utc) from <table> group by sym` on the rows the UI actually
reads, not `max(pub_utc)` over the whole table.

## 1. Reading X (and other walled platforms) without a paid API

Direct keyless reads of X timelines are walled — verified dead from this server 5 Oct 2026:
`syndication.twitter.com/srv/timeline-profile` (429 "Rate limit exceeded"),
`cdn.syndication.twimg.com/timeline/profile` (200 + 0 bytes), nitter.net / nitter.privacydev /
nitter.tiekoetter (403 / Anubis bot wall), xcancel.com (451 service suspended),
rsshub.app + rsshub.rssforever (404 / 503), `r.jina.ai/https://x.com/<handle>` (Cloudflare 403).
X API read requires a paid tier. **Do not write these up as "X is unusable" — use the index route.**

What works, keyless, no auth, from this box:

```
https://news.google.com/rss/search?q=<QUERY>+when:30d&hl=en-US&gl=US&ceid=US:en
```

Three query shapes, each carrying a different trust level:

| Query | Returns | Label it |
|---|---|---|
| `site:x.com/<handle-lowercase>` | posts indexed **under that account's URL path** (small count: 2–100) | `X resmi @handle` |
| `site:x.com <handle>` | posts that index for the handle, incl. **third-party posts that mention it** | `X soal @handle` (or "mention") |
| `site:<official-domain>` | the project's own newsroom/blog (e.g. `site:ondo.finance`, `site:world.org`) | `<domain> (situs resmi)` |

Counts are wildly asymmetric — `site:x.com/aster_dex` returned 100 posts, `site:x.com/ondofinance`
returned 0 while the broad form returned 100. **Issue both** forms and let the path form win the
dedupe, so an item that is provably the account's own post is labelled as such and the rest stay
honestly "mention". Add the token's aliases/name/domain to `site:` queries too — and remember
`site:` is loose: verify per-entity relevance in code, not by trusting the query.

## 2. Parsing rules for Google News RSS (each one bit us)

- Titles carry a trailing source suffix pasted on by Google: `"<title> - <source>"`. Strip it with a
  regex that tolerates en/em dashes (`\s*[-–—]\s*<source>$`) — a plain `t.endswith(" - x.com")`
  misses the `– x.com` variants and leaves them in the UI.
- The `<link>` is a `news.google.com/rss/articles/CBMi…` redirect. It **cannot** be resolved from
  this server: the base64 payload holds a Google internal `AU_yqL…` id, and a direct GET returns
  0 bytes. Keep the Google link as-is; do not burn calls trying to extract the real tweet URL, and
  do not claim authorship you cannot prove.
- `<source>` is the publisher (`x.com`, `CoinDesk`, `Ondo Finance`). `<pubDate>` is RFC-822 →
  `email.utils.parsedate_to_datetime(...)`; assume UTC when tzinfo is missing.
- Publish timestamps lag (an item can appear with a date 3–7 days old), so **freshness must be
  measured on `pubDate`, not on when you fetched it.**

## 3. Noise rules (reuse the existing NOISE_RE, then tighten)

- Junk that survives a naive length filter: `"<title> - Ondo Finance"` (empty title), `"Articles by
  World (@worldnetwork) - x.com"` (profile index page), `"gm,frens"`, and FX-converter SEO pages
  `"Convert 100 BOME (BOOK OF MEME) to TWD"`.
- **Regex gotcha:** `convert \d|…` inside a `\b( … )\b` group silently fails on `convert 100`
  because the trailing `\b` sits after a single digit — "100" has no boundary after "1". Use
  `convert \d+`. Always unit-test the noise regex against the real junk strings you just saw
  (`--selftest` in the script, asserts on 4–6 literal titles).
- Require an **entity hit** before a media item is admitted: token symbol, alias, or official
  handle appearing in the title. Without it, `site:`/broad queries leak unrelated stories
  (a Kenya news-agency post landed under a memecoin).
- `INSERT OR IGNORE` on a stable key (`link`) means rows stored **before** a filter change stay in
  the table forever. Re-filter on every save: load `(link, title)`, delete rows that fail the
  current junk/noise rules, then insert. Otherwise the UI keeps showing junk you already fixed.

## 4. Lane wiring: collector silent, push gated on materiality

- Collector: `no_agent` cron every 30 min (`8,38 * * * *` — offset from the sibling `*/30` job so
  both don't fire in the same second), wrapper `scripts/token_news_cron.sh` →
  `token_news.py --cron --auto`. The `--cron` flag is what makes it silent: fetch + save, print
  **nothing**, exit 0. Default/verbose modes keep their human summary on stdout for manual runs.
- `--auto` derives the symbol list from the dashboard's own state file (`porto_risk.json`
  `assets[].sym`) plus a hardcoded extras list, so the lane follows the portfolio instead of a
  symbol list that rots.
- Push: do **not** add a second alerting job for the same items — the existing 30-min delta job
  already reports "new item vs previous snapshot". Gate that line so only *material* items notify:
  `tier == "terverifikasi" and level == "HIGH"`, where `level` = `HIGH` iff a gebrakan/event regex
  matched (partnership, launch, listing, unlock, burn, buyback, upgrade, mainnet, hack, ETF,
  regulation…). Routine tweets then appear in the dashboard without DMing anyone. Beware a
  first-run burst: when a new source class is introduced every item looks new, so the first delta
  after wiring pushes a batch — expected once, mention it to the user rather than "fixing" it.
- Store new rows in the same DB as the existing tier-1 items and merge at read time
  (`news_for()` reads both, then sorts: verified first, newest first) so the dashboard and the
  delta job pick up the new source with no UI change.
- Surface freshness in the UI: carry `updated_utc` (max pubDate of the merged per-token set) in the
  payload and render "update terbaru <ago>" in the section header. "Looks stale" complaints get
  resolved by a visible timestamp as much as by fresher data.

## 5. Report honesty

State the difference in confidence between the two X labels, and that a truly author-verified feed
needs the paid X API. Offer the paid upgrade as an explicit user decision instead of silently
labelling mentions as official.

## 6. Files from the working instance (5 Oct 2026)

- `~/.hermes/scripts/token_news.py` — collector (`--selftest`, `--alert`, `--cron`, `--auto`,
  `--json`); config dict `TOKENS` = handle + domains + aliases + media query per symbol.
- `~/.hermes/scripts/token_news_cron.sh` — silent wrapper for the cron.
- `~/.hermes/scripts/porto_intel.py::news_for()` — merge + tiering + labelling;
  table `crypto_impact.db::token_news(link PK, sym, pub_utc, title, source, kind, level, first_seen)`.
- Cron `token news resmi · 30m (senyap)`, `8,38 * * * *`, `no_agent`, `deliver=origin`.
