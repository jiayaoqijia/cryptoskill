---
name: parallel-algorithms
domain: software-engineering/parallel-algorithms
trigger: "Mapping a computation onto the hardware's parallel patterns."
anti_trigger: "Not for serial algorithm choice, and not for vendor library pick lists."
scope: "Reductions, scans, tiling, and patterns that map to the hardware."
status: seedling
---

# Parallel algorithms

## Standard

An algorithm that is efficient on a serial machine can be the wrong shape for throughput hardware, because the shapes differ: a serial sum is a loop, and a parallel sum is a tree. The canonical patterns — reduction, scan, tiling, and stencil sweeps — exist because they map onto coalesced access and warp-cooperative work, and a computation expressed in those patterns gets the hardware's cooperation for free. A computation expressed as a serial loop with parallel annotations gets none of it.

The reduction tree makes the cost structure visible. Pairwise tree reduction has logarithmic depth and every step is fully coalesced; a sequential accumulation in one thread is depth-equal-to-n and leaves the hardware idle. The same reasoning covers scans, where the work-efficient pattern trades a few extra passes for coalesced access, and tiling, where a large domain is cut into blocks that fit shared memory so each element is loaded once and used many times. The practice is not to invent these patterns but to recognise which one a computation already is.

Primary sources: <https://docs.nvidia.com/cuda/> and <https://www.khronos.org/registry/OpenCL/>.

## Decision rules

- Name the pattern each computation maps to before writing kernel code.
- Express reductions as trees with cooperative loads; never a one-thread accumulation.
- Rebuild serial prefix logic as a scan when threads need running aggregates.
- Tile domains so each element is loaded once and reused, with tile size from the shared-memory budget.
- State the stride between the threads of one warp, and make it the access unit of the pattern.
- Record which pattern each kernel implements, and the serial code it replaced.

## Procedure

1. Write the computation's dataflow and mark what each output element reads.
2. Classify against the canonical patterns: reduction, scan, tile-stencil, element-wise map.
3. Choose the pattern's standard decomposition — tree depth, tile dimensions, scan passes.
4. Derive the launch geometry from the pattern and the device limits.
5. Implement with cooperative loads and coalesced strides inside the pattern.
6. Verify the result exactly (reductions) or within the format's tolerance before benchmarking.

## Anti-patterns

- A parallel loop that is a serial algorithm wearing thread indices.
- Reductions done by atomic contention instead of a tree.
- Tiles sized by habit on a new device.
- Scans implemented as one pass with scattered access.
- Measuring throughput before verifying correctness on a reduction.

## Done checklist

- [ ] Pattern named per computation.
- [ ] Reductions as cooperative trees.
- [ ] Prefix logic rebuilt as scans.
- [ ] Tiles sized from the shared-memory budget.
- [ ] Warp stride equal to the access unit.
- [ ] Correctness verified before benchmarking.

## Sources

- CUDA parallel algorithms documentation: <https://docs.nvidia.com/cuda/>
- OpenCL Worked examples: <https://www.khronos.org/registry/OpenCL/>
- Parallel algorithm analysis: <https://citeseerx.ist.psu.edu/>
