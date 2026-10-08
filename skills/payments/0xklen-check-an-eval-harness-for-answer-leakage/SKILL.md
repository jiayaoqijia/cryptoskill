---
name: check-an-eval-harness-for-answer-leakage
description: Use when eval scores are surprisingly high. Audits prompt construction and scoring for the gold answer or its hint leaking into the model's input.
---

# Check an Eval Harness for Answer Leakage

High scores usually come from a bug in the harness, not a leap in ability. The commonest bug is the answer reaching the model through the prompt or the retrieved context.

## Procedure

1. Print the exact string sent to the model for three items and read it. If the gold answer appears, you found the bug.
   ```python
   import itertools
   for row in itertools.islice(stream, 3):
       print("=== PROMPT ===", build_prompt(row))
   ```
2. Check the answer field is not in the prompt template — a `{row}` f-string that renders the whole record leaks the label.
3. Check retrieved context and tool outputs for the answer; a RAG eval that retrieves the gold snippet scores on copying.
4. Check the few-shot examples against the test items. Overlapping near-duplicates leak through the exemplars.
5. Check the scorer separately: a substring match against the full expected string passes on a partial echo.
6. Run a null control — a model given the prompt with the answer blanked should score near chance. If it still scores high, the answer leaks elsewhere.
7. Re-run after the fix and compare; the drop is the size of the leak.

```python
assert gold not in prompt, "gold answer leaked into the prompt"
```

## Pitfalls

- A f-string template with the whole row object leaks every field, including the label.
- Few-shot examples often overlap the test set; deduplicate before accepting the score.
- Retrieval returning the exact source of the gold answer is a copying eval, not a reasoning eval.
- A lenient scorer passing on a partial match masquerades as capability.
- An easy split with no leakage still scores high — confirm item difficulty, not just the plumbing.

## Verification

    python3 eval.py --dump-prompts 3 | grep -F "$GOLD" ; echo "exit=$?"   # exit 1 = no leak found

Report: "The answer field was rendered into the prompt via an f-string; fixed and re-run dropped 94% -> 71%. Leak size = 23 points."
