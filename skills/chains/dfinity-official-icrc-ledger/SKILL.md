---
name: icrc-ledger
description: "Deploy and interact with ICRC-1/ICRC-2 token ledgers (ICP, ckBTC, ckETH). Covers transfers, balances, approve/transferFrom allowances, fee handling, and ledger deployment. Use when working with ICP transfers, token transfers, balances, ICRC-1, ICRC-2, approve, allowance, or any fungible token on IC. Do NOT use for ckBTC minting or BTC deposit/withdrawal flows — use ckbtc instead."
license: Apache-2.0
compatibility: "icp-cli >= 0.2.2"
metadata:
  title: ICRC Token Ledgers
  category: DeFi
---

# ICRC Ledger Standards

## What This Is
ICRC-1 is the fungible token standard on Internet Computer, defining transfer, balance, and metadata interfaces. ICRC-2 extends it with approve/transferFrom (allowance) mechanics, enabling third-party spending like ERC-20 on Ethereum.

## Prerequisites

- For Motoko: mops with `core = "2.3.1"` in mops.toml
- For Rust: `ic-cdk = "0.19"`, `candid = "0.10"`, `icrc-ledger-types = "0.1"` in Cargo.toml

## Canister IDs

| Token | Ledger Canister ID | Decimals |
|-------|-------------------|----------|
| ICP | `ryjl3-tyaaa-aaaaa-aaaba-cai` | 8 |
| ckBTC | `mxzaz-hqaaa-aaaar-qaada-cai` | 8 |
| ckETH | `ss2fx-dyaaa-aaaar-qacoq-cai` | 18 |

Index canisters (for transaction history):
- ICP Index: `qhbym-qaaaa-aaaaa-aaafq-cai`
- ckBTC Index: `n5wcd-faaaa-aaaar-qaaea-cai`
- ckETH Index: `s3zol-vqaaa-aaaar-qacpa-cai`

All ICRC-1 ledgers expose `icrc1_fee : () -> (nat) query` to return the current transfer fee. Fees are denominated in the token's smallest unit (e8s for ICP where 1 ICP = 10⁸ e8s, satoshis for ckBTC, wei for ckETH). Each ledger sets its own fee, and fees can change at runtime.

## Common Pitfalls

1. **Assuming all ledgers share the same fee** -- Each ledger sets its own fee (e.g., ICP = 10000 e8s, ckBTC = 10 satoshis). Never copy a fee value from one ledger and use it for another. Look up the fee via `icrc1_fee` (on-chain query or `icp canister call <ledger> icrc1_fee '()'` via CLI). Fees can also change at runtime, so always handle `BadFee { expected_fee }` — the ledger tells you the correct fee in the error response.

2. **Forgetting approve before transferFrom** -- ICRC-2 transferFrom will reject with `InsufficientAllowance` if the token owner has not called `icrc2_approve` first. This is a two-step flow: owner approves, then spender calls transferFrom.

3. **Not handling Err variants** -- `icrc1_transfer` returns `Result<Nat, TransferError>`, not just `Nat`. The error variants are: `BadFee`, `BadBurn`, `InsufficientFunds`, `TooOld`, `CreatedInFuture`, `Duplicate`, `TemporarilyUnavailable`, `GenericError`. You must match on every variant or at minimum propagate the error.

4. **Using wrong Account format** -- An ICRC-1 Account is `{ owner: Principal; subaccount: ?Blob }`, NOT just a Principal. The subaccount is a 32-byte blob. Passing null/None for subaccount uses the default subaccount (all zeros).

5. **Omitting created_at_time** -- Without `created_at_time`, you lose deduplication protection. Two identical transfers submitted within 24h will both execute. Set `created_at_time` to `Time.now()` (Motoko) or `ic_cdk::api::time()` (Rust) for dedup.

6. **Hardcoding canister IDs as text** -- Always use `Principal.fromText("ryjl3-tyaaa-aaaaa-aaaba-cai")` (Motoko) or `Principal::from_text("ryjl3-tyaaa-aaaaa-aaaba-cai")` (Rust). Never pass raw strings where a Principal is expected.

7. **Calling ledger from frontend** -- ICRC-1 transfers should originate from a backend canister, not directly from the frontend. Frontend-initiated transfers expose the user to reentrancy and can bypass business logic. Use a backend canister as the intermediary.

8. **Shell substitution in `--argument-file` / `init_args.path`** -- Expressions like `$(icp identity principal)` do NOT expand inside files referenced by `init_args: { path: ... }` or `--argument-file`. The file is read as literal text. Either use `--argument` on the command line (where the shell expands variables), or pre-generate the file with `envsubst` / `sed` before deploying.

