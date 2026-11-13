---
name: ac-time-and-clocks
description: "Handling time correctly in software: monotonic versus wall clocks and what each is for, clock skew between machines, NTP and how clocks actually stay honest, UTC as a transport format and its local-presentation exceptions, the timezone database as a changing dependency, leap seconds and discontinuities, and the written time-policy record. It explains how software should treat time; it never recommends an NTP product and never converts times by guesswork. Use when asking \"monotonic clock\", \"wall clock\", \"clock skew\", \"NTP\", \"UTC everywhere\", \"timezone database\", \"tzdata\", \"leap second\", \"why do my timestamps disagree\", \"time went backwards\", \"timer drift\", \"midnight boundary\". Not for locale formatting of dates for users (ac-i18n-and-localisation), not for stream event-time semantics (ac-stream-processing), not for scheduled job semantics (ac-scheduled-jobs)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Time and clocks

## Overview

Software time is two different things wearing one word. The wall clock reads calendar time and can be corrected backwards by synchronisation; the monotonic clock only advances and exists to measure durations. Systems fail when the two are swapped: durations computed from wall-clock reads can come out negative after a correction, and timestamps stored in a machine's local zone become uninterpretable once it moves.

This skill covers the rules that keep each use correct: which clock for which purpose, how much skew to expect between machines and how to reason across it, UTC as the storage and transport format, the timezone database as an actively changing dependency that must be updated, and the rare discontinuities — leap seconds and zone redefinitions — that break systems that assumed time was smooth. Formatting time for a human reader belongs to the localisation skill; receiving and ordering events in streams to the stream skill.

Primary sources: <https://www.rfc-editor.org/rfc/rfc3339> and <https://www.rfc-editor.org/rfc/rfc5905>.

## When to use

- Choosing which clock to read for a measurement or a timestamp.
- Storing or exchanging times between processes and machines.
- Reasoning about events whose timestamps came from different hosts.
- Handling timezone database updates and time discontinuities.

## When NOT to use

- For presenting dates in a user's locale (use ac-i18n-and-localisation).
- For event-time windows and watermarks (use ac-stream-processing).
- For when a job should run (use ac-scheduled-jobs).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/monotonic-versus-wall.md` | `software-engineering/monotonic-versus-wall` | The two clocks, their guarantees, and the failure of using the wrong one. |
| `subskills/clock-skew.md` | `software-engineering/clock-skew` | How far machines disagree, and reasoning safely across their timestamps. |
| `subskills/ntp-and-synchronisation.md` | `software-engineering/ntp-and-synchronisation` | What NTP does and does not fix, and its own failure modes. |
| `subskills/utc-storage-and-transport.md` | `software-engineering/utc-storage-and-transport` | One zone for machines, local zones only at the human edge. |
| `subskills/timezone-database.md` | `software-engineering/timezone-database` | The rules change, and the binary carries them. |
| `subskills/discontinuities.md` | `software-engineering/discontinuities` | Leap seconds, zone redefinitions, and their absorbable risk. |
| `subskills/time-policy-record.md` | `software-engineering/time-policy-record` | The written record: clock choices, formats, zones, and update ownership. |

## Status and honest limits

Clock behaviour is a property of the runtime, the operating system, and the synchronisation setup, and all three vary: some monotonic clocks pause during suspend, some wall clocks step rather than slew, and zone rules change by government decision with little notice. The rules here are the discipline, but the deployed runtime's own documentation is the authority on its clock guarantees. Nothing recommends a specific time source, and any cross-machine ordering more precise than the measured skew is a claim the clocks cannot support.
