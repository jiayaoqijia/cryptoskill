---
name: internet-identity-attributes
description: "Trust a signed-in user's verified email, display name or organization SSO domain in a canister, rather than only their principal. Internet Identity signs an attribute bundle alongside the delegation, and the backend verifies the signer, the frontend origin and a nonce it issued itself before believing any of it. Use when a canister must know something about the caller beyond their principal, when gating access or an allowlist on an address the user provably controls, when showing a name the user never typed into your app, or when the backend rejects a bundle the frontend has just obtained. Covers the frontend request, scoping attributes to the account signed in with, and the identity-attributes library for Motoko and Rust. Assumes sign-in already works: load internet-identity first. Do NOT use for the sign-in flow itself, for an email address the user typed in (that is ordinary app input, which II has not checked), or for an agent or CLI acting as a user (agent-web-identity)."
license: Apache-2.0
compatibility: "moc >= 1.6.0, ic-cdk >= 0.20.1"
metadata:
  title: Internet Identity Attributes
  category: Auth
---

# Internet Identity Attributes

## Prerequisites

This skill assumes a working sign-in built with `@icp-sdk/auth`: load the `internet-identity` skill first. The attribute bundle travels alongside a delegation, so there is nothing here to request without one.

The `frontend_origins` value configured below must be the origin identities are derived for, the **primary origin** where the app has pinned one, not the origin the user happens to be visiting. A suite gets this wrong by default.

- For the Motoko backend: `mo:identity-attributes` >= 0.4.0 (mops), the mixin that injects the two sign-in methods and verifies the attribute bundle. It pulls in `mo:core` >= 2.5.0 and requires `moc` >= 1.6.0 for `include`.
- For the Rust backend: the `identity-attributes` crate and `ic-cdk` >= 0.20.1.

## Identity attributes

When the backend needs more than the principal (e.g. a verified email), II returns a signed attribute bundle alongside the delegation. The backend exposes two methods: `_internet_identity_sign_in_start` issues a nonce, `_internet_identity_sign_in_finish` verifies the bundle. The `identity-attributes` library adds both: the `mo:identity-attributes` mixin in Motoko, and the `#[identity_attributes]` attribute in Rust (see "Backend: Rust" below). Both return the same Candid types, so the frontend is the same against either.

## Keys

`requestAttributes({ keys, nonce })` requires both; there is no default key set.

| Key | Meaning | Use for |
|---|---|---|
| `name` | Display name from the user's II-linked account | Personalisation |
| `email` | Raw address from the II-linked account; **II does not check it** | Contact info, mailing lists |
| `verified_email` | Present only when II established the user controls the address (an OpenID provider marked it verified, or the user verified it with II) | Access gating; the only email to authorise on |

Request both `email` and `verified_email` for fallback: when verified, both carry the same value; otherwise only `email` arrives.

`scopedKeys` scopes keys to the account the user signs in with, so they are shared in the same step with no extra prompt:

| Call | Keys | Default `keys` |
|---|---|---|
| `scopedKeys({ openIdProvider: 'google' })` | `openid:https://accounts.google.com:<key>` | `name`, `email`, `verified_email` |
| `scopedKeys({ openIdProvider: 'apple' })` | `openid:https://appleid.apple.com:<key>` | same |
| `scopedKeys({ openIdProvider: 'microsoft' })` | `openid:https://login.microsoftonline.com/{tid}/v2.0:<key>` (`{tid}` literal) | same |
| `scopedKeys({ ssoDomain: 'acme.com' })` | `sso:acme.com:<key>` | `name`, `email` (no `verified_email`) |

Pass `keys` to narrow, e.g. `scopedKeys({ openIdProvider: 'google', keys: ['name', 'verified_email'] })`.

## Frontend

```javascript
import { AuthClient } from "@icp-sdk/auth/client";
import { AttributesIdentity } from "@icp-sdk/core/identity";
import { HttpAgent, Actor } from "@icp-sdk/core/agent";
import { safeGetCanisterEnv } from "@icp-sdk/core/agent/canister-env";
import { Principal } from "@icp-sdk/core/principal";

const II_PRINCIPAL = "rdmx6-jaaaa-aaaaa-aaadq-cai";
const rootKey = safeGetCanisterEnv()?.IC_ROOT_KEY;

async function signInWithAttributes(authClient, canisterId, idl) {
  // Anonymous handle, used only to ask for the nonce.
  const anonymousActor = Actor.createActor(idl, { agent: await HttpAgent.create({ rootKey }), canisterId });

  // In parallel, one interaction for the user. `nonce` is a function the client
  // calls when it needs the value, so the request is in flight while II opens.
  const signInPromise = authClient.signIn();
  const attributesPromise = authClient.requestAttributes({
    keys: ["name", "verified_email"],
    nonce: () => anonymousActor._internet_identity_sign_in_start(),
  });

  const identity = await signInPromise;
  const attributes = await attributesPromise;

  // The bundle travels as sender_info on each call made with this identity.
  const verifiedAgent = await HttpAgent.create({
    identity: new AttributesIdentity({
      inner: identity,
      attributes,
      signer: { canisterId: Principal.fromText(II_PRINCIPAL) },
    }),
    rootKey,
  });
  const verifiedActor = Actor.createActor(idl, { agent: verifiedAgent, canisterId });

  const result = await verifiedActor._internet_identity_sign_in_finish();
  if ("err" in result) {
    throw new Error(`Attribute verification failed: ${JSON.stringify(result.err)}`);
  }
  return identity;
}
```

