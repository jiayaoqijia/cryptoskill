---
name: muting-alert-channels
description: "Use when muting an alert bot or notification lane."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
prerequisites:
  commands: [grep, python3]
metadata:
  hermes:
    tags: [alerts, telegram, cron, kill-switch, notifications, ops]
---

# Muting an outbound alert channel — silently, and provably

Turning a notification bot off looks trivial and is not: the usual lane design *prints the
payload when the send fails*, so a mute implemented as "skip the send" ends up flooding the
user's main chat. This skill is the procedure plus the three checks that make "it's off" a
verifiable claim.

## When to use

User says any of: "non aktifin <bot>", "matiin bot alert", "stop kirim dulu", "pause notif",
"jangan posting", "jangan kirim ke X lagi". Applies to cron-driven alert lanes, standalone
Telegram bots (alert bot, news bot, engine bot), webhook senders, digest mailers.

**Scope check first.** If the thing named is not a delivery channel — a stop-loss value, a
score threshold, a gate flag — this is the wrong door. Locate the file that actually owns
that value before touching anything, and if no such value exists in the system, say that
instead of inventing a place to put it.

## Step 1 — Pin the channel and audit its senders

1. **Resolve the user's shorthand to a real bot.** Shorthand like "memebot" maps to a bot
   username through its credentials file, not by guessing:
   `python3 -c "import json;print(json.load(open('$HOME/.hermes/data/perf_bot.json'))['bot'])"`
   → `@memescallsbot`. Never print the token.
2. **Audit every sender of THAT channel before claiming it is off:**
   `grep -rln "deliver(\|tg_push(" ~/.hermes/scripts/*.py` — the senders are usually fewer
   than it feels (one shared helper plus a couple of on-demand scripts).
3. **Scope your greps.** A bare `grep -rI` over `$HOME` will read multi-MB catalog/index
   files; one unscoped search dumped 42 MB of matches. Always constrain with `--include`,
   `-l` and explicit directories.
4. **Touch only the named channel.** Muting the bot the user named must not touch the news
   bot, the engine bot, or anything else sharing the same scripts — and the report should
   say which channels were deliberately left running.
5. **Choose mute-the-sink vs pause-the-producter, and say which.** Muting delivery while the
   scanner/tracker keeps running preserves the measured record (ledger, checkpoints,
   heartbeats) so nothing is lost when it is switched back on. Pausing the cron jobs is a
   separate, blunter action that stops data accrual — offer it explicitly when the user's
   intent could be "stop everything", and default to the reversible one.

## Step 2 — One choke point, two switches

- Put the check inside the **single function every sender already calls** (e.g. the shared
  `deliver()`), never at N call sites. Then coverage is provable with one grep.
- Support **both** an env var (one-off runs) and a **flag file** under `~/.hermes/data/`
  (`~/.hermes/data/<channel>_off`). The file flag survives restarts and needs no env plumbing
  through the many cron entries that may invoke the script directly.
- Keep an audit trail: the channel's push log records a distinct status for the suppressed
  send (e.g. `MATI`) instead of silently writing nothing.

## Step 3 — The rule that matters most: a muted channel must be SILENT

Most lanes here are **silence-on-success**: on send failure the payload is *printed* to
stdout, and `deliver: origin` turns that print into a message in the origin chat — a safety
net so an alert is never lost. That design makes the naive mute actively harmful:

> Skip-the-send **alone** prints the payload → cron delivers it → the chat the user asked to
> quiet gets flooded. **Muting the bot is not the same as moving its output to the DM.**

So the mute path must **drop the payload and leave stdout empty**, and record the suppression
in the log.

- **An existing `ALERT_PUSH=off`-style switch is usually a PRINT-MODE switch** (run locally,
  print instead of send), not a mute. Never reach for it to silence a channel — verify what a
  switch does to stdout before using it.
- **Manual/on-demand commands are the exception:** if the user explicitly asks for that report
  while the channel is muted, print it locally rather than dropping it. What was muted is the
  *unattended push*, not the user's ability to ask.

## Step 4 — Prove it (all three, then report)

1. **End-to-end, exactly as cron runs it**: run the producer and assert `stdout = 0 bytes`
   *and* a `| MATI |` line in the push log. Quote the last pre-mute line
   (`KIRIM … <message_id>`) next to it as contrast — the message_id is Telegram's own receipt.
2. **Catch fallbacks**: walk the Step 1 audit list and confirm each sender hits the same
   choke point (also run at least one *other* lane, not just the one you happened to test).
