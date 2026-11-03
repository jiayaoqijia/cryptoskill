---
name: cketh
description: "Integrate ckETH and ckERC20 tokens (ckUSDC, ckUSDT, ckEURC, ckWBTC, ckLINK, ...) into an IC app. Covers discovering supported ckERC20 tokens, converting ETH/ERC-20 to ckETH/ckERC20 via per-account deposit addresses (deposit_eth / deposit_erc20, works from exchanges) or the helper smart contract (depositEth / depositErc20), withdrawing with withdraw_eth / withdraw_erc20, address derivation, fees, minimums, and which calls belong in the frontend vs the backend. Use when the user mentions ckETH, ckERC20, ckUSDC, ckUSDT, or depositing/withdrawing ETH or ERC-20 tokens to/from ICP. Do NOT use for plain ICRC-1 transfers of ck tokens (use icrc-ledger) or for signing arbitrary Ethereum transactions from a canister (use evm-rpc)."
license: Apache-2.0
compatibility: "icp-cli >= 0.2.2, Node.js >= 22 for frontend code"
metadata:
  title: ckETH and ckERC20 (chain-key Ethereum)
  category: DeFi
---

# ckETH and ckERC20 Integration

## What This Is

ckETH (1:1 ETH) and ckERC20 tokens (1:1 ERC-20, e.g. ckUSDC) are ICRC-1/ICRC-2 tokens on ICP. **One minter canister handles ETH and every ERC-20.** It holds the Ethereum funds at addresses derived from its threshold-ECDSA key, talks to Ethereum through the EVM RPC canister, mints after a deposit is final on Ethereum, and burns via an ICRC-2 allowance before it sends a withdrawal. Every ckERC20 token has its own ledger and index. Gas for ERC-20 withdrawals is paid in **ckETH**.

Plain transfers between ICP accounts are ordinary ICRC-1 calls: load `icrc-ledger` for those. This skill covers conversion and token discovery.

## Canister IDs and Ethereum addresses

| | Ethereum Mainnet | Sepolia testnet |
|---|---|---|
| Minter (ETH + all ckERC20) | `sv3dd-oaaaa-aaaar-qacoa-cai` | `jzenf-aiaaa-aaaar-qaa7q-cai` |
| ckETH ledger | `ss2fx-dyaaa-aaaar-qacoq-cai` (ckETH) | `apia6-jaaaa-aaaar-qabma-cai` (ckSepoliaETH) |
| ckETH index | `s3zol-vqaaa-aaaar-qacpa-cai` | `sh5u2-cqaaa-aaaar-qacna-cai` |
| ckERC20 ledger suite orchestrator | `vxkom-oyaaa-aaaar-qafda-cai` | `2s5qh-7aaaa-aaaar-qadya-cai` |
| Helper contract (`deposit_with_subaccount_helper_contract_address`) | `0x18901044688D3756C35Ed2b36D93e6a5B8e00E68` | `0x2D39863d30716aaf2B7fFFd85Dd03Dda2BFC2E38` |
| Minter main address (holds funds, sends withdrawals) | `0xb25eA1D493B49a1DeD42aC5B1208cC618f9A9B80` | `0x1789F79e95324A47c5Fd6693071188e82E9a3558` |

The minter, ckETH and every ckERC20 ledger live on the fiduciary subnet. Read Ethereum addresses at runtime from `get_minter_info` (they change on upgrades); the table is a snapshot from 2026-11.

## Discovering ckERC20 tokens

The **minter** decides which tokens can be deposited and withdrawn. Read `get_minter_info` (query):

- `supported_ckerc20_tokens: opt vec record { ckerc20_token_symbol; erc20_contract_address; ledger_canister_id }`. This is the authoritative list.
- `minimum_deposit_amounts: opt vec record { erc20_contract_address; minimum_deposit_amount }` and `minimum_eth_deposit_amount`. These apply only to the deposit-address flow.
- `minimum_withdrawal_amount` (ckETH, in wei), `cketh_ledger_id`, `deposit_with_subaccount_helper_contract_address`.

