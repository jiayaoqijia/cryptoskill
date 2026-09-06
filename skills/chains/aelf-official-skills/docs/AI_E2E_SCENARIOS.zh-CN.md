中文 | [English](AI_E2E_SCENARIOS.md)

# AI 端到端执行场景

本文给出可直接执行的 AI 场景链路，帮助模型理解“从路由到执行”的完整路径。

## 场景 1：查询 aelf 区块高度

目标：用户说“帮我查当前链上区块高度”。

执行链路：
1. 读取 `skills-catalog.json`，定位具备链读取能力的 skill。
2. 通过路由矩阵选择 `aelf-node-skill`（而非 `aelfscan`）。
3. 运行快速引导：
```bash
./bootstrap.sh --only aelf-node-skill --skip-install
```
4. 根据该 skill 仓文档完成客户端接入（MCP/OpenClaw/CLI 任一）。
5. 调用对应读取工具（如 get-chain-status / get-block-height）。

成功标准：
1. 能返回最新区块高度。
2. 输出中包含使用的 skill 与调用方式（便于追踪）。

## 场景 2：转账前路由（EOA/CA）

目标：用户说“帮我转账 1 ELF 给某地址”，但未说明身份模式。

执行链路：
1. 先做身份路由判断：
- 若无 CA 关键词，默认 `portkey-eoa-agent-skills`。
- 若出现 guardian/CA hash/register/recover，切 `portkey-ca-agent-skills`。
2. 确认 active wallet context 已设置（`portkey_set_active_wallet` 或 create/unlock 自动写入）。
3. 先执行只读检查（余额、地址合法性、网络配置）。
4. 再执行写操作（transfer），并使用 `signerMode=auto`。
5. 若 context 指向加密钱包，补充 `password` 入参或密码 env。
6. 若用户希望先模拟，优先走 simulate 或 dry-run（若工具支持）。

成功标准：
1. 路由决策可解释（为什么选 EOA/CA）。
2. 转账前有必要前置检查，避免直接写链。
3. 输出包含失败恢复建议（余额不足、网络错误、context/密码缺失）。

## 场景 3：Awaken Swap 组合编排（钱包 + DEX）

目标：用户说“帮我在 Awaken 上把 ELF 换成 USDT”。

执行链路：
1. 先用路由矩阵判定钱包身份模式：
- 无 CA 信号：`portkey-eoa-agent-skills`
- 有 CA/guardian 信号：`portkey-ca-agent-skills`
2. 使用钱包 skill 做只读前置检查（余额、地址、网络）并确认 active context。
3. 使用 `awaken-agent-skills` 获取 quote。
4. 使用 `signerMode=auto` 执行 allowance/approve 与 swap（或优先 simulate/dry-run）。
5. 若 context signer 需要解密密码，补充 `password` 入参或密码 env。
6. 返回交易结果并附带本次组合路由说明。

成功标准：
1. 明确给出“钱包 skill + Awaken skill”的组合关系。
2. swap 前已完成必要前置检查与权限检查。
3. 输出包含失败恢复建议（余额不足、approve 失败、网络异常）。

## 场景 4：AI 作为贡献者接入新 Skill

目标：AI 收到“将一个新 skill 接入本聚合仓”的需求。

执行链路：
1. 先读取 `CONTRIBUTING.zh-CN.md` 与 `docs/AI_SKILL_CONTRACT.zh-CN.md`。
2. 对照 schema 校验目标结构：
- `docs/schemas/workspace.schema.json`
- `docs/schemas/skill-frontmatter.schema.json`
- `docs/schemas/openclaw.schema.json`
- `docs/schemas/skills-catalog.schema.json`
3. 若 skill 支持 MCP + setup，确保 catalog 输出 `setupCommands.ironclaw`、`clientSupport.ironclaw`、`distributionSources` 与 `clientInstall`。
4. 在 `workspace.json` 增加新路径，使用 `${SKILLS_BASE}` 占位。
5. 如存在依赖，补充直接依赖 `dependsOn`。
6. 按顺序执行门禁：
```bash
bun run catalog:generate
bun run health:check
bun run readme:check
bun run security:audit
./bootstrap.sh --only <skill-id> --skip-install
```
7. 按契约固定 6 段格式整理 PR 描述。

成功标准：
1. catalog 成功生成且 schema 为 `1.3.0`。
2. `health/readme/security/bootstrap` 门禁全部通过。
3. PR 描述包含 Goal/Non-goal、关键文件、契约映射、验证输出、风险与回滚。

补充安装规则：
1. GitHub repo URL 只用于 discovery。
2. OpenClaw/IronClaw 执行时，优先读取 `clientInstall.*.installCommand`。

## 常见错误恢复模板

1. 依赖下载失败
- 动作：`./bootstrap.sh --source github --only <skill-id>`

2. 未找到 skill-id
- 动作：`bun run catalog:generate` 后重试 `--only`

3. 健康检查失败
- 动作：按 `health:check` 报错补齐对应产物（setup/mcp/openclaw）
