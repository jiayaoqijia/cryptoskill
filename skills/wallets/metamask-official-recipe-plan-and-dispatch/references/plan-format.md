# Plan format

A cheaper model follows this plan as written. Make it exact and complete, so nothing is left to interpret or rediscover.

## Rules

- No noise. Every line carries a fact the worker acts on. Cut background, history, restated ticket text and reasoning the worker does not need.
- Length follows the change. Cut noise, never a fact the worker needs. A small fix fits in 20 to 30 lines; a larger change lists more steps. Past about 80 lines, the ticket needs splitting.
- Write `Change` as ordered steps. Each step names the file and symbol, the exact change, the helper or controller logic to reuse, the edge cases to handle, and the criterion it serves.
- Use the sections below, as bullets. No introduction, summary or closing.
- Name files and symbols as `path:line` or `path` plus symbol.
- Do not restate the ticket. Each criterion takes one line: the criterion, then its proof.
- One decision per bullet. Mention a rejected alternative only when the worker would otherwise pick it, in one line.
- No hedging: drop "consider", "might", "ensure", "robust", "as needed", "if appropriate".
- Risks only when concrete and checkable.
- Reuse existing helpers and controller logic; name them. Never plan a local copy of shared logic.
- Every criterion is proven in the running app. Say what to observe and how it is read (harness action and field, test ID or state path); if nothing exposes it, say so under Risks. Recipe choice belongs to the run. Tests are regression coverage under Tests, never proof; rewrite or drop a criterion only a test can show.

## Template

```markdown
# <ticket> · <fix-bug|dev>
Approved by @<github login> · <YYYY-MM-DD> · planned against <origin branch>@<short sha>

## Criteria and proof
- AC1 <criterion> → <what to observe> via <action and field, test ID or state path>

## Root cause | Current behavior
- `<path:line>` <what happens and why>

## Change
1. `<path>` <symbol>: <exact change>. Reuse `<helper>`. Edge cases: <cases>. Serves AC<n>.
- Files: `<path>`, `<path>`

## Tests
- `<test path>`: <case> (regression coverage, not proof)

## Risks
- <concrete risk and how the run checks it>

## Out of scope
- <what the worker must not change>
```

Use `Root cause` for fix-bug and `Current behavior` for dev.
