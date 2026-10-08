---
name: test-an-eval-for-gaming-shortcuts
description: Use when an eval score could be won without doing the task. Probes for length, format, and keyword shortcuts a model can exploit.
---

# Test an Eval for Gaming Shortcuts

Some evals are passable without solving the problem: answer the most common label, pad the length, match the format. Find the shortcut before your model does.

## Procedure

1. Build a trivial baseline that ignores the input: majority-class, always-yes, longest-output, or the most frequent answer string.
2. Report that baseline. If the model only beats majority-class by 2 points, the eval mostly measures the label prior.
3. Check the length prior: correlate score with output length. A judge that rewards verbosity makes "write more" a strategy.
   ```python
   import pandas as pd
   d = pd.read_json("results.jsonl", lines=True)
   print(d[["score", "out_tokens"]].corr())    # |r|>0.3 signals a length shortcut
   ```
4. Check the format prior: does matching the expected structure (a bullet list, a JSON key) alone earn points? Score a format-only response with no content.
5. Check lexical overlap: compute score vs word-overlap with the reference. High overlap-only scoring rewards echoing the question.
6. Add a shortcut-resistant variant: shuffle option order, paraphrase the reference, or require reasoning the echo cannot fake.
7. Keep the trivial baselines in the eval so a future model cannot quietly win on them.

```python
from collections import Counter
majority = Counter(labels).most_common(1)[0][1] / len(labels)   # baseline floor
```

## Pitfalls

- Forgetting the majority-class baseline makes a mediocre model look good.
- A substring-match scorer rewards saying the answer token anywhere, including in a refusal.
- Length in tokens vs characters changes the correlation; pick one and state it.
- A shortcut found by one system may be exploited harder by the next; treat it as a standing bug.
- Fixing the scorer but not re-running past results leaves an inconsistent historical record.

## Verification

    python3 eval.py --baseline majority-class --report-shortcuts   # prints baseline floor and length r

Report: "Majority baseline 0.58; our model 0.61 — a 3-point margin over a no-input rule, and score-length r=0.41. Eval declared weakly discriminating; scorer tightened."
