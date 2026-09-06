[中文](CONTRIBUTING.zh-CN.md) | English

# aelf-skills Contribution Guide (Adding New Skills)

This guide is the hard gate for both human contributors and AI agents.
Chinese is the primary version; this file is the mirrored English version.

## 1. Goals

1. Make new-skill onboarding executable in one pass.
2. Remove ambiguity for cold-start AI agents.
3. Keep rules, scripts, templates, and generated artifacts aligned.

## 2. Scope and Non-goals

1. Scope
- Integration in this repo: `workspace.json`, `skills-catalog.json`, README snapshot, bootstrap/health/readme/security gates.

2. Non-goals
- No business-logic changes inside each skill repository.
- No replacement of per-skill SDK/API docs.
- No migration of `agent-skills-e2e` responsibilities.

## 3. Bilingual Policy (Mandatory)

1. Chinese primary: update Chinese docs first.
2. English mirror: same structure, same section numbering, same MUST semantics.
3. Rule change equals interface change: contract/template/rule updates must be committed in both languages.

## 4. Hard Gates for New Skills (MUST)

1. Register project path in `workspace.json` and keep JSON valid.
2. Target skill repo must include:
- `package.json` with `name` and `version`
- `SKILL.md` front matter with `name` and `description`
- MCP support: `src/mcp/server.ts` or `scripts.mcp`
- `openclaw.json` when OpenClaw native is declared
- setup support: `scripts.setup` or `bin/setup.ts|bin/setup.js`
3. Capability boundary must be explicit in `SKILL.md`: capabilities, limits, risks, non-goals.
4. Schema references (mandatory):
- `docs/schemas/workspace.schema.json`
- `docs/schemas/skill-frontmatter.schema.json`
- `docs/schemas/openclaw.schema.json`
- `docs/schemas/skills-catalog.schema.json`

## 5. Path Portability and Environment Contract (MUST)

1. `workspace.json` paths SHOULD use environment placeholders (for example `${SKILLS_BASE}/AElf/aelf-node-skill`).
2. Unresolved placeholders are blocking errors.
3. Recommended local setup:

```bash
export SKILLS_BASE=/path/to/your/workspace
```

## 6. Dependency and Conflict Rules (MUST)

1. `workspace.json.projects[].dependsOn` is optional and represents direct dependencies by skill id.
2. `dependsOn` must be unique and reference existing skill ids.
3. Duplicate skill ids are blocking failures in catalog generation.
4. `bootstrap --only` resolves transitive dependency closure automatically.
5. Dependency cycle is a blocking failure.

## 7. Execution Flow

1. Complete minimum artifacts in skill repo.
2. Update `workspace.json` in this repo.
3. Run `bun run catalog:generate`.
4. Run `bun run health:check`.
5. Run `bun run readme:check`.
6. Run `bun run security:audit`.
7. Run `./bootstrap.sh --only <skill-id> --skip-install`.
8. Open PR with command output summary.

Golden path example: `docs/examples/EXAMPLE_NEW_SKILL_DIFF.md`.

## 8. Acceptance Gates (MUST)

```bash
bun run catalog:generate
bun run health:check
bun run readme:check
bun run security:audit
./bootstrap.sh --only <skill-id> --skip-install
```

Notes:
1. For full dependency validation, remove `--skip-install`.
2. `workspace.json` may include non-skill repos; `[WARN]` entries are acceptable if explained in PR.

## 9. Failure Mapping (Pattern -> Cause -> Fix)

| Stdout/Stderr Pattern | Cause | Fix Action |
|---|---|---|
| `[WARN] ... SKILL.md not found, project skipped` | Project has no `SKILL.md` | Add `SKILL.md` with required front matter |
| `declared native-setup but setup command not available` | Native setup declared but no setup entry | Add `scripts.setup` or `bin/setup.ts/js` |
| `declared openclaw native but openclaw.json missing` | OpenClaw native declared without config | Add valid `openclaw.json` |
| `[WARN] Unknown skill IDs in --only: ...` | Invalid `--only` id input | Correct id and retry |
| `[FAIL] Duplicate skill id detected:` | Two projects map to same skill id | Rename/fix front matter or workspace path |
| `[FAIL] <id>: dependsOn references unknown skill id` | Invalid dependency declaration | Fix `dependsOn` ids |
| `[FAIL] Dependency cycle detected: ...` | Cyclic dependency graph | Remove cycle from `dependsOn` |
| `[FAIL] Unresolved environment variable(s) in path` | Missing environment variable for workspace path | Export variable (for example `SKILLS_BASE`) |

## 10. CI/CD Gates

1. CI workflow: `.github/workflows/gates.yml`.
2. CI uses fixture workspace (`testdata/workspace.ci.json`) for stable repeatable checks.
3. CI gate command set:
- `catalog:generate` with fixture workspace
- `health:check` against fixture catalog
- `readme:check`
- `security:audit`
- `bootstrap --only fixture-node-skill --source local --skip-install`
4. Fixture CI is baseline coverage. Real multi-repo integration remains local responsibility.

## 11. Security Boundary

1. `bootstrap` does not execute setup commands; it only downloads, optionally installs dependencies, and runs health checks.
2. Setup command safety is enforced by `bun run security:audit` pattern scan.
3. High-risk setup command patterns (for example `curl|bash`, `sh -c`) must be removed or justified before merge.

## 12. PR Submission Requirements

1. PR summary must include Goal/Non-goal, key files, validation commands, risks, rollback.
2. Chinese and English docs must be updated in the same PR.
3. README-only updates are not accepted when rules/contracts/templates changed.
