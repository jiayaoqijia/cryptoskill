---
name: codegen-record
domain: software-engineering/codegen-record
trigger: "Writing down every generation contract the system carries."
anti_trigger: "Not for the generated output, and not for release notes."
scope: "The written record of generators and their contracts."
status: seedling
---

# Codegen record

## Standard

The codegen record lists every generator in the system with its input, its output, its freshness policy, and its owner. It exists because generation pipelines are numerous and quiet: each one works, each one is a dependency between two artifacts, and the person debugging a mismatch months later needs the map — which artifacts derive from which inputs, and which check catches the drift between them.

Its second purpose is upgrade safety. A generator upgrade changes output with no input change; a schema change changes output with no generator change; a language target upgrade changes both. The record states what is pinned, what is trusted, and what each check catches, so an upgrade plan knows what must be re-verified and what can be assumed.

Primary source: <https://www.openapis.org/>.

## Decision rules

- List every generator with input, output targets, freshness policy, and owner.
- Pin and record the generator version and the input version consumed.
- Record the drift check attached to each pair and what it detects.
- Record the escalation: what the record's owner does when a check fires.
- Attach a decision log for generator upgrades and pin changes.
- Reconcile with the build's declaration so the record matches what actually runs.

## Procedure

1. Inventory every generation step and its artifacts.
2. Record inputs, outputs, freshness, owner per generator.
3. Record versions pinned and the drift check per pair.
4. Record the escalation procedure on check failure.
5. Append every upgrade and pin change to the log.
6. Reconcile against the build configuration and fix divergences.

## Anti-patterns

- A record listing generators without their inputs' owners.
- No drift check recorded against a committed output.
- Upgrades applied without a log entry explaining the diff.
- A record that has never been reconciled against the build.
- Escalation undefined, so a fired check waits for whoever notices it.

## Done checklist

- [ ] Generator inventory complete.
- [ ] Inputs, outputs, freshness, owner recorded per generator.
- [ ] Versions pinned and recorded.
- [ ] Drift check per pair recorded.
- [ ] Escalation defined.
- [ ] Record reconciled against the build.

The record should also note the blast radius per generator: which services and which downstream artifacts break when it fires, and which check catches the failure first. That single line turns a fired check from a mystery into a bounded problem, and it is the line responders reach for first.

## Sources

- OpenAPI as a generation contract: <https://www.openapis.org/>
- Pinning and reproducibility: <https://reproducible-builds.org/>
- Build and CI practice: <https://martinfowler.com/articles/continuousIntegration.html>
