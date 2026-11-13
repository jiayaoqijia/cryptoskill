---
name: distance-and-proximity
domain: software-engineering/distance-and-proximity
trigger: "Computing distance and radius honestly over a sphere."
anti_trigger: "Not for index structures, and not for polygon containment."
scope: "Great-circle distance, projections, and radius queries."
status: seedling
---

# Distance and proximity

## Standard

The distance between two points on the Earth is an arc across its ellipsoid, and computing it has a correctness ladder. Euclidean distance on raw degrees is wrong always — one degree of longitude shrinks with the cosine of latitude, and treating them as equal squares distorts distance by geography. Great-circle distance on a sphere — the haversine formula — is right to about half a percent, which is plenty for search results and geofences of ordinary precision. Geodesic distance on the ellipsoid is exacting and slower; the honest design picks the rung the use case needs rather than paying for ellipsoids a match-radius never asked for.

Radius queries follow the two-step shape: a bounding-box filter expanded by the radius, then an exact distance refinement on the candidates. The expansion of metres into degrees differs by latitude, and near the poles it stops behaving at all — a ten-kilometre radius expanded into box degrees is fine in Rome and nonsense in Svalbard. Systems that operate across latitudes state the metric of the expansion instead of hoping it will not matter.

Primary sources: <https://en.wikipedia.org/wiki/Haversine_formula> and <https://postgis.net/documentation/>.

## Decision rules

- Pick the precision rung deliberately: Euclidean-never, haversine for ordinary radius, geodesic where sub-percent error is a requirement, with the choice recorded.
- Radius queries always two-step: box expansion by the radius, then exact distance refinement on candidates.
- State the expansion metric: metres-to-degrees is latitude-dependent, and a constant conversion is a polar defect.
- Distances over households' scale cross the projection question; compute in a local projected grid when measuring in metres, and on the ellipsoid when global.
- Bound the radius the system permits; unbounded user-supplied radii are unbounded index scans.
- Verify with known pairs, including one high-latitude pair and one across the anti-meridian.

## Procedure

1. Choose the distance formula rung and record why.
2. Implement the radius query as expansion plus refinement.
3. Implement the metres-to-degrees expansion with the latitude dependence stated.
4. Bound the maximum radius the system will honour.
5. Verify with a table of known pairs and their true distances, including the edge latitudes.
6. Record the formula choice and the verification table in the geospatial record.

## Anti-patterns

- Euclidean distance on lat/lng degrees shipped as kilometres.
- Haversine precision paid for where a rough adjective would have done, while the radius expansion is still wrong by a factor of two.
- A constant degrees-per-metre expansion across a country the size of Canada.
- Radius queries without the bounding-box first step, timed out on the first big city.
- No upper bound on radius, so a prank or a bug scans the planet.

## Done checklist

- [ ] Formula rung chosen and recorded.
- [ ] Two-step radius query implemented.
- [ ] Latitude-dependent expansion implemented.
- [ ] Radius upper-bound set.
- [ ] Known-pairs verification including high-latitude and anti-meridian.
- [ ] Choices in the record.

## Sources

- Haversine formula: <https://en.wikipedia.org/wiki/Haversine_formula>
- PostGIS distance functions and their semantics: <https://postgis.net/documentation/>
- Geographic datatypes overview: <https://www.postgresql.org/docs/current/datatype-geometric.html>
