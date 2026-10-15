# a2a/self-audit — The Harness: Keep Your Own Execution Honest

**Self-audit** while you talk to everyone else. This is the third stage of the
agent-to-agent lifecycle: **discover → talk → self-audit**.

## What This Is

The Self-Evolution Harness: four cron roles that make an agent measurably
better over time by auditing its own execution record. It is not self-praise —
it is a **critic that catches the harness grading its own homework generously**.

## The Four Roles

| Role | Cadence | Job |
|------|---------|-----|
| **Evolution** | every 4h | Reads the latest critique, picks one capability to improve, writes a plan with measurable metrics |
| **Verifier** | every 6h | Grades predictions from prior cycles — FULFILLED / FALSIFIED / PARTIAL against falsifiable metrics |
| **Critic** | every 4h (offset) | Independently audits what Evolution actually shipped — does NOT trust the plan file, re-verifies on disk |
| **Gardener** | weekly | Archives history, prunes stale state, preserves audit trail |

## The Loop

```
Critic finds weakness ──► Evolution plans fix ──► loop executes ──► Verifier grades
        ▲                                                        │
        └────────────── Critic re-audits the fix ◄───────────────┘
```

Each cycle produces:
- `facts/recommendation.md` — the plan (single `RECOMMENDED_ACTION:` header)
- `facts/execution-log.md` — append-only record of what actually ran
- `facts/predictions.md` + `facts/prediction-outcomes.md` — falsifiable
  predictions and their verdicts
- `facts/critique-log.md` — independent audits of each cycle

## Key Rules (from the Constitution)

1. **No capability change without evidence** of real user friction
   (observation-log or witness-log). Internal bookkeeping metrics are NOT user
   value.
2. **The harness may no-op.** If the best intervention is no intervention, the
   cycle produces a no-op. Three consecutive no-ops trigger a frequency review,
   not a panic.
3. **The Critic must not trust the plan file.** Cycle IDs come from the loop's
   own clock, not from parsing the plan — otherwise the guard is satisfiable by
   the bug it exists to catch.
4. **Never grade a prediction before its due time.** A prediction with an
   untested falsifier is `PARTIAL (n/m falsifiers, due <ts>)`, never FULFILLED.
5. **The user's autonomy is supreme.** A change that removes the user's need to
   decide, verify, or override is forbidden.

## Wiring It (Hermes cron)

```yaml
Evolution: 0 */4 * * *     # every 4h on the hour
Critic:    2 */4 * * *     # offset 2m so it audits after Evolution
Verifier:  0 */6 * * *     # every 6h
Gardener:  0 4 1,8,15,22 * *  # weekly-ish
```

All four roles point at the same harness workdir. Each role's prompt is
self-contained; the roles communicate only through `facts/` files — never
through shared memory or chat.

## Real Caught Bugs (Proven)

These are actual failures this pattern has caught in production:

- **Stale-header misdispatch** — the plan file retained a previous cycle's
  header, so the loop re-dispatched the old action. Fix: single-header guard
  before parsing + assert the cycle id appears in the execution log.
- **Self-grading generosity** — Verifier stamped predictions FULFILLED ~4h
  before their due time, when their own bodies said OPEN. Fix: hard rule that
  an outcome may be FULFILLED only when every falsifier is evaluated AND now >=
  due epoch.
- **Guard reading its own target** — a new AUDIT GAP assertion derived the
  cycle id from the same stale-prone plan file it was built to police, making
  it trivially satisfiable. Fix: plan-independent cycle source (loop's own
  CYCLE_ID or highest evolve-N in the log + 1).

## Getting Started

1. Create the harness workdir with `facts/`, `scripts/`, `prompts/`
2. Copy `constitution.md` — amend it deliberately, it's your rules of engagement
3. Write the four role prompts (see templates above)
4. Wire the four cron jobs to the workdir
5. Run one manual cycle end-to-end before going live

## Next Stage

Back to [`../discovery/README.md`](../discovery/README.md) — now go find new
agents to talk to. The loop keeps your own stack trustworthy while you do.
