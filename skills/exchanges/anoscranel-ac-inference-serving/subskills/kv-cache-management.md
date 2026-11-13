---
name: kv-cache-management
domain: software-engineering/kv-cache-management
trigger: "Managing the per-request key-value cache as the scarce serving resource."
anti_trigger: "Not for attention math, and not for GPU kernel optimization."
scope: "The per-request cache: sizing, fragmentation, and paging strategies."
status: seedling
---

# KV cache management

## Standard

Each active request carries a KV cache: for every generated token, every attention layer stores key and value tensors so future tokens can attend to the past. The cache grows with sequence length, lives in scarce HBM, and — in naive block allocation — wastes real memory to fragmentation and to duplicated shared prefixes. The batch size a GPU admits is decided by how much KV the leftover memory — after weights — can hold.

PagedAttention treats the KV cache like virtual memory: fixed-size blocks, allocated on demand, with near-zero external fragmentation, and the possibility of sharing blocks across requests whose prefixes are identical. That is the shift from cache-as-one-allocation to cache-as-managed-pages — and the reason identical-prefix workloads (standing instruction blocks, beam search, few-shot families) can share storage instead of duplicating it.

Primary sources: <https://arxiv.org/abs/2309.06180> and <https://docs.vllm.ai/en/latest/>.

## Decision rules

- Compute KV bytes per token per layer (2 × head count × head dim × dtype for both keys and values) before any capacity claim.
- State max concurrency as the KV headroom divided by the average-cache size for the workload's sequence mix.
- Prefer block-managed (paged) allocation over monolithic cache blocks when sequences vary in length.
- Exploit prefix sharing where workloads repeat prefixes: measure the shared fraction, do not assume it.
- Set a hard cap on tokens per request so one runaway sequence cannot evict the whole batch.
- Record preemption or eviction policy: what happens when KV memory runs out mid-request.

## Procedure

1. Compute per-token, per-layer KV size for the target model.
2. Subtract weight and activation memory from HBM to get KV headroom.
3. Derive reachable concurrency for the workload's length distribution.
4. Record the allocation scheme: contiguous, paged, or shared-prefix aware.
5. Define and record the out-of-memory behaviour: preemption, eviction, queueing.
6. Test one rejected and one accepted oversized request before declaring the cap works.

## Anti-patterns

- Sizing concurrency by request count rather than by KV bytes.
- Ignoring fragmentation under varied sequence lengths with contiguous caches.
- Sharing prefixes across requests believed similar — measure the overlap first.
- No per-request token cap: a single long generation stalls the fleet.
- Unknown out-of-memory behaviour discovered in production rather than tested.

## Done checklist

- [ ] Per-token KV size computed.
- [ ] Headroom and reachable concurrency stated.
- [ ] Allocation scheme recorded.
- [ ] Prefix-sharing fraction measured if used.
- [ ] Token cap set and tested both sides.
- [ ] OOM policy recorded and rehearsed.

## Sources

- PagedAttention (Kwon et al., SOSP 2023): <https://arxiv.org/abs/2309.06180>
- vLLM engine docs: <https://docs.vllm.ai/en/latest/>
- LLM architecture context: <https://en.wikipedia.org/wiki/Large_language_model>
