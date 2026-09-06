---
name: review-plan-findings-feedback
description: Manually review a feedback file produced after implementation-plan review findings were addressed. Use when the user asks to verify that plan changes correctly close, correctly reject, or fail to close the original findings, while checking for newly introduced or newly exposed problems. Independently adjudicates only new candidate problems with the implementation-plan-review protocol, writes surviving unresolved or new findings to the plan-id findings directory, and replies with the output path or a concise no-new-findings status.
disable-model-invocation: true
---

# Review Plan Findings Feedback

Review a follow-up feedback file after plan-review findings were addressed. Do
not implement code and do not edit the plan. The only user-facing artifact is a
findings file. Adjudication work artifacts may be created only in this run's
fresh scratchpad directory.

## Inputs And Assumptions

- The user provides the feedback file path, usually `.ai/impl_plans/<plan-id>/findings-feedback/<timestamp>/feedback.md`.
- The implementation plan path, issue snapshot, and original review findings are expected to already be present in the conversation context because this skill is run in the same session as `implementation-plan-review`.
- Do not require the user to pass those inputs again. Infer the plan id from the current session first, then from the feedback path if needed.
- Recover the exact issue snapshot used by the original review. Do not silently substitute a newer issue version.
- If the plan id, issue snapshot, or original findings cannot be recovered with confidence, stop and ask for the missing context rather than guessing.

## Workflow

### 1. Resolve The Plan Id

Infer exactly one `plan-id`, such as `issue-418`.

Priority:

1. The most recent implementation plan path in session context: `.ai/impl_plans/<plan-id>.md`.
2. The feedback file path: `.ai/impl_plans/<plan-id>/findings-feedback/<timestamp>/feedback.md` — the plan-id is the first path segment after `impl_plans/`.
3. Scratchpad paths from the prior review: `.ai/impl_plans/<plan-id>/scratchpads/<timestamp>/...` — same rule: the plan-id is the first segment after `impl_plans/`, not a suffix to strip.

Confirm `.ai/impl_plans/<plan-id>.md` exists before proceeding.

### 2. Create This Run's Findings Directory First

Before reading or listing any files under `.ai/impl_plans/<plan-id>/findings/`, run:

```bash
bash .agents/skills/review-plan-findings-feedback/scripts/new_findings_dir.sh <plan-id>
```

This creates a fresh timestamped directory `.ai/impl_plans/<plan-id>/findings/<timestamp>/` (nothing existing is touched or deleted) and prints its absolute path on stdout. Use exactly that printed path for this run's output — never glob or guess a path under `.../findings/` yourself, and never reuse a directory from an earlier run. (If the printed path is ever lost from context, the lexicographically-last timestamp subdirectory is the most recent, since the timestamp format sorts chronologically — but prefer the printed path.) If the script exits non-zero, it prints `error: <message>` on stderr; fix the cause and rerun it before doing review work.

### 3. Read Required Inputs

Read in full:

- The feedback file supplied by the user.
- The current implementation plan: `.ai/impl_plans/<plan-id>.md`.
- The exact issue snapshot used by the original review.
- The original review findings from the current conversation context.

Read targeted evidence as needed:

- Prior scratchpads cited by the original findings.
- Relevant code, tests, docs, and `.cursor/rules/*.mdc` files needed to verify whether the feedback and plan edits are correct.

Do not open unrelated implementation plans.

### 4. Re-Review The Closure

For each original finding:

- Check whether the feedback accurately understood the finding.
- Check whether the current plan actually changed in a way that closes the valid part of the finding.
- If the feedback rejects the finding, decide whether the rejection is acceptable. Treat an accepted rejection the same as a closed finding: do not report it as new/unresolved.
- If the plan does not close the finding, or the rejection is not acceptable, retain the original finding as unresolved. Do not adjudicate it again.
- Re-check the underlying code/rules when the finding depends on codebase reality.

Then scan the edited plan sections for newly introduced or newly exposed issues.
Apply the same review standard as `implementation-plan-review`, but distinguish
unresolved original findings from genuinely new candidate problems before
launching any adjudicator.

A problem is new only when it is not substantively covered by an original
finding. Treat it as the unresolved original finding, without new adjudication,
when it has the same violated requirement, affected behavior, and corrective
obligation, even if the feedback review discovers new evidence, a clearer
wording, another manifestation, or a different severity. Treat a distinct
requirement violation, failure mode, edge case, affected surface, or materially
different corrective obligation as a new candidate. When both are present,
split the unresolved original part from the genuinely new candidate.

Do not report:

