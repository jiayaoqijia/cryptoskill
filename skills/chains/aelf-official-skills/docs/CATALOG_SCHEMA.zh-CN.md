中文 | [English](CATALOG_SCHEMA.md)

# Catalog Schema 语义说明（v1.3.0）

本文档定义 `skills-catalog.json` 的字段语义，供 AI 与开发者统一理解。

## 1. 顶层结构

```json
{
  "schemaVersion": "1.3.0",
  "generatedAt": "ISO-8601",
  "source": "workspace.json",
  "skills": [],
  "warnings": []
}
```

字段说明：
1. `schemaVersion`：schema 版本。当前为 `1.3.0`。
2. `generatedAt`：生成时间（UTC ISO 字符串）。
3. `source`：catalog 的输入来源文件名。
4. `skills`：技能数组。
5. `warnings`：非阻断告警（例如路径存在但不是 skill 仓）。公开模式默认做路径脱敏，不暴露本机绝对路径。

## 2. skill 字段语义

每个 `skills[]` 包含：
1. `id`：稳定的路由 ID，用于 `--only <skill-id>`。
2. `displayName`：面向人类展示名称。
3. `npm.name` / `npm.version`：默认下载坐标与版本。
4. `repository.https`：npm 失败时 github fallback 地址。
5. `distributionSources`：机器可读 discovery 源（`githubRepo`, `npmPackage`，以及可选 `clawhubId`）。
6. `description`：技能简介（用于高层路由）。
7. `description_zh`：可选中文描述。中文界面优先使用，缺失时回退 `description`。
8. `capabilities`：能力短句列表（用于 intent 匹配）。
9. `artifacts`：能力产物存在性布尔值。
10. `setupCommands`：面向人类/本地仓的兼容展示命令。
11. `clientSupport`：客户端支持级别矩阵，包含 `ironclaw`。
12. `clientInstall`：`openclaw` 与 `ironclaw` 的机器可执行 activation 契约。
13. `openclawToolCount`：OpenClaw 工具数量。
14. `dependsOn`：可选直接依赖 skill id 列表，用于编排顺序与组合执行。
15. `sourcePath`：仅本地模式可选字段，公开 catalog 默认不含。

## 3. artifacts 语义

1. `skillMd: true`
- 意味着目标仓存在 `SKILL.md`，可提取能力、限制与安全规则。

2. `mcpServer: true`
- 意味着存在 `src/mcp/server.ts` 或等价 `scripts.mcp` 能力入口。

3. `openclaw: true`
- 意味着存在 `openclaw.json` 可用于 OpenClaw 工具描述。

## 4. `distributionSources` 与 `clientInstall`

1. `distributionSources`
- 用来描述宿主在哪里发现 skill。
- `githubRepo` 只用于源码定位，不是 IronClaw 的最终 activation 输入。
- `npmPackage` 是默认可执行分发坐标。
- `clawhubId` 仅在 OpenClaw managed install 可用时出现。

2. `clientInstall.openclaw`
- `managed-install`：宿主应走 ClawHub / managed install，本地无需执行命令。
- `package-setup`：宿主应执行 `installCommand`，通常是 `bunx -p <pkg> <setup-bin> openclaw`。

3. `clientInstall.ironclaw`
- `trusted-local-install`：宿主应执行 `installCommand`，通常是 `bunx -p <pkg> <setup-bin> ironclaw`。
- `requiresTrustPromotion: true` 表示宿主必须给出 trust 提示，因为会写入 trusted 本地 skill 与 MCP 配置。

## 5. clientSupport 枚举语义

1. `native`
- 开箱即用，通常有官方产物 + setup 命令。

2. `native-setup`
- 有原生支持，但需要先执行 setup 命令注入配置。

3. `manual-mcp`
- 支持 MCP，但需手工配置，不保证一键 setup。

4. `manual-cli-or-mcp`
- 可通过 CLI 或 MCP 手工接入。

5. `manual`
- 可手工使用，但无标准自动 setup 路径。

6. `unsupported`
- 当前不支持该客户端。

## 6. capabilities 写法规范

建议：
1. 使用动词开头的短句（例如 `Query block status`、`Create wallet`）。
2. 一条能力描述一个动作，不混合多个独立流程。
3. 避免模糊词（如 `handle everything`）。
4. 包含边界词（如 `read-only`、`simulate/send`）。

## 7. 模式与兼容性

1. 公开模式（默认）
- 命令：`bun run catalog:generate`
- 输出：`skills-catalog.json`
- 特点：不包含 `sourcePath`，warnings 经过路径脱敏，适合外部 AI 消费。

2. 本地模式（路径调试）
- 命令：`bun run catalog:generate:local`
- 输出：`skills-catalog.local.json`
- 特点：包含 `sourcePath`，仅适用于本机环境。

3. 增量说明（1.3.0）
- 新增 `setupCommands.ironclaw`，用于表达 trusted skill setup 命令。
- 新增 `clientSupport.ironclaw`，用于表达 IronClaw 支持级别。
- 新增 `distributionSources` 与 `clientInstall`，用于区分 discovery 与 activation。
- 旧消费者如暂不使用新增字段，需按“忽略未知字段”兼容读取。
