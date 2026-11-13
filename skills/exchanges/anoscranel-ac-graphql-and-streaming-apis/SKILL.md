---
name: ac-graphql-and-streaming-apis
description: "Designing GraphQL schemas and streaming interfaces that stay fast: schema shape and nullability, the N+1 problem and dataloader batching, query depth and cost limits, federation across services, pagination with cursors, subscriptions and server-sent events, and the written interface record. It explains how these interfaces behave under load; it never recommends a framework and never guarantees a latency. Use when asking \"GraphQL schema design\", \"N+1 queries\", \"dataloader\", \"query depth limit\", \"GraphQL federation\", \"cursor pagination\", \"subscription versus SSE\", \"why is my GraphQL slow\", \"query cost analysis\". Not for REST resource and versioning decisions (ac-api-design), not for event-driven messaging between services (ac-event-driven-architecture), not for transport security and injection (ac-security-engineer)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# GraphQL and streaming APIs

## Overview

GraphQL and streaming interfaces invert control: the client decides what it wants and the server must satisfy that request without knowing in advance what it will be. That flexibility is the attraction and the problem. A schema that permits arbitrary traversal permits expensive queries; a subscription that delivers every change delivers too many; and a resolver that looks trivial becomes a fan-out when the client asks for a list.

This skill covers the mechanics that make those interfaces work: how schema shape and nullability constrain clients, why the N+1 pattern appears and how batching addresses it, how depth and cost limits bound a query before it runs, how federation splits a graph across teams, how cursor pagination stays stable, and where subscriptions differ from server-sent events. REST contracts and event messaging belong to other skills.

Primary sources: <https://graphql.org/> and <https://www.w3.org/>.

## When to use

- When designing or reviewing a GraphQL schema.
- When a GraphQL endpoint is slow and the cause is suspected to be resolver fan-out.
- When splitting a graph across services or teams.
- When choosing between subscriptions and server-sent events.

## When NOT to use

- For REST resource modelling and versioning (use ac-api-design).
- For service-to-service messaging and event schemas (use ac-event-driven-architecture).
- For authentication, injection, and abuse controls (use ac-security-engineer).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/schema-shape-and-nullability.md` | `software-engineering/schema-shape-and-nullability` | Types, nullability, and the client behaviour each choice forces. |
| `subskills/n-plus-one-and-batching.md` | `software-engineering/n-plus-one-and-batching` | Resolver fan-out, dataloader batching, and the request-scoped cache. |
| `subskills/query-cost-and-depth.md` | `software-engineering/query-cost-and-depth` | Depth limits, cost analysis, and rejecting expensive queries before execution. |
| `subskills/federation-and-schema-ownership.md` | `software-engineering/federation-and-schema-ownership` | Splitting a graph across teams without creating a distributed monolith. |
| `subskills/cursor-pagination.md` | `software-engineering/cursor-pagination` | Stable cursors, ordering, and why offset pagination breaks. |
| `subskills/subscriptions-and-sse.md` | `software-engineering/subscriptions-and-sse` | Push transport choice, delivery guarantees, and reconnection. |
| `subskills/graphql-interface-record.md` | `software-engineering/graphql-interface-record` | The written record: schema, limits, cost model, and ownership. |

## Status and honest limits

GraphQL tooling changes faster than the principles, and a specific server library's behaviour may differ from the general pattern described here. Cost analysis is an approximation of database work and never an exact bound, so limits reject the obviously expensive rather than the truly expensive. Nothing here guarantees a latency, and a schema that is well designed can still be slow if the resolvers behind it are.
