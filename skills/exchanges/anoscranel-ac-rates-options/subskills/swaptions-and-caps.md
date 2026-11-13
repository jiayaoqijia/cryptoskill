---
name: swaptions-and-caps
domain: investing/swaptions-and-caps
trigger: "Reading a swaption, cap, or floor and what it gives the holder."
anti_trigger: "Not for predicting rates, and not for generic option theory."
scope: "Payer and receiver swaptions, caps and floors, and how they decompose."
status: seedling
---

# Swaptions and caps

## Standard

A swaption is an option to enter a swap at a stated rate on a stated date. The payer swaption gives the right to pay fixed — it gains value when rates rise — and the receiver gives the right to receive fixed, gaining when rates fall. The underlying is defined by its tenor, the length of the swap entered into, and its expiry, the date the choice is made; those two numbers together identify the instrument.

Caps and floors are portfolios of options on forward rates, one per accrual period, which is why a cap is described as a strip of caplets. A cap pays when the reference rate exceeds the strike for a period, and a floor pays when it falls below. The decomposition matters because a cap's value is sensitive to the whole strip, so its behaviour differs from a single swaption of similar maturity, especially when the curve moves.

Primary sources: <https://www.cmegroup.com/> and <https://www.bis.org/>.

## Decision rules

- Record the instrument type, expiry, tenor, strike, and currency.
- Record whether the holder pays or receives fixed, or buys a cap or floor.
- Record the reference rate and its fixing convention for caps and floors.
- Record the notional and whether it amortises.
- Record the premium and settlement convention.
- Record the model used for any sensitivity reported.

## Procedure

1. Identify the instrument and its two defining dates.
2. Record strike, notional, and direction.
3. Record the reference rate and fixing convention.
4. Record the premium and settlement.
5. Record the model behind any greeks reported.
6. Write the instrument summary with its terms.

## Anti-patterns

- Confusing a payer swaption with a receiver.
- Quoting a swaption without its tenor.
- Treating a cap as a single option on one rate.
- Ignoring amortisation in the notional.
- Reporting greeks without the model that produced them.

## Done checklist

- [ ] Instrument, expiry, tenor recorded.
- [ ] Direction and strike recorded.
- [ ] Reference rate and fixing recorded.
- [ ] Notional and amortisation recorded.
- [ ] Premium and settlement recorded.
- [ ] Model recorded.

A further distinction is settlement: a physically settled swaption delivers a swap whose value must then be managed, while a cash-settled one pays a lump sum computed from the swap's value at exercise. The choice affects the hedge, the accounting, and the funding, and a trade that is compared across the two without noting the difference is compared on the wrong basis.

## Sources

- Exchange interest-rate option specifications: <https://www.cmegroup.com/>
- Market standards and documentation: <https://www.bis.org/>
- Rate and swap data: <https://www.federalreserve.gov/>
