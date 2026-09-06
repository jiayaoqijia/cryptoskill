---
name: polyhub_copy
description: Manage copy-trading tasks, view signals, positions and trades on Polyhub using an API key.
---

# Polyhub Copy Skill

Version: v0.3.9

## When to use

Use this skill when the user asks about:

- Listing, creating, updating or deleting copy-trading tasks
- Viewing copy task positions or trades
- Selling positions (single or all)
- Batch updating or deleting copy tasks
- Viewing total PnL across copy tasks
- Viewing copy signals and signal stats
- Managing take-profit / stop-loss (TPSL) rules

## Requirements

- `POLYHUB_API_BASE_URL` is fixed to `https://polyhub.skill-test.bedev.hubble-rpc.xyz`.
- `POLYHUB_API_KEY` — API key (must start with `phub_`)
- `curl` must be available in the runtime environment.
- `jq` is strongly recommended for building JSON payloads safely.

If `POLYHUB_API_KEY` is missing, guide the user to register and apply for one first at `https://polyhub.hubble.xyz/`.
Recommended guidance:

1. Open Polyhub Web: `https://polyhub.hubble.xyz/`
2. Click the avatar menu.
3. Open `Skills API Key`.
4. Click `申请 API Key`.
5. Set both `POLYHUB_API_BASE_URL` and `POLYHUB_API_KEY`.

Suggested wording:

```text
API key is not configured yet, so I can't run copy-trading or account actions for now.

Please register first on PolyHub:
https://polyhub.hubble.xyz/

After registration, click your avatar in the top-right corner and open `Skills API Key` to apply.

Send me the generated key and I'll continue right away.
```

## Safety rules

- Never print `POLYHUB_API_KEY` in the output.
- Treat all IDs and user-provided JSON fields as untrusted input.
- For write actions (`POST`/`PATCH`/`DELETE`), repeat the action summary and wait for explicit user confirmation before calling the API.
- Prefer building JSON with `jq -n` instead of interpolating raw shell strings.
- Validation rules:
  - `taskId` must be a 24-char hex MongoDB ObjectID: `^[0-9a-fA-F]{24}$`
  - `ruleId` must be non-empty.
  - `taskIds` in batch operations must all match the `taskId` format.
  - `status` for positions should only be passed when the user explicitly requests a filter.

## Tools

Use the `bash` tool to call the API with `curl`.

## Fast Path

For common intents, map user requests like this:

- “列出任务” -> `GET /api/v1/copy-tasks`
- “删除任务” -> 先 `GET /api/v1/copy-tasks/{taskId}/positions?status=active`，有 active positions 时先 `POST /api/v1/copy-tasks/{taskId}/sell-all`，再 `DELETE /api/v1/copy-tasks/{taskId}`
- “暂停/恢复/停止任务” -> `PATCH /api/v1/copy-tasks/{taskId}` with `status`
- “改跟单模式/改单笔或总仓位限制” -> `PATCH /api/v1/copy-tasks/{taskId}` with `taskConfig`
- “看持仓/成交” -> `GET /positions` or `GET /trades`
- “卖出某个仓位/全部仓位” -> `POST /sell` or `POST /sell-all`
- “看跟单信号/统计” -> `GET /api/v1/copy-signals` or `/stats`

### Curl base setup

```bash
BASE="https://polyhub.skill-test.bedev.hubble-rpc.xyz"
AUTH=(-H "Authorization: Bearer $POLYHUB_API_KEY" -H "Content-Type: application/json")
```

### Validate helpers

```bash
if [[ ! "$TASK_ID" =~ ^[0-9a-fA-F]{24}$ ]]; then echo "Invalid taskId"; exit 2; fi
```

```bash
if [[ -z "${RULE_ID:-}" ]]; then echo "Invalid ruleId"; exit 2; fi
```

```bash
for id in "${TASK_IDS[@]}"; do
  if [[ ! "$id" =~ ^[0-9a-fA-F]{24}$ ]]; then
    echo "Invalid taskId in batch: $id"
    exit 2
  fi
done
```

---

## Copy Tasks

### Action: List copy tasks

- `GET /api/v1/copy-tasks`
- Query params: `includeDeleted=true|false` (default: true)

