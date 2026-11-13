---
name: failure-classification
domain: software-engineering/failure-classification
trigger: "Sorting agent failures by the step and reason that caused them."
anti_trigger: "Not for one best answer, and not for service error budgets."
scope: "Where it went wrong: classify by step, reason, and stage."
status: seedling
---

# Failure classification

## Standard

An agent failure is a trajectory with a wrong destination, and the useful classification locates the step where it left the road. The classes come from the span types: a generation step can mis-route (the model chose the wrong tool or none), a tool step can return the unexpected (error, empty, or wrong-scale output), and the loop can fail between them (a result misread, a stop condition never met). Classification by step type turns "the agent failed" into "the third tool call returned an unhandled empty and every later step built on that".

The proportion matters more than the instance. One mis-routed call is noise; a weekly pattern of mis-routes at the same step is a tool-description defect, and only classified counts reveal the pattern. The classification scheme is small, fixed, and recorded — every failed run gets exactly one primary class and any number of contributing ones.

Primary sources: <https://arxiv.org/abs/2308.03688> and <https://opentelemetry.io/docs/specs/semconv/gen-ai/>.

## Decision rules

- Classify the primary failure: the first step whose output made the destination wrong.
- Use a small fixed vocabulary of classes; extension is a dated change.
- Every failed run receives exactly one primary class; contributors are optional.
- Record the class on the run record, not in a separate unjoinable sheet.
- Aggregate weekly; the pattern is the finding, not the instance.
- A wrong final answer with a sound trajectory is its own class; the steps are not blamed for the conclusion.

## Procedure

1. Load the failed run's trajectory.
2. Walk to the first step whose output steered the run wrong.
3. Assign the primary class from the fixed vocabulary.
4. Note contributing classes for later steps that compounded the error.
5. Write the classification onto the run record.
6. Aggregate per class per week and review for patterns.

## Anti-patterns

- "Model was dumb" as a class; the vocabulary exists to prevent it.
- Blaming the last step when the first divergence is the honest primary.
- Classes extended ad hoc until the weekly count means nothing.
- Classification kept apart from the run record where it cannot be joined.
- Pausing at instance-level analysis instead of counting proportions.

## Done checklist

- [ ] Primary failure step located.
- [ ] Fixed vocabulary applied.
- [ ] One primary class recorded on the run.
- [ ] Contributors noted.
- [ ] Weekly aggregation run.
- [ ] Pattern review on the calendar.

## Sources

- Agent failure analysis: <https://arxiv.org/abs/2308.03688>
- GenAI span structure: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- Trace inspection: <https://langfuse.com/docs>
