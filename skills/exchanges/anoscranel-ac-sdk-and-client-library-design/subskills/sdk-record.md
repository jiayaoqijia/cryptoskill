---
name: sdk-record
domain: software-engineering/sdk-record
trigger: "Writing the record of a client library's contract with its users."
anti_trigger: "Not for generated API reference, and not for release notes."
scope: "The written record: surface, defaults, versioning, and deprecation policy."
status: seedling
---

# SDK record

## Standard

The SDK record states the public surface and what is deliberately internal, the defaults a caller inherits, the error hierarchy, the configuration and credential handling, and the versioning and deprecation policy. Those five items are the library's contract with the people who depend on it, and none of them is discoverable from generated documentation, which describes what exists rather than what is promised.

Its second function is to make a release reviewable. A change that adds a public name, alters a default, or removes a deprecated method is visible against this record, and the reviewer can ask whether the version number matches the change rather than reconstructing the intent from a diff.

Primary sources: <https://semver.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record lists the public types and marks which are stable.
- Inherited defaults are recorded with their rationale and their override mechanism.
- The error hierarchy is recorded with retryability per type.
- Configuration precedence and credential handling are recorded.
- The versioning policy records the breaking-change definition and the deprecation period.
- Review triggers are dated: new public name, default change, dependency addition, deprecation removal.

## Procedure

1. Record the public surface and stability markers.
2. Record the defaults and overrides.
3. Record the error hierarchy.
4. Record configuration and credentials.
5. Record the versioning and deprecation policy.
6. Set review triggers and amend at each.

## Anti-patterns

- A record that duplicates the generated reference.
- Defaults undocumented, so callers cannot reason about latency.
- A versioning policy that exists only in the authors' habits.
- No trigger for a default change, which is a silent behaviour change.
- Stability markers applied to everything, which marks nothing.

## Done checklist

- [ ] Public surface and stability recorded.
- [ ] Defaults and overrides recorded.
- [ ] Error hierarchy recorded.
- [ ] Configuration and credentials recorded.
- [ ] Versioning policy recorded.
- [ ] Triggers dated.

The record should also state the smallest supported version of each runtime, since a library's compatibility floor is a promise to callers on older platforms and one that is easy to raise accidentally by adopting a newer language feature in an unrelated change.


The record should also name the telemetry the library emits, since a client that phones home with usage data is a decision the caller inherits: what is collected, whether it can be disabled, and where it is documented are part of the contract rather than an implementation detail.

## Sources

- Semantic versioning: <https://semver.org/>
- Pre-registration practice for stated policies: <https://osf.io/prereg/>
- Client library behaviour: <https://www.rfc-editor.org/rfc/rfc9110>
