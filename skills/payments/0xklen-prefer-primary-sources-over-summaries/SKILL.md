---
name: prefer-primary-sources-over-summaries
description: Use when citing a fact, number, or rule. Goes to the primary document — filing, paper, spec, dataset — before trusting a secondary summary.
---

# Prefer Primary Sources Over Summaries

Every hop away from the origin adds a chance to distort. Secondary sources are useful for finding the primary one, not for quoting.

## Procedure

1. Classify each claim's source. Primary = the artifact itself (SEC filing, peer-reviewed paper, RFC, source code, court docket, raw dataset). Secondary = a news piece, blog, review, or Wikipedia citing it.
2. If the source is secondary, extract its citation and fetch the primary. For papers use the DOI: `curl -sL "https://doi.org/10.1234/abcd" -o paper.pdf`, then `pdftotext paper.pdf - | grep -n -i "<term>"`.
3. For rules and specs, read the operative clause, not the changelog summary. RFC: `curl -s https://www.rfc-editor.org/rfc/rfc8446.txt | sed -n '/^4\.1/,/^4\.2/p'`.
4. For numbers, find the table, not the abstract's rounded restatement. Note the exact denominator ("of 1,204 respondents", not "most").
5. Quote the primary verbatim with a locator (page, section, line). Paraphrase only after quoting.
6. Record the primary's version or timestamp — a spec changes and the secondary summary may predate the change.
7. If the primary is paywalled or inaccessible, say "secondary only; primary not retrieved" instead of implying you read it.

```bash
# SEC filing, primary text of the actual 10-K
curl -s -A "research contact@example.com" \
  "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000320193&type=10-K" 
```

## Pitfalls

- The abstract's "significant improvement" is often not the table's effect size; the table includes the confidence interval.
- News "according to a study" frequently misstates direction or magnitude — compare to the paper's own conclusion sentence.
- Reference implementations drift from specs; when they differ, cite both and say which governs.
- A primary source can itself be wrong; preference for primary is about traceability, not infallibility.
- Archived primaries: cite the retrieval date because the live page may have been edited.

## Verification

    grep -c 'secondary only' notes.md   # keep this count low

Each quoted figure traces to a page/section of the primary. Report: "Figure 3 in <DOI> reports 12.4% (n=1,204); the news summary said 'about 20%' — citing the paper."
