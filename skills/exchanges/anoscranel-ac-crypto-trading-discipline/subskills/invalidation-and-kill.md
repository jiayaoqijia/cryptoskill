---
name: invalidation-and-kill
domain: crypto-trading/invalidation-and-kill
trigger: "Pre-committing invalidation conditions, price/time/thesis/data triggers, and mandatory kill criteria"
anti_trigger: "Holding positions past invalidation points in hope of recovery; removing stop-loss orders during drawdowns"
scope: "Pre-committed invalidation conditions (price, time, thesis, data); kill criteria closing positions; review triggers"
status: seedling
---

# Invalidation and Kill

## Standard

- **Klein, _The Power of Intuition_ / Pre-Mortem (2007)**: prospective simulation of failure before execution reveals hidden vulnerabilities and establishes non-negotiable exit triggers. <https://www.crownpublishing.com/book/9780385511874/>
- **Kahneman, _Thinking, Fast and Slow_ (2011)**: loss aversion causes decision-makers to maintain failing courses of action; pre-committed rules bypass emotional attachment. ⚠️ cited without URL.
- **Popper, _The Logic of Scientific Discovery_ (1934)**: a proposition is only valid if it specifies in advance the exact observational evidence that would falsify it. <https://www.taylorfrancis.com/books/mono/10.4324/9780203994627/logic-scientific-discovery-karl-popper>
- **Thaler, "Mental Accounting Matters" (1999)**: pre-commitment devices protect decision-makers from sunk cost fallacies and emotional hold strategies. <https://www.jstor.org/stable/117326>
- ⚠️ Practitioner heuristic: an invalidation rule must be binary and automated where possible; if human discretion is required to execute a kill order, the failure rate increases significantly.

## Decision rules

1. Every position must have pre-committed invalidation conditions defined across four dimensions: price, time, thesis, and data.
2. Price invalidation is absolute; reaching the predetermined stop level requires immediate exit without exception or manual intervention.
3. Time invalidation mandates closure if the market fails to reach anticipated structural milestones within the specified horizon.
4. Thesis invalidation requires exit when the underlying operational or structural assumptions of the pre-trade memo are disproven by incoming data.
5. Kill criteria are binding constraints that close positions regardless of current profit or loss status; overriding a kill criterion is a critical protocol violation.
6. When neither profit target nor invalidation triggers within the maximum time window, a mandatory review and close rule applies.
7. ⚠️ House: removing or widening an invalidation stop after order placement is recorded as an unmitigated protocol breach.

## Procedure

1. Define the exact price level where technical invalidation occurs during pre-trade memo preparation.
2. Establish the maximum holding time horizon (in hours or days) before trade entry.
3. List specific data-dependent invalidation markers (e.g., metric shifts, structural breaks) in the memo.
4. Program automated execution triggers or set rigid alerts for price and time invalidation thresholds.
5. Monitor active positions continuously against the four invalidation dimensions.
6. Upon breach of any invalidation condition, execute the kill order immediately and record the exit timestamp and reason.
7. File an incident report in the journal if human hesitation delayed the execution of any kill criterion.

## Anti-patterns

- **Moving the stop loss.** Widening the invalidation distance as price approaches the stop level. Fix: treat stop modifications as forbidden; accept the loss according to plan.
- **Holding past time horizon.** Maintaining a stagnant position long past its scheduled completion time. Fix: enforce automatic time-based exits when the horizon expires.
- **Hope-based management.** Refusing to close a failing position because "it might bounce back." Fix: replace hope with binary invalidation rules.
- **Discretionary overrides.** Using subjective judgment to ignore a triggered thesis invalidation. Fix: make invalidation rules strictly mechanical and non-negotiable.

## Done checklist

- [ ] Price invalidation level is defined and locked before entry.
- [ ] Time horizon and expiration limit are established.
- [ ] Thesis and data invalidation markers are documented in the memo.
- [ ] Kill criteria are programmed or set for immediate execution upon breach.
- [ ] No stop-loss widening or manual override occurred during the trade lifecycle.

## Sources

- Klein, _The Power of Intuition_ / Pre-Mortem: <https://www.crownpublishing.com/book/9780385511874/>
- Kahneman, _Thinking, Fast and Slow_: ⚠️ cited without URL.
- Popper, _The Logic of Scientific Discovery_: <https://www.taylorfrancis.com/books/mono/10.4324/9780203994627/logic-scientific-discovery-karl-popper>

⚠️ Gaps: network congestion or exchange outages during high-volatility events can delay the execution of automated stop-loss orders, exposing positions to slippage beyond planned invalidation levels.
