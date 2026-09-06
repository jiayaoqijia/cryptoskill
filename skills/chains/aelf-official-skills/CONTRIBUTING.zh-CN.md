中文 | [English](CONTRIBUTING.md)

# aelf-skills 贡献规范（新增 Skill）

本规范是人类贡献者与 AI Agent 共用的硬门禁。
中文为主版本，英文为镜像版本。

## 1. 目标

1. 让新增 skill 接入可一次执行通过。
2. 消除冷启动 AI Agent 的歧义空间。
3. 保持规则、脚本、模板、产物一致。

## 2. 范围与非目标

1. 范围
- 本仓接入：`workspace.json`、`skills-catalog.json`、README 快照、bootstrap/health/readme/security 门禁。

2. 非目标
- 不改各 skill 仓业务逻辑。
- 不替代各 skill 仓 SDK/API 文档。
- 不迁移 `agent-skills-e2e` 职责。

## 3. 双语策略（强制）

1. 中文主版本先更新。
2. 英文镜像必须同结构、同章节编号、同 MUST 语义。
3. 规则变更即接口变更：契约/模板/规则改动必须中英同 PR 提交。

## 4. 新增 Skill 硬门槛（MUST）

1. 在 `workspace.json` 注册项目路径并保持 JSON 有效。
2. 目标 skill 仓必须包含：
- `package.json` 且含 `name`、`version`
- `SKILL.md` front matter 含 `name`、`description`
- MCP 支持：`src/mcp/server.ts` 或 `scripts.mcp`
- 声明 OpenClaw native 时必须有 `openclaw.json`
- setup 支持：`scripts.setup` 或 `bin/setup.ts|bin/setup.js`
3. `SKILL.md` 必须明确能力边界：capabilities、limits、risks、non-goals。
4. 强制 schema 引用：
- `docs/schemas/workspace.schema.json`
- `docs/schemas/skill-frontmatter.schema.json`
- `docs/schemas/openclaw.schema.json`
- `docs/schemas/skills-catalog.schema.json`

## 5. 路径可移植与环境变量契约（MUST）

1. `workspace.json` 路径应优先使用环境变量占位（如 `${SKILLS_BASE}/AElf/aelf-node-skill`）。
2. 占位符无法解析属于阻塞错误。
3. 推荐本地配置：

```bash
export SKILLS_BASE=/path/to/your/workspace
```

## 6. 依赖与冲突规则（MUST）

1. `workspace.json.projects[].dependsOn` 为可选，表示直接依赖 skill id。
2. `dependsOn` 必须去重，且只能引用已存在 skill id。
3. catalog 生成时出现重复 skill id 必须阻塞失败。
4. `bootstrap --only` 会自动解析传递依赖闭包。
5. 依赖环必须阻塞失败。

## 7. 实施流程

1. 在 skill 仓补齐最小产物。
2. 更新本仓 `workspace.json`。
3. 执行 `bun run catalog:generate`。
4. 执行 `bun run health:check`。
5. 执行 `bun run readme:check`。
6. 执行 `bun run security:audit`。
7. 执行 `./bootstrap.sh --only <skill-id> --skip-install`。
8. 提交 PR 并附命令输出摘要。

黄金路径示例：`docs/examples/EXAMPLE_NEW_SKILL_DIFF.zh-CN.md`。

## 8. 验收门禁（MUST）

```bash
bun run catalog:generate
bun run health:check
bun run readme:check
bun run security:audit
./bootstrap.sh --only <skill-id> --skip-install
```

说明：
1. 需完整依赖验证时可去掉 `--skip-install`。
2. `workspace.json` 可包含非 skill 仓；出现 `[WARN]` 可接受，但必须在 PR 说明。

## 9. 失败映射（Pattern -> Cause -> Fix）

| 输出模式 | 原因 | 修复动作 |
|---|---|---|
| `[WARN] ... SKILL.md not found, project skipped` | 项目缺少 `SKILL.md` | 补齐 `SKILL.md` 与 front matter |
| `declared native-setup but setup command not available` | 声明 native-setup 但无 setup 入口 | 增加 `scripts.setup` 或 `bin/setup.ts/js` |
| `declared openclaw native but openclaw.json missing` | 声明 OpenClaw native 但缺配置 | 补齐合法 `openclaw.json` |
| `[WARN] Unknown skill IDs in --only: ...` | `--only` 输入了无效 id | 修正 id 后重试 |
| `[FAIL] Duplicate skill id detected:` | 两个项目映射到同一 skill id | 修正 front matter 或 workspace 路径 |
| `[FAIL] <id>: dependsOn references unknown skill id` | 依赖声明无效 | 修正 `dependsOn` id |
| `[FAIL] Dependency cycle detected: ...` | 依赖图存在环 | 移除 `dependsOn` 环路 |
| `[FAIL] Unresolved environment variable(s) in path` | workspace 路径依赖的环境变量未设置 | 导出变量（如 `SKILLS_BASE`） |

## 10. CI/CD 门禁

1. CI workflow：`.github/workflows/gates.yml`。
2. CI 使用 fixture workspace（`testdata/workspace.ci.json`）保证稳定可重复。
3. CI 命令集：
- 使用 fixture workspace 执行 `catalog:generate`
- 对 fixture catalog 执行 `health:check`
- 执行 `readme:check`
- 执行 `security:audit`
- 执行 `bootstrap --only fixture-node-skill --source local --skip-install`
4. Fixture CI 是基础门禁，真实多仓联调仍由本地承担。

## 11. 安全边界

1. `bootstrap` 不执行 setup 命令；仅下载、可选安装依赖、健康检查。
2. setup 命令安全通过 `bun run security:audit` 模式扫描兜底。
3. 高风险模式（如 `curl|bash`、`sh -c`）必须移除或在合并前给出充分说明。

## 12. PR 提交要求

1. PR 说明必须包含 Goal/Non-goal、关键文件、验证命令、风险、回滚。
2. 中英文文档必须同 PR 同步。
3. 当规则/契约/模板变更时，不接受仅改 README。
