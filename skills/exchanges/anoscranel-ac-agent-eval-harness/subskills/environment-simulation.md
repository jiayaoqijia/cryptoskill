---
name: environment-simulation
domain: software-engineering/environment-simulation
trigger: "Building the controlled world the harness runs in."
anti_trigger: "Not for production environments, and not for the scenario set."
scope: "Simulated worlds that stay honest about what they omit."
status: seedling
---

# Environment simulation

## Standard

The harness runs the agent inside a simulation boundary: a filesystem, a set of tool services, a clock, maybe a network. The simulation is an envelope around the agent, and its honesty requirement is explicitness — every fidelity gap between the simulation and production is stated, because it will be found by the agent eventually.

The classic fidelity gaps get named in the spec: file systems with wrong permissions or latencies; APIs with response formats captured before a breaking contract change; clocks that never cross midnight; networks that never drop. Simulated state initialises each scenario; the simulation's data set is separated from the code so scenario data can be reviewed without reading Python; and persistent environments are reset per run, because a stale state between runs is a defect that only fires on Tuesdays.

Primary sources: <https://martinfowler.com/articles/practical-test-pyramid.html> and <https://en.wikipedia.org/wiki/Software_testing>.

## Decision rules

- Enumerate what the simulation does not reproduce; write it into the spec.
- Simulation state is initialised per run; no cross-run state leakage.
- Scenario data separated from harness code so it is reviewable.
- Captured real responses refreshed on a schedule; check against real contracts.
- Faithful failure modes: the environment must simulate refusal, fault, and delay.
- A production-only behaviour, once discovered, becomes a documented gap or a new real-tool exception.

## Procedure

1. Define the boundary: filesystem, services, clock, network.
2. Initialise state from scenario data; reset per run.
3. Wire each simulated tool to replay captured real responses.
4. Script in failure modes the production source would exhibit.
5. Write the fidelity-gap list into the harness spec.
6. Schedule re-capture against current production contracts.

## Anti-patterns

- Simulations that only simulate success.
- Cross-run state carry-over that makes scenarios order-dependent.
- Scenario data buried in code.
- Fidelity gaps discovered one at a time, in production.
- The simulation's contract drift unobserved for months.

## Done checklist

- [ ] Boundary defined.
- [ ] State reset per run.
- [ ] Scenario data separated from code.
- [ ] Failure modes scripted in.
- [ ] Fidelity-gap list in the spec.
- [ ] Re-capture schedule set.

A second honesty rule applies to scale: simulation inputs sized to triple the production rate or volume will find limits the real system never asked about, while inputs sized below production hide the behaviour that appears only under load. Match the envelope to the observed production range, state the range used, and mark scenarios whose point is to exceed that range as deliberate stress rather than as representative.

## Sources

- Test pyramid and isolation discipline: <https://martinfowler.com/articles/practical-test-pyramid.html>
- Simulation practice: <https://en.wikipedia.org/wiki/Software_testing>
- Agent system evaluation contexts: <https://arxiv.org/abs/2308.03688>
