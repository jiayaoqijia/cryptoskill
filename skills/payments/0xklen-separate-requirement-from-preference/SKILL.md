---
name: separate-requirement-from-preference
description: Use when requests mix hard constraints with tastes ("it must be blue and fast"). Splits each into a testable requirement or a deferrable preference so neither is silently dropped.
---

# Separate requirement from preference

Requests arrive braided: the non-negotiable tangled with the nice-to-have. This skill untangles them so the build can trade preferences without breaking constraints.

## Procedure

1. List every stated want from the request in `wants.md`, one per line.
2. For each, ask: "if we violate this, does the user's task fail, or does it just look different?" Failure means requirement; appearance means preference.
3. Tag requirements `must` and preferences `should` or `could`, and note the source of each tag (regulation, contract, physics, taste).
4. For every `must`, name the test that catches a violation; a requirement no test can catch is a preference in disguise.
5. For every `should`/`could`, note the cost to satisfy it and whether it can be deferred without breaking a `must`.
6. Find hidden requirements the user implied but never said: data retention, accessibility, localisation, rate limits. Write them down.
7. When a `must` and a `should` conflict on cost, resolve in favour of the `must` and record the dropped preference.
8. Re-read the split with the requester; people often discover a preference was a requirement only when they see it labelled.
9. Name the decider for each borderline item so the tag is a decision, not an opinion in a file.
10. Re-check the split when a preference turns out to be load-bearing, such as a colour that carries meaning.

11. Ask for the failure consequence of dropping each `should`; if none exists, it is a `could`.

## Pitfalls

- Elevating a preference to a requirement because the requester was emphatic; volume is not a constraint.
- Demoting a real constraint (legal, accessibility) to a preference because it is inconvenient.
- A `must` with no test, which will be violated quietly.
- Missing implied requirements that only surface in an incident (retention, exports).
- Recording the split but never showing it, so the disagreement resurfaces late.
- Marking everything `must` to avoid the conversation about what can slip.
- Tagging an accessibility need as a preference, which is neither true nor lawful.

- Treating a preference list as a priority order without stating the tradeoff.

## Verification

    grep -cE '^\s*-\s*(must|should|could)' wants.md; grep -cE 'test:' wants.md

Report the `must` list with its tests, and preferences deferred with their cost.
