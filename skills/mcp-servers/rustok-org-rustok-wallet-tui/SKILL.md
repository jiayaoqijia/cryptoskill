---
name: rustok-wallet-tui
description: Self-custody Ethereum agent wallet. Installs from a verified release and runs entirely on your machine as a single container image (MCP over stdio); private keys never leave it. New connections are read-only. Read wallet context, balances and DeFi positions (Aave v3, ERC-4626); preview transactions. Sending funds on-chain is gated in a separate terminal console, never inside the agent chat: you approve each payment, or confirm autonomous mode once and the wallet sends on its own after that; message signing is refused outright, in every mode. You assume all risk for funds on the agent wallet — there are no hard-coded spending limits.
version: 0.12.0
metadata:
  openclaw:
    emoji: "🦀"
    homepage: https://github.com/rustok-org/mcp
---

# rustok-wallet-tui

> **License note:** this OpenClaw skill package (`skills/rustok-wallet-tui/`) is MIT-0
> per ClawHub requirements. The Rustok wallet core itself is proprietary; only the
> compiled binary image is distributed.

You are connected to a **self-custody** Ethereum agent wallet that runs entirely
on the user's machine as a single Docker image (`ghcr.io/rustok-org/rustok-wallet-tui`).
The container runs the wallet core + gateway and speaks MCP over **stdio**; the
private keys live only in the user's local Docker volume and never leave it.

> ⚠️ **Self-custody, real funds, your risk.** This wallet has **no hard-coded
> spending limits or budgets** — the user consciously accepts that funds sent to
> the agent wallet are at risk. txguard still flags risky transactions, but it
> does not block them. All supported chains the user enables are live (incl.
> Ethereum mainnet). New connections expose only read tools. If the user explicitly grants preview/execute, always preview before executing and show the user the details.

## What's protected — and what isn't (be honest with the user)

The wallet's guarantee is narrow and specific. State it plainly; do not oversell it.

