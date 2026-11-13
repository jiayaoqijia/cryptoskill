---
name: ac-content-addressed-storage
description: "Storing data by its content rather than its location: content addressing and what a hash address guarantees, hash algorithm choice, Merkle trees and batched verification, deduplication and what it shares, garbage collection and reference liveness, registries and how tools resolve names to digests, and the written record. It explains how a store finds data by content and how that fails; it never recommends a storage system. Use when asking \"content addressed\", \"content hash\", \"Merkle tree\", \"digest\", \"blob storage\", \"artifact registry\", \"dedupe\", \"garbage collection of blobs\", \"why is this build immutable\", \"layer dedup\", \"cas store\", \"verify by checksum\". Not for supply chain signing and provenance of artifacts (ac-software-supply-chain), not for build caching (ac-monorepo-and-build-systems), not for cache invalidation at the application tier (ac-caching-and-invalidation)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Content-addressed storage

## Overview

Most storage names data by where it lives: a path, a table row, a URL. Content-addressed storage names data by what it is: the cryptographic digest of the bytes. Two copies of the same content share one address, any change produces a new address, and a fetch can verify that what arrived is what was named. The address and the integrity check become the same operation.

The reference model this skill maps has three parts — blobs addressed by hash with metadata and annotations layered on top, a Merkle tree that makes verification proportional to what changed, and a reference graph that determines what is reachable and therefore what a garbage collector may remove. Around them sit the questions that recur in every content store: which hash algorithm to trust for what lifetime, what deduplication shares, what a registry adds to addressing, and what fetch layers and content stores each verify when a store references another by digest.

Primary sources: <https://docs.docker.com/registry/spec/api/> and <https://llvm.org/docs/>.

## When to use

- Designing or evaluating a store that addresses data by digest.
- Reasoning about deduplication, garbage collection, and reference liveness.
- Working with artifact or container registries and how tools resolve layers by digest.
- Deciding hash algorithm, verification boundaries, and replication checks for a content store.

## When NOT to use

- For signing and provenance of released artifacts (use ac-software-supply-chain).
- For build remote-caching semantics (use ac-monorepo-and-build-systems).
- For application-tier caching and TTL choices (use ac-caching-and-invalidation).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/addressing-model.md` | `software-engineering/addressing-model` | Hash as name, immutability of the address, collisions, and what addressing does not guarantee. |
| `subskills/hash-algorithm-choice.md` | `software-engineering/hash-algorithm-choice` | Cryptographic versus non-cryptographic, truncation, algorithm agility, and the multi-hash pattern. |
| `subskills/merkle-trees.md` | `software-engineering/merkle-trees` | Batched verification, partial sync, roots as checkpoints, and the cost of changing one leaf. |
| `subskills/dedup-and-isolation.md` | `software-engineering/dedup-and-isolation` | What dedup shares, cross-tenant leakage, and compression's own dedup surprises. |
| `subskills/references-and-gc.md` | `software-engineering/references-and-gc` | Reachability, roots, mark-and-sweep at the blob tier, and the race between deletion and fetch. |
| `subskills/registry-resolution.md` | `software-engineering/registry-resolution` | Tags as moving pointers, digest pinning, resumability, and concurrent manifest publication. |
| `subskills/storage-address-record.md` | `software-engineering/storage-address-record` | The written record of algorithms, root values, retention, and verification evidence. |

## Status and honest limits

Content addressing guarantees that bytes matching a digest are the bytes that were addressed — it does not guarantee those bytes were worth storing, that their source was authorised, or that whoever supplied the digest supplied the content. Weak hashes age badly, and registries mix immutable digests with mutable pointers, which is where most practical confusion begins. Every claim this skill makes about a store should be checked against that store's own specification; naming by content is a convention, and conventions vary.
