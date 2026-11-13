---
name: occupancy-and-resources
domain: software-engineering/occupancy-and-resources
trigger: "Choosing block size and resource use as a scheduling decision."
anti_trigger: "Not for vendor tuning tools, and not for latency budgeting of serial code."
scope: "Resident warps as scheduling slack, traded against per-thread state."
status: seedling
---

# Occupancy and resources

## Standard

Occupancy is the fraction of a device's maximum resident warps that a kernel actually keeps on each streaming processor. Resident warps are the slack the scheduler uses to hide memory latency: when one warp stalls on a global read, another runs. But occupancy is bought with per-thread resources — every register a thread holds lowers how many threads can be resident, and every byte of shared memory a block claims lowers how many blocks fit. Maximum occupancy is therefore not a goal; it is a budget line, and the honest question is how much latency-hiding the kernel needs, not how high the number can go.

The trade is measurable. A kernel with few memory stalls may run best at low occupancy, using many registers per thread; a latency-bound kernel may need high occupancy and may be worth rewriting to use fewer registers. Raising occupancy by shrinking resources can also slow a kernel down when the shrink forces spills to local memory — the slowest possible outcome, paying both the latency and the reduced arithmetic the spills cause. Only measurement at the kernel's real occupancy range resolves which side of the trade wins.

Primary sources: <https://docs.nvidia.com/cuda/> and <https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/>.

## Decision rules

- Compute the register-per-thread and shared-memory-per-block budgets from the target device.
- Derive the achievable occupancy from those budgets before selecting a block size.
- Record occupancy as achieved, with the limits that bound it — registers, shared memory, or block slots.
- Treat spills to local memory as a defect to remove, not a cost to accept.
- Sweep block sizes across the real occupancy range rather than trusting a single configuration.
- Prefer fixing the stall source when high occupancy merely hides a coalescing defect.

## Procedure

1. Record the device's limits: registers per processor, shared memory per block, resident blocks.
2. Compute the occupancy each block size achieves with the kernel's actual resource use.
3. Sweep the achievable block sizes, measuring runtime on realistic input.
4. Identify which resource binds occupancy at the best configuration.
5. Check the compiler's spill report; remove spills before drawing conclusions from occupancy.
6. Record the chosen configuration with the sweep data that justified it.

## Anti-patterns

- Maximising occupancy as a target rather than a budget decision.
- Judging configurations on one input size.
- Accepting register spills while tuning occupancy around them.
- Copying a known kernel's block size onto a different device generation.
- Raising occupancy to hide a memory-pattern defect that a layout fix would remove.

## Done checklist

- [ ] Device resource limits recorded.
- [ ] Occupancy derived per candidate block size.
- [ ] Sweep across the real range measured.
- [ ] Binding resource identified.
- [ ] Spill report checked and spills removed.
- [ ] Chosen configuration recorded with sweep data.

## Sources

- CUDA occupancy documentation: <https://docs.nvidia.com/cuda/>
- CUDA best-practices guide: <https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/>
- OpenCL specification: <https://www.khronos.org/registry/OpenCL/>
