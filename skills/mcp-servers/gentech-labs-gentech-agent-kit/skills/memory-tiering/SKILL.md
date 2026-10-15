---
name: memory-tiering
description: "When saving/pruning memory, tier facts by relevance."
version: 1.0.0
author: Gentech
license: MIT
tags: [memory, context, tiering, agentic-behavior, fleet]
---

# Memory Tiering — Intelligence for Intelligence

Jordan's model (Aug 20, 2026): an agent's always-loaded memory (MEMORY.md / USER.md)
should NOT be a dump. It should be a **curated index** of the facts we touch every
session, with everything else parked in the vault brain where it's one search away.

## When to Use
- Before saving a NEW durable fact to persistent memory.
- When pruning / consolidating MEMORY.md or USER.md (including via the fleet dietician).
- When you notice a memory file approaching the 85% threshold.
- When a fact becomes RESOLVED and you decide whether to keep it loaded.

Two tiers:
- **Always-loaded** (MEMORY.md / USER.md) — facts referenced EVERY session. Identity,
  rails, wallet, rules, standing strategy. Lean, high-signal.
- **Vault brain** (retrievable) — facts referenced less often, or RESOLVED. Not lost,
  just parked. Pull back via session_search / search_files when the topic resurfaces.

## Why (the intelligence part)
- Every session reads the memory file. Bloat = slower, more tokens, worse focus.
- **More memory = worse performance** (proven Jul 28, 2026: elaborate memory stack
  deleted → agent worked dramatically better).
- Trimming from the BACK (oldest-first) is dumb — an old high-frequency fact gets
  archived while a recent resolved worry stays loaded. Tier by **relevance**, not age.

## Tiering rules

### ALWAYS-LOADED (keep in MEMORY.md/USER.md)
- **Identity**: who the agent is, personality, speech, the boss.
- **Core rails/keys**: payment rails, wallets, canonical repos, the strategy that
  shapes every decision.
- **Standing rules/red lines**: "never fake receipts," "spend less," "flag blockers
  immediately," "build first talk later."
- **Recurring topics** (per Jordan Aug 20): agentic treasury, x402, AWS, APIs.
- **Active commitments with near deadlines.**

### ARCHIVES TO VAULT BRAIN (low-frequency / resolved)
- **Resolved worries**: problem solved, deadline passed, task done. Compress or archive.
- **One-off events**: a single completed hackathon/hire/date.
- **Task progress / session logs**: go to the brain (Green Room / Mess Hall / handoffs),
  NOT persistent memory.
- **Any fact not touched in many sessions** and not needed for the standing model.

## How to apply (standing agentic behavior — every save)
1. Before adding memory, ask: "needed EVERY session, or only when this topic comes
   up?" Only-on-topic → save to the Vault instead.
2. When a fact is RESOLVED: compress to a one-liner or archive — don't keep the
   full narrative loaded.
3. At ~85% threshold: consolidate in ONE atomic batch (remove stale + add new),
   never cram.
4. Fleet dietician (memory-dietician.py) tiers by relevance, not back-of-file.
5. When a topic resurfaces, pull the archived entry back from the vault and re-load
   it if it's now a standing fact.

## Pitfalls
- Don't archive on a whim — if referenced across sessions, keep it.
- Don't keep resolved worries loaded "just in case" — archive them; the vault has room.
- The vault brain has room — that's its purpose. Overflow belongs there.
- This is a STANDING behavior, applied on every save, not a one-time cleanup.
