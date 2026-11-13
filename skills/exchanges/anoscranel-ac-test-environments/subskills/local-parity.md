---
name: local-parity
domain: software-engineering/local-parity
trigger: "Making a developer machine and a CI runner agree."
anti_trigger: "Not for CI pipeline design, and not for test design."
scope: "Making the developer machine and CI agree."
status: seedling
---

# Local parity

## Standard

The classic failure has a name because it happens everywhere: passes on the laptop, fails in CI, and the difference hides in one of a few places — a service the laptop has running that the runner does not, a data directory the laptop accumulated, a locale or a timezone the laptop never questioned, a resource file resolved by absolute path. Each is an undeclared dependency, and parity comes from declaring it: the environment is defined once, provisioned the same way everywhere, and anything outside the definition is treated as a defect in the definition.

Full parity is an asymptote, and chasing it exactly is a trap. The workable target is declared parity: same provisioning script, same pinned dependencies, same seeded data, and a documented list of known differences with their justification. The laptop keeps its editor and its warm caches; the tests get the same world everywhere, and where they cannot, the difference is written down instead of discovered at merge.

Primary source: <https://martinfowler.com/>.

## Decision rules

- Provision test environments from one definition, used by both local and CI.
- Pin versions — runtime, dependencies, services — in that definition, not per machine.
- Record the known-difference list with a justification for each entry.
- Treat every works-locally-fails-in-CI incident as a probe for an undeclared dependency.
- Reset local environments from the definition periodically, or drift hides in them.
- Keep secrets and credentials out of the definition; inject them at run time per environment.

## Procedure

1. Write the environment definition once and provision both targets from it.
2. Diff the two provisioned environments for undeclared differences.
3. Record each accepted difference with its reason.
4. Reset the local environment from the definition and re-run the suite.
5. On each parity incident, add the missing declaration and its test.
6. Keep the definition versioned beside the code it serves.

## Anti-patterns

- A definition for CI and a habit for the laptop.
- Fixing CI failures by patching the runner, widening the gap.
- Undocumented differences remembered by the two people who know them.
- Local state — databases, files, services — treated as part of the environment.
- Secrets baked into a provisioned image.

## Done checklist

- [ ] Single definition provisioning both targets.
- [ ] Environment diff run and explained.
- [ ] Known-difference list recorded.
- [ ] Local reset performed from the definition.
- [ ] Parity incidents converted to declarations.
- [ ] Definition versioned.

## Sources

- Test environment reproducibility: <https://martinfowler.com/articles/continuousIntegration.html>
- Reproducible builds and environments: <https://reproducible-builds.org/>
- Container-based parity practice: <https://docs.docker.com/>
