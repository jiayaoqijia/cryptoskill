中文 | [English](AI_SKILL_CONTRACT.md)

# AI Skill 接入执行契约（AI Skill Contract）

本契约定义 AI 在“新增 skill 接入本聚合仓”时的强约束行为。
关键词语义采用 RFC 风格：
- `MUST`：必须
- `SHOULD`：建议（有充分理由可偏离）
- `MAY`：可选

## 1. 目标

1. 确保 AI 一次生成可执行、可验证、可合并的变更。
2. 确保 AI 输出与仓库门禁和 schema 一致。

## 2. 输入契约（AI 接收）

AI 执行前必须拿到：
1. 聚合仓路径。
2. 新 skill 仓路径或 URL。
3. skill npm 包名（若已发布）与目标 `skill-id`。
4. 能力边界（MCP/OpenClaw/CLI）。
5. 是否允许 install 级验证。
6. 环境变量占位根路径（默认 `SKILLS_BASE`）。

若输入缺失：
1. AI `MUST` 明确列出缺失项。
2. AI `SHOULD` 提供默认值并标记 assumptions。

## 3. 输出契约（AI 产出）

AI 输出 `MUST` 严格包含 6 个段落：
1. Goal / Non-goal
2. Files to change
3. Contract mapping（逐条映射 MUST）
4. Validation commands
5. Risk & rollback
6. Acceptance evidence

AI 输出 `MUST NOT` 停留在高层建议而不落地到文件和命令。

## 4. 文件与 Schema 契约（MUST）

1. `workspace.json`
- `MUST` 注册新项目路径。
- `MUST` 满足 `docs/schemas/workspace.schema.json`。
- `MAY` 包含 `dependsOn`（直接依赖 skill id）。

2. 目标 skill 仓
- `MUST` 存在 `package.json` 且有 `name`、`version`。
- `MUST` 通过 `package.json bin` -> `bin/setup.js|bin/setup.ts` 暴露稳定的 npm installer binary。
- `MUST` 存在 `SKILL.md` front matter 且有 `name`、`description`。
- 若 skill 支持 IronClaw 路由，`SHOULD` 增加 `version` 与 `activation.*` 字段。
- `MUST` 满足 `docs/schemas/skill-frontmatter.schema.json`。
- `MUST` 提供 MCP 支持：`src/mcp/server.ts` 或 `scripts.mcp`。
- 声明 OpenClaw native 时，`MUST` 存在 `openclaw.json` 且满足 `docs/schemas/openclaw.schema.json`。
- 声明 native setup 时，`MUST` 存在 `scripts.setup` 或 `bin/setup.ts|bin/setup.js`。
- 若声明 IronClaw native setup，setup 入口必须支持 `bun run setup ironclaw`（或等价 `bin/setup.ts ironclaw`）。
- GitHub repo/tree URL 仅用于 discovery；OpenClaw/IronClaw 的最终 activation `MUST` 通过 catalog 元数据表达。

3. 生成产物
- `MUST` 输出 schemaVersion `1.3.0` 的 catalog。
- `MUST` 满足 `docs/schemas/skills-catalog.schema.json`。
- 若 workspace 声明 `dependsOn`，catalog `MUST` 同步输出。
- 对外发布/可安装 skill，`MUST` 额外输出 `distributionSources` 与 `clientInstall`。

4. 文档同步
- 若规则/契约/模板发生变更，AI `MUST` 同步更新中英文文档。

## 5. 依赖、冲突与路径规则（MUST）

1. `dependsOn` 必须引用已存在 skill id。
2. 重复 skill id 属于阻塞失败。
3. `bootstrap --only` 必须自动带上传递依赖。
4. 依赖环属于阻塞失败。
5. workspace 路径中的 `${ENV_VAR}` 必须可解析；无法解析属于阻塞失败。

## 6. 验证契约（MUST）

AI 完成后必须执行并报告：

```bash
bun run catalog:generate
bun run health:check
bun run readme:check
bun run security:audit
./bootstrap.sh --only <skill-id> --skip-install
```

可选完整安装验证：

```bash
./bootstrap.sh --only <skill-id>
```

## 7. 禁止项（MUST NOT）

1. 跳过 `workspace.json` 注册。
2. 规则变更时只改 README，不改契约/模板文档。
3. 声明能力却缺少对应产物。
4. 隐藏失败命令输出。
5. 忽略 `[FAIL]` 门禁却宣称完成。

## 8. 失败处理与回滚（SHOULD）

1. 任一门禁失败时，AI `SHOULD` 给出最小修复路径。
2. 当前轮无法修复时，AI `MUST` 说明 blocker 与影响范围。
3. AI `SHOULD` 给出回滚点（需撤销的文件）。

## 9. 常见失败模式映射

| 输出模式 | 原因 | 修复 |
|---|---|---|
| `[WARN] ... SKILL.md not found, project skipped` | skill 缺少 markdown | 补齐 `SKILL.md` 与 front matter |
| `declared native-setup but setup command not available` | 缺 setup 入口 | 增加 `scripts.setup` 或 `bin/setup.ts/js` |
| `declared openclaw native but openclaw.json missing` | 缺 OpenClaw 配置 | 补齐 `openclaw.json` |
| `[FAIL] Duplicate skill id detected:` | skill id 冲突 | 修正 front matter `name`/workspace 映射 |
| `[FAIL] <id>: dependsOn references unknown skill id` | 依赖 id 无效 | 修正 `dependsOn` |
| `[FAIL] Dependency cycle detected: ...` | 依赖图有环 | 解除环路 |
| `[FAIL] Unresolved environment variable(s) in path` | 环境变量未设置 | 导出所需环境变量 |

## 10. 完成定义（Definition of Done）

满足以下条件才算完成：
1. 新 skill 出现在 `skills-catalog.json`（schema `1.3.0`）。
2. `health:check` 无 fail。
3. `readme:check` 通过。
4. `security:audit` 通过。
5. `bootstrap --only <skill-id>` 可运行（快速门禁可用 `--skip-install`）。
6. 中英文文档同步，章节编号一致。
