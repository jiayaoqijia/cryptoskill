---
name: environment-record
domain: software-engineering/environment-record
trigger: "Writing down every environment class and its contract."
anti_trigger: "Not for infrastructure code, and not for release notes."
scope: "The written record of every environment class."
status: seedling
---

# Environment record

## Standard

The environment record lists every environment class — local, CI, preview, staging, and any specialist stage — with its definition source, its data policy, its concurrency rules, its cost ceiling, and its owner. It exists because environments multiply quietly, each one justifiable the day it is created, and the estate's properties are discovered only when something fails: which environments can be trusted for which claims, and which ones the next incident will start by suspecting.

Its second purpose is the parity contract stated upfront. Each class records what it promises to resemble — production in shape, or a subset, or a synthetic world — so a test result is read against the environment that produced it. A green suite on an environment that resembles nothing is a weaker claim than a red one on a stage that does, and the record is where that reading begins.

Primary source: <https://martinfowler.com/>.

## Decision rules

- Record each class with its definition source and provisioning method.
- Record the data class per environment: synthetic, masked, or shared-mutable.
- Record the concurrency policy and the isolation mechanism.
- Record the resemblance claim: what the environment is intended to model.
- Record cost ceilings, teardown rules, and the owner per class.
- Reconcile the record against live inventory monthly, and log the drift.

## Procedure

1. Enumerate environment classes and their definitions.
2. Fill in data policy, concurrency, resemblance claim, and owner per class.
3. Record cost ceilings and teardown wiring per class.
4. Verify each class's record against one live instance.
5. Reconcile monthly against inventory.
6. Amend with dates as classes change.

## Anti-patterns

- Records without a resemblance claim, so results are over-read.
- Environments whose existence is the record's only trace of them.
- Concurrency rules that live in a team's habits.
- A record never compared to running reality.
- No owner, so drift and cost have no respondent.

## Done checklist

- [ ] Classes enumerated with definitions.
- [ ] Data, concurrency, resemblance, owner recorded.
- [ ] Cost and teardown recorded.
- [ ] Verified against live instances.
- [ ] Monthly reconciliation logged.
- [ ] Dated amendments kept.

The record's resemblance claim is the line that resists the strongest temptation in test infrastructure: staging everything. An environment that claims to model a subset and models it well is a stronger instrument than one that claims everything and models nothing precisely.

## Sources

- Deployment pipeline stages: <https://martinfowler.com/bliki/DeploymentPipeline.html>
- Continuous integration environments: <https://martinfowler.com/articles/continuousIntegration.html>
- Reproducible provisioning: <https://reproducible-builds.org/>
