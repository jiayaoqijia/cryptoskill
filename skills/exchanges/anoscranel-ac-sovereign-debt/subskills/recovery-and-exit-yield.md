---
name: recovery-and-exit-yield
domain: investing/recovery-and-exit-yield
trigger: "Estimating sovereign recovery and reading the exit instrument's yield."
anti_trigger: "Not for predicting a negotiation outcome, and not for recommending a bond."
scope: "Recovery arithmetic, the exit instrument, and what the yield signals."
status: seedling
---

# Recovery and exit yield

## Standard

Sovereign recovery is not a liquidation value; it is the present value of what the new instruments are expected to pay, relative to the old claim's face. That arithmetic requires assumptions about the new bonds' coupons, maturities, and the probability that the sovereign services them, and the answer is therefore a range built from those assumptions rather than an estimate of asset value.

The exit yield is the yield at which the new instruments trade once issued, and it carries information the recovery calculation does not. A new bond trading at a yield far above its coupon says the market doubts the programme's durability; one trading close to the coupon says the market accepts the restructuring as sufficient. Recording both the recovery estimate and the exit yield separates what the terms gave from what the market believed.

Primary sources: <https://www.imf.org/> and <https://www.bis.org/>.

## Decision rules

- Record the old claim's face value and the new instruments' terms.
- Compute the recovery as the present value of the new instruments at a stated discount rate.
- Record the discount rate and its source, since it drives the answer.
- Record the exit yield and compare it with the assumed discount rate.
- Record the assumptions about future servicing and any step-up or GDP-linked feature.
- Record the range across plausible discount rates rather than a single figure.

## Procedure

1. Record the old claim and the new instruments.
2. Compute the present value at two discount rates.
3. Record the implied recovery range.
4. Record the exit yield at issuance.
5. Compare the exit yield with the assumed rate.
6. Write the analysis with the range and the market's read distinguished.

## Anti-patterns

- Treating recovery as a single number.
- Using a discount rate that the exit yield contradicts without noting it.
- Ignoring GDP-linked or step-up features in the new instruments.
- Assuming the new instruments will be serviced as scheduled because they were agreed.
- Confusing the haircut on face with the recovery on present value.

## Done checklist

- [ ] Old claim and new terms recorded.
- [ ] Present value computed at two rates.
- [ ] Recovery range stated.
- [ ] Exit yield recorded.
- [ ] Exit yield compared with the assumed rate.
- [ ] Features of the new instruments recorded.

## Sources

- Sovereign restructuring analysis: <https://www.imf.org/>
- Market data and standards: <https://www.bis.org/>
- Rate data for discounting: <https://fred.stlouisfed.org/>
