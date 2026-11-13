---
name: constraints-verbatim
domain: collaboration/constraints-verbatim
trigger: "Compress this handoff without losing rules; the summary dropped a must; check the constraints survived; a safety note got softened; what is still forbidden"
anti_trigger: "Choosing what to pass at all (subskills/context-selection.md); verifying state on the receiving end (subskills/resumption-check.md); writing the artifact's sections (subskills/handoff-artifact.md)"
scope: "Never summarize constraints: copy must / must-not / may rules verbatim and run a binding-state check after any compression"
status: "seedling"
---

# Constraints Verbatim

## Standard

- **Sun et al., "When Must Becomes Maybe: Erosion of Workflow Constraints in LLM Agent Handoffs" (2026), arXiv:2608.24569**: handoffs carry tasks forward while eroding established judgments; a requirement that must be satisfied before action becomes a caveat the next agent may set aside. Measured failure: multihop compression deactivated 97.2 percent of safety blockers; ownership deferral deactivated 76.7 percent. Restoring the full blocker description raised recognition from 6.2 to 99.2 percent and cut forbidden action from 85.2 to 0.0 percent. An authorization-check prompt cut forbidden action to 1.6 percent while artifact deactivation stayed at 95.3 percent, so a clean endpoint can conceal a damaged handoff. <https://arxiv.org/abs/2608.24569>
- **Ganz et al., "The Handoff Tax" (2026), arXiv:2608.24358**: a lossy transfer costs the receiver more than it saves the sender; ambiguity is paid for downstream. <https://arxiv.org/abs/2608.24358>
- **Gawande, The Checklist Manifesto (2009)**: checklists catch what memory drops under load; the constraint block is that checklist. ⚠️ cited without URL.
- House line: semantic availability is not operational preservation; the receiver can repeat a rule and still not obey it.

## Decision rules

1. Constraints are copied, never paraphrased; keep the words must, must not, may, only, before, until.
2. A constraint keeps its role: a blocker stays a precondition, never a caveat. "Must be satisfied before action" does not become "was flagged".
3. Run a binding-state check after any compression: for each constraint, classify must, must-not, or may, and confirm it still constrains.
4. Compress around constraints, never through them: cut narrative first; constraints are never cut.
5. Conditions travel with the rule: "when X" goes wherever "do Y" goes.
6. A conflict between constraints is surfaced, not silently resolved.

## Procedure

1. Extract every constraint into one block, separate from narrative.
2. Tag each constraint: must (required before action), must-not (forbidden action), may (permitted latitude), each with its condition.
3. Copy the exact wording; fix nothing, improve nothing.
4. Compress the rest of the handoff.
5. Re-run the binding-state check on the compressed artifact: every rule still tagged, still binding, count unchanged.
6. Test as the receiver: answer "what is authorized and what is not" from the artifact alone; any gap means restore verbatim from source.
7. If any hop in the chain compressed constraints, rebuild the block from the original source, never from the lossy copy.

## Anti-patterns

- **Paraphrase drift.** "Do not deploy before review" becomes "review first". Fix: verbatim block.
- **Ownership deferral.** "The previous team flagged a concern" obliges nobody. Fix: name who must do what before what.
- **Caveat burial.** A blocker inside a narrative paragraph. Fix: constraint block at the top.
- **Reconstruction from memory.** Rebuilding constraints from a lossy summary. Fix: original source only.
- **Endpoint-only check.** "The final step worked, so the handoff was fine." Fix: check the artifact, not just the outcome.

## Done checklist

- [ ] Constraint block extracted with must / must-not / may tags and conditions.
- [ ] Wording verbatim from the original source.
- [ ] Binding-state check run after compression; tag count unchanged.
- [ ] Receiver can answer what is authorized from the artifact alone.

## Sources

- Sun et al. (2026), arXiv:2608.24569: <https://arxiv.org/abs/2608.24569>
- Ganz et al. (2026), arXiv:2608.24358: <https://arxiv.org/abs/2608.24358>
- Gawande, The Checklist Manifesto (2009). ⚠️ cited without URL.

⚠️ The percentages above come from one experimental setup on one paper; the mechanism (constraint deactivation under compression) is the load-bearing finding, not the exact rates.
