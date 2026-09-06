---
name: gate-dex-wallet-tx-checkin
version: "1.5.2"
updated: "2026-04-03"
description: "Mandatory tx check-in before any wallet signing MCP call: run the prebuilt tx-checkin CLI from tools/tx-checkin/bin/ (no Go compile or go build for end users). Applies before dex_wallet_sign_transaction, dex_wallet_sign_message, and dex_tx_x402_fetch unless product documents a replacement MCP check-in. Installation does not auto-run the binary."
---

# Gate DEX Tx Check-in (terminal)

> **Mandatory execution path**: check-in is performed by the **`tx-checkin`** CLI in the user terminal. Do **not** substitute an MCP-only call for this step unless product explicitly documents an MCP tool that performs the same gateway check-in (this skill assumes **terminal only**).
>
> **End users — no compile**: Use the **prebuilt** check-in executables shipped under **`tools/tx-checkin/bin/`** for your OS. **Do not** run **`go build`**, **`go run`**, or install Go for normal use. Only **maintainers** rebuilding artifacts need the Go toolchain (see Prerequisites).

## Hard rule (wallet skill policy)

- **Before every** `dex_wallet_sign_transaction`, **every** `dex_wallet_sign_message`, and **every** `dex_tx_x402_fetch` call, the agent **MUST** complete this terminal check-in flow successfully in the same user session (after user confirmation, immediately before that MCP call).
- **CLI path**: The agent **MUST** resolve the **prebuilt** binary from this skill’s **`skill_root`** (folder with **`SKILL.md`**) — **do not require the user to set `TX_CHECKIN`**, **do not ask the user to compile**. On **Linux**, run **`{skill_root}/tools/tx-checkin/bin/tx-checkin-linux-amd64`** (see Prerequisites).
- **Gateway URL**: **Do not prompt the user** to set **`TX_CHECKIN_GATEWAY_BASE`** or any other gateway override; use the **built-in default** in the prebuilt binary unless product documentation explicitly requires a different host for that session.
- **Do not skip** check-in because a previous transaction succeeded without it, or because no error appeared yet.
- **x402:** **Do not** call `dex_tx_x402_fetch` first to probe 402 or GV behavior — check-in comes first; then pass `checkin_token` into `dex_tx_x402_fetch` per [x402.md](./x402.md).
- If check-in fails (non-zero exit, `ok: false`, or missing `checkin_token` when required by your gateway), **abort** — do not call signing tools or `dex_tx_x402_fetch`.
- Passing `checkin_token` into MCP tools requires **backend/MCP support**; if the tool has no parameter, rely on gateway session binding (see §9 of the backend technical documentation).

## Applicable scenarios

- **Always** before `dex_wallet_sign_transaction` (transfers, withdraws, DApp txs, any raw tx signing).
- **Always** before `dex_wallet_sign_message` (personal_sign, EIP-712, DApp login signatures). **`message` 字段**：与待签名内容一致，见下文 **Check-in `message` 规则**。
- **Always** before `dex_tx_x402_fetch` (HTTP 402 / x402 payment). Use **`-intent` / `-message` / `-body-file`** as required for the x402 flow; then pass **`checkin_token`** into the MCP tool — see [x402.md](./x402.md).
- If the gateway returns an error mentioning check-in / registration, re-run this flow and retry only after success.

## Prerequisites

1. **Prebuilt check-in only (end users)** — files live under **`{skill_root}/tools/tx-checkin/bin/`**, where **`skill_root`** is the absolute path to the **gate-dex-wallet** folder that contains **`SKILL.md`** (repo clone, Cursor skills dir, etc.).

   **Normal use**: run the matching file below **as-is** (double-click / terminal). **No `go build`, `go run`, or Go installation.** The **`.go` sources** in **`tools/tx-checkin/`** are for maintainers only.

   **Users do not need to configure any env var.** The **agent** resolves the CLI path from **`skill_root`** and the host OS, then runs that file:

   | Host (`uname -s` in bash) | Executable (relative to `skill_root`) |
   |---------------------------|---------------------------------------|
   | **Linux** | **`tools/tx-checkin/bin/tx-checkin-linux-amd64`** — always try this on Linux (x86_64/amd64) |
   | **Darwin** (macOS) | **`tools/tx-checkin/bin/tx-checkin-darwin-universal`** |
   | **Other** (e.g. **MINGW**/MSYS: Windows shells) | **`tools/tx-checkin/bin/tx-checkin-windows-amd64.exe`** |

   **Optional override**: if **`TX_CHECKIN`** is already set in the environment (CI or custom layout), the agent may use that path instead.

   On Unix/macOS, if execution fails with “Permission denied”, run **`chmod +x`** on the chosen binary once.

   **Maintainers**: from **`tools/tx-checkin`**, cross-compile with Go (`GOOS`/`GOARCH`, `CGO_ENABLED=0`); on **macOS**, run **`lipo -create -output bin/tx-checkin-darwin-universal bin/tx-checkin-darwin-arm64 bin/tx-checkin-darwin-amd64`** after building both slices (the slice binaries need not be shipped).

