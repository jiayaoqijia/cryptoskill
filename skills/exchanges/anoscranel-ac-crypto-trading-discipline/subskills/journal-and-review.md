---
name: journal-and-review
domain: crypto-trading/journal-and-review
trigger: "Recording trade audit trails, separating outcome and process review, conducting periodic journal audits"
anti_trigger: "Evaluating decisions solely based on financial profit or loss; failing to record pre-trade assumptions"
scope: "The journal as audit trail: memo reference, execution, exit reason, evidence; outcome vs process review; periodic cadence"
status: seedling
---

# Journal and Review

## Standard

- **Montier, _The Little Book of Behavioural Investing_ (2010)**: keeping a structured decision journal prevents hindsight bias and forces objective evaluation of reasoning over randomness. <https://www.wiley.com/en-us/The+Little+Book+of+Behavioural+Investing%3A+How+To+Act+More+Intelligently+Than+Your+5+Friends-p-9780470686157>
- **Kahneman, _Thinking, Fast and Slow_ (2011)**: distinguishing between outcome quality and decision quality prevents rewarding poor processes that happened to succeed. ⚠️ cited without URL.
- **Duhigg, _The Power of Habit_ (2012)**: systematic review loops create feedback mechanisms that reinforce disciplined operational habits. <https://www.penguinrandomhouse.com/books/209177/the-power-of-habit-by-charles-duhigg/>
- **Endsley, "Toward a Theory of Situation Awareness in Dynamic Systems" (1995)**: post-decision reviews must audit the information available at decision time rather than evaluating with hindsight omniscience. <https://journals.sagepub.com/doi/10.1518/001872095779049543>
- ⚠️ Practitioner heuristic: review sessions should evaluate process adherence on every trade regardless of financial result; a winning trade executed outside protocol is classified as a failure.

## Decision rules

1. Every completed trade must have an immutable journal entry linking the pre-trade memo, execution fills, exit timestamp, and final PnL.
2. Review must strictly separate outcome (did it make money?) from process (was the pre-trade plan followed precisely?).
3. Winning trades executed in violation of protocol receive a negative process grade and trigger a mandatory behavioral review.
4. Losing trades executed in strict accordance with protocol receive a positive process grade and require no behavioral correction.
5. Periodic review cadence is mandatory: weekly summary of all trade records and monthly aggregation of process compliance metrics.
6. Hindsight bias is actively suppressed by evaluating decisions using only the data recorded in the pre-trade memo at entry time.
7. ⚠️ House: maintaining a trading journal with omitted entries or altered histories invalidates the desk operational record.

## Procedure

1. Archive the pre-trade memo upon trade closure, appending actual entry and exit execution timestamps.
2. Record the exact exit reason (price invalidation, time expiration, thesis completion, or manual kill).
3. Calculate process adherence: check whether pre-trade memo, risk budget, sizing rules, and invalidation stops were followed without deviation.
4. Assign a binary process grade (compliant vs non-compliant) and a financial outcome grade (profit vs loss).
5. Compile weekly review logs: aggregate all trade records into a single performance and discipline summary file.
6. Conduct monthly audits of process compliance rates to detect emerging behavioral drift or rule degradation.
7. Store all journal files in the designated audit repository with secure, unalterable version control.

## Anti-patterns

- **Outcome-based evaluation.** Praising poor discipline because a trade happened to make money. Fix: judge trades solely on process compliance, ignoring financial outcome.
- **Hindsight re-evaluation.** Criticizing a correct decision because subsequent news events changed market direction. Fix: evaluate decisions based strictly on information available at entry.
- **Skipping the journal.** Failing to record trades that felt insignificant or minor. Fix: enforce mandatory journaling for every single market exposure.
- **Vague exit notes.** Writing "closed manually" without specifying which rule or condition prompted the exit. Fix: record the exact invalidation or thesis completion trigger.

## Done checklist

- [ ] Every trade record links memo, execution, and exit data.
- [ ] Process review is explicitly separated from financial outcome.
- [ ] Protocol violations are flagged and investigated regardless of profit.
- [ ] Weekly and monthly review cadences are maintained.
- [ ] Journal entries remain unedited after trade closure.

## Sources

- Montier, _The Little Book of Behavioural Investing_: <https://www.wiley.com/en-us/The+Little+Book+of+Behavioural+Investing%3A+How+To+Act+More+Intelligently+Than+Your+5+Friends-p-9780470686157>
- Kahneman, _Thinking, Fast and Slow_: ⚠️ cited without URL.
- Endsley, "Toward a Theory of Situation Awareness in Dynamic Systems": <https://journals.sagepub.com/doi/10.1518/001872095779049543>

⚠️ Gaps: subjective bias in self-evaluating process adherence can lead operators to rationalize minor protocol deviations during profitable trades.
