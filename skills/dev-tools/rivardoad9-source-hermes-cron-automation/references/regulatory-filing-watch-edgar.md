# Watching SEC filings / regulatory events (EDGAR + press + news)

For "tell me when <ETF / filing / regulatory decision> changes" — a `no_agent` cron script that polls
EDGAR and news, dedupes by accession number / headline hash, and stays silent unless something new
lands. Proven 16 Oct 2026 on the INJ ETF watch (`~/.hermes/scripts/inj_etf_watch.py`).

## Endpoints that work from this server (verified live)

| What | URL | Notes |
|---|---|---|
| All filings of one entity | `https://data.sec.gov/submissions/CIK0002073616.json` | CIK zero-padded to 10 digits. `filings.recent` = parallel arrays `form[]`, `filingDate[]`, `accessionNumber[]`, **newest first**. |
| Full-text search (find the CIK, catch new docs) | `https://efts.sec.gov/LATEST/search-index?q=%22injective%22&hits=12` | Hit `_source.display_names` gives "Entity Name (CIK 0000000000)"; `_id` = `<accession>(:doc)`. Also surfaces SEC/bourse documents, not just issuer filings. |
| SEC press releases | `https://www.sec.gov/news/pressreleases.rss` | Catches an approval announced by press before any new filing. |
| News by keyword | `https://news.google.com/rss/search?q=%22injective%22+ETF&hl=en-US&gl=US&ceid=US:en` | Parse `<item>` with stdlib `re` — no feedparser needed. |

**Always send a real UA** (`{"User-Agent": "<name> (<email>)"}`) — SEC throttles/blocks anonymous clients.

## Resolving the watch target once

Don't hardcode guesses: run the full-text query, read `display_names` + CIK out of the hits, then poll
that CIK. Real resolution from one query: `Canary Staked INJ ETF` = CIK 2073616, `21Shares Injective ETF`
= CIK 2061622, `Injective Institutional Services, LLC` (the transfer-agent entity) = CIK 2141906.

## Form types that matter for an ETF launch (map them to plain language in the alert)

- `S-1`, `S-1/A` — registration / amendments. Process moving, **not** approval.
- `485APOS`, `485BPOS` — post-effective amendment → product may start operating (closest thing to launch).
- `8-A12B` — registering a new class of securities on an exchange → listing is near.
- `CERT` — exchange certification of a new product.
- `19b-4` — listing rule change.
- `TA-1` — transfer-agent registration (supporting infrastructure, not the ETF).

Label each alert with the form type + its meaning instead of calling everything "approval" — the user
needs to know whether the event is procedural or near-launch.

## Three traps (all hit in the first build)

1. **First run must be seeded, or it dumps the whole filing history.** Ship a `--seed` flag that records
everything as seen and prints nothing, and run it once before enabling the cron.
2. **After seeding, still alert on older unseen filings, one per tick.** Fix the loop: collect all unseen
   indices, alert on the newest (`baru_idx[0]`, EDGAR is newest-first), then mark **all** unseen ones as
   seen. Iterating oldest-unseen-first spams one old filing per hour.
3. **No date window = an ancient filing can alert after a state reset.** Keep a cutoff (`>= today − 21d`)
   and expose it as `--days N` so you can widen the window and actually test the alert path instead of
   waiting for a real event.

## Test recipe that doesn't spam the user

1. `python3 <script> --seed` → silent, state file created with the newest accession per entity.
2. `python3 <script>` twice → both silent (dedupe works).
3. Remove the newest accession from the state file, run with `--days 400` → exactly one alert, correct
   form label and Archives URL. Then re-seed.

## Catalyst reality check to state in the first message

An ETF filing is a *future* event, so the alert should never be framed as a price catalyst by itself.
Empirical base rate measured on this server (16 Oct 2026, Binance daily closes): the alt spot-ETF
launch wave of late Oct 2025 — SOL, HBTC alt complex — all four names (SOL, LTC, HBAR, XRP) were
**negative 30 days after launch** (-27.5%, -10.4%, -24.4%, -15.5%) and none printed a new high
afterwards. The re-rating happens into the *anticipation*; the launch/approval is where it gets sold.
Caveat to repeat: that window overlapped a broad market pullback, so it is a pattern, not clean causation.
