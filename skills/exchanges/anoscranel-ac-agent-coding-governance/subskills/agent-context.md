---
name: agent-context
domain: software-engineering/agent-context
trigger: "\"set up an AGENTS.md\", \"the agent ignores the repo rules\", \"write the agent instructions\", \"compact the rules file\"."
anti_trigger: "Governing the agent's output (subskills/ai-assisted-coding.md); human-facing docs, docstrings and API reference; a README written for people; testing whether instructions worked; in-code conventions."
scope: "Writing AGENTS.md and rules files; context budget, retrieval, compaction for coding agents"
status: "seedling"
---

# Agent Context

## Standard

- **AGENTS.md is plain Markdown with no version and no required fields** (https://agents.md/). It is stewarded by the Agentic AI Foundation under the Linux Foundation, alongside MCP and goose.
- **Closest-file-wins**: the nearest instruction file to the file being edited governs, and an explicit user prompt overrides everything (https://agents.md/).
- **Length limits**: Anthropic recommends a conventions file under 200 lines, because longer files cut adherence; Codex caps project docs at 32 KiB. ⚠️ corpus-sourced guidance
- **Context rot is measured**: accuracy falls from about 95 % to 60–70 % as context grows, even on trivial tasks (Chroma research). ⚠️ single-vendor research
- **Budget rules**: pointers, not contents. Supply skeleton maps and fetch bodies just in time.

## Decision rules

1. Lead with commands: build, test, lint, run. Those are the lines used most.
2. One file per directory scope. Nested only where the rules genuinely differ.
3. Keep the root file short. A rules file is an attention budget, not a dump.
4. State each rule once. A rule repeated in three places drifts in one of them.
5. Name boundaries explicitly: what is off-limits, what needs a human gate.
6. Prefer a repo map plus retrieval over a full source dump. Coding agents beat raw long-context dumps.
7. Split work into separate sessions per lane rather than growing one window.
8. The human-gate list is part of the instructions. It states what the agent must never do alone.

## Procedure

1. List what an agent must know here: commands, layout, conventions, boundaries.
2. Write the root file:
   ```markdown
   ## Commands: npm ci · npm test · npm run lint
   ## Boundaries: migrations are human-gated; no secrets in fixtures
   ```
3. Keep it under 200 lines. If it grows, move detail to the directory that needs it.
4. Add nested files only where the rules diverge, and replace prose with pointers: paths, commands, file names.
5. Add a repo map script so the agent can fetch structure cheaply.
6. Compact after each audit: delete rules no code enforces, merge duplicates.
7. Test the file: give the agent a real task and check that it follows each rule once.
8. Version it with the code, review it on every convention change, and enforce any rule that matters in CI as well (out of scope for this leaf: pipeline wiring).

## Anti-patterns

- A 600-line rules file nobody trims.
- The same rule stated in three files, one copy stale.
- Pasting source into the instructions.
- Commands missing, so the agent guesses the test runner.
- A rules file nobody updated after conventions changed.

## Done checklist

- [ ] Commands first, then layout, conventions, boundaries.
- [ ] Root file under 200 lines.
- [ ] Each rule stated once.
- [ ] Pointers instead of pasted source.
- [ ] Verified against a real task, not just written.
- [ ] Versioned and reviewed with the code.

## Sources

- <https://agents.md/>
- <https://agenticweb.wiki/protocols/agents-md>
- https://agents.md/
