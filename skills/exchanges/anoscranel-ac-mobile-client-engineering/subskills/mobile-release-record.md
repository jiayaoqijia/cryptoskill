---
name: mobile-release-record
domain: software-engineering/mobile-release-record
trigger: "Writing the record of a mobile release and the versions in the field."
anti_trigger: "Not for store submission procedure, and not for API versioning."
scope: "The written record: versions in the field, rollout state, and upgrade policy."
status: seedling
---

# Mobile release record

## Standard

The mobile release record states which builds are in the field, what percentage of the base has each, what the rollout state is, and what the current minimum supported version is. It exists because a mobile base is a population you cannot query directly, and the version distribution is the fact that decides every compatibility question.

Its second function is to hold the upgrade policy. A minimum version that was raised six months ago and never revisited is an assumption about a tail that has probably shrunk, and a record that carries the measurement dates allows the policy to be re-decided on evidence rather than on the memory of why it was set.

Primary sources: <https://developer.android.com/> and <https://osf.io/prereg/>.

## Decision rules

- The record lists each build in the field with its version and its share of the base.
- The rollout state of the current release is recorded with its percentage and halt threshold.
- The minimum supported version is recorded with the measurement that justified it.
- The forced-upgrade mechanism and its wording are recorded.
- The known version-specific defects are recorded with their affected versions.
- Review triggers are dated: each release, each minimum-version decision, each measured distribution shift.

## Procedure

1. Record the builds in the field and their shares.
2. Record the current rollout state and halt threshold.
3. Record the minimum supported version and its justification.
4. Record the upgrade mechanism and wording.
5. Record version-specific defects and their scope.
6. Review at each release and re-record the distribution.

## Anti-patterns

- Recording the release without the distribution.
- Setting a minimum version and never re-measuring the tail.
- Omitting the halt threshold, so the rollout decision is improvised.
- Recording a defect without the versions it affects.
- Treating the store's reported numbers as the whole base.

## Done checklist

- [ ] Builds and shares recorded.
- [ ] Rollout state and halt threshold recorded.
- [ ] Minimum version and justification recorded.
- [ ] Upgrade mechanism recorded.
- [ ] Version-specific defects recorded.
- [ ] Triggers dated.

The record is also where the compatibility obligation becomes visible: listing every build in the field with its share makes it obvious that an API change affects a stated percentage of users rather than an abstraction called old clients, and that number is what turns a versioning debate into a decision.


## Sources

- Android release and distribution tooling: <https://developer.android.com/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Apple release guidance: <https://developer.apple.com/>
