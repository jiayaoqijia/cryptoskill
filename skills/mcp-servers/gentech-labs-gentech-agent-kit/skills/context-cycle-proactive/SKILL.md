---
name: context-cycle-proactive
description: "At 80-90% context, save to the brain, route to the right channel, load fresh context, and resume. Built-in lifecycle so every agent stays synced to the second brain and never drops work."
version: 1.1.0
author: Gentech
tags: [context, memory, resume, session-hygiene, save, brain]
license: MIT
---

# Context Cycle — Proactive Save & Resume

## When to Use
- Conversation/working context reaches **80-90%** and you can't make room (the trigger).
- Mid-way through a big build and you hit a natural stopping point.
- The user says "save progress," "start new," "load a new context," or "/new."
- You notice memory pressure and want to save before it drops the ball.

## The Problem This Solves
Even with a large context window, active build sessions fill up fast. When context hits
~80-90% and you can't make room, the session degrades and work gets dropped. This is the
**proactive** protocol: you detect the pressure, save your place to the brain, route the
log to the right channel, load a fresh context, and pick the task back up.

## The Cycle — 5 Steps (Save → Route → Load → Resume)

### Step 1: SAVE progress to the brain (vault / second brain)
Write a dated progress file to the vault so nothing is lost. Use the context bridge
generator if available, then fill it in:
```bash
python3 <path-to>/session-hygiene/scripts/context-save.py   # if present in the agent
```
Capture the real content (bridge path varies by setup; the principle is the same):
- **Active work**: what you were building, current task, dependencies
- **Decisions made**: the calls taken + reasoning
- **Blockers**: anything stuck or needing the user/another lane
- **Next steps**: the exact resume point, so the next session picks up cleanly

**Rule:** Save where you are BEFORE you move on. Never let memory fill up and drop the ball.

### Step 2: ROUTE the log to the right channel
Decide where the progress note belongs. This is the agent's judgment call — where does
this work need to live, and who needs to see it?

| Content | Channel / folder |
|---|---|
| Coordination, decisions, blockers, status | **HQ** (your main group, `00-HQ/`) |
| Ideas, considerations, open questions | **Mess Hall** (`11-Mess Hall/considerations.md`) |
| Heavy build / code / dev progress | **Labs** (`01-HANDOFFS/gentech-to-labs/`) |
| Finance / treasury / yield | **Treasury** (`01-HANDOFFS/gentech-to-treasury/`) |
| Content / social / hackathon | **Entertainment** (`01-HANDOFFS/gentech-to-entertainment/`) |

For cross-agent work, drop a handoff file into the relevant `01-HANDOFFS/<lane>/` folder
so that lane's agent picks it up on wake-up. Sync the vault after writing so the second
brain and backups have it: `cd <vault> && ob sync` (or your repo's sync command).

### Step 3: LOAD a fresh context
Compact / start a new session so the context window is clear. Tell the user:
> "Memory at [X]% — saved progress to the brain, logged to [channel]. Ready for /new?"

If /new isn't wanted yet, at minimum clear the working context via compaction so the
window is fresh but the save is already in the vault.

### Step 3a: PROMPT the user to start new when you can't do it yourself (Jordan directive Aug 16 2026)
**The problem it fixes:** agents cut it close at high memory instead of starting a fresh
context — so work gets dropped or the session degrades. An agent often CANNOT start a new
context on its own (no `/new` access, no self-compaction). The fix is to **ask the user**,
explicitly and early, instead of pushing to the edge.

**The rule — at ~85% memory (or the agent's execute threshold), prompt the user:**
> "I'm going to save progress and log everything to the brain. Go ahead and start new
> (`/new`), and we can continue the conversation."

**Do this BEFORE the save is critical, not after.** The sequence:
1. Save progress to the brain (Step 1) + route the log (Step 2) — so nothing is lost.
2. **Prompt the user to start new** — give them the exact words to say/type.
3. On the fresh session, load the resume point (Step 4) and continue — do NOT restart.

**Why this matters:** a lost save is never worth the extra minutes of context. Prompting
the user to start new is the reliable way to clear the window when the agent can't do it
itself. This is a labeled, required behavior — not a nice-to-have.

### Step 4: RESUME the task
On the fresh session (or after compaction), load the resume point:
1. Read the latest context bridge / `latest-context.md`
2. Read the relevant handoff file if you wrote one in Step 2
3. Re-establish: what was in progress, decisions, next steps
4. Continue the task from the exact checkpoint — do NOT restart it

### Step 5: CONFIRM continuity
Verify the resume landed: the task picks up where it stopped, no duplicate work, and
the next cycle starts from the new checkpoint. If anything was lost, recover from the
vault archive / session search rather than redoing it.

## Context Thresholds — tiered by model window (Jordan approved Aug 11 2026)

The execute point depends on the model's context window, not one flat number. A single
threshold either churns fast agents (interrupting healthy long builds) or strands slow ones.

| Agent | Window | 80% (think) | Execute save | Why |
|---|---|---|---|---|
| Forge (DeepSeek Flash) | 5M tokens | 85% | **90%** | Huge headroom, quality holds late |
| Gentech (GLM 5.2 / DeepSeek V4 Flash) | 128K | 80% | **85%** | Degrade begins past ~85% |
| Gentech Flash (GLM 4.5 Flash) | 64K | 80% | **80%** | Small window fills fast, degrade hits earlier |

**Rule (Jordan):** save EARLY rather than late. At 80% you don't wait — you assess the
road ahead (next task size, next stop) and start the save if the path looks long. Losing
a save is never worth pushing context to the limit. The 85/90 execute is the firm
backstop; the 80% assessment + natural-stopping-point rule is the real protection.

## Pitfalls
- **Don't skip Step 1 (save)** — routing to a channel without first saving progress means
  the next session has no resume point.
- **Don't just say "memory's full"** — always execute the cycle: save → route → load → resume.
- **Don't restart a finished task** — if the save shows the task was complete, don't redo it.
- **Cross-agent work needs a handoff file** — logging to your own group alone doesn't wake
  up the other agents.
- **Sync the brain** — a local file nobody pushed doesn't help other agents or backups.

## Verification
After a cycle, confirm:
1. Progress saved to the context bridge (dated file exists)
2. Log routed to the correct channel/handoff folder
3. Brain synced (sync command ran)
4. Resume point identified in the latest bridge file
5. Fresh context loaded; task resumes from the checkpoint, not from scratch
