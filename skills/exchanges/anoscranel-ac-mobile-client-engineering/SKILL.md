---
name: ac-mobile-client-engineering
description: "Building and shipping mobile clients under constraints the web does not have: app release cycles and store review latency, offline-first state and conflict resolution, forced upgrade and version skew across installed bases, network and battery budgets, push delivery and deep links, device and OS fragmentation, and the written release record. Use when asking \"app store review\", \"offline first\", \"force upgrade\", \"deep link\", \"version skew clients\", \"mobile release train\", \"push notification delivery\", \"why is the old app version still calling the API\". Not for responsive web layout and WCAG (ac-frontend-ui), not for API contract evolution (ac-api-design), not for CI pipeline wiring (ac-ci-and-release)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Mobile client engineering

## Overview

A mobile client is software you cannot roll back. The build that ships sits on devices you do not control, behind a store review you do not schedule, and stays installed for years after you stop supporting it. That single fact reshapes every engineering decision that follows: the release becomes a staged rollout rather than a deployment, the API must serve several client versions at once, and the state on the device must survive being offline for a week.

This skill covers the disciplines that follow from that constraint: the release train and review latency, offline-first state and the conflict resolution it forces, forced-upgrade policy and version skew, the budgets for network and battery, push and deep-link delivery, and the fragmentation of devices and OS versions. Responsive web and API contract design belong to other skills.

Primary sources: <https://developer.android.com/> and <https://developer.apple.com/>.

## When to use

- When planning a mobile release and its rollout stages.
- When designing state that must work offline and reconcile later.
- When a client version must be retired or forced to upgrade.
- When push, deep links, or device fragmentation affect behaviour.

## When NOT to use

- For responsive layout and WCAG conformance (use ac-frontend-ui).
- For API contract evolution and versioning (use ac-api-design).
- For CI pipelines, canaries, and release automation (use ac-ci-and-release).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/release-train-and-review.md` | `software-engineering/release-train-and-review` | Store review latency, staged rollout, and the release that cannot be recalled. |
| `subskills/offline-first-state.md` | `software-engineering/offline-first-state` | Local persistence, sync, and conflict resolution when the device was offline. |
| `subskills/version-skew-and-upgrade.md` | `software-engineering/version-skew-and-upgrade` | Supporting several client versions, and the forced-upgrade decision. |
| `subskills/network-and-battery-budgets.md` | `software-engineering/network-and-battery-budgets` | Data, latency, and power budgets on a device you do not control. |
| `subskills/push-and-deep-links.md` | `software-engineering/push-and-deep-links` | Delivery guarantees, tokens, and links that must survive install. |
| `subskills/fragmentation-and-devices.md` | `software-engineering/fragmentation-and-devices` | OS versions, screen classes, and hardware capability tiers. |
| `subskills/mobile-release-record.md` | `software-engineering/mobile-release-record` | The written record: versions in the field, rollout state, and upgrade policy. |

## Status and honest limits

Store policies, review times, and platform APIs change without notice, and a technique that works on one platform may be unavailable on another. Nothing here substitutes for reading the current platform documentation. This skill also cannot tell you what your installed base looks like: the version distribution, device mix, and network conditions are measurements you have to take, and every decision here depends on them.
