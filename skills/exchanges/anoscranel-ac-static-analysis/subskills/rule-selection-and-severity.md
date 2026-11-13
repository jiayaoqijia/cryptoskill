---
name: rule-selection-and-severity
domain: software-engineering/rule-selection-and-severity
trigger: "Choosing which rules to enforce and how loudly."
anti_trigger: "Not for running the tool, and not for writing new rules from scratch."
scope: "Choosing rules a team will act on, and ranking them."
status: seedling
---

# Rule selection and severity

## Standard

Severity is a promise about response. A rule marked error says the build stops; warned says the author should consider; info says nothing, and should be deleted. Teams undermine the whole apparatus by mismatching severity to behaviour: errors that everyone bypasses teach that errors are optional, and a warning level crowded with stylistic findings buries the one finding that predicted a defect.

The selection criterion is action. A rule earns its error level when the team will fix every instance it finds today and forever; it earns a warning when the team wants the signal but not the obstruction; it earns removal when its findings generate discussion about the rule rather than the code. That last case is the quiet failure — a rule whose every finding is argued away trains reviewers to skip the section of the report it appears in.

Primary source: <https://martinfowler.com/>.

## Decision rules

- Assign error only to rules with unanimous fix-on-find commitment.
- Assign warning to rules whose findings are valuable but occasionally wrong.
- Prefer a strict superset: run info-rules invisibly and trial promotions from their data.
- Review the severity ladder when a rule's findings stop being acted on.
- Time-box new rules as warnings before promoting them, using the trial's false-positive data.
- Record every rule's intent in one line, so severity changes have a reason to point to.

## Procedure

1. Draft the rule set with a one-line intent per rule.
2. Assign severities by the action criterion.
3. Trial each new rule at warning level for a fixed period.
4. Collect its false-positive findings during the trial.
5. Promote, keep, or drop based on the trial data.
6. Record the final ladder with intents.

## Anti-patterns

- Errors that get routinely suppressed, hollowing the error level.
- Severity by default settings, copied unexamined.
- Info-level rules that produce output nobody reads.
- Promoting a rule to error without a trial.
- A severity ladder nobody reviews as the codebase changes.

## Done checklist

- [ ] Rule intents written.
- [ ] Severities assigned by action criterion.
- [ ] New rules trialled at warning.
- [ ] False-positive data collected per trial.
- [ ] Promotions justified by trial data.
- [ ] Ladder reviewed and recorded.

The action criterion cuts both ways, and it is worth recording: a rule demoted or dropped should leave a note of the findings it used to produce, so when the defect class it caught resurfaces in an incident, the record shows what was known rather than what was forgotten.

## Sources

- Code quality discipline: <https://martinfowler.com/articles/continuousIntegration.html>
- Code smell definitions: <https://martinfowler.com/bliki/CodeSmell.html>
- Software engineering literature: <https://dl.acm.org/>
