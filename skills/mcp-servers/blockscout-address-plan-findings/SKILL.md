---
name: address-plan-findings
description: Validate review findings about an implementation plan against the codebase and repo rules, fix the valid ones in the plan, and write a feedback file noting what changed and what was rejected (and why). For plan-review findings, not code-review findings.
argument-hint: "[plan-id (optional override, e.g. issue-418)]"
disable-model-invocation: true
---

# Address Plan Findings

A reviewer (often the `/implementation-plan-review` skill, or the user) hands you a list of **findings** about an implementation plan — each a claimed gap, inaccuracy, or risk in the plan, usually with a severity, a location, a problem, and a recommendation. Your job is to **judge each finding on its merits**, then **edit the plan to fix the ones that are genuinely valid**, and leave a written record of your decisions.

Two things make this skill what it is, and you must hold both:

- **You edit the *plan*, never the source code.** The findings are about a planning document under `.ai/impl_plans/`. "Fixing" a finding means revising that `.md` plan so the eventual implementation will be correct — it does **not** mean implementing anything. Do not touch application code, tests, or docs in this run. (If the findings are actually about a code diff / PR — a *code review* — this skill does not apply; stop and say so.)
- **A finding is a hypothesis, not a fact.** Reviewers are sometimes wrong: they misread the code, misremember a convention, or flag something the plan already handles. Verify every claim against ground truth before acting on it. Rubber-stamping a wrong finding corrupts the plan just as badly as ignoring a right one.

## Inputs

- **Findings**: the list of comments, pasted into the invocation. If none were pasted, ask for them — do not invent findings.
- **Plan id** (`$1`, optional override): you rarely pass this — it's normally inferred in step 0.

## Workflow

### 0. Identify the plan and its id

You need the `plan-id` so you can find the plan file (`.ai/impl_plans/<plan-id>.md`) and its feedback directory. This skill is normally run in the same session that just produced the plan (e.g. right after `/plan-export`), so you won't be handed the path — **infer it.** If a plan-id was passed explicitly as `$1`, that wins; otherwise:

1. **From the findings themselves.** Their *Location* and *Scratchpad* references almost always contain a path like `.ai/impl_plans/issue-418.md` or `.ai/impl_plans/issue-418/scratchpads/260714-1022/…` — the plan-id is the first path segment after `impl_plans/` (`issue-418`), not a suffix to strip. This is the strongest signal and it's right there in the invocation.
2. **From the session history.** If the findings carry no such path, look back a few messages for the plan file most recently created or discussed (the `.ai/impl_plans/<id>.md` that `/plan-export` wrote) and take the id from its filename.
3. If you still can't pin it down, or the signals point at more than one plan, ask — don't guess. Operating on the wrong plan is worse than pausing.

Confirm the plan file exists before going further.

### 1. Create this run's feedback directory (before any work)

Run the bundled script with the resolved plan-id:

```bash
bash .agents/skills/address-plan-findings/scripts/new_feedback_dir.sh <plan-id>
```

It creates a fresh timestamped directory `<repo>/.ai/impl_plans/<plan-id>/findings-feedback/<timestamp>/` (nothing existing is touched or deleted) and prints its absolute path on stdout — that's where your feedback file goes in step 6. Always use exactly that printed path; never glob or guess a path under `.../findings-feedback/` yourself, and never reuse a directory from an earlier run. (If the printed path is ever lost from context, the lexicographically-last timestamp subdirectory is the most recent, since the timestamp format sorts chronologically — but prefer the printed path.) The script resolves the project root itself (`git rev-parse --show-toplevel`), so it targets the correct `.ai/impl_plans` whether you're in the principal checkout or a `git worktree`, regardless of your current directory. If it exits non-zero (bad plan-id, plan file missing, target path blocked, or not inside a git repo) it prints `error: <message>` on stderr telling you why; fix the cause and re-run rather than working around it.

### 2. Read the plan and the evidence

- Read the **whole plan file** so you understand the structure your edits must stay consistent with (section order, slice markers, the conventions `/plan-export` baked in).
- If a finding cites a **scratchpad** (e.g. `…/scratchpads/<timestamp>/finding-NN-*.md`), read it — it usually carries the reviewer's grounded analysis (the variants weighed, the evidence, the recommendation) and is the fastest way to see what they actually checked.
- Do **not** open other plans under `.ai/impl_plans/`. They're irrelevant to this one and only burn context and bias your judgment toward another feature's choices.

