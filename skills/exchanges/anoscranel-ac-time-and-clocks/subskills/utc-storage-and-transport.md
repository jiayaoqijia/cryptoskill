---
name: utc-storage-and-transport
domain: software-engineering/utc-storage-and-transport
trigger: "Choosing the format and zone for stored and transmitted times."
anti_trigger: "Not for presenting times to users in their locale (ac-i18n-and-localisation)."
scope: "One zone for machines, local zones only at the human edge."
status: seedling
---

# UTC storage and transport

## Standard

The rule is old because it is right: store and transmit time in one zone — UTC — and convert to local zones only at the last moment, for a human to read. Every exception is a debt: a timestamp stored in a machine's local zone becomes ambiguous when the zone changes or when the machine moves; a timestamp stored without a zone is a puzzle every later reader must solve; and daylight-saving transitions make local-zone storage genuinely wrong twice a year for the hour that repeats.

The transport format should carry its own offset so the value needs no context to interpret. A timestamp with an explicit offset — ending in Z or a numeric offset — is unambiguous; a timestamp without one is a claim about the writer's zone that the reader can only guess. The conversion to local time belongs in the presentation layer, keyed to the viewer's known zone, and nowhere else in the system.

## Decision rules

- Store timestamps in UTC; convert at the presentation edge only.
- Use a transport format that carries its timezone explicitly.
- Reject inputs that arrive without a timezone, or tag them with a documented default.
- Never store local-zone timestamps for later machine consumption.
- Beware the repeated hour at a daylight-saving fall-back: store UTC and the ambiguity vanishes.
- Audit databases and interfaces for naked timestamps with no zone information.

## Procedure

1. Define the canonical storage and transport format for the system.
2. Audit stored timestamps and interfaces for zoneless values.
3. Correct any local-zone storage to the canonical form.
4. Convert at the presentation edge only, keyed to the viewer's zone.
5. Validate inputs for explicit offsets or a documented default.
6. Record the format in the time policy and in the interface documentation.

## Anti-patterns

- Storing "the time" without a zone and hoping.
- Distributed systems where each service stores its host's local time.
- Converting to local time at every layer rather than one.
- Naive parsing of timestamps that assumes the reader's zone.
- Treating the database server's zone as the storage zone because that is where the data lives.

## Done checklist

- [ ] Canonical format defined.
- [ ] Zoneless values audited and corrected.
- [ ] Conversion confined to the presentation edge.
- [ ] Inputs validated for explicit zones.
- [ ] DST ambiguity handled by storage choice.
- [ ] Format recorded in policy and interfaces.

## Sources

- Timestamps on the internet, the standard format: <https://www.rfc-editor.org/rfc/rfc3339>
- Date and time API guidance: <https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/time/package-summary.html>
- ISO 8601 and its data elements: <https://www.iso.org/iso-8601-date-and-time-format.html>
