# Inspiration sources (external)

Five curated libraries for real-world design evidence. Use them to ground visual decisions in shipped work instead of inventing patterns from memory. Each entry says what the site is actually good for, how to query it, and how to access it from this machine.

## 1. mobbin.com — 600k+ screens, UX flows, MCP

**Best for:** real app screens and multi-step flows (onboarding, checkout, paywall, empty states, settings). The single best source for "how do shipped apps actually solve this screen" questions, and for flow logic rather than single-screen looks.

**Query pattern:** `site:mobbin.com <product type> <screen> flow` e.g. `site:mobbin.com fintech onboarding kyc flow`, `site:mobbin.com saas pricing paywall`.

**Access:** PAID. The library sits behind a paid subscription, so treat it as unavailable unless the user explicitly has an account. Do not scrape paywalled screens, do not sign up, never suggest buying it mid-task. With an account the query patterns above still apply; without one, use the free substitutes below.

**Free substitutes for the same need:** `site:pageflows.com <flow>` for multi-step flows, `site:screenlane.com <screen>` for individual screens, plus screenshots the user already has. Verify the paywall state before promising depth from any of them.

**Mobbin MCP** exists but requires the paid account, so it is out of scope by default.

## 2. designspells.com — animations and tiny UI details

**Best for:** micro-interactions, transitions, hover/state choreography, loading and success moments. Use when a build looks static or when a component needs one memorable detail.

**Query pattern:** `site:designspells.com <interaction>` e.g. `site:designspells.com button hover`, `site:designspells.com tab transition`.

**Access:** aggressively rate-limited (HTTP 429 on plain requests). Use `browser_exec` with a real browser, wait for load, read the DOM. Never hammer it.

**How to use the output:** copy the motion idea (duration, easing, what moves and what stays), not the visual skin. Name the effect in the handoff so the dev can find it again.

## 3. recent.design — OG images, icons, launch videos

**Best for:** marketing surfaces — social/OG cards, icon sets, launch and product videos. Use before designing a launch page, a share card, or an app icon.

**Query pattern:** `site:recent.design <surface>` e.g. `site:recent.design og image saas`, `site:recent.design app icon gradient`.

**Access:** pages return 200 to curl; still prefer `browser_exec` for rendered layout.

## 4. brandguidelines.net — brand identities and design systems

**Best for:** identity work and token design — logo usage, type scales, color systems, spacing rules, voice. Use when a project needs a real design-system skeleton rather than ad-hoc colors.

**Query pattern:** `site:brandguidelines.net <industry> identity` or `<company> brand guidelines`.

**Access:** 200 to curl; content is mostly static HTML so `web_extract` is fine.

**Rule:** use these as structure references. Never reproduce another company's marks, exact palette, or proprietary typeface for a client project.

## 5. deck.gallery — pitch decks

**Best for:** narrative structure and slide rhythm — how a story is sequenced across pages, how a number slide is framed, how density varies. Use for decks, proposals, and any multi-slide deliverable.

**Query pattern:** `site:deck.gallery <industry> deck` e.g. `site:deck.gallery fintech seed deck`.

**Access:** Cloudflare returns 403 to curl. `browser_exec` only.

**How to use the output:** steal the sequence (problem → proof → number → ask), not the slide art.

---

## Workflow rule

Before starting any visual deliverable, pull **2–3 references** and write down what you are taking from each in one line: `mobbin: 4-step KYC flow, one decision per screen` / `designspells: tab underline slides, 220ms ease-out`. Then build. This prevents the default failure mode of designing from memory and producing generic work.

If a source is unreachable (login wall, Cloudflare, 429), say so and continue with the sources that do work. Never describe a reference you could not open.

## Source → task map

| Task | Primary | Secondary |
|---|---|---|
| App screen or flow | pageflows / screenlane (free) | designspells |
| Micro-interaction / motion | designspells | recent.design |
| Launch page, OG card, icon | recent.design | deck.gallery |
| Brand / design tokens | brandguidelines | designspells |
| Deck or proposal | deck.gallery | brandguidelines |

Mobbin is paid: use it only when the user says they have an account. Never make a deliverable depend on it.
