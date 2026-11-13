---
name: red-flags
domain: crypto-trading/red-flags
trigger: "Running the checklist that ends a token diligence early."
anti_trigger: "Not for confirming a decision you have already made."
scope: "The checklist that ends a diligence early: unauditable reserves, undisclosed unlocks, paid volume, yield promises, anonymous control."
status: seedling
---

# Red flags

## Standard

Most bad outcomes are visible in advance to anyone who runs a short list. The flags below are not proofs of fraud; they are conditions under which the remaining diligence is not worth the time, because the thing being evaluated cannot be evaluated with public information. A red flag ends the record with a stated reason.

The strongest flags share a property: they remove your ability to check. An undisclosed supply schedule, reserves that cannot be audited, a team with no verifiable identity behind upgradeable contracts — each of these makes every other number in the record unverifiable, which is the actual finding.

Primary sources: <https://www.investor.gov/introduction-investing> and <https://www.sec.gov/investor>.

## Decision rules

- Any single flag in the stop list ends the diligence and records the reason. It is not a score to be outweighed.
- Promised yield is a flag when the source of the yield cannot be named and traced.
- Anonymous control is a flag when the anonymous party holds mint or upgrade rights; anonymity alone with no powers is a note, not a stop.
- Paid volume is a flag when incentive programmes account for most turnover and the expiry is near.
- Reserve claims that cannot be checked on-chain or by a reputable attestation are a flag.
- If a promoter discourages verification, that is itself a flag.

## Procedure

1. Run the stop list before any other leaf: undisclosed schedule, unauditable reserves, unverifiable control, promised yield, manufactured volume, pressure to skip checks.
2. For each flag found, write the evidence and the date.
3. Stop. Do not continue the remaining leaves; record why.
4. If no flag is found, record the negative result explicitly, with the checks performed.
5. Re-run the stop list whenever supply, control, or incentives change.

## Anti-patterns

- Treating a red flag as a risk to be priced rather than a reason to stop.
- Accepting a verbal assurance as resolution of a flag.
- Continuing the analysis because effort has already been spent.
- Scoring flags against attractive fundamentals.
- Softening the record's language to avoid criticising a project.

## Done checklist

- [ ] Stop list run before other leaves.
- [ ] Each found flag carries evidence and date.
- [ ] Diligence stopped and reason recorded if any flag fired.
- [ ] Negative result recorded explicitly where no flag fired.
- [ ] Re-check trigger noted (supply, control, or incentive change).

## Sources

- Investor education on fraud and disclosure: <https://www.investor.gov/introduction-investing>
- Securities regulation context: <https://www.sec.gov/investor>
- Ethereum token standards documentation: <https://ethereum.org/en/developers/docs/standards/tokens/>
