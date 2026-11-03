# ckETH / ckERC20: custodial backend canister

The canister owns the ck tokens and keeps one 32-byte subaccount per user (`[len, principal bytes, 0-padding]`). Every minter call comes from the canister's principal, so:

- `deposit_erc20` / `deposit_eth` register the address of `(canister, user_subaccount)`. Show the returned `address` to the user and re-call it to re-arm the 24h window.
- For the helper-contract flow, pass the **canister id** as `principal` (bytes32) and the user subaccount as `subaccount`.
- Withdrawals approve the minter from the user's subaccount on the ckETH ledger (gas) and on the ckERC20 ledger (amount), then call `withdraw_erc20` with both `from_*_subaccount` fields.
- The minter guards per principal. Concurrent `withdraw_*`/`deposit_*` calls from this canister are **rejected** (the minter traps with `AlreadyProcessing`), so serialize them or retry. Track per-user balances with `icrc1_balance_of` on `(canister, user_subaccount)`.
- Gate every endpoint on an authenticated caller, and see `canister-security` for reentrancy and async-safety around balances.

## Rust

`Cargo.toml` dependencies: `ic-cdk = "0.19"`, `candid = "0.10"`, `serde = { version = "1", features = ["derive"] }`, `icrc-ledger-types = "0.1"`.

