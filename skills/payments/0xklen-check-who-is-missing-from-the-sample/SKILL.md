---
name: check-who-is-missing-from-the-sample
description: Use when generalising from a sample, survey, or review corpus. Names the population excluded by the sampling frame before stating any rate.
---

# Check Who Is Missing From the Sample

A percentage is meaningless until you know who had no chance to be counted. State the sampling frame and the excluded majority before quoting any rate.

## Procedure

1. Write the target population in one line ("all US adults who applied for a mortgage in 2024").
2. Write the actual sampling frame: where respondents could realistically come from (online panel, app users, paper returns, scraped reviews). Name it explicitly.
3. Enumerate exclusions. Every frame drops people: no internet, no email, deleted their account, left no review, language other than English, died, moved. List at least the plausible ones.
4. Quantify the response rate. `responses / invited`. A 3% response rate on a survey of 100,000 is a 3,000-person study of whoever answers surveys — not 100,000 people.
5. For scraped corpora, check survivorship: reviews that were deleted, products that were removed, posts by banned users.
6. Test whether the missing are plausibly different on the outcome. Compare a known covariate of responders vs non-responders if you have any.
7. State the generalisation limit in the output: "this describes online-panel adults, not all adults."

```python
invited, responded = 100000, 3000
print(f"response rate {responded/invited:.1%}")   # 3.0%
# with a 3% rate, nonresponse bias can dominate any estimated proportion
```

## Pitfalls

- Convenience samples (MTurk, Prolific, Twitter, app reviews) skew young, urban, and online; rates do not transfer to the general population.
- Selection on the outcome: asking people who bought the product whether they like it.
- Response bias operates in a direction — the angry and the delighted answer, the neutral do not.
- Hard-to-reach groups are exactly the ones at the tail of most distributions.
- Weighting fixes representativeness only for covariates you measured and weighted on.

## Verification

    grep -iE 'response rate|sampling frame|excluded' report.md

Report: "Sample = 3,000 online-panel respondents (3.0% response rate); describes engaged panel members, not all applicants — generalisation limited accordingly."