- Findings that are fully closed.
- Pure summaries.
- Style nits that do not affect correctness, coverage, maintainability, safety, or junior-dev readiness.
- Environment command-prefix mechanics, unless the verification scope itself is objectively wrong.

### 5. Adjudicate Only New Candidate Problems

Skip this step when the closure review produces no genuinely new candidates.
Never launch a new adjudicator for an original finding, regardless of its
closure disposition.

Before creating candidate inputs or launching adjudicators, read these
`implementation-plan-review` resources completely:

- `.agents/skills/implementation-plan-review/references/finding-adjudication-protocol.md`
- `.agents/skills/implementation-plan-review/assets/finding-adjudication-report.md`

Create a fresh adjudication run:

```bash
bash .agents/skills/implementation-plan-review/scripts/new_scratchpads_dir.sh \
  .ai/impl_plans/<plan-id>.md
```

Use exactly the absolute path printed on stdout as this feedback review's
adjudication run directory. Never reuse or write into an earlier scratchpad
run. For each new candidate, create:

```text
finding-01-short-slug/
├── input.md
├── full-report.md  # written by the adjudicator
└── brief.md        # generated by the finalizer
```

Create `input.md` with:

- the candidate ID;
- absolute current plan, original issue snapshot, template, protocol, and output paths;
- one neutral, falsifiable candidate hypothesis;
- focused research questions;
- candidate-specific scope or edge cases;
- an explicit statement that `Confirmed`, `Downgraded`, `Question`, and `Closed` are all successful outcomes.

Do not include the feedback, original findings, prior scratchpads or
adjudications, a preferred solution, or an expected disposition. The main
reviewer owns novelty classification; the adjudicator decides only whether the
candidate is an actionable problem in the current plan.

Launch one independent subagent per candidate, batching when concurrency is
limited. Use `fork_turns="none"` and prefer a strong reasoning model
(`gpt-5.6-sol` with `xhigh` reasoning when available) unless the user requests
otherwise. The launcher prompt must contain only:

- the absolute protocol path and an instruction to read it completely;
- the absolute `input.md` path;
- the exact writable candidate directory;
- the absolute template path;
- the requirement to run the protocol's finalization loop before returning.

Require each adjudicator to write `full-report.md`, run
`finalize_adjudication.py`, fix every validation error, and return only the
protocol's short completion record. The finalizer generates `brief.md`; never
edit it manually.

After all adjudicators finish, verify the complete run:

```bash
python3 .agents/skills/implementation-plan-review/scripts/verify_adjudication_run.py \
  --run <absolute-run-directory> \
  --expected-count <candidate-count>
```

If verification fails, send the exact errors to the responsible adjudicator
and require correction and re-finalization. Read all valid `brief.md` files
first; inspect a full report or extract a tagged section only when progressive
disclosure is warranted.

The main reviewer owns cross-finding deduplication, conflicts, cumulative scope,
and one common severity scale. Only `Confirmed`, actionable `Downgraded`, and
unresolved `Question` candidates survive. Omit `Closed` candidates. Deduplicate
surviving new candidates against unresolved original findings before writing
the output.

### 6. Write Output Only If Findings Survive

If one or more unresolved original findings or adjudicated new findings survive,
create exactly one Markdown file inside the directory printed in step 2:

```text
.ai/impl_plans/<plan-id>/findings/<timestamp>/findings.md
```

The file must contain only a list of reportable findings. Do not add an
introduction, summary, "no findings" line, or review sections.

Use this item shape:

```markdown
- **Severity:** Major
  **Location:** Phase N / plan section + relevant repo file or rule
  **Problem:** What remains wrong or what new problem was introduced.
  **Recommendation:** Concrete change to the plan.
  **Rationale:** Why it matters.
  **Scratchpad:** Path to the generated brief.md.
```

For an unresolved original actionable finding, preserve its original generated
`brief.md` path. For a surviving new actionable finding, use the new
adjudication's generated `brief.md`. Never link directly to `full-report.md`.
Omit `Scratchpad` only for a pure `Question`.

If no findings survive, do not create any file in the findings directory.

### 7. Chat Output

If a findings file was created, reply with only a clickable link to it:

```markdown
[.ai/impl_plans/<plan-id>/findings/<timestamp>/findings.md](.ai/impl_plans/<plan-id>/findings/<timestamp>/findings.md)
```

If no new findings were found and every original finding was closed by plan edits, reply exactly:

```text
No new findings.
```

If no new findings were found and at least one original finding was rejected by the feedback but you accept the rejection, reply exactly:

```text
No new findings. Rejections accepted.
```

Do not repeat findings in chat.