For each ledger, read `icrc1_metadata` for `icrc1:decimals`, `icrc1:fee` and `icrc1:logo`. **Decimals differ per token** (ckETH 18, ckUSDC 6, ckWBTC 8). For the index canister id use the orchestrator: `get_orchestrator_info` (`managed_canisters[].{erc20_contract, ledger, index, archives}`) or `canister_ids(record { chain_id = 1; address = "0x..." })`.

Mainnet tokens on 2026-11-02: ckUSDC `xevnm-gaaaa-aaaar-qafnq-cai` (6 decimals), ckUSDT `cngnf-vqaaa-aaaar-qag4q-cai` (6), ckEURC `pe5t5-diaaa-aaaar-qahwa-cai` (6), ckXAUT `nza5v-qaaaa-aaaar-qahzq-cai` (6), ckWBTC `bptq2-faaaa-aaaar-qagxq-cai` (8), ckWSTETH `j2tuh-yqaaa-aaaar-qahcq-cai` (18), ckLINK `g4tto-rqaaa-aaaar-qageq-cai` (18), ckUNI `ilzky-ayaaa-aaaar-qahha-cai` (18), ckSHIB `fxffn-xiaaa-aaaar-qagoa-cai` (18), ckPEPE `etik7-oiaaa-aaaar-qagia-cai` (18), ckOCT `ebo5g-cyaaa-aaaar-qagla-cai` (18), ckBAT `j7x7x-syaaa-aaaar-qcbea-cai` (18). On Sepolia, only ckSepoliaUSDC `yfumr-cyaaa-aaaar-qaela-cai` (Sepolia USDC `0x1c7D4B196Cb0C7B01d743Fbc6116a902379C7238`) is supported. New tokens are added by NNS proposal, so never hardcode the list.

## Account model: who calls the minter

The minter credits and debits ICRC accounts `{ owner; subaccount }`. Choose one of two models:

- **Non-custodial (frontend calls the minter directly).** The user's identity (Internet Identity, or an ICRC signer: see `internet-identity` / `wallet-integration`) calls `deposit_erc20`/`deposit_eth`, `icrc2_approve` and `withdraw_*`. The tokens belong to the user's own principal. This needs no backend.
- **Custodial (your canister calls the minter).** The canister is the owner and keeps one 32-byte subaccount per user. All calls come from the canister's principal (see [references/backend.md](references/backend.md)).

`deposit_erc20` and `deposit_eth` have **no `owner` argument**: the account is always `caller + subaccount`. A backend cannot register a deposit address for a user-owned account. Only the owner can arm its own address.

## Deposit flow A: per-account deposit address (recommended)

Works from any wallet **and from centralized exchanges**, because it needs only a plain transfer to an address. It has been live on mainnet since 2026-09 for ERC-20 and ETH.

1. **Register.** The owner calls `deposit_erc20(record { erc20_contract_address = "0x…"; mode = variant { Unsponsored = record { subaccount = opt <32 bytes> | null } } })` or `deposit_eth(record { mode = … })`. These are update calls, free, and idempotent. The response is `{ address; minimum_deposit_amount; status }`.
2. **Send.** The user sends the ERC-20 (a plain `transfer`) or ETH to `address`, **on Ethereum L1 only**. Several transfers add up, because the minter reads the address' total balance.
3. **Detect.** The minter scans the registered `(address, asset)` pair for **24 h**: at 30 s, 30 s, 60 s, 2 min, … then hourly. A balance ≥ `minimum_deposit_amount` moves the status from `Scanning { valid_until; last_scanned_block; scan_count }` to `AwaitingSweep { scanned_balance; detected_at_block; … }`.
4. **Sweep and mint.** The minter signs a one-time EIP-7702 delegation of the deposit address to the sweeper contract plus an attestation of `(principal, subaccount)`. It then sweeps the funds through the helper contract to its main address. The sweep emits `ReceivedEthOrErc20`, and the minter mints the **full swept amount** once that block is finalized, typically about 20 min. The sweep gas is paid by the minter, not the user.
5. **Re-arm.** Call `deposit_*` again whenever the user returns, or to poll status. After the window expires, or after a sweep, the next call re-arms the pair for 24 h. Funds that arrived while the pair was not armed are not lost: they are detected after re-arming.

