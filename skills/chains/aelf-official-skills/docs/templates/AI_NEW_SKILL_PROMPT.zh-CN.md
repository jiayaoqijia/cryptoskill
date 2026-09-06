中文 | [English](AI_NEW_SKILL_PROMPT.md)

# AI 新增 Skill Prompt 模板（中文主版本）

将以下模板完整复制给 AI，再替换 `<...>` 占位符。

## Prompt Template

````md
你是本仓实现代理。
请严格遵循 `docs/AI_SKILL_CONTRACT.zh-CN.md`。

### 1) Context
- Aggregation repo: <AGGREGATION_REPO_PATH>
- Skill repo path/url: <SKILL_REPO_PATH_OR_URL>
- Skill id: <SKILL_ID>
- NPM package: <NPM_PACKAGE_NAME>@<VERSION_OR_LATEST>
- Workspace 环境变量根路径（默认）：SKILLS_BASE=<PATH_TO_WORKSPACE_ROOT>
- Capability boundary:
  - MCP: <YES/NO>
  - OpenClaw native: <YES/NO>
  - IronClaw native setup: <YES/NO>
  - CLI: <YES/NO>
- Install-level validation allowed: <YES/NO>

### 2) Required changes
- 更新 `workspace.json`，路径使用占位符（例如 `${SKILLS_BASE}/...`）。
- 如有依赖，声明直接依赖 `dependsOn`。
- 确保 skill 仓最小产物：
  - `package.json` name/version
  - `package.json bin` 中有稳定的 setup 可执行入口
  - `SKILL.md` front matter name/description（如适用，再加 `version` 与 `activation.*`）
  - MCP 支持（`src/mcp/server.ts` 或 `scripts.mcp`）
  - 声明 OpenClaw native 时需要 `openclaw.json`
  - setup 支持（`scripts.setup` 或 `bin/setup.ts|bin/setup.js`）；若声明 IronClaw native setup，还需支持 `setup ironclaw`
  - README / SKILL 明确 GitHub 只负责 discovery，activation 走 npm/ClawHub 契约
- 重新生成 catalog 与 README 快照。

### 3) Schema references (MUST)
- `docs/schemas/workspace.schema.json`
- `docs/schemas/skill-frontmatter.schema.json`
- `docs/schemas/openclaw.schema.json`
- `docs/schemas/skills-catalog.schema.json`

### 4) Output format（MUST include all sections）
1. Goal / Non-goal
2. Files to change
3. Contract mapping (MUST-by-MUST)
4. Validation commands
5. Risk & rollback
6. Acceptance evidence

### 5) Validation commands（run and report）
```bash
bun run catalog:generate
bun run health:check
bun run readme:check
bun run security:audit
./bootstrap.sh --only <SKILL_ID> --skip-install
```

若允许完整安装验证，再执行：
```bash
./bootstrap.sh --only <SKILL_ID>
```

### 6) Prohibited actions
- 不得跳过 `workspace.json`。
- 不得声明能力却缺少产物。
- 不得把 GitHub tree URL 当作 OpenClaw/IronClaw 的最终安装输入。
- 不得隐藏失败命令输出。
- 不得忽略 `[FAIL]` 输出。
- 若规则/契约/模板有变更，必须同步更新中英文文档。
````

## 推荐附加输入

1. `SKILL.md` 当前内容（若已有）。
2. `package.json` 当前 scripts。
3. 客户端优先级（OpenClaw/Cursor/Codex/Claude Code）。
4. 是否需要声明依赖（`dependsOn`）。