```bash
curl -sS --fail-with-body "${AUTH[@]}" "$BASE/api/v1/copy-tasks?includeDeleted=true"
```

Guidance:

- Use `includeDeleted=true` when the user wants a full history or is looking for a previously deleted task.
- Use `includeDeleted=false` when the user only wants active/non-deleted tasks.

### Action: Create copy task

- `POST /api/v1/copy-tasks`
- Required field: `targetTrader` (Polymarket address of the smart money)
- Optional fields from `domain.CreateCopyTaskPayload`: `targetUsername`, `taskConfig`, `filteredByTag`, `tpslRules`

Before calling: ask the user for `targetTrader` at minimum. Summarize and confirm.

Minimum fields to ask:

- Always ask: `targetTrader`
- Ask only if needed: `filteredByTag`, `targetUsername`
- If the user wants custom copy behavior: ask for the relevant `taskConfig` fields explicitly
- If the user wants TPSL on creation: ask for `tpslRules`

```bash
PAYLOAD="$(jq -n \
  --arg targetTrader "0x..." \
  '{targetTrader: $targetTrader}')"

curl -sS --fail-with-body "${AUTH[@]}" -X POST "$BASE/api/v1/copy-tasks" \
  -d "$PAYLOAD"
```

If the user wants advanced config, build `taskConfig` and `tpslRules` explicitly instead of accepting arbitrary JSON.

### Pre-flight: Balance Check

Before creating a copy task, check if the user has sufficient balance:

```bash
curl -sS --fail-with-body "${AUTH[@]}" "$BASE/api/v1/portfolio/stats"
```

Check `availableBalance` from the response:
- If `availableBalance >= 100`: proceed with task creation
- If `availableBalance < 100`: show deposit guidance (see below)
- If `availableBalance < 10`: strongly recommend depositing before creating any tasks

### Deposit Guidance

Depositing is **not supported via skill or API**. Always direct the user to the web UI.

When balance is insufficient, present this message:

```
当前可用余额: $XX

建议至少 $100 才能有效跟单。充值只能通过网页端操作：
👉 https://polyhub.hubble.xyz/copy-history?action=deposit
（打开后会自动弹出充值窗口）
充值完成后回来告诉我，我帮你继续创建跟单任务。
```

### Quick Copy from Discover

When the user comes from a discover flow (already has a target address and optionally a tag), use this streamlined creation:

1. Run balance check (see Pre-flight above)
2. Confirm with user: "要跟单 {address} 吗？标签: {tag or '全部市场'}"
3. Create task:

```bash
PAYLOAD="$(jq -n \
  --arg targetTrader "0x..." \
  --arg filteredByTag "Sports" \
  '{targetTrader: $targetTrader, filteredByTag: $filteredByTag}')"

curl -sS --fail-with-body "${AUTH[@]}" -X POST "$BASE/api/v1/copy-tasks" \
  -d "$PAYLOAD"
```

If `filteredByTag` is not specified (user wants all markets), omit it:

```bash
PAYLOAD="$(jq -n \
  --arg targetTrader "0x..." \
  '{targetTrader: $targetTrader}')"
```

After successful creation, show:
```
✅ 跟单任务已创建
📊 查看任务: https://polyhub.hubble.xyz/copy-history
```

### Action: Get copy task

- `GET /api/v1/copy-tasks/{taskId}`

```bash
curl -sS --fail-with-body "${AUTH[@]}" "$BASE/api/v1/copy-tasks/$TASK_ID"
```

### Action: Update copy task

- `PATCH /api/v1/copy-tasks/{taskId}`
- Body: partial JSON. Common fields:
  - `status`
  - `taskConfig`
  - `filteredByTag`
  - `targetUsername`
  - `tpslRules` using `create` / `update` / `cancel`

Before calling: validate `taskId`, summarize changes, and confirm.

Minimum fields to ask:

- Always ask: `taskId`
- Ask only the fields the user wants to change:
  - Task lifecycle: `status`
  - Copy behavior: `taskConfig`
  - Trader label/tag filters: `targetUsername`, `filteredByTag`
  - TPSL maintenance: `tpslRules`

```bash
PAYLOAD="$(jq -n \
  --arg status "PAUSED" \
  '{status: $status}')"

curl -sS --fail-with-body "${AUTH[@]}" -X PATCH "$BASE/api/v1/copy-tasks/$TASK_ID" \
  -d "$PAYLOAD"
```

