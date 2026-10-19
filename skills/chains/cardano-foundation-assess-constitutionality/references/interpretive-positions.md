# Interpretive Positions

These are **readings of the constitutional text, not the text itself**. They exist because
the provisions below are genuinely ambiguous and reviewers who skip the ambiguity reach
confident wrong answers. Each entry states the reading and the reasoning behind it.

Rules for using this file:

- Always attribute. Write "on the reading that II.7.5 requires the administrator to exist at
  the moment of withdrawal" — never "Article II.7.5 requires". The reader must be able to
  locate and reject the interpretation without rejecting the Constitution.
- A reader may disagree. If the assessment's outcome turns on one of these readings, say so
  explicitly and state what the outcome would be under the competing reading.
- These are not precedent. They do not bind anyone, and no past governance action is cited
  in support of them.

---

## Article II.6.1 — format and immutability

**Reading.** The requirement is a standardized legible format behind an immutable anchor:
"the document hosted by such a URL shall be immutable and incapable of being altered after
submission". It covers the anchored document, the one whose hash is on chain, and nothing it
links to. Mutability is a question of fact about the specific URL.

**Reasoning.** An IPFS CID is content-addressed and cannot change. A URL that names a moving
reference can: a GitHub branch path (`refs/heads/…`), a page on an ordinary web server, or an
IPNS name until it is resolved to a fixed CID. A Git tag or release asset sits in between; tags
can be moved and assets replaced, so treat it as changeable unless it is a commit hash.

**Consequence.** Establish what kind of URL the anchor is before writing the row. A
branch-path or plain-server anchor is Violated on this reading, with the remedy (resubmit
behind a content-addressed anchor). If the kind cannot be established, the row is
Not-yet-verifiable.

**Competing reading.** The on-chain hash makes any change detectable, so the anchored content
is effectively fixed as long as the hash still matches. On that reading a mutable URL whose
content still hashes correctly satisfies II.6.1. Where this decides the outcome, the report
says so.

---

## Article II.7.1 — terms of the withdrawal

**Reading.** The four elements the text names, purpose, period for delivery, costs and
expenses, and refund circumstances, stated in the anchor satisfy II.7.1. Granular milestones,
payment schedules, and dates below that level may be deferred to a contract executed after
ratification.

**Reasoning.** II.7.1 requires the terms to be stated, not that every operational detail be
fixed before the vote. Where an administrator holds pause and refund authority, that
framework is the enforcement layer for detail settled later.

**Consequence.** Continuous or open-ended scope is not automatically a defect. It does place a
burden on the assessment to explain why the request still describes specified activities,
by reference to the total amount, the period, and the administrator's authority. An open
scope with no amount cap, no period, and no pause authority fails, because nothing bounds it.

---

## Article II.7.2 — disclosure of prior treasury receipts

**Reading.** Disclosure in any form satisfies II.7.2. The Constitution prescribes no level of
detail, so a reviewer may not impose one.

**Reasoning.** The provision requires that prior receipts be disclosed. Reading in a
granularity standard the text does not contain converts a disclosure duty into a formatting
duty.

**Consequence.** Silence is a missing required element, so the row is Violated on this reading,
with a note of what was not disclosed and that one sentence cures it. Absent disclosure is not
by itself dispositive of the whole action; report it so readers can weigh it.

---

## Article II.7.4 — audit allocation, a two-part test

**Reading.** Two prongs must both be met: (a) an allocation for periodic independent financial
audits, and (b) an allocation for implementation of oversight metrics.

**Reasoning.** The provision requires *allocation*, not *itemization*. A named auditor with a
defined scope, a reporting cadence, and a plausible sum satisfies it even when the budget
line is not labelled "audit". Conversely, a bare line reading "Audits" with no scope, no
counterparty, and no description does not, because nothing establishes an audit was actually
provided for.

**Consequence.** Read the full exploded budget before concluding an allocation is missing.
Check both prongs separately; oversight metrics are frequently overlooked when a financial
audit is present. An allocation with a defined scope, cadence and amount satisfies prong (a)
even before an auditor is named: the text requires the allocation, not the counterparty.

---

## Article II.7.5 — the administrator must exist at the moment of withdrawal

**Reading.** The administrator may be a natural person, an institution, a company, or a smart
contract. What matters is that it exists and can act when funds leave the Treasury.

