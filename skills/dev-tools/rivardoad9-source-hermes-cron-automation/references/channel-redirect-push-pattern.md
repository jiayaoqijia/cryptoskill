# Redirecting a cron lane's output to another channel (push-or-print)

Verified 2026-09-28 — moving a whole 5-lane alert stack (P1/P2/P3/EARLY WATCH/TRACK) from the
originating Telegram chat into a dedicated bot the user had just created. Companion fact:
`hermes-gateway-ops` → `references/telegram-multi-bot-delivery.md` (why `deliver` can't pick the
bot, and how to push through a specific bot's own Bot API).

## Why not just change `deliver`

Cron delivery always leaves through the platform bot in `~/.hermes/.env`, and for private DMs
`chat_id == user id`, so re-pointing `deliver` at the new bot's chat id silently posts to the
old chat. If the destination is a *different bot/account*, the job's script must push itself.

## The pattern: wrap `main()`, never touch the print sites

One `run()` per lane, added right before the `if __name__ == "__main__":` block:

```python
def run():
    """Cron entry point. Success = EMPTY stdout (cron stays silent → no double post).
    Failure = the text is printed, so the old cron channel becomes the safety net."""
    import contextlib, io
    import lowcap_common as L                 # shared sender (local import keeps the diff tiny)
    if not L.should_push(sys.argv[1:]):
        return main()
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = main()
    L.deliver(buf.getvalue(), "P2")
    return rc


if __name__ == "__main__":
    sys.exit(run())
```

`deliver(text, lane)` = push to the new channel; on failure it `print()`s the text itself, so
the pre-existing `deliver: origin` path still delivers it. Nothing above the wrapper changes.

## Invariants — each maps to a real failure mode

- **Success prints NOTHING.** If the lane also prints, the old channel gets a duplicate. Note
  the trap: "delivered" is now *defined* as empty stdout, which silently invalidates the old
  habit of verifying delivery by reading the lane's stdout — update the skill/docs in the same
  pass, or the next session will "verify" a healthy lane and call it broken.
- **Failure prints the full text, never a traceback.** The push helper must catch everything
  (`except Exception` → return `False, reason`); a bot/network outage degrades to the old
  channel, it never loses the alert and never kills the lane.
- **Manual/diagnostic runs never push.** One shared `should_push(argv)` + `LOCAL_FLAGS =
  ("--selftest", "--local", "--print", "--dry", "--digest", "--all")`; otherwise hand-running a
  digest spams the user's fresh alert channel.
- **Environment kill switch** (`ALERT_PUSH=off`) so tests and debugging can't publish. Pair it
  with "the wrapper is skipped entirely when the flag is present", so `--selftest` keeps
  printing to the terminal where a human expects it.
- **One delivery implementation.** HTML conversion, chunking and the HTTP call live in ONE
  module; other senders delegate to it rather than carrying a copy that drifts.
- **Log every attempt with the provider's `message_id`**
  (`~/.hermes/data/alert_push.log`: `ts | lane | SENT/FAILED | n chars | message_id`). With
  stdout empty by design, that line is the only evidence — and the only way to tell "no signal
  today" from "the channel is broken".
- **Test the fallback path deliberately** (point the credential path at a nonexistent file and
  assert: no exception, `False` returned, text reached stdout, failure logged). That test is
  what makes the "alert never lost" claim true instead of aspirational.

## Migration order that worked

1. Land the shared sender + its selftest, with the fallback covered.
2. Convert ONE lane, then drive it live end-to-end (real run → log line with `message_id` →
   confirm stdout is 0 chars). Also run the diagnostic flag and confirm it printed locally and
   pushed nothing.
3. Only then convert the remaining lanes — a wiring mistake can't take out every lane at once.
4. Prove the lanes that legitimately have nothing to say still exit 0 with empty stdout.
