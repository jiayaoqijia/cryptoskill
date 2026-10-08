---
name: write-compliance-findings-for-counsel-review
description: Use when handing a screening or transaction question to a lawyer, and the write-up must state facts, sources and the open questions without phrasing them as legal conclusions.
---

# Write compliance findings for counsel review

A lawyer cannot answer a question they cannot restate. The deliverable is a facts-and-sources
package that states what was observed, from which version of which authority, and where the
ambiguity sits — plainly labelled as questions, never as verdicts.

## Procedure

1. Open with the question, in one sentence, as a question. Not "the address is sanctioned" but
   "does interacting with this address engage the designation as at 2026-10-01?".

2. Present a facts table where every row carries its source and its as-of timestamp:

```
       cat > finding.md <<'MD'
       | fact | value | source | as_of |
       |---|---|---|---|
       | subject | 0x8589...1fda07 | customer record | 2026-10-08 |
       | list | OFAC SDN | sha256:ab12... | 2026-10-08T06:00Z |
       | screen result | exact match, row 412 | sdn.csv | 2026-10-08T06:01Z |
       MD
```

3. Separate observation from inference with explicit headings. Observations cite artefacts;
   inferences are labelled as such and say what would falsify them.

4. List the open questions numbered, each one narrow enough to answer. "Is this prohibited?" is
   better than "what should we do?", and both are better than a conclusion dressed as a
   recommendation.

5. Attach the raw evidence as an appendix: the matched row, the digest, the transaction hash. Do
   not paraphrase the list entry — quote it.

6. State the jurisdictional facts the answer will depend on: where the customer is, where the
   entity is, which regulator's rules you assume apply. Flag any of these you could not confirm.

7. Mark every deadline and its source, and mark which ones are assumptions pending confirmation.

## Pitfalls

- Writing a conclusion and calling it a finding. "This is a hit, so we must freeze" mixes the
  observation with the legal consequence and pre-empts the counsel review it was supposed to
  request.
- Omitting the list version. Without it, counsel cannot tell whether the designation was in force
  on the transaction date.
- Paraphrasing a designation instead of quoting it; designation text is precise about scope.
- Burying the open question under pages of narrative, so the actual question is never answered.
- Presenting a vendor risk score as if it were a legal status, which changes the nature of the
  question counsel is being asked.

## Verification

    grep -c "^| fact" finding.md
    grep -nE "^## (Observations|Inferences|Questions|Assumptions)" finding.md

Both blocks must be present; a finding with observations but no separate questions section is
advice in disguise and fails review.

Report the question, the facts with sources and as-of dates, the assumptions, and the open
questions. Nothing in this package is legal advice, and no conclusion in it is final until
qualified counsel has given their determination.
