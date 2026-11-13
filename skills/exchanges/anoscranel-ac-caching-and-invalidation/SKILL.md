---
name: ac-caching-and-invalidation
description: "Putting a cache in front of something and keeping it correct: what to cache and the hit-rate arithmetic, TTL versus event-driven invalidation, cache-aside and read-through patterns, stampede and thundering-herd control, stampede-safe rebuilds, negative caching, consistency windows and what a reader can see, and the written cache policy record. It explains the correctness and failure modes of caching; it never recommends a product and never promises a latency. Use when asking \"cache invalidation\", \"TTL\", \"cache stampede\", \"thundering herd\", \"cache aside\", \"read through\", \"stale data\", \"when should I evict\", \"negative caching\", \"why is the cache wrong\", \"cache key design\". Not for query and index tuning in the database (ac-query-and-index-design), not for CDN and browser caching headers (ac-performance), not for content delivery architecture (ac-architecture)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Caching and invalidation

## Overview

A cache is a second copy of data that is allowed to be wrong, under rules the system chooses. Every caching question reduces to those rules: how long wrong is acceptable, who notices when it is wrong, and what happens when the cache is empty all at once. A cache with no stated staleness bound is not a performance optimisation; it is an unspecified correctness model.

This skill covers the patterns and their failure modes: what to cache and how hit rate translates into load reduction, TTL versus explicit invalidation, the read and write patterns that decide who populates the cache, the stampede that arrives when a popular key expires, and the negative caching that protects against repeated misses. Query tuning inside the database belongs to its own skill.

Primary sources: <https://aws.amazon.com/caching/best-practices/> and <https://redis.io/docs/manual/client-side-caching/>.

## When to use

- When introducing or resizing a cache in front of a data source.
- When cached data is stale and the bound is unclear.
- When a popular key expiring causes a load spike.
- When choosing between TTL and explicit invalidation.

## When NOT to use

- For index and query-plan tuning (use ac-query-and-index-design).
- For HTTP cache headers and browser-level caching (use ac-performance).
- For overall system structure and service boundaries (use ac-architecture).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/what-to-cache.md` | `software-engineering/what-to-cache` | Read-write ratio, cost of a miss, and the hit-rate arithmetic. |
| `subskills/ttl-versus-invalidation.md` | `software-engineering/ttl-versus-invalidation` | Time-based expiry against event-driven eviction, and the window each leaves. |
| `subskills/cache-patterns.md` | `software-engineering/cache-patterns` | Cache-aside, read-through, write-through, and who owns population. |
| `subskills/stampede-and-herd.md` | `software-engineering/stampede-and-herd` | What happens when a hot key expires, and the controls that bound it. |
| `subskills/negative-caching.md` | `software-engineering/negative-caching` | Caching absence, and the correctness trap it sets. |
| `subskills/consistency-windows.md` | `software-engineering/consistency-windows` | What a reader can observe, and how to state the bound in a contract. |
| `subskills/cache-policy-record.md` | `software-engineering/cache-policy-record` | The written record: keys, TTLs, invalidation, and the staleness bound. |

## Status and honest limits

Caching trades correctness for load, and the trade is only defensible when the staleness bound is written down and the consumers accept it. Products differ in eviction policy, persistence, and cluster behaviour, and this skill describes the mechanism rather than any product's defaults. Nothing here recommends a cache product, and a cache added without an invalidation story is a future incident with a performance graph attached.
