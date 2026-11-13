---
name: inclusive-accessible
domain: writing/inclusive-accessible
trigger: "\"is this biased\", \"inclusive-language pass\", \"alt text\", \"accessible version\", \"easy read\"."
anti_trigger: "General plain-language rewriting (subskills/plain-language.md); scoring readability (subskills/readability-measures.md)."
scope: "Bias-free terms, alt text, link text, heading order, reading-level for access"
status: "seedling"
---

# Inclusive & accessible text

## Standard

- **Bias-free language is codified.**
 APA 7's guidelines cover age, disability, gender, participation in research, racial and ethnic identity, sexual orientation, socioeconomic status and intersectionality (https://apastyle.apa.org/style-grammar-guidelines/bias-free-language).
 Precedence rule for disability: "the expressed preference of people with disabilities regarding identification supersedes matters of style".
- **Pronouns.** CMOS 18 (19 Sep 2024) endorses the generic singular "they" (CMOS 5.51, 5.266; https://www.chicagomanualofstyle.org/help-tools/what-s-new.html ⚠️ body paywalled; read from the free change list). It applies to a person whose gender is unknown, unspecified or concealed.
- **WCAG 2.2 (W3C Recommendation, Oct 2023):** SC 1.1.1 alt text carries the information, not "image of"; SC 2.4.4 link text identifies the destination out of context; SC 1.3.1 headings, lists and tables marked so structure survives; SC 3.1.5 Reading Level (https://www.w3.org/TR/WCAG22/).
- **Reading level is a Level AAA trigger with one consequence:** above lower secondary reading ability, a *supplemental* version must exist. Simpler text is not mandated, and AAA is never a conformance requirement (https://w3.org/WAI/WCAG22/Understanding/reading-level.html).
- **Easy Read is a stricter register:** short sentences, one idea each, active voice, defined terms (https://arxiv.org/pdf/2509.11991). Metrics alone are insufficient; validate with a target reader.

## Decision rules

1. Person-first versus identity-first: the community's stated preference beats any guide.
2. Singular "they" for unknown gender; the person's own pronoun where known.
3. Alt text carries the image's function here. Decorative images take empty alt.
4. Link text names the destination. Never "click here" or a bare URL.
5. Headings descend one level at a time; never chosen for font size.
6. Simplify only where the audience needs it. ⚠️ High-familiarity readers skipped over-simplified summaries, including study limitations (https://dl.acm.org/doi/10.1145/3613904.3642289). Keep expert text precise; add the supplement.
7. Plain vocabulary is an access need, not a machine tell: simple prose is what gets non-native writers falsely flagged (https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961).

## Procedure

1. Audit terms: roles, groups, disabilities, ages. Replace birthplace-for-identity, gendered defaults, euphemisms.
2. Apply precedence: stated identity, then community convention, then guide. Record choices on the style sheet.
3. Write alt text for each informative image: what it shows, why it matters, one sentence. Mark decorative images.
4. Rewrite link text to name the destination; check each link out of context.
5. Check heading sequence, header rows on tables, real list markup.
6. Add plain-language or Easy Read supplements alongside expert text, never instead.
7. Test: one screen-reader pass, one reader from the target group. Log failures.

## Anti-patterns

- Defining a group's term over the group's stated preference.
- Alt text that describes pixels instead of information.
- "Click here" links and bare URLs.
- Simplifying expert text until precision is gone.
- Treating plain vocabulary as an AI tell.

## Done checklist

- [ ] Term audit done; preferences on the style sheet.
- [ ] Pronouns correct; alt text functional.
- [ ] Link text meaningful out of context.
- [ ] Heading order sequential; tables and lists structural.
- [ ] Supplements added; expert precision kept.
- [ ] Screen-reader and target-reader test logged.

## Sources

- https://apastyle.apa.org/style-grammar-guidelines/bias-free-language
- https://www.chicagomanualofstyle.org/help-tools/what-s-new.html · https://www.w3.org/TR/WCAG22/
- https://dl.acm.org/doi/10.1145/3613904.3642289 · https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961
- <https://arxiv.org/pdf/2509.11991>
- <https://owl.purdue.edu/owl/subject_specific_writing/journalism_and_journalistic_writing/ap_style.html>