3. **Producers still healthy**: heartbeat/`.last` mtimes advancing, ledger rows still growing.

Then report: what is off, what is deliberately still running, the one-line reversal, and the
tradeoff (quota/CPU still spent if producers keep running).

## Rerouting a lane to another bot (the other answer besides mute)

"Lempar ke <bot X> aja, laporannya per daily, jangan spam" is THREE knobs, not one — target channel,
CADENCE, and payload shape. Changing only the target keeps the 15-minute spam (now on the other bot);
changing only the cadence keeps it in the wrong chat. Do all three in one edit and say so.

- **`deliver` cannot reach another profile's bot.** Deliver targets are profile-scoped, so posting into
a different bot's channel needs that lane's shared sender (here `news_send.py --file <tmp> --kind card`,
which reads its token from that lane's `.env`). Write a wrapper in `~/.hermes/scripts/` that runs the
producer, pipes stdout to that sender, and set the job to `deliver: local` so the engine does not ALSO
post the same stdout into the origin DM. Add `failure_deliver: origin` so a broken send is still
visible somewhere instead of dying silently in a log.
- **Never end a wrapper with `exit 0` after `sender || echo …`.** That makes every failure look like
success and destroys the job's `last_status` as evidence. Capture the code, exit it:
  ```bash
  python3 "$HOME/.hermes/scripts/news_send.py" --file "$TMP" --kind card
  RC=$?; rm -f "$TMP"; [ "$RC" -ne 0 ] && echo "<lane>: gagal kirim" >&2; exit "$RC"
  ```
  `news_send.py`-style senders exit 0 only on an `ok:true` API response and print nothing on success, so
  the exit code IS the proof; a stray "sent" claim without it is not.
- **Reuse the producer's own report mode.** Check its `argparse` first (`--full`, `--force`, `--watch`)
  — a daily digest is usually the existing full-snapshot flag, not a second formatter to maintain. A
delta job that stays silent unless a threshold moves cannot "report daily"; switch it to the full mode
  in the same edit that changes the schedule.
- Update the job's `name` and `prompt` too: a job still called "whale delta 15m (DM)" while running at
  07:00 into the news bot misleads the next session that reads `cron list`.

## Pitfall — an outbound-only bot has no process to kill

`ps aux | grep -i <bot>`, `systemctl list-units` and a `crontab -l` can all come back empty while the
bot still pushes messages: lanes here send from cron scripts through a token, with no listener and no
long-poll. Absence of a process is NOT evidence the channel is muted. Find the sender first
(`grep -rln "<bot_username>\|<token_file>" ~/.hermes/scripts`), then pause the jobs that call it — for
push-only lanes, pausing the producing cron job IS the whole switch, and the token/file staying on disk
is what makes revival one command.

## Pitfall — tests that read production state

Putting the flag file in production broke three pre-existing tests in the same session. The
delivery tests read the module-level flag path, so once `~/.hermes/data/<channel>_off`
existed, `deliver()` returned "muted" and the tests waiting for
*"send failed → payload IS printed"* / *"missing credentials reason"* / *"GAGAL logged"*
failed — a **false alarm produced by a correct production change**.

Fix and rule (**tests must be neutral toward production state**):

- Inside the test block, point the module-level path at a **non-existent temp path**:
  `MEMEBOT_FLAG = os.path.join(td, "memebot_off")`, saving the original first.
- Declare `global <FLAG>` in the **function head**. A `global` statement inside a nested block
  raises `SyntaxError: name assigned before global declaration`.
- Restore the original in `finally`.
- **Verify the suite passes BOTH with the production flag present and absent** (`mv` it to
  `/tmp` and back within one command — never leave production state deleted after a test run).
- The same rule applies to every path-override of this kind (`CALL_LEDGER_PATH`, `EW_*`,
  state files): tests inject temp paths, they never read the live ones.

## Pitfall — don't assert a channel is off from code reading alone

A switch in the source proves intent, not effect. Only two facts prove the mute: the empty
stdout of a real cron-style run, and the suppressed-status line in the push log. If the mute
is only claimed because the code looks right, say "implemented, not yet verified" instead of
"done".

## Reversal

Document one command in the report (`rm ~/.hermes/data/<channel>_off`), and have a test that
asserts the normal send path still works — so "reversible" is demonstrated, not promised.

## Worked example

`references/lowcap-memebot-killswitch.md` — the 30 Sep 2026 @memescallsbot mute: choke point,
exact flag/env names, the `MATI` log line, the live proof, and the test fix in code.
