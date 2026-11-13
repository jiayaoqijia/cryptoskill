---
name: nearest-neighbour
domain: software-engineering/nearest-neighbour
trigger: "Serving which of these is closest, quickly and honestly."
anti_trigger: "Not for radius queries alone, and not for route planning."
scope: "The k-NN query and the index that makes it fast."
status: seedling
---

# Nearest neighbour

## Standard

The nearest-neighbour question — which of these points is closest to here, or the k closest — differs from the radius question because the search expands until it finds, rather than filtering everything within a stated bound. The index does the finding: a spatial tree descends the branches whose boxes could still contain something closer than the best candidate so far, pruning the rest. The result is a query whose cost scales with how far the answer is, not with how large the table is.

An honest k-NN result states k and the tie behaviour. Distances tie at airports and at grid intersections, and whether the system's tenth-pizza-shop is deterministic under ties is a user-visible decision worth recording rather than repeating. The distinction that disciplines the whole query is candidates versus answers again: the pruned search returns exactly the k true nearest, while an approximation that scans cells by encoding distance is a fuzzy business whose worst cases cluster exactly where users query most — the dense district where every business is.

Primary sources: <https://en.wikipedia.org/wiki/R-tree> and <https://postgis.net/documentation/>.

## Decision rules

- Prefer the index's true k-NN operator over an approximate cell-scan when the answer is user-facing; approximate scans are for candidate generation, not promises.
- State k and the tie policy in the interface contract, and test ties deliberately.
- Consider a maximum-search bound so a query in an empty region terminates without scanning half the index.
- Geohash-prefix scanning needs an explicit verification pass, and its edge cases are dense areas across cell boundaries — verify with exactly that fixture.
- Measure k-NN latency on the dense urban sample, not the uniform one; density is the hard case.
- Record the index structure the answer relies on, so a change to the index is recognized as a change to the query's behaviour.

## Procedure

1. Fix the query contract: k, tie policy, maximum search radius, and the distance formula rung.
2. Implement over the spatial index's native nearest operator where one exists.
3. Where one does not, implement the expanding-ring scan with the encoding's edge cases tested.
4. Add the termination bound for empty regions and record its diameter.
5. Verify with fixtures: a dense cluster with ties, a sparse region, and a query point near a cell boundary.
6. Record the contract, fixtures, and dense-sample latency numbers with the date.

## Anti-patterns

- A prefix "radius" guessed large enough to be probably-right, with no verification pass.
- Ties resolved by insertion order, so adding a restaurant changes which of two equidistant ones answers.
- Nearest queries against a table with no spatial index, timing out on city scale.
- Approximate cell-scan results presented as exact, with users noticing in the dense district first.
- Measuring latency on a uniform grid and calling the average a characterisation.

## Done checklist

- [ ] Contract with k, ties, bound stated.
- [ ] Index-native operator used where present.
- [ ] Verification pass for encoding scans.
- [ ] Termination bound for sparse regions.
- [ ] Dense-cluster and boundary fixtures pass.
- [ ] Dense-sample latency recorded.

## Sources

- R-tree nearest-neighbour behaviour: <https://en.wikipedia.org/wiki/R-tree>
- PostGIS nearest-neighbour operator documentation: <https://postgis.net/documentation/>
- Geohash edge behaviour: <https://en.wikipedia.org/wiki/Geohash>
