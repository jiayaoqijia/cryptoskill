---
name: properties-and-types
domain: software-engineering/properties-and-types
trigger: "Designing event properties and their types."
anti_trigger: "Not for naming events, and not for the warehouse schema downstream."
scope: "Typed properties, enums over free strings, and the fields every event carries."
status: seedling
---

# Properties and types

## Standard

The property set decides which questions are answerable later. A property is a named field on an event: plan tier, item count, share target, file size. The design rules fit in one breath: every event carries a small standard envelope (timestamp, platform, app version, the event-specific object identifier it acts on); the additional properties are declared at proposal time with their type; and free-text strings are banned for values that take a known finite set — the enum is recorded in the plan, and the analytics layer validates against it.

The free-text trap deserves its own sentence. plan_tier: "pro " (with a trailing space on one platform) is a distinct value from "pro" and no amount of downstream cleaning recovers the ones both platforms recorded two ways. Free text belongs for human-typed content (search queries, notes) and nowhere else; the property design review enforces it, along with the units: file_size_bytes means what it says because someone in the future will ask whether this was megabytes and no one will be able to answer.

Primary sources: <https://developer.mozilla.org/en-US/docs/Web/API/Beacon_API> and <https://en.wikipedia.org/wiki/Customer_data_platform>.

## Decision rules

- Standard envelope on every event: timestamp, platform, app version, and owner identifier already carried.
- Properties are declared with a type and a unit at proposal time.
- Free-text properties banned for finite sets — enum values are recorded where they can be validated.
- Names state units where a unit exists: _bytes, _ms, _count suffixes.
- Human language text carries a language tag where it can arrive in any language.
- The proposal must state the expected volume class of the property — constantly present or occasional.

## Procedure

1. Define the once-settled standard envelope.
2. For each proposed event: declare its additional properties with type and unit.
3. Enforce the enum rule at proposal review.
4. Add localization tags to human-text properties.
5. Add the property design to the taxonomy's schema version.
6. Run periodic type audits: value scans for string where an enum was declared.

## Anti-patterns

- Free-text finite sets: "pro " trailing-space pollution.
- Proposing event properties without limits — no proposal should exist without its property design.
- Unknown-unit properties pushed through: size without _bytes.
- Properties that silently change case across platforms: ItemCount vs item_count.
- Settling for boolean where the finite enum has more than two members.

## Done checklist

- [ ] Envelope defined and stable.
- [ ] Property declared with type and unit at proposal time.
- [ ] Free-text banned except human text.
- [ ] Language tags on human-text properties.
- [ ] Volume class recorded for each property.
- [ ] Type audit completed after the first quarter.

## Sources

- Client-side event delivery: <https://developer.mozilla.org/en-US/docs/Web/API/Beacon_API>
- Wider background on the data aggregation layer: <https://en.wikipedia.org/wiki/Customer_data_platform>
- Time and formatting know-how every property design leans on: <https://cldr.unicode.org/>
