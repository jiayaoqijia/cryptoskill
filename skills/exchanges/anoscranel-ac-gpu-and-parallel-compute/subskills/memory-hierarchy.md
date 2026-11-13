---
name: memory-hierarchy
domain: software-engineering/gpu-memory-hierarchy
trigger: "Placing data across global, shared, and register memory."
anti_trigger: "Not for CPU cache lines, and not for allocation APIs."
scope: "Global, shared, and register memory, and what each costs."
status: seedling
---

# Memory hierarchy

## Standard

Device memory comes in layers whose costs differ by two orders of magnitude. Global memory is large, visible to all threads, and slow unless access is coalesced. Shared memory is small, per-block, and fast — on the order of the CPU registers it resembles. Registers are fastest and allocated per thread, but their count limits how many threads can be resident, which links this leaf to occupancy: every extra register per thread is paid for in scheduling slack.

The design decision is explicit staging. Data is loaded from global memory into shared memory or registers once, by a whole warp cooperating, and then reused many times from the fast layer. A kernel that reads its inputs from global memory on every use pays the slow rate every time, and no amount of occupancy recovers it. The staging decision is made per data structure, and structures that are used once belong in global memory — staging costs more than it saves.

Primary sources: <https://docs.nvidia.com/cuda/> and <https://www.khronos.org/registry/OpenCL/>.

## Decision rules

- Record the shared-memory budget per block for the target device before designing staging.
- Stage into shared memory only what is reused across threads in the block.
- Count registers per thread as a cost against occupancy, not as a free resource.
- Let read-once data stay in global memory; staging it is pure overhead.
- Load cooperatively: the whole warp moves data into the fast layer, not one thread at a time.
- State the reuse factor of every staged buffer — reuse below a small number wastes the staging.

## Procedure

1. Inventorise each data structure with its size, lifetime, and reuse count.
2. Mark which structures are reused across threads within a block.
3. Stage only those into shared memory; compute per-thread values into registers.
4. Size the staging against the shared-memory budget and adjust block dimensions.
5. Write cooperative load paths that gather from global memory into the staged layout.
6. Measure the kernel with and without staging on realistic data sizes.

## Anti-patterns

- Staging everything because shared memory is fast.
- Reading the same global data repeatedly inside the inner loop.
- Ignoring the register count until occupancy mysteriously halves.
- One thread loading a buffer the whole block uses.
- Designing staging for tiny inputs where the staging is the whole runtime.

## Done checklist

- [ ] Structures inventorised with reuse counts.
- [ ] Staging limited to cross-thread reuse.
- [ ] Register budget accounted against occupancy.
- [ ] Read-once data left in global memory.
- [ ] Cooperative load paths written.
- [ ] With-and-without staging measured.

## Sources

- CUDA memory hierarchy documentation: <https://docs.nvidia.com/cuda/>
- OpenCL memory model: <https://www.khronos.org/registry/OpenCL/>
- CPU–GPU memory pattern analysis: <https://citeseerx.ist.psu.edu/>
