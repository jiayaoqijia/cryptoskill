---
name: execution-model
domain: software-engineering/execution-model
trigger: "Understanding how warps execute and why divergence costs."
anti_trigger: "Not for vendor API details, and not for CPU pipelines."
scope: "Warps in lockstep, divergence as serialisation, and latency hiding."
status: seedling
---

# Execution model

## Standard

Throughput processors execute threads in fixed-size groups — warps on GPUs, equivalent work-groups elsewhere — and the group is the unit of scheduling. All threads in a warp advance through the same instruction at the same time; there is one program counter per warp, not per thread. The consequence governs everything else: when threads in a warp take different branches, the hardware executes each side in turn and masks the threads not on it. Divergence does not fail and does not warn — it serialises, and the warp runs at the speed of the sum of its paths.

The second property is that per-thread latency is long and mostly does not matter. A memory reference costs hundreds of cycles, and the device hides that latency by switching to other resident warps while the first waits. The programme that feels fast is the one that keeps enough warps resident to cover their own stalls; the programme that feels slow is often not slow per instruction, but short of independent work to schedule during stalls.

Primary sources: <https://docs.nvidia.com/cuda/> and <https://www.khronos.org/registry/OpenCL/>.

## Decision rules

- State the warp or group size for the target device before reasoning about branch costs.
- Keep branch conditions uniform within a warp wherever the data layout allows it.
- Treat divergence as a serialisation cost to be measured, not a coding sin to be avoided at any price.
- Judge a kernel by whether enough independent work exists to hide its own latency.
- Prefer reorganising data so that neighbouring threads take the same path, over rewriting control flow.
- Record the divergence cost when it is measured, with the access pattern that produced it.

## Procedure

1. Identify the warp size and the mapping from thread index to data element.
2. Mark each branch and classify it uniform or divergent within a warp.
3. Restructure layouts so branches align with warp boundaries where possible.
4. For remaining divergence, estimate the serialisation as the sum of path costs.
5. Check resident-warp count against the latency the kernel must hide.
6. Measure before and after with the same data, and record both numbers.

## Anti-patterns

- Reasoning about per-thread performance in an engine that schedules per warp.
- Fighting divergence with deeply nested conditionals that cost more than they save.
- Assuming a faster clock will fix a latency-bound kernel.
- Ignoring the mapping between thread index and memory address, which decides uniformity.
- Optimising an inner loop whose divergence is caused by the data layout.

## Done checklist

- [ ] Warp size and thread-to-element mapping stated.
- [ ] Branches classified uniform or divergent.
- [ ] Layout-driven divergence restructured where possible.
- [ ] Remaining divergence cost estimated.
- [ ] Latency-hiding work counted.
- [ ] Before and after measurements recorded.

## Sources

- CUDA programming documentation: <https://docs.nvidia.com/cuda/>
- OpenCL specification: <https://www.khronos.org/registry/OpenCL/>
- Metal shading language specification: <https://developer.apple.com/metal/Metal-Shading-Language-Specification.pdf>
