---
name: environment-drift
domain: software-engineering/environment-drift
trigger: "Detecting when environments stop describing their definition."
anti_trigger: "Not for configuration service choice, and not for drift causes elsewhere."
scope: "Detecting when environments stop matching."
status: seedling
---

# Environment drift

## Standard

An environment is provisioned from a definition and then lives its own life: someone patches a package to unblock a test, someone raises a timeout, someone adds a debug service and removes it later, or does not. Drift is the gap between what the definition says the environment is and what it has become, and it is the reason a suite that passed for months starts failing without anyone changing the tests or the code they test — the environment changed underneath them.

The detection options are ordered by cost and certainty. Recreate-from-definition — rebuild from scratch periodically, or always — is the strongest, because it makes drift impossible by refusing to keep drifted state. Configuration inspection compares state against the definition and reports the gap, cheaper and weaker. Nothing, which lets drift accumulate until a panicked debugging session discovers the drift by hand, is the default when no one chooses.

Primary source: <https://martinfowler.com/>.

## Decision rules

- Record which environments are immutable-by-construction: recreated on every use.
- Schedule recreate-from-definition for every long-lived environment on a calendar cadence.
- Apply patches that change an environment to its definition, never to the instance.
- Keep the drift report visible — last-recreated date on the environment status.
- Investigate a suite that worked-for-months-then-failed for environmental drift before code.
- Record every emergency patch with a follow-up to fold it back into the definition.

## Procedure

1. List environments and their definition sources.
2. Mark which are immutable-recreated and which are long-lived.
3. For long-lived environments, schedule the recreate cadence.
4. Change one environment deliberately and verify the drift detection notices.
5. Sweep out-of-band instance patches into the definitions.
6. Publish last-recreated status per environment.

## Anti-patterns

- Patching the instance to make today's test pass.
- Recreating only when something breaks, so drift is discovered in a panic.
- Definitions that no longer match any running environment.
- A drift report nobody looks at.
- Debug services left running in an environment and forgotten.

## Done checklist

- [ ] Environments listed with definitions.
- [ ] Immutable versus long-lived marked.
- [ ] Recreate cadence scheduled.
- [ ] Drift detection verified by deliberate change.
- [ ] Instance patches swept into definitions.
- [ ] Status published.

The recreate cadence is also the answer to the question of what drift costs: a weekly recreation bounds the lifetime of any unknown patch to seven days, which converts a class of mysterious failures into a class of failures with an upper bound on their cause's age.

## Sources

- Infrastructure reproducibility: <https://reproducible-builds.org/>
- Deployment pipeline practice: <https://martinfowler.com/bliki/DeploymentPipeline.html>
- Immutable infrastructure: <https://docs.docker.com/>
