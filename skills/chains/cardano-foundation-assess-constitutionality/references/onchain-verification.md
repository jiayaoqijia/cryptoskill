# On-Chain Verification Steps

This skill makes no network calls. It hands the user the commands, they run them, and the
assessment reasons over what comes back. For a transaction that has not been submitted yet, the
fields read from `proposal_list` below come from the decoded transaction instead; see
`transaction-input.md`. Present a command only when its answer will actually
change a finding, and say which provision it settles.

Endpoint shapes below are taken from the bundled Koios spec at
`../../docs/sources/koios/specs/results/koiosapi-mainnet.yaml`. Read that
spec for response fields, filters, and auth. Koios accepts PostgREST-style query filters on
GET endpoints. Any provider works; Koios is used here because its docs are bundled.

Until a command's output has been supplied, every provision that depends on it is
**Not-yet-verifiable**. Never assume the expected answer.

The commands need `curl`, `jq` and `python3`. Chain data is a point-in-time fact: record the
epoch it was read at, because delegation and balances can change before enactment.

---

## 1. Resolve the action and its anchor

Settles: what is actually being proposed, and Article II.6.1 format and immutability.

`proposal_list` is a GET endpoint returning all governance proposals.

```sh
curl -s "https://api.koios.rest/api/v1/proposal_list?proposal_id=eq.<gov_action_id>" | jq '.[0]'
```

Ask for: `proposal_type`, `proposal_tx_hash`, `meta_url`, `meta_hash`, `meta_json`,
`proposed_epoch`, `expiration`, `return_address`, and for treasury actions `withdrawal`
(each entry's `stake_address` and `amount` in lovelace; the same map is in
`proposal_description.contents[0]`).

Then retrieve the anchor document itself, so the assessment reads what was actually
anchored rather than a copy:

```sh
# IPFS anchor
curl -s "https://ipfs.io/ipfs/<cid>"

# HTTPS anchor
curl -s "<meta_url>"
```

Hash what was retrieved. `b2sum` is not on stock macOS; Python is:

```sh
python3 -c "import hashlib,sys;print(hashlib.blake2b(open(sys.argv[1],'rb').read(),digest_size=32).hexdigest())" anchor.jsonld
```

`cardano-cli hash anchor-data --url <url> --expected-hash <meta_hash>` does the fetch and the
comparison in one step, for HTTPS and `ipfs://` URLs.

Two things to check on the anchor, both bearing on II.6.1:

- Does the retrieved document hash to `meta_hash`? A mismatch means the anchored content is
  not what is being served, which is a finding in its own right.
- Can the URL's content change without the anchor changing? A branch URL can. A content
  addressed CID cannot. An IPNS name has to be resolved before judging it.

---

## 1a. Parameter map, for ParameterChange actions only

Settles: which parameters are actually being changed. Run this before any guardrail analysis.

For a `ParameterChange`, `proposal_description.contents` carries the parameter map as its second
element. That map is authoritative; the proposal's prose is not.

```sh
curl -s "https://api.koios.rest/api/v1/proposal_list?proposal_id=eq.<gov_action_id>" \
  | jq '.[0].proposal_description.contents[1]'
```

Returns the changed parameters and their proposed values, for example:

```json
{
  "minPoolCost": 75000000,
  "maxTxExecutionUnits": { "steps": 10000000000, "memory": 17500000 },
  "maxBlockExecutionUnits": { "steps": 20000000000, "memory": 77500000 }
}
```

Read the map carefully against the narrative, and note both directions of divergence:

- **A parameter in the map that the prose does not discuss.** It still engages PARAM-01, its
  category guardrails, and the Appendix I.2.1 critical tracks. Assess it.
- **A parameter restated at its current value.** Nested parameters make this easy to miss: an
  action changing only `memory` submits the whole `maxTxExecutionUnits` object, carrying `steps`
  along at its existing setting. This effects no change and is ordinarily unremarkable, but say
  so explicitly rather than leaving it unmentioned, because a reader comparing the map to the
  assessment will otherwise think it was overlooked.

A proposal stating that "no other protocol parameters are changed" is describing effect, not
map contents. Both statements can be true at once. Verify rather than infer.

To settle a per-epoch or once-per-two-epochs guardrail such as NETWORK-01, the prior action's
enactment epoch is also needed, alongside this action's `proposed_epoch` and `enacted_epoch`
from the same record.

---

## 2. Withdrawal destination

Settles: Article II.7.6, all three prongs.

```sh
curl -s -X POST "https://api.koios.rest/api/v1/account_info" \
  -H "Content-Type: application/json" \
  -d '{"_stake_addresses":["<destination_stake_address>"]}' | jq '.[0]'
```

Read three fields, and report each separately rather than as one pass or fail:

| Prong | Field | Satisfied when |
|---|---|---|
| Not delegated to a stake pool | `delegated_pool` | `null` |
| Delegated to the predefined abstain option | `delegated_drep` | exactly `drep_always_abstain` |
| Separate, auditable account | `total_balance`, history | a distinct account, not a reused operational one |

