---
name: your-skill-name
description: >
  Replace with a trigger-style description of when this skill should activate.
  Be specific — this is what the agent uses to decide whether to load the skill.
  Example: "Sui TypeScript SDK integration. Use when writing, reviewing, or
  debugging TypeScript code that interacts with Sui RPCs, transactions, or
  on-chain state."
---

# Skill Title

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

<!--
  Replace "Skill Title" with a clear name, e.g. "Sui TypeScript SDK Skill".
  The opening paragraph should orient the agent: what domain does this cover,
  what common mistakes does it prevent, and what makes Sui-specific usage
  different from general-purpose patterns?
-->

Brief description of what this skill covers and why it exists. Call out the most
common AI-coding mistakes this skill prevents (e.g., using deprecated APIs,
confusing Sui with other chains, misunderstanding the object model).

This skill routes to focused reference files. Load only the ones relevant to the
current task.

<!--
  Cite the canonical source(s) this skill is derived from (official docs,
  spec, repo, etc.) and instruct the agent to fetch from them when unsure
  rather than guessing or extrapolating from related tools. Example:

  All patterns in this skill are derived from:
    https://docs.example.com/

  If unsure about any API, fetch the relevant page before answering.
  Do not guess or extrapolate from other SDKs or libraries.
-->

All patterns in this skill are derived from:
  <CANONICAL_SOURCE_URL>

If unsure about any API, fetch the relevant page before answering.
Do not guess or extrapolate from other SDKs or libraries.

---

## Reference files

<!--
  List each supporting markdown file in the skill directory.
  Each entry should follow this format:

  ### slug — Human-Readable Title
  **Path:** `slug.md`
  **Load when:** describe the tasks/contexts that require this file.
  **Covers:** list the sections or topics inside the file.

  Tips:
  - Keep files focused on a single concern (setup, syntax, patterns, etc.)
  - Name files with short, descriptive slugs (e.g., setup.md, objects.md)
  - "Load when" should use task-oriented language the agent can match against
-->

## Routing guide

<!--
  Map common tasks to which reference files the agent should load.
  This table is the primary decision tool — keep it comprehensive.
  Use "all reference files" for broad tasks like full builds or code review.
-->

| Task | Load |
|------|------|
| Setting up a new project | setup |
| Writing core logic | core |
| Following best practices | patterns |
| Seeing a worked example | examples |
| Implementing a complete feature | core + patterns |
| Full project from scratch | **all reference files** |
| Code review | **all reference files** |

## Skill Content

<!--
  This is where the core knowledge of your skill lives — the rules, guidelines,
  and domain expertise that the agent should always have loaded when this skill
  is active. Unlike reference files (which are loaded on demand), everything in
  this section is available to the agent immediately.

  Structure this section around:
  - Key concepts the agent must understand to work in this domain
  - Rules and constraints that always apply (e.g., "always use X instead of Y")
  - Common mistakes and how to avoid them
  - Sui-specific differences from general-purpose patterns

  Keep it concise. If a topic requires extended explanation, examples, or
  reference tables, put it in a reference file instead and link to it from the
  routing guide above.
-->

### Key concepts

<!-- Define the core abstractions and mental model for this domain. -->

### Rules

<!-- List the non-negotiable rules the agent must follow. Be direct and specific. -->

### Common mistakes

<!-- Describe frequent errors and their correct alternatives. -->
