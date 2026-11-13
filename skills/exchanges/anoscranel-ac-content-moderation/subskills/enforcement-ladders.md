---
name: enforcement-ladders
domain: software-engineering/enforcement-ladders
trigger: "Designing proportionate, graduated actions for violations."
anti_trigger: "Not for deciding severity of a category, and not for appeal handling."
scope: "Graduated actions proportionate to severity and history."
status: seedling
---

# Enforcement ladders

## Standard

An enforcement ladder maps violation severity and user history to graduated actions: warning, content removal with notice, feature restriction, temporary suspension, and account termination. The design question is proportionality — a first minor violation meeting the same response as a severe one teaches users that the system is arbitrary, and a severe violation meeting a warning teaches them it is toothless. The ladder makes proportionality an explicit data structure rather than a per-case judgement.

The ladder is parameterised by severity tier and history class. Each rung names its action, its duration, its notification text, and its reversal path. Escalation is data-driven — the same severity with a prior violation escalates by stated steps, not reviewer discretion — and exceptional cases are handled by an override path that is itself logged and reviewed, so discretion exists without silently replacing the ladder.

Primary sources: <https://en.wikipedia.org/wiki/Content_moderation> and <https://transparency.meta.com/>.

## Decision rules

- Each ladder rung names action, duration, notification text, and reversal path.
- Severity tier × history class determines the rung; the table is data, not memory.
- Escalation steps between rungs are stated; skip-to-top is an explicit override.
- Overrides are logged, reviewed on a cadence, and audited for consistency.
- Every enforcement action carries the rule and item that triggered it.
- Notification texts are reviewed for clarity: the user learns what happened and why.

## Procedure

1. Define severity tiers from the taxonomy's severity attribute.
2. Define history classes and the lookback window for each.
3. Draft the severity × history action table.
4. Write notification text per rung and its translation plan.
5. Wire the override path with logging and a review cadence.
6. Record the ladder version; every enforcement references it.

## Anti-patterns

- Severity decided case-by-case with no recorded mapping.
- Termination for first minor violations; warnings for severe ones.
- Silent enforcement with no notification to the user.
- Shadow enforcement actions outside the ladder and unlogged.
- Overrides so frequent the ladder is decoration.

## Done checklist

- [ ] Severity tiers defined from taxonomy.
- [ ] History classes with lookback windows.
- [ ] Severity × history action table written.
- [ ] Notification texts per rung.
- [ ] Override path with logging and review.
- [ ] Ladder versioned and referenced by every action.

Duration design deserves its own look: temporary restrictions have a stated end that the system actually enforces, because an expiry that only lifts when someone notices is an indefinite restriction wearing a temporary one's label. The ladder records both the rung's duration and the mechanism that ends it.

## Sources

- Content moderation overview: <https://en.wikipedia.org/wiki/Content_moderation>
- Platform transparency reporting: <https://transparency.meta.com/>
- Regulatory context: <https://en.wikipedia.org/wiki/Digital_Services_Act>
