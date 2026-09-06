[中文](AI_NEW_SKILL_PROMPT.zh-CN.md) | English

# AI New Skill Prompt Template

Copy the template below to your AI and replace all `<...>` placeholders.

## Prompt Template

````md
You are the implementation agent for this repository.
Follow `docs/AI_SKILL_CONTRACT.md` strictly.

### 1) Context
- Aggregation repo: <AGGREGATION_REPO_PATH>
- Skill repo path/url: <SKILL_REPO_PATH_OR_URL>
- Skill id: <SKILL_ID>
- NPM package: <NPM_PACKAGE_NAME>@<VERSION_OR_LATEST>
- Workspace env root (default): SKILLS_BASE=<PATH_TO_WORKSPACE_ROOT>
- Capability boundary:
  - MCP: <YES/NO>
  - OpenClaw native: <YES/NO>
  - IronClaw native setup: <YES/NO>
  - CLI: <YES/NO>
- Install-level validation allowed: <YES/NO>

### 2) Required changes
- Update `workspace.json` using path placeholders (for example `${SKILLS_BASE}/...`).
- If needed, declare direct dependencies via `dependsOn`.
- Ensure minimum artifacts in skill repo:
  - `package.json` name/version
  - `package.json bin` with a stable setup executable
  - `SKILL.md` front matter name/description (and `version` + `activation.*` for IronClaw when applicable)
  - MCP support (`src/mcp/server.ts` or `scripts.mcp`)
  - `openclaw.json` if OpenClaw native is declared
  - setup support (`scripts.setup` or `bin/setup.ts|bin/setup.js`), including `setup ironclaw` when IronClaw native setup is declared
  - README / SKILL distribution wording: GitHub discovery only, activation via npm/ClawHub contract
- Regenerate catalog and README snapshots.

### 3) Schema references (MUST)
- `docs/schemas/workspace.schema.json`
- `docs/schemas/skill-frontmatter.schema.json`
- `docs/schemas/openclaw.schema.json`
- `docs/schemas/skills-catalog.schema.json`

### 4) Output format (MUST include all sections)
1. Goal / Non-goal
2. Files to change
3. Contract mapping (MUST-by-MUST)
4. Validation commands
5. Risk & rollback
6. Acceptance evidence

### 5) Validation commands (run and report)
```bash
bun run catalog:generate
bun run health:check
bun run readme:check
bun run security:audit
./bootstrap.sh --only <SKILL_ID> --skip-install
```

If install-level validation is allowed, also run:
```bash
./bootstrap.sh --only <SKILL_ID>
```

### 6) Prohibited actions
- Do not skip `workspace.json`.
- Do not declare capability without required artifact.
- Do not treat GitHub tree URLs as final OpenClaw/IronClaw install inputs.
- Do not hide failed commands.
- Do not ignore `[FAIL]` outputs.
- If rules/contracts/templates are updated, update Chinese and English docs together.
````

## Recommended Optional Inputs

1. Current `SKILL.md` content (if it already exists).
2. Current `package.json` scripts.
3. Client priority order (OpenClaw/Cursor/Codex/Claude Code).
4. Whether dependency declaration (`dependsOn`) is required.
