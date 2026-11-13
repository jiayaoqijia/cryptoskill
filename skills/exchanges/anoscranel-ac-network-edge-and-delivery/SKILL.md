---
name: ac-network-edge-and-delivery
description: "How traffic reaches an origin from the outside: DNS resolution and change propagation, TLS termination and certificate lifecycles at the edge, load balancer algorithms and health-driven ejection, CDN caching behaviour and cache-key design, origin shielding and stampede control at the edge, routing rules and redirects, and the written edge record. It explains how the delivery layer routes and caches; it never recommends a vendor and never promises a latency. Use when asking \"load balancer\", \"sticky session\", \"TLS termination\", \"certificate expiry\", \"CDN cache key\", \"cache-control at the edge\", \"origin shield\", \"health check ejection\", \"redirect chain\", \"DNS propagation\", \"anycast\". Not for application caching and invalidation (ac-caching-and-invalidation), not for service health endpoints and lifecycle (ac-service-lifecycle), not for network security controls (ac-security-engineer)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Network edge and delivery

## Overview

Between a user's request and an application's code sits a stack most engineers touch rarely and debug under pressure: DNS decides which address answers, a load balancer decides which instance receives, TLS terminates somewhere with a certificate that expires, and a CDN may answer entirely from a cache whose key and rules someone configured once. Each layer has its own failure modes and its own propagation delays, and the combination decides what users experience before any application code runs.

This skill covers that delivery stack: DNS changes and their propagation properties, TLS termination and certificate renewal at the edge, load balancer behaviour including health-driven ejection and session affinity, CDN cache keys and cache-control at the edge, origin shielding as stampede control, and redirect chains. Application-level caching belongs elsewhere; this is the layer that answers before the application does.

Primary sources: <https://developer.mozilla.org/en-US/docs/Web/HTTP> and <https://www.rfc-editor.org/>.

## When to use

- When designing or debugging how requests reach an origin.
- When a DNS or certificate change is planned and timing matters.
- When a CDN is serving wrong or stale content and the cause is at the edge.
- When load balancer behaviour — affinity, ejection, draining — affects correctness.

## When NOT to use

- For application cache correctness and TTL choices (use ac-caching-and-invalidation).
- For service health endpoints and shutdown draining (use ac-service-lifecycle).
- For network security controls and segmentation (use ac-security-engineer).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/dns-and-propagation.md` | `software-engineering/dns-and-propagation` | Resolution order, TTLs, and how fast a change becomes universal. |
| `subskills/tls-termination.md` | `software-engineering/tls-termination` | Where TLS ends and what the certificate lifecycle costs. |
| `subskills/load-balancer-behaviour.md` | `software-engineering/load-balancer-behaviour` | Algorithms, health ejection, and session affinity. |
| `subskills/cdn-cache-keys.md` | `software-engineering/cdn-cache-keys` | What the key includes, what vary means, and why keys drift. |
| `subskills/origin-shielding.md` | `software-engineering/origin-shielding` | Controlling origin load and stampede at the edge. |
| `subskills/redirects-and-routing-rules.md` | `software-engineering/redirects-and-routing-rules` | Chains, loops, and the rules layer at the edge. |
| `subskills/edge-record.md` | `software-engineering/edge-record` | The written record of the delivery configuration. |

## Status and honest limits

Edge services differ in defaults, terminology, and the exact knobs they expose; the concepts here are shared but the flag names are not, and a configuration recorded against one provider does not transfer verbatim to another. Nothing here recommends a vendor. Propagation at the DNS layer is bounded by TTLs others set, so a change is never fully under the changer's control, and the honest record states what was requested rather than claiming what the world has already accepted.
