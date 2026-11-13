---
name: timezone-database
domain: software-engineering/timezone-database
trigger: "Treating the timezone database as a changing dependency."
anti_trigger: "Not for locale formatting of the presented time (ac-i18n-and-localisation)."
scope: "The rules change, and the binary carries them."
status: seedling
---

# The timezone database

## Standard

The mapping between a zone's name and its offsets is not mathematics — it is a dataset of political decisions, and it changes. Governments move their daylight-saving dates, occasionally abolish them, and sometimes redefine a zone's base offset with weeks of notice. Software that converts using its own compiled copy of the rules will diverge from software with a newer copy, and a meeting scheduled through the old rules happens at the wrong time.

The consequence for engineering is that the zone database is a real dependency with a release process: it must be updated on hosts, in container images, and in runtime libraries, and the update has to be treated as a change worth testing. A system that schedules future events using zone rules must also record which rules it used, because a future event scheduled under old rules and recalculated under new ones silently moves.

## Decision rules

- Track the zone database as a dependency in the inventory, with its version.
- Update it on hosts and in images on a regular cadence, not on incident.
- Record which zone-rule version was used when future events are scheduled.
- Prefer zone names over fixed offsets in data, so rule updates apply.
- Check application runtimes that bundle their own copy — the host update does not reach them.
- After a rule change for a relevant zone, verify scheduled future times still land as intended.

## Procedure

1. Inventory where the zone database lives: hosts, images, bundled runtimes.
2. Record current versions of each.
3. Establish the update cadence and the owner.
4. For future-event scheduling, record the rule version at schedule time.
5. On a rule change for a relevant zone, re-verify affected future events.
6. Note the dependency in the time policy record.

## Anti-patterns

- Assuming the operating system's update reaches a runtime that bundles its own copy.
- Storing future times as fixed offsets, freezing old rules in place.
- No version tracking, so "is this host on new rules?" is unanswerable.
- Learning about a rule change from users arriving at the wrong hour.
- Container images never rebuilt after a database release.

## Done checklist

- [ ] Database copies inventoried with versions.
- [ ] Update cadence and owner set.
- [ ] Rule version recorded at future-event scheduling.
- [ ] Zone names used over fixed offsets in data.
- [ ] Bundled runtimes checked separately.
- [ ] Post-update verification for affected zones.

## Sources

- IANA time zone database, the source of rules: <https://www.iana.org/time-zones>
- Time zone database distribution and format: <https://data.iana.org/time-zones/tzdb/>
- CLDR time-related data: <https://cldr.unicode.org/>
