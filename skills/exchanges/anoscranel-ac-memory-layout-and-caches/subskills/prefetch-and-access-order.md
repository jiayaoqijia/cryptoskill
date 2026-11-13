---
name: prefetch-and-access-order
domain: software-engineering/prefetch-and-access-order
trigger: "Designing access patterns the hardware can predict."
anti_trigger: "Not for query plans, and not for network prefetching."
scope: "Sequential streams, strided access, and the patterns hardware predicts."
status: seedling
---

# Prefetch and access order

## Standard

The hardware prefetcher learns simple patterns: a forward stream, a fixed stride within a page, and a short repeating sequence in some designs. When a loop's access pattern matches one of those, the prefetcher hides most of the DRAM latency and the loop runs at near-cache speed; when it does not — pointer chasing, backwards traversal, irregular strides — every access stalls on memory and the difference can be an order of magnitude.

The design consequence is that iteration order is a performance decision as much as an algorithmic one. A matrix traversed row-major when stored column-major touches one new cache line per element; the same traversal in the other order amortizes a line across many elements. Software prefetch hints exist, but they help only when the pattern is predictable a few accesses ahead, which is another way of saying the layout itself must be regular.

Primary sources: <https://www.akkadia.org/drepper/cpumemory.pdf> and <https://agner.org/optimize/>.

## Decision rules

- Record the storage order of any multidimensional data and traverse in that order on the hot path.
- Classify each hot loop's pattern: stream, fixed stride, or irregular.
- Avoid pointer-chasing walks on hot paths, or batch the target data into a contiguous copy first.
- Prefer structure-of-arrays for uniform field access; array-of-structs when fields are used together.
- Use software prefetch only where the address is computable several iterations ahead and measurement confirms a win.
- Measure with the prefetcher warm, not in a cold single pass.

## Procedure

1. Identify the hot loops and their dominant data references.
2. Classify each as stream, stride, or irregular.
3. Check traversal order against storage order.
4. Restructure to match, or copy to a contiguous layout when the source cannot change.
5. Measure per-loop and end-to-end after the change.
6. Record the pattern classification and both measurements.

## Anti-patterns

- Traversing against the storage order for readability alone.
- Software-prefetching irregular access patterns.
- Evaluating prefetch or layout changes on a cold cache.
- Choosing structure-of-arrays without knowing which fields travel together.
- Keeping an irregular hot path because the data model is elegant.

## Done checklist

- [ ] Hot loops classified by pattern.
- [ ] Traversal order matches storage order.
- [ ] Pointer chasing eliminated or batched.
- [ ] Layout choice justified by field usage.
- [ ] Warm-cache measurements taken.
- [ ] Classification and measurements recorded.

## Sources

- Memory patterns and prefetching: <https://www.akkadia.org/drepper/cpumemory.pdf>
- Agner Fog optimization resources: <https://agner.org/optimize/>
- Performance tooling: <https://www.brendangregg.com/linuxperf.html>
