---
name: tool-doubles
domain: software-engineering/tool-doubles
trigger: "Deciding which tools run real and which are doubled."
anti_trigger: "Not for the harness scenarios, and not for guardrail wiring."
scope: "Deciding mock, stub, or real for each tool."
status: seedling
---

# Tool doubles

## Standard

Each tool in a scenario is either run real or replaced by a double. A mock asserts against expected calls; a stub returns a canned recorded result; a fake reimplements a cheap approximation; a real call executes against the actual system. The decision is per tool, per scenario, and hinges on two questions the harness spec states explicitly: is the tool's authentic behaviour what the scenario tests, and can a real call do irreversible harm or spend real money?

The classification is irreversibility first. A tool that can delete data, charge a card, or send an email to a human is doubled in every scenario without a stated, deliberate exception. A tool whose authentic responses the agent must handle — the weird data, the slow latency, the error — is real in scenario sets that specifically test handling. And the default for read-only external tools: real where cheap and stable, doubled where flaky or metered, with the choice recoded as data that future signature changes.

Primary sources: <https://en.wikipedia.org/wiki/Mock_object> and <https://testing.googleblog.com/>.

## Decision rules

- Every irreversible tool is doubled in every scenario, without exception by default.
- The choice per tool per scenario is data in the harness spec, not a code comment.
- Double returns replay recorded real responses; hand-crafted responses encode assumptions.
- Real calls reserved for: behaviour-under-test is the tool itself; or data freshness matters.
- A double of an irreversible tool must faithfully refuse as well as succeed.
- Recorded doubles are re-captured when the real tool's contract changes; drift check scheduled.

## Procedure

1. Enumerate the agent's tools; mark each for irreversibility and external cost.
2. Mark every irreversible tool as doubled by default across all scenarios.
3. For each scenario, mark each reversible tool real-or-double with the rationale.
4. Capture doubles by recording real responses, not by writing fictional ones.
5. Reduce latency variance: doubles assert fixed behaviour rather than varying.
6. Schedule contract-drift checks between doubles and real tools.

## Anti-patterns

- A real irreversible call in a routine regression scenario.
- Fictional double responses that smuggle the author's guesses about the API.
- Doubling everything, so no real behaviour is ever exercised before ship.
- The choice buried in code, invisible to spec review.
- Doubles whose response format drifts from the real contract, undetected.

## Done checklist

- [ ] Irreversibility marked per tool.
- [ ] Doubles default-on for irreversible tools.
- [ ] Per-scenario choices recorded with rationale.
- [ ] Doubles captured from real responses.
- [ ] Doubles model refusals as well as successes.
- [ ] Contract-drift check scheduled.

## Sources

- Stands-in classification: <https://en.wikipedia.org/wiki/Mock_object>
- Google testing practice: <https://testing.googleblog.com/>
- Test-double selection craft: <https://en.wikipedia.org/wiki/Software_testing>
