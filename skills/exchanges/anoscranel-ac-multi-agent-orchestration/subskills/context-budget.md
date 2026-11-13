---
name: context-budget
domain: collaboration/context-budget
trigger: "Determining what information to pass to a subagent; handling model handoffs and trajectory compression"
anti_trigger: "Dumping entire conversation transcripts into a subagent prompt; paraphrasing safety constraints"
scope: "Minimal sufficient context, not the transcript; constraints passed verbatim; direction-dependent handoffs; file-based state"
status: seedling
---

# Context Budget

## Standard

- **ArXiv 2608.24358, "The Handoff Tax"**: model-handoff interface flips with direction; escalating from cheap to strong models requires passing *less* trajectory (full trajectory recovers under fifty percent of the quality gap), whereas downshifting from strong to cheap requires passing *more* trajectory. <https://arxiv.org/abs/2608.24358>
- **ArXiv 2608.24569, "Constraint Leakage in Compression"**: normal text compression yields approximately one hundred percent constraint deactivation and fifty-four percent forbidden-action leakage; constraints must be passed verbatim rather than paraphrased. <https://arxiv.org/abs/2608.24569>
- **House rule on state**: file-based state stored in designated markdown files on disk beats chat memory for inter-agent handoffs, preventing context drift across sessions. ⚠️ House threshold.

## Decision rules

1. Never pass a raw chat transcript to a subagent when a structured summary and file pointer will suffice.
2. When escalating from a cheaper model to a stronger model, pass a concise task definition and minimal background (less trajectory).
3. When downshifting from a strong model to a cheaper model, pass comprehensive background, completed sections, and explicit instructions (more trajectory).
4. All negative constraints and forbidden actions must be passed verbatim; never paraphrase security rules or output format constraints.
5. Store intermediate working state in files on disk rather than passing large text blobs through chat messages.
6. If the context passed to an agent exceeds its effective attention window or degrades instruction adherence, trim non-essential background.

## Procedure

1. Evaluate the target agent model and its position in the handoff chain (escalation vs downshifting).
2. Gather the minimum necessary background documents and file paths required for the sub-task.
3. Extract all mandatory constraints and forbidden actions from the parent directive verbatim.
4. Compose the context payload: concise mission statement, verbatim constraints, and file pointers.
5. If downshifting, append completed artifacts and full trajectory history to the prompt payload.
6. Dispatch the prompt and verify that the agent acknowledges the constraints before starting work.

## Anti-patterns

- **Transcript dump.** Forwarding fifty turns of chat history to a subagent. Fix: extract the current state and file pointers.
- **Paraphrased rules.** Rewriting "Never write to /tmp" as "Try to avoid temporary folders." Fix: quote rules verbatim.
- **Lost state.** Relying on chat memory for multi-step handoffs between agents. Fix: write state to disk files.
- **Ignoring handoff direction.** Passing full history when escalating, or zero history when downshifting. Fix: match trajectory to direction.

## Done checklist

- [ ] Context payload limited to minimal sufficient information.
- [ ] Constraints and forbidden actions passed verbatim without paraphrasing.
- [ ] Handoff direction accounted for (less trajectory for escalation, more for downshifting).
- [ ] Working state stored in disk files rather than chat memory.
- [ ] Subagent verified to have received and acknowledged constraints.

## Sources

- ArXiv 2608.24358, "The Handoff Tax": <https://arxiv.org/abs/2608.24358>
- ArXiv 2608.24569, "Constraint Leakage in Compression": <https://arxiv.org/abs/2608.24569>
- Internal operational guidelines on context budgets and handoff hygiene.