```rust
use candid::{CandidType, Deserialize, Nat, Principal};
use ic_cdk::call::Call;
use ic_cdk::update;
use icrc_ledger_types::icrc1::account::{Account, Subaccount};
use icrc_ledger_types::icrc2::approve::{ApproveArgs, ApproveError};

const CKETH_MINTER: &str = "sv3dd-oaaaa-aaaar-qacoa-cai";
const CKETH_LEDGER: &str = "ss2fx-dyaaa-aaaar-qacoq-cai";

// ---- minter types (subset of the minter's Candid interface) ----
#[derive(CandidType, Deserialize)]
enum DepositMode { Unsponsored { subaccount: Option<Subaccount> } }

#[derive(CandidType, Deserialize)]
struct DepositErc20Arg { erc20_contract_address: String, mode: DepositMode }

#[derive(CandidType, Deserialize, Debug)]
struct CkErc20Token { ckerc20_token_symbol: String, erc20_contract_address: String, ledger_canister_id: Principal }

#[derive(CandidType, Deserialize, Debug)]
struct DetectedDeposit { erc20_contract_address: String, scanned_balance: Nat, detected_at_block: Nat }

#[derive(CandidType, Deserialize, Debug)]
enum DepositStatus {
    Scanning { valid_until: u64, last_scanned_block: Option<Nat>, scan_count: u64 },
    AwaitingSweep(DetectedDeposit),
}

#[derive(CandidType, Deserialize, Debug)]
struct DepositErc20Response { address: String, minimum_deposit_amount: Nat, status: DepositStatus }

#[derive(CandidType, Deserialize, Debug)]
enum DepositErc20Error {
    TokenNotSupported { supported_tokens: Vec<CkErc20Token> },
    TooManyTokensForAccount,
    TooManyActiveDeposits,
    TemporarilyUnavailable(String),
}

#[derive(CandidType, Deserialize)]
struct WithdrawErc20Arg {
    amount: Nat,
    ckerc20_ledger_id: Principal,
    recipient: String,
    from_cketh_subaccount: Option<Subaccount>,
    from_ckerc20_subaccount: Option<Subaccount>,
}

#[derive(CandidType, Deserialize, Debug)]
struct RetrieveErc20Request { cketh_block_index: Nat, ckerc20_block_index: Nat }

#[derive(CandidType, Deserialize, Debug)]
enum LedgerError {
    InsufficientFunds { balance: Nat, failed_burn_amount: Nat, token_symbol: String, ledger_id: Principal },
    InsufficientAllowance { allowance: Nat, failed_burn_amount: Nat, token_symbol: String, ledger_id: Principal },
    AmountTooLow { minimum_burn_amount: Nat, failed_burn_amount: Nat, token_symbol: String, ledger_id: Principal },
    TemporarilyUnavailable(String),
}

#[derive(CandidType, Deserialize, Debug)]
enum WithdrawErc20Error {
    TokenNotSupported { supported_tokens: Vec<CkErc20Token> },
    RecipientAddressBlocked { address: String },
    CkEthLedgerError { error: LedgerError },
    CkErc20LedgerError { cketh_block_index: Nat, error: LedgerError },
    TemporarilyUnavailable(String),
}

#[derive(CandidType, Deserialize)]
struct Eip1559TransactionPriceArg { ckerc20_ledger_id: Principal }

#[derive(CandidType, Deserialize, Debug)]
struct Eip1559TransactionPrice {
    gas_limit: Nat,
    max_fee_per_gas: Nat,
    max_priority_fee_per_gas: Nat,
    max_transaction_fee: Nat,
    timestamp: Option<u64>,
}

fn minter() -> Principal { Principal::from_text(CKETH_MINTER).unwrap() }

/// One subaccount per user of this canister: [len, principal bytes, 0-padding].
fn user_subaccount(user: &Principal) -> Subaccount {
    let bytes = user.as_slice();
    let mut sub = [0u8; 32];
    sub[0] = bytes.len() as u8;
    sub[1..1 + bytes.len()].copy_from_slice(bytes);
    sub
}

fn caller_not_anonymous() -> Principal {
    let caller = ic_cdk::api::msg_caller();
    assert_ne!(caller, Principal::anonymous(), "Authentication required");
    caller
}

/// Deposit address for (this canister, user subaccount). ckERC20 is minted to that account.
/// Call again (e.g. on every page load) to re-arm the 24h scanning window and to read the status.
#[update]
async fn erc20_deposit_address(erc20_contract_address: String) -> Result<DepositErc20Response, String> {
    let user = caller_not_anonymous();
    let arg = DepositErc20Arg {
        erc20_contract_address,
        mode: DepositMode::Unsponsored {
            subaccount: Some(user_subaccount(&user)),
        },
    };
    let (res,): (Result<DepositErc20Response, DepositErc20Error>,) =
        Call::unbounded_wait(minter(), "deposit_erc20")
            .with_arg(arg)
            .await
            .map_err(|e| format!("deposit_erc20 rejected: {e:?}"))? // traps (e.g. malformed address) surface here
            .candid_tuple()
            .map_err(|e| format!("decode: {e:?}"))?;
    res.map_err(|e| format!("{e:?}"))
}

async fn approve(ledger: Principal, from: Subaccount, amount: Nat) -> Result<(), String> {
    let args = ApproveArgs {
        from_subaccount: Some(from),
        spender: Account { owner: minter(), subaccount: None },
        amount,
        expected_allowance: None,
        expires_at: None,
        fee: None,
        memo: None,
        created_at_time: Some(ic_cdk::api::time()),
    };
    let (res,): (Result<Nat, ApproveError>,) = Call::unbounded_wait(ledger, "icrc2_approve")
        .with_arg(args)
        .await
        .map_err(|e| format!("{e:?}"))?
        .candid_tuple()
        .map_err(|e| format!("{e:?}"))?;
    res.map(|_| ()).map_err(|e| format!("approve failed: {e:?}"))
}

/// Withdraw ckERC20 held in the caller's subaccount of this canister to an Ethereum address.
/// The same subaccount must also hold enough ckETH to pay the Ethereum gas.
#[update]
async fn withdraw_erc20(ckerc20_ledger_id: Principal, recipient: String, amount: Nat) -> Result<RetrieveErc20Request, String> {
    let user = caller_not_anonymous();
    let sub = user_subaccount(&user);

    let (price,): (Eip1559TransactionPrice,) = Call::unbounded_wait(minter(), "eip_1559_transaction_price")
        .with_arg(Some(Eip1559TransactionPriceArg { ckerc20_ledger_id }))
        .await
        .map_err(|e| format!("{e:?}"))?
        .candid_tuple()
        .map_err(|e| format!("{e:?}"))?;
    let gas_allowance = price.max_transaction_fee.clone() + price.max_transaction_fee / 2u32; // +50% margin

    approve(Principal::from_text(CKETH_LEDGER).unwrap(), sub, gas_allowance).await?;
    approve(ckerc20_ledger_id, sub, amount.clone()).await?;

    let arg = WithdrawErc20Arg {
        amount,
        ckerc20_ledger_id,
        recipient,
        from_cketh_subaccount: Some(sub),
        from_ckerc20_subaccount: Some(sub),
    };
    let (res,): (Result<RetrieveErc20Request, WithdrawErc20Error>,) =
        Call::unbounded_wait(minter(), "withdraw_erc20")
            .with_arg(arg)
            .await
            .map_err(|e| format!("withdraw_erc20 rejected: {e:?}"))?
            .candid_tuple()
            .map_err(|e| format!("{e:?}"))?;
    res.map_err(|e| format!("{e:?}"))
}

ic_cdk::export_candid!();
```

## Motoko

`mops.toml`: `core = "2.0.0"` or newer (checked against mo:core 2.7).

