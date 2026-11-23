# Testing a bash alert script without any risk of messaging the user

Applies to `no_agent` cron scripts whose only side effect is a Telegram send (watchdogs,
milestone alerts, threshold notifiers). Sibling detail for the DB-backed extraction technique and
the design checklist: `references/watchdog-design-and-testing.md`. Worked example in the wild:
`flowmetrix-ops/scripts/fm_watchdog_notify_safe_test.sh` + its
`references/watchdog-signal-scan-and-testing.md`.

## The recipe (verified 12 Sep 2026, 4 scenarios green)

Copy the script, don't edit it. Point the copy at a **fake `.env` with no bot token** — a
`notify()` written as `[ -n "$BOT_TOKEN" ] && curl …` then becomes a no-op, so the test is
incapable of sending anything. Rewire every input path it reads:

```bash
mkdir -p /tmp/t
printf 'line1\n' > /tmp/t/out.log ; printf 'line1\n' > /tmp/t/err.log
printf 'DRY_RUN=false\nSTARTING_BALANCE_USD=288.27\n' > /tmp/t/env      # NO token
sed -e 's|ENV_FILE=.*|ENV_FILE="/tmp/t/env"|' \
    -e 's|STATE="/tmp/<name>_state"|STATE="/tmp/t/state"|' \
    -e 's|OUTLOG=.*-out.log"|OUTLOG="/tmp/t/out.log"|' \
    -e 's|ERRLOG=.*-error.log"|ERRLOG="/tmp/t/err.log"|' \
    "$HOME/.hermes/scripts/<name>.sh" > /tmp/t/wd.sh
bash -n /tmp/t/wd.sh            # syntax before anything else
```

Then drive states through FAKE LOGS rather than a live system: run twice (baselines), append a
synthetic line, run, assert. For a once-only alert (milestone) also assert the FLAG FILE appears
on the alerting run and that a fourth run is silent.

Assert on the script's own echo markers (`guard fired`, `exit alert`, `back to break-even`) —
those are what the cron output records — not on prose in the message.

## Traps that make a test pass for the wrong reason

1. **A new scan can silently have no baseline.** If an earlier section ends with
   `if [ "$WATERMARK" = 0 ]; then …; exit 0; fi` ("first run is baseline only"), a scan added
   AFTER it writes its own baseline on the **second** run. A missing state file after one manual
   run is expected, not a bug: run twice before concluding "no findings", and never treat a
   single silent run as proof the new branch works.
2. **Verify the `sed` matched.** A pattern written as `$HOME/...` does NOT match a literal
   `~/.hermes/...` inside the script's embedded heredoc — the copy then reads PRODUCTION config
   and the scenario "passes" for the wrong reason. After rewriting: grep the copy for the ORIGINAL
   path (must be absent), or print the resolved value inside the test. Prefer loose patterns
   (`OUTLOG=.*-out.log"`) over exact-value ones.
3. **A targeted write can hit the wrong file.** When the test rewrites a *config file path* that
   appears inside an embedded python block, the substitution must be checked the same way —
   a silent miss means the test exercised the real data.

## Which log carries the signal

`console.log` → the **out** log; `console.warn`/`console.error` → the **err** log. A condition
that is not an error — a guard firing, a clean refusal, entries being held — appears ONLY in the
out log, so an err-only scan will never see it. Give each log its own line watermark.

pm2 out-log lines carry **no timestamps**. To decide whether something happened before or after
an operator action, don't trust `tail`: count distinguishing markers over the same window
(e.g. `grep -c "entries held"` vs `grep -c "entries running"`), or find the newest full cycle
marker. A write that "hasn't been reflected yet" is usually just an unread cycle.

## Verify the clock before converting any schedule

Re-check with `date '+%H:%M %Z (%z)'` and cross-check against a cron output FILENAME (the tick is
in the name) before translating a schedule or telling the user a time. On this host the old
"server is UTC+8, WIB = server − 1h" mapping is WRONG: on 12 Sep 2026 `date` reported
`WIB (+0700)` and a `*/30` job produced `19:30` / `20:00` files while local time was 20:2x, i.e.
the scheduler's native time IS WIB. `/etc/timezone` reading `Asia/Shanghai` proves nothing — a
`TZ` env override wins. State the mapping you measured in the job prompt.
