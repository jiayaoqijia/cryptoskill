---
name: golden-scenarios
domain: software-engineering/golden-scenarios
trigger: "Building the scenario set an agent harness runs."
anti_trigger: "Not for live-run inspection, and not for model benchmarks."
scope: "Building the scenario set from real traces, not invention."
status: seedling
---

# Golden scenarios

## Standard

A golden scenario is a recorded instance of the agent doing real work, captured before the harness existed: the user's request, the tool calls the agent made, the answer it produced. The set is built by mining run records for the work actually asked, not by imagining what a user might want — invented scenarios test the author's assumptions about the agent, and those assumptions are exactly what fails in production.

The mining discipline has categories. Representative flows: the common path, weighted by frequency. Edge cases from real logs: the malformed input, the tool that returned empty, the interrupted run. Historical regressions: every shipped defect becomes a scenario that fails against the old build and passes against the new, forever. The proportions follow real usage, and scenario count is a budget question: coverage against a live corpus, not a synthetic-number ambition.

Primary sources: <https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html> and <https://arxiv.org/abs/2308.03688>.

## Decision rules

- Source scenarios from real run records and production traces, not invention.
- Categorise as: representative flow, logged edge case, historical regression.
- Add a regression scenario for every shipped defect, dated, kept forever.
- Weight the mix by observed usage frequency, not by what looks interesting.
- State the coverage target as corpus representation, not as a count.
- Re-mine after each agent scope change; stale scenarios mislead both directions.

## Procedure

1. Collect run records covering the period since the last scenario refresh.
2. Cluster by task shape and user request type.
3. Select representative flows proportionally with edge cases and regressions.
4. Record each scenario's origin: trace ID, date, and category.
5. Freeze the set version; the harness run cites the version.
6. Schedule the re-mine cadence and log each refresh.

## Anti-patterns

- Inventing scenarios from the author's imagination of use.
- Deleting regression scenarios after they pass a few times.
- Over-weighting exotic edge cases because they are interesting.
- Quoting scenario count as coverage.
- Never refreshing the set until production breaks.

## Done checklist

- [ ] Scenarios mined from real traces.
- [ ] Categorised with origin recorded per scenario.
- [ ] Regressions added for every shipped defect.
- [ ] Mix weighted by usage frequency.
- [ ] Coverage stated as corpus representation.
- [ ] Refresh cadence scheduled and first refresh dated.

The set also deserves an adversarial stripe: alongside mined traces, a small fixed group of deliberately hostile scenarios probes the failure modes the traces never show, because polite users and well-formed inputs are what most traces contain. These are labelled adversarial, not counted as representative, and refreshed when incident records reveal a new attack shape.

## Sources

- End-to-end test discipline: <https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html>
- AgentBench, evaluating LLMs as agents: <https://arxiv.org/abs/2308.03688>
- Preregistration practice for frozen sets: <https://osf.io/prereg/>
