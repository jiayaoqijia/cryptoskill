# Bounded Novelty Assessment

Use only when the request concerns originality, prior art, “first” claims, closest work, or whether a candidate contribution appears previously known.

## 1. Decompose the candidate contribution

Create independently searchable claims:

| Claim ID | Object/construction | Property/notion | Model/setup | Assumption | Parameter regime | Claimed difference |
|---|---|---|---|---|---|---|

A contribution may be new in one dimension and known in another. Do not treat a new implementation, proof technique, parameter point, model, or functionality as the same type of novelty.

## 2. Identify closest work

Closest work is selected by formal overlap, not title/abstract similarity. Compare:

| Work/version | Construction/problem | Security notion/model | Assumptions | Parameters | Functionality | Proof basis | Compatible cost | Difference |
|---|---|---|---|---|---|---|---|---|

Align terminology and cost models before judging differences. A stronger claim under a stronger assumption may not dominate a weaker-assumption result.

## 3. Seek disconfirming evidence

Actively search:

- historical and alternative terminology;
- earlier/extended/corrected versions;
- cited predecessors and later citations;
- adjacent fields using different notation;
- negative results, impossibility results, attacks, and corrections;
- surveys/theses/standards as maps to primary sources;
- relevant unpublished/patent/non-English sources only when included in scope.

## 4. Grade the conclusion

| Grade | Allowed conclusion |
|---|---|
| Not assessable | Claim or search coverage is too vague/inaccessible |
| Partial prior-art map | Relevant work found, but major source/query gaps remain |
| Strong bounded negative search | No match found after documented multi-source, synonym, and citation chaining under a stopping rule |
| Matching prior art found | An inspected source materially matches the candidate claim |

No grade proves global novelty.

## 5. Required final wording

Use this shape:

> No earlier result matching criteria **X** was found in sources **Y**, using query families **Z**, with cutoff **D** and stopping rule **R**. The closest inspected works are **A/B/C** and differ in **M/N/P**. Coverage excludes or could not verify **G**. This is a bounded search conclusion, not proof of global novelty.

If matching prior art is found, identify the exact version and claim location and compare it against each candidate contribution claim.

## 6. Prohibited shortcuts

- one database or one query as global evidence;
- absence from arXiv/ePrint as absence from the literature;
- title/abstract similarity as a complete claim comparison;
- citation counts as priority evidence;
- treating an inaccessible source as either supporting or disproving novelty;
- using “first,” “unprecedented,” or “novel” without the bounded coverage statement.

