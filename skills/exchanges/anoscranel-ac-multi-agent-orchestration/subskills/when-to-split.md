---
name: when-to-split
domain: collaboration/when-to-split
trigger: "Deciding whether to add a second agent to a task; weighing coordination overhead against parallel speedup"
anti_trigger: "A task that fits in one read and one edit; adding agents for performance on serial steps"
scope: "Deciding when a multi-agent split is justified by independent contexts, parallel wall-clock need, or producer-validator separation"
status: seedling
---

# When to Split

## Standard

- **Anthropic, "Building effective agents" (2024)**: agent architectures should start from the simplest possible design (single agent with tools); workflow patterns like orchestrator-workers or evaluator-optimizer are added only when tasks require distinct sub-problems, independent contexts, or parallel exploration. <https://www.anthropic.com/engineering/building-effective-agents>
- **Brooks, _The Mythical Man-Month_**: adding workers to a serial task increases coordination overhead faster than output, because communication paths scale quadratically while individual capacity remains linear. <https://www.pearson.com/en-us/subject-catalog/p/mythical-man-month-the-essays-on-software-engineering-anniversary-edition/P200000000149/9780201835953>
- **Handoff tax research**: every transfer of state between models loses context and incurs token and latency costs, making unwarranted splits a net negative for accuracy.
- **House baseline**: one agent is the default for any task that can be verified in a single pass; splitting requires a stated structural justification. ⚠️ House threshold.

## Decision rules

1. If a task is serial and fits in a single context window, do not split it.
2. If two sub-tasks share eighty percent of their required context and must execute in sequence, keep them in one agent.
3. Split only when sub-tasks have genuinely disjoint context requirements that exceed single-window reliability or when parallel wall-clock execution is mandatory.
4. Split when producer-validator separation is required (whoever builds must not approve).
5. If the coordination overhead (message framing, file handoffs, sync checks) exceeds fifty percent of the total task time, revert to a single agent. ⚠️ House threshold.
6. Never add an agent to solve a prompt clarity problem; fix the prompt instead.

## Procedure

1. Inspect the task requirements and list all distinct sub-components.
2. Check whether the sub-components can be executed in parallel or require strict serial dependency.
3. Calculate the context overlap: what percentage of files and instructions do both sub-components need?
4. Estimate the coordination overhead: number of handoffs, file writes, and verification checks needed between agents.
5. Apply the justification test: does the split achieve parallel speedup, isolate untrusted context, or enforce producer-validator separation?
6. If no test passes, abort the split and assign the task to a single agent.
7. If justified, define the exact boundary between the agent scopes before dispatching.

## Anti-patterns

- **Premature swarm.** Spawning multiple agents for a task a single agent finishes in two turns. Fix: keep it single.
- **Shared-brain split.** Two agents working on the exact same files with overlapping instructions. Fix: merge them or partition the files.
- **Serial relay race.** Passing output from agent one to agent two to agent three sequentially without parallel gain or validation need. Fix: collapse into one stream.
- **Hiding prompt ambiguity behind agents.** Adding workers because the primary prompt was unclear. Fix: rewrite the prompt.

## Done checklist

- [ ] The task has been evaluated for serial vs parallel structure.
- [ ] Context overlap has been measured or estimated.
- [ ] A concrete justification (parallel wall-clock, disjoint context, or validation split) is recorded.
- [ ] Coordination overhead has been weighed against expected speedup.
- [ ] Single-agent default was attempted or ruled out by structural constraints.

## Sources

- Anthropic, "Building effective agents": <https://www.anthropic.com/engineering/building-effective-agents>
- Brooks, _The Mythical Man-Month_: <https://www.pearson.com/en-us/subject-catalog/p/mythical-man-month-the-essays-on-software-engineering-anniversary-edition/P200000000149/9780201835953>
- Handoff tax research: internal architectural notes on multi-agent communication limits.