Example: update `taskConfig` safely

```bash
PAYLOAD="$(jq -n \
  --argjson buyOnly true \
  --argjson maxBoughtPerMarket 50 \
  '{taskConfig: {buyOnly: $buyOnly, maxBoughtPerMarket: $maxBoughtPerMarket}}')"
```

Example: change copy mode to `ONE_TO_ONE`

```bash
PAYLOAD="$(jq -n \
  '{taskConfig: {copyMode: "ONE_TO_ONE"}}')"

curl -sS --fail-with-body "${AUTH[@]}" -X PATCH "$BASE/api/v1/copy-tasks/$TASK_ID" \
  -d "$PAYLOAD"
```

Example: change copy mode to `FIXED_SIZE`

`FIXED_SIZE` should include `taskConfig.fixedAmount`.

```bash
PAYLOAD="$(jq -n \
  --argjson fixedAmount 5 \
  '{taskConfig: {copyMode: "FIXED_SIZE", fixedAmount: $fixedAmount}}')"

curl -sS --fail-with-body "${AUTH[@]}" -X PATCH "$BASE/api/v1/copy-tasks/$TASK_ID" \
  -d "$PAYLOAD"
```

Copy mode guidance:

- `taskConfig.copyMode` is the field that controls the task's copy mode.
- Confirmed mode values in the current codebase: `ONE_TO_ONE`, `FIXED_SIZE`.
- If switching to `FIXED_SIZE`, also ask for `taskConfig.fixedAmount`.
- If switching to `ONE_TO_ONE`, omit `fixedAmount` unless the user explicitly wants to keep it stored.

### TaskConfig field guidance

Use these fields when the user wants to change task-level copy behavior. Prefer changing only the fields the user explicitly asked for.

Common fields:

- `taskConfig.copyMode`
  - Controls copy sizing mode.
  - Confirmed values: `ONE_TO_ONE`, `FIXED_SIZE`.
- `taskConfig.fixedAmount`
  - Used when `copyMode=FIXED_SIZE`.
  - Represents a fixed notional amount for copied orders.
- `taskConfig.navMultiplier`
  - Multiplies the computed order size.
  - Current default in backend user config is `1`.
- `taskConfig.positionUtilization`
  - Position utilization / max amount per copy-trade style control.
  - Backend default is `0`, which means no filter.
- `taskConfig.buyOnly`
  - If `true`, non-`BUY` signals are skipped.
- `taskConfig.buyLimitPerTradeMin`
  - Minimum allowed copied buy amount per trade.
  - `0` effectively means no lower bound.
- `taskConfig.buyLimitPerTradeMax`
  - Maximum allowed copied buy amount per trade.
  - `0` effectively means no upper bound.
- `taskConfig.maxBoughtPerCopyTask`
  - Caps total bought amount at task level.
  - `0` effectively means no cap.
- `taskConfig.maxBoughtPerMarket`
  - Caps total bought amount for a single market inside the task.
  - `0` effectively means no cap.
- `taskConfig.priceRangeMin`
  - Minimum allowed execution price.
  - Default from user config is typically `0.01`.
- `taskConfig.priceRangeMax`
  - Maximum allowed execution price.
  - Default from user config is typically `0.99`.
- `taskConfig.minLiquidity`
  - Minimum market liquidity filter.
  - `0` effectively means no filter.
- `taskConfig.minFillSize`
  - Minimum fill shares filter.
  - `0` effectively means no filter.
- `taskConfig.maxPriceDeviation`
  - Maximum allowed price deviation percentage.
- `taskConfig.expiryHours`
  - Order expiry configuration for copied orders.
  - Backend default from user config is typically `0`.
- `taskConfig.convictionLevel`
  - Conviction-based filter level.
  - Confirmed values: `OFF`, `LOOSE`, `STANDARD`, `STRICT`.
  - Backend default is `STANDARD`.

Recommended clarification rules before updating:

