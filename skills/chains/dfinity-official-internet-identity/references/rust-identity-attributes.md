# Rust backend for identity attributes

The `identity-attributes` crate is the Rust side of the `mo:identity-attributes` Motoko package: the same checks, the same environment variables, and the same Candid types, so one frontend works against either backend.

```toml
[dependencies]
candid = "0.10"
ic-cdk = "0.20.1"
identity-attributes = "0.1"
```

```yaml
canisters:
  - name: backend
    settings:
      environment_variables:
        trusted_attribute_signers: "rdmx6-jaaaa-aaaaa-aaadq-cai"  # required
        frontend_origins: "https://your-app.icp.net"              # required, comma-separated
        trusted_sso_domains: "acme.com"                           # optional, comma-separated; omit to reject all sso: keys
```

`#[identity_attributes]` marks the function that receives the caller and their verified attributes, called only for a bundle that passes every check, and adds `_internet_identity_sign_in_start` and `_internet_identity_sign_in_finish`. The function cannot be `async` or generic:

```rust
use candid::Principal;
use ic_cdk::query;
use identity_attributes::{identity_attributes, IdentityAttributes};
use std::cell::RefCell;
use std::collections::BTreeMap;

thread_local! {
    // On the heap to keep the example short: an upgrade clears it.
    static PROFILES: RefCell<BTreeMap<Principal, IdentityAttributes>> =
        const { RefCell::new(BTreeMap::new()) };
}

#[identity_attributes]
fn on_verified(caller: Principal, attributes: IdentityAttributes) {
    PROFILES.with_borrow_mut(|profiles| profiles.insert(caller, attributes));
}

#[query]
fn get_profile(user_id: Principal) -> Option<IdentityAttributes> {
    PROFILES.with_borrow(|profiles| profiles.get(&user_id).cloned())
}

ic_cdk::export_candid!();
```

`IdentityAttributes` is `{ name: Option<String>, email: Option<String>, sso: Option<String> }`:

- `email` comes from `verified_email` (or `openid:<provider>:verified_email`), and for an SSO sign-in from `sso:<domain>:email`. The unverified `email` key of other sources is never read.
- `sso` is the organization's domain when the values came from `sso:` keys, and `None` otherwise.

What the finish method checks, in order, and the `err` it returns:

| Check | Error |
|---|---|
| A bundle is attached | `NoAttributes` |
| It decodes to an ICRC-3 `Value::Map` | `MalformedCandid` |
| `frontend_origins` is set | `FrontendOriginsNotConfigured` |
| `implicit:origin` is one of `frontend_origins` | `FrontendOriginMismatch { expected, got }` |
| `implicit:issued_at_timestamp_ns` is at most five minutes old | `Stale { ageNs }` |
| `implicit:nonce` was issued here and not consumed | `UnknownNonce` |
| A required implicit field is present | `MissingField` |
| Every `sso:<domain>:*` key's domain is trusted | `UntrustedSsoSource { domain }` |
| Name and email come from `sso:` keys or from others, never both | `MixedSsoSources { ssoKeys, otherKeys }` |
| Each field comes from one key, and `sso:` keys from one domain | `AmbiguousAttribute { field, sources }` |

The result is Candid `variant { ok; err : Error }`, so the frontend checks `"err" in result`. A call carrying a bundle traps when `trusted_attribute_signers` is unset or does not list the bundle's signer.

Nonces are kept on the heap, so an upgrade clears them and a sign-in in flight fails with `UnknownNonce` and starts again. A nonce expires after five minutes, and at most 4096 are held, the oldest evicted first.

`identity_attributes::sign_in_start()` and `identity_attributes::sign_in_finish(on_verified)` are the functions behind the two methods, for a canister that defines them itself.