**How the address is computed.** It uses non-hardened derivation from the minter's tECDSA secp256k1 `key_1` with path `[minter canister id bytes, [0x01], owner principal bytes, 32-byte subaccount (all zeros for the default)]`, and the address is `keccak256(uncompressed pubkey)[12..]`. It is one address per account, shared by ETH and every ERC-20, and stable across calls. You can derive it offline (`deriveEthDepositAddress` in [references/frontend.md](references/frontend.md)) to display or verify it, but only a `deposit_*` call arms scanning.

Limits: at most 5 assets armed per account (`TooManyTokensForAccount`), and a global cap (`TooManyActiveDeposits`). A `minimum_deposit_amount` of `2^256-1` means deposits are unavailable for that token. On mainnet on 2026-11-02 the minimum was 0.005 ETH, 10 USDC/USDT and 8 EURC.

## Deposit flow B: helper smart contract (Ethereum wallet signs)

The user's Ethereum wallet (MetaMask etc.) calls the helper contract. Funds move straight to the minter's main address, and the contract emits `ReceivedEthOrErc20(address indexed erc20ContractAddress, address indexed owner, uint256 amount, bytes32 indexed principal, bytes32 subaccount)`. The minter scrapes these logs and mints after finalization, about 20 min. No IC call is needed.

```solidity
function depositEth(bytes32 principal, bytes32 subaccount) payable
function depositErc20(address erc20Address, uint256 amount, bytes32 principal, bytes32 subaccount) // after ERC20.approve(helper, amount)
```

- **principal → bytes32**: `[len(principal bytes)] ++ principal bytes ++ zero padding` to 32 bytes, hex with a `0x` prefix. Use `encodePrincipalToEthAddress(principal)` from `@icp-sdk/canisters/cketh`. The name is misleading: it returns bytes32, not an address.
- **subaccount → bytes32**: the 32 raw bytes, or 32 zero bytes for the default account.
- ETH sent to `depositEth` emits the event with `erc20ContractAddress = 0x0`.

## Withdrawal: ckETH → ETH

1. `icrc2_approve` on the ckETH ledger, with spender = the minter and amount ≥ the withdrawal amount. Burns are fee-free, but the approve itself costs the 0.000002 ckETH ledger fee.
2. `withdraw_eth(record { recipient = "0x…"; amount = <wei>; from_subaccount = opt … })` returns `Ok { block_index }`, the ckETH burn index, which doubles as the **withdrawal id**.
3. The minter sends an EIP-1559 transfer with a **21,000 gas limit**, usually within about 6 min. The recipient receives `amount − max_transaction_fee`. The estimate comes from `eip_1559_transaction_price(null)`, and the unspent part is not refunded. The minimum is `minimum_withdrawal_amount`: 0.005 ETH on mainnet since 2026-05 (older docs say 0.03).

## Withdrawal: ckERC20 → ERC-20

1. `eip_1559_transaction_price(opt record { ckerc20_ledger_id = <ledger> })` returns `max_transaction_fee` in wei, using a 65,000 gas limit.
2. `icrc2_approve` on the **ckETH** ledger for at least `max_transaction_fee` plus a margin, because the minter re-estimates at call time.
3. `icrc2_approve` on the **ckERC20** ledger for at least `amount`.
4. `withdraw_erc20(record { amount; ckerc20_ledger_id; recipient; from_cketh_subaccount = opt …; from_ckerc20_subaccount = opt … })` returns `Ok { cketh_block_index; ckerc20_block_index }`. `cketh_block_index` is the withdrawal id.
5. The recipient receives the **full** `amount` in ERC-20, and the gas is burned from ckETH. If the ckERC20 burn fails (`CkErc20LedgerError`), the ckETH burn is reimbursed minus the ckETH ledger fee.

