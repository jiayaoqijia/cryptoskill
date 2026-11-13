---
name: bounding-boxes-and-filters
domain: software-engineering/bounding-boxes-and-filters
trigger: "Using bounding boxes as the cheap filter, knowing where they mislead."
anti_trigger: "Not for the index structures themselves, and not for distance queries."
scope: "The cheap approximate filter and where it misleads."
status: seedling
---

# Bounding boxes and filters

## Standard

A bounding box is the smallest axis-aligned rectangle containing a shape, and it is the workhorse of spatial filtering because rectangle intersection is a few comparisons — cheap enough to run over millions of candidates inside a spatial index whose nodes are themselves boxes. The standard two-step shape of a spatial query follows: a filter pass that uses boxes to find candidates, then a refinement pass that runs the real geometry test only on those candidates. The expensive predicate is computed rarely because the cheap one runs first.

The misleading part is that a bounding box is a claim about coverage, not content. A long diagonal road's box covers a city block it never touches; the anti-meridian slice of Alaska wraps the globe in longitude; and a polygon with holes has a box full of not-polygon. The filter step therefore over-selects by design, which is correct, but any step that treats the candidate set as the answer — counting boxes, or drawing them — states something the geometry does not support.

Primary sources: <https://en.wikipedia.org/wiki/Minimum_bounding_box> and <https://postgis.net/documentation/>.

## Decision rules

- Use bounding boxes only as the filter step; the refinement pass exists, always, and is not an optional loop.
- Expanding a distance query's box must account for the metric of the refinement: a radius in metres expands the box in degrees, and the expansion is not symmetric in latitude.
- Date-line queries need the split treatment: one query becomes two when the box would cross longitude 180.
- Boxes describing shapes with holes or concavities over-select in proportion to the shape's emptiness; accept it, but do not count candidates as results.
- Any published count, fee, or coverage dependent on spatial containment must come from the refinement pass, never from the filter.
- Document each two-step query with which step the reported number came from.

## Procedure

1. Express the query's true predicate precisely (within, intersects, within-distance, contains).
2. Compute the filter envelope, expanding for metric and date-line requirements.
3. Run the index filter with the envelope, producing a candidate set.
4. Run the refinement predicate on the candidates, producing the answer set.
5. Verify the answer set on a known sample, including a shape straddling the anti-meridian.
6. Record the filter's candidate/answer ratio on production shapes as the over-selection baseline.

## Anti-patterns

- Reporting filter-pass counts as results and shipping a coverage map with box-shaped islands.
- Distance queries with unexpanded or symmetrically-expanded boxes in high latitudes.
- One query across the anti-meridian, silently returning nothing.
- Optimising the filter and never measuring the refinement, then being surprised aconcave shapes dominate cost.
- Treating the two-step as one step for pagination; the last page of the filter is not the last page of the answer.

## Done checklist

- [ ] True predicate written before the envelope.
- [ ] Envelope expansion verified for metric and latitude.
- [ ] Date-line split handled and tested with a known straddler.
- [ ] Refinement measured alongside the filter.
- [ ] Reported numbers always from the refinement.
- [ ] Over-selection ratio recorded as the baseline.

## Sources

- Minimum bounding box overview: <https://en.wikipedia.org/wiki/Minimum_bounding_box>
- Two-step filter and refinement practice: <https://postgis.net/documentation/>
- Spatial types overview: <https://dev.mysql.com/doc/refman/8.0/en/spatial-types.html>