### 3. Validate each finding independently

Treat each finding as a claim to confirm or refute against the real codebase and the repo's own rules — exactly the critical posture of `/review-described-changes`, but pointed at the plan:

- Open the **actual** files, symbols, tests, and `.cursor/rules/*.mdc` the finding names. Reason from what the code and rules say *today*, not from the finding's paraphrase of them.
- Decide: **valid** (a real problem the plan should fix), **invalid** (the claim doesn't hold, or the plan already handles it), or **partially valid** (some of it warrants a change, some doesn't).
- Be skeptical in both directions. A confidently-worded finding can still be wrong; a minor-looking one can still be right. Severity labels in the input are the reviewer's opinion, not a verdict.

### 4. Apply fixes for the valid findings

Edit **only the plan file** to address every valid (or partially-valid) finding:

- Make the smallest change that genuinely closes the finding, and keep it consistent with the plan's existing wording, structure, and conventions. You're improving a document a developer/agent will execute verbatim — clarity and correctness there, not prose volume.
- For a partially-valid finding, apply the warranted part and let the rejected part be explained in the feedback file.
- Leave invalid findings unactioned — their justification lives in the feedback file, not in plan edits.

### 5. Re-validate plan integrity (if it uses slice markers)

Plans produced by `/plan-export` wrap every section in `<!-- impl-plan:begin slug="…" -->` markers that `scripts/slice_impl_plan.py` must be able to slice. If the plan has these markers, re-run the validator after your edits and fix until it exits `0` — a plan that no longer slices cannot be implemented:

- Host: `uv run python scripts/slice_impl_plan.py .ai/impl_plans/<plan-id>.md --inspect`
- Devcontainer: `python scripts/slice_impl_plan.py .ai/impl_plans/<plan-id>.md --inspect`

### 6. Write the feedback file

Write one Markdown file into the directory from step 1: `.ai/impl_plans/<plan-id>/findings-feedback/<timestamp>/feedback.md`. It has exactly two sections, and the asymmetry between them is deliberate:

- **What was changed** — one *brief* bullet per finding you closed. Brevity is right here because the plan diff already carries the detail; this list just maps each closed finding to the edit that closed it.
- **Not closed** — one *detailed, plain-language* bullet per finding you did **not** action (invalid, or the rejected part of a partial), explaining **why**. This list must stand on its own: a rejected finding leaves no trace in the plan, so the person who raised it (or the user) needs your full reasoning — grounded in what the code/rule/plan actually says — to either accept the rejection or push back. Write it so someone who never saw your tool calls can follow it.

Key each bullet to the finding's number/title from the input so the mapping is unambiguous. If a section has no entries, write a single bullet saying so explicitly (`- None — every finding was valid and addressed.` / `- None — no finding was valid.`) rather than leaving it blank.

Use this structure:

```markdown
# Findings feedback — <plan-id>

## What was changed

- **Finding 1 — <short title>:** <concise note on the edit that closed it>
- **Finding 2 — <short title>:** <concise note on the edit that closed it>

## Not closed

- **Finding 3 — <short title>:** <thorough plain-language explanation of why no change was warranted — what you checked and what it actually showed>
```

### 7. Output: the file path, and nothing else

Your entire chat reply is the path to the feedback file, as a clickable link:

```
[.ai/impl_plans/<plan-id>/findings-feedback/<timestamp>/feedback.md](.ai/impl_plans/<plan-id>/findings-feedback/<timestamp>/feedback.md)
```

Do **not** restate what you changed or why you rejected anything in chat — all of that lives in the file, and repeating it defeats the point of writing the file. The path is the whole message.

## Notes

- **Plan document only.** The sole files you create or modify are the plan `.md` and the feedback file (plus creating this run's directory in step 1). No source/test/doc edits — that's implementation, not this skill.
- **Plan findings, not code-review findings.** If the input is review of a code diff/PR rather than a plan document, this skill doesn't apply.
- **Don't pad the verdict.** Closing zero findings (all invalid) or all of them is a perfectly valid outcome; report it honestly. Validity is decided by the code and the rules, not by how many findings "should" be real.
