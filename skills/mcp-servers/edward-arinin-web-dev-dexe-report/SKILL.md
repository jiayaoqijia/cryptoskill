---
name: dexe-report
description: |
  Pull a complete DeXe DAO report in ONE `dexe_dao_report` call — members,
  delegations, treasury, proposals, turnout ("who voted"), experts, validators,
  activity and deadlines — show only what moved with the `since` diff, and put
  it on a schedule with /schedule (cloud cron) or /loop (this session). Use when
  the user says "report", "stats", "activity", "who voted", "how is my DAO
  doing", "weekly digest", "monitor my DAO", "check it every day".
---

# dexe-report

One call answers the standing questions about a DAO. Do **not** hand-assemble a
report from `dexe_read_dao_members` + `dexe_read_treasury` + `dexe_proposal_list`
+ one `dexe_proposal_voters` per proposal — that is the 12-18-call pattern
`dexe_dao_report` exists to replace. Full reference: `docs/REPORTING.md`.

`dexe_dao_report` is in the **default** toolset profile and needs no API key,
no RPC of your own, and no signer. It never broadcasts anything.

## 1. The report call

```jsonc
{ "govPool": "0x…", "chainId": 56 }
```

Eleven sections: `identity`, `settings`, `treasury`, `membership`, `delegation`
(who delegated to whom — no address list needed), `experts`, `validators`,
`proposals`, `turnout` (every proposal at once), `activity`, `deadlines`.

| Param | Default | Use it for |
|---|---|---|
| `sections` | all 11 | Narrow the work: `["deadlines","proposals"]` for a watch. |
| `user` | — | Adds that wallet's unvoted proposals + claimable rewards to `deadlines`. |
| `proposalLimit` | `30` | How many of the newest proposals to walk. |
| `memberLimit` | `50` | Member/delegation rows. |
| `persist` | `true` | Stores the snapshot that `since: "last"` diffs against. |

The text output leads with **NEEDS ATTENTION** and **CHANGES SINCE …**; the rest
is in `structuredContent` (typed by `outputSchema`). Render it the way the user
asked — table, bullet digest, or a one-line verdict.

## 2. The `since` diff

```jsonc
{ "govPool": "0x…", "chainId": 56, "since": "last" }
```

`"last"` diffs against this DAO's previous run — no timestamp bookkeeping.
`changes` carries `newProposals`, `proposalStateChanges`, `membersJoined`,
`membersCountDelta`, `delegationChanges`, `delegationTotalDelta`,
`treasuryDeltas`, `notes`. Explicit anchors also work: ISO-8601, Unix seconds,
`"block:62000000"`.

**`since: "last"` errors on the very first run** (no snapshot stored yet). Run
once without `since`, then use `"last"` from then on — and put that fallback
sentence into every scheduled prompt.

## 3. Scheduling

"Set up a weekly report for my DAO" means one of two things — ask which:

- **`/loop`** — repeats in THIS session, any interval, local MCP server and
  local `.env`. Dies with the session.
- **`/schedule`** — a CLOUD routine: fresh sandbox each run, cron in **UTC**,
  **minimum interval 1 hour**, **no access to the local machine**. The dexe MCP
  server must be attached to the routine, the prompt must be self-contained, and
  the fresh sandbox has no snapshot, so `since: "last"` needs the fallback.

Paste-able daily digest (`/loop`):

```
/loop 24h Call dexe_dao_report {govPool:"0x…", chainId:56, since:"last"}. If it errors because there is no baseline, call it again without `since`. Post a 5-line digest: live deadlines, new proposals, state changes, member/delegation moves, treasury deltas. If nothing changed, say "no change" in one line. Name any section that came back unavailable.
```

Paste-able hourly vote watch (`/loop`):

```
/loop 1h Call dexe_dao_report {govPool:"0x…", chainId:56, user:"0xYourWallet", sections:["deadlines","proposals"]}. Only speak up if deadlines contains an item I have not voted on or something is executable — otherwise reply exactly "clear".
```

The `/schedule` equivalents (with the cron conversion and the routine prompt
written out) are in `docs/REPORTING.md`.

## Gotchas

- **Subgraph sections are BSC mainnet (56) only** — `membership`, `delegation`,
  `turnout`, `activity`, `experts`. On any other chain they come back
  `available: false` with a reason and a `followUp`, listed in `unavailable[]`,
  while the on-chain sections still render. **Always tell the user which
  sections are missing.** Silently reporting half a DAO as the whole DAO is the
  failure mode here.
- **`since: "last"` on a first run is an error, not an empty diff.**
- **`changes.baseline`** tells you the diff quality: `snapshot` (complete),
  `timestampOnly` (only what the indexer can date), `none`.
- **`membersNoLongerInWindow` is window-scoped** — an address can drop out
  because newer members pushed it past `memberLimit`, not because it left.
  `membersCountDelta` is the authoritative sign; the report says so in `notes`.
- **Read-only.** A scheduled report must never be the thing that signs. Do not
  chain it into `dexe_proposal_vote_and_execute` without the user in the loop.
- **Custom questions** the report does not cut: `dexe_graph_query` (also
  default-visible) — but never guess entity or field names (`DaoPool` is queried
  as `daoPools`). Check the `dexe://graph-schema` resource, or call
  `dexe_graph_schema` for live introspection (`read` toolset). Across ALL your
  DAOs: `dexe_user_inbox` (`read` toolset).

## Related

- `dexe_guide {flow:"report_dao_activity"}` — the machine-readable version of
  this recipe.
- `dexe_guide {flow:"read_dao_data"}` — the whole read surface.
- `docs/REPORTING.md`, `docs/GRAPH.md` (also the MCP resource
  `dexe://graph-schema`).
