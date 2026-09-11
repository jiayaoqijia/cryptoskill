---
name: dexe-agent-team
description: |
  Run a team of agent personas against one DeXe DAO — a proposer creates, voters
  take opposite sides, a delegator hands power to a hub, a validator closes the
  round — using the `DEXE_AGENT_PK_*` keyring and per-call `signerKey`. Covers
  the safety model (plaintext hot keys, which guards enforce vs advise, the daily
  spend budget), funding inside the cap, the on-chain order that actually works,
  and per-persona reconciliation from the agent ledger. Use when the user says
  "run agents", "multi-agent", "swarm", "agent team", "simulate a DAO", "agents
  vote against each other", "test my DAO with bots".
---

# dexe-agent-team

Each persona is one hot key in the agent keyring, picked per call with
`signerKey: "agent<n>"`. Full reference: `docs/AGENTS.md`. Machine-readable plan:
`dexe_guide {flow:"agent_team"}`.

## 0. Say the risk out loud, first

Before configuring anything, tell the user plainly:

- **The persona keys sit in plaintext in `.env`** — no passphrase, no keychain.
- **They sign without asking.** `signerKey` broadcasts with no per-tx prompt, and
  you will be issuing those calls in a loop.
- **Use burner wallets, a throwaway DAO, and chain 97 first.** Personas with
  enough power can create *and pass* real proposals.

```bash
node -e "const{Wallet}=require('ethers');for(let i=1;i<=8;i++){const w=Wallet.createRandom();console.log('DEXE_AGENT_PK_'+i+'='+w.privateKey,' #',w.address)}"
```

### Enforces vs advises

