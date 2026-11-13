---
name: canister-audit
description: "Audit an existing Internet Computer Rust canister (ic-cdk) for security flaws and PROVE a confirmed one with a PocketIC reproduction. Covers detecting the canister, a high-recall static first pass, a systematic review against the canister-security pitfalls, and the distinctive step: building the canister to wasm and executing the exploit in PocketIC to turn a suspected flaw into a demonstrated one. Use when reviewing or auditing a canister you did NOT write, or proving a finding before you report it. Complements canister-security (which teaches the secure patterns); this one finds and proves violations of them."
license: Apache-2.0
compatibility: "a Rust ic-cdk canister repo (ic-cdk >= 0.18); cargo + the wasm32-unknown-unknown target; the pocket-ic crate (16.x) for the proof step, which downloads its matching server; Semgrep and cargo-audit optional"
metadata:
  title: Canister Audit
  category: Security
---

# Canister Audit

## What This Is

A workflow for auditing a Rust `ic-cdk` canister you did not write, and for turning a suspected flaw into a *proven* one. `canister-security` teaches the patterns a canister should follow; this skill is the other side of that coin - given existing code, find where those patterns are violated, and prove the highest-severity finding by reproducing the exploit in PocketIC. A grep hit or a hunch is a *candidate*; a PocketIC test that drives the deployed wasm and crosses the security boundary is *evidence*.

The worked example throughout is a deliberately-broken ledger canister, `token_vault`, whose accounting invariant `sum(balances) <= total_deposited` is broken by exactly one unguarded method.

## Prerequisites

- Rust toolchain + the wasm target: `rustup target add wasm32-unknown-unknown`.
- Optional static tools: `cargo-audit` (RustSec dependency CVEs) and Semgrep (a coarse first pass; Rust support is experimental, so treat it as high-recall).
- For the proof step: the `pocket-ic` crate (e.g. `16.1`). With `POCKET_IC_BIN` unset, `PocketIc::new()` downloads the matching server release from `dfinity/pocketic` on first use. To pin a binary you have verified (sha256) instead, point `POCKET_IC_BIN` at it; the server's major version must match the crate's.

## The audit workflow

