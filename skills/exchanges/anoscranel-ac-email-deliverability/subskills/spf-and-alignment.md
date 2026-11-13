---
name: spf-and-alignment
domain: software-engineering/spf-and-alignment
trigger: "Setting up or diagnosing the SPF record and its include chain."
anti_trigger: "Not for DKIM signing, and not for DNS hosting in general."
scope: "The envelope-from check, the include graph and its lookup budget."
status: seedling
---

# SPF and alignment

## Standard

SPF answers a narrow question from the receiving side: is this connection, from this IP, authorised to use this envelope-from domain? The answer comes from a DNS TXT record: a list of mechanisms — ip4, ip6, include, mx — that the receiver evaluates against the connecting IP. The check is on the envelope sender, the bounce address the mail is really from, not the visible header address a human reads; the two can differ, and the difference is exactly what the alignment rules in DMARC referee.

The structural limit is the ten-lookup budget. Each include mechanism means the receiver must fetch and evaluate another domain's record, and the whole evaluation fails with a permanent error once ten DNS lookups are consumed. Senders accumulate includes — the corporate platform, the billing system, the support desk — until the graph silently exceeds the limit and every evaluation after the tenth mechanism returns none, which is a failure the sender caused.

Primary sources: <https://datatracker.ietf.org/doc/html/rfc7208> and <https://en.wikipedia.org/wiki/Sender_Policy_Framework>.

## Decision rules

- Record which platforms legitimately send as the domain, before writing mechanisms.
- Prefer explicit ip4 or ip6 blocks over nested includes where the addresses are known and stable.
- Count the lookup walk: every include — not every mechanism — consumes budget; keep the total under ten.
- End with a default policy; all is a declaration, ~all is a softened one, and the choice is a stated position on unknown senders.
- Verify with an independent checker that walks the graph and reports both the result and the lookup count.
- Re-verify after any provider change; a vendor's record change alters the walk without the sender touching DNS.

## Procedure

1. Inventory every system that sends mail as the domain, direct or through a provider.
2. Draft the mechanisms; pull each provider's published include target and count the walk.
3. Add the default policy and publish the TXT record.
4. Run an independent evaluation that reports the result and the lookup count.
5. Record the walk — mechanisms, lookups, result — with the date.
6. Re-verify on any provider, DNS, or architecture change.

## Anti-patterns

- Publishing an include chain that walks over ten lookups, then blaming receivers.
- Adding mechanisms defensively without inventorying who actually sends.
- Restricting all soft enough that forwarding breaks silently, or hard enough to learn from the bounce logs.
- Assuming the header From was checked; SPF sees the envelope.
- Checking the record once and never re-testing after provider changes.

## Done checklist

- [ ] Senders inventoried before mechanisms written.
- [ ] Include walk counted and under ten.
- [ ] Default policy stated deliberately.
- [ ] Independent checker reports result and count.
- [ ] Walk recorded with the date.
- [ ] Re-verification on provider change scheduled via the record.

## Sources

- RFC 7208, the SPF specification: <https://datatracker.ietf.org/doc/html/rfc7208>
- The alignment context: <https://datatracker.ietf.org/doc/html/rfc7489>
- Overview of the record and its limits: <https://en.wikipedia.org/wiki/Sender_Policy_Framework>
