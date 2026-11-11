---
name: evm-contract-control-audit
description: >-
  Find out who controls an EVM smart contract or protocol. Use when the user
  asks who owns, who controls, who can upgrade, who can mint or pause, or who
  holds the admin roles on an Ethereum, Base, Arbitrum, Optimism, Polygon, BSC
  or other EVM contract; whether an admin is an EOA or a multisig; whether a
  Safe is 1-of-N; whether privileged calls go through a timelock; to audit a
  protocol's admin surface or control graph; to produce a monitoring config for
  owner/role/upgrade changes; or to verify an ERC-8241 control disclosure
  against the chain. Read-only: no key, no wallet, nothing is ever sent
  on-chain.
---

# Auditing who controls an EVM contract

This skill answers "who controls this contract?" from on-chain state: owners,
proxy upgrade admins, beacons, Safe signers and thresholds, timelock delays,
AccessControl and AccessManager roles, and the control graph above a target. It
is built on [ownerwatch](https://github.com/imal1ice/ownerwatch) and is entirely
read-only.

## The one rule that governs every answer

**A read of chain state is a chain view, not a verdict.** Report what the
contract state says, not whether the protocol is safe:

- An EOA admin on-chain may be one private key, a hardware wallet, or an MPC
  setup. The chain cannot tell them apart. Say "a single externally-owned
  account on-chain" and let the team state the custody.
- A Safe's signers may all be one person, or a well-run quorum. The chain shows
  the threshold, not who holds the keys.
- The absence of a finding is **not** proof that a contract is safe — only that
  this read did not surface one. Always report what the read could **not**
  establish.
- **Never claim a privileged call is possible from its role structure alone.**
  A role-admin that points at `DEFAULT_ADMIN_ROLE` does not prove the holder can
  grant it: `grantRole` can be overridden by a custom guard that reverts. Prove
  it with a simulation (`--prove`, below) before you call anything a bypass.

## How to run it

Prefer the **ownerwatch-mcp** server if it is configured in the agent — call its
`probe_admin_surface`, `check_disclosure` and `suggest_monitoring_config` tools.
Otherwise use the CLI:

```bash
pip install ownerwatch        # Python 3.10+
```

The CLI needs an RPC URL for the target's chain (`--rpc`). Public endpoints:

| Chain | RPC |
|---|---|
| Ethereum | https://ethereum-rpc.publicnode.com |
| Base | https://base-rpc.publicnode.com |
| Arbitrum One | https://arbitrum-one-rpc.publicnode.com |
| Optimism | https://optimism-rpc.publicnode.com |
| Polygon | https://polygon-bor.publicnode.com |
| BNB Chain | https://bsc-rpc.publicnode.com |
| Avalanche C | https://avalanche-c-chain-rpc.publicnode.com |

A read that fails (RPC down, rate-limited, wrong chain, no code at the address)
proves nothing either way. Say so; do not report a failed read as a clean one.

## What to do, by request

**"Who controls / who can upgrade this?"** — the admin-surface report:

```bash
ownerwatch probe --markdown --rpc <rpc> 0xTarget [0xMore ...]
```

Walks each target's owner, upgrade admin, beacon, Safe and timelock, and flags
EOAs, 1-of-N Safes and powers held with no timelock. Add `--json` for structured
output, `--label <name>` for a title.

**"List every role holder"** — replay the logs (needs an RPC with log history):

```bash
ownerwatch probe --markdown --roles-from-logs --rpc <rpc> 0xAccessControlContract
```

Lists every current holder of every role, replayed from `RoleGranted`/
`RoleRevoked` since deployment and re-confirmed with `hasRole`. To test the
protocol's known Safes/keys for roles without probing them as targets, pass them
to `--role-candidates 0xA,0xB`.

**"Prove a finding is real"** — simulate the privileged call:

```bash
ownerwatch probe --prove --rpc <rpc> 0xTarget
```

Runs each finding's privileged call (`transferOwnership`, `upgradeTo`,
`grantRole`, a mint/pause role, a timelock `schedule`) as an `eth_call` from the
holder and from a stranger (`0x…dEaD`) at one pinned block. It reports `proven`
only when the call **succeeds from the holder and reverts from the stranger**.
A call that reverts from both, succeeds from both, or whose arguments cannot be
guessed is reported `not simulated: <why>`, never proven. Nothing is ever sent.

**"Give the team a monitor"** — write a ready config, then run it:

```bash
ownerwatch probe --yaml --label <name> --rpc <rpc> 0xTarget 0xSafe > config.yaml
ownerwatch run --config config.yaml      # add an alerts webhook (Discord/Slack/Telegram) first
```

For a weekly CI check instead, the GitHub Action `imal1ice/ownerwatch-action@v1`
runs the same config and fails the build when control drifts.

**"Verify this ERC-8241 disclosure"** — check it at a pinned block:

```bash
ownerwatch disclosure check disclosure.json --rpc <rpc> [--block N]
```

Each record comes back `ok`, `mismatch` or `unverifiable`, and the checker also
lists control it sees on the declared components that the disclosure left out.
It exits 1 on any mismatch or undisclosed power, 2 when the chain could not be
read.

## How to report back

1. Lead with the one rule: this is a chain view, not a verdict.
2. For each target: the owner, the upgrade admin, the Safe (signers/threshold)
   or timelock (delay) above it, and whether any privileged call has no delay.
3. Call out the sharp findings plainly — an EOA admin, a 1-of-N Safe, an upgrade
   or mint/pause power with no timelock — and, when asked whether one is
   exploitable, show the `--prove` result rather than arguing from structure.
4. End with what the read could not establish (off-chain key custody, anything
   not in contract state), so the team knows the edges of the answer.
