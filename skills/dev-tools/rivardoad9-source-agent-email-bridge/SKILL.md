---
name: agent-email-bridge
description: Bridge two AI agents over email; guardrails and files.
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [email, agents, bridge, gmail]
    related_skills: [hermes-cron-automation, email-inbox-triage]
---

# Agent-to-agent email bridge

## When to Use

Use when a human is acting as courier between Hermes and another AI agent that only has an inbox —
Cue/Manus agents, a hosted assistant, or any peer that cannot reach this machine. Not for real-time
work: email latency is minutes and the peer can never call local tools.

Hermes talks to another agent (here: Cue, `zemiz461@bot.cue.im`) over plain email. The other agent
runs in the cloud and cannot reach the local machine, so email is the transport: no public endpoint,
no exposed tools, no token to leak.

## Pieces

- `~/.hermes/scripts/cue_bridge.py` — polls Gmail, answers via `hermes -z`, sends in the same thread.
- Cron `2c5c2e1a5f7d`, every 10 min, `no_agent`, `deliver=local` (log only, never a chat ping),
  `failure_deliver=origin` so breakage is visible.
- State `~/.hermes/state/cue_bridge.json`: `seen` ids, `baseline_ms`, last 6 turns of history.
- Gmail label `Cue Bridge` + two filters (from/to the agent address): add label, remove `INBOX`
  and `UNREAD`. Gmail only notifies for inbox mail, so the thread is silent on the phone.

## Rules that make it work

1. **Baseline on first run.** Store `baseline_ms` and only answer mail newer than it. Without this
   the first run replies to months of old agent mail.
2. **Guard deterministically, not just in the prompt.** `BLOCK_RE` rejects delete/overwrite, `.env`,
   tokens, API keys, passwords, seed phrases, `git push --force`, `chmod 777`, `curl | bash`,
   withdraw/transfer before the agent ever runs. Reply with a fixed refusal asking for the human's
   confirmation. Test the regex with both Indonesian and English phrasings (`hapus`, `timpa`).
3. **The inner agent does not know the bridge sends mail.** It will answer "this machine has no
   mailer". Tell it in the system prompt that delivery is handled and that it should emit
   `ATTACH: /abs/path` lines for files.
4. **Attachments, not base64 chunks.** The script strips `ATTACH:` lines and builds `multipart/mixed`.
   Validate: realpath under `$HOME`, regular file, ≤15 MB, max 3, and refuse names containing
   `.env`/`.pem`/`.key`/`id_rsa`/`credentials`/`secrets` or paths under `~/.hermes/secrets`.
5. **Cap the inbound body** (~4000 chars) and cut quoted history at `On ... wrote:` so the agent does
   not re-read the whole thread.
6. **Timeout ≥600 s** per turn: tasks that touch real repos take minutes.

## Setup checklist for a new peer

1. Get the peer's address from the peer itself.
2. Add the peer address plus owner address to the script constants.
3. Create label + the two filters via Gmail API (`settings/filters`), archive existing threads.
4. Send an intro mail, wait for a reply, then run the script once to prove both directions.
5. Register the cron with `deliver=local`.

## Verification

- Thread message count and labels: fetch the thread, confirm only `Label_x` + `SENT`, never `INBOX`/`UNREAD`.
- Sent mail: walk `payload.parts`, check `Content-Disposition: attachment` and byte sizes.
- Executed-task claims: re-run the command yourself before believing a summary.

## Pitfalls

- Empty stdout when nothing is new — that is what keeps the cron silent; do not print status lines.
- `metadata` format sometimes returns `payload` without `headers`; use `full` and read `payload.headers`.
- First run must set the baseline and exit silently, otherwise it answers the archive.
- Long answers get truncated by the mail provider; attachments solve it, chunking is a dead end.
