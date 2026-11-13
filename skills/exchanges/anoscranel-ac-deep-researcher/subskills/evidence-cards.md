---
name: evidence-cards
domain: research-operations/evidence-cards
trigger: "\"this fact keeps coming up\", \"record this number properly\", \"is this claim card-worthy\", \"we'll need this again\"."
anti_trigger: "The bulk audit trail of the whole study (subskills/evidence-ledger.md); first-pass claim checking (subskills/verify-claims.md)."
scope: "Writing a claim card for every load-bearing, contested or single-source fact, and updating the same card when it re-arises"
status: "seedling"
---

# Evidence cards

## Standard

- A fact earns a card when it is load-bearing, contested, or single-source. The card preserves the verification work after the session
 ends; session memory is not storage.
- The card shape is fixed: claim, evidence, counter-evidence, confidence, and
 sources.
- Cards live in one claims folder you pick at the start of the study (any folder
 works; keep it stable), one file per slug. One fact, one card. When a fact re-arises, update the same card; never fork a second copy.
- Confidence on the card is capped by the source-trust ladder: a card built
 on a vendor claim says vendor rung, always.

## Decision rules

- Load-bearing means the verdict, money, law, or a named decision depends on
 the fact. Contested means two lineages disagree. Single-source means only
 one lineage carries it, however strong that lineage looks.
- If none of the three triggers fires, the fact belongs in the ledger, not in
 a card.
- A stale card is a liability. On re-verification with new evidence, update
 the card and its status; on supersession, delete the old observation and
 write the new one.

## Procedure

1. Detect the trigger: load-bearing, contested, or single-source.
2. Write the card in the fixed shape described above.
3. Fill the five fields in plain sentences. Evidence names what supports the
 claim; counter-evidence names what cuts against it.
4. Set confidence at or below the best rung, with the rung named.
5. File the card in that claims folder as `<slug>.md`, and cross-link it from
 the study's report.
6. When the fact re-arises in a later study, open the existing card and
 update it in place.

## Anti-patterns

- A card for trivia. Three triggers exist so trivia stays in the ledger.
- Two cards for one fact, drifting apart in two folders.
- Confidence written from how the claim feels instead of its best rung.
- A card whose sources section lists an index page instead of the primary.

## Done checklist

- Every triggered fact has exactly one card.
- Every card has all five fields filled.
- Every card's confidence matches its best rung.
- The study report links each card it relied on.

The card's counter-evidence field is the one most often left empty, and an empty field is ambiguous: it can mean the claim survived a search for contradicting evidence, or that no search was made. Recording which of the two applies is what makes the card an assessment rather than a quotation with metadata.

## Sources

- <https://osf.io/prereg/>
- <https://www.cisa.gov>