2. **Gateway base URL** (built into the prebuilt CLI): **`https://webapi.w3-api.com/api/web/v1/web3-gv-api`**. Full check-in request URL = that prefix + **`-path`** **`/api/v1/tx/checkin`**. There is no **`-base-url`** flag. **Signing** still uses only the internal gv path `/api/v1/tx/checkin`, not the gateway prefix. **Do not ask users to configure gateway env vars** for normal flows.
3. **Credential** — the CLI sends the **raw** token as the HTTP `Authorization` header (no `Bearer ` prefix). **No `-auth` flag and no `GATE_AUTHORIZATION` env.**
   - **Default**：从 **`~/.cursor/mcp.json`** 读取 `mcpServers.*.headers.Authorization`，自动去掉 `Bearer `。多个服务时优先名称匹配 `gate|wallet|dex|mcp`；**`TX_CHECKIN_MCP_SERVER=<key>`** 可指定唯一服务。
   - **Override (CI / 无 Cursor 配置)**：`export MCP_TOKEN='<裸 token>'`（会优先于 mcp.json）。
   - **自定义配置文件路径**：`CURSOR_MCP_JSON=/path/to/mcp.json`  
   登录变更后保存 Cursor MCP 配置即可；**勿在聊天中粘贴完整 token**。
4. Internal gv **`path`** is always **`/api/v1/tx/checkin`** for this endpoint (unless the backend documents otherwise).

For **`dex_wallet_sign_transaction`** after **`dex_tx_transfer_preview`**: take the preview JSON field **`txBundle`** (string) **as-is** — write it to a file and run **`tx-checkin`** with **`-tx-bundle-file`** plus `-wallet`, `-chain`, `-chain-category` from the same preview / wallet context. **Do not** assemble or edit txbundle JSON by hand (no `jq` construction from `unsigned_tx_hex`).

For **`dex_wallet_sign_message`**, or flows without preview `txBundle` (e.g. some DApp / x402 per backend), use **`-message`**, **`-intent` / `-intent-file`**, or **`-body-file`** as documented below.

## Check-in `message` 规则（与签名类型一致）

1. **`dex_wallet_sign_message`**：`message` = **待签名的那条消息**（与后续 MCP 要签的 payload 一致）。CLI：**`-message "<...>"`**。
2. **`dex_wallet_sign_transaction`**（且上游为 **`dex_tx_transfer_preview`**）：check-in 的 `message` **等于** 预览返回的 **`txBundle`** 字符串。终端：**将该字符串写入文件后** **`tx-checkin -tx-bundle-file <path>`**（不要 `-tx-checkin-category`）。**禁止**用脚本从 `unsigned_tx_hex` 等字段拼接 txbundle。

若后端要求 `intent` 对象、或全量自定义 body，用 **`-intent` / `-intent-file` / `-body-file`**（与 `-message`、`-tx-bundle-file` 互斥，按 CLI 校验）。

详见后端技术文档 §2.3。

## Agent flow

1. Confirm the user intends to proceed to signing (e.g. after explicit confirm on a preview or message text).
2. **In the user terminal, run check-in** (mandatory immediately before any signing MCP tool; example — set **`skill_root`** to the absolute path of **gate-dex-wallet**; adjust flags to match the transaction):

```bash
# Agent: pick CLI from skill_root + OS (no user export required). Optional: TX_CHECKIN overrides.
skill_root="<absolute/path/to/gate-dex-wallet>"
if [ -z "${TX_CHECKIN:-}" ]; then
  case "$(uname -s)" in
    Linux)  TX_CHECKIN="$skill_root/tools/tx-checkin/bin/tx-checkin-linux-amd64" ;;
    Darwin) TX_CHECKIN="$skill_root/tools/tx-checkin/bin/tx-checkin-darwin-universal" ;;
    *)      TX_CHECKIN="$skill_root/tools/tx-checkin/bin/tx-checkin-windows-amd64.exe" ;;
  esac
fi
chmod +x "$TX_CHECKIN" 2>/dev/null || true

# Sign message: -message = exact payload to be signed
"$TX_CHECKIN" \
  -path "/api/v1/tx/checkin" \
  -wallet "<wallet_address>" \
  -chain "<chain>" \
  -chain-category "<chain_category>" \
  -message "<message_to_sign>"

# Sign transaction after dex_tx_transfer_preview: write preview field txBundle (string) to a file, pass as-is
# Example: jq -r '.txBundle' preview.json > bundle.txt   # if preview JSON is saved as preview.json
"$TX_CHECKIN" \
  -path "/api/v1/tx/checkin" \
  -wallet "<wallet_address>" \
  -chain "<chain>" \
  -chain-category "<chain_category>" \
  -tx-bundle-file "<path_to_txBundle.txt>"
```

The JSON body always includes `"source": 3` (aiAgent); there is no `-source` flag.

Use `-intent` / `-intent-file` instead of `-message` when the backend expects an `intent` object. For a full body built elsewhere, use `-body-file <file>` (the tool still sets/overrides `"source": 3` in the compacted JSON).

3. On success, parse **stdout** JSON: `ok`, `checkin_token`, `need_otp`. If `need_otp` is true, prompt the user per product OTP flow.
4. On non-zero exit or `ok` false, stop; show stderr / error; do not call signing tools.
5. Only then continue with the signing MCP call ([transfer.md](./transfer.md), [dapp.md](./dapp.md), [withdraw.md](./withdraw.md)) or **`dex_tx_x402_fetch`** ([x402.md](./x402.md)). **`dex_wallet_sign_transaction`**, **`dex_wallet_sign_message`**, and **`dex_tx_x402_fetch`** (when the tool defines it) require the **`checkin_token`** argument: use the **`checkin_token`** string from the **successful** terminal check-in **stdout JSON** (same flow as the transaction, message, or x402 payment).

On failed HTTP or transport errors, **stderr** may include **`# Replay with curl`** (multiline bash) to replay the same request locally; treat **`Authorization`** as secret.

## Further reading

For CLI flags, response shape, and the `api-sign` algorithm, refer to backend technical documentation or the inline descriptions above.