- If the user says “改成固定金额跟单”, ask for `fixedAmount`.
- If the user says “放大/缩小仓位”, clarify whether they mean `navMultiplier` or `fixedAmount`.
- If the user says “限制单笔金额”, clarify whether they mean `buyLimitPerTradeMin`, `buyLimitPerTradeMax`, or both.
- If the user says “限制总仓位”, clarify whether they mean `maxBoughtPerCopyTask` or `maxBoughtPerMarket`.
- If the user says “限制价格区间”, ask for both `priceRangeMin` and `priceRangeMax`.
- If the user says “调严格一点/调宽松一点”, clarify whether they mean `convictionLevel`.
- If the user says “恢复跟单/暂停跟单/停止任务”, clarify whether they mean task `status` or a `taskConfig` change.

Example: update `navMultiplier`

```bash
PAYLOAD="$(jq -n \
  --argjson navMultiplier 1.5 \
  '{taskConfig: {navMultiplier: $navMultiplier}}')"
```

Example: enable buy-only mode

```bash
PAYLOAD="$(jq -n \
  --argjson buyOnly true \
  '{taskConfig: {buyOnly: $buyOnly}}')"
```

Example: limit per-trade buy amount

```bash
PAYLOAD="$(jq -n \
  --argjson min 2 \
  --argjson max 10 \
  '{taskConfig: {buyLimitPerTradeMin: $min, buyLimitPerTradeMax: $max}}')"
```

Example: limit total bought amount

```bash
PAYLOAD="$(jq -n \
  --argjson maxBoughtPerCopyTask 100 \
  --argjson maxBoughtPerMarket 25 \
  '{taskConfig: {maxBoughtPerCopyTask: $maxBoughtPerCopyTask, maxBoughtPerMarket: $maxBoughtPerMarket}}')"
```

Example: restrict execution price range

```bash
PAYLOAD="$(jq -n \
  --argjson min 0.1 \
  --argjson max 0.9 \
  '{taskConfig: {priceRangeMin: $min, priceRangeMax: $max}}')"
```

Example: combine multiple taskConfig changes

```bash
PAYLOAD="$(jq -n \
  --argjson buyOnly true \
  --argjson navMultiplier 1.2 \
  --argjson maxBoughtPerMarket 20 \
  '{
    taskConfig: {
      buyOnly: $buyOnly,
      navMultiplier: $navMultiplier,
      maxBoughtPerMarket: $maxBoughtPerMarket
    }
  }')"

curl -sS --fail-with-body "${AUTH[@]}" -X PATCH "$BASE/api/v1/copy-tasks/$TASK_ID" \
  -d "$PAYLOAD"
```

Example: update `convictionLevel`

```bash
PAYLOAD="$(jq -n \
  --arg convictionLevel "STRICT" \
  '{taskConfig: {convictionLevel: $convictionLevel}}')"

curl -sS --fail-with-body "${AUTH[@]}" -X PATCH "$BASE/api/v1/copy-tasks/$TASK_ID" \
  -d "$PAYLOAD"
```

Conviction level guidance:

- `OFF`: disable conviction filter.
- `LOOSE`: lower threshold, more signals can pass.
- `STANDARD`: default mode.
- `STRICT`: higher threshold, fewer signals can pass.
- If the user gives an unknown value, normalize to one of the four explicit options before calling the API.

Example: update `taskConfig` and `status` together

```bash
PAYLOAD="$(jq -n \
  --arg status "RUNNING" \
  --argjson buyOnly true \
  '{
    status: $status,
    taskConfig: {
      buyOnly: $buyOnly
    }
  }')"

curl -sS --fail-with-body "${AUTH[@]}" -X PATCH "$BASE/api/v1/copy-tasks/$TASK_ID" \
  -d "$PAYLOAD"
```

Example: update TPSL rules safely

```bash
PAYLOAD="$(jq -n \
  --arg ruleId "$RULE_ID" \
  --argjson takeProfitPct 20 \
  '{tpslRules: {update: [{id: $ruleId, takeProfitPct: $takeProfitPct}]}}')"
```

Example: update task status

```bash
PAYLOAD="$(jq -n \
  --arg status "PAUSED" \
  '{status: $status}')"

curl -sS --fail-with-body "${AUTH[@]}" -X PATCH "$BASE/api/v1/copy-tasks/$TASK_ID" \
  -d "$PAYLOAD"
```

Status guidance:

