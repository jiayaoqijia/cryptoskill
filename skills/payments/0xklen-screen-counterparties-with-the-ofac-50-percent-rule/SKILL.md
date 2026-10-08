---
name: screen-counterparties-with-the-ofac-50-percent-rule
description: Use when a corporate counterparty, fund or holding company is not itself listed but may be majority-owned by a designated person, so ownership must be aggregated and each intermediate entity screened.
---

# Apply the 50% ownership rule to a counterparty

A company that is not named on a list can still be blocked because a designated person owns 50%
or more of it, directly or through a chain of entities. No authority publishes this derived list —
you have to compute it, and the computation is the deliverable.

## Procedure

1. Build the ownership tree before any payment. Pull filings into one directory so each percentage
   has a citation.

       mkdir -p ~/cdd/$ENTITY && cd ~/cdd/$ENTITY
       # registrar / SEC / Companies House extracts, one file per layer
       ls -1 ownership-*.pdf articles-*.pdf

2. Sum direct and indirect stakes along every path. The rule aggregates: 60% held by an entity
   that is itself 60% held by a designated person gives that person 36% — below the line — while
   two 30% stakes from two designated persons gives 60% — at the line.

       python3 - <<'PY'
       paths = [("A", 0.60), ("B", 0.30), ("C", 0.30)]  # (designated holder, pct)
       print(sum(p for _, p in paths))                  # 1.20 -> blocked at the entity level
       PY

3. Screen every node in the tree — the operating company, each holding company, each general
   partner and each nominee — not just the entity on the invoice. Walk upward until you reach a
   natural person or a named listed party.

4. Mark each node with a disposition: `designated`, `>50% owned by designated`, `below threshold`,
   or `ownership unresolved`. Aggregate totals below 50% are still reportable as a red flag and
   feed enhanced due diligence.

5. Re-derive the tree when ownership filings change. A merger, a share issue, or a new fund LP can
   push an unlisted company over the line without any list update.

6. Escalate anything at or above the line to the compliance owner to block or reject. Do not
   process a "small" payment to a majority-owned entity on the reasoning that the amount is
   immaterial — the rule has no de minimis.

## Pitfalls

- Reading only the invoice counterparty and never the parent. Ownership evidence is rarely on the
  payment instructions.
- Treating the rule as a single-jurisdiction quirk; the EU and UK apply an equivalent ownership
  and control test, and their thresholds and aggregation of indirect holdings differ in detail.
- Using a nominee director as the beneficial owner. Look through to the person with the actual
  interest, and record how the chain was verified.
- Assuming a compliance vendor computes this for you. Vendor ownership data is often stale by a
  quarter, which is exactly the window a restructuring uses.
- Confusing "control" (veto rights, board appointment) with "ownership". Both can trigger
  blocking; record them separately.

## Verification

    grep -c "^designated," ownership-nodes.csv
    grep -E ",(5[0-9]|6[0-9]|7[0-9]|8[0-9]|9[0-9]|100)(\.[0-9]+)?,blocked$" ownership-nodes.csv

The second command must print nothing for a clean pass; any row it prints is an aggregated
ownership path at or above 50% and blocks the payment.

Report the ownership paths with percentages, the filing each rests on, and the disposition per
node. This is a factual screen for a human reviewer; the blocking decision belongs to a qualified
compliance officer or counsel, not to this procedure.
