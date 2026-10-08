---
name: audit-third-party-scripts
description: Use when third-party tags dominate load cost. Accounts for each vendor's bytes and CPU, then replaces embeds with facades and defers the rest.
---

# Audit Third-Party Scripts

Third parties are the fastest-growing part of most bundles and the least owned by the team. Each tag is a vendor's main-thread tax on your Core Web Vitals.

## Procedure

1. Attribute load cost per origin with the Lighthouse third-party summary:

       npx lighthouse https://shop.example.com --only-audits=third-party-summary --output=json | jq '.audits."third-party-summary".details.items[] | {entity, transferSize, blockingTime}'

2. Classify each vendor: analytics (defer to idle), embeds (replace with a facade), ads/tags (contain in an iframe), chat (load on interaction).
3. Replace heavy embeds with a static facade that swaps to the real iframe on click:

       <lite-youtube videoid="dQw4w9WgXcQ" style="background-image:url(/thumb.jpg)"></lite-youtube>

4. Load analytics after first paint, not in the head:

       addEventListener('load', () => requestIdleCallback(() => import('/analytics.js')));

5. For tag managers, audit the container in the vendor UI and delete tags no one can name an owner for; dead tags still execute.
6. Re-measure `blockingTime` per entity after the changes and keep the table in the repo.

## Pitfalls

- Adding a vendor to fix a metric while its own script costs more than the metric was worth.
- Lazy-loading a chat widget that then appears 4 s into a session anyway, so the cost moved rather than disappeared.
- Loading a consent banner that itself blocks rendering; it must be the lightest thing on the page.
- Assuming a tag manager's "async" mode makes every contained tag async; a tag inside can still be synchronous.
- Auditing once and never re-checking; third-party payloads change without a deploy on your side.

## Verification

    npx lighthouse https://shop.example.com --only-audits=third-party-summary --output=json | jq '[.audits."third-party-summary".details.items[].blockingTime] | add'

The summed third-party blocking time must drop below the pre-change baseline. Report the top three entities with their blocking time before and after.