9. **Minting account cannot call `icrc2_approve`** -- If the ledger's `minting_account` and `initial_balances` use the same principal, that principal cannot call `icrc2_approve` — the ledger traps with "the minting account cannot delegate mints." Always use a **separate** principal for `minting_account` and different ones for `initial_balances`. In production, the minting account is typically a dedicated minter canister (e.g., the ckBTC minter); for local development, any principal that differs from your funded accounts works.

10. **Transfers to/from the minting account have zero fee** -- A transfer TO the minting account is a **burn**, and a transfer FROM the minting account is a **mint**. Both require `fee = null` (or `fee = ?0`). Passing the regular transfer fee (e.g., `fee = ?10000` for ICP) will fail with `BadFee { expected_fee = 0 }`. The error message gives no indication that burn/mint semantics are involved — it just says the expected fee is 0.


## Implementation

### Motoko

#### Imports and Types

```motoko
import Principal "mo:core/Principal";
import Nat "mo:core/Nat";
import Nat8 "mo:core/Nat8";
import Nat64 "mo:core/Nat64";
import Blob "mo:core/Blob";
import Time "mo:core/Time";
import Int "mo:core/Int";
import Runtime "mo:core/Runtime";
```

#### Define the ICRC-1 Actor Interface

```motoko
persistent actor {

  type Account = {
    owner : Principal;
    subaccount : ?Blob;
  };

  type TransferArg = {
    from_subaccount : ?Blob;
    to : Account;
    amount : Nat;
    fee : ?Nat;
    memo : ?Blob;
    created_at_time : ?Nat64;
  };

  type TransferError = {
    #BadFee : { expected_fee : Nat };
    #BadBurn : { min_burn_amount : Nat };
    #InsufficientFunds : { balance : Nat };
    #TooOld;
    #CreatedInFuture : { ledger_time : Nat64 };
    #Duplicate : { duplicate_of : Nat };
    #TemporarilyUnavailable;
    #GenericError : { error_code : Nat; message : Text };
  };

  type ApproveArg = {
    from_subaccount : ?Blob;
    spender : Account;
    amount : Nat;
    expected_allowance : ?Nat;
    expires_at : ?Nat64;
    fee : ?Nat;
    memo : ?Blob;
    created_at_time : ?Nat64;
  };

  type ApproveError = {
    #BadFee : { expected_fee : Nat };
    #InsufficientFunds : { balance : Nat };
    #AllowanceChanged : { current_allowance : Nat };
    #Expired : { ledger_time : Nat64 };
    #TooOld;
    #CreatedInFuture : { ledger_time : Nat64 };
    #Duplicate : { duplicate_of : Nat };
    #TemporarilyUnavailable;
    #GenericError : { error_code : Nat; message : Text };
  };

  type TransferFromArg = {
    spender_subaccount : ?Blob;
    from : Account;
    to : Account;
    amount : Nat;
    fee : ?Nat;
    memo : ?Blob;
    created_at_time : ?Nat64;
  };

  type TransferFromError = {
    #BadFee : { expected_fee : Nat };
    #BadBurn : { min_burn_amount : Nat };
    #InsufficientFunds : { balance : Nat };
    #InsufficientAllowance : { allowance : Nat };
    #TooOld;
    #CreatedInFuture : { ledger_time : Nat64 };
    #Duplicate : { duplicate_of : Nat };
    #TemporarilyUnavailable;
    #GenericError : { error_code : Nat; message : Text };
  };

  type Value = {
    #Nat : Nat;
    #Int : Int;
    #Text : Text;
    #Blob : Blob;
  };

  // Remote ledger actor reference (ICP ledger shown; swap canister ID for other tokens)
  transient let icpLedger = actor ("ryjl3-tyaaa-aaaaa-aaaba-cai") : actor {
    icrc1_balance_of : shared query (Account) -> async Nat;
    icrc1_transfer : shared (TransferArg) -> async { #Ok : Nat; #Err : TransferError };
    icrc2_approve : shared (ApproveArg) -> async { #Ok : Nat; #Err : ApproveError };
    icrc2_transfer_from : shared (TransferFromArg) -> async { #Ok : Nat; #Err : TransferFromError };
    icrc1_fee : shared query () -> async Nat;
    icrc1_decimals : shared query () -> async Nat8;
    icrc1_metadata : shared query () -> async [(Text, Value)];
    icrc1_supported_standards : shared query () -> async [{ name : Text; url : Text }];
  };

  // Fee for the ICP ledger — look up via icrc1_fee if targeting a different ledger
  transient let icpFee : Nat = 10000;

  // Check balance
  public func getBalance(who : Principal) : async Nat {
    await icpLedger.icrc1_balance_of({
      owner = who;
      subaccount = null;
    })
  };

  // Transfer tokens (this canister sends from its own account)
  // WARNING: Add access control in production — this allows any caller to transfer tokens
  public func sendTokens(to : Principal, amount : Nat) : async Nat {
    let now = Nat64.fromNat(Int.abs(Time.now()));
    let result = await icpLedger.icrc1_transfer({
      from_subaccount = null;
      to = { owner = to; subaccount = null };
      amount = amount;
      fee = ?icpFee;
      memo = null;
      created_at_time = ?now;
    });
    switch (result) {
      case (#Ok(blockIndex)) { blockIndex };
      case (#Err(#InsufficientFunds({ balance }))) {
        Runtime.trap("Insufficient funds. Balance: " # Nat.toText(balance))
      };
      case (#Err(#BadFee({ expected_fee }))) {
        Runtime.trap("Wrong fee. Expected: " # Nat.toText(expected_fee))
      };
      case (#Err(_)) { Runtime.trap("Transfer failed") };
    }
  };

  // ICRC-2: Approve a spender
  public shared ({ caller }) func approveSpender(spender : Principal, amount : Nat) : async Nat {
    // caller is captured at function entry in Motoko -- safe across await
    let now = Nat64.fromNat(Int.abs(Time.now()));
    let result = await icpLedger.icrc2_approve({
      from_subaccount = null;
      spender = { owner = spender; subaccount = null };
      amount = amount;
      expected_allowance = null;
      expires_at = null;
      fee = ?icpFee;
      memo = null;
      created_at_time = ?now;
    });
    switch (result) {
      case (#Ok(blockIndex)) { blockIndex };
      case (#Err(_)) { Runtime.trap("Approve failed") };
    }
  };

  // ICRC-2: Transfer from another account (requires prior approval)
  // WARNING: Add access control in production — this allows any caller to transfer tokens
  public func transferFrom(from : Principal, to : Principal, amount : Nat) : async Nat {
    let now = Nat64.fromNat(Int.abs(Time.now()));
    let result = await icpLedger.icrc2_transfer_from({
      spender_subaccount = null;
      from = { owner = from; subaccount = null };
      to = { owner = to; subaccount = null };
      amount = amount;
      fee = ?icpFee;
      memo = null;
      created_at_time = ?now;
    });
    switch (result) {
      case (#Ok(blockIndex)) { blockIndex };
      case (#Err(#InsufficientAllowance({ allowance }))) {
        Runtime.trap("Insufficient allowance: " # Nat.toText(allowance))
      };
      case (#Err(_)) { Runtime.trap("TransferFrom failed") };
    }
  };
}
```