On the second prong: any other DRep fails, including one that abstains as a matter of
practice. The Constitution names the predefined option.

For the separate-account prong, the account's history shows whether it is fresh or reused:

```sh
curl -s "https://api.koios.rest/api/v1/account_txs?_stake_address=<destination_stake_address>" | jq 'length, .[0:5]'
```

If the destination is a script credential, `script_info` returns the script, for example an
m-of-n native script and its key hashes, which is the best evidence of who controls the funds:

```sh
curl -s -X POST "https://api.koios.rest/api/v1/script_info" \
  -H "Content-Type: application/json" \
  -d '{"_script_hashes":["<script_hash>"]}' | jq '.[0]'
```

Address type is readable from the bech32 prefix without any query, per CIP-19: `stake17…`
(header `0xf1`) is script-locked, `stake1u…` (header `0xe1`) is key-hash. Report which it is.
On the reading in `interpretive-positions.md`, key-hash custody does not by itself fail
II.7.6.

---

## 3. Administrator evidence

Settles: Article II.7.5 designation and, on the reading in `interpretive-positions.md`, that the
administrator exists at withdrawal. Evidence that the administrator agreed to serve is reported
as an open question; the text requires designation, not agreement.

Existence: when the destination is a script, `script_info` (section 2) shows its keys, and a
transaction signed by them, such as the one that registered and delegated the account, shows
the keyholders acted.

Agreement, two kinds of evidence; check both before reporting that none was found.

**Channel A, a signature on the submission transaction.** Fetch the raw transaction and
compare its vkey witness key hashes (blake2b-224) against keys the administrator is known to
use, established from transactions it indisputably submitted.

```sh
curl -s -X POST "https://api.koios.rest/api/v1/tx_cbor" \
  -H "Content-Type: application/json" \
  -d '{"_tx_hashes":["<tx_hash>"]}' | jq -r '.[0].cbor'
```

This returns CBOR. Decode it as in `transaction-input.md` section 1 and read the vkey
witnesses. Compare their key hashes with the administrator's keys, for example the keys of the
destination's native script from `script_info`.

**Channel B, a CIP-100 author signature on the anchor.** An `authors[].witness` entry naming
the administrator. A public key in the document proves nothing on its own, since anyone can
paste one. The ed25519 signature itself must verify: URDNA2015 canonicalization of the
`{@context, body}` subdocument, blake2b-256 hash, verified against the listed `publicKey`.

An author signature over the very document that designates the administrator is sufficient
even with no transaction witness.

If both kinds of evidence were checked and neither was found, say so in open questions with
what would settle it. If they could not be checked, say that instead. Neither changes the
II.7.5 row, which turns on designation.

---

## 4. Net Change Limit

Settles: whether the withdrawal fits the treasury limit currently in force.

Never hardcode a figure. TREASURY-01a sets the limit through an on-chain action agreed by
DReps with more than 50% of the active voting stake. In practice that is an Info action. Info
actions are never ratified or enacted, so `ratified_epoch` and `enacted_epoch` stay `null` on
them; agreement shows only in the vote tally.

Find the candidate Info actions, then check which reached the threshold:

```sh
curl -s "https://api.koios.rest/api/v1/proposal_list?proposal_type=eq.InfoAction&select=proposal_id,proposed_epoch,expiration,title:meta_json->body->>title&order=proposed_epoch.desc" \
  | jq '[.[] | select((.title // "") | test("net change"; "i"))]'

curl -s "https://api.koios.rest/api/v1/proposal_voting_summary?_proposal_id=<gov_action_id>" \
  | jq '.[0] | {epoch_no, drep_yes_pct}'
```

The title filter is a convenience, not a definition: read the anchor of the action that passed
to get the limit and its epoch window from the document itself. Then sum the
TreasuryWithdrawals enacted inside that window, add this one, and confirm the arithmetic with
the user before relying on it:

```sh
curl -s "https://api.koios.rest/api/v1/proposal_list?proposal_type=eq.TreasuryWithdrawals&enacted_epoch=gte.<A>&enacted_epoch=lte.<B>&select=proposal_id,enacted_epoch,withdrawal" \
  | jq '[.[].withdrawal[].amount | tonumber] | add / 1000000'
```

If more than one approved limit covers the window, follow the Net Change Limit position in
`interpretive-positions.md`.

Compliance here is an affirmation in one sentence, not a section. Report it as a finding only
if the withdrawal actually exceeds the limit.

---

## 5. Refund-style withdrawals

Settles: whether a withdrawal described as a deposit refund really is one.

Before accepting that characterization, confirm the destination equals the original action's
`return_address`, from that action's `proposal_list` record. If it does not match, the
withdrawal is not a refund regardless of how it is described, and the ordinary Article II.7
analysis applies in full.

---

## 6. Constitution currency

Settles: whether the mirrored text is still the enacted Constitution. See `constitution-meta.md` for
the command and how to read its result.
