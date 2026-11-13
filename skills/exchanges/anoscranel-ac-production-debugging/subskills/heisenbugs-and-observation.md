---
name: heisenbugs-and-observation
domain: software-engineering/heisenbugs-and-observation
trigger: "A failure that disappears when you try to observe it."
anti_trigger: "Not for race condition repair (that is ac-debugging's scientific loop)."
scope: "Why attaching tools changes timing, and what that does to evidence."
status: seedling
---

# Heisenbugs and observation

## Standard

A heisenbug is a failure that changes when you measure it. The physical cause is usually timing: a debugger stops the world, a profiler changes scheduling, verbose logging adds milliseconds between two threads that were racing, and the extra delay lets the losing thread win. The observation does not cause the bug — the race was always there — but it changes which way the race resolves.

The practical consequence for production debugging is a rule about evidence: an observation tool is itself an intervention, and its outputs must be recorded as such. A profiling run that shows no deadlock is not evidence there is no deadlock; it is evidence that the deadlock does not occur under profiling. The skill is choosing observations with the smallest timing footprint first, and reserving the invasive ones for when the cheap ones have failed.

## Decision rules

- Record every observation tool used, with a note that its output is from an instrumented run.
- Prefer sampling profilers and read-only state capture over stopping-the-world tools.
- Order interventions from cheapest to most invasive; each one can perturb the failure away.
- If a failure disappears under observation, do not conclude it is fixed; conclude the observation changed the timing.
- Compare the timing budget of the tool with the timing window of the suspected race.
- Use a canary capture — logging deployed to one instance — to limit perturbation to a subset.

## Procedure

1. Note the suspected timing window for the failure.
2. List the available observations ordered by footprint.
3. Deploy the cheapest observation first and record its footprint.
4. If the failure vanishes, record the perturbation explicitly rather than closing the case.
5. Escalate to invasive tools only with a written reason for their use.
6. Record which intervention last still showed the failure.

## Anti-patterns

- Declaring a race fixed because it stopped reproducing under a debugger.
- Shipping an invasive profiler fleet-wide when one instance would serve.
- Ignoring the tool's own overhead when reading its output.
- Alternating tools so fast that none shows a stable picture.
- Treating "cannot reproduce under observation" as "does not exist".

## Done checklist

- [ ] Timing window of the failure estimated.
- [ ] Observations ordered by footprint.
- [ ] Each intervention's footprint recorded.
- [ ] Non-reproduction under observation recorded as perturbation, not cure.
- [ ] Last-observed-failure intervention identified.
- [ ] Written note distinguishes instrumented from uninstrumented runs.

## Sources

- Race detection and its limits: <https://github.com/google/sanitizers>
- Concurrency testing approaches: <https://martinfowler.com/articles/nonDeterminism.html>