```motoko
import Principal "mo:core/Principal";
import Array "mo:core/Array";
import Blob "mo:core/Blob";
import Nat "mo:core/Nat";
import Nat8 "mo:core/Nat8";
import Int "mo:core/Int";
import Time "mo:core/Time";
import Runtime "mo:core/Runtime";

persistent actor Self {

  type Account = { owner : Principal; subaccount : ?Blob };
  type CkErc20Token = { ckerc20_token_symbol : Text; erc20_contract_address : Text; ledger_canister_id : Principal };

  type DepositMode = { #Unsponsored : { subaccount : ?Blob } };
  type DepositStatus = {
    #Scanning : { valid_until : Nat64; last_scanned_block : ?Nat; scan_count : Nat64 };
    #AwaitingSweep : { erc20_contract_address : Text; scanned_balance : Nat; detected_at_block : Nat };
  };
  type DepositErc20Response = { address : Text; minimum_deposit_amount : Nat; status : DepositStatus };
  type DepositErc20Error = {
    #TokenNotSupported : { supported_tokens : [CkErc20Token] };
    #TooManyTokensForAccount;
    #TooManyActiveDeposits;
    #TemporarilyUnavailable : Text;
  };

  type LedgerError = {
    #InsufficientFunds : { balance : Nat; failed_burn_amount : Nat; token_symbol : Text; ledger_id : Principal };
    #InsufficientAllowance : { allowance : Nat; failed_burn_amount : Nat; token_symbol : Text; ledger_id : Principal };
    #AmountTooLow : { minimum_burn_amount : Nat; failed_burn_amount : Nat; token_symbol : Text; ledger_id : Principal };
    #TemporarilyUnavailable : Text;
  };
  type WithdrawErc20Arg = {
    amount : Nat;
    ckerc20_ledger_id : Principal;
    recipient : Text;
    from_cketh_subaccount : ?Blob;
    from_ckerc20_subaccount : ?Blob;
  };
  type WithdrawErc20Error = {
    #TokenNotSupported : { supported_tokens : [CkErc20Token] };
    #RecipientAddressBlocked : { address : Text };
    #CkEthLedgerError : { error : LedgerError };
    #CkErc20LedgerError : { cketh_block_index : Nat; error : LedgerError };
    #TemporarilyUnavailable : Text;
  };
  type Eip1559TransactionPrice = {
    gas_limit : Nat;
    max_fee_per_gas : Nat;
    max_priority_fee_per_gas : Nat;
    max_transaction_fee : Nat;
    timestamp : ?Nat64;
  };

  type ApproveArgs = {
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
  type Ledger = actor { icrc2_approve : shared ApproveArgs -> async { #Ok : Nat; #Err : ApproveError } };

  transient let MINTER = "sv3dd-oaaaa-aaaar-qacoa-cai";
  transient let minter : actor {
    deposit_erc20 : shared { erc20_contract_address : Text; mode : DepositMode } -> async { #Ok : DepositErc20Response; #Err : DepositErc20Error };
    withdraw_erc20 : shared WithdrawErc20Arg -> async { #Ok : { cketh_block_index : Nat; ckerc20_block_index : Nat }; #Err : WithdrawErc20Error };
    eip_1559_transaction_price : shared query ?{ ckerc20_ledger_id : Principal } -> async Eip1559TransactionPrice;
  } = actor (MINTER);
  transient let ckethLedger : Ledger = actor "ss2fx-dyaaa-aaaar-qacoq-cai";

  // One 32-byte subaccount per user: [len, principal bytes, 0-padding].
  func userSubaccount(p : Principal) : Blob {
    let bytes = p.toBlob().toArray();
    Array.tabulate<Nat8>(32, func(i) {
      if (i == 0) { Nat.toNat8(bytes.size()) } else if (i <= bytes.size()) { bytes[i - 1] } else { 0 }
    }).toBlob()
  };

  func requireUser(caller : Principal) {
    if (caller.isAnonymous()) { Runtime.trap("Authentication required") };
  };

  // Deposit address of (this canister, caller's subaccount). Re-call to re-arm the 24h window / read status.
  public shared ({ caller }) func erc20DepositAddress(erc20 : Text) : async { #Ok : DepositErc20Response; #Err : DepositErc20Error } {
    requireUser(caller);
    await minter.deposit_erc20({ erc20_contract_address = erc20; mode = #Unsponsored({ subaccount = ?userSubaccount(caller) }) })
  };

  func approve(ledger : Ledger, from : Blob, amount : Nat) : async () {
    let res = await ledger.icrc2_approve({
      from_subaccount = ?from;
      spender = { owner = Principal.fromText(MINTER); subaccount = null };
      amount;
      expected_allowance = null;
      expires_at = null;
      fee = null;
      memo = null;
      created_at_time = ?Int.abs(Time.now()).toNat64();
    });
    switch res { case (#Err(_)) { Runtime.trap("icrc2_approve failed") }; case (#Ok(_)) {} };
  };

  // Withdraw ckERC20 from the caller's subaccount; the same subaccount must hold ckETH for gas.
  public shared ({ caller }) func withdrawErc20(ckerc20Ledger : Principal, recipient : Text, amount : Nat) : async { #Ok : { cketh_block_index : Nat; ckerc20_block_index : Nat }; #Err : WithdrawErc20Error } {
    requireUser(caller);
    let sub = userSubaccount(caller);
    let price = await minter.eip_1559_transaction_price(?{ ckerc20_ledger_id = ckerc20Ledger });
    await approve(ckethLedger, sub, price.max_transaction_fee * 3 / 2); // +50% margin
    let tokenLedger : Ledger = actor (ckerc20Ledger.toText());
    await approve(tokenLedger, sub, amount);
    await minter.withdraw_erc20({
      amount;
      ckerc20_ledger_id = ckerc20Ledger;
      recipient;
      from_cketh_subaccount = ?sub;
      from_ckerc20_subaccount = ?sub;
    })
  };
};
```
