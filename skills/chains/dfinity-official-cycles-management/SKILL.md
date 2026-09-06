---
name: cycles-management
description: "Manage cycles and canister lifecycle. Covers cycle balance checks, top-ups, freezing thresholds, canister creation, and ICP-to-cycles conversion via the CMC. Use when working with cycles, canister funding, freezing threshold, frozen canister, out of cycles, top-up, canister creation, or cycle balance. Do NOT use for wallet-to-dApp integration or ICRC signer flows — use wallet-integration instead."
license: Apache-2.0
compatibility: "icp-cli >= 0.2.2"
metadata:
  title: Cycles Management
  category: Infrastructure
---

# Cycles & Canister Management

## What This Is
Cycles are the computation fuel for canisters on Internet Computer. Every canister operation (execution, storage, messaging) burns cycles. When a canister runs out of cycles, it freezes and is eventually uninstalled -- its code and data are deleted, but its metadata (canister ID, controllers, settings) survives. 1 trillion cycles (1T) costs approximately 1 USD equivalent in ICP (the exact rate is set by the NNS and fluctuates with ICP price via the CMC).

**Note:** icp-cli uses the **cycles ledger** (`um5iw-rqaaa-aaaaq-qaaba-cai`) by default. The cycles ledger is a single canister that tracks cycle balances for all principals, similar to a token ledger. Commands like `icp cycles balance`, `icp cycles mint`, and `icp canister top-up` go through the cycles ledger. There is no legacy wallet concept in icp-cli. The programmatic patterns below (accepting cycles, creating canisters via management canister) remain the same regardless of which funding mechanism is used.

## Prerequisites

- For Motoko: `mops` package manager, `core = "2.0.0"` in mops.toml
- For Rust: `ic-cdk >= 0.19`

## Canister IDs

| Service | Canister ID | Purpose |
|---------|------------|---------|
| Cycles Minting Canister (CMC) | `rkp4c-7iaaa-aaaaa-aaaca-cai` | Converts ICP to cycles, creates canisters |
| Cycles Ledger | `um5iw-rqaaa-aaaaq-qaaba-cai` | Tracks cycle balances for all principals |
| Management Canister | `aaaaa-aa` | Canister lifecycle (create, install, stop, delete, status) |

The Management Canister (`aaaaa-aa`) is a virtual canister -- it does not exist on a specific subnet but is handled by every subnet's execution layer.

## Mistakes That Break Your Build

1. **Running out of cycles silently freezes the canister** -- There is no warning. A frozen canister stops executing messages but keeps paying rent for its memory and allocations, so the balance continues to drain. When it reaches zero the canister is uninstalled: code and data are gone permanently, and only the metadata (canister ID, controllers, settings) remains. Set a freezing threshold and monitor balances.

2. **Not setting freezing_threshold** -- Default is 30 days. If your canister burns cycles fast (high traffic, large stable memory), 30 days may not be enough warning. Set it higher for production canisters. The freezing threshold defines how many seconds worth of idle cycles the canister must retain before it freezes.

3. **Confusing local vs mainnet cycles** -- Local replicas give canisters virtually unlimited cycles. Code that works locally may fail on mainnet because the canister has insufficient cycles. Always test with realistic cycle amounts before mainnet deployment.

4. **Sending cycles to the wrong canister** -- Cycles sent to a canister cannot be retrieved. There is no refund mechanism for cycles transferred to the wrong principal. Double-check the canister ID before topping up.

5. **Forgetting to set the canister controller** -- If you lose the controller identity, you permanently lose the ability to upgrade, top up, or manage the canister. Always add a backup controller. Use `icp canister settings update --add-controller PRINCIPAL` to add one.

6. **Using ExperimentalCycles in mo:core** -- In mo:core 2.0, the module is renamed to `Cycles`. `import ExperimentalCycles "mo:base/ExperimentalCycles"` will fail. Use `import Cycles "mo:core/Cycles"`.

7. **Using `icp cycles transfer` to fund a canister** -- `icp cycles transfer <amount> <principal>` moves cycles between cycles-ledger balances, the same as a token transfer between accounts. Passing a canister's principal as the recipient credits that principal's cycles-ledger balance, not the canister's actual execution/compute cycle balance -- `icp canister status` will not show the cycles as received, and the canister keeps burning down its real balance toward freezing with no indication anything went wrong. Use `icp canister top-up <canister> --amount <N> -e ic` instead, which deposits cycles directly onto the canister via the management canister. See "Top Up a Canister" below for both commands side by side.

