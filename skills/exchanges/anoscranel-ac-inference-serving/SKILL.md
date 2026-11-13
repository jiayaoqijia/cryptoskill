---
name: ac-inference-serving
description: "Serving model inference to real traffic: the memory wall and why tokens per second is a budget problem, KV-cache management as the core allocation, batching from static-naive to continuous with its latency trade, streaming responses and the first-token latency that users feel, throughput-versus-latency as the explicit design axis, autoscaling model replicas, and the written serving record. It explains how inference infrastructure behaves under load; it never promises a tokens-per-second figure. Use when asking \"LLM inference serving\", \"KV cache\", \"continuous batching\", \"first token latency\", \"TTFT\", \"model deployment GPUs\", \"inference throughput\", \"streaming responses\", \"serving stack\", \"vLLM vs TensorRT\", \"why is inference slow\", \"inference autoscaling\". Not for GPU kernel programming within a model (ac-gpu-and-parallel-compute), not for the deployment mechanics of ordinary services (ac-ci-and-release), not for picking model tiers per request (ac-token-cost-optimization)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Inference serving

## Overview

Training a model once and serving it to traffic are different engineering problems. Training is a batch job that ends; serving is a queue that never empties. The serving problem is a memory-and-scheduling problem: every active request holds a KV cache that grows with the generated length, the accelerator's high-bandwidth memory is finite, and the operator trades how many requests run concurrently against how fast each one completes. Throughput and latency are not two settings — they are the two ends of one dial.

This skill covers the serving layer: the memory wall as the organizing constraint, KV-cache allocation as the craft, batching from static to continuous, streaming and the user-felt first-token latency, the throughput-latency dial, and GPU-fleet scaling. Kernel-level programming inside a model belongs to the GPU skill; ordinary deployment mechanics belong to release engineering.

Primary sources: <https://arxiv.org/abs/2309.06180> and <https://docs.vllm.ai/en/latest/>.

## When to use

- When serving model inference to concurrent traffic.
- When choosing between throughput and latency, or diagnosing which one the workload actually bought.
- When sizing GPU memory for an inference fleet.
- When evaluating a serving engine's claims against a workload's shape.

## When NOT to use

- For kernel programming and memory layout inside the model (use ac-gpu-and-parallel-compute).
- For rollout and rollback mechanics of ordinary services (use ac-ci-and-release).
- For routing requests to model tiers on cost grounds (use ac-token-cost-optimization).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/the-memory-wall.md` | `software-engineering/the-memory-wall` | Why serving speed is a memory budget problem, not a compute problem. |
| `subskills/kv-cache-management.md` | `software-engineering/kv-cache-management` | The per-request cache: sizing, fragmentation, and paging strategies. |
| `subskills/batching-strategies.md` | `software-engineering/batching-strategies` | From static batching to continuous: what each trades. |
| `subskills/streaming-and-first-token.md` | `software-engineering/streaming-and-first-token` | Streaming and TTFT: the latency the user actually feels. |
| `subskills/throughput-versus-latency.md` | `software-engineering/throughput-versus-latency` | The one dial: where an operating point is chosen and stated. |
| `subskills/gpu-fleet-scaling.md` | `software-engineering/gpu-fleet-scaling` | Replicas, batch admission, and why CPU autoscaling rules do not transfer. |
| `subskills/serving-record.md` | `software-engineering/serving-record` | The written record: fleet shape, operating point, and the measurements behind them. |

## Status and honest limits

Serving claims are workload-specific to a degree that general numbers mislead: a 4x throughput claim from one paper's workload can invert under a different sequence-length mix. Every number in a serving record carries its workload shape, and engines evolve quickly enough that any performance statement has a shelf life. Nothing here recommends an engine; the mechanics apply to any stack that holds KV caches in finite memory.
