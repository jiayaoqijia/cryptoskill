---
name: numeric-formats
domain: software-engineering/numeric-formats
trigger: "Choosing precision and numeric format on throughput hardware."
anti_trigger: "Not for CPU floating-point semantics, and not for vendor tuning."
scope: "Half and mixed precision, tensor units, and result-changing formats."
status: seedling
---

# Numeric formats

## Standard

Throughput hardware gains speed by narrowing numbers. Half precision and other reduced formats double the data a memory transfer carries and double the arithmetic units a given silicon can hold, and matrix units accelerate reduced formats far beyond the general-purpose path. The gain is real, but the format is not free: every narrowing reduces the range and resolution a value can represent, and results computed in reduced formats differ from results computed in wide formats — sometimes by amounts that matter, sometimes drowned by the noise of the model that produced them.

The honest treatment has two halves. First, the choice is empirical: the procedure is to try the narrower format on the real workload and compare the end result against the wide baseline, judge the error against the decision that output feeds, and keep the format only where the error is tolerable. Second, lossless and near-lossless tricks are available first — accumulate in wide precision while storing narrow, keep reductions in wide formats, and reserve the narrowest formats for the steps where error provably washes out. A common middle path is mixed precision: narrow where the bulk of the work is, wide at the accumulations and the small set of sensitive steps.

Primary sources: <https://docs.nvidia.com/cuda/> and <https://en.wikipedia.org/wiki/Half-precision_floating-point_format>.

## Decision rules

- State the decision the computed numbers feed before choosing a format, not after.
- Compute the wide-precision baseline and keep it as the comparison reference.
- Accumulate reductions and dot products in a wider format than the operands.
- Judge reduced formats by end-result error against the decision, never by looking good in isolation.
- Record the format at every step of the pipeline — mixed precision means precision is a map, not a setting.
- Re-verify whenever the pipeline up- or downstream changes, because tolerable error is a property of the whole.

## Procedure

1. Write the baseline in the widest practical format and record its output.
2. Identify the steps whose mass of arithmetic dominates runtime.
3. Apply the narrowest format to those steps first, accumulating in wide.
4. Compare end results against the baseline, and judge the deviation against the downstream decision.
5. Map the final precision configuration — which steps narrow, which wide, where the accumulation happens.
6. Re-measure both speed and end-result error, and record both with the baseline.

## Anti-patterns

- Narrowing everything for speed and never computing a baseline.
- Comparing intermediate values, when the end result is what the decision consumes.
- Storing narrow but also accumulating narrow, losing the cheap accuracy win.
- Assuming error that was tolerable last release remains tolerable after a pipeline change.
- Treating precision as one global setting rather than a per-step map.

## Done checklist

- [ ] Wide baseline computed and kept.
- [ ] Dominant-arithmetic steps identified.
- [ ] Narrow formats applied there with wide accumulation.
- [ ] End-result error judged against the decision.
- [ ] Precision map recorded per step.
- [ ] Speed and error both recorded.

## Sources

- CUDA numerical formats documentation: <https://docs.nvidia.com/cuda/>
- Half-precision format reference: <https://en.wikipedia.org/wiki/Half-precision_floating-point_format>
- IEEE 754 interplay with language semantics: <https://en.cppreference.com/w/cpp/language>
