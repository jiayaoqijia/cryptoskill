---
name: debug-prompt
domain: prompt-engineering/debug-prompt
trigger: "When a prompt underperforms, the model refuses, quality drops after an edit, or an agent misbehaves."
anti_trigger: "The output is fine and the job is to prove it stays fine — that is evaluation work."
scope: "The ordered triage of a failing prompt: read the raw output first, wording last."
status: "seedling"
---

# Debug a failing prompt

## Standard

The debugging order is ranked by expected value per hour, and it is roughly the reverse
of what most people try (<https://ai.google.dev/gemini-api/docs/prompting-strategies> §5):

1. **Read the failing output in full.** About half of "bad prompt" reports are
 truncation or wrong-document retrieval. Look at the actual raw text before changing
 anything.
2. **Add missing information.** Ask: could a competent human succeed with only this
 context? If not, the prompt is not the problem; the context is.
3. **Show the output shape; do not describe it.** One exemplar beats a paragraph of
 format prose.
4. **Enforce the shape mechanically** with a JSON schema parameter where supported.
5. **Decompose multi-duty calls.** Retrieve-plus-decide-plus-format in one call is a
 known failure shape.
6. **Change the model.** Cheaper than a week of prompt archaeology.
7. **Only now, wording.** Micro-copy is real but small and does not transfer between
 model families.

For agent setups, also check the harnesses class of causes before wording: is the tool
catalog itself ambiguous, is context rot degrading recall, is a guardrail firing
upstream of the model (<https://learn.microsoft.com/en-us/security/zero-trust/sfi/defend-indirect-prompt-injection>).

Primary sources: <https://www.anthropic.com/engineering/building-effective-agents> and <https://ai.google.dev/gemini-api/docs/prompting-strategies>.

## Procedure

1. Capture the raw input and raw output verbatim; note model, snapshot, temperature.
2. Run the ordered checks above; stop at the first one that explains the failure.
3. Fix exactly one thing. If two fixes tempt you, pick the higher-ranked one first.
4. Re-run the same input three-plus times to rule out sampling luck.
5. Add the failing input to the golden set so the fix regresses loudly if it returns.
6. If the fix was wording, write the failing and passing outputs side by side into the
 golden set comments.

## Decision rules

| Failure shape | First suspect |
|---|---|
| Empty, cut off, or partial answer | Truncation or max-tokens, not the prompt |
| Answers the wrong question | Missing context or retrieval sent the wrong document |
| Right content, wrong shape | Shape not shown and not enforced |
| Intermittent failure | Temperature above 0, or an unseeded sampling path |
| Sudden drop after a model update | Model drift; test before touching the prompt |

## Anti-patterns

- Rewriting prose first; wording is the last resort on this ladder.
- Changing three things at once; the fix becomes unattributable.
- Debugging from a memory of the output instead of the raw output.

## Done checklist

- [ ] The failure was reproduced on the raw transcript.
- [ ] The fix maps to exactly one rung of the ladder.
- [ ] The failing case now lives in the golden set.

## Sources

- <https://www.anthropic.com/engineering/building-effective-agents>
- <https://ai.google.dev/gemini-api/docs/prompting-strategies>
