---
name: handoff-mesh
description: "Built-in communication layer for multi-agent setups. Full-mesh handoff folders (any agent can hand off to any other), an hourly watcher that surfaces open handoffs, weekly archive cleanup, and a completion-reporting loop so every handoff is handled AND verified. The durable 'brain' counterpart to real-time channels like Buzz."
version: 1.2.0
author: Gentech
tags: [handoff, coordination, multi-agent, mesh, inbox, communication, vault]
license: MIT
---

# Handoff Mesh — Communication Layer for Multi-Agent Setups

## When to Use
- You run **more than one agent** (multi-agent strategy) and they need to hand work to each other.
- An agent finishes something and another agent (or a human) needs to pick it up.
- You want a **durable, searchable** coordination layer — not just real-time chat.
- You want to know, at a glance, what handoffs are open and whether they got done.

## What This Is
A **full-mesh handoff system** built on the vault (Obsidian) — the durable brain.
Any agent can drop a handoff into any other agent's inbox. A watcher surfaces
open handoffs hourly. Nightly maintenance archives old ones. And a
completion-reporting loop closes the deal: the agent that reads a handoff
reports back what it did before it's marked resolved.

This is the **storage + verification** half of agent communication. Real-time
channels (Buzz, Telegram) are the *talking* half; this is the *remembering and
proving* half. They complement each other — the vault stays the source of truth.

## The Layout
```
01-HANDOFFS/
    INBOX/
        <group>/                    ← one receive folder per agent/group
            <YYYY-MM-DD>-<topic>.md ← a handoff note for that agent
            _archive/               ← resolved notes (auto-moved, purged weekly)
    <from>-to-<to>/                 ← optional explicit sender→receiver folders
```

## The Protocol (4 steps — the loop)

### Step 1 — SEND: drop a handoff into the target's inbox
Write `<date>-<topic>.md` into the target group's `INBOX/<group>/` folder.
Format:
```markdown
# <topic>
**From:** <agent/group>
**To:** <group>
**Date:** <YYYY-MM-DD>
**Status:** open

## What's needed
<what the receiving agent should do>

## Context / files
<any links or paths>
```
Commit + push (or `ob sync`).

### Step 2 — WATCH: surface open handoffs automatically
Run the watcher hourly (or on each agent's wake-up). It scans every inbox lane
and reports any note still `Status: open` (not resolved, not archived).
```bash
python3 handoff-watcher.py [vault_path]
```
- **Silent when clear** — only pings when there's actually something to do.
- **Quiet overnight** — schedule it for waking hours only (e.g. 7 AM–11 PM ET).
- Wire it as a `no_agent` cron (pure script, zero tokens) so it's cheap.

### Step 3 — ACT + REPORT: the agent that reads it reports back
This is the half that makes handoffs *verified*, not just *seen*:
1. **Read** the handoff → acknowledge it in the group (never silent).
2. **Act** on it.
3. **Report back** — post a short "done / what I did" note to the sender's lane
   or the group, so the loop closes. This is the completion-reporting rule.
4. **Mark resolved + archive** only AFTER the work is verified.

### Step 4 — CLEAN: archive weekly so it never gets too big
Nightly/weekly maintenance:
- Move resolved notes to `_archive/`.
- **Purge `_archive/` entries older than 7 days.**
- Auto-archive stale OPEN notes older than 7 days (still unresolved).

## The Watcher Script
`handoff-watcher.py` (stdlib-only, stable output — safe as a `monitor_script`):
- Lists every `<group>/` subfolder under `INBOX/`.
- Finds `*.md` notes NOT in `_archive/` and NOT marked resolved.
- **STATEFUL — reports only NEW changes.** It keeps a state file
  (`handoff-watcher.state.json`) of what it already reported, and only prints:
  - 🆕 NEW open handoffs (appeared since last run)
  - ✅ CLEARED handoffs (were open, now resolved)
  - 🔧 NEW recent completions (`--days N`)
- **Silent when nothing changed** — if no handoff appeared/cleared and no new
  completion, it prints NOTHING, so the cron stays quiet until there's a real
  signal. This is the watchdog pattern: report only what's new, not everything
  every time.
- **Also surfaces recent completions** by scanning each group's
  `<group>-completions.md` — so you see what agents actually shipped, not just
  what's open. Add `--days N` to widen the window.
- **Tappable Obsidian deep-links** — every open handoff prints an
  `obsidian://open?vault=NAME&file=...` link that opens the note in the
  user's Obsidian app. Set your vault name via `--vault-name NAME` (or edit
  `VAULT_NAME` in the script). The links only open if the note has synced to
  the device (Obsidian Sync) first.

