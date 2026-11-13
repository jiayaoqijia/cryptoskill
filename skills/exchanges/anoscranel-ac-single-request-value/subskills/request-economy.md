---
name: request-economy
domain: prompt-engineering/request-economy
trigger: "Understanding requests as the currency when limits or per-request pricing bind."
anti_trigger: "Not for prompt wording, and not for infrastructure cost."
scope: "Reading the limit: requests as the binding currency, and the arithmetic of allowance."
status: seedling
---

# Request economy

## Standard

A metered API has two or three overlapping currencies: requests per minute, requests per day, and sometimes tokens per minute. When the request count is the binding one — a free daily allowance, a per-minute cap, a pay-per-call tariff — the working discipline changes: the smallest measurable unit of waste is a request that returned less than it could have, and the smallest unit of planning is the session's remaining allowance.

The arithmetic is straightforward and worth writing down. An allowance of so many requests per day, against a task with a known number of sub-questions, gives the requests-per-answer ratio: how many calls the current habit burns to finish one unit of real work. A ratio of one is the target this skill drives toward; a ratio of ten means the task fails at one-tenth of its potential scale. The ratio, not the allowance, is what the operator controls.

Primary sources: <https://docs.anthropic.com/en/api/rate-limits> and <https://ai.google.dev/gemini-api/docs/rate-limits>.

## Decision rules

- Identify which currency binds: requests per minute, per day, or price per request.
- Compute and write down the requests-per-answer ratio for the current working habit.
- Reserve a fraction of the daily allowance for corrections before starting a long sequence.
- Treat a mid-sequence exhaustion as a design failure to be prevented, not bad luck.
- Prefer one dense request over several thin ones when the answers share context.
- Re-check the vendor's current published limit page before a run that depends on it; limits differ by tier, model, and programme, and they change.

## Procedure

1. Read the provider's limits page and record the numbers with the date.
2. Count the requests the current habit burns per finished answer.
3. Compute the ratio and the maximum answers per allowance.
4. Set aside the correction reserve, then plan the day's sequences within the remainder.
5. After each run, recompute the ratio from the ledger; the trend is the skill's measure.
6. Lower the ratio by moving work into fewer, better-prepared requests.

## Anti-patterns

- Optimising token count while the request count is the binding limit.
- Starting a long multi-request sequence with the allowance nearly exhausted.
- Treating the allowance as stable across sessions without re-reading the limits page.
- Retrying a rejected request immediately instead of rescheduling it.
- Letting the ratio live in intuition instead of the ledger.

## Done checklist

- [ ] Binding currency identified from the vendor's page, with date.
- [ ] Requests-per-answer ratio computed and recorded.
- [ ] Correction reserve set aside.
- [ ] Daily sequences planned within the allowance remainder.
- [ ] Ratio re-measured after each run from the ledger.
- [ ] Mid-sequence exhaustion designed out.

## Sources

- Provider rate-limit documentation, Anthropic: <https://docs.anthropic.com/en/api/rate-limits>
- Provider rate-limit documentation, Google: <https://ai.google.dev/gemini-api/docs/rate-limits>
- Provider rate-limit documentation, OpenAI: <https://platform.openai.com/docs/guides/rate-limits>
