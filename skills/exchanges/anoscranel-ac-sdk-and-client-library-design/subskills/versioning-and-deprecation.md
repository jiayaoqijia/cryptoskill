---
name: versioning-and-deprecation
domain: software-engineering/versioning-and-deprecation
trigger: "Versioning a published library and retiring a method."
anti_trigger: "Not for API endpoint versioning, and not for release automation."
scope: "Semantic versioning, and retiring a published method."
status: seedling
---

# Versioning and deprecation

## Standard

Semantic versioning is a commitment about what a number means: a patch release fixes without changing behaviour, a minor release adds without breaking, and a major release may break. The commitment is only useful if the library's authors agree on what "breaking" means for their language — adding a method to an interface can break every implementer, and adding a field to a struct can break exhaustive matching.

Deprecation is the mechanism that makes a major release survivable. A method marked deprecated, documented with its replacement, and kept working for a stated period gives callers a migration path that does not require reading a changelog at upgrade time. Deprecating in one release and removing in the next is a removal disguised as a deprecation, and it is why callers stop upgrading.

Primary sources: <https://semver.org/> and <https://www.rfc-editor.org/rfc/rfc9110>.

## Decision rules

- Record what the library treats as breaking, including the language-specific cases.
- Record the deprecation period and the release in which removal is planned.
- Record how a deprecation is signalled: annotation, warning, documentation, or all three.
- Record the migration documentation for each breaking change.
- Record whether pre-release versions are used and what they signal.
- Record the support window for older major versions, since callers on the previous major need a date.

## Procedure

1. Record the breaking-change definition for this library.
2. Record the deprecation signalling and period.
3. Record removal scheduling.
4. Record migration documentation per break.
5. Record pre-release conventions.
6. Write the versioning policy.

## Anti-patterns

- Adding an abstract method in a minor release and calling it additive.
- Deprecating and removing in consecutive releases.
- A deprecation warning with no replacement documented.
- A major version bump with no migration guide.
- Supporting an old major indefinitely, which makes the new one harder to change.

## Done checklist

- [ ] Breaking definition recorded.
- [ ] Deprecation period recorded.
- [ ] Signalling recorded.
- [ ] Migration documentation recorded.
- [ ] Pre-release convention recorded.
- [ ] Support window recorded.

The support window is the commitment most often left implicit, and it is the one callers need for planning: a library that supports only the latest major forces upgrades on the maintainer's schedule, while one that supports three gives callers a year, and stating the number converts an expectation into a policy.


## Sources

- Semantic versioning specification: <https://semver.org/>
- Interface evolution context: <https://www.w3.org/>
- Release practice: <https://www.rfc-editor.org/rfc/rfc9110>
