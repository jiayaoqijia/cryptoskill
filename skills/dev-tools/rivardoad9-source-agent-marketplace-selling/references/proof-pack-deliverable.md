# Selling evidence, not opinions — the proof-pack deliverable

Marketplace buyers cannot verify a claim, so they pay for the one thing they *can* check. That is the whole
wedge of a verification listing: every delivery ships machine-readable proof the buyer can re-run.

## Deliverable shape

Three artifacts, always the same:

1. `report.pdf` — one to two pages a human reads: headline numbers in tables, then the raw appendix.
2. `evidence.json` — every request and its raw hex response, the block, and the RPC host used.
3. `bundleSha256` — hash over a canonical subset of `evidence.json` (`sort_keys=True`,
   `separators=(",",":")`, volatile fields like timestamps excluded). Printed in the PDF header. This is what
   makes "you cannot edit the report after the fact" true instead of a slogan.

Two sections in the PDF are non-negotiable and are what buyers quote back:

- **How to verify yourself** — copy-pasteable `curl` for at least one check, with the note that the full request
  set is in the JSON. Evidence that needs a proprietary tool to confirm is not evidence.
- **Limits** — state at block N, on-chain only, no exchange balances, no off-chain reputation, proxy contracts
  read as the proxy. Overclaiming is the fastest way to lose a dispute.

## Generator

`~/.hermes/scripts/onchain_proof_pack.py` (Python stdlib + reportlab; no keys, read-only RPC):

```bash
python3 ~/.hermes/scripts/onchain_proof_pack.py --chain bsc \
  --address 0x<wallet> --name "Label" \
  --token 0x<erc20>:SYMBOL --token 0x<erc721>:NFT \
  --contract 0x<addr>:Label --pair 0x<lp>:Label --tx 0x<hash>
```

Outputs to `~/.hermes/data/proof_pack/<label>-<timestamp>/` and prints dir, PDF size, bundle hash, block, and
what it decoded — read that print before attaching anything to an order.

Checks implemented: chainId + latest block (anchor with hash and timestamp), native balance, ERC-20/721
`balanceOf` + `decimals`, contract code size + `totalSupply`/`owner`/`paused` when present, LP `getReserves` +
`token0`/`token1`, and transaction receipts (`status`, block, gasUsed, log count). Public RPCs cycle per chain
(`bsc`, `base`, `eth`) so a single dead endpoint does not fail the run.

Extend it by adding to the `SEL` selector map and one `add(...)` call — keep the same `{check, method, target,
raw, decoded, rpc}` shape so the appendix stays uniform.

## Delivery discipline

- **Run it at order time.** A bundle is a state read at one block; a stale bundle is a false claim. The hash and
  block in the PDF must be from the run that answers that order.
- **One wallet per order**, quote extra contracts/tokens as an add-on rather than silently truncating.
- **Sample on the listing** = page 1 of a real report rendered to PNG, never a mock-up. Use the seller's own
  wallet/contracts so the sample is reproducible.
- If a check reverts or returns `0x`, record it as a failed check in the appendix instead of dropping it — the
  absence is itself information, and a silently missing row looks like tampering.

## Listing copy that converts

Title: outcome + differentiator (`On-chain Proof Pack - verified state + re-runnable evidence`).
Description order: what you get → what you can use it to settle → scope (chains, per-order limits) → limits stated
up front → delivery format and language. Buyers of verification work read the limits section first; hiding them
reads as a red flag.
