---
name: ac-email-deliverability
description: "Sending email that arrives: SPF and DKIM as the alignment pair, DMARC as the policy that ties them, the shared reputation that follows a domain, bounce and complaint loops that feed it back, sender identity as the thing every inbox provider actually judges, and writability list hygiene as deliverability work rather than marketing work. It explains how email authentication and reception decisions work; it never recommends a sender vendor and never guarantees inbox placement. Use when asking \"SPF\", \"DKIM\", \"DMARC\", \"email deliverability\", \"why are my emails going to spam\", \"hard bounce versus soft bounce\", \"warm up a domain\", \"email authentication\", \"10 DNS lookup limit\", \"postmaster\", \"complaint rate\". Not for application-level email drafting and tone (ac-business-writing), not for webhook processing of provider events (ac-webhook-and-async-delivery), not for DNS general mechanics (ac-network-edge-and-delivery)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Email deliverability

## Overview

Email delivery is a reputation negotiation between a sender and an inbox provider that has never met the sender's users and optimises for their complaint button. The protocol questions — is this mail really from the domain it claims, does the domain vouch for it, what happens when it fails — are answerable with DNS records and policy. The reception question — does the provider want to show it — is answered by history: bounces, complaints, spam-trap hits, and sending patterns that belong to the domain and the IP reputation behind it.

This skill covers the mechanics of that negotiation: the authentication pair and its alignment rules, the policy layer, the feedback loops a sender must operate, and the sender-side hygiene that quietly decides most of the outcome. Drafting good email is a different skill; processing provider webhooks is a different skill; this one is about getting legitimate mail accepted.

Primary sources: <https://datatracker.ietf.org/doc/html/rfc7489> and <https://support.google.com/a/answer/81126>.

## When to use

- Setting up or diagnosing SPF, DKIM, or DMARC for a sending domain.
- Handling bounces, complaints, and spam feedback loops.
- Troubleshooting why legitimate mail lands in spam or is refused.
- Establishing a new sending domain or provider.

## When NOT to use

- For writing the content and tone of an email (use ac-business-writing).
- For webhook endpoint mechanics of provider events (use ac-webhook-and-async-delivery).
- For DNS resolution and edge delivery in general (use ac-network-edge-and-delivery).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/spf-and-alignment.md` | `software-engineering/spf-and-alignment` | The envelope-from check, the include graph and its lookup budget. |
| `subskills/dkim-signing.md` | `software-engineering/dkim-signing` | Domain-signatures, key rotation, and the body-hash that breaks. |
| `subskills/dmarc-policy.md` | `software-engineering/dmarc-policy` | The policy layer, alignment, and the reports that tell the truth. |
| `subskills/reputation-and-senders.md` | `software-engineering/reputation-and-senders` | Domain and IP reputation, warm-up, and send-level hygiene. |
| `subskills/bounce-and-complaint-loops.md` | `software-engineering/bounce-and-complaint-loops` | Hard versus soft, the feedback loops, and the suppression list. |
| `subskills/list-hygiene.md` | `software-engineering/list-hygiene` | Permission, engagement decay, and the addresses that poison a domain. |
| `subskills/deliverability-record.md` | `software-engineering/deliverability-record` | The written record: DNS state, loops, thresholds, and actions taken. |

## Status and honest limits

Inbox providers publish guidelines, not rules; their filters change without notice and treat even perfect authentication as a floor, not a pass. Nothing here guarantees placement, and nothing in this skill manipulates filters — it makes a legitimate sender legible to them. DMARC reports and postmaster tools are the only observability a sender has, and both lag the events they describe.
