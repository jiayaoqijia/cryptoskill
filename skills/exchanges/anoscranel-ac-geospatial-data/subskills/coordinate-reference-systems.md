---
name: coordinate-reference-systems
domain: software-engineering/coordinate-reference-systems
trigger: "Understanding what a coordinate is measured against, and what mixing systems costs."
anti_trigger: "Not for index structures, and not for cartography as a craft."
scope: "Datums, projections, and the cost of mixing them."
status: seedling
---

# Coordinate reference systems

## Standard

A coordinate is a measurement against a reference system: a datum that defines the shape of the Earth it measures, a projection that flattens that shape into a plane if one is used, and an axis convention that says which number is first. The systems differ. WGS 84 — the GPS standard, the one lat/lng data is written in — is a global ellipsoid; national grids are projected planes tuned to a region; and historic datasets carry their own datums. Two numbers with no stated system are not a location; they are a puzzle with several plausible answers, some hundreds of metres apart.

Mixing systems without conversion is the classic defect. A pair of coordinates in a projected metres-grid treated as WGS 84 degrees plots somewhere in the ocean or a thousand kilometres away; subtler mixes shift results by tens of metres — enough to place a store on the wrong side of a road, or a user outside the geofence they are standing in. The discipline is to declare the reference once, convert at ingest with a stated transform, and store the declared system as data provenance.

Primary sources: <https://www.rfc-editor.org/rfc/rfc7946> and <https://postgis.net/documentation/>.

## Decision rules

- Store the reference system as a column or a declared global, never as an assumption.
- Choose one canonical system for storage — WGS 84 for global point data is the common answer — and convert everything else at ingest.
- Record the datum and ellipsoid for any legacy data whose system is not labelled; guessing shifts tens of metres.
- Projection choice is a query decision, not a storage decision: keep source data in its native system, project at query time for the computation being done.
- Never compare distances computed in mixed systems; a geodesic in WGS 84 and a Euclidean distance in a projected grid are different claims.
- Validate the ranges a system permits; latitude above 90 or a projected grid's coordinates outside its zone declare themselves as conversion defects.

## Procedure

1. Inventory the sources and the reference system each one states.
2. Declare the canonical storage system and its axis order.
3. Convert non-canonical sources at ingest with a recorded transform; label the origin system.
4. Validate ranges after conversion, and quarantine the failures rather than silently adjusting.
5. Document the system used by each downstream consumer, especially distance and area computations.
6. Record the reference systems, transforms, and their validation results in the geospatial record.

## Anti-patterns

- Storing bare numbers because they look like lat/lng and hoping.
- Distance computed from a projected grid and stated in kilometres without a scale factor.
- Treating axis order as universal; different systems disagree on whether x or latitude is first.
- A single lat/lng column silently holding two datums from two vintages of export.
- Reprojecting at storage time and losing the source, so the original system can no longer be verified.

## Done checklist

- [ ] Reference systems inventoried per source.
- [ ] Canonical system declared with axis order.
- [ ] Conversions at ingest with recorded transforms.
- [ ] Range validation quarantining anomalies.
- [ ] Consumers' computation systems documented.
- [ ] Systems and transforms in the record.

## Sources

- GeoJSON specification, WGS 84 mandate: <https://www.rfc-editor.org/rfc/rfc7946>
- PostGIS coordinate system documentation: <https://postgis.net/documentation/>
- Spatial types in a general database: <https://dev.mysql.com/doc/refman/8.0/en/spatial-types.html>