8. **Using `-n ic` on a command that names a canister** -- `-n`/`--network` and `-e`/`--environment` are different selectors and conflict with each other; passing both is an error. A canister **name** can only be resolved through an environment, so `-n` fails on it:

   ```bash
   icp canister status backend -n ic
   # Error: Specifying a network is not supported if you are targeting a canister
   # by name, specify an environment instead
   ```

   So `-e ic` for anything naming a canister (`top-up`, `status`, `settings update`, `create`), and `-n ic` for commands that take a principal or no canister at all (`cycles mint`, `cycles balance`, `cycles transfer`). This is why the mainnet examples below mix the two flags. Load `icp-cli` for the full flag rules.

## Implementation

### Motoko

#### Checking and Accepting Cycles

```motoko
import Cycles "mo:core/Cycles";
import Principal "mo:core/Principal";
import Runtime "mo:core/Runtime";

persistent actor {

  // Check this canister's cycle balance
  public query func getBalance() : async Nat {
    Cycles.balance()
  };

  // Accept cycles sent with a call (for "tip jar" or payment patterns)
  public func deposit() : async Nat {
    let available = Cycles.available();
    if (available == 0) {
      Runtime.trap("No cycles sent with this call")
    };
    let accepted = Cycles.accept<system>(available);
    accepted
  };

  // Send cycles to another canister via inter-canister call
  public func topUpCanister(target : Principal) : async () {
    let targetActor = actor (Principal.toText(target)) : actor {
      deposit_cycles : shared () -> async ();
    };
    // Attach 1T cycles to the call
    await (with cycles = 1_000_000_000_000) targetActor.deposit_cycles();
  };
}
```

#### Creating a Canister Programmatically

```motoko
import Principal "mo:core/Principal";

persistent actor Self {

  type CanisterId = { canister_id : Principal };

  type CreateCanisterSettings = {
    controllers : ?[Principal];
    compute_allocation : ?Nat;
    memory_allocation : ?Nat;
    freezing_threshold : ?Nat;
  };

  // Management canister interface
  let ic = actor ("aaaaa-aa") : actor {
    create_canister : shared { settings : ?CreateCanisterSettings } ->
      async CanisterId;
    canister_status : shared { canister_id : Principal } ->
      async {
        status : { #running; #stopping; #stopped };
        memory_size : Nat;
        cycles : Nat;
        settings : CreateCanisterSettings;
        module_hash : ?Blob;
      };
    deposit_cycles : shared { canister_id : Principal } -> async ();
    stop_canister : shared { canister_id : Principal } -> async ();
    delete_canister : shared { canister_id : Principal } -> async ();
  };

  // Create a new canister with 1T cycles
  public func createNewCanister() : async Principal {
    let result = await (with cycles = 1_000_000_000_000) ic.create_canister({
      settings = ?{
        controllers = ?[Principal.fromActor(Self)];
        compute_allocation = null;
        memory_allocation = null;
        freezing_threshold = ?2_592_000; // 30 days in seconds
      };
    });
    result.canister_id
  };

  // Check a canister's status and cycle balance
  public func checkStatus(canisterId : Principal) : async Nat {
    let status = await ic.canister_status({ canister_id = canisterId });
    status.cycles
  };

  // Top up another canister
  public func topUp(canisterId : Principal, amount : Nat) : async () {
    await (with cycles = amount) ic.deposit_cycles({ canister_id = canisterId });
  };
}
```

### Rust

#### Checking Balance and Accepting Cycles

```rust
use ic_cdk::{query, update};
use candid::Nat;

#[query]
fn get_balance() -> Nat {
    Nat::from(ic_cdk::api::canister_cycle_balance())
}

#[update]
fn deposit() -> Nat {
    let available = ic_cdk::api::msg_cycles_available();
    if available == 0 {
        ic_cdk::trap("No cycles sent with this call");
    }
    let accepted = ic_cdk::api::msg_cycles_accept(available);
    Nat::from(accepted)
}
```

#### Creating and Managing Canisters

