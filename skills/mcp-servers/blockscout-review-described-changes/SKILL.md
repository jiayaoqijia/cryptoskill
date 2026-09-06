---
name: review-described-changes
description: Critically review a GitHub issue plus a "described changes" overview written by a developer — open the referenced code, verify the overview's claims against what the code actually does, and report gaps, inconsistencies, and likely mistakes — without modifying any files. Invoke manually.
disable-model-invocation: true
---

# Review Described Changes

The **described changes** are a quick-and-dirty overview a developer wrote after discussing the problem — a rough sketch of what they intend to change. It is **not authoritative**. Approach it critically: read it skeptically, verify every claim against the actual code, and surface what is missing or wrong. The issue describes the real problem; the overview is just one person's first pass at a solution and will contain imprecision, missing files, and optimistic assumptions.

Your job is to read the issue, read the overview, open the code they reference, and report your critical assessment. **Do not modify any files** — this is read-only.

## Inputs

- **GitHub issue**: a number or full URL. The repo is `blockscout/mcp-server`.
- **Described changes**: the overview, pasted into the invocation.

If either input is missing from the invocation, ask for it before proceeding. Do not guess the issue number or invent the overview.

## Workflow

1. **Read the issue in full.** Prefer `gh`; fall back to `WebFetch` on the URL if `gh` is unavailable:

   ```bash
   gh issue view <number> --repo blockscout/mcp-server --comments
   ```

   Capture the actual problem, motivation, and any acceptance criteria the issue states.

2. **Read the described-changes overview carefully.** Extract the concrete claims: which files it says will change, which functions/symbols/configs it names, which tests/docs it mentions, and the approach it implies. Treat each claim as a hypothesis to verify, not a fact.

3. **Open the referenced code — do not reason from file names.** Use the `Read` tool on every file the overview and issue point at, and use `rg` to locate the symbols they name:

   ```bash
   rg -n "function_in_overview|ENV_VAR|ClassName" -S .
   ```

   Broaden to obvious neighbors when it sharpens your judgment: where a new tool would be registered, the matching test module, the doc/spec section. The point is to ground your assessment in what the code actually does, not what the overview claims it does.

4. **Cross-check against repo conventions** where the changes touch them: `.cursor/rules/*.mdc` (e.g. new MCP tool, tool module structure, testing, version management), plus `SPEC.md`, `AGENTS.md`, and `API.md`. These tell you what a *complete* change normally includes here, which is how you spot what the overview omitted.

5. **Reconcile and assess.** Square the issue, the overview, and the code you read, then report the problems below.

## What counts as an "obvious mistake"

A focused critical pass, not a deep audit:

- A referenced file, function, path, or symbol doesn't exist or is named differently in the code.
- A described change contradicts what the code actually does today.
- An obviously-required surface is missing given repo conventions — e.g. tool registration in `server.py`, or a `SPEC.md`/`API.md` update.
- **Test coverage is missing or wrong**: no unit tests for new logic, missing integration tests where real network behavior matters, or the testing approach itself is flawed — e.g. asserting against mocks in a way that never exercises the real logic, testing the wrong layer, or skipping error/negative paths. Check the testing rules in `.cursor/rules/2xx-*.mdc`.
- The proposed logic is simply wrong — it wouldn't actually solve the issue, or would break existing behavior.
- The overview is internally inconsistent.

Stay proportional. This is a rough overview, so when something is unclear rather than clearly wrong, raise it as an open question rather than asserting a defect. On versioning, mirror the project's existing neutrality: don't demand a version bump unless a repo rule, the issue, or the overview already calls for one.

## Output

Conversational, in the chat — no files created or changed. The issue and overview are already in context, so do **not** re-summarize them. Focus on your critical judgment:

### Do I agree with the described changes?
An honest overall read: agree / mostly agree with caveats / significant concerns — and why, in a few sentences.

### Gaps & inaccuracies
Bullets, each tied to the specific file, symbol, or rule that informs it. Distinguish what is clearly wrong from what you are only uncertain about (mark the latter as questions).

### Open questions for the author
Only questions whose answer would actually change the implementation — scope, approach, or whether a change is needed at all. First try to resolve each one yourself from the issue and the code; raise it here only if it genuinely can't be settled that way (intent, scope boundaries, decisions made elsewhere). Drop anything that's mere curiosity or wouldn't affect what gets built.

Close by reminding the user that this is a preliminary critique and that no files were changed — you have not started implementing.