- Valid task `status` values for update are: `RUNNING`, `PAUSED`, `STOPPED`.
- Use `PAUSED` when the user wants to temporarily stop following new trades.
- Use `RUNNING` when the user wants to resume an active task.
- Use `STOPPED` only when the user explicitly wants the task stopped rather than just paused.
- Do not use `DELETED` in update payloads; deletion should use `DELETE /api/v1/copy-tasks/{taskId}`.
- Prefer uppercase status values in payloads.

### Action: Delete copy task

- `DELETE /api/v1/copy-tasks/{taskId}`

Required flow before delete:

1. Validate `taskId`.
2. Check active positions with `GET /api/v1/copy-tasks/{taskId}/positions?status=active`.
3. If any active positions exist, restate that deleting the task will first clear those positions, then delete the task.
4. After explicit confirmation, call `POST /api/v1/copy-tasks/{taskId}/sell-all`.
5. Only after the position cleanup step finishes, call `DELETE /api/v1/copy-tasks/{taskId}`.

Before calling: validate `taskId` and confirm the full sequence.

Minimum fields to ask:

- Always ask: `taskId`

Pre-check active positions:

```bash
curl -sS --fail-with-body "${AUTH[@]}" "$BASE/api/v1/copy-tasks/$TASK_ID/positions?status=active"
```

If active positions exist, clear them first:

```bash
curl -sS --fail-with-body "${AUTH[@]}" -X POST "$BASE/api/v1/copy-tasks/$TASK_ID/sell-all"
```

Then delete the task:

```bash
curl -sS --fail-with-body "${AUTH[@]}" -X DELETE "$BASE/api/v1/copy-tasks/$TASK_ID"
```

Guidance:

- There is no dedicated API to delete positions directly; use `sell-all` as the required position cleanup step.
- If no active positions are returned, delete the task directly after confirmation.
- If `sell-all` partially skips positions, report the skipped reasons, but continue with task deletion unless the user explicitly wants to stop.

### Action: Get total PnL

- `GET /api/v1/copy-tasks/total-pnl`

```bash
curl -sS --fail-with-body "${AUTH[@]}" "$BASE/api/v1/copy-tasks/total-pnl"
```

---

## Positions & Trades

### Action: List positions

- `GET /api/v1/copy-tasks/{taskId}/positions`
- Query params: `status` (optional)
  - Confirmed values in current code: `active`, `closed`

```bash
curl -sS --fail-with-body "${AUTH[@]}" "$BASE/api/v1/copy-tasks/$TASK_ID/positions?status=active"
```

Guidance:

- `active` returns positions with remaining amount above the close threshold.
- `closed` returns positions whose remaining amount is effectively zero.
- If `status` is omitted or unknown, the backend currently returns all positions.
- Prefer `active` / `closed` rather than `open` / `closed`.

### Action: List trades

- `GET /api/v1/copy-tasks/{taskId}/trades`

```bash
curl -sS --fail-with-body "${AUTH[@]}" "$BASE/api/v1/copy-tasks/$TASK_ID/trades"
```

### Action: Sell position

- `POST /api/v1/copy-tasks/{taskId}/sell`
- Required field: `marketId` (preferred) or `conditionId`
- Optional field: `amount` (partial sell; omit to sell full position)

Before calling: validate `taskId`, summarize (which market, amount), and confirm.

Minimum fields to ask:

- Always ask: `taskId`
- Always ask one of: `marketId` or `conditionId`
- Ask `amount` only when the user wants a partial sell

```bash
PAYLOAD="$(jq -n \
  --arg marketId "..." \
  --argjson amount 10 \
  '{marketId: $marketId, amount: $amount}')"

curl -sS --fail-with-body "${AUTH[@]}" -X POST "$BASE/api/v1/copy-tasks/$TASK_ID/sell" \
  -d "$PAYLOAD"
```

### Action: Sell all positions

- `POST /api/v1/copy-tasks/{taskId}/sell-all`

Before calling: validate `taskId` and confirm — this sells ALL positions for the task.

Minimum fields to ask:

- Always ask: `taskId`

```bash
curl -sS --fail-with-body "${AUTH[@]}" -X POST "$BASE/api/v1/copy-tasks/$TASK_ID/sell-all"
```

---

## Batch Operations

### Action: Batch update tasks

- `POST /api/v1/copy-tasks/batch-update`
- Required: `taskIds` (array of task IDs)
- Optional: `status` (string), `taskConfig` (object)

