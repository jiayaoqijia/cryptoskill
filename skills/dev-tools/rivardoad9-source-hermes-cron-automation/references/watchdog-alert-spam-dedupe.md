# Watchdog alert spam — how a silent watchdog became the noise source (10 Sep 2026)

## What the user saw

> "kok dpt pemberitahuan bot eror mulu ya" — a notification every 15 minutes, for hours.

## What was actually happening

The FlowMetrix live watchdog (`~/.hermes/scripts/fm_live_watchdog.sh`, cron `*/15`, no_agent,
deliver=origin) checks a standing condition: *can the engine's Telegram command bot hold a
poll?* Since 15:45 WIB the answer was no (the engine was polling the wrong bot token, a separate
defect), so on every single tick it did two things:

1. `echo "bot dead"` → the job's stdout is delivered verbatim to the user's chat → one chat
   message every 15 minutes.
2. A `notify` curl to the engine's own bot with a long warning → a second message every 15 min.

Two channels, one standing condition, zero dedupe. The watchdog was working correctly; the
delivery model was not.

## The rules that fixed it

- **Liveness from the log TAIL, not from a window.** The old code counted `bot launch failed`
   lines appearing since its last watermark. That is a "did something new happen" test, not a
   "is it broken now" test — a quiet window would have read as healthy. The new check is
   `tail -n 5 <errlog> | grep -qE "bot launch failed|retrying the command bot"`, which is true
   for as long as the failure loop is running, however quiet the tick window is.
- **Dedupe with a state file + a horizon.** `/tmp/fm_watchdog_state.bot` holds the epoch of the
   last alert; the alert fires only when `now - last >= 6h`. Everything else is silent (no
   stdout, no notify).
- **Exactly one recovery message.** When the tail no longer shows the failure and the state file
  exists → send one `✅ <thing> normal lagi`, delete the state file, done.
- **Pre-seed the state on deploy** when you know the condition is currently true and the user is
  already being told, so the fix itself does not fire another alert.

## Generalisation (use it for every future watchdog)

A watchdog has three modes — healthy (say nothing), broken (say it once, then respect the
horizon), recovered (say it once) — and the failure mode of a naive implementation is to
collapse the middle mode into the first. Also remember the inverse lesson: a watchdog that
alerts on a NON-standing condition (a new execution error, a position opening) is naturally
deduped by the event itself and does not need a horizon.

Corollary for one-shot checks created to babysit a single event (the 20:45 "was the PPI alert
sent?" job): write them to print only when the answer is BAD, so a normal outcome stays silent.

## Where the delivery contract lives

`no_agent` + script: empty stdout = nothing delivered, non-empty stdout = delivered verbatim,
non-zero exit = the scheduler sends its own error alert. Design for silence on success — the
cron job's own alerting is the safety net, not the message channel.
