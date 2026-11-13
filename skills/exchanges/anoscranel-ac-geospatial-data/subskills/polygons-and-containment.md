---
name: polygons-and-containment
domain: software-engineering/polygons-and-containment
trigger: "Answering which region contains this point, correctly."
anti_trigger: "Not for distance queries, and not for map drawing."
scope: "Point-in-polygon, polygons that self-intersect, and validity."
status: seedling
---

# Polygons and containment

## Standard

A polygon is a closed ring of points, and containment — is this point inside this polygon — is the query that neighbourhood, delivery-zone, and geofence features all reduce to. The arithmetic checks how many times a ray from the point crosses the polygon's boundary: an odd count means inside. That simple rule holds only for simple polygons; the moment a ring crosses itself, or a polygon declares holes, "inside" requires a stated rule, because different libraries and different specifications answer differently for exactly those shapes.

Validity is therefore a storage decision. A polygon that self-intersects, or a ring that closes on a different point than it opened, produces geometry that some systems repair silently, some reject, and some compute nonsense on. The discipline is to validate at ingest, to repair on stated rules or reject loudly, and to store only geometry whose semantics the query layer can rely on. GeoJSON gave the interchange a validity rule for exactly this reason, and the honest pipeline references which rule it enforces.

Primary sources: <https://www.rfc-editor.org/rfc/rfc7946> and <https://postgis.net/documentation/>.

## Decision rules

- Validate polygons at ingest: ring closure, self-intersection, hole orientation — and reject or repair under a written rule, never silently.
- State and record the winding convention, because GeoJSON's is not every library's, and mixing them inverts holes into solid.
- Containment of a polygon with holes must consider holes as exclusions; a fixture with a point inside a hole proves the behaviour.
- A point exactly on the boundary is a declared case, tested deliberately; different consumers disagree, and a geofence that flips there is a support ticket.
- Multi-region containment — which of these zones — must state tie behaviour for overlapping zones exactly as k-NN states ties.
- Record the validity rules enforced, because a downstream consumer inheriting geometry deserves to know what was already checked.

## Procedure

1. Write the validity rule: closed rings, simple boundaries, hole orientation, and the repair-or-reject decision for each failure.
2. Enforce it at ingest and record the rejection or repair counts.
3. Implement or invoke the containment predicate, and fix the on-boundary policy explicitly.
4. Test with fixtures: point in hole, point on shared vertex, overlapping zones, a polygon described clockwise and its anticlockwise twin.
5. For multi-zone queries, define and test the overlap-tie rule.
6. Record the validity rule, the fixtures, and the boundary policy in the geospatial record.

## Anti-patterns

- Storing vendor-supplied polygons unvalidated, then debugging why a suburb is inside-out.
- Hole orientation flipped by an exporter, so the lake a zone excludes became the zone.
- Boundary points resolved inconsistently between the production query and the nightly job.
- Overlapping delivery zones answering differently by which was inserted first.
- Silent library "repair" of invalid geometry, so nobody knows which shape the answers describe.

## Done checklist

- [ ] Validity rule written and enforced at ingest.
- [ ] Winding convention recorded and consistent.
- [ ] Hole exclusion tested with fixtures.
- [ ] On-boundary policy fixed and tested.
- [ ] Overlap-tie rule defined for multi-zone.
- [ ] Validity rules in the record.

## Sources

- GeoJSON polygon validity: <https://www.rfc-editor.org/rfc/rfc7946>
- PostGIS geometry validation: <https://postgis.net/documentation/>
- Spatial types overview: <https://dev.mysql.com/doc/refman/8.0/en/spatial-types.html>
