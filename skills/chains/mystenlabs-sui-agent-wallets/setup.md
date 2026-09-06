# Provisioning an agent wallet on Sui

Derived from [`/for-agents/commands`](https://docs.waap.human.tech/for-agents/commands),
[`/networks/sui`](https://docs.waap.human.tech/networks/sui) and
[`/cli-reference`](https://docs.waap.human.tech/cli-reference).

## What the account is

One login provisions an account whose signing keys are generated and used inside
secure hardware. Nothing on the agent's machine holds key material.

In WaaP Squid Mode on Sui, the authority to sign is a **capability object**.
Signing is gated on that object, so the permission is onchain state rather than a
server-side flag. Two consequences worth designing around:

- **It is transferable.** The user can move it to another address, so they are
  not locked to one operator.
- **A Move package can wrap it.** Because it is an object, Move logic can hold
  it and impose conditions before a signature is ever requested.

⚠️ The capability object is specific to Squid Mode. The standard mode signs in
secure hardware, gated by security policies, and has no such object. A Move
package that imposes one rule across several chains is **demonstrable, not
shipped**. Do not present it to a developer as something they can build against
today.

## Two curves

| Curve | Chains | Live today |
|---|---|---|
| `secp256k1` | EVM networks | **EVM: yes** |
| `ed25519` | Sui, Solana, and other ed25519 chains | **Sui and Solana: yes** |

One login provisions both, so the same account signs on Sui and on EVM without a
second wallet. The addresses are native on each chain; no asset moves between them.

⚠️ Other chains on these curves are reachable **without new cryptography**, but
each still needs transaction formatting and network plumbing. Do not tell a
developer the account transacts on any chain on either curve today.

## Two signing modes

| | Standard | WaaP Squid Mode |
|---|---|---|
| Who completes the signature | Secure hardware on WaaP's infrastructure, gated by security policies | That hardware together with an independent validator network. Both required |
| Where signing authority lives | Server-side, policy-gated | A capability object your own Sui address owns |
| What the account must hold | The destination chain's gas | **SUI** for Sui gas and **IKA** for the network fee |

The two are not the same trust model, so do not describe them interchangeably.

## Chains and networks

Every signing command requires an explicit `--chain`:

| Chain | Identifier | Example |
|---|---|---|
| EVM | `<id>`, `evm:<id>`, or `eip155:<id>` | `evm:8453` |
| Sui | `sui:<network>` | `sui:mainnet`, `sui:testnet`, `sui:devnet` |
| Solana | `solana:<network>` | `solana:mainnet` |

**There is no global chain.** `chain set` and `chain get` are deprecated and
store nothing, so a transaction always names the network it is going to. `--rpc`
is optional and also per-call.

## Provisioning with the CLI

```bash
npm install -g @human.tech/waap-cli

waap-cli signup
waap-cli policy set --daily-spend-limit 100
waap-cli squid init
waap-cli squid addresses
```

`squid init` provisions both curves. `squid addresses` prints the Sui, Solana
and EVM addresses for the one account.

## Funding

**Fund the Sui address before the first signature.** A Squid Mode signature
settles on Sui and is completed by the validator network, so the account needs
**SUI** and **IKA**. An unfunded account fails in a way that reads like a bug in
your own code.

Sui specifics that catch people out:

- **Bridged ETH is not native SUI.** Bridging ETH via the Sui Bridge creates a
  wrapped token; you still need native SUI for gas. Send native SUI first.
- **Reserve at least 0.2 SUI** for a running agent, more if it transacts often.
  Transactions are cheap (typically under 0.01 SUI) but not free.
- **Stray agent instances drain gas fast.** Running several copies by accident is
  a common way to empty an account.

## Running several agents on one machine

The CLI reads exactly two environment variables and does **not** load a `.env`
file from the working directory:

| Variable | Purpose |
|---|---|
| `WAAP_CLI_ENV` | Which deployment to target: `production` (default), `staging`, `development` |
| `WAAP_CLI_SESSION_DIR` | Where the session is stored |

**Give every agent or CI job its own `WAAP_CLI_SESSION_DIR`.** Two processes
sharing one session directory fight over the same session file. Sessions are not
scoped by environment, so changing `WAAP_CLI_ENV` without also changing
`WAAP_CLI_SESSION_DIR` lets a staging session overwrite a production one.

## Output for automation

`--json` forces JSON on stdout and suppresses plaintext progress logs; `--quiet`
suppresses progress on stderr. Combine them for a clean machine-readable stream.
Progress always goes to stderr, results to stdout. Never parse stderr.

```bash
waap-cli whoami --json
# → {"evmWalletAddress":"0x...","suiWalletAddress":"0x..."}
```

## Provisioning from the SDK

```bash
npm install @human.tech/waap-sdk
```

```ts
import { initWaaPSquid, WAAP_EVENTS } from '@human.tech/waap-sdk'

const waap = initWaaPSquid({
  environment: 'production',
  chains: ['evm', 'sui']
})

await waap.session.login()
await waap.squid.onboard()

waap.session.on(WAAP_EVENTS.squidReady, () => {
  console.log(waap.squid.getStatus())
})
```

Accounts in this mode are created explicitly. Call `onboard()` after login and
before any signing, or the first signature will fail on an account that does not
exist yet.

For a Sui dApp, the wallet also implements the `sui:switchChain` feature standard
via `@mysten/wallet-standard`, and coordinates with `@mysten/dapp-kit`'s network
context. See [`/networks/sui`](https://docs.waap.human.tech/networks/sui).

## Versions

⚠️ **Check the registry rather than trusting a version written in a document.**

```bash
npm view @human.tech/waap-cli dist-tags
npm view @human.tech/waap-sdk dist-tags
```

Squid Mode requires `@human.tech/waap-cli` **2.1+** and `@human.tech/waap-sdk`
**2.2+**. Earlier versions have no `squid` command group and no `initWaaPSquid`,
so an agent built against an older install fails at provisioning rather than at
signing, which is a confusing place to debug.

`waap-cli commands --json` emits the authoritative command schema for the
installed version. Prefer it over any document when generating automation.

## Running in a container

The CLI is the surface for agents. It is headless, it holds no key, and it
authenticates a session rather than loading a secret, so a container image built
around it has nothing sensitive baked in.

Do not mount a key into the container. There is no key to mount, and a design
that wants one has reintroduced the problem this setup exists to remove.
