# Reading Canister Environment Variables at Runtime

`icp deploy` injects `PUBLIC_CANISTER_ID:<canister-name>` for every canister in the environment into every canister's settings (SKILL.md § Canister Environment Variables). Reading them from canister code:

## Motoko

Requires motoko-core v2.1.0+. `Runtime.envVar` needs the `<system>` capability and returns `?Text`. The capability does not cross an ordinary `func` boundary, so a helper that calls it must itself be declared `<system>` and be called with `<system>` from a context that holds the capability (actor init or an update method body):

```motoko
import Runtime "mo:core/Runtime";
import Principal "mo:core/Principal";

// note the `<system>` on the function — a plain `func` cannot call Runtime.envVar
func bridgePrincipal<system>() : ?Principal {
  switch (Runtime.envVar<system>("PUBLIC_CANISTER_ID:bridge")) {
    case (?id) { ?Principal.fromText(id) };
    case null { null };
  };
};

// call site inside an update method, propagating the capability:
// let bridge = bridgePrincipal<system>();
```

A `query` cannot obtain the `<system>` capability, so it cannot read the variable directly. To expose a resolved ID through a query method, mirror it into a `transient var` during a call that can read it (actor init or an update method) and have the query return the cached value.

## Rust

```rust
let id = ic_cdk::api::env_var_value("PUBLIC_CANISTER_ID:other_canister");
```

## Read lazily, not at init

Read the variable at call time rather than caching it during canister initialization:

- **First install:** a sibling canister may not exist yet when this canister initializes; the variable is present once the full `icp deploy` completes.
- **Reinstall:** a pointer stored in canister state (e.g. via a setter method) is wiped by `--mode reinstall`, while the automatic variables are re-stamped with the correct IDs on every deploy — lazy reads self-heal.
