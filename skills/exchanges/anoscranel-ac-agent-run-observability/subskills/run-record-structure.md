---
name: run-record-structure
domain: software-engineering/run-record-structure
trigger: "Defining the object that captures a whole agent run."
anti_trigger: "Not for the ledger or SLO telemetry, and not for offline eval."
scope: "The whole run as an object: spans, inputs, outputs, timing, lineage."
status: seedling
---

# Run record structure

## Standard

A run record is the durable object a run leaves behind: its unique identifier, the model and instructions that began it, every step it took, and the linkage between steps that lets the whole trajectory be read after completion. The unit of capture is the run; the unit of inspection is the step; the two are joined lineage.

The record's claim to existence is after-the-fact understanding. The final answer of an agent says what it concluded; the run record says what it saw, tried, and rejected on the way. Design begins with the questions the record must answer — why did it call this, what did this step cost, did it retry, which path did it take between the branching steps — because those questions decide the minimum content of every span.

Primary sources: <https://opentelemetry.io/docs/specs/semconv/gen-ai/> and <https://langfuse.com/docs>.

## Decision rules

- Give every run a unique identifier recorded before the first step executes.
- Model each model call and each tool call its own span; a step that wraps both keeps them as separate ones.
- Link every span to the run and to its parent step; trajectory lineage survives the run's end.
- Assign a model-result identifier to each generation step; subsequent steps reference it when they build on it.
- Capture the instruction set and tool manifests at run start; an unrecorded context makes replay impossible.
- Make the record whole-run durable access available to debugging after completion.

## Procedure

1. Define the run entity: unique identifier, starting state, model, manifest, timestamp.
2. Define the span entity: type (generation/tool), inputs, outputs, duration, parent.
3. Define the linkage: run→span parent, span→span causality, output→next-input reference.
4. Choose the store: write-ahead, so a crashed run leaves a partial but readable trajectory.
5. Test with a real run without calling a tool, then a run that does.
6. Verify reconstruction from the record matches what an observer saw live.

## Anti-patterns

- Logging only the final answer; the trajectory is the object of interest.
- One blob per run; steps cannot be inspected without parsing the whole.
- Store the prompt but not the tool manifests; replay then mocks the wrong tools.
- LOSing the linkage between generation and tool steps.
- No unique run identifier; runs from the same prompt cannot be told apart.

## Done checklist

- [ ] Run entity with a unique identifier.
- [ ] Span entity of generation and tool calls.
- [ ] Lineage linkage both directions.
- [ ] Instruction set and tool manifest captured at start.
- [ ] Write-ahead so crashed runs leave a trajectory.
- [ ] Reconstruction verified from the record alone.

## Sources

- GenAI tracing conventions: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- Tracing documentation: <https://langfuse.com/docs>
- GenAI conventions on OpenTelemetry: <https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/README.md>
