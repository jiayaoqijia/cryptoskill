---
name: ai-tool-evaluation
description: Use when judging an AI tool for adoption.
version: 1.0.0
author: Hermes Agent
license: MIT
triggers:
  - legit ga buat dicoba
  - scam atau legit
  - competitor ai agent
  - mana yang worth dipakai
  - tool ai mana yang bagus
metadata:
  hermes:
    tags: [research, vetting, ai-products, decision]
    related_skills: [analyst-claim-verification, agent-marketplace-selling, external-skill-adoption]
---

# Vetting an AI product before adopting it

Answers three questions with evidence: is this thing real, who else does it, and which one should he
actually use now. The output is a decision, not a feature roundup.

## When to Use

Do sends a product link or name and asks "legit ga buat dicoba", "ini bakal scam?", "ada competitor lain?",
"mana yang worth gw pakai skrg". Also when a tool is already in use and he asks whether to keep it.

Not for installing a third-party skill bundle into Hermes → `external-skill-adoption`. Not for marketplace
selling mechanics → `agent-marketplace-selling`. Not for DeFi protocol risk → `defi-platform-due-diligence`.

## Step 0 — Open-source repo: provenance before prose

When the link is a repository rather than a company, the first call is `gh api repos/<owner>/<name>`; it returns
owner org, `created_at`, `pushed_at`, `stargazers_count`, `forks_count`, `license`, `has_issues`, and size in one
response. Pull `gh api repos/<owner>/<name>/commits | length` too, because commit count is the substance figure.

Read stars per day against commit count, not stars alone. Six thousand stars on a one-commit, one-day-old repo is
attention, not adoption, and the verdict sentence should say exactly that: hype is a fact about the idea, the
commit graph is the fact about the code. Also check `has_issues: false` (no public bug record) and whether the
repo is a bundle for a separate host product — if it is, run `npm view <host-pkg> dist-tags versions` to see
whether that host is actually published, still on `rc`/`alpha`, and therefore whether "just try it" is honest.

Separate three claims in the answer: the org is real and the repo exists (verifiable), the design idea is
interesting (arguable), the code is proven (usually not, at this age). Never let the first carry the third.

## Step 1 — Entity and money, before features

Find, in this order: the legal entity, the founder's own site/LinkedIn, the YC or accelerator page, and news
coverage of the raise.

The floor for "not a scam": a named legal entity, a founder whose identity is consistent across LinkedIn,
personal site and accelerator page, a lead investor, and a privacy policy you can read. No entity + no policy
+ payment demanded up front is where you stop and say avoid.

Write the funding line as stage + amount + lead, not as a compliment. Raised a lot is not survived: a $6M seed
competing with a $1B war chest is a different risk than a $6M seed in an empty category, and the reader needs
the difference.

## Step 2 — Read the product's own docs, not the landing page

Open the pricing page, the docs/plans page, and the privacy policy. They routinely disagree, and the
disagreement is the signal: a pricing page advertising a paid tier while the docs say paid subscriptions are
not currently offered dates the company's phase better than any interview.

Read generosity the same way. A very large free allowance (hundreds of messages a day, "almost unlimited") is
seasonal: it is investor money buying growth, and pricing arrives later. Say that in the verdict instead of
presenting the free tier as a stable cost.

## Step 3 — Map the data exposure

List what the product can connect, and for each: read-only or write, can it move money, can it send mail on his
behalf, how is access revoked, is data used for training, does deletion actually delete.

Keep two sentences separate: "technically cannot move money" describes the plumbing; "company is trustworthy"
describes the company. The first is verifiable from docs, the second is not, and blending them is how a young
vendor gets sold as safe.

## Step 4 — Build the competitive map before recommending

Any consumer AI category worth entering now has three layers, and the recommendation depends on all three:

1. **Funded independents** — same category, with raise and valuation.
2. **Consolidation** — acquisitions, because an acquired product's roadmap is no longer the product's.
3. **Platform owners** — Meta, Apple, OpenAI, Google. They do not launch a competitor, they ship a feature to
   the app already on his phone.

