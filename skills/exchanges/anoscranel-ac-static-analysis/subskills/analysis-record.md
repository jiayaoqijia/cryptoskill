---
name: analysis-record
domain: software-engineering/analysis-record
trigger: "Writing down the rules the team enforced and why."
anti_trigger: "Not for the tool's output, and not for the review thread."
scope: "The written record of rules, severities, and exceptions."
status: seedling
---

# Analysis record

## Standard

The analysis record states the enforced rules with their intents and severities, the trial data that justified each promotion, the suppression inventory with reasons and expiries, and the baseline with its trend. It exists because rules outlive the people who chose them and suppressions outlive the people who wrote them — and without a record, the defaults of dead arguments govern living code.

Its second purpose is the argument itself. When a rule fires and someone disagrees, the question is not the finding but the rule, and the rule's justification lives here: the intent in one line, the trial's false-positive data, the severity decision, and the date. A team that can point at that answers in a minute; a team that cannot re-argues from scratch each time, and the argument is lost to whichever side is tireder.

Primary source: <https://martinfowler.com/>.

## Decision rules

- Record every enforced rule with its intent, severity, and adoption date.
- Record trial data — false-positive rate and findings acted on — for each promoted rule.
- Record the suppression inventory with reasons and expiry dates.
- Record the baseline size and its trend against the adoption date.
- Record rule changes as dated amendments, never silent edits.
- Review the whole record on a calendar cadence, not when someone complains.

## Procedure

1. Assemble the rule set with intents and severities.
2. Attach each rule's trial data.
3. Export the suppression inventory with reasons and expiries.
4. Record the baseline size and the reporting cadence.
5. Amend with dates on every rule or severity change.
6. Calendar a full review and record its outcome.

## Anti-patterns

- Rules enforced with no recorded intent.
- Suppressions with no expiry and no review.
- A baseline recorded once and never trended.
- Silent severity changes between releases.
- A record reviewed only when a rule annoys someone.

## Done checklist

- [ ] Rules recorded with intents and severities.
- [ ] Trial data attached per rule.
- [ ] Suppression inventory current.
- [ ] Baseline and cadence recorded.
- [ ] Changes dated.
- [ ] Review scheduled and held.

A useful addition is the rule's history line: promoted on a date from trial data, severity argued once by whom. When the same rule is challenged every quarter by a new arrival, the recorded history ends the re-litigation without dismissing the challenger, who may be right this time.

## Sources

- Continuous integration quality practice: <https://martinfowler.com/articles/continuousIntegration.html>
- Technical debt management: <https://martinfowler.com/bliki/TechnicalDebt.html>
- Empirical software engineering: <https://dl.acm.org/>
