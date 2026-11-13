---
name: prime-brokerage
domain: investing/prime-brokerage
trigger: "Working out what a prime broker does and what it obliges."
anti_trigger: "Not for recommending a provider, and not for legal advice."
scope: "Give-ups, custody of positions, financing, and the prime broker's role."
status: seedling
---

# Prime brokerage

## Standard

A prime broker sits between a fund and the executing brokers. The fund executes with many brokers; the prime broker clears and settles centrally, holds the positions, finances them, and provides the reporting that ties the whole picture together. The mechanism that makes this work is the give-up: the executing broker gives the trade up to the prime broker, who becomes the counterparty for settlement.

The arrangement concentrates two things. It concentrates operational dependency, because the fund's ability to settle depends on one entity's systems, and it concentrates counterparty exposure, because the financing is secured on the positions the prime broker also holds. The terms that matter are the ones governing rehypothecation, cross-default, and the circumstances in which positions can be liquidated — and those are read before the account is opened, not after.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## Decision rules

- Record the prime broker's role: clearing, custody, financing, or all three.
- Record the give-up arrangements with each executing broker.
- Record what may be rehypothecated and on what terms.
- Record the financing terms, including rates and collateral eligibility.
- Record the events that permit the prime broker to liquidate positions.
- Record the reporting frequency and the reconciliation process.

## Procedure

1. Map the entities and each one's role.
2. Record give-up arrangements and their mechanics.
3. Record rehypothecation and collateral terms.
4. Record financing rates and eligibility.
5. Record default and liquidation triggers.
6. Write the arrangement summary with the obligations named.

## Anti-patterns

- Treating the prime broker as a service provider with no counterparty risk.
- Ignoring rehypothecation terms.
- Assuming positions held at the prime broker are bankruptcy-remote.
- Overlooking cross-default clauses.
- Reading one agreement clause without the schedule that qualifies it.

## Done checklist

- [ ] Roles mapped.
- [ ] Give-ups recorded.
- [ ] Rehypothecation recorded.
- [ ] Financing terms recorded.
- [ ] Liquidation triggers recorded.
- [ ] Reporting and reconciliation recorded.

The dependency also runs through the give-up: because the prime broker becomes the settlement counterparty, a disruption at the prime broker affects trades executed elsewhere, and a fund that has diversified its executing brokers may still have a single point of failure in the entity that clears them all.


The reporting is also where the concentration becomes visible: a fund using one prime broker sees its whole book in one statement, which is convenient and also the reason a failure at that entity affects every position at once rather than a segment of them.


## Sources

- Broker-dealer regulation and custody context: <https://www.sec.gov/investor>
- Market infrastructure and collateral standards: <https://www.bis.org/>
- Investor education on brokerage arrangements: <https://www.investor.gov/introduction-investing>
