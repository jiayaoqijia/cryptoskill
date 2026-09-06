[中文](AI_SKILL_CONTRACT.zh-CN.md) | English

# AI Skill Integration Execution Contract

This contract defines strict AI behavior for adding a new skill to this aggregation repository.
Keywords follow RFC semantics:
- `MUST`
- `SHOULD`
- `MAY`

## 1. Objective

1. Ensure AI generates executable, verifiable, merge-ready changes in one pass.
2. Keep AI output aligned with repository gates and schemas.

## 2. Input Contract (What AI receives)

Before execution, AI must have:
1. Aggregation repository path.
2. New skill repository path or URL.
3. Skill npm package name (if published) and target `skill-id`.
4. Capability boundaries (MCP/OpenClaw/CLI).
5. Whether install-level validation is allowed.
6. Environment placeholder root (default: `SKILLS_BASE`).

If inputs are missing:
1. AI `MUST` list missing items explicitly.
2. AI `SHOULD` propose defaults and mark them as assumptions.

## 3. Output Contract (What AI produces)

AI output `MUST` contain exactly 6 sections:
1. Goal / Non-goal
2. Files to change
3. Contract mapping (MUST-by-MUST)
4. Validation commands
5. Risk & rollback
6. Acceptance evidence

AI output `MUST NOT` stop at high-level suggestions without concrete files and commands.

## 4. File and Schema Contract (MUST)

1. `workspace.json`
- `MUST` register new project path.
- `MUST` follow `docs/schemas/workspace.schema.json`.
- `MAY` include `dependsOn` (direct dependency ids).

2. Target skill repository
- `MUST` include `package.json` with `name` and `version`.
- `MUST` expose a stable npm installer binary for setup via `package.json bin` -> `bin/setup.js|bin/setup.ts`.
- `MUST` include `SKILL.md` front matter with `name` and `description`.
- `SHOULD` include `version` and `activation.*` fields when the skill supports IronClaw routing.
- `MUST` satisfy `docs/schemas/skill-frontmatter.schema.json`.
- `MUST` provide MCP support: `src/mcp/server.ts` or `scripts.mcp`.
- If OpenClaw native is declared, `MUST` include `openclaw.json` and satisfy `docs/schemas/openclaw.schema.json`.
- If native setup is declared, `MUST` include `scripts.setup` or `bin/setup.ts|bin/setup.js`.
- If IronClaw native setup is declared, setup must support `bun run setup ironclaw` (or equivalent `bin/setup.ts ironclaw`).
- GitHub repo/tree URLs are discovery sources only; final activation for OpenClaw/IronClaw `MUST` be expressible through catalog metadata.

3. Generated catalog
- `MUST` produce schema version `1.3.0`.
- `MUST` satisfy `docs/schemas/skills-catalog.schema.json`.
- `MUST` include `dependsOn` in catalog when declared in workspace.
- `MUST` emit `distributionSources` and `clientInstall` for published/installable skills.

4. Documentation synchronization
- If rule/contract/template changed, AI `MUST` update Chinese and English docs together.

## 5. Dependency, Conflict, and Path Rules (MUST)

1. `dependsOn` must reference existing skill ids.
2. Duplicate skill ids are blocking failures.
3. `bootstrap --only` must include transitive dependencies.
4. Dependency cycles are blocking failures.
5. `${ENV_VAR}` placeholders in workspace paths must be resolvable; unresolved placeholders are blocking failures.

## 6. Validation Contract (MUST)

AI must execute and report:

```bash
bun run catalog:generate
bun run health:check
bun run readme:check
bun run security:audit
./bootstrap.sh --only <skill-id> --skip-install
```

Optional full install validation:

```bash
./bootstrap.sh --only <skill-id>
```

## 7. Prohibited Actions (MUST NOT)

1. Skipping `workspace.json` registration.
2. Updating README only while skipping contract/template docs when rules changed.
3. Declaring capability without required artifact.
4. Hiding failed command outputs.
5. Ignoring `[FAIL]` gates and claiming done.

## 8. Failure Handling and Rollback (SHOULD)

1. On any gate failure, AI `SHOULD` provide minimal repair path.
2. If not fixable in current round, AI `MUST` report blocker and impact scope.
3. AI `SHOULD` provide rollback points (which files to revert).

## 9. Common Failure Pattern Mapping

| Pattern | Cause | Repair |
|---|---|---|
| `[WARN] ... SKILL.md not found, project skipped` | Skill markdown missing | Add `SKILL.md` with valid front matter |
| `declared native-setup but setup command not available` | Missing setup entry | Add `scripts.setup` or `bin/setup.ts/js` |
| `declared openclaw native but openclaw.json missing` | Missing OpenClaw config | Add `openclaw.json` |
| `[FAIL] Duplicate skill id detected:` | Conflicting skill ids | Fix front matter `name`/workspace mapping |
| `[FAIL] <id>: dependsOn references unknown skill id` | Invalid dependency id | Fix `dependsOn` |
| `[FAIL] Dependency cycle detected: ...` | Cyclic dependency graph | Remove cycle |
| `[FAIL] Unresolved environment variable(s) in path` | Missing env variable | Export required variable |

## 10. Definition of Done

Done means all conditions below are met:
1. New skill appears in `skills-catalog.json` (schema `1.3.0`).
2. `health:check` has no fail.
3. `readme:check` passes.
4. `security:audit` passes.
5. `bootstrap --only <skill-id>` runs (or `--skip-install` baseline for quick gate).
6. Chinese and English docs stay synchronized with identical section numbering.