```rust
use candid::{Nat, Principal};
use ic_cdk::update;
use ic_cdk::management_canister::{
    create_canister_with_extra_cycles, canister_status, deposit_cycles, stop_canister, delete_canister,
    CreateCanisterArgs, CanisterStatusArgs, DepositCyclesArgs, StopCanisterArgs, DeleteCanisterArgs,
    CanisterSettings, CanisterStatusResult,
};

#[update]
async fn create_new_canister() -> Principal {
    let caller = ic_cdk::api::canister_self(); // capture canister's own principal
    let user = ic_cdk::api::msg_caller(); // capture caller before await

    let settings = CanisterSettings {
        controllers: Some(vec![caller, user]),
        compute_allocation: None,
        memory_allocation: None,
        freezing_threshold: Some(Nat::from(2_592_000u64)), // 30 days
        reserved_cycles_limit: None,
        log_visibility: None,
        wasm_memory_limit: None,
        wasm_memory_threshold: None,
        environment_variables: None,
    };

    let arg = CreateCanisterArgs {
        settings: Some(settings),
    };

    // Send 1T cycles with the create call
    let result = create_canister_with_extra_cycles(&arg, 1_000_000_000_000u128)
        .await
        .expect("Failed to create canister");

    result.canister_id
}

#[update]
async fn check_status(canister_id: Principal) -> CanisterStatusResult {
    canister_status(&CanisterStatusArgs { canister_id })
        .await
        .expect("Failed to get canister status")
}

#[update]
async fn top_up(canister_id: Principal, amount: u128) {
    deposit_cycles(&DepositCyclesArgs { canister_id }, amount)
        .await
        .expect("Failed to deposit cycles");
}

#[update]
async fn stop_and_delete(canister_id: Principal) {
    stop_canister(&StopCanisterArgs { canister_id })
        .await
        .expect("Failed to stop canister");

    delete_canister(&DeleteCanisterArgs { canister_id })
        .await
        .expect("Failed to delete canister");
}
```

## Deploy & Test

### Check Cycle Balance

```bash
# Check your canister's cycle balance
icp canister status backend
# Look for "Balance:" line in output

# Check balance on mainnet
icp canister status backend -e ic

# Check any canister by ID
icp canister status ryjl3-tyaaa-aaaaa-aaaba-cai -e ic
```

### Top Up a Canister

```bash
# Top up with cycles from the cycles ledger (local)
icp canister top-up backend --amount 1000000000000
# Adds 1T cycles to the backend canister

# Top up on mainnet
icp canister top-up backend --amount 1000000000000 -e ic

# Convert ICP to cycles and top up in one step (mainnet)
icp cycles mint --icp 1.0 -n ic   # no canister argument, so -n is fine (see Pitfall 8)
icp canister top-up backend --amount 1000000000000 -e ic
```

```bash
# CORRECT -- funds the canister's execution balance:
icp canister top-up backend --amount 600b -e ic

# WRONG -- sends to the recipient's cycles-ledger balance, canister cannot use it:
icp cycles transfer 600000000000 <canister-principal> -n ic
```

`--amount` on `icp canister top-up` accepts `k`/`m`/`b`/`t` suffixes (thousand/million/billion/trillion).

### Create a Canister via icp

```bash
# Create an empty canister (local)
icp canister create my_canister

# Create on mainnet with specific cycles
icp canister create my_canister -e ic --cycles 2000000000000

# Add a backup controller
icp canister settings update my_canister --add-controller BACKUP_PRINCIPAL_HERE
```

### Set Freezing Threshold

```bash
# Set freezing threshold to 90 days (in seconds: 90 * 24 * 60 * 60 = 7776000)
icp canister settings update backend --freezing-threshold 7776000

# Mainnet
icp canister settings update backend --freezing-threshold 7776000 -e ic
```

## Verify It Works

```bash
# Deploy and check status
icp network start -d
icp deploy backend
icp canister status backend
# Expected output includes:
#   Status: Running
#   Balance: 3_100_000_000_000 Cycles (local default, varies)
#   Freezing threshold: 2_592_000

# Check balance programmatically (if you added getBalance)
icp canister call backend getBalance '()'
# Expected: a large nat value, e.g. (3_100_000_000_000 : nat)

# On mainnet: verify cycles balance is not zero
icp canister status backend -e ic
# If Balance shows 0, the canister will freeze. Top up immediately.
```
