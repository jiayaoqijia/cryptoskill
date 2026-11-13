---
name: liquidity-terms-and-gates
domain: investing/liquidity-terms-and-gates
trigger: "Reading a fund's lockup, gates, and redemption mechanics."
anti_trigger: "Not for measuring portfolio liquidity, and not for the allocation call."
scope: "Lockups, notice periods, gates, and what an exit actually requires."
status: seedling
---

# Liquidity terms and gates

## Standard

A fund's liquidity terms define when an investor can ask for money back and what the manager may do when too many do. A lockup sets the minimum holding period, a notice period sets how far ahead the request must be made, a gate caps the proportion of the fund that can be redeemed at once, and a suspension allows the manager to stop redemptions altogether.

The important reading is the interaction. A fund with a one-year lockup and a quarterly gate can take considerably longer than a year to exit if others redeem first, and the investor's position in the queue is determined by mechanics rather than by need. Recording the terms as a timeline under a stress assumption, rather than as a list of provisions, is what shows the actual exit horizon.

Primary sources: <https://www.sec.gov/investor> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the lockup, notice period, and redemption frequency.
- Record the gate as a percentage of the fund and the method of allocation.
- Record any suspension provision and who may invoke it.
- Record the side-pocket or designated-investment treatment for illiquid assets.
- Construct a stress timeline showing the exit horizon if redemptions are heavy.
- Record the terms under which the manager may change them, and the notice required.

## Procedure

1. Record the lockup and notice terms.
2. Record gates and their allocation method.
3. Record suspension provisions.
4. Record side-pocket treatment.
5. Build the stress exit timeline.
6. Write the liquidity assessment.

## Anti-patterns

- Reading the lockup without the gate.
- Assuming redemption requests are met in order of receipt.
- Ignoring the manager's ability to suspend.
- Overlooking side pockets that strand assets.
- Treating stated terms as unchangeable.

## Done checklist

- [ ] Lockup and notice recorded.
- [ ] Gate and allocation recorded.
- [ ] Suspension recorded.
- [ ] Side-pocket treatment recorded.
- [ ] Stress timeline built.
- [ ] Assessment written.

A further subtlety is that gates are usually applied pro rata across requesting investors rather than first-come, which changes the calculus: an investor who requests early gains nothing if the gate is pro rata, and the relevant question becomes whether the investor's need can wait for a subsequent window rather than whether they were first in the queue.

The side-pocket treatment is where the timeline most often lengthens without warning: assets moved into a side pocket are typically held until realisation, with no redemption right at all, and a fund that designates a large proportion can leave investors holding an illiquid residual long after the main vehicle has wound down.


## Sources

- Fund redemption disclosure: <https://www.sec.gov/investor>
- Investment management standards: <https://www.cfainstitute.org/>
- Fund governance research: <https://www.nber.org/>
