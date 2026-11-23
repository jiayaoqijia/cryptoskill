# Deadline / renewal reminder jobs (one-shot, H-N)

Class of ask: *"gw punya VPS expired 20/10/2026, nanti H-3 reminder gw ya"* — expiry/renewal of the
machine Hermes itself runs on, a domain, a card, an unlock date, a filing deadline.

## Shape that works (verified 5 Oct 2026: VPS expiring 20 Oct → job at 17 Oct 08:00 WIB)

```
cronjob action=create
  schedule="2026-10-17T08:00:00"          # ISO timestamp, native server TZ (= user WIB here)
  deliver="origin"                        # the chat the user asked in
  enabled_toolsets=["terminal","file"]
  attach_to_session=true                  # user can REPLY to the reminder and the agent has the brief
```

`attach_to_session` is the point: a reminder the user replies to ("oke migrasi, mulai") should not
land in a dead-end fire-and-forget session. `repeat` stays `once` for an ISO timestamp.

## Make it an ARMED reminder, not a nudge

The prompt must instruct the agent to *collect* at fire time, not just say "don't forget":

1. First line states the fact with both dates: "VPS expired 3 hari lagi: 20 Okt 2026" (today = 17 Okt).
2. Live inventory of what dies with the box, from real commands (never estimated):
   - active/total cron count from `~/.hermes/cron/jobs.json`
   - `du -sh ~/.hermes/{cron,data,skills} <vault>`
   - per-repo `git status --short | wc -l` + `git log -1 --format='%h %ad %s' --date=short`
3. A decision checklist: renew vs migrate; if migrating — push each repo, back up `~/.hermes/{cron,data,skills}`,
   park `.env`/tokens somewhere safe, list which services actually run here (Hermes gateway, cloudflared
   webhook) so the user knows what must move.
4. One closing line: what the user must decide today.

Guardrails to write INTO the prompt: read-only, never print API keys/tokens, never delete or modify
anything, and deliver via the final response only (no cross-posting to other platforms).

## Task reminders (“remind me tomorrow”)

Different from an expiry/H-N deadline: the user wants a personal nudge, not a live inventory.

- **Re-read the clock before choosing the day.** After midnight, casual “besok” usually means the day that has already started, not the next calendar day. Run `date` and state the actual date in the reply so a wrong interpretation is caught immediately.
- **Schedule inside the user’s stated availability, not at a default morning hour.** “Kelas pagi, baru bisa handle siang” → 12:30 WIB, not 08:00. A reminder that fires while he is unavailable trains him to ignore reminders.
- ISO timestamp in native WIB, `repeat` once, `deliver=origin`; verify `next_run_at` after creation.
- The prompt must carry the list, numbers, and copy-paste template itself — the cron session has no chat history. Explicitly tell it to remind only, not to execute the outreach or send messages on the user’s behalf.
- Do not turn a one-off “remind me” into a recurring job; recurrence needs an explicit request. A noon reminder after a morning class is correct even when the request was made at midnight.

## Pitfalls

- **State the reminder day explicitly, users give the expiry.** H-3 of 20 Oct 2026 = 17 Oct 2026 —
  compute it and put both dates in the reply so a wrong date is caught before it matters.
- **Verify `next_run_at` after creating** (must show the intended local time; here WIB). A deadline job
  that fires in the wrong timezone is worse than none. `schedule` as a bare ISO timestamp is native
  server TZ, which for this profile equals WIB.
- If the expiring box is the Hermes host itself, the reminder is also a backup audit: check uncommitted
  work now (vault had 79 files uncommitted for 2.5 weeks) and offer to clear it in the same session,
  rather than discovering it stranded at H-1.
