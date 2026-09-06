中文 | [English](NEW_SKILL_CHECKLIST.md)

# 新增 Skill PR Checklist（中文主版本）

在 PR 中复制并勾选以下清单。

## 1. 基础注册

- [ ] 已在 `workspace.json` 注册新项目路径。
- [ ] 路径可解析（`${SKILLS_BASE}` 或等效环境变量已配置）。
- [ ] 如存在依赖，`dependsOn` 已声明且仅包含直接 skill id。

## 2. 最低产物（MUST）

- [ ] `package.json` 存在且含 `name`、`version`。
- [ ] `package.json bin` 暴露稳定的 setup 可执行入口（`bin/setup.js|bin/setup.ts`）。
- [ ] `SKILL.md` 存在且 front matter 含 `name`、`description`。
- [ ] MCP 支持存在：`src/mcp/server.ts` 或 `scripts.mcp`。
- [ ] 若声明 OpenClaw native，`openclaw.json` 存在。
- [ ] 若声明 native-setup，存在 `scripts.setup` 或 `bin/setup.ts|bin/setup.js`。
- [ ] 若声明 IronClaw native setup，必须支持 `setup ironclaw` 且安装到 trusted skill 路径。

## 3. Schema 一致性

- [ ] `workspace.json` 满足 `docs/schemas/workspace.schema.json`。
- [ ] `SKILL.md` front matter 满足 `docs/schemas/skill-frontmatter.schema.json`。
- [ ] `openclaw.json`（若存在）满足 `docs/schemas/openclaw.schema.json`。
- [ ] 生成后的 `skills-catalog.json` 满足 `docs/schemas/skills-catalog.schema.json`。
- [ ] 生成后的 catalog 包含 `distributionSources` 与 `clientInstall`。

## 4. 架构与产品要求

- [ ] 配置优先，无第三方服务硬编码开关。
- [ ] 外部依赖失败可降级，不阻塞主流程。
- [ ] 错误语义统一并具备 trace 线索。
- [ ] `SKILL.md` 明确 capabilities、limits、risks、non-goals。

## 5. 门禁命令

- [ ] `bun run catalog:generate`
- [ ] `bun run health:check`
- [ ] `bun run readme:check`
- [ ] `bun run security:audit`
- [ ] `./bootstrap.sh --only <skill-id> --skip-install`

可选完整验证：
- [ ] `./bootstrap.sh --only <skill-id>`

## 6. 文档同步（双语强制）

- [ ] 中文文档已更新：`CONTRIBUTING.zh-CN.md` / `docs/*.zh-CN.md`（规则变更时）。
- [ ] 英文镜像已同步：`CONTRIBUTING.md` / `docs/*.md`。
- [ ] 中英文章节编号与 MUST 顺序一致。

## 7. PR 信息完整性

- [ ] PR 描述包含 Goal / Non-goal。
- [ ] PR 描述包含关键变更文件列表。
- [ ] PR 描述包含命令输出摘要。
- [ ] PR 描述包含风险与回滚方案。
