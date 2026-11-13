---
name: discontinuities
domain: software-engineering/discontinuities
trigger: "Handling leap seconds, zone redefinitions, and other breaks in smooth time."
anti_trigger: "Not for the zone database update process (that is timezone-database)."
scope: "Leap seconds, zone redefinitions, and their absorbable risk."
status: seedling
---

# Discontinuities

## Standard

Most of the time, time is smooth: one second follows the last. Occasionally it is not. A leap second inserts an extra second into a day; a zone redefinition changes the offset for a stretch of time; a daylight-saving transition repeats or skips an hour of local time. Software that computes differences across these boundaries can produce results that are off by exactly the discontinuity — an hour, or a second — and nothing else looks wrong.

The engineering response is proportionate: for most systems, store in UTC and let the presentation layer carry the zone, and the daylight-saving case dissolves; for the leap second, accept the smear or the small anomaly once every few years unless the system's domain — astronomy, finance timestamps — makes the exact instant matter. The danger is not the events themselves, which are announced, but code that silently assumes a fixed offset between two zones or a fixed number of seconds in a minute.

## Decision rules

- Identify whether any code computes durations across a local clock discontinuity.
- For such code, compute in UTC and convert at the edge instead.
- For zone pairs with a changing offset, never store a fixed difference as data.
- Decide the leap-second posture — smear, step, or exact — and record it once.
- Treat "seconds in a day" and "hours in a day" as unknowns in correctness-sensitive code.
- Test critical paths against a known transition: create zones and times around one.

## Procedure

1. Inventory computations that subtract or compare times across zones.
2. Move any of them to UTC-based computation with edge conversion.
3. Check that zone differences are derived, not hard-coded constants.
4. Record the leap-second posture and its justification.
5. Write one test around a real daylight transition for the presentation path.
6. Record both decisions in the time policy.

## Anti-patterns

- A hard-coded offset between two zones in production data.
- Local-zone subtraction across a daylight transition.
- Assuming every minute has sixty seconds in timing-critical code.
- Rediscovering the leap second as an outage every time it occurs.
- Testing the happy path only, where all days have twenty-four hours.

## Done checklist

- [ ] Cross-zone computations inventoried.
- [ ] UTC-based computation replaces local subtraction.
- [ ] No fixed zone offsets stored as data.
- [ ] Leap-second posture decided and recorded.
- [ ] A transition test exists for the presentation path.
- [ ] Policy updated with both decisions.

## Sources

- Leap seconds and their application: <https://www.iana.org/time-zones/>
- UTC and time scales: <https://www.nist.gov/pml/time-and-frequency-division/>
- POSIX time and leap seconds: <https://pubs.opengroup.org/onlinepubs/9699919799/>
