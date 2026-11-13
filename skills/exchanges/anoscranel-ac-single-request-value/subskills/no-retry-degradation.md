---
name: no-retry-degradation
domain: prompt-engineering/no-retry-degradation
trigger: "Squeezing value from the response already received instead of spending another request."
anti_trigger: "Not for platform retry budgets, and not for infrastructure resilience."
scope: "Answering from the response already received rather than burning a retry."
status: seedling
---

# No-retry degradation

## Standard

A rejected, truncated, or weak response triggers the same instinct everywhere: send it again. Under a per-request regime the retry is a full unit of currency spent on the same question, and if it fails the same way it doubles the cost without changing the answer. The metered discipline inverts the instinct: before re-spending, extract everything the first response contains, then decide between a degraded path forward and a targeted follow-up — a follow-up that references the response already in hand, not a from-scratch re-request.

The distinction is between retry and remediation. A retry resends the same request hoping for a better roll; remediation reads the failure's shape — rejection code, truncation point, weak section — and sends the smallest follow-up that converts the existing response into a usable answer. A truncated response usually contains a usable prefix; an answer with one weak section needs only that section's follow-up; and a rejection with an error code is a scheduling signal, not a prompt problem.

Primary sources: <https://docs.anthropic.com/en/api/rate-limits> and <https://sre.google/sre-book/handling-overload/>.

## Decision rules

- Read the whole response before deciding anything; the usable fraction is usually larger than it first appears.
- If the response is partial, draft the degraded deliverable from the partial before considering any further call.
- Send follow-ups that quote or reference the existing response, never a silent full re-request.
- Treat a rejection code as queueing and scheduling information; apply the backoff, do not rephrase.
- Keep the day's reserve for exactly these follow-ups; a plan with no reserve plans to fail mid-sequence.
- Record every retry temptation and its outcome; the count is the habit's measure.

## Procedure

1. On any weak response, extract every usable part before composing anything new.
2. Draft the deliverable at the degraded scope the partial supports.
3. Decide whether the gap justifies a follow-up or whether the degraded draft serves.
4. Compose the follow-up as a reference to the existing response with the specific gap named.
5. On a rejection, record the code, apply the pause, and reschedule rather than resend.
6. Log response, extraction, decision, and any follow-up in the ledger.

## Anti-patterns

- Resending the identical request after a truncation.
- Discarding a usable prefix because the ending was weak.
- A follow-up that restates the whole task instead of naming the gap.
- Repeating the send over a rate-limit code and forfeiting the pause.
- A session plan with no reserve for remediation follow-ups.

## Done checklist

- [ ] Usable fraction extracted before any new compose.
- [ ] Degraded draft attempted from the partial.
- [ ] Follow-ups reference the existing response.
- [ ] Rejections handled as scheduling, not rephrasing.
- [ ] Reserve maintained for remediation.
- [ ] Every retry temptation logged.

## Sources

- Provider rate-limit documentation, Anthropic: <https://docs.anthropic.com/en/api/rate-limits>
- Handling overload, Google SRE: <https://sre.google/sre-book/handling-overload/>
- The twelve-factor app: <https://12factor.net/>