**Tracking either withdrawal:** call `withdrawal_status(variant { ByWithdrawalId = <id> })` (query; also `BySenderAccount`, `ByRecipient`). The status goes `Pending → TxCreated → TxSent { transaction_hash } → TxFinalized (Success | Reimbursed | PendingReimbursement)`. For ckETH, `retrieve_eth_status(block_index)` also works.

## Mistakes That Break Your Build

1. **Hardcoding the token list or helper address.** Read `supported_ckerc20_tokens` and `deposit_with_subaccount_helper_contract_address` from `get_minter_info`. `smart_contract_address`, `eth_helper_contract_address` and `erc20_helper_contract_address` are the **legacy** helpers: ETH-only or without subaccount. Do not build on them.
2. **Depositing an unsupported ERC-20.** The helper contract has no whitelist: an unsupported token is transferred to the minter and never minted. Check the token against `supported_ckerc20_tokens` first. In flow A, an unsupported token sent to a deposit address is not credited either.
3. **Sending to the wrong place.** ETH or tokens sent directly to the minter's main address are not attributed to anyone. Deposit addresses work on **Ethereum L1 only**: transfers on Arbitrum, Base, BSC, etc. to the same address are not credited. Mainnet and Sepolia use different helpers and minters.
4. **Expecting the backend to arm a user's deposit address.** `deposit_erc20`/`deposit_eth` credit `caller + subaccount`. In a non-custodial app the **frontend** must call it with the user's identity. The anonymous principal traps.
5. **Treating the deposit address as "fire and forget" forever.** Scanning lasts 24 h per registration. Call `deposit_*` again when the user comes back. A balance below `minimum_deposit_amount` is never swept until it is topped up.
6. **Using `u64` for amounts.** Wei amounts exceed `u64` above about 18.4 ETH, and many 18-decimal tokens overflow too. Use `Nat` (Rust `candid::Nat`, TS `bigint`). Always scale by the ledger's `icrc1_decimals`.
7. **Forgetting ckETH for ckERC20 withdrawals.** A user holding only ckUSDC cannot withdraw. They need ckETH ≥ `max_transaction_fee` plus margin, **and** an approval on the ckETH ledger. Each approve costs that ledger's fee: 0.000002 ckETH, or 0.01 ckUSDC/ckUSDT.
8. **Approving the wrong ledger or spender.** The spender is always the **minter** (`sv3dd-…`), never the ledger or the helper contract. An ERC-20 withdrawal needs two approvals on two ledgers.
9. **Withdrawing ETH to a contract.** `withdraw_eth` uses 21,000 gas, so contract recipients with non-trivial `receive()` logic fail. The zero address traps, and blocklisted addresses return `RecipientAddressBlocked`.
10. **Concurrent minter calls from one principal.** `withdraw_*`, `deposit_erc20` and `deposit_eth` take a per-principal guard and **trap** (the call is rejected) on `AlreadyProcessing`, `TooManyConcurrentRequests` or `TooManyPendingRequests`. A custodial canister acts as a single principal for all users, so serialize its minter calls and retry rejected calls.
11. **USDT approve.** USDT reverts on changing a non-zero allowance to another non-zero value. Approve 0 first (helper flow only).
12. **Leaving `created_at_time` unset on retries.** Approvals from canisters should set `created_at_time` so that retries deduplicate (see `icrc-ledger`).

## Implementation: frontend (TypeScript)

