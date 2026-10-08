---
name: rewrite-jargon-into-plain-language
description: Use when a doc, email, or error text must be understood by a non-expert reader. Swaps insider terms for concrete words and defines the few terms that must stay.
---

# Rewrite Jargon into Plain Language

Write for the reader who knows the domain but not your team's shorthand. Every acronym costs comprehension; spend it only when the reader uses it too.

## Procedure

1. List every acronym and internal term in the draft; for each, decide keep, expand, or replace using the reader's vocabulary.
2. On first use, expand an acronym that stays: "content delivery network (CDN)", then use the short form.
3. Replace internal codenames with what they do: "the Phoenix service" becomes "the billing service".
4. Swap Latinate verbs for Anglo-Saxon: "terminate" becomes "stop", "commence" becomes "start", "facilitate" becomes "help", "endeavour" becomes "try".
5. Convert passive to active: "the record is deleted by the job" becomes "the job deletes the record".
6. Give one concrete example in place of an abstraction: instead of "handles edge cases", write "handles a refund larger than the original charge".
7. Turn a noun pile ("user account provisioning pipeline") into a clause: "the pipeline that provisions user accounts".
8. Replace a metaphor that only insiders read ("warm the cache cold start"): say what happens and when.
9. Keep a defined-term list in a `GLOSSARY.md` if five or more acronyms must stay; link it once at the first occurrence.
10. Test with someone outside the team; every question they ask marks a term to fix.
11. Preserve precision: do not simplify a term that means something specific in the domain, such as "idempotent", without defining it properly.

## Pitfalls

- Dumbing down to the point of losing a real distinction between two costs or two states.
- Expanding an acronym on every mention instead of once, which adds noise.
- Replacing a term the team and its docs use everywhere, creating a third vocabulary.
- Explaining a term with another jargon term the reader also lacks.
- Assuming "plain" means short; clarity can need a qualifier the reader requires.
- Swapping a term for a synonym that changes the technical meaning (retry vs re-run).
- Over-explaining background the reader already has, which reads as condescending.

## Verification

    grep -oE '\b[A-Z]{2,}\b' doc.md | sort -u

The command lists every acronym; each must be expanded once at first use or listed in the glossary.

Run the rewritten text past one person outside the team and report the terms they still had to ask about.