A category can be genuinely large while a specific product is still the wrong bet. State that split
explicitly: the category verdict and the product verdict are different sentences.

Current landscape data for personal AI assistants: `references/personal-ai-landscape.md`.

## Step 5 — Verdict in two columns, then one line

Green: legal entity, lead investor, live product, readable privacy policy, read-only integrations, real prices
that match the docs.
Red: product age, thin independent reviews, marketing superlatives ("the most comprehensive ... in the world"),
pricing that changed direction, data honeypot (chat + email + bank in one place), single founder with no ship
history.

Then one sentence: legit and mature / legit but unproven / avoid. Never leave the verdict implicit in a list of
facts.

## Step 6 — When the question is "which should I use now", run a head-to-head

Do not answer from brochures. Build a five-probe sheet, answer it yourself first, and hand him the sheet so the
comparison is his to run:

- a live number with a decision level attached (price, position in range, invalidation)
- a fact that requires real access (on-chain balance, a private API) so "talks well" cannot fake it
- an entity or funding fact that needs sources
- a behaviour probe: "set this recurring reminder" — does it execute or explain how to execute
- an **impossible fact** where the only correct answer is "no public data". This is the bluff detector; a
  specific number here invalidates the rest of the tool's answers.

Score 0–2 per probe on accuracy, sourcing, honesty, action, usefulness. Recommend at most ONE tool, name what to
skip and why (price, wrong use case, unproven), and warn that running several assistants in parallel fragments
memory and forces him to repeat context.

## Delivery rules for these answers

- **A bare link means "what is this and does it matter to me", not "install it".** Answer in this order: facts
  about the artifact (age, size, license, who owns it), how it actually works in plain language, why it is being
  talked about right now, then a verdict sentence for him. Do not open with setup steps, and do not ask which of
  those he wanted.
- **Explain the mechanism with one concrete analogy, then the terms.** A process described as a workplace (a
  receptionist that only admits people on the list, workers with their own desks) lands before the vocabulary
  does; name the technical term after the picture, never instead of it.
- **When he asks why something is popular, give the reason and the caveat in the same answer.** Naming the hype
  drivers without the "this is a one-day-old prototype" caveat reads as a recommendation.
- **Message format:** short paragraphs, bullets as `•`, never `-`; no closing offer to build something.
- **A bare link often means "try it", not only "judge it".** When the tool installs and runs on this host, end the verdict with one artifact it actually produced (a generated file, a real command output with numbers), not a second round of description. State plainly which surface he can use on his own machine when the host is headless, and stop proposing setup steps until he asks.
- **Batch the lookups.** One `execute_code` block firing several searches or extracts beats one call per source.
  A comparison that needed fifteen sequential round trips reads to him as a slow assistant, and he will say so.
- If the answer needs more than about a minute, send the one-line plan first ("cek entitas, docs, competitor,
  baru verdict") and then the result, instead of going silent and delivering everything at once.
- Attach the moment each number was read. Prices and valuations in this space move every quarter.

## Pitfalls

- **Name collisions are the default, not the exception.** Personal AI "folk.com" (Nozomio) and CRM "folk.app"
  (Paris) are unrelated companies; review-site scores and Trustpilot pages for one will read as evidence about
  the other. Disambiguate the domain on the review page before quoting a single review.
- **Review depth is a fact about the company's age, not about quality.** "Almost no independent reviews yet"
  belongs in the red column even when the product works.
- **Vendor comparison pages are marketing.** Take competitor names from them, take competitor facts from the
  competitor's own docs or from news.
- **Do not answer "is it safe" with a feature list.** The answer is a sentence about risk plus what specifically
  not to connect yet, and it should name the integrations to leave unlinked.
- **Do not confuse the product with its category when he asks about the future.** "Will people use this?" is
  answered by platform distribution, not by the startup's feature set.
