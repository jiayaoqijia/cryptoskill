---
name: delegation-prompts
domain: collaboration/delegation-prompts
trigger: "Writing the prompt for a subagent or worker agent; setting up output contracts and checkpoint files"
anti_trigger: "Writing vague operational instructions with no word caps; expecting the agent to ask clarifying questions"
scope: "Worker prompt structure: role preamble, mission in one line, verbatim constraints, output contract, file checkpointing, no questions"
status: seedling
---

# Delegation Prompts

## Standard

- **House delegation standard**: every worker prompt must contain a role preamble, a one-line mission, verbatim constraints, an explicit word cap, and an incremental output contract where the file serves as the checkpoint. ⚠️ House threshold.
- **Anthropic, "Effective agent design"**: structured prompt templates with clear tool and output specifications reduce agent hallucination and format drift during delegation. <https://www.anthropic.com/engineering/building-effective-agents>
- **No-questions discipline**: subagents must flag gaps in state rather than halting to ask questions, preventing interactive deadlock in unattended loops.

## Decision rules

1. The delegation prompt must open with a clear role preamble defining the agent's function.
2. The core mission must be stated in exactly one line following the preamble.
3. All negative constraints and boundary rules must be included verbatim.
4. An explicit word cap (e.g., "Under 1100 words") must be enforced on narrative or text outputs.
5. The output contract must require incremental file writes (appending sections as completed) rather than a single terminal dump.
6. Instruct the agent never to ask clarifying questions back to the supervisor; if blocked, it must record the gap and stop.

## Procedure

1. Draft the role preamble naming the agent's functional role.
2. Write the single-line mission statement defining the exact deliverable.
3. Paste all mandatory constraints and format rules verbatim from the master spec.
4. Set the word cap and language requirements (e.g., plain English, Markdown only).
5. Specify the target output file path and the incremental write protocol (append on completion of each section).
6. Add the no-questions rule: state that ambiguous gaps must be flagged with warning markers rather than interactive queries.
7. Review the complete prompt against the delegation checklist before dispatching.

## Anti-patterns

- **Vague assistance request.** "Please help me research this topic and do your best." Fix: specify exact deliverable and file path.
- **Monolithic terminal dump.** Expecting the agent to hold the entire report in memory and emit it all in the final chat turn. Fix: require incremental file appends.
- **Interactive deadlock.** Allowing the agent to stop and ask the user questions mid-task. Fix: enforce gap-flagging and continuation.
- **Unbounded length.** Leaving word counts unspecified, leading to bloated prose. Fix: set strict word caps.

## Done checklist

- [ ] Role preamble defined.
- [ ] Mission stated in one line.
- [ ] Constraints included verbatim.
- [ ] Explicit word cap and Markdown format set.
- [ ] Incremental file checkpointing protocol established.
- [ ] No-questions discipline enforced.

## Sources

- Anthropic, "Effective agent design": <https://www.anthropic.com/engineering/building-effective-agents>
- Internal operational standards for subagent delegation prompts and checkpoints.
