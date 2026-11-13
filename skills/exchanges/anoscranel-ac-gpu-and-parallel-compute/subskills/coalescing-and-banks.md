---
name: coalescing-and-banks
domain: software-engineering/coalescing-and-banks
trigger: "Getting global memory coalesced and shared memory conflict-free."
anti_trigger: "Not for API details, and not for cache-line reasoning on CPUs."
scope: "Contiguous access patterns as the first lever, and bank conflicts."
status: seedling
---

# Coalescing and banks

## Standard

When a warp reads global memory, the hardware can serve the whole warp in one transaction if the addresses form a contiguous, aligned range covering one or a few device words — this is coalescing, and it is the largest single performance lever in most kernels. When the same warp reads scattered addresses, the hardware issues one transaction per element, and the kernel runs at the memory system's worst rate while using a fraction of its bandwidth. The pattern, not the volume, decides the cost.

Shared memory has its own rule, and its own silent failure. It is divided into banks that can each serve one request per cycle; when threads in a warp ask different words inside the same bank, the requests serialise — a bank conflict. The layout that puts neighbouring threads on neighbouring banks is the same discipline as coalescing applied to the fast layer, and padding a data layout by one word to break a conflict-ridden stride is a standard, measurable fix.

Primary sources: <https://docs.nvidia.com/cuda/> and <https://www.khronos.org/registry/OpenCL/>.

## Decision rules

- Write the address formula for each access before reasoning about anything else.
- If threads-in-a-warp read addresses that differ by a constant stride, make the stride the natural width and alignment.
- Aim for a range of addresses covering a small number of contiguous device words per warp access.
- For shared memory, check whether threads in a warp hit distinct banks; pad strides that repeat banks.
- Prefer structure changes — transposition, tiled layouts — over access-order gymnastics in the kernel.
- Record the transaction count per access, not just bytes, when measuring.

## Procedure

1. Write down the address each lane of a warp computes, symbolically, for each access.
2. Classify the pattern contiguous, strided, or scattered.
3. For strided or scattered accesses, reshape the data layout so adjacent lanes touch adjacent addresses.
4. For shared memory, compute the bank of each lane's address and detect conflicts.
5. Pad or transpose the layout until lanes sit on distinct banks.
6. Re-measure transaction counts and bandwidth achieved against the device's peak.

## Anti-patterns

- Struct-of-arrays turned into array-of-structs, forcing whole-struct reads for one field.
- Optimising arithmetic while global accesses stay scattered.
- Assuming alignment; stating alignment is a decision, not an accident.
- Copying a CPU pointer layout onto a device and expecting bandwidth.
- Fixing bank conflicts by removing shared memory rather than padding the layout.

## Done checklist

- [ ] Address formulas written symbolically per access.
- [ ] Accesses classified contiguous, strided, or scattered.
- [ ] Layout reshaped where it beats code changes.
- [ ] Bank conflicts computed and removed.
- [ ] Transaction counts measured.
- [ ] Achieved bandwidth compared with device peak.

## Sources

- CUDA best-practices guide: <https://docs.nvidia.com/cuda/cuda-c-best-practices-guide/>
- OpenCL specification: <https://www.khronos.org/registry/OpenCL/>
- Memory layout and coalescing analysis: <https://citeseerx.ist.psu.edu/>
