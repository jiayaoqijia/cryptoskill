---
name: log-hypothesis-testing
domain: software-engineering/log-hypothesis-testing
trigger: "Testing a causal hypothesis against logs you cannot break into."
anti_trigger: "Not for instrumentation design or log pipelines (that is ac-reliability)."
scope: "Testing a hypothesis against logs when you cannot break into the process."
status: seedling
---

# Log hypothesis testing

## Standard

The scientific method from ac-debugging still governs production work, but the experiment changes shape: instead of a breakpoint, the hypothesis is tested against what the logs already contain or can be made to contain. The question is always falsifiable in logs' terms — "if the retry caused the duplicate charge, then two charge attempts with the same correlation ID will appear within the window" — and the logs either contain that pattern or they do not.

The honest discipline is stating in advance which log pattern would disprove the hypothesis. Without it, log reading degrades into confirmation searching: a thousand lines will contain something consistent with any theory, and the absence of a pattern is only meaningful if you said beforehand what absence would look like. Record the prediction before running the search.

## Decision rules

- State the hypothesis as a specific, falsifiable log pattern before searching.
- State the pattern that would disprove it, and search for that too.
- Bound the time window first — from the event backwards — before grepping.
- Distinguish "the logs show the opposite" from "the logs are absent"; missing logs are missing evidence, not evidence.
- Note the log level actually deployed; debug lines that were never enabled cannot confirm anything.
- Record searches that found nothing, with the query and the window.

## Procedure

1. Narrow the time window around the failure.
2. Write the hypothesis as a concrete log pattern.
3. Write the disproving pattern.
4. Search both within the window.
5. Classify the result: confirmed, refuted, or undetermined due to missing logs.
6. Record the queries and windows either way.

## Anti-patterns

- Grepping for anything that fits a theory already believed.
- Treating absent logs as absence of the event.
- Searching unbounded time and matching unrelated occurrences.
- Reading logs whose timestamps span hosts without correcting for skew.
- Skipping the disproving search.

## Done checklist

- [ ] Time window bounded.
- [ ] Hypothesis expressed as a log pattern.
- [ ] Disproving pattern stated.
- [ ] Both searches run.
- [ ] Result classified including undetermined.
- [ ] Queries recorded.

One more distinction keeps the method honest: logs record what the code chose to say, so a hypothesis about behaviour the code never logs is untestable by this route, and the right next move is to add a targeted log line for the next occurrence — deployed and noted in the record — rather than to keep re-searching what was never captured.

## Sources

- Structured logging and its uses: <https://martinfowler.com/articles/structured-logging.html>
- Log analysis practice: <https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-analytics-overview>
- Hypothesis-driven debugging: <https://sre.google/sre-book/debugging-tips/>
