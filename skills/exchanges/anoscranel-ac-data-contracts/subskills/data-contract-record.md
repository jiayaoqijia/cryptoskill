---
name: data-contract-record
domain: software-engineering/data-contract-record
trigger: "Writing the record of a data contract and its enforcement."
anti_trigger: "Not for data dictionaries, and not for compliance attestation."
scope: "The written record: terms, owner, checks, and version."
status: seedling
---

# Data contract record

## Standard

The contract record states the schema and semantics, the freshness and completeness guarantees with their measurement, the compatibility rule, the owner and escalation route, the checks and where they run, and the current version. Those six items describe an interface between teams, and each is what a consumer needs in order to rely on the dataset rather than hope about it.

Its second function is to make the contract's history legible. A version number with a change log records what changed and when, which is what allows a consumer investigating a defect to determine whether the dataset's behaviour changed or their expectation did. Without the history, that question is unanswerable and the conversation becomes attribution.

Primary sources: <https://www.w3.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record states each field with its type, unit, and null semantics.
- Freshness and completeness are recorded with the measurement behind them.
- The compatibility rule and change classification are recorded.
- The owner, channel, and escalation expectation are recorded.
- Each check is recorded with its enforcement point and severity.
- The version and change log are recorded, with the date of each change.

## Procedure

1. Record the schema and semantics.
2. Record the guarantees and their measurement.
3. Record the compatibility rule.
4. Record the owner and escalation.
5. Record the checks and enforcement points.
6. Record the version and change log.

## Anti-patterns

- A record without the measurement behind its guarantees.
- Ownership recorded but not reachable.
- Checks listed without where they run.
- No change log, so the contract's history is reconstructed from memory.
- A version that increments without a description of what changed.

## Done checklist

- [ ] Schema and semantics recorded.
- [ ] Guarantees and measurement recorded.
- [ ] Compatibility rule recorded.
- [ ] Owner and escalation recorded.
- [ ] Checks and enforcement recorded.
- [ ] Version and change log recorded.

The record should also state the contract's review date, since a dataset's guarantees drift as the pipeline behind it changes: a contract written when the feed arrived hourly and never revisited will still claim hourly after the schedule has quietly become daily.


The record should also name the consumers it knows about, since a contract's guarantees are only meaningful relative to the readers it protects: a dataset with three registered consumers and ten unregistered ones is a contract that covers a fraction of its actual surface.

## Sources

- Data interchange standards: <https://www.w3.org/>
- Pre-registration practice for stated terms: <https://osf.io/prereg/>
- Governance guidance: <https://csrc.nist.gov/>