### Rust

#### Cargo.toml Dependencies

```toml
[package]
name = "icrc_ledger_backend"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
ic-cdk = "0.19"
candid = "0.10"
icrc-ledger-types = "0.1"
serde = { version = "1", features = ["derive"] }
```

#### Complete Implementation

```rust
use candid::{Nat, Principal};
use icrc_ledger_types::icrc1::account::Account;
use icrc_ledger_types::icrc1::transfer::{TransferArg, TransferError};
use icrc_ledger_types::icrc2::approve::{ApproveArgs, ApproveError};
use icrc_ledger_types::icrc2::transfer_from::{TransferFromArgs, TransferFromError};
use ic_cdk::update;
use ic_cdk::call::Call;

const ICP_LEDGER: &str = "ryjl3-tyaaa-aaaaa-aaaba-cai";
// Fee for the ICP ledger — look up via icrc1_fee if targeting a different ledger
const ICP_FEE: u64 = 10_000;

fn ledger_id() -> Principal {
    Principal::from_text(ICP_LEDGER).unwrap()
}

// Check balance
#[update]
async fn get_balance(who: Principal) -> Nat {
    let account = Account {
        owner: who,
        subaccount: None,
    };
    let (balance,): (Nat,) = Call::unbounded_wait(ledger_id(), "icrc1_balance_of")
        .with_arg(account)
        .await
        .expect("Failed to call icrc1_balance_of")
        .candid_tuple()
        .expect("Failed to decode response");
    balance
}

// Transfer tokens from this canister's account
// WARNING: Add access control in production — this allows any caller to transfer tokens
#[update]
async fn send_tokens(to: Principal, amount: Nat) -> Result<Nat, String> {
    let fee = Nat::from(ICP_FEE);
    let transfer_arg = TransferArg {
        from_subaccount: None,
        to: Account {
            owner: to,
            subaccount: None,
        },
        amount,
        fee: Some(fee),
        memo: None,
        created_at_time: Some(ic_cdk::api::time()),
    };

    let (result,): (Result<Nat, TransferError>,) = Call::unbounded_wait(ledger_id(), "icrc1_transfer")
        .with_arg(transfer_arg)
        .await
        .map_err(|e| format!("Call failed: {:?}", e))?
        .candid_tuple()
        .map_err(|e| format!("Decode failed: {:?}", e))?;

    match result {
        Ok(block_index) => Ok(block_index),
        Err(TransferError::InsufficientFunds { balance }) => {
            Err(format!("Insufficient funds. Balance: {}", balance))
        }
        Err(TransferError::BadFee { expected_fee }) => {
            Err(format!("Wrong fee. Expected: {}", expected_fee))
        }
        Err(e) => Err(format!("Transfer error: {:?}", e)),
    }
}

// ICRC-2: Approve a spender
#[update]
async fn approve_spender(spender: Principal, amount: Nat) -> Result<Nat, String> {
    let fee = Nat::from(ICP_FEE);
    let args = ApproveArgs {
        from_subaccount: None,
        spender: Account {
            owner: spender,
            subaccount: None,
        },
        amount,
        expected_allowance: None,
        expires_at: None,
        fee: Some(fee),
        memo: None,
        created_at_time: Some(ic_cdk::api::time()),
    };

    let (result,): (Result<Nat, ApproveError>,) = Call::unbounded_wait(ledger_id(), "icrc2_approve")
        .with_arg(args)
        .await
        .map_err(|e| format!("Call failed: {:?}", e))?
        .candid_tuple()
        .map_err(|e| format!("Decode failed: {:?}", e))?;

    result.map_err(|e| format!("Approve error: {:?}", e))
}

// ICRC-2: Transfer from another account (requires prior approval)
// WARNING: Add access control in production — this allows any caller to transfer tokens
#[update]
async fn transfer_from(from: Principal, to: Principal, amount: Nat) -> Result<Nat, String> {
    let fee = Nat::from(ICP_FEE);
    let args = TransferFromArgs {
        spender_subaccount: None,
        from: Account {
            owner: from,
            subaccount: None,
        },
        to: Account {
            owner: to,
            subaccount: None,
        },
        amount,
        fee: Some(fee),
        memo: None,
        created_at_time: Some(ic_cdk::api::time()),
    };

    let (result,): (Result<Nat, TransferFromError>,) = Call::unbounded_wait(ledger_id(), "icrc2_transfer_from")
        .with_arg(args)
        .await
        .map_err(|e| format!("Call failed: {:?}", e))?
        .candid_tuple()
        .map_err(|e| format!("Decode failed: {:?}", e))?;

    result.map_err(|e| format!("TransferFrom error: {:?}", e))
}
```