Before calling: summarize which tasks and what changes, and confirm.

Minimum fields to ask:

- Always ask: `taskIds`
- Ask at least one of: `status`, `taskConfig`

```bash
TASK_IDS=("64f0c7e7b8e4f8c1a1b2c3d4" "64f0c7e7b8e4f8c1a1b2c3d5")
PAYLOAD="$(jq -n \
  --arg status "PAUSED" \
  --argjson taskIds "$(printf '%s\n' "${TASK_IDS[@]}" | jq -R . | jq -s .)" \
  '{taskIds: $taskIds, status: $status}')"

curl -sS --fail-with-body "${AUTH[@]}" -X POST "$BASE/api/v1/copy-tasks/batch-update" \
  -d "$PAYLOAD"
```

Example: batch update `taskConfig.copyMode`

```bash
TASK_IDS=("64f0c7e7b8e4f8c1a1b2c3d4" "64f0c7e7b8e4f8c1a1b2c3d5")
PAYLOAD="$(jq -n \
  --argjson taskIds "$(printf '%s\n' "${TASK_IDS[@]}" | jq -R . | jq -s .)" \
  '{
    taskIds: $taskIds,
    taskConfig: {
      copyMode: "ONE_TO_ONE"
    }
  }')"

curl -sS --fail-with-body "${AUTH[@]}" -X POST "$BASE/api/v1/copy-tasks/batch-update" \
  -d "$PAYLOAD"
```

Batch update guidance:

- `status` uses the same allowed values as single-task update: `RUNNING`, `PAUSED`, `STOPPED`.
- `taskConfig` replaces the task config object sent in the batch request, so only send fields you intentionally want to set.
- If neither `status` nor `taskConfig` is provided, the backend currently just returns the selected tasks.
- Use batch update only when the same change should apply to all listed tasks.

### Action: Batch delete tasks

- `POST /api/v1/copy-tasks/batch-delete`
- Required: `taskIds` (array of task IDs)

Required flow before batch delete:

1. Validate all `taskIds`.
2. For each task, check `GET /api/v1/copy-tasks/{taskId}/positions?status=active`.
3. If a task has active positions, include it in the confirmation summary and state that those positions will be cleared before deletion.
4. After explicit confirmation, run `POST /api/v1/copy-tasks/{taskId}/sell-all` for each task that still has active positions.
5. After the position cleanup passes finish, call batch delete once with all `taskIds`.

Before calling: confirm the full cleanup-then-delete operation.

Minimum fields to ask:

- Always ask: `taskIds`

Example: pre-check one task's active positions

```bash
curl -sS --fail-with-body "${AUTH[@]}" "$BASE/api/v1/copy-tasks/$TASK_ID/positions?status=active"
```

Example: clear positions for one task before batch delete

```bash
curl -sS --fail-with-body "${AUTH[@]}" -X POST "$BASE/api/v1/copy-tasks/$TASK_ID/sell-all"
```

```bash
TASK_IDS=("64f0c7e7b8e4f8c1a1b2c3d4" "64f0c7e7b8e4f8c1a1b2c3d5")
PAYLOAD="$(jq -n \
  --argjson taskIds "$(printf '%s\n' "${TASK_IDS[@]}" | jq -R . | jq -s .)" \
  '{taskIds: $taskIds}')"

curl -sS --fail-with-body "${AUTH[@]}" -X POST "$BASE/api/v1/copy-tasks/batch-delete" \
  -d "$PAYLOAD"
```

Guidance:

- There is no batch position-delete endpoint; clean positions task by task with `sell-all`, then call `batch-delete`.
- If some `sell-all` calls skip positions, report that in the confirmation/result summary and continue unless the user explicitly asks to stop.

---

## Copy Signals

### Action: List copy signals

- `GET /api/v1/copy-signals`
- Query params:
  - `limit` (int, default 50)
  - `cursor` (int, offset for pagination)
  - `since` (RFC3339 timestamp)
  - `sinceCreatedAt` (RFC3339 timestamp)
  - `action` (one of: `COPIED`, `SKIPPED`, `FAILED`, `RECEIVED`)
  - `trader` (address filter)

