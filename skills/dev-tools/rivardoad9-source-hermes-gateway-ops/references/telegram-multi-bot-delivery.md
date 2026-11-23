# Delivering to a SPECIFIC bot (not the gateway bot)

Verified 2026-09-28 while routing the low-cap alert stack into a dedicated alert bot the user
had just created (`@memescallsbot`) instead of the main chat.

## The trap: a private-DM chat_id is not bot-specific

For **private chats `chat_id == the user's Telegram user id`**. The user's DM with bot A and
their DM with bot B are different chats that share the same number. Consequences:

- `deliver: "telegram:<telegram-user-id>"` on a cron job does **not** mean "send through the bot in
  that DM". Hermes cron delivery has no bot parameter — it always leaves through the platform
  bot configured in `~/.hermes/.env` (the gateway bot).
- So a "targeted" chat id looks perfectly correct in the job config and still lands in the
  **gateway bot's** DM. Symptom: user says *"kok masih masuk chat lama?"* while every log says
  the send was clean. Only group/channel ids (negative, `-100…`) are unambiguous.
- Corollary: same-numbered jobs in `jobs.json` targeting different bots are indistinguishable —
  do not diagnose this from config, diagnose it from which bot the message arrived from.

## The fix: push through the target bot's own Bot API

```python
url = f"https://api.telegram.org/bot{token}/sendMessage"
data = urllib.parse.urlencode({"chat_id": cid, "text": body, "parse_mode": "HTML",
                               "disable_web_page_preview": "true"}).encode()
with urllib.request.urlopen(urllib.request.Request(url, data=data), timeout=25) as r:
    resp = json.loads(r.read())
# resp["ok"] → bool, resp["result"]["message_id"] → the evidence
```

Rules that were load-bearing:

- **Credential in its own file**, `~/.hermes/data/<purpose>_bot.json`, mode **600**, and never
  printed. Validate the token with `getMe` before trusting it (gives username + bot id).
- **Inventory the bots before planning any routing.** `~/.hermes/scripts/identify_bots.py` resolves every
  `TELEGRAM_BOT_TOKEN=` it finds in the known .env paths to `@username` + bot id via `getMe` — run it instead
  of grepping for tokens by hand. It does **not** read the JSON credential files, so bots whose token lives in
  `~/.hermes/data/<purpose>_bot.json` are missing from its output: `getMe` those separately. A partial
  inventory is the trap — "we only have 3 bots" reads convincing and is wrong.
- **A bot can only DM a user who pressed `/start`.** If the user says they started it and
  `getUpdates` is still empty, wait and retry — the update lags. `pending_update_count: 0`
  alone is NOT proof they never started it.
- **`getUpdates` is safe only for a bot with no other consumer.** Never for the gateway bot or
  the trading-engine bot — it hijacks their long-poll and eats a real update.
- **A pasted token often carries a stray character.** A space in the middle of the token is
  common; strip whitespace and re-check the shape (Telegram tokens are 35 chars) before
  declaring the token invalid.
- **`parse_mode=HTML`, not Markdown.** Content with file names/underscores (`call_perf_report.py`)
  breaks Markdown — Telegram reads `_…_` as italic and rejects/mangles the message. Escape
  `& < >` first, then re-insert `<b>`/`<code>`/`<i>`. Keep italic conversion to whole-line-only
  so mid-line underscores survive.
- **Split at ~3900 chars, per line, never mid-tag**; keep one chunker implementation shared by
  every sender.

## Evidence, not vibes

The proof of delivery is the `message_id` returned by the API (or the message in the bot) —
NOT the script's stdout. Log one line per attempt to a push log
(`ts | lane | SENT/FAILED | n chars | message_id`); that file is how you tell "no signal
today" apart from "the bot is broken" when a lane is silent by design.

Related pattern (redirecting an existing cron lane's output into the new bot while keeping the
old channel as a fallback): `hermes-cron-automation` →
`references/silent-and-dedupe-patterns.md` §5.
