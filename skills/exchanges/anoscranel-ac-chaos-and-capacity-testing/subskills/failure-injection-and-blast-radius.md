---
name: failure-injection-and-blast-radius
domain: software-engineering/failure-injection-and-blast-radius
trigger: "Injecting a fault with a bounded and stoppable effect."
anti_trigger: "Not for security testing, and not for unplanned production experiments."
scope: "Injecting a fault with a stop button and a stated limit."
status: seedling
---

# Failure injection and blast radius

## Standard

A failure injection is only acceptable when its worst case is known before it runs. That means a stated blast radius — which instances, which users, which percentage of traffic — an abort condition that ends the experiment automatically, and a person with the authority to stop it. Without those three, the experiment is not a controlled test but an incident with a hypothesis attached.

The injection method determines what can be learned. Killing a process tests restart behaviour; adding latency to a dependency tests timeout and retry behaviour; blocking a network path tests partition handling. Each reveals a different thing, and choosing the method that is easiest to inject rather than the one that matches the hypothesis produces a result that answers a question nobody asked.

Primary sources: <https://principlesofchaos.org/> and <https://sre.google/>.

## Decision rules

- Record the hypothesis: the expected behaviour, stated before the injection.
- Record the blast radius: the targets, the percentage, and the user segment affected.
- Record the abort condition and who can trigger it.
- Record the injection method and the specific failure it produces.
- Record the observability in place before the experiment, since an unobserved experiment proves nothing.
- Record the rollback or recovery step and its expected duration.

## Procedure

1. State the hypothesis and the expected observable behaviour.
2. Define the blast radius and how it is enforced technically.
3. Define the abort condition and the authority to stop.
4. Verify the observability before injecting.
5. Inject and record the timeline.
6. Stop, verify recovery, and record the finding.

## Anti-patterns

- Injecting without a stated hypothesis.
- A blast radius defined in a document rather than enforced by configuration.
- Experimenting without the dashboards that would show the effect.
- Leaving the injection running after the finding is clear.
- Recovering without verifying that the system returned to baseline.

## Done checklist

- [ ] Hypothesis recorded before injection.
- [ ] Blast radius defined and enforced.
- [ ] Abort condition and authority recorded.
- [ ] Injection method recorded.
- [ ] Observability verified beforehand.
- [ ] Recovery verified against baseline.

The observability prerequisite deserves to be a hard gate rather than a recommendation: an experiment without the dashboards that would show its effect cannot distinguish a system that handled the fault from one that did not notice it, and the second outcome will be recorded as success.


## Sources

- Principles of chaos engineering: <https://principlesofchaos.org/>
- Site reliability engineering guidance: <https://sre.google/>
- Cloud native resilience practice: <https://www.cncf.io/>
