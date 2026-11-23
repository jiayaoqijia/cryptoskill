# Agent-gated NFT mints

Campaigns that cap a mint to a Binance Agent ID (`.ai` handle) rather than an allowlist. Two
shapes: a contract with a `NoHandle`-style gate inside `mint()`, or a protocol that also demands an
off-chain attempt/challenge receipt before the transaction.

## 1. Read the project's own status endpoint first

Most of these sites ship JSON: `/api/status`, `/api/mint-prompt`, `/api/config`. Parse it for
`admission`, `mintPrice`, `maxMintsPerWallet`, `supplyCap`, `paused`, contract addresses and
`marketplaceFeeBps`.

- `admission: closed` / "temporarily paused" → stop. No sign-in signature, no transaction. Report
  the stated reason and the on-chain remaining supply, and say when it is expected to reopen rather
  than retrying.
- A 429 `Service busy` from their MCP/API is rate limiting: back off with jitter and retry. It is
  not the admission answer.
- "Remaining supply" on the site is usually stale — read `totalSupply()` and the cap from the
  contract.

## 2. Verify the wiring before signing

Cheap reads that catch a cloned or decoy deployment:

- non-empty code at the mint contract, NFT and gate
- `mint.nft()` == NFT, `NFT.minter()` == mint contract, gate registry == the registry the prompt names
- `paused()` false, `mintPrice` 0, per-wallet cap matches the site's claim
- supply: `totalSupply()` vs `MAX_SUPPLY`
- fee cap: `eth_estimateGas` × `eth_gasPrice`, converted to the user's currency, compared against
  their stated ceiling before proposing anything

ABIs keyless: Sourcify v2 `https://sourcify.dev/server/v2/contract/56/<addr>?fields=abi` returns
`abi` plus a `signatures` list carrying each 4-byte selector. Compute missing selectors with
pycryptodome keccak, and decode custom errors the same way (`NoHandle(address)` = `0xc3d01ac8`).

## 3. What "free" is actually worth

- **Soulbound** (`locked`, ERC-5192, transfers revert) → zero resale value. The entire follow-up is
  the campaign's social task; say so instead of implying a market.
- **Tradeable** → read the project's marketplace floor, listed count and fee first. A deep listing
  book means "just under floor" can still sit unsold.
- **Challenge receipt** (SAT-style puzzle with fragment reads, tool budget, deadline) is real work:
  size the solver before promising two mints, and treat one attempt as one attempt, not permission
  to retry until it wins.

## 4. Post-mint

- Daily social campaigns: the number in the post is the on-chain token id, read from the contract —
  never from a page preview.
- Listing: use the marketplace contract named in the status payload; price at or just under floor
  and state the fee in the message.
- After the campaign, tell the user to turn Developer Mode back off and leave only gas money in the
  wallet.
