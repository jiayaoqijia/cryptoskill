中文 | [English](README.md)

# aelf Skills

这是 aelf 技能生态的统一发现与 bootstrap 入口。

[![npm](https://img.shields.io/npm/v/@blockchain-forever/aelf-skills)](https://www.npmjs.com/package/@blockchain-forever/aelf-skills)

本仓库提供：
1. 面向人类与 AI 的双语入口文档。
2. 机器可读目录：`skills-catalog.json`。
3. 一键脚本：`bootstrap.sh`。

## AI 快速指令（OpenClaw / Codex / Cursor / Claude Code）

```text
仓库：https://github.com/AElfProject/aelf-skills
这是一个跨客户端通用指令，可用于 OpenClaw、Codex、Cursor、Claude Code。
先读取：skills-catalog.json、docs/SKILL_ROUTING_MATRIX.zh-CN.md、docs/AI_E2E_SCENARIOS.zh-CN.md。
然后执行：
1) ./bootstrap.sh --source github --dest ./downloaded-skills
2) bun run health:check -- --skills-root ./downloaded-skills
3) 读取 `skills-catalog.json` 里的 `clientInstall.openclaw` / `clientInstall.ironclaw`；若存在 `installCommand`，由宿主或 agent 在本地执行，而不是把 GitHub tree URL 当成最终安装输入
路由规则：按 SKILL_ROUTING_MATRIX；若有歧义，输出 Recommended/Alternative/Reason。
失败规则：按 docs/AI_E2E_SCENARIOS.zh-CN.md 的常见错误恢复模板执行。
```

## 范围说明

本入口仓只负责 **发现、下载、安装、能力索引**。

不会替代各 skill 仓内部客户端接入逻辑。
`OpenClaw`、`Cursor`、`Claude Desktop`、`IronClaw`、`Codex`、`Claude Code` 的具体接入仍由各 skill 仓负责。
AI Agent 可直接跳转到 [AI 导航入口](#ai-导航入口) 查看路由与执行指引。

## Discovery 与 Activation

Skill 分发一律拆成两个阶段：
1. `discovery`：GitHub repo URL / npm package / ClawHub slug 负责让宿主发现 skill。
2. `activation`：宿主或 agent 读取 `skills-catalog.json` 中的机器契约并执行安装命令。

固定规则：
1. GitHub tree/repo URL 只用于 discovery，不是 IronClaw 的最终安装载体。
2. IronClaw 一律优先读取 `clientInstall.ironclaw.installCommand`，并预期存在 trusted 本地安装步骤。
3. OpenClaw 若存在 `distributionSources.clawhubId`，优先走 `ClawHub` / managed install；否则回退到 `clientInstall.openclaw.installCommand`。

## 环境依赖

- `bun >= 1.1.0`（硬要求）
- `npm >= 10`
- `git >= 2.39`
- `tar`（GNU tar 或 bsdtar）

## 本地环境配置

`workspace.json` 使用 `${SKILLS_BASE}` 占位路径以保证可移植性。
`workspace.json` 仅用于 Codex 本地工作区配置；外部消费者请直接使用 `skills-catalog.json` 作为数据源。

```bash
export SKILLS_BASE=/path/to/your/workspace
```

示例：
- `${SKILLS_BASE}/AElf/aelf-node-skill`
- `${SKILLS_BASE}/awaken/awaken-agent-skills`

## 安装

```bash
npm install @blockchain-forever/aelf-skills
# 或
bun add @blockchain-forever/aelf-skills
```

## 快速开始

```bash
# 1) 生成公开 catalog 并同步 README 表格
bun run catalog:generate

# 2) 生成包含 sourcePath 的本地 catalog（用于本地 bootstrap/health）
bun run catalog:generate:local

# 3) 执行基础门禁
bun run health:check
bun run readme:check
bun run security:audit

# 4) 拉起指定 skill
./bootstrap.sh --only aelf-node-skill --skip-install

# 5) 检查 hub/catalog 版本漂移（非阻塞）
bun run update:check
```

## Bootstrap 命令

```bash
./bootstrap.sh [--catalog <path>] [--dest <dir>] [--source auto|npm|github|local] [--skip-install] [--skip-health] [--only <csv>]
```

默认行为：
1. `--source auto`（先 npm，失败回退 github）
2. 默认执行 install
3. 默认执行 health
4. 默认使用 `skills-catalog.json`

## 更新自检

`aelf-skills` 内置了更新提醒，会在 `bootstrap`、`health:check`、`catalog:generate` 运行时做非阻塞检测。
检测结果使用本地缓存（默认 TTL 24 小时），不会阻塞主流程。
提醒输出会基于 `lastNotifiedAt` 做节流：默认 24 小时内最多提示一次。

命令：
1. `bun run update:check`
2. `bun run update:check -- --force`
3. `bun run update:check:json`

环境变量：
1. `AELF_SKILLS_UPDATE_CHECK=0|1`（默认 `1`）
2. `AELF_SKILLS_UPDATE_TTL_HOURS=24`（默认 `24`）
3. `AELF_SKILLS_UPDATE_CACHE_PATH=<path>`（默认 `~/.aelf-skills/update-check-cache.json`）

## 机器清单说明

`skills-catalog.json` 是稳定机器接口。

每个 skill 关键字段：
1. `id`, `displayName`
2. `npm`（`name`, `version`）
3. `repository.https`
4. `distributionSources`（`githubRepo`, `npmPackage`，以及可选 `clawhubId`）
5. `description`, `capabilities`
6. `artifacts`（`skillMd`, `mcpServer`, `openclaw`）
7. `setupCommands`（兼容展示字段，例如 `claudeDesktop`、`cursor`、`openclaw`、`ironclaw`）
8. `clientSupport`（支持矩阵，例如 `claude_desktop`、`cursor`、`ironclaw`、`codex`）
9. `clientInstall`（`openclaw` / `ironclaw` 的机器可执行安装契约）
10. `dependsOn`（可选，schema `1.3.0`）

Schema 参考：
1. `docs/schemas/workspace.schema.json`
2. `docs/schemas/skill-frontmatter.schema.json`
3. `docs/schemas/openclaw.schema.json`
4. `docs/schemas/skills-catalog.schema.json`

Schema 演进规则：
1. `patch`（`1.3.x`）：文案/文档修订，不改变字段语义。
2. `minor`（`1.x.0`）：向后兼容的字段新增。
3. `major`（`x.0.0`）：仅用于破坏性变更。

## AI 导航入口

1. Catalog 字段语义：[docs/CATALOG_SCHEMA.zh-CN.md](docs/CATALOG_SCHEMA.zh-CN.md) | [docs/CATALOG_SCHEMA.md](docs/CATALOG_SCHEMA.md)
2. Intent 路由矩阵：[docs/SKILL_ROUTING_MATRIX.zh-CN.md](docs/SKILL_ROUTING_MATRIX.zh-CN.md) | [docs/SKILL_ROUTING_MATRIX.md](docs/SKILL_ROUTING_MATRIX.md)
3. 端到端执行场景（含恢复建议）：[docs/AI_E2E_SCENARIOS.zh-CN.md](docs/AI_E2E_SCENARIOS.zh-CN.md) | [docs/AI_E2E_SCENARIOS.md](docs/AI_E2E_SCENARIOS.md)
4. Type Safety 基线与推进状态：[docs/TYPE_SAFETY_MATRIX.zh-CN.md](docs/TYPE_SAFETY_MATRIX.zh-CN.md) | [docs/TYPE_SAFETY_MATRIX.md](docs/TYPE_SAFETY_MATRIX.md)

## 当前技能快照

该表由 `bun run catalog:generate` 自动同步。

<!-- SKILL_TABLE_START -->
| ID | npm 包名 | 版本 | OpenClaw 工具数 | 描述 |
|---|---|---:|---:|---|
| aelf-node-skill | @blockchain-forever/aelf-node-skill | 0.1.3 | 11 | AElf 节点查询与合约调用技能。 |
| aelfscan-skill | @aelfscan/agent-skills | 0.2.2 | 61 | AelfScan 浏览器数据检索与分析技能。 |
| awaken-agent-skills | @awaken-finance/agent-kit | 1.2.4 | 11 | Awaken DEX 交易与行情数据技能。 |
| eforest-agent-skills | @eforest-finance/agent-skills | 0.4.3 | 48 | eForest 代币与 NFT 市场操作技能。 |
| portkey-ca-agent-skills | @portkey/ca-agent-skills | 2.3.0 | 32 | Portkey CA 钱包注册、认证、Guardian 与转账技能。 |
| portkey-eoa-agent-skills | @portkey/eoa-agent-skills | 1.2.6 | 21 | Portkey EOA 钱包与资产操作技能。 |
| tomorrowdao-agent-skills | @tomorrowdao/agent-skills | 0.2.0 | 44 | TomorrowDAO 治理、BP 与资源操作技能。 |
<!-- SKILL_TABLE_END -->

## 健康检查

若检查失败，请参考 [常见错误恢复模板](docs/AI_E2E_SCENARIOS.zh-CN.md#常见错误恢复模板)。

```bash
# 检查 workspace.json 中的本地源仓
bun run health:check

# 检查指定下载目录
bun run health:check -- --skills-root ./downloaded-skills
```

## 安全边界

1. `bootstrap` 不执行 setup 命令。
2. `bootstrap` 仅做下载、可选依赖安装、health 检查。
3. 使用 `bun run security:audit` 检测 setup 命令风险模式。

## CI 门禁

CI workflow：`.github/workflows/gates.yml`

基于 fixture 的稳定门禁：
1. 使用 `testdata/workspace.ci.json` 执行 `catalog:generate`
2. 对 fixture catalog 执行 `health:check`
3. 执行 `readme:check`
4. 执行 `security:audit`
5. 执行 `bootstrap --only fixture-node-skill --source local --skip-install`

## 贡献规范

1. 贡献规范：[CONTRIBUTING.zh-CN.md](CONTRIBUTING.zh-CN.md) | [CONTRIBUTING.md](CONTRIBUTING.md)
2. AI 执行契约：[docs/AI_SKILL_CONTRACT.zh-CN.md](docs/AI_SKILL_CONTRACT.zh-CN.md) | [docs/AI_SKILL_CONTRACT.md](docs/AI_SKILL_CONTRACT.md)
3. AI Prompt 模板：[docs/templates/AI_NEW_SKILL_PROMPT.zh-CN.md](docs/templates/AI_NEW_SKILL_PROMPT.zh-CN.md) | [docs/templates/AI_NEW_SKILL_PROMPT.md](docs/templates/AI_NEW_SKILL_PROMPT.md)
4. PR 自检清单：[docs/templates/NEW_SKILL_CHECKLIST.zh-CN.md](docs/templates/NEW_SKILL_CHECKLIST.zh-CN.md) | [docs/templates/NEW_SKILL_CHECKLIST.md](docs/templates/NEW_SKILL_CHECKLIST.md)
5. SKILL 模板：[docs/templates/SKILL_TEMPLATE.zh-CN.md](docs/templates/SKILL_TEMPLATE.zh-CN.md) | [docs/templates/SKILL_TEMPLATE.md](docs/templates/SKILL_TEMPLATE.md)
6. 黄金路径示例：[docs/examples/EXAMPLE_NEW_SKILL_DIFF.zh-CN.md](docs/examples/EXAMPLE_NEW_SKILL_DIFF.zh-CN.md) | [docs/examples/EXAMPLE_NEW_SKILL_DIFF.md](docs/examples/EXAMPLE_NEW_SKILL_DIFF.md)
