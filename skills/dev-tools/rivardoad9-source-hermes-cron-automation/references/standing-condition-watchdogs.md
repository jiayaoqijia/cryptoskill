# Watchdogs that assert a STANDING condition (and the timezone trap next door)

Companion to `references/silent-and-dedupe-patterns.md`. That file covers EVENT-shaped jobs
(one message per event). This one covers the other half: a job that re-asserts a condition
that STAYS true, plus the schedule facts that are easy to get wrong.

## 1. Standing conditions must be deduped — the user sees every line

`no_agent=true` + non-empty stdout = **the text is delivered to the chat verbatim, every
tick**. So a line written for the operator's own debugging becomes a user-facing
notification, and a condition that stays true for hours becomes a notification that repeats
for hours.

Incident (10 Sep 2026): the FlowMetrix live watchdog checked the engine's Telegram command
bot and `echo`-ed `bot dead` on every run (plus a Telegram notify of its own). While the bot
was broken the user received the same alert every 15 minutes for hours. Their complaint was
about the MESSAGE, not the underlying bug:

> "kok dpt pemberitahuan bot eror mulu ya"

Fix shape — silent while unchanged, one line on change, long re-alert interval for a
standing problem:

```bash
STATE="/tmp/<job>_state.bot"
DEAD=0
tail -n 5 "$ERRLOG" | grep -qE "<failure pattern>" && DEAD=1   # current state, from the log TAIL
if [ "$DEAD" = 1 ]; then
  LAST=$(cat "$STATE" 2>/dev/null || echo 0); NOW=$(date +%s)
  if [ $((NOW - LAST)) -ge 21600 ]; then        # re-alert at most every 6h
    notify "...still broken..."; echo "$NOW" > "$STATE"; echo "still broken (new alert echoed)"
  fi
elif [ -f "$STATE" ]; then                       # recovered: say it ONCE, then go quiet
  notify "✅ recovered"; rm -f "$STATE"
fi
```

## 2. "No new errors in this window" is NOT "healthy"

The first version of that check looked for failure lines among the lines written since the
previous run (a watermark). In a quiet window it finds none and reports a **false recovery**.
Read the condition from the **tail of the log** (current state); use a watermark only to
decide whether there is something NEW to report.

Same reasoning as the existing rule about restart verification: an optimistic log line
("started") is not proof of health, and an absence of errors is not proof of anything.

## 3. Where the evidence is when a user says "I keep getting notified"

```bash
ls -t ~/.hermes/cron/output/<job_id>/ | head -8     # run history
tail -5 ~/.hermes/cron/output/<job_id>/<newest>.md  # what each tick actually emitted
cronjob action=list                                 # last_status / deliver / no_agent
```

Identical bodies on every tick in that directory is the signature of an undeduped watchdog.
`last_status: ok` on all jobs does NOT mean the user found them useful — a job can be
"ok" while spamming.

## 4. Schedule facts — verify the mapping, don't trust notes

- **Server TZ on this box is WIB (Asia/Jakarta) and Hermes cron is native WIB.** Evidence:
  cron output filenames match `TZ=Asia/Jakarta date`, and the engine's own `node-cron`
  schedules print `(Asia/Jakarta)`. An older version of this skill's SKILL.md claimed
  "server UTC+8, user WIB = server −1h" — that is stale; re-check with
  `TZ=Asia/Jakarta date '+%H:%M:%S'` against a fresh cron output filename before repeating
  any offset claim. Always state the zone explicitly in prompts and replies.
- **A `*/N` schedule on a no_agent job costs 0 tokens** but still writes an output file per
  tick: tightening a poller from 15 min to 5 min (10 Sep 2026, news tick → faster release
  detection) is free in LLM terms, and the extra ticks stay silent while idle.
- **Concurrency:** two jobs covering overlapping times for the same script will double-run
  it (and can race on its state file). Prefer ONE job whose schedule covers both windows
  over two overlapping jobs.
- **Editing a job's schedule** via `cronjob action=update` returns the new `next_run_at` —
  quote that as the proof the change landed, rather than asserting it.