**Reasoning.** Monitoring that cannot begin until after disbursement is not monitoring. An
oversight body that the withdrawal itself is meant to constitute is therefore
self-referential and fails, because at the operative moment there is nobody to oversee.

**Consequence.** Do not write that II.7.5 requires "a party between recipient and disbursal";
that overstates it. Self-administration, where the recipient is its own administrator, is not
unconstitutional per se. It becomes serious when combined with a structural failure such as
an oversight architecture that does not yet exist.

The text requires designation and nothing more: "shall designate one or more administrators
responsible for monitoring how the funds are used, and ensuring the deliverables are achieved".
A designation conditioned on a future event ("proposed administrator, subject to
confirmation") is not yet a designation. A heading such as "Proposed administrators" over a
body that states they serve is a designation; judge the operative terms, not the label.
Directing funds to an organization's contract does not by itself make that organization the
administrator.

Whether the designated administrators agreed to serve is not a textual requirement. It is
still worth reporting as an open question, because a voter may weigh it. The evidence comes
in two kinds: a signature on the submission transaction by a key the administrator controls,
or a verified CIP-100 author signature on the anchor. Key presence alone proves nothing, since
a public key can be copied.

---

## Article II.6.2 — supporting materials outside the anchor

**Reading.** II.6.2 asks for "relevant supporting materials" and sets no condition on where they
live. Material the anchor references, such as a full proposal with the budget, refund terms or
the administrators' names, counts toward II.6.2 and the Article II.7 provisions it carries.

**Reasoning.** II.6.1 imposes immutability on the anchored document only. Requiring referenced
material to be immutable too would add an obligation the text does not state.

**Consequence.** Assess the referenced material as part of the action. When it sits behind a
URL that can change, say so in open questions, with what was read and its hash, so a reader
can tell whether it later changed. That is a voter's concern, not a constitutional defect.

---

## Net Change Limit — which limit is in force

**Reading.** The limit in force is the latest one DReps approved under TREASURY-01a whose period
covers the withdrawal. The Constitution does not say how a later limit relates to an earlier
one for the same period, so the finding always states which limit it relied on.

**Consequence.** Write "Based on the understanding that the Net Change Limit in force is …"
and name the action. If another approved limit covers the same window, give the outcome under
it in one sentence. If no approved limit can be established, ask the user rather than assume
one.

---

## Article II.7.6 — a narrow textual reading of destination requirements

**Reading.** II.7.6 requires three things: separate community-auditable accounts, no delegation
to a stake pool, and delegation to the predefined always-abstain DRep option. It does **not**
require script-locked custody.

**Reasoning.** The text names those prongs. A key-hash address that meets all three satisfies
II.7.6 on the on-chain record. Reading in a script-custody requirement adds an obligation the
provision does not state.

**Consequence.** A key-hash destination is acceptable where the administrator is distinct from
the recipient and bears responsibility for the funds. It aggravates an II.7.5 concern when
combined with recipient-controlled custody, but report it as aggravating rather than as an
independent defect.

Note the precision required on the abstain prong: the Constitution names the *predefined*
always-abstain option. A DRep that merely abstains in practice does not satisfy it.

The holding-period obligations in II.7.6 engage only while an administrator holds ada before
onward disbursement. A single automated transfer engages only the destination prongs.

---

## Protocol-as-administrator — a very narrow exception

**Reading.** For a single, automated, unconditional transfer completing in one transaction,
the protocol itself performs the administrator's function, and II.7.4 and II.7.5 are
satisfied without a separate administrator.

**Reasoning.** The disbursement is publicly verifiable in one transaction and admits no
discretion, so an intermediary would add no constitutional benefit.

**Consequence.** Frame this explicitly as a narrow exception whenever it is relied on. Anything
involving staged disbursement, discretion, or conditions falls outside it and requires the
ordinary accountability architecture.

---

## The Constitution sets a floor, not a governance manual

**Reading.** Where a provision states a requirement and the action meets it, the provision is
satisfied, even if the arrangement is weak, self-serving, or plainly improvable. The Constitution
prescribes a minimum, not best practice. Whether a structure that clears the minimum is *good
enough to fund* is committed to DReps and the Community, not resolved by the constitutional
question.

**Reasoning.** Provisions such as Article II.7.5 name what must exist (a designated administrator
responsible for monitoring) without prescribing its quality, independence, or enforcement powers.
Reading those attributes in converts a floor into a standard the text does not set, and hands the
reviewer a discretion the Constitution withheld. The remedy for an arrangement that meets the
floor but is unattractive is a vote against it, not a finding of unconstitutionality.

**Consequence.** This is the rule that resolves the common hard case: the text is met, the
structure is thin, and the analysis wants to hedge. Do not hedge. Find the provision satisfied,
then move the structural concern to open questions or the counterargument, stated at full strength
and attributed to the reader who must weigh it.

Two limits on this principle, or it would swallow every finding:

- It does not rescue an arrangement that fails the floor. Machinery that cannot function at the
  operative moment is not a weak version of compliance, it is non-compliance. Contrast the
  administrator who exists but is poorly checked (satisfied) with the administrator that the
  withdrawal itself is meant to bring into being (not satisfied).
- It applies to the quality of an arrangement, never to the absence of a required element. A
  missing disclosure, a missing allocation, or a missing designation is not thinness.

Applied honestly, this principle produces definite findings on contested facts. An assessment that
records a provision as contested when the floor is met and the text is clear has not been careful,
it has declined to answer.

---

## Appendix I.2.6 — reversion plans, graded by element

**Reading.** The two elements Appendix I.2.6 requires of a reversion plan carry different weight.
Absence of the revert targets is a defect. Absence of the network-recovery element, or of the
monitoring commitment, is an open question unless the change carries unaddressed propagation or
availability risk.

**Reasoning.** The provision's purpose is that someone has thought concretely about undoing the
change. Revert targets are the irreducible core: without them nothing can be undone, and no
argument substitutes for them. The network-recovery element serves a narrower purpose, guarding
against a change that could degrade the network in ways a parameter reset alone would not fix.

Where a proposal establishes that disastrous failure is not a credible mode, that purpose is
already served. A parameter touching only reward distribution cannot affect block production or
propagation. A network parameter supported by diffusion benchmarking under MBEU-M-04a has been
measured against the very risk the recovery element exists to catch.

Reading "must include" strictly against both elements would fire on nearly every parameter
proposal, because proposers routinely argue the contingency away instead of writing a recovery
section. A finding returned every time carries no information and crowds out the findings that
matter.

**Consequence.** Grade the elements separately. Escalate a missing recovery element to a defect
when a network parameter is changed with no benchmarking and no monitoring commitment, because
there the risk is real and unexamined. Where the proposal has addressed the risk, report the
omission as an open question and say what would settle it.

**Competing reading.** "Must include" read strictly makes both elements required, so a missing
recovery element is Violated whatever the risk. Where a row turns on this, the report says so.

Partial reversibility is never a defect on its own. Appendix I.2.6 states that not all changes
can be reverted, so a proposal disclosing where its own revert path stops short is complying with
the provision rather than falling short of it, and the disclosure counts in its favour.

---

## Governance design questions that are not constitutional defects

**Reading.** The following are matters for the proposer and the voters, not constitutional
compliance:

- Value contingent on a future hard fork or a separate governance action.
- Multiple workstreams bundled into one request.
- Whether the amount represents good value.

**Reasoning.** The Constitution does not prescribe how proposers structure requests. Iterative
upgrades are expected. Where an administrator can pause and refund, a failed condition has a
remedy. Voters decide whether they accept the scope.

**Consequence.** Route these to an open-questions section as considerations a voter may
reasonably weigh. Do not grade them as defects. Hard fork names and protocol version numbers
carry no constitutional weight and should not be presented as constitutional facts.

---

## Ada denomination and price volatility

**Reading.** Where a withdrawal is denominated in ada as the guardrails require, movement in
the ada/USD rate is not a constitutional issue.

**Reasoning.** The requirement is about the unit of denomination. A reference fiat figure used
for context does not change what was requested.

**Consequence.** Do not raise volatility as a defect against an ada-denominated request.

---

## The distinction that governs every assessment

Constitutionality is not merit. A request may be unwise, poorly scoped, or badly argued and
still be constitutional; it may be valuable and popular and still violate a provision. Every
finding must trace to specific constitutional text. When the objection is really about
whether the idea is any good, it belongs in open questions, labelled as such.
