---
name: interrupt-harness
domain: software-engineering/interrupt-harness
trigger: "Building the hold, kill, and divert paths that actually stop an agent."
anti_trigger: "Not for agent design, and not for logging."
scope: "Hold, kill, and divert — and how interruption itself fails."
status: seedling
---

# Interrupt harness

## Standard

An interrupt is only as good as the path that executes it. The hold path parks a proposed call in a reviewable state; the kill path terminates the session and commits nothing in progress; the divert path asks the agent to continue with a boundary restated. Each path has a specific failure mode to test for: the hold that leaks (a call dispatched while awaiting review), the kill that does not take (stop signal ignored, sub-processes orphaned, in-flight parallel calls completing regardless), the divert that resumes the same forbidden attempt in new words.

The kill test is the harness's acceptance test: run an agent whose task requires a forbidden action, interrupt mid-flight, and prove from the system state — not from logs alone — that nothing completed. A parallel call emitted before the kill that lands after the kill is the classic failure; the harness must sequence termination so that in-flight calls are cancelled or their effects rolled back, and verify by direct inspection of the tool layer.

Primary sources: <https://owasp.org/www-project-top-10-for-large-language-model-applications/> and <https://en.wikipedia.org/wiki/Idempotence>.

## Decision rules

- Every gated action has exactly one of three dispositions: hold, kill, divert — pre-stated per tier.
- The kill path is idempotent at the tool layer: repeated or late-arriving calls are rejected, not double-executed.
- Verify kill by direct state inspection at the tool layer, not by log absence.
- The divert path carries a re-stated boundary and a counter; repeated diversions on the same run escalate to hold or kill.
- The hold queue retains everything needed to either resume or audit: input, reasoning, proposed action, replay token.
- Timeouts on holds are explicit; the hold expires closed, never open.

## Procedure

1. Write the disposition per tier into the action-class table.
2. Implement the three paths with their invariants: hold never leaks, kill never orphans, divert never silently repeats.
3. Run the kill acceptance test: forbidden task, interrupt mid-flight, inspect tool-layer state directly.
4. Run the hold leak test: propose a gated call, hold, attempt dispatch from other paths — all must fail.
5. Run the divert escalation test: restate the boundary, attempt again, measure escalation.
6. Record each test's outcome with its timestamp in the guardrail record.

## Anti-patterns

- Treating the model's co-operation ("okay I will stop") as the interrupt mechanism — only the harness can truly stop.
- Killing the session but leaving long-running server-side jobs alive.
- Holds with indefinite review horizons and no expiry.
- Divert with no counter; the agent retries the forbidden call re-worded, repeatedly.
- No direct state verification after kill — trusting logs that report nothing.

## Done checklist

- [ ] Dispositions pre-stated per tier.
- [ ] Kill tested by direct tool-layer state inspection.
- [ ] Hold tested for leak from all other dispatch paths.
- [ ] Divert carries re-stated boundary and escalation counter.
- [ ] Hold expiry is closed, not open.
- [ ] All three tests recorded with timestamps in the record.

## Sources

- OWASP LLM Top 10, excessive-agency and consumption framings: <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
- Idempotence for kill-safety at the tool layer: <https://en.wikipedia.org/wiki/Idempotence>
- NIST AI RMF execution controls: <https://www.nist.gov/itl/ai-risk-management-framework>
