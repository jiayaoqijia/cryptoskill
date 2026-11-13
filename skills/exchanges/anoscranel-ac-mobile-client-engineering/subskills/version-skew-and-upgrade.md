---
name: version-skew-and-upgrade
domain: software-engineering/version-skew-and-upgrade
trigger: "Deciding how many client versions to support and when to force an upgrade."
anti_trigger: "Not for API versioning, and not for store policy."
scope: "Supporting several client versions, and the forced-upgrade decision."
status: seedling
---

# Version skew and upgrade

## Standard

An installed base is never on one version. Users defer updates, devices stop receiving them, and a long tail of old clients keeps calling your API years after you stopped thinking about them. That tail is a compatibility obligation: every breaking change must either be served to old clients in their own shape or be gated by a minimum-version check.

The forced upgrade is the escape hatch and it has a real cost. Blocking old clients removes the maintenance burden and removes the users who cannot or will not update, and the decision should be tied to a measured threshold — a percentage of traffic, a security exposure, or a dependency that cannot be supported — rather than to the team's preference for a clean codebase.

Primary sources: <https://developer.android.com/> and <https://developer.apple.com/>.

## Decision rules

- Record the current version distribution by share of active users and share of requests.
- Record the minimum supported version and the date it was raised.
- Record which API behaviours differ by client version, and how they are gated.
- Record the forced-upgrade mechanism: hard block, soft prompt, or feature gate.
- Record the measured justification for raising the minimum.
- Record the migration path offered to users on the deprecated version.

## Procedure

1. Measure the version distribution and record it with a date.
2. List the behaviours that differ across versions.
3. Choose the gating mechanism for each behaviour.
4. Set the minimum supported version and record the justification.
5. Implement the upgrade prompt or block and record its wording.
6. Re-measure after each release and record the tail's movement.

## Anti-patterns

- Raising the minimum version because the code is inconvenient to maintain.
- Hard-blocking without a migration path.
- Assuming a prompt will be acted on without measuring.
- Gating behaviour on a version number when a capability check would do.
- Never measuring the tail, so the distribution is guessed.

## Done checklist

- [ ] Version distribution measured with a date.
- [ ] Minimum supported version recorded with justification.
- [ ] Behaviour differences and gates recorded.
- [ ] Upgrade mechanism recorded.
- [ ] Migration path recorded.
- [ ] Re-measurement scheduled.

The distribution should be measured by requests as well as by users, because the two can differ sharply: a small share of users on an old build can generate a large share of traffic if they are the ones with the most sessions or the most background syncing, and the maintenance cost follows the traffic rather than the headcount.


## Sources

- Android version and API level guidance: <https://developer.android.com/>
- Apple deployment target guidance: <https://developer.apple.com/>
- Semantic versioning reference: <https://semver.org/>
