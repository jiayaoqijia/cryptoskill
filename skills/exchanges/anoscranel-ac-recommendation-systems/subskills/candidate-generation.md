---
name: candidate-generation
domain: software-engineering/candidate-generation
trigger: "Building the cheap first stage that decides what the scorer ever sees."
anti_trigger: "Not for the scoring model, and not for vector index internals."
scope: "Cheap recall sources whose union is the judge of coverage."
status: seedling
---

# Candidate generation

## Standard

The scorer can only rank what candidate generation hands it, so the first stage is where coverage lives and where the ceiling is set. No amount of scoring sophistication can surface an item that no retriever fetched. The stage earns its keep through recall: a union of cheap sources — collaborative neighbourhoods from item and user co-occurrence, content similarity from embeddings or tags, popularity within the user's segment, co-purchase and co-view graphs — each tuned to answer "what should plausibly be considered for this user" rather than "what is good".

The union, not any single source, is the design's defence. Each retriever has blind spots — collaborative fails on new items, content-based fails on unseen tastes, popularity is blind to the individual, co-occurrence trails the catalogue's own structure — and their union covers more of the space than any one alone. The stage is then judged on recall against a ground truth: for interactions that actually happened, did the union contain the interacted item? A union that misses the very items users eventually interacted with will quietly cap the end-to-end system while the scorer experiments on the middle of the funnel.

Primary sources: <https://en.wikipedia.org/wiki/Recommender_system> and <https://en.wikipedia.org/wiki/Content-based_filtering>.

## Decision rules

- The union's recall against realized positive interactions is the stage's primary metric.
- Each source's blind spots are known and named; new-item signals exist before they are needed, not as a later retrofit.
- Source quotas and the dedupe-and-merge rule are explicit; if the union is dominated by one source, deduped quota is data.
- All sources through the same user-item context boundaries as the scorer: language, region, eligibility, availability.
- The recall-per-category and quota-per-category cut is possible, because the failure mode is rarely uniform across the catalogue.
- Retriever latency is budgeted explicitly, and slipping stages block bail-out rather than being silently hidden by caching.

## Procedure

1. Inventory the space as one query per user per surface; name the latency budget.
2. List the cheap signals available with their failure modes: collaborative, content, popularity, co-occurrence.
3. Combine with nominal quotas and dedupe; record what got dropped from each quota.
4. Build the recall test: realized positive interactions; count the times the union contained them.
5. Evaluate the recall by category; widen or shrink sources based on coverage, not on scorer feedback.
6. Connect the coverage evaluation to the shard's eligible inventory, and treat the drop count as a first-class metric.

## Anti-patterns

- A single glamorous embedding-based source of truth where new items never surface.
- Quota starvation by a tuned popularity source, with no record of what got dropped.
- Retriever latency invisible because the expensive scorer's endpoint hides it; budget stage-level.
- Evaluating the scorer on the union's output without tracking what the union excluded it from.
- Recall tuning targets the best cases rather than the modal case.

## Done checklist

- [ ] Latency budget per source, honoured end to end.
- [ ] Blind spots named per source; no single-source dependency.
- [ ] Explicit quotas and dedupe rules.
- [ ] Recall measured against realized positive interactions.
- [ ] Category-level recall visible.
- [ ] Dropped-candidate counts recorded.

## Sources

- Recommender system overview: <https://en.wikipedia.org/wiki/Recommender_system>
- Content-based filtering: <https://en.wikipedia.org/wiki/Content-based_filtering>
- Collaborative filtering: <https://en.wikipedia.org/wiki/Collaborative_filtering>