`@icp-sdk/canisters/cketh` (v4) wraps `withdrawEth`, `withdrawErc20`, `getMinterInfo` and `eip1559TransactionPrice`, but **not** `deposit_erc20`/`deposit_eth`/`withdrawal_status`. Generate bindings from the deployed interface instead:

```bash
npm i @icp-sdk/core@^6 @icp-sdk/canisters@^4 @dfinity/utils@^5 viem@^2 @dfinity/ic-pub-key@^1
icp canister metadata sv3dd-oaaaa-aaaar-qacoa-cai candid:service -n ic > cketh_minter.did
npx @icp-sdk/bindgen --did-file ./cketh_minter.did --out-dir ./src/bindings
```

The generated wrapper uses `{ __kind__: "Variant", Variant: … }` for variants and `field?: T` for `opt`.

The complete module is in [references/frontend.md](references/frontend.md). It covers `listCkErc20Tokens`, `getErc20DepositAddress`/`getEthDepositAddress` (flow A), `deriveEthDepositAddress` (offline), `depositViaHelper` (flow B with viem, including the USDT approve reset), `withdrawEth`, `withdrawErc20` and `withdrawalStatus`. Its core calls:

```typescript
const res = await minter.deposit_erc20({ erc20_contract_address: usdc, mode: { __kind__: "Unsponsored", Unsponsored: { subaccount } } });
const price = await minter.eip_1559_transaction_price({ ckerc20_ledger_id: ckUsdcLedger });
await ckEthLedger.approve({ spender: { owner: minterId, subaccount: [] }, amount: (price.max_transaction_fee * 3n) / 2n });
await ckUsdcLedger.approve({ spender: { owner: minterId, subaccount: [] }, amount });
const w = await minter.withdraw_erc20({ ckerc20_ledger_id: ckUsdcLedger, recipient, amount });
```

Detect a completed deposit by polling `icrc1_balance_of` on the token's ledger, or the index canister's `get_account_transactions`. Mints carry a CBOR memo that `decode_ledger_memo` on the minter decodes into `Convert { from_address; tx_hash; log_index }`.

## Implementation: backend (custodial, Rust and Motoko)

See [references/backend.md](references/backend.md). It has per-user subaccounts, `deposit_erc20` called by the canister (owner = canister), and `withdraw_erc20` with both approvals from the user's subaccount. Both the Rust and the Motoko versions are complete.

A backend does not need the EVM RPC canister. Only if the **canister itself** must sign the helper-contract deposit on Ethereum, load `evm-rpc`.

## Verify It Works

```bash
# Minter config: supported tokens, helper address, minimums
icp canister call sv3dd-oaaaa-aaaar-qacoa-cai get_minter_info '()' -n ic --query

# Register/inspect a deposit address on Sepolia (caller = your identity)
icp canister call jzenf-aiaaa-aaaar-qaa7q-cai deposit_eth \
  '(record { mode = variant { Unsponsored = record { subaccount = null } } })' -n ic
# Expected: (variant { Ok = record { address = "0x..."; minimum_deposit_amount = 5_000_000_000_000_000 : nat; status = variant { Scanning = record { ... } } } })

# Gas a ckUSDC withdrawal would burn (wei of ckETH)
icp canister call sv3dd-oaaaa-aaaar-qacoa-cai eip_1559_transaction_price \
  '(opt record { ckerc20_ledger_id = principal "xevnm-gaaaa-aaaar-qafnq-cai" })' -n ic --query

# Withdrawal status by id (ckETH burn index)
icp canister call sv3dd-oaaaa-aaaar-qacoa-cai withdrawal_status '(variant { ByWithdrawalId = 12345 : nat64 })' -n ic --query

# Balance on a ckERC20 ledger
icp canister call xevnm-gaaaa-aaaar-qafnq-cai icrc1_balance_of '(record { owner = principal "YOUR-PRINCIPAL"; subaccount = null })' -n ic
```
