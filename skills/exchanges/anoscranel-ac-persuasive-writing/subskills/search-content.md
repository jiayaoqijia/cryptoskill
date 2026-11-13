---
name: search-content
domain: writing/search-content
trigger: "\"write for search\", \"get cited by ChatGPT\", \"E-E-A-T\", \"answer engine optimization\", \"make this page citable\"."
anti_trigger: "A page written to convert a visitor (subskills/marketing-copy.md); site engineering, schema markup or crawl configuration; feed posts (subskills/social-posts.md)."
scope: "Search- and answer-engine-facing pages: intent, E-E-A-T, citability"
status: "seedling"
---

# Search content

## Standard

- **Intent first, then the answer.** Phrase the brief as a real question, lead with a direct 40–60-word answer (<https://blog.hubspot.com/marketing/answer-engine-optimization>). Then expand under contextual subheadings.
- **E-E-A-T is a rater framework, not a ranking factor.** Google states trust matters most and that "E-E-A-T itself isn't a specific ranking factor" (https://developers.google.com/search/docs/fundamentals/creating-helpful-content, updated 2026-10-05). Self-assess who, how and why, and disclose where a reader would ask "How was this created?"
- **There are no extra requirements for AI answers.** "There are no additional requirements to appear in AI Overviews or AI Mode, nor other special optimizations necessary" (https://developers.google.com/search/docs/appearance/ai-features, updated 2025-12-10). The page must be indexed and eligible for a snippet.
- **Volume without value violates policy.** Generating "many pages without adding value for users may violate Google's spam policy on scaled content abuse" (https://developers.google.com/search/docs/fundamentals/using-gen-ai-content, updated 2026-10-01). Method is neutral; intent to manipulate is not.
- **A citation is a fresh draw, not a position held.** Across four independent longitudinal datasets, roughly two-thirds of cited URLs are replaced within four weeks. The identical cited set recurs only 0.06% of the time on ChatGPT and never above 2.5% on any engine (<https://matthewbertram.com/blog/ai-answer-variance-study>).
- **The durable asset is the entity, not the citation.**
 Brand-name presence agrees across repeat asks at 0.832 while citation lists agree at 0.309. ⚠️ Source not cited inline; check the Sources list before relying on this figure.

## Decision rules

1. Answer the question in the first paragraph; the answer is quotable without the page around it.
2. Name an author, a date and a review process. Fabricated author profiles are "a form of deception".
3. Add data, quotes and outbound citations; each claim carries a checkable source, and the entity footprint grows off-site — LinkedIn, YouTube, PR, reviews.
4. Report AI visibility as a distribution, never a single run. One measurement carries a 95% interval of about ±33 points; 7–8 repeats bring it to about ±10.
6. Treat "citations compound into a moat" as unsupported.

## Procedure

1. List the 10–20 priority prompts, written as a reader would ask them.
2. Draft the direct answer first, then the evidence sections beneath it.
3. Attach attribution: named author, publication date, review note, sources linked.
4. Add first-party data points no competitor restates; mark estimates as estimates.
5. Verify every number, version and date against a primary source; log the check.
6. Review the metadata as carefully as the body: title, description, structured data, alt text.
7. Track citation rate, quote versus paraphrase and position in the answer across repeated runs. **The human publishes.**

## Anti-patterns

- Keyword-led copy with no answer in the first paragraph.
- Unnamed, undated, unreviewed content claiming authority.
- A single AI-visibility number reported as a score.
- Near-identical pages with uniqueness gates as the excuse.
- A vendor citation figure restated without its statistic.

## Done checklist

- [ ] Priority prompts listed and answered directly.
- [ ] Direct answer of 40–60 words leads each section.
- [ ] Named author, date and process present.
- [ ] Every number verified against a primary source.
- [ ] Metadata reviewed by a human.
- [ ] Visibility measured across repeated runs.
- [ ] **Human-gated:** published by a named person.

## Sources

- <https://blog.hubspot.com/marketing/answer-engine-optimization>
- <https://matthewbertram.com/blog/ai-answer-variance-study>
- https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- https://developers.google.com/search/docs/appearance/ai-features
