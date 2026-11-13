---
name: ac-cost-aware-engineering
description: "Treating running cost as a design constraint rather than an afterthought: unit economics per request and per tenant, the cost drivers that dominate at scale, storage and egress and their tiers, cost attribution and tagging, the build-versus-buy line where cost crosses, budget alarms that act rather than notify, and the written cost record. Use when asking \"cloud cost\", \"FinOps\", \"cost per request\", \"egress cost\", \"cost attribution\", \"why is our bill so high\", \"cost per tenant\", \"storage tiering\", \"reserved capacity\", \"cost as a non-functional requirement\". Not for performance profiling and latency (ac-performance), not for capacity measurement and headroom (ac-chaos-and-capacity-testing), not for vendor contract negotiation."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Cost-aware engineering

## Overview

Running cost is a property of the architecture, and it is decided early whether or not anyone decides it deliberately. A design that stores every event forever, calls a managed service per request, or moves data across regions has chosen a cost profile, and the choice is invisible until the invoice arrives at scale.

This skill covers the engineering of that constraint: how to compute unit economics rather than totals, which drivers dominate as volume grows, how storage and egress pricing shapes design, how attribution makes a cost visible to the team that causes it, where building becomes cheaper than buying, and how a budget alarm becomes an action rather than a notification. Performance and capacity measurement belong to other skills.

Primary sources: <https://www.finops.org/> and <https://www.cncf.io/>.

## When to use

- When designing a system whose cost will scale with usage.
- When a bill has grown faster than the traffic that justifies it.
- When attribution is needed to make a cost actionable.
- When evaluating whether to build a component or buy it.

## When NOT to use

- For latency and profiling work (use ac-performance).
- For capacity headroom measurement (use ac-chaos-and-capacity-testing).
- For contract negotiation and vendor pricing terms (outside engineering).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/unit-economics.md` | `software-engineering/unit-economics` | Cost per request, per tenant, and per unit of business value. |
| `subskills/cost-drivers-at-scale.md` | `software-engineering/cost-drivers-at-scale` | What dominates as volume grows, and what does not. |
| `subskills/storage-and-egress.md` | `software-engineering/storage-and-egress` | Tiers, retention, and the transfer costs that surprise. |
| `subskills/cost-attribution.md` | `software-engineering/cost-attribution` | Tagging, shared-cost allocation, and making a cost visible to its owner. |
| `subskills/build-versus-buy.md` | `software-engineering/build-versus-buy` | The volume at which building beats buying, and the costs both hide. |
| `subskills/budget-alarms.md` | `software-engineering/budget-alarms` | Alarms that trigger an action rather than a notification. |
| `subskills/cost-record.md` | `software-engineering/cost-record` | The written record: unit cost, drivers, attribution, and trend. |

## Status and honest limits

Pricing is vendor-specific, changes without notice, and is frequently discounted in ways that make list prices a poor guide to actual spend. The engineering principles here are stable; the numbers are not, and every figure in a cost record should carry its date and its source. Nothing here substitutes for reading a current price list, and a unit cost computed from list prices can be wrong by a large factor against a negotiated bill.