The full list of boundaries — password delivery, updates, what we do not verify at
all — lives in [docs/CAVEATS.md](https://github.com/rustok-org/mcp/blob/main/docs/CAVEATS.md).

| | |
|---|---|
| **Protected** | Private keys stay in the user's **local Docker volume** and never leave the machine. **Sending funds on-chain** (`execute_transaction`) is gated in a **separate console window** (`rustok console`, opened by the user — see below): parked for the user's approval, with a PIN for high-risk items — unless the user has confirmed **autonomous mode** there, a confirmation only they can give, once per wallet. |
| **Refused, not gated** | `sign_message` (EIP-191) is **refused outright** — in every mode, autonomous included. The console never sees a signature request, because signing does not happen at all: parking a signature for approval (`kind:sign`) is planned and not built. A tool that is listed and always refuses is neither a capability to rely on nor a hole to fear. Tell the user that rather than letting them plan around a signature. |
| **Outside the model** | An agent with **shell / `docker exec` access to the container** can read secrets and bypass client isolation. Direct message and typed-data signing are refused by the core in all wallet modes; a compromised host can still steal the private key. That is why the console is a **separate window, not an agent command**. Trusting your own agent is the user's call, the same as never pasting a seed phrase into an untrusted tool. |

**Never claim** the agent (or a prompt-injected agent) "cannot move funds." What is
true: keys stay local, and supervised sends wait for approval in the console.
Once the user confirms autonomous mode, an execute grant can spend the full
wallet balance without approval of each payment.

### The mode switch, and why a send may still park

The user switches the wallet's mode **in the console**: press **`c`** on the
Dashboard, pick `read_only` / `supervised` / `autonomous`, enter the PIN. That
is how autonomy is turned ON — and OFF: switching back to `supervised` parks
every future send again, and `read_only` refuses every write outright. The
agent cannot flip that switch, and neither can an environment variable or a
launch flag. Until a human has confirmed autonomy there, an autonomous-looking
wallet **parks every send** exactly like a supervised one.

**Turning autonomy on does not release what already waits.** A payment parked
before the switch stays parked — it goes out when the user releases it in the
console, or expires. Do not retry it: a retry adds a second parked copy that
will be paid separately if released, and switching the mode releases neither
of them.

**Your session reads the wallet's mode once, when it connects.** If the user
switches the mode mid-session, your tool list does not change until the next
connect — a tool you still see may now be refused by the core. The refusal is
the wallet enforcing the new mode; tell the user what it said, do not retry
around it.

Confirmation from a messenger does not exist yet — the console is the only
place the switch can be thrown.

## What changed in 0.9.8

- **`sign_message` is refused outright, and these texts finally say so.** Every
  earlier release described it as an ungated hole you had to guard against. It is
  not a hole and not a protection: signing is an unfinished capability, and
  parking a signature for approval is planned and not built. Live acceptance of
  0.9.7 asked the wallet and got a refusal; nine texts had said otherwise.

## What changed in 0.9.7

- **The wallet states what it does not promise.** A `## Legal` section below, and
  a full [DISCLAIMER](https://github.com/rustok-org/mcp/blob/main/DISCLAIMER.md)
  that names the limit of every safeguard — starting with the one easiest to read
  as absolute: autonomous mode sends without asking once confirmed.

## What changed in 0.9.5

- **Gas limits now carry headroom.** A limit set to exactly the estimate turned
  any drift between estimating and executing into a burnt fee — a contract call
  could pay its gas and do nothing. Plain transfers were never affected.
- **ERC-20 tokens are documented at last** (see below). The wallet has been able
  to report registered tokens since 0.9.4, but nothing here said so, and an
  unregistered token reads exactly like an absent one.
- **`rustok connect --force` names what it is about to drop** instead of quietly
  rebuilding the registration from the current shell.

## Prerequisites

- **Podman** (recommended) or **Docker**, curl, a SHA-256 tool and **trusted cosign 3+**. Install the verifier independently using a trusted system package channel; do not download and execute an unverified verifier in this bootstrap. See [Sigstore installation](https://docs.sigstore.dev/cosign/system_config/installation/).
- An Ethereum RPC URL (public endpoints can be used for testing).

## One-time onboarding (the user does this in their own terminal, once)

Use the **published release SKILL.md** from the release/listing you trust. The repository file is a template: its bootstrap hash is deliberately unfilled and refuses to run. The generated [release SKILL.md](https://github.com/rustok-org/mcp/releases/download/wallet-tui-v0.12.0/SKILL.md) binds the installer bytes before execution. A release bundle is also published as `wallet-skill.zip` with SKILL.md, claw.json, the exact installer, manifest and signature bundle.

**1. Verify and install the command.** Blob verification uses the fixed release workflow/tag identity below, independently of downloaded certificate data. OCI verification inside the verified installer separately uses the image-publishing workflow on main. Missing/broken/old verifier, bad signature or unavailable verification network refuses installation. Reading the installer costs about ~214 lines of POSIX sh.

```sh
(
  set -eu
  wallet_version=0.12.0
  expected_installer_sha256='@INSTALLER_SHA256@'
  # This hash is filled in the published release SKILL.md, not guessed locally.
  printf '%s\n' "$expected_installer_sha256" | grep -Eq '^[0-9a-f]{64}$' || {
    echo 'Use the published release SKILL.md: this source template is not an installer.' >&2; exit 1;
  }
  cosign_version=$(cosign version 2>/dev/null) || {
    echo 'Install trusted cosign 3+ independently before continuing.' >&2; exit 1;
  }
  cosign_major=$(printf '%s\n' "$cosign_version" | sed -n 's/^GitVersion:[[:space:]]*v\([0-9][0-9]*\)\..*/\1/p')
  case "$cosign_major" in ''|*[!0-9]*) exit 1 ;; esac
  [ "$cosign_major" -ge 3 ] || exit 1
  stage_dir=$(mktemp -d)
  trap 'rm -rf "$stage_dir"' EXIT
  release_base="https://github.com/rustok-org/mcp/releases/download/wallet-tui-v$wallet_version"
  for asset in install.sh release.manifest release.manifest.sigstore.json; do
    curl --proto '=https' --tlsv1.2 -fsSL "$release_base/$asset" -o "$stage_dir/$asset"
  done
  cosign verify-blob "$stage_dir/release.manifest" \
    --bundle "$stage_dir/release.manifest.sigstore.json" \
    --certificate-identity "https://github.com/rustok-org/mcp/.github/workflows/release-shelf.yml@refs/tags/wallet-tui-v$wallet_version" \
    --certificate-oidc-issuer https://token.actions.githubusercontent.com
  if command -v sha256sum >/dev/null 2>&1; then
    actual_sha=$(sha256sum "$stage_dir/install.sh" | cut -d' ' -f1)
  elif command -v shasum >/dev/null 2>&1; then
    actual_sha=$(shasum -a 256 "$stage_dir/install.sh" | cut -d' ' -f1)
  elif command -v openssl >/dev/null 2>&1; then
    actual_sha=$(openssl dgst -sha256 "$stage_dir/install.sh" | sed 's/.*= //')
  else
    echo 'A SHA-256 tool is required.' >&2; exit 1
  fi
  [ "$actual_sha" = "$expected_installer_sha256" ] || {
    echo 'Installer checksum mismatch; refusing to execute it.' >&2; exit 1;
  }
  less "$stage_dir/install.sh" # read the same verified file before executing it
  sh "$stage_dir/install.sh" --manifest "$stage_dir/release.manifest" \
    --bundle "$stage_dir/release.manifest.sigstore.json"
)
```

The installer never initializes a wallet, changes keys or registers an agent. It stores the signed release digest for all standard future launches; an image tag being repointed cannot change those selected bytes. It does not bootstrap cosign automatically.

**2. Create the wallet** — the user chooses a 6-digit approval PIN; it prints the
12-word phrase ONCE:

```bash
rustok init
```

**3. Register this wallet with the agent client (read-only by default):**

```bash
rustok connect claude
```

To grant transactions, the user runs `rustok connect claude --force --capabilities read_wallet,preview_tx,execute_tx` in their own terminal and confirms the expansion. Capabilities only bound the client; wallet policy/PIN remains a separate gate. Existing explicit subsets are preserved on reconnect/update; implicit or invalid old grants migrate to read-only. A read-only session cannot poll execution status. It must not interpret losing status access as a failed payment or replay an unknown outcome.

`rustok init` asks the user to choose a **6-digit approval PIN** (typed twice) —
the one code they will ever enter: it unlocks the console session and confirms
payments. The keyring password that encrypts the keystore is generated by `init`
itself and kept in the engine's secret store; the user never sees or types it,
and it never reaches shell history, `inspect` or any config file. `init` prints
exactly one thing, once: the **12-word recovery phrase**.

The 12 words are the only backup — write them down offline; the wallet does not
store them. Recovery is `rustok restore` (or importing the words into any standard
BIP-39 wallet — same address). A copy of the wallet volume by itself is **not** a
backup: the password that opens it lives outside the volume and is not something
the user knows. If the PIN is forgotten, `rustok set-pin` lets them choose a new
one — the old PIN is not needed. This changes the approval PIN, not keystore encryption. Restore from the same phrase recovers the same private key and does not revoke a leaked key.

> **Rule of two windows:** never run `rustok init`, `rustok restore`,
> `rustok set-pin` or the approval console through an agent shell/command — the
> seed and PIN would leak into the agent's context. These belong only in the
> user's own terminal (window 2). Do not ask the user for their PIN or their
> phrase in this chat, ever.

## Stopping and uninstalling

`rustok stop` stops the selected wallet process. `read_only` refuses new writes;
removing a client registration removes its launch entry but does not stop live
sessions. None of these actions deletes stored secrets or revokes the private
key. Before stopping for teardown, stop new requests,
resolve pending approvals and wait for active execution outcomes as described
under maintenance below. Never automatically replay an unknown payment.

**Before uninstalling, explain that stored keyring passwords are deleted. An
encrypted volume alone is not a recoverable backup.** The user must confirm they
have their recovery phrase backed up offline before proceeding; never ask them
to paste it into chat.

The user runs `rustok uninstall` in their own terminal. It deregisters supported
clients, stops wallets and removes stored passwords/RPC secrets, the installed
shim/release record and the installer PATH block. Encrypted key volumes remain.
Check reported warnings for registrations or other state that still need manual
removal; do not describe a partial teardown as complete.

To delete key volumes too, choose `rustok uninstall --purge-keys` **instead of**
ordinary uninstall. It requires the user's own terminal and the exact
`delete my keys` confirmation before changes. Without the recovery phrase,
deleting those keys makes the funds unrecoverable. These are human maintenance
commands, not agent commands.

## Where the balance you show comes from

The wallet reads chains through an RPC node. Since 0.11.0 it carries two public
endpoints for each chain it shows (Ethereum, Base, Arbitrum by default), so a
fresh install reports balances without the user configuring anything, and USDC
appears beside the native coin without being registered.

**Tell the user this when it matters, and never as a footnote to a payment:** any
node that reads a balance learns the address and the IP that asked — the
carried ones, one they name themselves, and their own provider's alike. They
replace the carried list with `RUSTOK_RPC_URLS_<chain>`; naming one replaces the
list rather than adding to it.

On Arbitrum two USDC rows are normal: the native token and the bridged one, which
the wallet labels `USDC.e`. On chain both call themselves `USDC` — only the
contract address separates them, which is why balance rows carry it. Never treat
them as one balance, and never sum them without saying you did.

## How the agent runs the wallet

`rustok connect claude|cursor|hermes|openclaw` generates the engine command using the saved immutable release digest, per-agent labels/volume and one explicit capability grant. Do not build a second version-tag recipe. Each client owns its wallet by default; shared-volume concurrent writers are not verified as separate client principals. Config paths with spaces remain single arguments.

Init uses `podman secret create` with the password on stdin, never in argv. The generated keyring password lives outside the encrypted volume, in a Podman secret or an owner-readable Docker fallback file. It is delivered through `RUSTOK_KEYRING_PASSWORD_FILE`; it is not collected by the agent, stored in agent config, printed or passed as a command-line password. These local file mounts unlock only the user's own wallet; they are not requests to read unrelated credentials. Host/shell compromise remains outside this protection. With Podman, RPC URLs configured through connect ride per-agent secrets; raw environment forwarding and the Docker fallback can expose configured RPC URLs in engine metadata. Keep keyed URLs out of agent chat.

For maintenance, `rustok update` verifies a signed release and preserves explicit subsets. Live sessions retain their old image/grants until a human restart. Stop new requests in all sessions, resolve pending approvals and wait for active execution terminal outcomes before `rustok stop`. Previews, pending approvals and status outcomes do not survive restart. Unknown payment results require audit/hash/network investigation; never replay automatically. No persistent execution ledger is promised.

## Why Rustok exists

Rustok gives an AI agent a wallet of its own — self-custody, no middleman — so agents can begin
to take part in the economy directly: weighing what's worth paying for, covering the compute,
data, and tools they rely on, and in time commissioning and paying the people who help them.

## Tools

The stdio wallet image defaults to **read-only** tools. Preview and execution require an explicit human capability grant; initialize only narrows that ceiling.
To run a restricted agent, set `RUSTOK_MCP_CAPABILITIES` to a subset
(`read_wallet` / `preview_tx` / `execute_tx`) — e.g. `read_wallet` for read-only.
The ceiling is enforced by the gateway, on the path every request takes: it
covers the MCP tools below **and** the HTTP routes behind them, so a session
cannot reach past its capabilities by calling the gateway directly. In releases
before 0.9.0 the ceiling was checked in the MCP layer only, which left every
route reachable beside it: the core refused signing for its own unrelated
reasons, but a session narrowed away from `read_wallet` still read the wallet
address and every balance. A client may narrow its own session further in
`initialize`, and can never widen it.

| Tool | Capability | What it does |
|------|-----------|--------------|
| `get_wallet_context` | read_wallet | Active wallet address, the assets it holds (native coin + registered tokens), the assets it could not read, allowed chains |
| `get_balances` | read_wallet | Balances of the active wallet — one row per asset, with `balance_formatted` to show and `token_address` to tell two same-named tokens apart — or the native balance of `{address, chain_id}` |
| `get_positions` | read_wallet | DeFi positions — Aave v3 (collateral/debt/health factor/LTV) + ERC-4626 vaults; optional `{address}` |
| `preview_transaction` | preview_tx | Preview any transaction `{to, value, chain_id, data?}` → decoded call (who/what is authorized), pre-sign simulation (revert check), gas, risk level |
| `execute_transaction` | execute_tx | Submit a previewed transaction `{preview_id}` — parked for human approval on a supervised wallet, released by the core on one whose owner confirmed autonomous mode; a `pending` result carries `next_step` for the human |
| `get_execution_status` | execute_tx | Poll a parked execution `{preview_id}` → `pending` / `executed` (+`tx_hash`) / `denied` / `expired` / `failed` (+`error_reason`), with the `not_after_unix` deadline. **`executed` means broadcast, not on-chain success** — see below |

### ERC-20 balances use a configured registry

The wallet reports tokens in its configured registry and does not discover every
token the address holds. On carried chains, the default registry includes USDC
(and USDC.e on Arbitrum). An explicit `RUSTOK_TOKENS_<chain>` value **replaces**
that chain's carried registry rather than adding to it. To select a registry:

```bash
-e RUSTOK_TOKENS_1="USDC:0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48:6"
-e RUSTOK_TOKENS_8453="USDC:0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913:6"
```

`SYMBOL:ADDRESS:DECIMALS`, comma-separated, one variable per chain, and the chain
must be listed in `RUSTOK_ALLOWED_CHAINS`. A malformed entry, a duplicate address
on one chain, or an unknown chain **fails startup** naming the chain — a
half-loaded registry is worse than none. Symbol and decimals are taken from the
user, not read from the contract: get the decimals wrong and the wallet will show
a wrong amount confidently.

**What this means for you, the agent:** before telling the user they hold none of
a token, say that it may simply not be registered. Reading an empty list as an
empty wallet is the likeliest way to be wrong here — and it has already happened.

## Behavioral guidelines

1. **Always `preview_transaction` first** and show its decoded call + simulation (revert check) + risk level so the user gives informed approval.
2. **The money path is preview → summary card → `execute_transaction` → core policy.**
   In supervised mode, the transaction waits for human approval (`state: "pending"`)
   in a separate terminal running `rustok console`. Once the user confirms
   autonomous mode, execution can broadcast without approval of each payment;
   an execute grant can spend the full wallet balance. Report the actual returned
   state rather than promising that a send only waits. Never offer to run the
   console yourself or ask the user to paste the approval PIN into chat.
3. **`executed` means the transaction was broadcast, not that it succeeded.**
   The wallet reports the hash the moment the network accepted the transaction
   for inclusion; a transaction that reverts on-chain still costs its gas and
   still reads as `executed` here. Verify the receipt independently before
   telling the user their swap or approval went through — an explorer, or
   `eth_getTransactionReceipt` where `status` must be `0x1`.
4. **Poll `get_execution_status` reasonably**: when the user asks, or every ~15–30
   seconds until the `not_after_unix` deadline (if it is `null` — only on request).
   Stop on any terminal state: `executed`, `denied`, `expired`, `failed`. A
   `denied` outcome is the human's answer — do not re-submit the same transaction;
   a not-found error means the id is no longer retained — stop polling.
5. **Surface what the preview decoded** (who/what is authorized, amount, revert check, estimated cost, risk level) before the user acts on it.
6. **Use `get_wallet_context` first** so you don't hallucinate balances or chains.
7. If a tool needs a capability the session lacks, it returns an authorization
   error — explain that to the user rather than retrying.
8. If the wallet is unreachable, tell the user the wallet container/onboarding may
   not be set up (see onboarding above).

## Legal

Provided **as is**, without warranty of any kind, under the MIT-0 license.
**What an agent does with this wallet is not an act of the authors:** the agent
driving it is third-party software whose output is unpredictable and may be
inaccurate, incorrect, or undesirable, and evaluating each proposed transaction
before approving it is the user's exclusive responsibility. Nothing this wallet
or the agent driving it produces is investment, accounting, legal, or tax advice.
Sending funds is gated at the console **unless autonomous mode was confirmed**;
**`sign_message` is refused outright** in every mode. The risk of loss is
substantial and the user assumes all of it.

Full terms, and every safeguard's limit named:
<https://github.com/rustok-org/mcp/blob/main/DISCLAIMER.md>
