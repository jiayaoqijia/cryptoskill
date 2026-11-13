---
name: reputation-and-senders
domain: software-engineering/reputation-and-senders
trigger: "Understanding what inbox providers weigh when they decide placement."
anti_trigger: "Not for the DNS authentication records, and not for marketing strategy."
scope: "Domain and IP reputation, warm-up, and send-level hygiene."
status: seedling
---

# Reputation and senders

## Standard

Authentication is the floor; reputation decides the placement. Inbox providers weigh a sending identity — domain, and the infrastructure behind it — by its history: how many recipients marked it spam, how many engaged, how many never existed, and whether the sending pattern looks like a person or a firehose. The reputation belongs to the identity, not to a single campaign, which is why one bad list damages the next good one.

Warm-up is the operational consequence: a new domain, or a domain moved to new infrastructure, has no history, and the provider treats unknown quantities cautiously. Volume is ramped deliberately while the early signals — opens, replies, deletions-unread — accumulate. The send-level hygiene that follows is permanent: consistent volume, list hygiene, and content that does not trip the filters, because every spike and every new source is evaluated against what the sender has been.

Primary sources: <https://sendgrid.com/en-us/blog/what-is-email-deliverability> and <https://support.google.com/a/answer/81126>.

## Decision rules

- Treat the sending domain as an asset: the decision to add a stream is a reputation decision.
- Separate identities by intent: transactional, product, and marketing streams each get their own subdomain and their own reputation.
- Warm a new identity with ramped volume over a stated window, watching placement signals, not just delivery counts.
- Record infrastructure changes as reputation events: a new provider or IP range means partial re-warming.
- Monitor postmaster and reputation tools per provider as the only direct signals available.
- Send consistently: providers model normal volume, and a ten-fold spike is a pattern change that gets evaluated as one.

## Procedure

1. Define the sending identities and which mail classes ride each subdomain.
2. Set the warm-up window and the volume ramp for a new identity.
3. Watch early placement signals — opens, replies, spam-folder placement tests — and adjust the ramp, not just the send.
4. On any infrastructure change, plan a re-warm proportional to the change.
5. Keep postmaster accounts registered and checked on a stated cadence.
6. Record each identity's history: start date, ramp, incidents, current signals.

## Anti-patterns

- Marketing a brand-new domain at full volume on day one.
- Riding one domain for transactional and bulk mail, so a complaint spike takes the invoices with it.
- Treating an infrastructure migration as invisible to receivers.
- Watching sent counts as success while every test lands in spam.
- No postmaster registration, so the only signals are support tickets from customers.

## Done checklist

- [ ] Sending identities defined with intent separation.
- [ ] Warm-up windows and ramps stated per identity.
- [ ] Early placement signals monitored, not just delivery counts.
- [ ] Infrastructure changes planned as re-warm events.
- [ ] Postmaster tools registered and on a cadence.
- [ ] Identity history recorded.

## Sources

- Deliverability overview: <https://sendgrid.com/en-us/blog/what-is-email-deliverability>
- Sender guidelines from a major receiver: <https://support.google.com/a/answer/81126>
- DMARC reports as a cross-check on alignment and volume: <https://datatracker.ietf.org/doc/html/rfc7489>
