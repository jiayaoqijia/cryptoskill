---
name: step-level-tracing
domain: software-engineering/step-level-tracing
trigger: "Capturing each model call and tool call as an inspectable span."
anti_trigger: "Not for service request logs, and not for the run object as a whole."
scope: "One span per tool call and model call, captured at fidelity."
status: seedling
---

# Step-level tracing

## Standard

Each step gets a span: what was called, with what inputs, what was returned, how long it took, and what came before and after. Fidelity is the distinguishing choice: a tool call's input captured as a hash cannot be inspected, and a model call's output captured as a redaction cannot be diffed against later evaluations. The default is capture-in-full for the fields the run-record questions require, with explicit redaction reserved for named sensitive fields rather than broad truncation.

Two span types cover most trajectories: the generation span (prompt version, model, output, usage) and the tool span (name, arguments, return value, timing). Structured at capture, both types follow their schema; code stored in argument objects serializes entirely, not by inspecting a truncated view of visible text.

Primary sources: <https://opentelemetry.io/docs/specs/semconv/gen-ai/> and <https://langfuse.com/docs>.

## Decision rules

- One span per call, typed generation or tool; wrappers do not merge them.
- Capture arguments and returns at the level of the analysis questions.
- Record timings, retries, and error code on the span itself.
- Name each span from what the caller asked for, not from a UUID; search depends on bearer names.
- Include prompt and model identifiers on every generation span.
- Institute explicit redaction for named secret or personal fields; never truncate quality broadly.

## Procedure

1. Enumerate the call types the agent makes: generation, tool, retrieval, sub-agent.
2. Define each span capture-range list: input fields, output fields, exclusions.
3. Choose the sensitive-field redaction rule; write it down.
4. Instrument each call site to emit its span before and after execution.
5. Run a compound task; inspect the emitted trajectory against the questions.
6. Adjust capture range from what the inspection could not answer.

## Anti-patterns

- A span with truncated or partial arguments.
- Outputs written only for successful calls.
- Spans nameless or named by hash.
- Timings read separately, absent from the span.
- Redaction covering arguments so broadly that the call cannot be understood.

## Done checklist

- [ ] Span per call, typed generation/tool.
- [ ] Arguments and returns captured at inspection level.
- [ ] Timing/retry/error recorded on the span.
- [ ] Human-readable span names.
- [ ] Sensitive-field redaction rule written and applied.
- [ ] Capture gaps adjusted after inspecting one run.

A further rule of thumb: the capture question is not "how much can we store" but "which inspection will regret this field's absence". Storage is cheap; the irreversible loss is a field never written. The capture contract grows from lived debugging questions, and the record reconciles it against what the spans actually carry.

## Sources

- GenAI span conventions: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- Tracing introduction: <https://langfuse.com/docs>
- Conventions source: <https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/README.md>
