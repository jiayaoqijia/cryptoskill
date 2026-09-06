---
name: sui-agent-wallets
description: >
  Giving an autonomous agent a wallet on Sui that it cannot drain. Use when
  writing, reviewing, or debugging code where an AI agent holds funds, signs
  transactions, or acts on a user's behalf on Sui, and when the task involves
  spend limits, human approval steps, scoped delegation, or signing across Sui
  and other chains from one account.
---

# Sui Agent Wallets Skill

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information sourced from [docs.sui.io](https://docs.sui.io) and [docs.waap.human.tech](https://docs.waap.human.tech). Each reference file cites the specific page it is derived from.

An agent that holds a private key can be talked out of it. Prompt injection, a
poisoned tool result, or a malicious NFT in the agent's own inbox are enough,
and the published incidents of an agent losing funds share a shape: the key was
reachable from the agent's context, so the agent's judgment was the only control
standing between an attacker and the money.

This skill covers the alternative on Sui: the agent holds **no key**, and the
limits are enforced **beneath** the agent rather than by its own code. In WaaP
Squid Mode on Sui that authority is a **capability object**, which means the
permission to sign is onchain state a Move package can gate, not a config file
the agent can edit.

The most common AI-coding mistakes it prevents:

- Putting a private key or seed phrase in an agent's environment, prompt, or
  tool output, then trying to control spend with instructions.
- Assuming a spend limit enforced in agent code is a security boundary. It is
  documentation. An agent that can edit its own config can raise its own limit.
- Treating a policy refusal as terminal when it is an escalation to a human.
- Treating Sui like an account-based chain when the authority is an object.
- Assuming a delegated scope is permanent, or that it can be recalled early. It
  expires, and the expiry is the control.

This skill routes to focused reference files. Load only the ones relevant to the
current task.

If unsure about any command, run `waap-cli commands --json`. It emits the
authoritative machine-readable command schema for the installed version, and the
docs recommend it over any page or `--help` when generating automation. Do not
guess or extrapolate from other SDKs or wallet CLIs.

**Sui fundamentals are not repeated here.** For Programmable Transaction Blocks,
the object model, and client configuration, load the official
[`ptbs`](https://github.com/MystenLabs/skills/tree/main/ptbs),
[`object-model`](https://github.com/MystenLabs/skills/tree/main/object-model) and
[`sui-client`](https://github.com/MystenLabs/skills/tree/main/sui-client) skills.

---

## Reference files

### setup — Provisioning an agent wallet on Sui
**Path:** `setup.md`
**Load when:** creating an agent's wallet for the first time, provisioning
signing on Sui, funding an account, or wiring the CLI into a container.
**Covers:** account creation, the Sui capability object, the two curves and
which chains sit on each, what the account must hold before it can sign, session
isolation for concurrent agents, and which package versions carry which commands.

### policy — Limits that the agent cannot raise
**Path:** `policy.md`
**Load when:** adding spend limits, approval steps, or any control on what an
agent may do with funds.
**Covers:** where the policy gate sits, what it checks before a signature
exists, the daily spend limit and what crossing it actually does, the human
approval step, and why an in-agent check is not a boundary.

### delegation — Scoped, expiring authority
**Path:** `delegation.md`
**Load when:** the agent must act repeatedly without prompting a human each
time, or a scope has to be granted to a sub-agent or a third party.
**Covers:** minting and spending a Privilege from the CLI, scopes bound to
recipients, chain, a cumulative ceiling and an expiry; the maximum lifetime and
the much shorter default; the difference between a session and a standing mandate.

## Routing guide

| Task | Load |
|------|------|
| Creating an agent's wallet on Sui | setup |
| Funding an agent so it can sign | setup |
| Running several agents on one machine | setup |
| Adding a spend limit or approval step | policy |
| Reviewing an agent for key exposure | policy + delegation |
| Letting an agent act without a prompt per action | delegation |
| Building a recurring or subscription payment flow | delegation |
| Signing on Sui and another chain from one account | setup |
| Implementing a complete agent that holds funds | **all reference files** |
| Code review of any agent that touches money | **all reference files** |

## Skill Content

### Key concepts

**The agent holds no key.** Keys are generated and used inside secure hardware
and never reach the agent's machine, container, or context. There is no key in an
env var, no seed phrase in a file, and nothing in a tool result that can be
exfiltrated by convincing the agent to print it.

**In Squid Mode the authority is a Sui object.** What the account holds is a
**capability object on Sui**. Signing is gated on that object, which is why the
permission is onchain state rather than a server-side flag. It is transferable,
so the user is not locked to one operator, and because it is an object a Move
package can wrap it and impose its own conditions before a signature is
requested. This is specific to Squid Mode; the standard mode signs in secure
hardware and has no capability object.

**Two curves, one account.** One login provisions two curves: `secp256k1` for
EVM chains and `ed25519` for Sui and Solana. The same account therefore signs on
Sui and on other chains without a second wallet. The addresses are native on
each chain, and nothing is moved between them.

⚠️ **Curve compatibility is not chain availability.** A chain sitting on one of
those curves is reachable without new cryptography, but each still needs
transaction formatting and network plumbing. **Live today: EVM, Sui and
Solana.** Do not tell a developer an account can transact on any chain on either
curve.

**The gate sits in front of the key, not around it.** Every signing request is
checked server-side before a signature exists: the exact transaction bytes are
verified, the policy engine returns one verdict, and the approval is single-use
and bound to that one request. An agent cannot route around a check it never
performs.

**`--chain` is required on every signing command.** There is no global default
`chain set` is deprecated and stores nothing. A transaction always names the
network it is going to.

### Rules

1. **Never put a private key or seed phrase where an agent can read it.** Not in
   an environment variable, not in a prompt, not in a file the agent's tools can
   open. If a design requires this, the design is the bug.
2. **Never treat an in-agent spend check as a control.** Write the limit where
   the agent cannot reach it. An agent that can edit its config can raise its own
   limit, and an agent under prompt injection will be asked to.
3. **Scope every delegated grant on all four axes**: which recipients, which
   chain, a cumulative ceiling, and an expiry. A grant missing any one of them is
   broader than it looks.
4. **Handle escalation, not just refusal.** Crossing the daily limit raises an
   approval request rather than failing outright. An agent that treats that as a
   terminal error stops working the first time it does its job.
5. **Never pass a Privilege in argv.** `--privilege-stdin` reads it from stdin so
   it stays out of shell history, `ps` output, and logs.
6. **Default to dry run.** An agent that can spend should ship not spending.
   Turning spending on is a decision with a number attached, not a flag someone
   forgets to set.
7. **Fund the account before the first signature.** On Sui the signature settles
   onchain, so the account needs SUI for gas. A WaaP Squid Mode account also needs
   IKA for the signing network's fee. An unfunded account fails in a way that
   reads like a bug in your code.
8. **Say what is live.** EVM, Sui and Solana today.

### Common mistakes

**Storing a key "just for the agent's hot wallet."** The amount does not change
the shape of the failure, only its size. Use an account whose key the agent
never sees.

**Enforcing the limit in the loop.** A check inside the agent's own code runs
after the agent has decided. The limit has to be evaluated by something the agent
does not control, on the request, before the signature exists.

**Retrying an escalation.** A request that comes back waiting for authorization
is not a failure to retry in a loop. It is a human being asked. Wait for it, or
surface it.

**Granting an unbounded scope because it is convenient.** A grant with no
recipient allowlist can pay anyone. Bound it, and let it expire.

**Expecting a standing mandate.** A scoped grant is a session, not a
subscription. Its maximum lifetime is enforced server-side and the default is far
shorter than the maximum, so a monthly billing flow cannot be built by granting
once and forgetting. See `delegation.md`.

**Assuming the wallet is scoped to your app.** It is not. The same account works
in the next application the user visits, which is a feature for the user and a
thing to remember when reasoning about balances your app did not create.

**Confusing the signing network with Sui itself.** In Squid Mode the signature is
completed by an independent validator network together with secure hardware; Sui
is where the authority object lives and where the transaction settles. They are
different parties doing different jobs.