## Deploy

Add to `icp.yaml`:

Pin the release version before deploying: get the latest release tag from https://github.com/dfinity/ic/releases?q=%22ledger-suite-icrc%22&expanded=false, then substitute it for `<RELEASE_TAG>` in the URL below.

```yaml
canisters:
  - name: icrc1_ledger
    build:
      steps:
        - type: pre-built
          url: https://github.com/dfinity/ic/releases/download/<RELEASE_TAG>/ic-icrc1-ledger.wasm.gz
    init_args:
      path: icrc1_ledger_init.args
      format: candid
```

Create `icrc1_ledger_init.args`, replacing `YOUR_PRINCIPAL` with the output of `icp identity principal`.

The `minting_account` **must** be a different principal than any principal in `initial_balances` (see pitfall #9). `initial_balances` accepts multiple entries to fund several accounts at genesis.

> **Pitfall:** Shell substitutions like `$(icp identity principal)` will NOT expand inside this file. You must paste the literal principal strings.

```
(variant { Init = record {
  token_symbol = "TEST";
  token_name = "Test Token";
  minting_account = record { owner = principal "MINTER_PRINCIPAL" };
  transfer_fee = 10_000 : nat;
  metadata = vec {};
  initial_balances = vec {
    record {
      record { owner = principal "PRINCIPAL_A" };
      100_000_000_000 : nat;
    };
    record {
      record { owner = principal "PRINCIPAL_B" };
      50_000_000_000 : nat;
    };
  };
  archive_options = record {
    num_blocks_to_archive = 1000 : nat64;
    trigger_threshold = 2000 : nat64;
    controller_id = principal "YOUR_PRINCIPAL";
  };
  feature_flags = opt record { icrc2 = true };
}})
```

Deploy:

```bash
icp network start -d
icp deploy icrc1_ledger
```
