---
name: session-handoff
domain: collaboration/session-handoff
trigger: "The session is ending mid-task; write a checkpoint; resume this work in a new session; the agent died mid-run; state only lives in chat"
anti_trigger: "Human shift or on-call handover (subskills/person-handoff.md); verifying a received handoff (subskills/resumption-check.md); the artifact's format rules (subskills/handoff-artifact.md)"
scope: "Agent and session handoffs: the checkpoint file is the state; continue the same session where possible; partial-file continuation; the running ledger"
status: "seedling"
---

# Session Handoff

## Standard

- **Ganz et al. (2026), arXiv:2608.24358**: continuing another model's context recovers less than half the quality gap; a fresh receiver pays the handoff tax on everything. Continuing the same session or agent, when it still exists, is the cheapest transfer. <https://arxiv.org/abs/2608.24358>
- **Sun et al. (2026), arXiv:2608.24569**: what survives a session boundary is what was written down; judgments that live only in the running context die with it. <https://arxiv.org/abs/2608.24569>
- **Google SRE Book, "Being On-Call"**: engineers log work as it happens so the next shift inherits a record, not a reconstruction. <https://sre.google/sre-book/being-on-call/>
- House line: the checkpoint file is the state; chat is scenery.

## Decision rules

1. If it is not in the file, it does not exist; chat history is not state.
2. Continue the same session where possible; a new session pays the tax on every recovered fact.
3. Write incrementally: append each completed work block as it finishes; never one dump at the end.
4. Decisions and constraints enter the ledger at the moment they are set, not later.
5. Checkpoint before any long or risky block; a dead worker leaves clean state.
6. On resume, verify before continuing: read the ledger, check artifacts match, then work from the file, never from memory of the old conversation.

## Procedure

1. Create the ledger file before the first work block: a done / doing / next skeleton plus a constraints block.
2. After each block, append what finished with its evidence, what is in flight, and the next block's first step.
3. Record decisions as they are made: the decision, one line of rationale, any constraint it adds.
4. Keep artifact pointers current: exact names and locations, re-checked at each checkpoint.
5. Before ending, run a completeness pass: a stranger can read done, doing, next, and the constraints standalone.
6. Resuming in the same session: state the plan in one line, then continue; do not re-derive finished work.
7. Resuming in a new session: read the ledger, verify the artifacts still match it, then continue from the first unfinished block.
8. Partial-file continuation: if a prior worker died mid-write, read what exists, continue from where it stops, and mark the seam.

## Anti-patterns

- **State in chat only.** The next session starts blind. Fix: file first, always.
- **Final dump.** One huge write at the end; a crash loses everything. Fix: incremental appends.
- **Amnesiac restart.** A new session with no ledger re-does solved work. Fix: verify, then continue.
- **Stale ledger.** The file lags the work. Fix: update at block boundaries, every block.
- **Context as contract.** Decisions and constraints kept only in the running context. Fix: ledger entry at the moment of decision.

## Done checklist

- [ ] Ledger file exists and is the single state source.
- [ ] Done / doing / next current as of the last completed block.
- [ ] Constraints and decisions recorded at creation time.
- [ ] Artifact pointers live and re-checked.
- [ ] Resume path documented: same session continues; new session verifies then continues.
- [ ] Partial writes marked and seamed.

## Sources

- Ganz et al. (2026), arXiv:2608.24358: <https://arxiv.org/abs/2608.24358>
- Sun et al. (2026), arXiv:2608.24569: <https://arxiv.org/abs/2608.24569>
- Google SRE Book, "Being On-Call": <https://sre.google/sre-book/being-on-call/>

⚠️ Continuing the same session assumes the platform can resume it; where it cannot, the ledger path above is the only state, and the tax is unavoidable.
