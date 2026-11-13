---
name: options-on-futures
domain: investing/options-on-futures
trigger: "Working out an option's expiry against the future it settles into."
anti_trigger: "Not for generic option pricing, and not for futures delivery mechanics."
scope: "The option's expiry, the future's expiry, and the gap between them."
status: seedling
---

# Options on futures

## Standard

A commodity option gives the right to buy or sell a futures contract at a stated price, and its expiry comes before the underlying future's delivery period. That ordering exists so the option can settle into a live future rather than into a contract already in delivery, and it creates two dates a trader must keep separate: the option's last trading day and the future's first notice day.

The gap between them is where the operational risk sits. A position exercised at option expiry becomes a futures position with its own margin, its own notice dates, and its own delivery obligations. A trader who treats the option's expiry as the end of the exposure will discover an obligation that arrives days later and belongs to a contract they had stopped thinking about.

Primary sources: <https://www.cmegroup.com/> and <https://www.cftc.gov/>.

## Decision rules

- Record the option's expiry and last trading day.
- Record the underlying future's expiry, first notice day, and last trading day.
- Record the gap in days between the option expiry and the future's notice day.
- Record whether exercise delivers a futures position or settles in cash.
- Record the closing plan for the delivered future, if exercise is a possibility.
- Record the exchange's automatic exercise rule for in-the-money options.

## Procedure

1. Obtain the option and the future specifications.
2. Record both expiry dates and the notice day.
3. Compute the gap between option expiry and delivery risk.
4. Record the exercise and settlement mechanism.
5. Write the plan for a delivered future position.
6. Record the automatic exercise threshold.

## Anti-patterns

- Treating the option's expiry as the end of the position.
- Ignoring the future's notice day when planning an exit.
- Assuming cash settlement when exercise delivers a future.
- Missing the automatic exercise rule for small in-the-money amounts.
- Holding an option through expiry without a decision.

## Done checklist

- [ ] Option expiry recorded.
- [ ] Future expiry and notice day recorded.
- [ ] Gap computed.
- [ ] Settlement mechanism recorded.
- [ ] Delivered-future plan written.
- [ ] Automatic exercise rule recorded.

The gap also decides the option's own volatility character: because the option expires while the future still has a life, its value at expiry is the future's value, not the spot commodity's, and any comparison with a spot-based payoff has to account for the basis between them.


## Sources

- Exchange option and futures specifications: <https://www.cmegroup.com/>
- Regulatory guidance on futures and options: <https://www.cftc.gov/>
- Investor education on commodity products: <https://www.investor.gov/introduction-investing>
