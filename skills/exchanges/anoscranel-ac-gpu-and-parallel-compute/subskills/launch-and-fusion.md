---
name: launch-and-fusion
domain: software-engineering/launch-and-fusion
trigger: "Deciding what runs on device and how kernels are chunked."
anti_trigger: "Not for vendor APIs as such, and not for CPU threading."
scope: "Launch overhead, fusion, streams, and the host–device transfer tax."
status: seedling
---

# Launch and fusion

## Standard

Every kernel launch costs time — a fixed overhead in the microseconds, paid for scheduling and setup regardless of how little work the kernel does. A program that issues thousands of tiny launches can spend more time launching than computing, and the fix is fusion: fewer kernels, each doing more, so the overhead amortises over real work. The same reasoning applies at the boundary of the device: a transfer between host memory and device memory crosses a slow bus, and a program that shuffles small buffers back and forth per kernel pays the crossing both ways, repeatedly.

The discipline is end-to-end accounting. The sums are simple and the profile is where the truth appears: transfer time and launch time must be made visible deliberately, because a profiler focused on kernel execution will happily report beautiful kernel timings while the wall-clock is dominated by crossings the report never mentions. Fusing two kernels is only correct if it does not force extra transfers; separating them is only correct if the transfers and launches that result are counted.

Primary sources: <https://docs.nvidia.com/cuda/> and <https://www.khronos.org/registry/OpenCL/>.

## Decision rules

- Account for wall-clock, not kernel time: launches, crossings, and host work all belong in the ledger.
- Prefer fusing small kernels when their inputs and outputs already sit on the device.
- Never round-trip to host memory inside a loop without counting the crossings.
- Batch small transfers, or eliminate them, before optimising the kernels they feed.
- Use concurrent streams when the transfers and compute can genuinely overlap; state the overlap you expect.
- Record the transfer ledger: each crossing's size, count, and measured time.

## Procedure

1. Count launches per second and the average kernel runtime; compute the launch overhead fraction.
2. Make transfers visible on the timeline — their size, direction, and duration per call.
3. Fuse or batch where the overhead fraction or crossing time dominates arithmetic.
4. Keep data resident on the device across iterations when it is produced and consumed there.
5. Where overlap is available, pipeline transfers and compute in separate streams.
6. Re-measure end-to-end and record the deltas against the earlier accounting.

## Anti-patterns

- Celebrating kernel-time improvements while wall-clock does not move.
- Data shipped to the device eagerly and shipped back the same frame.
- Fusing kernels in a way that forces extra transfers, creating the overhead it saved.
- Overlapping transfers in theory, without a timeline that shows the overlap.
- Launching many tiny kernels to keep code modular, without counting the launch tax.

## Done checklist

- [ ] Launch overhead fraction computed.
- [ ] Transfers visible with size and duration in the timeline.
- [ ] Fusion or batching applied where it was the true cost.
- [ ] Device-resident data kept resident across use.
- [ ] Stream overlap verified, not assumed.
- [ ] End-to-end delta recorded.

## Sources

- CUDA streams and concurrency documentation: <https://docs.nvidia.com/cuda/>
- OpenCL command queues: <https://www.khronos.org/registry/OpenCL/>
- CPU–GPU transfer cost analysis: <https://citeseerx.ist.psu.edu/>
