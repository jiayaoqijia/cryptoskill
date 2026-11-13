---
name: accelerator-record
domain: software-engineering/accelerator-record
trigger: "Writing the record of a kernel, its numbers, and its transfers."
anti_trigger: "Not for vendor profiling tools, and not for release notes."
scope: "The written record: device, numbers, and the transfer ledger."
status: seedling
---

# Accelerator record

## Standard

The accelerator record states the kernel's pattern and geometry, the device it was measured on, the numbers it produced, and the transfers that surround it — because none of those travel with the code. A kernel's performance is a property of a device generation, a data layout, and a launch configuration; the same kernel on a successor device can run several times faster or slower, and without the record there is no way to know which assumption moved.

The record's most-omitted section is the transfer ledger. Kernel-only measurements flatter every accelerator programme, since the wall-clock includes the crossings; the ledger lists each transfer with its size, direction, and measured time, so a later reviewer can see whether the computation was ever the dominant cost. Numbers carry their device, driver, and input shape; a speedup claimed without those is a claim about a machine the reader does not have.

Primary sources: <https://docs.nvidia.com/cuda/> and <https://osf.io/prereg/>.

## Decision rules

- The record states pattern, launch geometry, and resource use for each kernel.
- Every measurement carries device, driver version, and input shape.
- The transfer ledger lists every crossing with size, direction, and measured time.
- Wall-clock is recorded alongside kernel-only time.
- Optimisation decisions are recorded with the before-and-after pair that justified them.
- The record is updated when the device generation changes — old numbers are archived, not deleted.

## Procedure

1. Record each kernel's pattern, block size, resource use, and occupancy achieved.
2. Collect the timeline including transfers; build the transfer ledger.
3. Record wall-clock and compute-only time, labelled, from the same run.
4. Attach device, driver, and input shape to every number recorded.
5. For each optimisation, store the paired measurements and the decision.
6. On a device or driver change, re-run the record's cases and archive the previous numbers.

## Anti-patterns

- Kernel-only timings presented as programme speed.
- Speedups without the baseline's device and input shape.
- Transfer counts stated vaguely as "some host traffic".
- Numbers from a previous architecture compared against a new one without re-measuring.
- Deleted baselines that made an optimisation claim unfalsifiable.

## Done checklist

- [ ] Pattern and geometry recorded per kernel.
- [ ] Device, driver, input shape attached to numbers.
- [ ] Transfer ledger complete with measured times.
- [ ] Wall-clock recorded alongside kernel time.
- [ ] Optimisation pairs recorded with decisions.
- [ ] Device-change re-measurement done and archived.

## Sources

- CUDA profiling and metrics documentation: <https://docs.nvidia.com/cuda/>
- Pre-registration practice for stated measurements: <https://osf.io/prereg/>
- OpenCL profiling events: <https://www.khronos.org/registry/OpenCL/>
