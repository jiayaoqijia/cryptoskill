# Type Safety 矩阵

最后更新：2026-03-04

## 范围
- 纳入仓库（6）：`eoa-agent-skills`、`portkey-agent-skills`、`awaken-agent-skills`、`eforest-agent-skills`、`tomorrowDAO-skill`、`aelf-node-skill`
- 排除仓库：`agent-skills-e2e`

## 统一基线
- `package.json` 脚本统一：
  - `typecheck:src`
  - `typecheck:test`
  - `typecheck`
- TypeScript 配置分层统一：
  - `tsconfig.base.json`
  - `tsconfig.src.json`
  - `tsconfig.test.json`
- 类型白名单统一：`bun-types` + `node`
- 第三方声明补丁策略统一：
  - 显式补齐 `aelf-sdk` 与 `aelf-sdk/src/util/keyStore.js` 声明

## CI 落地策略
- `test.yml` 新增 `typecheck` 步骤，当前为**观察模式**：
  - `continue-on-error: true`
- 现有质量门禁保持不变：
  - `deps:check`
  - `build:openclaw:check`
  - `test:coverage:ci`

## 仓库状态
| Repo | `typecheck:src` | `typecheck:test` | `typecheck` |
|---|---|---|---|
| eoa-agent-skills | Pass | Pass | Pass |
| portkey-agent-skills | Pass | Pass | Pass |
| awaken-agent-skills | Pass | Pass | Pass |
| eforest-agent-skills | Pass | Pass | Pass |
| tomorrowDAO-skill | Pass | Pass | Pass |
| aelf-node-skill | Pass | Pass | Pass |

## 债务追踪
- 执行命令：`bun run type-debt:report`
- 输出文件：
  - `docs/type-safety/type-debt-latest.json`
  - `docs/type-safety/type-debt-history.json`
