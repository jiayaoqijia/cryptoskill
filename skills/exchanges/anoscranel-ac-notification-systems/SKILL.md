---
name: ac-notification-systems
description: "Sending notifications to your users' own channels: the notification as a routed artefact rather than an email, channel selection and the fan-out across email, push, in-app and SMS, delivery receipts and the retry paths that differ per channel, quiet hours and user preference as routing inputs, templates with per-channel context, digest and batch policies that respect attention, and the written notification record. It explains how a notification platform behaves; it never recommends a vendor and never decides how often to interrupt a user. Use when asking \"notification system\", \"push notification\", \"in-app notification\", \"fan out\", \"notification preferences\", \"quiet hours\", \"digest\", \"read receipts\", \"cross-channel notification\", \"why did users turn off notifications\". Not for mobile push implementation on one platform (ac-mobile-client-engineering), not for webhook delivery to endpoints you do not own (ac-webhook-and-async-delivery), not for email deliverability mechanics (ac-email-deliverability)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Notification systems

## Overview

A notification is a routed artefact: one event becomes several channel-specific deliveries — email, mobile push, in-app badge, SMS — each through an API with its own failure modes, retry conventions, and idempotency expectations. That fan-out has to be designed, not discovered platform by platform, because the phenomena that hurt are cross-channel: the same event delivered more than once across channels, a 3am reset token written as a marketing-tuned push, and the user who turns off the whole system because one stream interrupted too much.

This skill covers the routing and delivery layer as a system: what a notification is as data, how fan-out renders it per channel, the delivery/retry semantics of each transport, the preference and attention model that decides when not to send, and the batching/digest policies that reduce interruption while preserving meaning. Single-channel plumbing (mobile push, webhooks, email authentication) belongs with their respective skills; this one handles the layer above them.

Primary sources: <https://developer.mozilla.org/en-US/docs/Web/API/Push_API> and <https://developer.apple.com/documentation/usernotifications>.

## When to use

- Designing a notification service across two or more channels.
- Defining what causes a notification and when it should not send.
- Handling delivery receipts and channel-specific retry semantics.
- Designing digest, batching, and attention policies.

## When NOT to use

- For implementing mobile push registration and display on the device (use ac-mobile-client-engineering).
- For delivering webhooks to external endpoints (use ac-webhook-and-async-delivery).
- For email deliverability mechanics like SPF/DKIM (use ac-email-deliverability).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/anatomy-and-events.md` | `software-engineering/anatomy-and-events` | The notification as data: event, recipient, template, and channels. |
| `subskills/fan-out-across-channels.md` | `software-engineering/fan-out-across-channels` | One event, many transports, and their differing contracts. |
| `subskills/delivery-receipts.md` | `software-engineering/delivery-receipts` | Receipts as facts, idempotency pre-send, and retry discipline. |
| `subskills/channel-policies.md` | `software-engineering/channel-policies` | Which channel carries what, by urgency and content. |
| `subskills/user-preferences-and-attention.md` | `software-engineering/user-preferences-and-attention` | Permission, quiet hours, batching windows, and not sending. |
| `subskills/digest-and-batching.md` | `software-engineering/digest-and-batching` | When many events must become one interruption. |
| `subskills/notification-record.md` | `software-engineering/notification-record` | The written record of routing, policies, and outcomes. |

## Status and honest limits

Notification platforms are thin layers over vendor-specific transports whose contracts differ and whose failure modes are drowned in per-provider dashboards. This skill describes the shared design space: the transports are inputs, not recommendations, and the channel-specific code details belong to their own skills. Nothing here should decide how often to interrupt a user; that is a product decision captured as a policy, and the code's job is only to enforce what the policy records.
