---
name: retrieval-cascade
domain: research-operations/retrieval-cascade
trigger: "\"go fetch this evidence\", \"search for sources on X\", \"which API do I use\", \"the search is rate-limited, now what\"."
anti_trigger: "Grounding a load-bearing answer with mandatory citations through the conditional Google tier (subskills/grounded-tier.md); grading what the search returns (subskills/source-triage.md)."
scope: "Executing retrieval keyless-first: specialist sources, cascade order, pacing, retry states and keyed escalation"
status: "seedling"
---

# Retrieval through the keyless-first cascade

## Standard

The cascade below fixes the order. Burn the free, strong
legs before any paid one:

1. Domain specialists first whenever the domain has one: papers through the
 scholarly indexes, code through the code hosts, models through the model
 hub. A specialist beats a general engine in its own domain.
2. Built-in quick search for one-hop facts.
3. Keyless link-discovery engines for research fan-out.
4. Keyless direct APIs for bulk: more than about ten queries goes to the JSON
 APIs, not the search pages.
5. Keyed tiers only after the keyless layer is genuinely exhausted.
6. A real headless browser is the escape hatch for JS-walled pages, paced
 at roughly one query every few seconds against shared carrier IPs.

The rate-limit retry rule is binding: a 429 or throttle means wait
5-15 minutes and retry first, because per-IP quotas often reset when the
carrier assigns a fresh egress IP. Fall through to a keyed tier only after a
retried limit still holds. The academic substrate's live-tested rate caps
(PubMed 3 req/s unkeyed, OpenAlex 100k credits/day, per-engine walls) are worth
checking before a bulk run.

## Decision rules

- Recall-critical retrieval (a missed source invalidates the study) means
 multiple source families, never one engine. No single index is complete
 (PRISMA-S item 1).
- One fact, one lookup. Do not fan the cascade for a one-hop answer.
- Bulk and repetition go to APIs with pacing; pages are for discovery.

## Procedure

1. Match the domain to its specialist source first.
2. Run the keyless search legs; capture lineage per result.
3. Fetch surviving candidates; archive each source verbatim on disk as it
 lands, never at the end.
4. On a throttle, wait and retry before any keyed escalation; log the state.
5. Log each fetch: tier used, time, and outcome. The log feeds the ledger.

## Anti-patterns

- Opening with the keyed tier while keyless legs stand.
- Machine-gun bursts against a shared egress IP.
- Falling through on the first 429 without the wait-and-retry.
- Fetching everything and archiving nothing until the end.

## Done checklist

- Every fetch names its tier.
- Every throttle got its wait-and-retry before escalation.
- Every retrieved source is on disk the moment it is retrieved.

The cascade's cost is also a variable worth recording: a query answered at the first tier costs seconds, one that reaches the fourth costs minutes, and a plan that assumes the cheap tier will succeed will overrun whenever it does not. Recording the tier that actually produced the answer is what makes the next plan's budget honest.

## Sources

- <https://training.cochrane.org>
- <https://osf.io/prereg/>
