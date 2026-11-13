---
name: agent-dashboards
domain: software-engineering/agent-dashboards
trigger: "Building dashboards that answer agent questions, not just chart them."
anti_trigger: "Not for general BI, and not for service SLO boards."
scope: "Dashboards for answers to agent questions, not just graphs."
status: seedling
---

# Agent dashboards

## Standard

A service dashboard answers "is the system healthy"; an agent dashboard answers behavioural questions: which steps fail most, which tools misfire, how often runs retry, where tokens concentrate, how the failure-class mix moves week over week. The unit is the question: each panel exists because someone asks it during debugging or review, and a panel no one reads is removed.

The honest dashboard shows distributions, not just averages. Mean steps-per-run hides the tail where failures live; the p95 and the failure-class counts are the panels that carry information. Every panel names its denominator — per run, per step, per class — because an agent-metric without a stated base is a decorative number.

Primary sources: <https://opentelemetry.io/docs/specs/semconv/gen-ai/> and <https://langfuse.com/docs>.

## Decision rules

- Start from the debugging questions; every panel maps to one.
- Show distributions and counts, not just means; the tail is the content.
- Every panel states its denominator: per run, per step, per class.
- Keep a weekly failure-class mix panel; the pattern is the finding.
- Keep a per-step cost concentration panel; money follows steps.
- Remove panels that no question reads; dashboards accrete silently.

## Procedure

1. List the recurring debugging and review questions.
2. Map each question to the trace field that answers it.
3. Build the panels with denominators stated on the panel.
4. Add the two standing panels: failure-class mix and cost concentration.
5. Review after two weeks; note which panels anyone actually consulted.
6. Prune the unread; date the pruning in the observability record.

## Anti-patterns

- A vanity panel of total runs; volume is not health.
- Means without distributions; the interesting runs are the tail.
- Metric without a denominator.
- A dashboard that mirrors the vendor default rather than the questions.
- Panels no one reads, kept out of inertia.

## Done checklist

- [ ] Panels built from stated questions.
- [ ] Distributions beside means.
- [ ] Denominators on panels.
- [ ] Failure-class mix panel standing.
- [ ] Cost concentration panel standing.
- [ ] Unread panels pruned with dates.

A further discipline: agent dashboards answer behavioural questions, so they drift from service dashboards in what counts as an event — a run, not a request; a step, not an endpoint. If a panel's unit was inherited from service monitoring without a question behind it, that inheritance deserves a second look, because agent traces answer trajectory questions that request metrics never posed.

## Sources

- GenAI semantic fields: <https://opentelemetry.io/docs/specs/semconv/gen-ai/>
- Dashboard practice: <https://langfuse.com/docs>
- Conventions repository: <https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/README.md>
