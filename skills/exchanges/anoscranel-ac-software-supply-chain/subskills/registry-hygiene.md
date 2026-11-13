---
name: registry-hygiene
domain: software-engineering/registry-hygiene
trigger: "Controlling which registries and namespaces the build trusts."
anti_trigger: "Not for registry product selection, and not for network egress rules."
scope: "Scopes, mirrors, and the namespace attacks."
status: seedling
---

# Registry hygiene

## Standard

A package name resolves against a namespace, and the namespace decides who controls the name. In most ecosystems, the public namespace is first-come-first-served: anyone can publish a package whose name is close to a popular one, or exactly matches a name that an internal mirror resolves differently. Dependency confusion is that second case — a build resolves an internal name against the public registry, and an attacker has published the same name there, with the attacker's code.

The defence is scope discipline. Internal packages resolve only against an internal registry or a configured scope; public packages resolve against the public one; and the resolution order is recorded so the ambiguity cannot be introduced by a rushed configuration change. A mirror adds availability and a point of control — a mirror's contents can be audited and frozen — but also a second thing to keep in sync, so the mirror's own staleness becomes a recorded property.

Primary source: <https://slsa.dev/>.

## Decision rules

- Record the resolution order: internal registry, mirror, public, and which scopes each serves.
- Give internal package names a scope or prefix that the public registry cannot resolve.
- Fail resolution that crosses a boundary: an internal name resolving publicly is a defect, not a fallback.
- Record the mirror's sync cadence and the staleness window accepted.
- Audit new direct dependencies for name proximity to established packages.
- Record who can publish to each registry and scope, and how a publisher is verified.

## Procedure

1. Document the resolution order and the scope assignment per registry.
2. Verify internal names cannot resolve against the public namespace.
3. Test the boundary: attempt to resolve an internal name publicly and confirm refusal.
4. Record mirror sync cadence and measured staleness.
5. Audit new dependency names for typosquatting proximity.
6. Record publisher identity and verification per registry.

## Anti-patterns

- Fallback to public resolution for an internal name.
- Package names chosen without checking the public namespace.
- A mirror trusted for availability but never measured for staleness.
- Scope configuration changed to fix one build, silently changing resolution for all.
- Publish credentials shared rather than bound to verified identities.

## Done checklist

- [ ] Resolution order and scopes documented.
- [ ] Internal-name public resolution tested and refused.
- [ ] Mirror staleness measured and recorded.
- [ ] Name-proximity audit in the intake checklist.
- [ ] Publisher verification recorded.
- [ ] Boundary test automated.

## Sources

- Supply-chain integrity: <https://slsa.dev/>
- Reproducible dependency resolution: <https://reproducible-builds.org/>
- Package manager scope configuration: <https://nodejs.org/en/learn/getting-started/an-introduction-to-the-npm-package-manager>
