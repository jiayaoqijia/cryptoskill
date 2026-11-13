---
name: secops-record
domain: security-hardening/secops-record
trigger: "Writing the standing record of a security operations program."
anti_trigger: "Not for the incident report itself, and not for compliance filings alone."
scope: "The written record: detections, metrics, drills, and their dates."
status: seedling
---

# SecOps record

## Standard

The ops record is the program's memory: what detections exist and their measured precision, what the queue metrics have shown over time, what hunts ran and excluded or confirmed, which vulnerabilities carry accepted exceptions and until when, and when each restore test and drill actually ran. It exists because security operations metrics decay within weeks and drift without a written baseline.

Its second purpose is the honest metric. Every number in operations has a blind spot, and the record is where the blind spot is stated next to the figure: time-to-detect excluding the unwatched channel, patch time excluding the frozen estate, click rate for one campaign difficulty. A record that pairs each metric with its caveat cannot be flattened into a good-news dashboard by later hands, which is precisely the property an audit or a serious incident will want.

Primary sources: <https://www.cisa.gov/> and <https://osf.io/prereg/>.

## Decision rules

- Record every detection with its coverage target, test evidence, and last re-measure date.
- Record queue metrics per period with each metric's blind spot named.
- Record hunts with hypotheses, windows, and coverage limits.
- Record exceptions with owner, rationale, and expiry — no unbounded accepts.
- Record drills and restore tests with measured times, not successes.
- Amend by dated append; corrections rewrite nothing silently.

## Procedure

1. Assemble the detection inventory with test dates.
2. Add the metric series with their caveats.
3. Add hunts, exceptions, and drills with dates.
4. Review on the stated cadence and append new periods.
5. At each review, re-date everything whose evidence has gone stale.
6. Reference the record from every incident and audit artifact.

## Anti-patterns

- A dashboard without the caveats that made its numbers meaningful.
- Exceptions recorded without expiry, which is open-ended risk.
- Drill outcomes recorded as pass or fail without elapsed times.
- Silently updated baselines so drift is invisible.
- A record nobody reads for a year, populated with year-old numbers.

## Done checklist

- [ ] Detection inventory with test dates.
- [ ] Metrics with blind spots named.
- [ ] Hunts with coverage limits.
- [ ] Exceptions owned and expiring.
- [ ] Drills with measured times.
- [ ] Append-only amendments.

The record also serves the incident that has not happened yet: in the first hour of a real event, the answer to what telemetry exists, what has been tested, and what is accepted risk is this record, and an out-of-date copy is worse than none because it is trusted.

## Sources

- Operations and exercises guidance: <https://www.cisa.gov/>
- Pre-registration practice for stated metrics: <https://osf.io/prereg/>
- Program standards context: <https://csrc.nist.gov/>
