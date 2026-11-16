---
name: blast-radius-bounds
domain: software-engineering/blast-radius-bounds
trigger: "Capping the damage an unchecked agent run can do between checks."
anti_trigger: "Not for capacity planning, and not for tool permissioning."
scope: "Caps and walls that make the worst unchecked run survivable."
status: seedling
---

# Blast-radius bounds

## Standard

Even a well-gated agent occasionally runs unchecked — the guardrail service is down, the bus routing is misconfigured, the model finds a path that was not classified. The blast-radius layer assumes that and bounds the damage: per-run resource caps (money, calls, bytes, time), per-object walls (locked scopes the agent cannot modify regardless of instruction), and review windows that pause the run when a threshold is crossed.

The frame is honest about the failure class: nothing in the guardrail layer can prove a strong model will not try a bypass, and only a true sandbox proof or formal method can bound what code execution can do; what resource caps and walls bound is what can be done to production state, which is the layer's actual reach. The caps are computed from the worst plausible unchecked-run trajectory, sized to survive it, and recorded with the analysis.

Primary sources: <https://owasp.org/www-project-top-10-for-large-language-model-applications/> and <https://en.wikipedia.org/wiki/Session_(computer_science)>.

## Decision rules

- Every run carries a resource envelope: money, call count, data volume, wall-clock time.
- Envelopes are enforced at the bus, not at the model's discretion.
- Locked scopes — directories, projects, accounts — are un-writable regardless of instruction provenance.
- Crossing a threshold pauses the run for review rather than silently continuing.
- Caps are sized to the worst plausible unchecked-run trajectory and the reasoning is recorded.
- Caps are low enough to interrupt and correct, high enough not to trigger on normal work.

## Procedure

1. Enumerate the resources a run can consume or modify.
2. Compute the worst plausible unchecked-run trajectory for the task class.
3. Set the per-run cap for each resource with the derivation recorded.
4. Identify locked scopes the agent must not modify; hard-enforce at the bus.
5. Define pause conditions: which threshold crossings pause vs terminate.
6. Test with a hostile task that attempts to exceed each resource boundary.

## Anti-patterns

- Caps set so high they can never fire — a figure with no derivation.
- Caps at the model's reported level rather than at the bus layer.
- No locked scopes — every object modifiable by a persuasive-enough instruction.
- Caps tuned to the observed-normal range, not the worst-plausible unchecked-range.
- Silent Continue on cap-crossing; the envelope is not a guardrail if it does not pause.

## Done checklist

- [ ] Resource envelopes per run, enforced at the bus.
- [ ] Locked scopes defined and enforced.
- [ ] Caps derived from worst-plausible analysis, recorded.
- [ ] Pause conditions stated.
- [ ] Hostile-task test attempted each boundary.
- [ ] Caps placed low enough to matter, high enough to work.

## Sources

- OWASP LLM Top 10, resource-consumption and scope framings: <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
- Session-bound concepts: <https://en.wikipedia.org/wiki/Session_(computer_science)>
- AI risk controls: <https://www.nist.gov/itl/ai-risk-management-framework>
