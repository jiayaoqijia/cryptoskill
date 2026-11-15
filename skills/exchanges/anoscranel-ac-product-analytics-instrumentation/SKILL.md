---
name: ac-product-analytics-instrumentation
description: 'Instrumenting product analytics so the data can answer questions later: the event taxonomy as its schema, naming events around the user-visible action, property design with types and enums, the identity stitching that connects anonymous to logged-in, the client-side delivery mechanics including beacons, batching, and lifecycle loss, the event plan and its governance, and the written event-record. It designs the tracking layer; it never recommends an analytics vendor and never reads the data to draw conclusions. Use when asking "event taxonomy", "event naming convention", "analytics event schema", "track event design", "property naming", "user vs account analytics", "anonymous to logged-in identity", "analytics instrumentation", "event tracking plan". Not for the experiment and its statistics (ac-online-experiments), not for the warehouse schema the events land in (ac-analytical-data-modeling), not for the privacy obligations the events create (ac-privacy-engineering).'
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Product analytics instrumentation

## Overview

Analytics fails silently. A mis-named event, a property recorded as a string that should be an enum, an inconsistency between platforms — none of these break anything at the moment of collection, and every one of them breaks a query months later when someone asks the question the data was collected to answer. The craft is designing the tracking layer so that questions not yet asked remain answerable.

This skill covers that design: the taxonomy as a schema with governance, events named for user-visible actions rather than implementation, properties typed and enumerated, identity stitched so the same human is countable across devices, the client-side delivery realities — beacons, batching, lifecycle dropout — accounted for in expectations, and the plan that keeps the taxonomy from rotting. The experiment that uses the events belongs to another skill; so does the warehouse schema and the privacy review.

Primary sources: <https://en.wikipedia.org/wiki/Clickstream> and <https://developer.mozilla.org/en-US/docs/Web/API/Beacon_API>.

## When to use

- When defining the event taxonomy or naming conventions.
- When designing properties, traits, and their types.
- When connecting anonymous to logged-in identity across devices.
- When client-side delivery loss must be accounted for before trusting counts.
- When the event plan needs drafting or a governance pass.

## When NOT to use

- For experiments and their statistics (use ac-online-experiments).
- For the warehouse schema the events land in (use ac-analytical-data-modeling).
- For privacy obligations the events create (use ac-privacy-engineering).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/the-event-taxonomy.md` | `software-engineering/the-event-taxonomy` | The schema that naming conventions enforce and governance maintains. |
| `subskills/event-naming-and-actions.md` | `software-engineering/event-naming-and-actions` | Naming events after user-visible actions, not implementation. |
| `subskills/properties-and-types.md` | `software-engineering/properties-and-types` | Typed properties, enums over free strings, and the fields every event carries. |
| `subskills/identity-stitching.md` | `software-engineering/identity-stitching` | Anonymous-to-logged-in, device graphs, and the counts that depend on them. |
| `subskills/client-delivery-realities.md` | `software-engineering/client-delivery-realities` | Beacons, batching, lifecycle loss, and the gap between fires and arrives. |
| `subskills/the-event-plan.md` | `software-engineering/the-event-plan` | The living document that maps every event and its owner. |
| `subskills/event-record.md` | `software-engineering/event-record` | The written record: taxonomy version, known gaps, taxonomy-change log. |

## Status and honest limits

Counts are estimates. Client-side delivery drops events — ad blockers, tab closure, network loss, page transitions — so any number read from the stream is a floor, not a truth. Nothing here recommends a vendor, and no taxonomy survives contact with a fourth team adding events without review: the governance section exists because the alternative is archaeology.
