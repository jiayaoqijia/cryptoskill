---
name: the-memory-wall
domain: software-engineering/the-memory-wall
trigger: "Understanding why inference serving is bound by memory bandwidth not compute."
anti_trigger: "Not for kernel code, and not for capacity planning headroom."
scope: "Why serving speed is a memory budget problem, not a compute problem."
status: seedling
---

# The memory wall

## Standard

Autoregressive decoding is a serial loop: each generated token needs every previous token's keys and values, and loading those tensors from accelerator memory consumes memory bandwidth, not compute. The result is that decoding is memory-bandwidth-bound — the accelerator sits partly idle waiting for weight activations and KV tensors to stream through. A model that could compute orders of magnitude faster would still serve at the memory system's pace.

This reframes every serving question. Adding compute does not speed up decoding; moving the same work closer to the memory, shrinking what must be loaded, or overlapping loads with useful compute does. That is why architecture changes like multi-query attention — sharing keys and values across heads to shrink the loaded tensors — directly translate into decoding speed without any kernel magic, and why serving engines live or die on KV-cache memory management rather than raw FLOPS.

Primary sources: <https://arxiv.org/abs/1911.02150> and <https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)>.

## Decision rules

- Treat memory bandwidth, not compute, as the decoding constraint when predicting serving behaviour.
- State the accelerator's HBM capacity and bandwidth before any concurrency arithmetic.
- Distinguish prefill — which IS compute-bound and parallel — from decode, which is not.
- Evaluate engine claims against this framing: gains that come from loading fewer bytes are real and repeatable; gains that ignore memory are suspect.
- Model the KV tensor size per token per layer before choosing a concurrency target.
- Record which model architecture properties (head count, sharing) change the loaded-tensor size.

## Procedure

1. Record the accelerator's memory capacity and bandwidth figures.
2. Compute per-token KV tensor size for the model's layers and heads.
3. Separate prefill from decode in any latency measurement.
4. Compute the concurrency the remaining KV headroom admits after weights.
5. Sanity-check any claimed throughput against the bandwidth it would require.
6. Write the arithmetic into the serving record with the workload's sequence mix.

## Anti-patterns

- Explaining slow decoding with insufficient FLOPS.
- Comparing engines on compute hardware without memory capacity context.
- Ignoring the prefill/decode split when a claim mixes both.
- Sizing concurrency from compute alone and overflowing into host memory mid-request.
- Treating architecture changes like attention sharing as quality curiosities rather than bandwidth facts.

## Done checklist

- [ ] HBM capacity and bandwidth recorded.
- [ ] Per-token KV size computed.
- [ ] Prefill and decode separated in measurements.
- [ ] Concurrency computed from KV headroom.
- [ ] Claims checked against bandwidth arithmetic.
- [ ] Workload sequence mix recorded with the numbers.

## Sources

- Multi-query attention (Shazeer): <https://arxiv.org/abs/1911.02150>
- Transformer architecture: <https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)>
- Serving engines landscape: <https://github.com/vllm-project/vllm>
