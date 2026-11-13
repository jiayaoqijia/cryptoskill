<!--
  Imported from: https://github.com/lingfan/tdxquant-mcp
  Source Path: skills/tdxquant-mcp/SKILL.md
  Curated for awesome-quant-skills
-->

---
name: tdxquant-mcp-sse
description: >
  当用户需要 A 股行情、K 线/Tick、财务、板块、通达信公式、可转债/新股、交易日历或交易查询，
  且通过本仓库的 MCP **HTTP/SSE** 服务（FastMCP，`/sse`）接入时使用。要求本机已配置 TQ_PATH、
  通达信/TdxQuant 可用，并已启动 `tdx_mcp.main_http`。先 tools_catalog，再按需调用具体工具；
  平台背景可 docs_get_tdxquant_intro。交易类工具默认 dry-run，勿替用户关闭。
---

# TdxQuant MCP（SSE）技能

## 何时使用

- 用户要查 **K 线、Tick、快照、板块成分、财务、公式、交易日历、可转债/新股** 等，并声明或隐含使用 **本项目的 MCP 服务**。
- 宿主已通过 **SSE** 连接到运行中的 `tdx_mcp.main_http`（不是 stdio 子进程场景时，仍适用同一套工具名与工作流）。

## 硬前提（调用任何业务工具前）

1. **通达信 / TdxQuant 终端**已按官方要求可用（登录、数据下载等由用户侧保证）。
2. 环境变量 **`TQ_PATH`** 已设置，否则服务进程无法启动。
3. **HTTP/SSE 服务已启动**（示例）：
   - `uv sync --extra http`
   - `uv run python -m tdx_mcp.main_http`
4. 客户端配置的 **SSE URL** 须指向 FastMCP 默认路径：**`http://<MCP_HOST>:<MCP_PORT>/sse`**（默认常为 `http://127.0.0.1:8765/sse`，以 `.env` 为准）。

若连接失败，核对：进程是否存活、防火墙、URL 是否包含 **`/sse`** 后缀。

## 推荐调用顺序

1. **`tools_catalog`**（无参数）— 获取当前服务注册的分类与工具**精确名称**（下划线风格，如 `market_get_kline`，禁止写成 `market.get_kline`）。
2. 需要向用户说明 **TdxQuant 是什么、运行环境、tqcenter 能力** 时：**`docs_get_tdxquant_intro`**（无参数），以返回的 `content` 为准。
3. 按任务调用具体工具；参数细节以工具 schema 与仓库内 `docs/agent-usage.md` 为准。

更细的「意图 → 工具」表见同目录 [`references/workflow.md`](references/workflow.md)。

## 证券代码

- 沪深示例：`600519.SH`、`000001.SZ`（**市场后缀大写**）。

## 安全与合规

- **`trade_order_stock` / `trade_cancel_order_stock`** 等：默认 **`dry_run=true`**，仅预览；**仅在用户明确授权且理解风险时**才可使用 `dry_run=false`，不得默认替用户关闭。
- **Hermes** 等宿主：建议对 MCP 工具做 **`include` 白名单**，缩小暴露面；见 [Hermes：Use MCP with Hermes](https://hermes-agent.nousresearch.com/docs/guides/use-mcp-with-hermes)。
- **禁止**在缺少工具返回时编造行情或财务数字；空结果应提示检查终端、数据下载与代码格式。

## 各宿主 MCP 配置片段

可复制示例见 [`references/host-config-snippets.md`](references/host-config-snippets.md)（Claude Code、OpenClaw、Hermes）。

## 仓库文档（人类与 Agent 共读）

| 文档 | 内容 |
|------|------|
| `docs/mcp-configuration.md` | stdio / HTTP、环境变量、排错 |
| `docs/agent-usage.md` | 完整工作流、意图表、交易说明 |
| `docs/tdxquant-intro.md` | 平台简介索引与 `docs_get_tdxquant_intro` |

## 协议说明

当前 `main_http` 使用 **SSE**（非 `streamable-http`）。若未来服务端改为 Streamable HTTP，需同步更新客户端 `transport` / URL（以 OpenClaw / Claude Code 文档为准）。
