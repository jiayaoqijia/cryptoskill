[中文](NEW_SKILL_CHECKLIST.zh-CN.md) | English

# New Skill PR Checklist

Copy and check this list in your PR.

## 1. Base Registration

- [ ] New project path is registered in `workspace.json`.
- [ ] Path is resolvable (`${SKILLS_BASE}` or equivalent env is configured).
- [ ] If dependency exists, `dependsOn` is declared with direct skill ids only.

## 2. Minimum Artifacts (MUST)

- [ ] `package.json` exists with `name` and `version`.
- [ ] `package.json bin` exposes a stable setup executable (`bin/setup.js|bin/setup.ts`).
- [ ] `SKILL.md` exists with front matter `name` and `description`.
- [ ] MCP support exists: `src/mcp/server.ts` or `scripts.mcp`.
- [ ] If OpenClaw native is declared, `openclaw.json` exists.
- [ ] If native-setup is declared, `scripts.setup` or `bin/setup.ts|bin/setup.js` exists.
- [ ] If IronClaw native setup is declared, `setup ironclaw` is supported and installs a trusted skill path.

## 3. Schema Alignment

- [ ] `workspace.json` matches `docs/schemas/workspace.schema.json`.
- [ ] `SKILL.md` front matter matches `docs/schemas/skill-frontmatter.schema.json`.
- [ ] `openclaw.json` (if present) matches `docs/schemas/openclaw.schema.json`.
- [ ] Generated `skills-catalog.json` matches `docs/schemas/skills-catalog.schema.json`.
- [ ] Generated catalog includes `distributionSources` and `clientInstall`.

## 4. Architecture and Product Requirements

- [ ] Config-first, no hardcoded third-party service switches.
- [ ] External dependency failures degrade gracefully without blocking main flow.
- [ ] Error semantics are unified with trace clues.
- [ ] `SKILL.md` clearly states capabilities, limits, risks, and non-goals.

## 5. Gate Commands

- [ ] `bun run catalog:generate`
- [ ] `bun run health:check`
- [ ] `bun run readme:check`
- [ ] `bun run security:audit`
- [ ] `./bootstrap.sh --only <skill-id> --skip-install`

Optional full validation:
- [ ] `./bootstrap.sh --only <skill-id>`

## 6. Documentation Sync (Bilingual Mandatory)

- [ ] Chinese docs are updated: `CONTRIBUTING.zh-CN.md` / `docs/*.zh-CN.md` (if rules changed).
- [ ] English mirrors are updated: `CONTRIBUTING.md` / `docs/*.md`.
- [ ] Chinese and English section numbering and MUST ordering are aligned.

## 7. PR Completeness

- [ ] PR description includes Goal / Non-goal.
- [ ] PR description includes key changed files.
- [ ] PR description includes command output summary.
- [ ] PR description includes risk and rollback plan.
