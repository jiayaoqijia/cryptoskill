---
name: event-schema-evolution
domain: software-engineering/event-schema-evolution
trigger: "Changing an event schema that existing consumers read."
anti_trigger: "Not for REST or GraphQL contract design, and not for database migrations."
scope: "Compatibility across producers and consumers that deploy separately."
status: seedling
---

# Event schema evolution

## Standard

Producers and consumers of an event deploy independently, so a schema change reaches consumers after the producer has already changed. Compatibility is therefore a contract about what a consumer can safely ignore: adding an optional field is backward compatible, removing one is not, and changing a field's meaning is worse than either because it breaks nothing mechanically while breaking everything semantically.

The registry exists to make that contract enforceable. It validates a new schema against the previous version and rejects an incompatible change at publication, which moves the failure from a consumer at three in the morning to the producer's build. The record should state the compatibility mode in force and the process for the changes it does not permit.

Primary sources: <https://www.cncf.io/> and <https://martinfowler.com/>.

## Decision rules

- Record the compatibility mode in force: backward, forward, full, or none.
- Record which changes are permitted under that mode and which require a new event type.
- Record the registry and the version identification, since a consumer needs to know what it is reading.
- Record the deprecation process for a field, including its timeline and observability.
- Record how a consumer behaves on an unknown field, since that decides whether additions are safe.
- Record the semantic changes that no registry can catch and the review that covers them.

## Procedure

1. Record the compatibility mode and its implications.
2. Record the permitted change classes under that mode.
3. Record version identification in the payload or the envelope.
4. Record the deprecation process and its monitoring.
5. Record consumer tolerance for unknown fields.
6. Record the review that catches semantic changes.

## Anti-patterns

- Changing a field's meaning and relying on the registry to approve it.
- Removing a field because a search suggests nothing reads it.
- A consumer that throws on an unknown field.
- Deprecating without observing whether the old field is still read.
- Versioning by mutating the event name in place.

## Done checklist

- [ ] Compatibility mode recorded.
- [ ] Permitted changes recorded.
- [ ] Version identification recorded.
- [ ] Deprecation process recorded.
- [ ] Consumer tolerance recorded.
- [ ] Semantic review recorded.

The deprecation process is where most of the discipline lives: a field marked deprecated and never observed is a field that either lingers forever or is removed while a consumer still reads it, and neither outcome is a decision. Instrumenting reads per field before removal is the step that converts a guess into a measurement.


## Sources

- Event streaming and schema guidance: <https://www.cncf.io/>
- Distributed systems practice: <https://martinfowler.com/>
- Integration pattern reference: <https://www.enterpriseintegrationpatterns.com/>
