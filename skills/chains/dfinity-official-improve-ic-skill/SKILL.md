---
name: improve-ic-skill
description: 'Improve an existing skill in the IC Skills repo (skills.internetcomputer.org). Load this skill whenever asked to improve, fix, update, enhance, review, or add content to an existing skill at skills/<skill-name>/SKILL.md — including adding pitfalls, updating canister IDs, fixing code examples, strengthening the description, or updating evals. Do NOT use for creating a brand-new skill (use skill-creator for that). Trigger examples: "the motoko skill is missing a pitfall", "update icp-cli for the new recipe format", "the ckbtc description is weak", "add an eval for the canister-security skill".'
---

# Improve IC Skill

A token-efficient workflow for improving an existing skill in the IC Skills repo. The guiding principle: **understand the problem first, change precisely, verify only what changed.** Evals exist as regression safety nets — run them selectively, not automatically on every pass.

## Step 0 — Understand the problem before touching anything

**This is a hard stop. Do not read any file, run any command, or make any change until you have a specific problem statement from the user.**

You need to know:
1. **What is the specific issue?** (e.g. "canister ID X is stale", "missing pitfall about Y", "description doesn't trigger on Z", "code example uses deprecated API W")
2. **Why does it matter?** (e.g. "agents generate broken code", "skill never triggers for this use case", "upstream sync added a new command we don't cover")

If the request is vague ("improve the motoko skill", "the ckbtc skill feels weak") — ask:

> "What specific issue should I focus on? For example: a missing pitfall, a stale canister ID, a broken code example, or a description that isn't triggering correctly."

**If the user cannot or will not provide a specific issue — stop. Do not proceed.** Do not read the skill. Do not run commands. Do not "explore and find improvements yourself." Explain clearly:

> "I need a specific problem to solve before I can start. Blind improvements risk changing things that don't need changing. To find a concrete issue, try: running `npm run validate`, checking `evaluations/<skill-name>.json` for failing cases, or pointing me to a GitHub issue or upstream diff."

If the user pushes back, repeats the vague request, or expresses frustration — hold the position. The answer is always the same: no specific issue = no work started.

The only exception: if the reason is unambiguous from context already in the conversation (a GitHub issue body, an upstream diff, a specific error message) — proceed directly to Step 1 without asking.

## Step 1 — Understand the skill

Read `skills/<skill-name>/SKILL.md` fully. Check:
- What it covers and what it's missing
- Whether it's upstream-tracked: `grep <skill-name> .claude/upstream.md` — if it appears, note which sections are owned by icskills (those cannot be overwritten from upstream)
- Recent git history: `git log --oneline -5 -- skills/<skill-name>/SKILL.md`

## Step 2 — Validate baseline

```bash
npm run validate
```

Fix any errors before making content changes. Warnings are acceptable — don't chase them unless they're relevant to your improvement.

## Step 3 — Identify improvements

Read with fresh eyes. Common high-value areas:

**Pitfalls** — highest-value content; every pitfall documented prevents an agent hallucination. Look for: incorrect usage patterns you know about, error messages agents typically misread, wrong defaults, API gotchas.

**Canister IDs and version numbers** — verify against mainnet and current release tags. Stale IDs silently break agent-generated code.

**Code examples** — verify syntax compiles, APIs still exist, no deprecated patterns.

**Description** — must state what it does, when to use it, AND when NOT to use it. Include specific keywords agents match on. A weak description means the skill never triggers.

**Required frontmatter** — `metadata.title` and `metadata.category` are required by CI. Missing these blocks deployment.

For upstream-tracked skills (`writing-motoko`, `migrating-motoko-actors`, `troubleshooting-motoko-migrations`, `reviewing-motoko`, `mops-cli`, `static-site`): read `.claude/upstream.md` carefully. Only modify icskills-owned sections freely; changes to shared content should also be filed upstream.

## Step 4 — Apply improvements

Edit `skills/<skill-name>/SKILL.md`. Stay focused — don't refactor things you weren't asked to touch.

## Step 5 — Validate again

```bash
npm run validate
```

Fix any errors. Warnings from unrelated sections are fine to leave.

Optionally run LLM quality scoring if the changes were substantial:

```bash
skill-validator score evaluate --provider claude-cli skills/<skill-name>
```

## Step 6 — Check and update evals

Open `evaluations/<skill-name>.json` at the repo root (not inside the skill directory).