| Control | Env | |
|---|---|---|
| keyring-only recipients (`dexe_agents_fund`) | — | **enforces**, not configurable |
| preview → `confirm: true` before any funding | — | **enforces** |
| per-transfer funding cap | `DEXE_AGENT_FUND_MAX_WEI` | **enforces** (default 0.1 native, rescaled to the token's decimals) |
| daily fleet budget | `SWARM_DAILY_BNB_BUDGET` | **enforces** — rolling 24 h of ledger value + gas, re-checked before every transfer |
| destination allowlist / value cap / rate limit | `DEXE_SIGNER_ALLOWLIST`, `DEXE_SIGNER_MAX_VALUE_WEI`, `DEXE_SIGNER_MAX_BROADCASTS_PER_MIN` | **enforce when set** — unset is *no* guard |
| pre-broadcast simulation (B9) | — | **enforces** on single sends |
| quorum / treasury-drain advisories | `DEXE_TREASURY_GUARD`, `DEXE_MIN_SAFE_QUORUM_PCT` | **advise only** — printed, never blocking |

Guards bound destinations, value and rate — **not governance outcomes**. Nothing
notices that your personas just passed a treasury transfer. Check `dexe_doctor`
for which guards are actually configured instead of assuming. And note the
budget is **not armed by default on a faucet testnet** (97): set
`SWARM_DAILY_BNB_BUDGET` explicitly if you want a cap there too.

## 1. Configure (`.env`, then restart)

```bash
DEXE_AGENT_PK_1=0x…        # → signerKey "agent1"   (alias AGENT_PK_1)
DEXE_AGENT_PK_2=0x…
DEXE_AGENT_FUNDER_PK=0x…   # → signerKey "funder"   (alias AGENT_FUNDER_PK)
DEXE_AGENT_FUND_MAX_WEI=100000000000000000
SWARM_DAILY_BNB_BUDGET=0.05
DEXE_TOOLSETS=core,agents,vote   # `agents` = the keyring tools, `vote` = the builders
```

The keyring tools are not in the default profile: `core,agents` gives
`dexe_agents_list` / `dexe_agents_fund` / `dexe_agents_ledger`, and `vote` adds
the raw builders that a delegation or validator leg needs.

`.env` only — a host `env` block silently shadows it. `process.loadEnvFile()`
runs once at startup, so **restart** after editing.

## 2. Roster → roles

```jsonc
dexe_agents_list { "chainId": 97, "token": "0x<govToken>" }
```

Assign roles only to slots this returns. Empty roster = the keyring never loaded;
stop and fix the env.

| Role | Call |
|---|---|
| Proposer | `dexe_proposal_create { signerKey }` (auto-votes FOR) |
| Voter | `dexe_proposal_vote_and_execute { signerKey, isVoteFor }` |
| Delegator | build → `dexe_tx_send { signerKey }` |
| Validator | `dexe_proposal_vote_and_execute { signerKey, driveValidatorRound: true }` — must be a registered validator |

## 3. Fund

```jsonc
dexe_agents_fund { "amount": "0.01", "agents": ["agent1","agent2"], "chainId": 97 }                 // preview
dexe_agents_fund { "amount": "0.01", "agents": ["agent1","agent2"], "chainId": 97, "confirm": true } // broadcast
dexe_agents_fund { "amount": "5000", "token": "0x<govToken>", "agents": ["agent2"], "chainId": 97, "confirm": true }
```

Previews first — show the plan and the budget impact, get a yes, then re-call
with `confirm: true`. Top-up semantics (only the shortfall, already-funded agents
skipped) make re-runs safe. The per-transfer cap is rescaled into the funded
token's decimals, and a token whose `decimals()` cannot be read is refused. A
refusal — cap or budget — is the guard working: raise it deliberately, never
split the transfer to slip under it.

## 4. The order that works on-chain

From the swarm scenarios that have run against live pools (S01 delegation,
S02 validator chamber, S07 full lifecycle):

```
1. approve(UserKeeper) + deposit   per delegator   build → dexe_tx_send { signerKey }
2. delegate(hub, amount)           per delegator   dexe_vote_build_delegate → dexe_tx_send { signerKey }
3. create proposal                 proposer        dexe_proposal_create { signerKey }
4. vote FOR / AGAINST              each voter      dexe_proposal_vote_and_execute { signerKey, isVoteFor, autoExecute:false }
5. validator round                 validators      dexe_proposal_vote_and_execute { signerKey, driveValidatorRound:true }
6. execute                         last persona    dexe_proposal_vote_and_execute { signerKey, autoExecute:true }
7. withdraw (unlock)               every voter     dexe_vote_build_withdraw → dexe_tx_send { signerKey }
```

- Deposits before delegations, delegations before the hub votes.
- **`autoExecute:false` for every voter but the last** — otherwise the persona
  that first crosses quorum executes the proposal and your contested vote
  silently becomes a one-vote vote.
- `signerKey` is accepted by `dexe_tx_send`, `dexe_dao_create`,
  `dexe_proposal_create`, `dexe_proposal_vote_and_execute` and the OTC
  composites. **Every `dexe_vote_build_*` / `dexe_proposal_build_*` builder
  returns an unsigned payload** — send it as a persona with `dexe_tx_send`.
- Send builder payloads **verbatim**: raw `vote()` / `delegate()` revert on fresh
  SphereX-era pools, and the builders already emit the required
  `GovPool.multicall([call])` wrapper.
- `signerKey` is hot-key only — WalletConnect mode rejects it.

## 5. Reconcile

**Who did what, and what it cost** — the ledger:

```jsonc
dexe_agents_ledger { "chainId": 97, "windowHours": 24, "limit": 50 }
dexe_agents_ledger { "signerKey": "agent3" }          // one persona
```

One entry per broadcast: `signerKey`, `address`, `chainId`, `tool`, `txHash`,
`outcome` (`broadcast` / `confirmed` / `reverted` / `failed`), `valueWei`,
`gasWei`, `at` — plus per-agent and total spend and the remaining budget. Spend
counts conservatively (in-flight charges the gas *estimate*, a revert charges gas
only, a refused send charges nothing), and that is the number the daily budget is
compared against. Read-only and local: the store is
`~/.dexe-mcp/agent-ledger.json` (`DEXE_AGENT_LEDGER_PATH`), no RPC needed. Keys
never reach it — labels and addresses only, with a scrubber over anything
key-shaped.

**Did the governance outcome land** — the report:

```jsonc
dexe_dao_report { "govPool": "0x…", "chainId": 56, "sections": ["proposals","turnout"] }
```

`turnout` (who voted, with what weight) is subgraph-backed: **BSC mainnet 56
only**. On 97 it returns `available:false` — use `dexe_proposal_state` instead
and say which sections are missing.

Close the run with a per-persona table: `signerKey → address → actions → txs →
spend`, the final proposal state, and the remaining budget.

## Gotchas

- **Locked tokens between rounds.** Voted tokens stay locked per-proposal even
  after execution and `votingPower()` reads 0 — one `dexe_vote_build_withdraw`
  per persona before the next round, or the next vote fails "No voting power
  available".
- **Delegation is one level** — hub-and-spoke, never a chain. A persona delegates
  only its own deposited balance; received delegations cannot be re-delegated.
- **Approve the UserKeeper, never the GovPool.**
- **First proposal on a fresh DAO can revert "low creating power"** — transient;
  re-run the same `dexe_proposal_create` and the landed deposit is skipped.
- **A cast validator vote cannot be cancelled** on fresh pools; top-up re-votes
  are allowed. Warn the persona's owner before it votes.
- **`DEXE_AGENT_LEDGER=off` kills attribution** and the budget's ability to see
  spend. Leave it on for any unattended run.
- **The daily budget is not armed by default on chain 97** (faucet coin has no
  value). Set `SWARM_DAILY_BNB_BUDGET` explicitly to cap testnet too.
- **One persona's transactions are serialized**; distinct personas broadcast in
  parallel. Do not try to parallelize a single persona.

## Related

- `dexe_guide {flow:"agent_team"}` — the machine-readable plan (interview
  questions with risk notes, step order, pitfalls)
- `docs/AGENTS.md` — full reference, env table, safety model
- `dexe_guide {flow:"vote_execute"}` — the validator round in detail
- `docs/SECURITY.md` — the broadcast-guard posture
