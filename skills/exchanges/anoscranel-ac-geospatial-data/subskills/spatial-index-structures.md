---
name: spatial-index-structures
domain: software-engineering/spatial-index-structures
trigger: "Choosing the structure that makes spatial queries findable."
anti_trigger: "Not for distance arithmetic, and not for rendering."
scope: "R-trees, quadtrees, and space-filling encodings, and what each is for."
status: seedling
---

# Spatial index structures

## Standard

A spatial index has to answer a question a b-tree cannot: which objects lie in this region or near this point, when the sort order of any single dimension scatters neighbours. The R-tree answers by hierarchy: each node stores a bounding box covering its children, so a query descends only into boxes it intersects. The quadtree answers by subdivision: space splits into four at each level until cells hold few objects. Space-filling encodings — geohash and its relatives — interleave the bits of both coordinates so that a one-dimensional ordering preserves locality, and then any ordinary index works.

Each structure earns its keep differently. R-trees suit stored geometry of mixed size with rectangle overlap queries; quadtrees suit fixed-point data and simple proximity in a bounded region; geohash suits simple points in systems with no native spatial index, at the cost of edge effects — two points across a boundary share almost no prefix, and nearness by prefix is an approximation, not a promise. The choice follows the query shape, and the index that fits the data distribution is the one worth measuring.

Primary sources: <https://en.wikipedia.org/wiki/R-tree> and <https://en.wikipedia.org/wiki/Quadtree>.

## Decision rules

- Choose by query family first: overlap and containment favour R-trees, proximity on points favours grid or encoding structures, and region-of-interest over heterogeneous geometry favours the tree.
- Geohash prefix matching is approximate: adjacent points across a boundary disagree early, so use it as a candidate filter with a verified second pass.
- For a native spatial index, insert real shapes, not points, when the workload queries shapes.
- Measure index behaviour on the real data distribution — a uniform synthetic set flatters any index, and coastlines punish them differently.
- Record the structure and its parameters, because a spatial index's performance claim without its data shape is not reproducible.
- Re-index on significant data growth; spatial indexes degrade non-linearly past their built-for density, unlike the graceful decline of simpler structures.

## Procedure

1. Write down the query families the workload actually issues.
2. Match each family to the structure that serves it, and let the dominant family decide the primary index.
3. Build the index on a realistic sample, and measure representative queries.
4. For encoded approaches, fix the precision level and record the candidate-split ratio between filter and verification.
5. On deployment, monitor index depth and query latency against the measured baseline.
6. Record structure, parameters, distribution statistics, and measured numbers with the date.

## Anti-patterns

- Prefix-matching geohashes for exact neighbours and claiming precision across boundaries.
- An R-tree measured on uniform points, deployed on a city road network.
- Storing coordinates as concatenated strings, sorted — an index that answers nothing spatial.
- One precision level for the whole planet's point data, with dense cities starved and oceans over-resolved.
- Never re-indexing after the dataset doubles; then blaming the database for the geometry.

## Done checklist

- [ ] Query families listed before structure chosen.
- [ ] Structure matched to the dominant family.
- [ ] Encoded approaches recorded as filters with verification passes.
- [ ] Real-distribution measurements recorded.
- [ ] Precision or parameters fixed and documented.
- [ ] Re-index trigger defined on growth.

## Sources

- R-tree overview: <https://en.wikipedia.org/wiki/R-tree>
- Quadtree overview: <https://en.wikipedia.org/wiki/Quadtree>
- Geohash overview: <https://en.wikipedia.org/wiki/Geohash>