1. **Detect the canister.** Confirm it is a Rust ic-cdk canister: a `Cargo.toml` depending on `ic-cdk`/`candid`, `#[ic_cdk::update]`/`#[ic_cdk::query]` entrypoints, a `.did`. A canister's logic is not recoverable from its deployed wasm, so you need the source - there is no audit-by-mainnet-address mode.
2. **Model the invariants first.** Before reading for bugs, write down what must always hold: the accounting identity, who may call what, which state moves across each `await`. The audit then hunts for a path that breaks each invariant. For `token_vault` the invariant is `sum(balances) <= total_deposited`.
3. **Static first pass (high-recall, best-effort).** Grep or Semgrep for the obvious footguns, treating every hit as a candidate to confirm, never an automatic finding:
   - state-changing update fns — `#[update]`, `#[ic_cdk::update]`, with or without arguments (`guard = ...`, `name = ...`), `async` or not — with no caller check (`is_controller`, an owner check, or a `== Principal::anonymous()` rejection). `CallerGuard` is a reentrancy lock, **not** a caller check: it admits the anonymous principal;
   - `fetch_root_key` / `fetchRootKey` / `shouldFetchRootKey` **anywhere** in the repo, including calls behind an environment check (`canister-security` pitfall #7 forbids it even there — environment branches leak into production builds); only test-only code is exempt. The fix to recommend is removing the call and passing the root key from the `ic_env` cookie (`IC_ROOT_KEY`, via `safeGetCanisterEnv()`) as `rootKey` to `HttpAgent.create()`;
   - `let _ = CallerGuard::new(...)` - a guard bound to `_` is dropped at the end of the statement, so the lock is released immediately;
   - `ic_cdk::caller()` - deprecated in favour of `msg_caller()`; legacy call sites often predate the current guard conventions.
   A deliberately high-recall rule flags `deposit`, `withdraw`, *and* `claim_bonus` here, even though `deposit` rejects the anonymous principal and `withdraw` takes a `CallerGuard` - the point is to surface candidates for review, not to decide. Example Semgrep rule (tested with Semgrep 1.185):
   ```yaml
   rules:
     - id: ic-update-missing-caller-auth
       message: update method with no visible caller check - candidate for review
       languages: [rust]
       severity: ERROR
       patterns:
         # Every update entrypoint: bare or parameterized attribute, sync or async.
         - pattern-either:
             - pattern: |
                 #[$ATTR]
                 fn $F(...) { ... }
             - pattern: |
                 #[$ATTR]
                 fn $F(...) -> $R { ... }
             - pattern: |
                 #[$ATTR]
                 async fn $F(...) { ... }
             - pattern: |
                 #[$ATTR]
                 async fn $F(...) -> $R { ... }
             - pattern: |
                 #[$ATTR(...)]
                 fn $F(...) { ... }
             - pattern: |
                 #[$ATTR(...)]
                 fn $F(...) -> $R { ... }
             - pattern: |
                 #[$ATTR(...)]
                 async fn $F(...) { ... }
             - pattern: |
                 #[$ATTR(...)]
                 async fn $F(...) -> $R { ... }
         - metavariable-regex:
             metavariable: $ATTR
             regex: ^(ic_cdk::)?update$
         # A bare `== Principal::anonymous()` is deliberately NOT a suppressor (a
         # comparison that does not reject the caller is not a guard), and neither
         # is CallerGuard (a reentrancy lock). Under-reporting is worse than noise.
         - pattern-not-regex: (is_controller|require_owner|require_admin)
   ```
   The suppression is by name only, so methods it hides are still reviewed in step 4 - it just orders the queue.
4. **Systematic review against the pitfalls.** Walk each entrypoint against the `canister-security` checklist (anonymous principal #2, TOCTOU across `await` #3, unguarded admin #8, storage / cycle-drain DoS #10/#5, callback-trap-after-mutation #11, and the rest). For each candidate, read the code and decide real or refuted. Trace every guard to its body: a `guard = "..."` function or helper proves nothing until you have read it, `require_authenticated`-style guards stop only the anonymous principal (not enough for admin methods), and a guard called as a statement whose `Result` is discarded (`require_owner();`) is a bypass - the mutation runs whether or not it returned `Err`. In `token_vault`, `claim_bonus` credits the caller with no guard and never touches `total_deposited`, so it breaks the invariant and is reachable by the anonymous principal (pitfalls #2 and #8); `deposit`'s `== Principal::anonymous()` check refutes its own candidate.
5. **Prove a confirmed HIGH/CRITICAL with PocketIC** (next section).
6. **Report.** Per finding: the pitfall, the `file:line`, the invariant broken, and - for a proven one - the reproduction. Frame an unproven candidate honestly as "suspected, not reproduced," and never ship a working exploit for an unpatched canister publicly - it belongs in a private report to the canister's controllers.

## Proving a finding with PocketIC

This is the step that separates an audit from a lint. Build the audited canister to wasm, load it into PocketIC, call the suspect method as the attacker (usually `Principal::anonymous()`), and assert the prohibited outcome. If the test passes, the exploit is real.

Keep the reproduction in a **separate, standalone crate** outside the audited repo's workspace, so PocketIC's dev-dependency never touches the target's manifests and your audit leaves the target unmodified. Drive the canister through its built wasm - ic-cdk canister code does not link for the host target.

`token_vault_repro/Cargo.toml`:

```toml
[package]
name = "token_vault_repro"
version = "0.1.0"
edition = "2021"
publish = false

# Empty [workspace] keeps this crate out of any enclosing workspace.
[workspace]

[dev-dependencies]
candid = "0.10"
pocket-ic = "16.1"
```

### 1. The flaw (`token_vault/src/lib.rs`)

```rust
// INTENTIONAL FLAW: credits the caller out of thin air - no anonymous-principal
// rejection, no owner guard, and it never touches total_deposited. Breaks the
// invariant sum(balances) <= total_deposited.
#[ic_cdk::update]
fn claim_bonus(amount: u64) {
    let caller = msg_caller();
    STATE.with(|s| {
        *s.borrow_mut().balances.entry(caller).or_default() += amount;
    });
}
```

### 2. The reproduction (separate `token_vault_repro` crate, `tests/repro.rs`)

```rust
use candid::{decode_one, encode_args, encode_one, Principal};
use pocket_ic::PocketIc;

fn install(pic: &PocketIc) -> Principal {
    let c = pic.create_canister();
    pic.add_cycles(c, 2_000_000_000_000);
    // Must be an absolute path: cargo runs integration tests from this crate's root.
    let path = std::env::var("CANISTER_WASM").expect("set CANISTER_WASM to the built .wasm");
    let wasm = std::fs::read(&path).unwrap_or_else(|e| panic!("read {path}: {e}"));
    pic.install_canister(c, wasm, encode_args(()).unwrap(), None);
    c
}

fn query_u64(pic: &PocketIc, c: Principal, method: &str, arg: Vec<u8>) -> u64 {
    let reply = pic.query_call(c, Principal::anonymous(), method, arg).expect("query rejected");
    decode_one(&reply).expect("reply decodes to u64")
}

#[test]
fn anonymous_principal_mints_unbacked_balance() {
    let pic = PocketIc::new();
    let c = install(&pic);
    let anon = Principal::anonymous();

    // Precondition: an empty ledger.
    assert_eq!(query_u64(&pic, c, "total_deposited", encode_args(()).unwrap()), 0);

    // Attack: the anonymous principal credits itself 1_000 out of thin air.
    pic.update_call(c, anon, "claim_bonus", encode_one(1_000u64).unwrap())
        .expect("claim_bonus is callable by the anonymous principal - that is the bug");

    let bal = query_u64(&pic, c, "balance_of", encode_one(anon).unwrap());
    let total = query_u64(&pic, c, "total_deposited", encode_args(()).unwrap());

    assert_eq!(bal, 1_000, "anonymous principal minted a balance");
    assert!(
        bal > total,
        "INVARIANT BROKEN: sum(balances) {bal} > total_deposited {total} - \
         the ledger records a balance no deposit backs"
    );
}
```

### 3. Run it

```bash
rustup target add wasm32-unknown-unknown
# Build the audited canister in its own repo (no changes to it).
(cd token_vault && cargo build --target wasm32-unknown-unknown --release)
# Run the repro with an ABSOLUTE wasm path - a relative one resolves against
# token_vault_repro/, not the directory you ran this from.
(cd token_vault_repro && \
  CANISTER_WASM="$PWD/../token_vault/target/wasm32-unknown-unknown/release/token_vault.wasm" \
  cargo test --test repro -- --nocapture)
```

If the audited crate is part of a Cargo workspace, its wasm lands in the **workspace** `target/` directory - adjust the path accordingly.

A passing test is the whole point: it proves the anonymous principal can create a balance no deposit backs - the accounting invariant is broken on the deployed wasm. That is the difference between "`claim_bonus` looks unguarded" and "here is the anonymous principal minting a balance." Claim exactly what the test shows: it does **not** by itself prove funds can be stolen. To prove theft, extend the test - fund the vault from an honest principal, have the attacker `claim_bonus` then `withdraw`, and assert the withdrawal succeeds and the honest user's funds can no longer be fully paid out.

## Notes

- The PocketIC server and the `pocket-ic` crate share a major version. Pin both and update the `update_call`/`query_call` signatures together if you bump (the 16.x API returns `Result<Vec<u8>, _>`).
- A clean or failed reproduction does **not** refute the static / review finding. A flaw can be real but awkward to reproduce in a unit test (timing, multi-canister setup); keep the reasoning and record the proof as pending.
- Static hits are candidates, not verdicts. The high-recall ruleset exists to miss nothing obvious; the review and the PocketIC proof are what confirm.
