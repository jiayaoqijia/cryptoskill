---
name: choose-a-stablecoin-settlement-rail
description: Use when picking which stablecoin and chain to settle payments on. Compares reserve quality, redemption, finality, freeze risk, and fees for a concrete payment volume.
---

# Choose a stablecoin settlement rail

Every stablecoin rail trades off reserve quality, redemption terms, finality, freeze risk, and cost. Pick per payment profile rather than defaulting to the most liquid token, and record the reasoning.

## Procedure

1. Fix the payment profile: ticket size, daily volume, counterparty type, chain of the counterparty, and required finality.
2. Score candidate rails on five axes, with numbers:
   - Reserve quality: attested fiat (USDC) > over-collateralised (DAI) > algorithmic.
   - Redemption: par at issuer, fee, minimum, settlement time.
   - Finality: Ethereum probabilistic (~12 min), an L2 soft confirm (~seconds) with a 7-day exit, or a chain with a finality gadget.
   - Freeze risk: denylist yes/no and its history.
   - Cost: L1 calldata versus L2 blob fees for the typical ticket.
3. Compute effective cost for the actual ticket; a $2 transfer on L1 with a $1.50 fee is 75% overhead, the same rail is fine at $50k.
   `python3 -c "print(round(1.5/2,4))"`  -> 0.75.
4. For high-value settlement prefer deterministic finality and no freeze; for micro-payments prefer a cheap L2 and accept soft finality.
5. Confirm the receiving side supports the chain and asset; a rail the counterparty cannot off-ramp is not a rail.
6. Record the decision and the date; fee markets and issuer terms change.

## Pitfalls

- Choosing the biggest stablecoin by cap when the counterparty's custodian rejects that chain.
- Comparing L1 and L2 fee estimates at quiet-gas hours and generalising.
- Ignoring the off-ramp: the true cost includes converting the stablecoin back to bank money.
- A rail that is cheap now because it is subsidised; model the unsubsidised fee.
- A rail chosen for today's volume becomes a constraint the moment volume multiplies; model the next tier, not just the current one.

## Verification

    python3 -c "print(round(fee/ticket,4))"   # overhead fraction for the real ticket size
    # reject any rail whose overhead fraction exceeds the business cap (e.g. 0.02)

Report the ranked rails with the five scored axes, the overhead for the actual ticket, and the chosen rail with its rationale.
