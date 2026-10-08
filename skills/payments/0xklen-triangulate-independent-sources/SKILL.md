---
name: triangulate-independent-sources
description: Use when a factual claim rests on a single source. Confirms it against at least two independent origins before repeating it.
---

# Triangulate Independent Sources

A claim is only as strong as the number of *independent* places it survives. Two articles quoting the same press release are one source, not two.

## Procedure

1. List every load-bearing factual claim in the answer. A claim is load-bearing when deleting it changes the conclusion.
2. For each claim record: URL, publisher, named author, publication date, and — critically — the origin that source cites.
3. Trace citations to their root. Run `curl -sL "<url>" | grep -oE 'https?://[^" ]+' | head`, then follow the first upstream link. If two sources resolve to the same root document, count them once.
4. Score independence. Two sources are independent only if they differ in at least two of: publisher, underlying data, named author, funding source.
5. Label each claim `[triangulated: N]`, `[single-source]`, or `[contradicted]` inline.
6. When sources disagree, keep both figures and name the disagreement. Never average two conflicting numbers into one.
7. If no second independent source exists, write `single-sourced from <X>` rather than quietly deleting the hedge.

A cheap independence probe:

```python
import hashlib, urllib.request
def fingerprint(url):
    body = urllib.request.urlopen(url, timeout=10).read()
    return hashlib.sha256(body).hexdigest()[:12]
# equal digests -> same upstream text -> one source
```

## Pitfalls

- Syndication: one wire story printed in 40 outlets reads like 40 sources. Grep for the wire credit ("Reuters", "AP") and collapse them.
- Circular reporting: an aggregator cites a blog that cites the aggregator back.
- Date collapse: several pieces from the same 24-hour news cycle usually share one origin.
- Silence is not denial — a source failing to mention a claim does not refute it.
- Two papers by the same group on the same cohort are not independent replications.

## Verification

    grep -c '\[single-source\]' answer.md

Every load-bearing claim is either triangulated across 2+ independent sources or explicitly marked single-source. Report: "Claim X triangulated across 2 independent sources (common origin suppressed); claim Z remains single-sourced and is flagged."
