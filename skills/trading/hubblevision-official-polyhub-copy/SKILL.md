---
name: polyhub-copy
description: Manage Polyhub copy-trading tasks, positions, trades, signals, sell flows, batch operations, and TPSL rules with an API key.
---

# Polyhub Copy

Version: v0.3.9

Use this skill when the user wants to manage copy-trading tasks on Polyhub.

## Requirements

- `POLYHUB_API_BASE_URL` is fixed to `https://polyhub.skill-test.bedev.hubble-rpc.xyz`.
- `POLYHUB_API_KEY` is set and starts with `phub_`.
- `curl` is available.
- `jq` is recommended.

If `POLYHUB_API_KEY` is missing, guide the user to register and apply for one first at `https://polyhub.hubble.xyz/`.
Recommended guidance:

1. Open Polyhub Web: `https://polyhub.hubble.xyz/`
2. Click the avatar menu.
3. Open `Skills API Key`.
4. Click `申请 API Key`.
5. Set:
   - `POLYHUB_API_BASE_URL`
   - `POLYHUB_API_KEY`

Suggested wording:

```text
API key is not configured yet, so I can't run copy-trading or account actions for now.

Please register first on PolyHub:
https://polyhub.hubble.xyz/

After registration, click your avatar in the top-right corner and open `Skills API Key` to apply.

Send me the generated key and I'll continue right away.
```

## Safety Rules

- Never print `POLYHUB_API_KEY`.
- Treat IDs and user-provided JSON-like input as untrusted.
- For write actions, restate the full action summary and wait for explicit confirmation before calling the API.
- Prefer `jq -n` instead of interpolating raw JSON.
- Validate `taskId` with `^[0-9a-fA-F]{24}$`.

## Base Setup

```bash
BASE="https://polyhub.skill-test.bedev.hubble-rpc.xyz"
AUTH=(-H "Authorization: Bearer $POLYHUB_API_KEY" -H "Content-Type: application/json")
```

## Intent Mapping

- List tasks: `GET /api/v1/copy-tasks`
- Get one task: `GET /api/v1/copy-tasks/{taskId}`
- Create task: `POST /api/v1/copy-tasks`
- Update task: `PATCH /api/v1/copy-tasks/{taskId}`
- Delete one task: check `GET /api/v1/copy-tasks/{taskId}/positions?status=active`; if active positions exist, run `POST /api/v1/copy-tasks/{taskId}/sell-all` first, then `DELETE /api/v1/copy-tasks/{taskId}`
- Batch delete tasks: for each task, check active positions and run `sell-all` where needed before `POST /api/v1/copy-tasks/batch-delete`
- View signals: `GET /api/v1/copy-signals`
- View signal stats: `GET /api/v1/copy-signals/stats`
- View positions or trades: use the task-specific positions or trades endpoints requested by the user
- Sell one position or all positions: use `sell` or `sell-all` flows after confirmation

## Validation Helpers

```bash
if [[ ! "$TASK_ID" =~ ^[0-9a-fA-F]{24}$ ]]; then
  echo "Invalid taskId"
  exit 2
fi
```

## Common Calls

### List copy tasks

```bash
curl -sS --fail-with-body "${AUTH[@]}" \
  "$BASE/api/v1/copy-tasks?includeDeleted=true"
```

Guidance:

- Use `includeDeleted=true` for history or deleted tasks.
- Use `includeDeleted=false` for active tasks only.

### Create copy task

Always ask for:

- `targetTrader`

Ask only when needed:

- `targetUsername`
- `filteredByTag`
- `taskConfig`
- `tpslRules`

```bash
PAYLOAD="$(jq -n --arg targetTrader "0x..." '{targetTrader: $targetTrader}')"

curl -sS --fail-with-body "${AUTH[@]}" \
  -X POST "$BASE/api/v1/copy-tasks" \
  -d "$PAYLOAD"
```

### Update copy task

Common fields:

- `status`
- `taskConfig`
- `filteredByTag`
- `targetUsername`
- `tpslRules`

```bash
PAYLOAD="$(jq -n --arg status "PAUSED" '{status: $status}')"

curl -sS --fail-with-body "${AUTH[@]}" \
  -X PATCH "$BASE/api/v1/copy-tasks/$TASK_ID" \
  -d "$PAYLOAD"
```

Copy mode guidance:

- `ONE_TO_ONE`
- `FIXED_SIZE`, which should include `taskConfig.fixedAmount`

### Example: switch to fixed-size copy

```bash
PAYLOAD="$(jq -n \
  --argjson fixedAmount 5 \
  '{taskConfig: {copyMode: "FIXED_SIZE", fixedAmount: $fixedAmount}}')"
```

### Delete copy task

Required flow:

1. Validate `taskId`.
2. Check active positions:

```bash
curl -sS --fail-with-body "${AUTH[@]}" \
  "$BASE/api/v1/copy-tasks/$TASK_ID/positions?status=active"
```

3. If active positions exist, confirm the cleanup step, then clear them first:

```bash
curl -sS --fail-with-body "${AUTH[@]}" \
  -X POST "$BASE/api/v1/copy-tasks/$TASK_ID/sell-all"
```

4. Delete the task:

```bash
curl -sS --fail-with-body "${AUTH[@]}" \
  -X DELETE "$BASE/api/v1/copy-tasks/$TASK_ID"
```

Guidance:

- There is no direct position-delete endpoint in the current API. Position cleanup before delete should use `sell-all`.
- If the active positions list is empty, delete the task directly after confirmation.

### Batch delete tasks

Required flow:

1. Validate all `taskIds`.
2. For each task, check active positions and run `sell-all` first when needed.
3. After the cleanup step finishes, batch delete:

```bash
TASK_IDS=("64f0c7e7b8e4f8c1a1b2c3d4" "64f0c7e7b8e4f8c1a1b2c3d5")
PAYLOAD="$(jq -n \
  --argjson taskIds "$(printf '%s\n' "${TASK_IDS[@]}" | jq -R . | jq -s .)" \
  '{taskIds: $taskIds}')"

curl -sS --fail-with-body "${AUTH[@]}" \
  -X POST "$BASE/api/v1/copy-tasks/batch-delete" \
  -d "$PAYLOAD"
```

## Error Handling

- `400`: invalid payload
- `401`: missing or invalid API key
- `404`: resource not found
- `5xx`: server error