Wire it as a `no_agent` cron with the **empty-stdout = silent** semantics:
non-empty output is delivered, empty output posts nothing. State file keeps it
quiet between genuine changes.

Example:
```bash
# Daily window of 2 days, vault named "gentech":
python3 handoff-watcher.py --days 2 --vault-name gentech
```

## Second Brain Setup Preset — wire a new agent's brain in one go
Use this when someone adds a **new agent / second brain** to an existing
fleet. It wires the full mesh so the new agent reads and acts on handoffs
automatically, out of the box:

1. **Create the inbox lanes** for the new agent under `01-HANDOFFS/INBOX/`:
   ```
   01-HANDOFFS/INBOX/<newgroup>/
       _archive/          # resolved notes (auto-moved, purged weekly)
   ```
   Add `<newgroup>` to `KNOWN_GROUPS` in `handoff-watcher.py`.

2. **Create the completion file** so the watcher can report what this agent ships:
   `01-HANDOFFS/<newgroup>-completions.md` (start with `# <Group> Completions`).

3. **Install the skill** on the new profile:
   ```bash
   # copy the whole handoff-mesh skill dir into the new profile's skills
   cp -r skills/handoff-mesh /root/.hermes/profiles/<new>/skills/
   ```
   Copy `scripts/handoff-watcher.py` to `/root/.hermes/profiles/<new>/scripts/`.

4. **Wire the cron** (`no_agent`, pure script, zero tokens). Create with
   Hermes cron, `script=handoff-watcher.py`, `deliver=origin`, schedule
   `*/15 11-23,0-3 * * *` (every 15 min, 7 AM–11 PM ET) — or any waking-hours
   cadence. Set `--vault-name <your-vault>` in the script args so the links
   open correctly.

5. **Consolidate with wake-up**: patch the new profile's wake-up-protocol
   Step 3 to (a) check the INBOX for open handoffs, and (b) report a
   completion note back to the sender before marking resolved. This makes the
   loop (read → act → report → resolve) run on every session start.

Once wired, the new agent's watcher fires every 15 min, surfaces open handoffs
with tappable Obsidian links + recent completions, and the agent's wake-up
closes the loop — all fleet-wide, all zero-token.

## Decision Table
| Situation | Action |
|-----------|--------|
| Agent A finishes work for Agent B | A writes handoff to B's inbox |
| Handoff sits open >1 hour | Watcher surfaces it; B picks it up |
| B reads the handoff | B acknowledges + acts + reports back |
| B completes the work | B marks resolved + archives, reports what it did |
| Handoff unresolved >7 days | Nightly maintenance auto-archives it |

## Pitfalls
- **Reading without reporting** — a handoff archived as "resolved" with no
  completion note is a silent failure. Always report what you did.
- **No archive cleanup** — inboxes grow unbounded. Purge `_archive/` weekly.
- **Watcher pinging overnight** — schedule it for waking hours only.
- **Only watching your own inbox** — in a mesh, check ALL lanes; any agent can
  hand off to any other.
- **Real-time chat ≠ durable record** — keep the handoff in the vault; chat is
  for talking, the vault is for remembering.

## Verification
- [ ] Every agent/group has an `INBOX/<group>/` folder + `_archive/`.
- [ ] Watcher surfaces open handoffs hourly (silent when clear).
- [ ] Agent that reads a handoff reports back what it did.
- [ ] Resolved notes archived; `_archive/` purged weekly.
- [ ] No handoff left unread or unreported at a stopping point.
