---
name: choose-few-shot-examples-for-coverage
description: Use when adding examples to a prompt. Select for coverage of the input space and the hard cases, not for the typical case, and keep the set small enough to read.
---

# Choose few-shot examples for coverage

Examples teach by demonstration, so their value is the space they cover, not how many you have. A handful of well-chosen, correctly-labelled cases beats twenty near-twins.

## Procedure

1. List the axes of variation in your real inputs: length, format, language, missing fields, edge values (empty, max, negative), and known confusions between two classes.

2. Pick examples that each occupy a different cell of that grid. Deliberately include the classes the model most often mixes up.

3. Include the rare-but-important case: the null field, the multi-line address, the one where two entities share a name.

4. Keep each example formatted exactly like the real input — same `snake_case` field names, same casing — or the model copies the demo's surface style onto the wrong output.

5. Order matters: put the most representative example last (recency), and keep class examples balanced so the final one does not bias the label prior.

6. Cap the set: 3-8 for extraction, more only if accuracy on your sample keeps rising. Measure each addition against the golden set.

7. Verify every example label by hand. One wrong demo teaches the wrong thing with high confidence.

8. Track the block's cost — examples are input tokens on every call — and keep the whole set under ~10% of your context budget.

9. Prune examples that stop pulling weight: if removing one leaves the golden score unchanged, delete it — a shorter set is cheaper and less able to overfit.

## Pitfalls

- Choosing only clean, typical examples; the model then fails on exactly the messy inputs you have in production.
- Enormous example sets that eat the context budget and dilute attention while adding no coverage.
- Class imbalance in the demos — five positives and one negative biases the output toward positive.
- Inconsistent formatting between examples and live input, which the model faithfully reproduces as noise.
- Copying a public example that uses a different label scheme than yours.
- Reusing examples from a different domain because they "look similar"; the model learns the wrong surface form.
- Adding an example that contradicts another; the model sees inconsistent labels and hedges on the ambiguous input.
- Letting the set grow to twenty because each example helped once; the marginal ones now crowd the budget.

## Verification

    python3 -c "import json;c=json.load(open('examples.json'));print(len(c), len({e['type'] for e in c}))"  # cases vs distinct types covered

Report: "6 examples covering 6 of 6 input axes (including the null-field and two-entity-same-name cases); golden-set accuracy rose 8 points after adding the confusion pair."