**If the file doesn't exist yet**, create it as part of this improvement session. A skill being improved is the right moment to seed its first evals. Start lean — 1-2 output_evals covering the most important pitfalls, and 2-3 trigger_evals for the description. Don't try to be comprehensive; a small, accurate eval file beats an overwhelming one that never gets run.

For **upstream sync sessions** where no eval file exists: seed cases directly from the upstream diff — new commands, changed defaults, renamed APIs, and new pitfalls in the diff are exactly where agents will hallucinate without updated guidance. The diff is your best source.

```bash
# Verify no eval file exists
ls evaluations/<skill-name>.json 2>/dev/null || echo "No evals yet — create them"
```

**If the file exists**, review the existing cases alongside your changes.

**Always update evals when:**
- You added a new pitfall — pitfalls are exactly where agents hallucinate without guidance; every new pitfall deserves a case
- You changed a command, API, or canister ID that an existing case now describes incorrectly — fix the case
- You introduced a new behavior that agents would likely get wrong without explicit guidance

**Keep the suite lean.** Don't add cases for things that are obvious or already well-covered. Each case is a future regression test that costs tokens to run.

## Step 7 — Run evals

Two separate things happen here — don't conflate them:

**A. Always run every case you added or changed (with baseline).** A new or edited eval case is code you just wrote. Running it confirms it actually passes with the skill and shows a real with-skill vs baseline delta. An unrun case can be mis-scoped — e.g. a prompt that says "just the command" paired with an expected behavior that requires an explanation will fail the with-skill run — and you'd be committing a silently broken regression test. Include these results in the PR. This is not optional, even when the change is "purely additive": additive means new cases, and new cases must be run.

**B. Re-run untouched existing cases only when relevant.** Re-running the rest of the existing suite is a regression check — "did I break something that was already tested?" Do this when:
- You changed or removed content that an existing eval explicitly tests (canister ID, command name, error message)
- You rewrote a section that several existing evals cover
- The description changed significantly — run trigger evals only
- You're unsure whether a change is safe

Skip re-running an existing case only when nothing you touched is content that case covers.

Check what evals exist before deciding:

```bash
node scripts/evaluate-skills.js <skill-name> --list
```

Run only the relevant subset:

```bash
# Single eval by index (cheapest)
node scripts/evaluate-skills.js <skill-name> --eval <N>

# Trigger evals only — for description changes
node scripts/evaluate-skills.js <skill-name> --triggers-only

# Run a case you added/changed WITH baseline (default) — this is what goes in the PR
node scripts/evaluate-skills.js <skill-name> --eval <N>

# Skip baseline (--no-baseline) only for a quick correctness spot-check, not for PR results
node scripts/evaluate-skills.js <skill-name> --eval <N> --no-baseline

# Full suite — only when you made broad changes across the whole skill
node scripts/evaluate-skills.js <skill-name>
```

Eval format reference:

```json
{
  "output_evals": [
    {
      "name": "descriptive name",
      "prompt": "scoped prompt asking for one thing — specify what to exclude to keep it fast",
      "expected_behaviors": [
        "Specific, checkable behavior the model should exhibit",
        "Another specific behavior"
      ]
    }
  ],
  "trigger_evals": [
    {
      "query": "realistic user prompt that should trigger this skill",
      "expected_behavior": "should trigger"
    },
    {
      "query": "realistic prompt that looks similar but should NOT trigger this skill",
      "expected_behavior": "should NOT trigger"
    }
  ]
}
```

Keep prompts tightly scoped — open-ended prompts generate long responses and risk timeouts. Ask for one thing; explicitly exclude what you don't want ("just the function, no deploy steps").

## Step 8 — Final check

```bash
npm run validate
```

The skill is ready for a PR. Include a brief summary of what changed and, if you ran evals in Step 7, paste the relevant results collapsed in a `<details>` block (see [Submit a PR](../../../CONTRIBUTING.md#8-submit-a-pr) for the exact format).

## Upstream-tracked skills

Before editing `writing-motoko`, `migrating-motoko-actors`, `troubleshooting-motoko-migrations`, `reviewing-motoko`, `mops-cli`, or `static-site`, read `.claude/upstream.md`. It lists which sections are icskills-owned. You can freely improve owned sections. For shared content, improvements should also be filed as issues upstream so they flow back on the next sync.