For one-click sign-in, build the client with `openIdProvider` or `ssoDomain`, add `scopedKeys` to the `@icp-sdk/auth/client` import, and request `scopedKeys({ openIdProvider: "google", keys: ["name", "verified_email"] })` or `scopedKeys({ ssoDomain: "acme.com" })` instead; the rest is unchanged.

Every bundle carries three implicit fields the backend MUST verify: `implicit:nonce` (one it issued and has not consumed), `implicit:origin` (a trusted frontend origin), `implicit:issued_at_timestamp_ns` (fresh, typically within five minutes).

## Backend: Motoko

```toml
[dependencies]
identity-attributes = "0.4.1"
core                = "2.5.0"

[toolchain]
moc = "1.6.0"
```

`include IdentityAttributes({ onVerified })` injects both methods and runs `onVerified` only on a bundle that passes the signer, origin, nonce, and freshness checks. It resolves the bundle to `{ name : ?Text; email : ?Text; sso : ?Text }`:

- OpenID and unscoped sources: `email` comes from `verified_email` (or `openid:<provider>:verified_email`), which is why the frontend requests `verified_email`.
- SSO sources: `name` and `email` come from `sso:<domain>:name` / `sso:<domain>:email`, accepted only for a domain in `trusted_sso_domains`, and `sso` is that domain. Otherwise `sso` is `null`.

```motoko
import IdentityAttributes "mo:identity-attributes";
import Map "mo:core/Map";
import Principal "mo:core/Principal";

persistent actor {
  type Profile = { name : ?Text; email : ?Text; sso : ?Text };

  let profiles = Map.empty<Principal, Profile>();

  include IdentityAttributes({
    onVerified = func(caller, attrs) {
      profiles.add(caller, attrs);
    };
  });

  public query func getProfile(userId : Principal) : async ?Profile {
    profiles.get(userId)
  };
};
```

```yaml
canisters:
  - name: backend
    settings:
      environment_variables:
        # Required. A local II (`ii: true`) has the same principal.
        trusted_attribute_signers: "rdmx6-jaaaa-aaaaa-aaadq-cai"
        # Required, comma-separated. The origin identities are DERIVED for.
        frontend_origins: "https://your-app.icp.net"
        # Optional, comma-separated; omit to reject all sso:* keys.
        trusted_sso_domains: "your-org.com"
```

Unset `trusted_attribute_signers` rejects every bundle as untrusted; unset `frontend_origins` makes `_internet_identity_sign_in_finish` return `#err(#FrontendOriginsNotConfigured)`. The error variants (`#NoAttributes`, `#MalformedCandid`, `#FrontendOriginMismatch`, `#Stale`, `#UnknownNonce`, `#AmbiguousAttribute`, `#UntrustedSsoSource`, `#MixedSsoSources`) tell the frontend whether to retry with a fresh nonce or surface a bug.

## Backend: Rust

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

A nonce does not survive an upgrade: a sign-in that was in flight across one fails with `UnknownNonce`, and the frontend's remedy is to start again from `_internet_identity_sign_in_start`. The same error answers a nonce older than five minutes, or one already spent. Treat `UnknownNonce` as "retry with a fresh nonce" rather than as a bug.

`identity_attributes::sign_in_start()` and `identity_attributes::sign_in_finish(on_verified)` are the functions behind the two methods, for a canister that defines them itself.

## Mistakes That Break Your Build

1. **Generating the attribute nonce on the frontend.** The nonce passed to `requestAttributes` MUST come from the backend (`_internet_identity_sign_in_start`), or the canister cannot check that the bundle's `implicit:nonce` is one it issued, and replay protection is gone.
2. **Reading attribute data without verifying the signer.** The IC verifies the signature, not who signed: any canister can produce a valid bundle. The trusted signer is `rdmx6-jaaaa-aaaaa-aaadq-cai`. Use the `identity-attributes` library with `trusted_attribute_signers` and `frontend_origins` configured. Hand-written Rust must check `msg_caller_info_signer()` before reading `msg_caller_info_data()`, or an attacker canister can forge `email = "admin@you.com"`.
3. **Substituting `{tid}` in the Microsoft scoped-key prefix.** The `microsoft` provider URL is the literal `https://login.microsoftonline.com/{tid}/v2.0`; keys look like `openid:https://login.microsoftonline.com/{tid}/v2.0:email` exactly. Filling in a tenant ID misses every lookup.
4. **Treating `email` as verified.** `email` is the raw address from the user's II-linked account; II does not check it, so treat it as user input. `verified_email` is present only when II established that the user controls the address: an OpenID provider marked it verified, or the user verified it with II. Gate access on `verified_email` only. There is **no `verified_email` under `sso:`**: an organization's SSO cannot produce one; its `sso:<domain>:email` is asserted by that organization's own provider, so trust it only for domains you list (`trusted_sso_domains`). What an organization can and cannot assert about its own staff is the `internet-identity-sso` skill.
