---
name: export-plan-review-comments
description: Export the survived comments from a completed implementation-plan review into a timestamped Markdown findings artifact. Use when the user asks to save, write, or export plan-review comments/findings under `.ai/impl_plans/PLAN_ID/findings/REVIEW_TIMESTAMP/finding.md` while preserving the original review wording and wrapping each finding in paired `comment` markers.
disable-model-invocation: true
---

# Export Plan Review Comments

Export the final review comments without re-reviewing the plan, changing verdicts, or implementing anything.

## Resolve the source and target

1. Identify exactly one plan file from the user request or the completed review:

   ```text
   .ai/impl_plans/<plan-id>.md
   ```

   If more than one plan is plausible, ask instead of guessing.

2. Resolve the review timestamp from the exact scratchpad paths cited by the comments:

   ```text
   .ai/impl_plans/<plan-id>/scratchpads/<YYMMDD-HHMM>/...
   ```

   Reuse that timestamp verbatim. Do not generate the current time, glob scratchpad directories, or reuse a timestamp from another review. If no exact review timestamp is recoverable, ask the user.

3. Write to:

   ```text
   .ai/impl_plans/<plan-id>/findings/<YYMMDD-HHMM>/finding.md
   ```

4. Treat every item actually present in the final review's actionable-comments section as one survived finding. Do not export summaries, coverage notes, closed candidates, intermediate commentary, or test-checklist repetitions.

## Preserve each comment

- Keep the original review wording almost verbatim.
- Do not normalize findings into a new schema.
- Do not rewrite links, severity labels, verdicts, recommendations, rationales, action text, or scratchpad paths.
- Make only a tiny edit when required to make a finding understandable on its own.
- Keep the original numbering text inside the block body.
- Preserve Markdown lists and blank lines within a comment.

Wrap each finding in a separate region:

```markdown
<!-- comment:begin slug="concise-kebab-case-slug" -->
1. **Severity:** Major
   **Location:** ...
   **Problem:** ...
   **Recommendation:** ...
   **Rationale:** ...
   **Scratchpad:** ...
<!-- comment:end slug="concise-kebab-case-slug" -->
```

Use a unique lowercase kebab-case slug. The begin and end slugs must match. Keep only blank lines between regions and no document-level introduction or summary.

## Write safely

- Create only the timestamped findings directory and `finding.md`.
- Use `apply_patch` for the file content.
- Do not modify the implementation plan, scratchpads, application code, tests, or documentation.
- If the target already exists with different content, do not overwrite it unless the user explicitly requested replacement or update.

## Validate

Run the bundled validator with the exact number of exported review comments:

```bash
python3 .agents/skills/export-plan-review-comments/scripts/validate_comments_export.py \
  .ai/impl_plans/<plan-id>/findings/<YYMMDD-HHMM>/finding.md \
  --expected-count <count>
```

Fix every validation error before finishing. Then read the file once to confirm that wording and links still match the source comments.

## Respond

Reply with only a clickable link to the created file:

```markdown
[.ai/impl_plans/<plan-id>/findings/<YYMMDD-HHMM>/finding.md](.ai/impl_plans/<plan-id>/findings/<YYMMDD-HHMM>/finding.md)
```
