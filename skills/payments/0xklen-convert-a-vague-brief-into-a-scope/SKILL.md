---
name: convert-a-vague-brief-into-a-scope
description: Use when handed a prose brief like "make it faster" or "clean up auth" with no deliverables. Turn it into numbered, testable items plus an explicit out-of-scope list.
---

# Convert a vague brief into a scope

A prose brief is a wish until it is numbered and testable. "Make it faster" cannot be finished, only argued about; "p95 < 300 ms on this fixture" can.

## Procedure

1. Paste the brief verbatim into a working file. Do not start until every clause maps to a deliverable or is marked `unclear`.

2. Extract each noun and verb phrase into a candidate deliverable. A verb with no object ("improve", "clean up") is `unclear`, not done.

3. Rewrite each candidate as a testable statement with a threshold: `make it faster` becomes `p95 /api/search < 300 ms on the 10k-row fixture`.

4. Add an `Out of scope` list naming the adjacent things a reader would assume are included: staging, docs, mobile, data migration.

5. Number the items `D1..Dn`, estimate each in half-days, and flag any item over one day for splitting.

6. Send the numbered list back for a single confirmation pass; this is the cheapest point in the project to correct scope.

7. Freeze the list. Later additions go through the change-order threshold, not straight into the work.

## Pitfalls

- Starting on "clean up auth" with no definition of done, then arguing about it after the fact.

- Omitting the out-of-scope list, so every future omission reads as a defect.

- Promoting a preference ("nicer colours") into a hard deliverable and over-delivering.

- Numbering the list after the first three items were already built, so they were never confirmed.

- Writing a threshold you cannot measure (sub-second "feel") and calling it acceptance.

## Verification

```
    grep -E '^D[0-9]+:' SCOPE.md | wc -l    # every deliverable numbered and estimated
    grep -A20 'Out of scope' SCOPE.md       # explicit exclusions exist
```

Report the numbered deliverable count and the exclusions before starting.
