---
name: text-policy-record
domain: software-engineering/text-policy-record
trigger: "Writing the system's text policy once, instead of per bug."
anti_trigger: "Not for storage-specific settings (that is text-in-storage)."
scope: "The written record: encoding, normalization, and boundary rules."
status: seedling
---

# Text policy record

## Standard

The text policy answers the questions this skill's leaves each answer locally: what encoding inside, which normalisation form, what unit for what limit, where conversion happens, what the stores declare. Written once, it converts a recurring class of bug — the encoding mismatch, the normalised hash, the sliced graphemes — into a lookup. Unwritten, it re-emerges in each new service that guesses.

The policy's value is at the boundaries, where two teams meet. A feed producer with the policy and a consumer with the policy interoperate without negotiation; without it, each assumes, and the mismatches are discovered in production data. Keeping the policy where the code lives — not in a wiki graveyard — is part of the discipline.

## Decision rules

- State the internal encoding and the normalisation form.
- State the unit rule: bytes for size, graphemes for display limits.
- List every boundary with its declared source encoding and conversion point.
- Record stores' character sets and collations, and the application limits derived from them.
- Name the recognised mojibake patterns and their causes from past incidents.
- Amend with dates; keep the exception list visible, not tribal.

## Procedure

1. Draft the policy from the leaf decisions.
2. Audit current services and stores against each rule.
3. Fix or register the exceptions found.
4. Publish beside the code and link it from onboarding.
5. Test with a boundary consumer built against the policy alone.
6. Amend with dates as rules change.

## Anti-patterns

- A policy that exists but that no boundary team read.
- Exceptions known only to senior engineers.
- Store collations recorded nowhere, discovered per incident.
- The policy in a wiki nobody visits.
- Silent rule changes without a dated amendment.

## Done checklist

- [ ] Encoding and form stated.
- [ ] Unit rule stated.
- [ ] Boundary list with conversions.
- [ ] Stores and collations recorded.
- [ ] Mojibake pattern list included.
- [ ] Exceptions visible and dated.

A final entry that pays for the whole document: the list of feeds and files that arrive in something other than the internal encoding, with the contact or standard that declared it — because when one of them silently changes, that entry is the difference between a one-line boundary fix and a week of guessing which side moved.

The policy should also carry its own version and the date of each amendment, because encoding decisions interact — a form change made after a store migration is a different document from one made before it, and the dates are what make the difference visible.

## Sources

- Unicode Standard: <https://www.unicode.org/versions/latest/>
- Normalization specification: <https://www.unicode.org/reports/tr15/>
- UTF-8 standard: <https://www.rfc-editor.org/rfc/rfc3629>
