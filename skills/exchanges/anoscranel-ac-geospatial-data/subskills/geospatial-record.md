---
name: geospatial-record
domain: software-engineering/geospatial-record
trigger: "Writing the record of a location system's reference systems and indexes."
anti_trigger: "Not for the map product, and not for the visual layer."
scope: "The written record: reference systems, indexes, and their measured behaviour."
status: seedling
---

# Geospatial record

## Standard

The geospatial record states what a location system measures against and how it queries: the canonical coordinate reference system and the transforms applied at ingest, the spatial index structures and their parameters, the precision rung chosen for distance, the validity rules polygons passed before storage, and the measured behaviour of representative queries on the real data distribution. Each entry carries its date, because reference systems do not drift but datasets do, and an index measured on last year's shape behaves differently on this year's.

Its working value is the debug that has not happened yet. A location bug arrives as a map that looks wrong, and the record converts the visual complaint into a bounded question: which coordinate system did this source declare, which transform ran, which precision rung computed this distance, which validity rule passed this polygon. Without the record, the answer is re-derived from folklore; with it, the question is which recorded decision the data disagrees with.

Primary sources: <https://www.rfc-editor.org/rfc/rfc7946> and <https://postgis.net/documentation/>.

## Decision rules

- Record the canonical reference system, the source systems, and the transform applied to each.
- Record the index structure, its parameters, and the distribution statistics it was measured on.
- Record the precision rung for each distance use case and why that rung was chosen.
- Record the polygon validity rules enforced at ingest, and the repair-or-reject counts each release.
- Record measured query behaviour — the dense-sample and sparse-sample numbers — with the dataset shape and date.
- Any change to reference system, index, or precision is a dated entry; a silent change is a defect.

## Procedure

1. Assemble the reference-system section: the canonical, the sources, the transforms.
2. Assemble the index section: the structures, the parameters, the distribution they were measured on.
3. Assemble the precision section: the rung per use case with the rationale.
4. Assemble the validity section: the rules and their enforcement behaviour at ingest.
5. Attach the measured numbers — the dense/sparse latency pair, the over-selection ratio — with dates.
6. Read the record first when a spatial complaint arrives, before looking at the map.

## Anti-patterns

- A reference system known only to the code that performed the conversion.
- Latency numbers recorded without the dataset shape, so the numbers mean nothing later.
- Validity rules remembered as what the library did when it was installed.
- Two distance computations in the codebase at different rungs, with no statement of which uses which.
- An ingest transform changed during a migration, recorded nowhere, converting history differently.

## Done checklist

- [ ] Reference systems and transforms recorded.
- [ ] Index structures with parameters and distributions.
- [ ] Precision rung per use case with rationale.
- [ ] Validity rules and enforcement counts.
- [ ] Measured dense/sparse numbers with dates.
- [ ] Record read first on every spatial complaint.

## Sources

- GeoJSON and its WGS 84 mandate: <https://www.rfc-editor.org/rfc/rfc7946>
- PostGIS documentation: <https://postgis.net/documentation/>
- Spatial database structures: <https://en.wikipedia.org/wiki/Spatial_database>