```bash
curl -sS --fail-with-body "${AUTH[@]}" "$BASE/api/v1/copy-signals?limit=20&action=COPIED"
```

Prefer composing the query from user intent. Only pass filters the user asked for.

Validation:

- `limit` must be a positive integer.
- `cursor` must be a non-negative integer.
- `since` and `sinceCreatedAt` must be RFC3339 or RFC3339Nano timestamps.
- Valid `action` values are: `COPIED`, `SKIPPED`, `FAILED`, `RECEIVED`.

Action guidance:

- `RECEIVED`: the signal was ingested.
- `COPIED`: the copy order was placed successfully.
- `SKIPPED`: the signal was intentionally not copied because checks or limits blocked it.
- `FAILED`: the system attempted processing but failed.

Example: fetch signals since a specific time

```bash
curl -sS --fail-with-body "${AUTH[@]}" \
  "$BASE/api/v1/copy-signals?since=2026-03-01T00:00:00Z&limit=50"
```

Example: fetch next page using cursor

```bash
curl -sS --fail-with-body "${AUTH[@]}" \
  "$BASE/api/v1/copy-signals?cursor=50&limit=50"
```

### Action: Stream copy signals

- `GET /api/v1/copy-signals/stream`
- Response type: Server-Sent Events (SSE)

```bash
curl -sS -N "${AUTH[@]}" "$BASE/api/v1/copy-signals/stream"
```

Stream guidance:

- Use this only when the user explicitly wants real-time signal updates.
- Expect events such as `ready` and `copy_signal`.
- Keep the connection open; this is not a one-shot request.

### Action: Get signal stats

- `GET /api/v1/copy-signals/stats`

Returns signal counts grouped by action and by trader.

```bash
curl -sS --fail-with-body "${AUTH[@]}" "$BASE/api/v1/copy-signals/stats"
```

---

## TPSL Rules (Take-Profit / Stop-Loss)

### Action: Get TPSL rule

- `GET /api/v1/copy-tasks/{taskId}/tpsl-rules/{ruleId}`

Minimum fields to ask:

- Always ask: `taskId`, `ruleId`

```bash
curl -sS --fail-with-body "${AUTH[@]}" "$BASE/api/v1/copy-tasks/$TASK_ID/tpsl-rules/$RULE_ID"
```

### Action: Simulate TPSL rule

- `POST /api/v1/copy-tasks/{taskId}/tpsl-rules/{ruleId}/simulate`

Minimum fields to ask:

- Always ask: `taskId`, `ruleId`

```bash
curl -sS --fail-with-body "${AUTH[@]}" -X POST "$BASE/api/v1/copy-tasks/$TASK_ID/tpsl-rules/$RULE_ID/simulate"
```

### TPSL inline payload guidance

When creating a task, `tpslRules` items may include:

- `sourceOrderId`, `sourceType`
- Optional entry info: `conditionId`, `tokenId`, `assetId`, `entryPrice`, `entrySize`, `side`
- Optional risk config: `takeProfitPct`, `takeProfitProb`, `stopLossPct`, `limitPriceOffset`, `orderTimeout`, `fallbackToMarket`

When updating a task, `tpslRules` should be wrapped as:

- `create`: array of new inline rules
- `update`: array of `{id, ...patchFields}`
- `cancel`: array of `ruleId`

Example: create a task with one TPSL rule

```bash
PAYLOAD="$(jq -n \
  --arg targetTrader "0x..." \
  --arg sourceOrderId "order_123" \
  --arg sourceType "copy_trade" \
  --argjson takeProfitPct 20 \
  --argjson stopLossPct 10 \
  '{
    targetTrader: $targetTrader,
    tpslRules: [
      {
        sourceOrderId: $sourceOrderId,
        sourceType: $sourceType,
        takeProfitPct: $takeProfitPct,
        stopLossPct: $stopLossPct
      }
    ]
  }')"
```

---

## Error handling

- `401`: API key missing/invalid/expired/disabled. Ask user to check or regenerate key.
- `404`: Task or resource not found. Ask user to verify `taskId`.
- `409`: Task already exists (duplicate `targetTrader`).
- `422`: Copy task limit exceeded.
- `400`: Invalid payload or invalid query param such as `includeDeleted`.
- `5xx`: Server error. Retry once with backoff; if still failing, report response body.
