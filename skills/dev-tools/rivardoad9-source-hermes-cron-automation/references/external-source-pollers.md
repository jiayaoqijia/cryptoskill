# Polling external sources with zero credentials (watchdog ingest)

For "can you detect X in realtime?" where X is a **public Telegram channel, a page without an
RSS feed, or any HTML source that updates**. Shape: `no_agent` cron script that polls, dedupes by
source-native id, and stays silent when nothing is new (see `silent-and-dedupe-patterns.md`).

Proven 15 Sep 2026: `https://t.me/whale_alert_io` watcher, live in one session.

## 1. The t.me/s/ trick — public channel, no login, no API key, no MTProto

`https://t.me/s/<channel_username>` serves the **channel preview** server-rendered: the last ~20
posts (id, ISO timestamp, text) as plain HTML. Verified: HTTP 200, 102 KB, 20 posts parsed.
This is the cheapest possible ingest — no `api_id`/`api_hash`, no bot token, no paid API.

Structure to parse (stdlib `urllib` + `re` is enough — no bs4 needed):

- post anchor: `data-post="<username>/<msg_id>"`
- time: `<time datetime="2026-09-15T...Z">`
- body: `<div class="tgme_widget_message_text ...">...</div>`
- permalink to hand the user: `https://t.me/<username>/<msg_id>`

## 2. Design rules that make it safe (copy these)

| Concern | Rule |
|---|---|
| Window is only ~20 posts | Poll fast relative to the channel's rate. Compute the rate from the preview itself (span of timestamps ÷ count): whale_alert ≈ **12 posts/day** → a `*/2` minute poll has ~50× margin, no post can ever scroll past unseen. |
| First run must not flood | On missing state file: write the newest id as baseline and print **nothing**. Never dump the 20 archived posts. |
| State location | `~/.hermes/cache/<name>_state.json` holding `{last_id, fails}` — **not `/tmp`** (wiped on reboot = whole window re-delivered). Allow an env override (`WHALE_STATE=...`) purely for testing. |
| Watcher was down for a day | Burst cap: print at most 6 newest new posts, then `… +N lagi`. Survives outages without spamming. |
| Fetch breaks (network/WAF/HTML change) | Counter in the same state file; alert **once** at ≥3 consecutive failures, reset to 0 on success. Never let a broken poller die silently. |
| Text hygiene | Strip tags after turning `<br>` into `\n`, drop the trailing anchor label the channel glues on (`Details`, `Read Analysis`, `View transaction`), and collapse runs of the same emoji so `🚨🚨🚨🚨` becomes `🚨`. |
| Delivery | `no_agent=true`, `script=<name>.py`, `schedule="*/2 * * * *"`, `deliver="origin"`. Empty stdout = silent tick, which is the desired 99% case. |

Output shape per post (works well in Telegram, one blank line between posts):

```
🐋 🚨 185,000,000 $USDC (184,996,762 USD) transferred from #Aave to Unknown Whale 1
https://t.me/whale_alert_io/103136
```

## 3. Test without spamming the user

1. Run once with a throwaway state file → expect **silent**, and the state file created with the newest id (= baseline works).
2. Copy the state to `/tmp`, decrement `last_id` by 3, run with `WHALE_STATE=/tmp/...` → prints exactly those 3 posts (= parse + format + ordering).
3. Confirm the real state file is untouched, then let the cron tick land and check `~/.hermes/cache/<name>_state.json` mtime + `~/.hermes/cron/output/<job_id>/` for the silent tick.

## 4. Report the honest latency, then name the upgrade paths

Polling is **near**-realtime: latency = 0..interval after the source posts. Say that explicitly
instead of calling it "realtime". Upgrades, cheapest first:

- **Poll faster** — same script, smaller interval (fine here because the script costs 0 AI tokens).
- **MTProto / Telethon** — true push (seconds), full history, many channels at once. Needs the user
  to create an app at `my.telegram.org` and provide `api_id` + `api_hash`; keep them in `.env` and
  never echo them to output.
- **Vendor API** (e.g. Whale Alert's paid API) — structured JSON with wallet labels and tx hashes,
  but it is a paid dependency; only worth it if the user wants the extra fields.

## 5. Keys / paths of the working instance

- Script: `~/.hermes/scripts/whale_alert_watch.py` (stdlib only, ~165 lines, env-overridable state path)
- Cron job: name `Whale Alert watch (t.me/whale_alert_io) — realtime-ish`, `*/2 * * * *`, `no_agent`
- State: `~/.hermes/cache/whale_alert_state.json`

Knobs to offer when the user reacts to volume (all are one-line edits): keyword/asset filter
(SOL-only, exchange in/outflow, nominal > $X), interval, or redirect output into another agent
(engine/NewsAgent) as context instead of a chat message. Default day-1 choice: **deliver
everything unfiltered** — at ~12 posts/day the volume itself is the signal, and guessing the user's
filter risks hiding the one alert they cared about.

## 6. Reuse checklist for a *new* channel/source

1. `curl -s -A '<browser UA>' https://t.me/s/<name>` → confirm 200 and count parsed posts.
2. Note the rate (span of the 20 timestamps) → choose the interval.
3. Copy `whale_alert_watch.py`, change `CHANNEL`, state path, and the emoji/prefix.
4. Run the 3 test steps above, then `cronjob create` with `no_agent=true` + `deliver=origin`.
5. Verify the first tick wrote state and stayed silent.
