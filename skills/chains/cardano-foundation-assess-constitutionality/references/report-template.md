# Assessment Report Template

Deliver the report in conversation, in full. When the user asks for a file afterwards, it is
`assessment-<slug>.md` in the working directory. Keep the section order below; readers and
reviewers rely on it.

Omit a section only when it would be empty, with one exception: the findings table is never
omitted and never abbreviated, because a missing row is indistinguishable from a passed one.

---

```markdown
# Constitutional Assessment: <title>

## Subject

| | |
|---|---|
| Action type | <TreasuryWithdrawals / ParameterChange / …> |
| Stage | Live action / Pre-submission / Draft |
| Identifier | <gov_action1…, or the transaction ID for a pre-submission transaction, or "not yet submitted"> |
| Source | <on-chain record; transaction decoded with <tool>; file path; URL as supplied by the user; or "pasted into conversation"> |
| Assessed | <date> |

## Basis

| | |
|---|---|
| Constitution | enacted epoch 609, anchor hash `b368bd…` |
| Currency | Confirmed current / Unverified |
| On-chain record | Supplied and assessed / Decoded from the transaction / Not supplied / Not applicable (draft) |
| Data read at | <epoch, and date> |

<If currency is unverified, one sentence: the assessment rests on the snapshot above and a
newer Constitution may have been enacted since.>

## Pre-submission checks

<Pre-submission transactions only. Both tables from transaction-input.md, mechanical and
constitutional, each row Pass / Fail / Not checked with the reason.>

| Check | Result | Basis |
|---|---|---|
| Deposit equals `govActionDeposit` | Pass | <value read, value expected> |
| Anchor content hashes to the anchor data hash | Fail | <computed hash, anchored hash> |

## Findings

| Provision | State | Basis |
|---|---|---|
| Article II.6.1 | Satisfied | <what establishes it> |
| Article II.7.4 | Violated | <the specific failure> |
| Article II.7.6 | Not yet verifiable | <what is missing and why> |

## Analysis

<One subsection per provision that is Violated or Not-yet-verifiable, and per provision whose
satisfaction was not obvious. Quote the operative language, apply it to the facts, state the
conclusion. Where the outcome turns on a reading from interpretive-positions.md, attribute it
and state what the competing reading would produce.>

<Satisfied provisions that were straightforward need one line each in the table and no
subsection. Do not pad.>

## Open questions

<Matters a voter may reasonably weigh that are not constitutional defects: scope, bundling,
conditionality, value for money. Labelled clearly as not constitutional findings.>

## Disposition

<Pre-submission only, first: **Readiness:** Ready to submit / Fix before submitting: <rows> /
Not checked: <rows>.>

<Assessment language. "No constitutional defects identified." / "Constitutional defects
identified under Article II.7.5." / "Assessment incomplete: II.7.5 and II.7.6 could not be
settled without the on-chain record.">

**Predicted verdict:** <A Constitutional Committee applying this analysis would likely find
the action Constitutional / Unconstitutional.> <Confidence: high / moderate / low, with the
reason.>

## Verification checklist

<Drafts, and live actions with unsupplied on-chain data. Each item states what must be true
and how to establish it. See onchain-verification.md.>

- [ ] Withdrawal destination is a separate account, not delegated to any stake pool, and
      delegated to the predefined `drep_always_abstain` option (II.7.6)
- [ ] Administrators are designated in the action's own terms, not conditionally (II.7.5)
- [ ] Anchor is immutable and its content hashes to the on-chain `meta_hash` (II.6.1)
- [ ] Withdrawal fits within the Net Change Limit currently in force
```

---

## Rules for the predicted verdict

The predicted verdict is the line most likely to be quoted in isolation and the line most
likely to be wrong. Constrain it:

- It never appears without the findings table above it in the same document. Never state it
  alone in conversation.
- Confidence is **low** whenever any provision is Not-yet-verifiable. Name which ones.
- It is a prediction about how a committee would rule, not a ruling. Never write that an
  action "is unconstitutional"; write that defects were identified under a named provision.
- When the prediction turns on an interpretive position, say so and give the alternative.

## Rules for the findings table

- A provision with several prongs (II.6.1 format, hash and immutability; II.7.1's four terms;
  II.7.6's three) gets one row per prong, so a reader can see which part failed.
- Every engaged provision gets a row. A provision examined and found satisfied is a row; a
  provision never examined is a row marked Not-yet-verifiable.
- Three states only: Satisfied, Violated, Not yet verifiable. No "probably", no "likely
  satisfied". If it is uncertain, it is Not-yet-verifiable and the Basis column says what
  would settle it.
- The Basis column cites what establishes the state: a quoted term from the proposal, a field
  from a supplied on-chain record, or the specific absence relied on.
