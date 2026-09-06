---
repo: metamask-extension
parent: ui-development
---

# MetaMask Extension Product UI — MMDS Guidance

Strategy: [Agentic Design System Strategy](../../../knowledge/agentic-design-system-strategy.md)
([Google Doc](https://docs.google.com/document/d/1wwvEJxom097q-ehSJAfqKvWb01ZW-kmlpy7BQW5In40/edit))

For Extension UI, the MetaMask Design System (MMDS) is the default source for
components, tokens, and documented patterns. Align new and changed UI with MMDS
wherever it supports the need, using current Storybook documentation as the
source of truth. Custom UI remains valid when it serves an intentional product
need that MMDS does not cover, but the rationale should be recorded.

This is a consumer gateway, not a second MMDS knowledge base. Do not add static
component inventories, release-specific API lists, or copied component
documentation here. Storybook MCP and the installed package provide current
knowledge; this skill provides the Extension workflow and durable constraints.

## When to Use

Use this guidance when creating, changing, or reviewing Extension UI, including
components, screens, stories, styles, tokens, themes, and UI behavior.

This skill owns MMDS alignment for product UI. Generic TypeScript and React
quality, component file scaffolding, and PR process remain separate concerns and
may be used alongside it. If a repository-specific scaffolding skill is
available, use it for file and test setup; do not duplicate its templates here.

## Create Workflow

1. Query current MMDS guidance before choosing a component, pattern, API, token,
   or interaction.
2. Use `@metamask/design-system-react` when it supports the need.
3. Search the Extension codebase and reuse suitable existing UI, including UI
   that is not yet in MMDS or is intentionally feature-specific.
4. Use Tailwind classes and the repository's design-token configuration for
   styling and layout not provided by MMDS.
5. Build new feature UI only when no suitable MMDS or existing Extension UI can
   be reused.
6. If no suitable component or documented pattern exists, record the
   documentation or system gap and make the custom decision explicit. Do not
   guess an API or silently substitute another platform's component.

## Review Workflow

When reviewing a UI diff, perform an MMDS-specific sub-review. Do not duplicate
general code-review etiquette or decide PR status; report the design-system
evidence and leave PR mechanics to the relevant workflow.

1. Identify changed UI files, components, stories, styles, tokens, themes, and
   renderable behavior.
2. Query current Storybook guidance for each changed MMDS building block and
   relevant pattern, using the Extension React/web documentation first.
3. Check that the implementation uses documented or story-proven props,
   variants, tokens, composition, and behavior.
4. Check component and pattern choice, existing-UI reuse, styling/token usage,
   accessibility, localization, keyboard behavior, and platform fit.
5. Check for new use of APIs or components marked `@deprecated` in current
   package metadata or documentation. Do not maintain a deprecated-name list in
   this skill; read the current replacement guidance and report a finding when
   no replacement is documented.
6. Identify custom UI and overrides. Treat them as findings when their product
   rationale or exception record is missing, not as automatic failures.
7. Separate deterministic issues from judgment findings, and report each finding
   with its file/line, evidence, current source, and recommended action.

Component or pattern choice, custom UI, and missing documentation are
design-system findings that generally need human judgment. Deterministic
repository checks may enforce token or deprecated-usage rules separately.

## Required Storybook MCP Workflow

Before creating, changing, or reviewing UI:

1. Start by querying `storybook-broker-mcp` with `list-all-documentation` so the
   available guidance reflects the current MMDS release.
2. Find the relevant Extension pattern documentation in the React/web Storybook.
3. Query `get-documentation` for the selected pattern and each UI building block.
4. Query `get-documentation-for-story` when documentation does not answer the
   question or a story is needed to establish real usage.
5. Use only props, variants, tokens, composition, and behavior explicitly
   documented or demonstrated by a story.

The Context Forge-provided `storybook-broker-mcp` is expected to be
preconfigured by the agent environment. Do not install, configure, authenticate,
or invent an endpoint for it from this skill. If the server or a required tool
is unavailable, or a call fails, state that the broker could not be reached and
use the fallback below.

Never infer an API from a name, a previous implementation, another platform, or
another UI library. If the required guidance is absent, record the gap and use
the fallback process below rather than guessing.

Do not apply guidance from another platform without an Extension mapping
documented in Storybook. If no mapping exists, treat it as a documentation gap.

## Fallback When Storybook MCP Is Unavailable

Use these sources in order:

1. The installed `@metamask/design-system-react` package and its type
   definitions under `node_modules`.
2. The installed Extension-facing MMDS styling surfaces:
   `@metamask/design-system-tailwind-preset` for Tailwind CSS v3, or the
   `@metamask/design-tokens/tailwind/theme.css` export for Tailwind CSS v4.
   Use `@metamask/design-tokens` for the installed token exports and styles.
3. The Extension's current Tailwind configuration and package configuration.
   Check the installed Tailwind version, preset or theme import, content
   globs, plugins, and safelist. Use only class names generated by that
   configuration and the installed MMDS preset or theme. If availability is
   unclear, verify the generated CSS or build output instead of inventing a
   class. Do not use default Tailwind colors, arbitrary values, or a manual
   safelist as a substitute for an MMDS token.
4. Current Extension usage and stories found by searching the repository for
   the installed component or token. Treat examples as usage evidence, not as
   a replacement for the installed package contract.
5. A generated MMDS release manifest or repository-provided release guidance.
6. The MMDS source repository as a last resort.

`@metamask/design-system-shared` may be relevant to Tailwind content scanning
when required by the installed MMDS configuration, but it is not a source for
Extension component APIs. Do not use React Native or TWRNC packages for
Extension UI.

The installed package version is the source of truth for the code being
changed. Read the matching exports and type definitions before writing or
reviewing usage. Do not restore a static inventory or copy undocumented APIs
into this skill to compensate for missing MCP.

## Durable Extension Constraints

- Prefer `@metamask/design-system-react` components.
- Reuse suitable existing Extension UI before creating new feature UI.
- Use Tailwind class names instead of SCSS for styling and layout.
- Do not create or modify SASS or SCSS files.
- Reuse an existing feature-level solution when the documented pattern calls
  for one; otherwise compose the smallest supported solution.
- Preserve accessibility, localization, and keyboard interaction requirements
  shown in the relevant Storybook documentation and stories.
- Use repository-approved exception documentation when custom UI is necessary;
  do not invent a new annotation format in this skill.

## Create and Review Checklist

- [ ] Current Storybook pattern and building-block guidance was queried, or the
      MCP fallback, Tailwind configuration checks, and any documentation gap
      were recorded.
- [ ] MMDS was used wherever it supports the need, and suitable existing
      Extension UI was considered.
- [ ] Only documented, story-proven, or installed-package-typed APIs are used.
- [ ] No new deprecated API or component usage was introduced.
- [ ] No undocumented platform substitution was made.
- [ ] Custom UI has an intentional product rationale and exception record when
      required by repository practice.
- [ ] Accessibility, localization, and keyboard behavior were preserved.
- [ ] No SASS or SCSS files were created or modified.
