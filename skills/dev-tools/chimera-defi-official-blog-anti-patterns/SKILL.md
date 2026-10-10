---
name: blog-anti-patterns
description: Use this skill when writing, editing, reviewing, or auditing a blog post or long-form article for this project (frontend/app/blog/*, docs/blog/*, the docs/*.md mirrors of the bake-off write-ups). It is a checklist of common software-blogging anti-patterns, each with the fix, plus a short before/after example. Trigger it before drafting a new post, before rewriting an existing one, and when ranking posts by how much they need work.
---

# Blog Anti-Patterns

A checklist for software blog posts, distilled from Michael Lynch's
[Anti-Patterns in Software Blogging](https://refactoringenglish.com/blog/anti-patterns-software-blogging/)
(Refactoring English, 2026-10-07). The wording here is ours. The article is the source.

The reader has a billion other things to read. Each check asks one question: does this
make the reader do work they did not sign up for?

## The checklist

Run every check against the title and the first three sentences first, then the body.

1. **Meandering intro.** Backstory, history or setup comes before the reason to read.
   - *Test:* after the title and three sentences, can a reader answer "is this for someone
     like me?" and "what do I get from it?"
   - *Fix:* lead with who it is for and the payoff (a technique, an answer, a number, a
     story). Move the backstory down or cut it.

2. **Preamble in the reader's path.** A subtitle, byline block, epigraph, banner image,
   callout or table of contents sits between the title and the first real sentence.
   - *Test:* count the things a reader passes before the opening paragraph.
   - *Fix:* each one spends the reader's attention. Keep only what earns its place; push
     the rest below the opening.

3. **"The reader knows everything I know."** Jargon, acronyms and internal names
   (flag names, ticket numbers, lab hostnames, campaign codenames) appear undefined.
   - *Test:* pick a real reference reader (e.g. "runs one validator at home, has never read
     our repo"). List the terms they would and would not recognise, then reread the post
     as them.
   - *Fix:* define a term in a short clause the first time it appears, compare it to
     something familiar, or replace it with a plain description. Drop internal names the
     reader never needs.

4. **Links doing the explaining.** A term is "explained" only by a hyperlink to a long
   page, or the post sends the reader to another article to follow the argument.
   - *Test:* could the target reader understand the whole post without clicking anything
     or hovering for a tooltip?
   - *Fix:* summarise the one or two sentences the reader needs inline. Keep the link as a
     bonus for going deeper, not as a prerequisite.

5. **Sequel injection.** The post opens by assuming the reader read a previous post
   ("in part one", "as we saw last time", "the companion article explains").
   - *Test:* would the opening make sense to someone landing from a search engine?
   - *Fix:* make the post stand alone. Summarise what matters from the earlier post in a
     sentence or two, and move cross-references to the end.

6. **Excessive formality.** Passive voice, inflated words ("utilised", "in order to",
   "it should be noted that"), stacked hedges, report-speak.
   - *Test:* read a paragraph aloud. Would you say it that way to a colleague?
   - *Fix:* write the way you talk. Active voice, short words, a person doing a thing.
     Personality is welcome; bland, uniform prose reads as machine-written.

7. **Broken on mobile.** A wide table, code block, chart or long unbroken string forces
   sideways scrolling of the whole page.
   - *Test:* view the page in the browser's mobile/responsive mode at ~375px.
   - *Fix:* wrap or scroll wide elements inside their own box; never let them widen the
     page.

8. **Hard-to-read text.** Low-contrast colour pairs (grey on grey), tiny or ornate fonts.
   - *Test:* run the browser's accessibility/contrast checker.
   - *Fix:* raise contrast; use a plain, legible font.

Checks 7 and 8 are about rendering, so they apply to the published page, not to a
markdown draft. Note them when auditing a TSX page; skip them for a `.md` draft.

## Project-specific rules that sit on top

- **Accuracy beats flow.** Never add a number, date or command to make a sentence punchier.
  Every measured figure must match `docs/CLIENT_BAKEOFF_RESULTS.md` (the arbiter), and a
  disk figure must say which lifecycle phase it was measured at (see `AGENTS.md`).
- **Edit in place.** When a claim is wrong, rewrite the sentence. Do not bolt on a
  correction paragraph after it.
- **Lean beats complete.** If a section serves a different reader (harness internals,
  raw logs, campaign history), cut it and link to the page that owns it, at the end.
- **A rewrite subtracts.** Add no new fact unless it answers a question the reader would
  ask; incident trivia (which run, which host, why a rerun happened) stays on the
  results page.
- **Fact-check passes bloat; re-cut after them.** Each accuracy fix tends to add a qualifier
  or a sentence. Make the qualifier a clause, and if a claim needs a long hedge or has no
  source (market share, "our best explanation"), cut the claim. Word count should usually
  end lower, but phase labels, versions and scope qualifiers ("as we ran it") are exempt:
  never cut one to hit a length. Fact-check the cut version too, because trimming drops
  exactly those: "the same tiers held" trimmed to "the same order held" claims more.

## Before and after

Before (meanders, assumes context, leans on a sequel and a link):

> This is the second post in our series. As described in the companion write-up, the
> campaign utilised the EXP-A protocol on `exp-lab` to evaluate restart behaviour across
> the CL constant, and results are summarised [here](#).

After (who it is for and the payoff, in plain words, standing alone):

> Running an Ethereum node at home? We restarted clients mid-sync on one machine to see
> which pick up where they left off and which start over. Here is what each one did, and
> how long you wait before it is back in sync.

(Illustrative only. In a real post, every figure behind a sentence like this must come
from the arbiter.)

## How to audit with this

For each post, score each of checks 1–6 as 0 (clean), 1 (minor) or 2 (bad), cite one
line as evidence for every non-zero score, and add the scores, counting checks 1–3 double
because they lose readers earliest. Note checks 7–8 separately for rendered pages. The
highest total benefits most from a rewrite.
