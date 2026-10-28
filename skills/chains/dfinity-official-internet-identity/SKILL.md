---
name: internet-identity
description: "Integrate Internet Identity authentication. Covers passkey, OpenID (Google, Apple, Microsoft), and organization SSO sign-in with @icp-sdk/auth, the SSO domain check (getSsoStatus), identity attributes (verified email, name) and their backend verification, sessions shared across subdomains, alternative origins, the /.well-known/ii-app-metadata document, and web push notifications (consent, the sender list, and sending from a Motoko or Rust canister). Use when adding sign-in, login, auth, passkeys, SSO, notifications, web push, or Internet Identity to a frontend or canister. Do NOT use for wallet integration or ICRC signer flows (use wallet-integration) or for an agent or CLI signing in as a user (use agent-web-identity)."
license: Apache-2.0
compatibility: "icp-cli >= 0.2.4, Node.js >= 22, moc >= 1.6.0"
metadata:
  title: Internet Identity
  category: Auth
---

# Internet Identity Authentication

## What This Is

Internet Identity (II) is the Internet Computer's native authentication system. Users sign in to II-powered apps with passkeys, with an OpenID account (Google, Apple, Microsoft), or through their organization's own SSO; no usernames or passwords. Each user gets a unique principal per app origin, preventing cross-app tracking.

Reference material for this skill lives in `references/`:

- `references/shared-sessions.md`: sharing one sign-in across sibling subdomains, end to end.
- `references/app-metadata.md`: every validation rule for `/.well-known/ii-app-metadata`.
- `references/enterprise-sso.md`: the organization's side of SSO (OIDC client, discovery file, limits, caching).
- `references/rust-identity-attributes.md`: the Rust backend for identity attributes, with the `identity-attributes` crate.
- `references/notifications.md`: notifying a signed-in user, end to end: consent, the sender list, sending, and delivery semantics.
- `references/older-api.md`: how `@icp-sdk/auth` 10.x and older differ.

## Prerequisites

- `@icp-sdk/auth@^11` with `@icp-sdk/core@^6`. **Pin both majors together.** auth 11 and 10 peer `@icp-sdk/core@^6`; auth 9 peers `^5`.
- For the Motoko backend: `mo:identity-attributes` >= 0.4.0 (mops), the mixin that injects the two sign-in methods and verifies the attribute bundle. It pulls in `mo:core` >= 2.5.0 and requires `moc` >= 1.6.0 for `include`.

## Canister IDs

| Canister | ID | URL | Purpose |
|----------|----|-----|---------|
| Internet Identity (backend) | `rdmx6-jaaaa-aaaaa-aaadq-cai` | | Mints delegations, signs attribute bundles |
| Internet Identity (frontend) | `uqzsh-gqaaa-aaaaq-qaada-cai` | `https://id.ai` | Serves the sign-in UI; `authorizeUrl` points here |

Both IDs are identical on mainnet and on a local network. Hardcode them.

## Mistakes That Break Your Build

1. **Wrong II URL for the environment.** `authorizeUrl` points at the **frontend** canister: `https://id.ai/authorize` on mainnet, `http://id.ai.localhost:8000/authorize` for a local II (`ii: true`). The URL is used verbatim, so include `/authorize`: `https://id.ai` opens the II home page and never returns a delegation.

2. **Passing `identityProvider` as a string, or half of it.** It is an object, `{ authorizeUrl, canisterId }`, both required together; a string or `URL` throws a `TypeError`. Omit the option entirely to get mainnet II, which is what most apps want.

3. **Top-level `await` in frontend code.** Vite 6 and earlier target `es2020`-era browsers by default, which have no top-level await, so the build fails; Vite 7 allows it. Wrap the setup in an `async function init()` (or a framework lifecycle hook). Code written that way builds on every version. Do NOT change `build.target` to `esnext` to make it compile.

4. **Treating `maxTimeToLive` as the lifetime of the signing key.** It bounds the **session** at II, and `maxTimeToIdle` ends a session nobody uses; the delegation your calls are signed with is short-lived and replaced by the client. Leave both unset unless the app has its own policy: II applies seven days idle and thirty days in total.

5. **Not awaiting `signIn()` or skipping the `try`/`catch`.** `signIn()` rejects when the user closes the popup or authentication fails.

6. **`shouldFetchRootKey` or `fetchRootKey()` in browser code.** The `ic_env` cookie (set by the frontend canister or the Vite dev server) carries the root key as `IC_ROOT_KEY`: pass it as `rootKey` to `HttpAgent.create()` and leave `host` unset. Fetching the root key at runtime lets a man-in-the-middle substitute a fake one on mainnet.

7. **Getting `2vxsx-fae` as the principal.** That is the anonymous principal: authentication silently failed. Usual causes: a wrong `authorizeUrl` (especially missing `/authorize`), an unhandled `signIn()` rejection, or reading the identity before `signIn()` resolved. `getIdentity()` throws `SessionNotHeldError` (not an anonymous identity) when a sign-in exists that this origin holds no credential for.

8. **Passing the principal as an argument.** The backend reads the caller from the IC protocol: `msg.caller` in Motoko, `ic_cdk::api::msg_caller()` in Rust. For access-control patterns see the **canister-security** skill.

9. **Adding `derivationOrigin` or `ii-alternative-origins` for the gateway domains.** II canonicalizes `ic0.app`, `icp0.io`, and `icp.net` to one form, so a canister served at any of them gets the same principal. Adding the configuration for that breaks authentication. A different principal there means a different passkey or device. A genuine second origin (a custom domain) does need it: see "Serving an app at more than one origin".

10. **Generating the attribute nonce on the frontend.** The nonce passed to `requestAttributes` MUST come from the backend (`_internet_identity_sign_in_start`), or the canister cannot check that the bundle's `implicit:nonce` is one it issued, and replay protection is gone.

11. **Reading attribute data without verifying the signer.** The IC verifies the signature, not who signed: any canister can produce a valid bundle. The trusted signer is `rdmx6-jaaaa-aaaaa-aaadq-cai`. Use the `identity-attributes` library (the `mo:identity-attributes` mixin in Motoko, the `#[identity_attributes]` attribute in Rust) with `trusted_attribute_signers` and `frontend_origins` configured. Hand-written Rust must check `msg_caller_info_signer()` before reading `msg_caller_info_data()`, or an attacker canister can forge `email = "admin@you.com"`.

12. **Substituting `{tid}` in the Microsoft scoped-key prefix.** The `microsoft` provider URL is the literal `https://login.microsoftonline.com/{tid}/v2.0`; keys look like `openid:https://login.microsoftonline.com/{tid}/v2.0:email` exactly. Filling in a tenant ID misses every lookup.

13. **Treating `email` as verified.** `email` is the raw address from the user's II-linked account; II does not check it, so treat it as user input. `verified_email` is present only when II established that the user controls the address: either an OpenID provider (e.g. Google) marked it verified, or the user linked and verified that email with II directly. Gate access on `verified_email` only. There is **no `verified_email` under `sso:`**: an organization's SSO cannot produce one; its `sso:<domain>:email` is asserted by that organization's own provider, so trust it only for domains you list.

14. **Sharing a cookie domain without a shared `derivationOrigin`.** Subdomains only share a sign-in when they share a principal. Without one derivation origin authorized for all of them, the shared record names an account the reading origin can never hold, and `/reauth` bounces the user forever. See `references/shared-sessions.md`.

15. **A silent re-issue without `hint`, on the default transport, or to an undeclared callback.** `prompt: 'none'` without `hint` fails with `InteractionRequiredError` (`reason` `account_selection_required`) when II holds more than one session. It runs on page load with no user gesture, so it needs `transport: 'redirect'` on a route of its own, declared in the origin's `/.well-known/ii-auth-callbacks`, or the redirect never comes back.

16. **Serving `/.well-known/ii-app-metadata` on the wrong origin, without CORS, or with one bad field.** II reads it from the derivation origin (when set) or the request origin, the document and the logo both need CORS, and one invalid field invalidates the whole document. See `references/app-metadata.md`.

17. **Installing majors that do not pair.** auth 11 peers `@icp-sdk/core@^6`; pinning core to `^5` out of habit gives:

    ```text
    npm error ERESOLVE unable to resolve dependency tree
    npm error Found: @icp-sdk/core@5.4.0
    npm error peer @icp-sdk/core@"^6" from @icp-sdk/auth@11.0.0
    ```

    Do not clear it with `--legacy-peer-deps` or `--force`. Pin `@icp-sdk/auth@^11` with `@icp-sdk/core@^6`, or stay on `@icp-sdk/auth@^9` if something else holds you on core 5.

18. **Signing in against a local II without `agentOptions`.** The client mints delegations by calling the II canister through an agent that verifies against the mainnet root key by default. With a local II the ceremony completes and the mint then fails with `TrustError: Certificate verification error` (`"Invalid signature"`). Pass `agentOptions: { rootKey }` from the `ic_env` cookie and leave `host` unset. A local II from an older network launcher lacks the minting methods: run `icp network update` and restart the network.

19. **Scheduling a logout from the delegation's expiration.** The delegation `getIdentity()` signs with is short-lived and replaced as it ages, so a timer from `identity.getDelegation()`'s expiration signs the user out after minutes. The session's end arrives as an `expired` status: subscribe, and leave the signed-in view when `isAuthenticated()` turns false.

20. **Checking an SSO domain from the browser.** Do not `fetch('https://<domain>/.well-known/ii-openid-configuration')` and do not look for `isValidSsoDomain` (removed in 11.x). Build the client with `ssoDomain` and read `getSsoStatus()`: II checks the domain against the same rules it signs in with, and the organization needs no CORS header.

21. **Awaiting the SSO check before `signIn()`, or wrapping the constructor in `try`/`catch` for the domain.** `signIn()` must be called synchronously in the click handler, or Safari blocks the popup. It proceeds in every SSO state, `invalid` included (II's own screens show progress and errors). In every state it rejects when the user closes the popup or authentication fails, so attach a rejection handler. The constructor never throws for a malformed domain: it reports `invalid`.

22. **Changing `ssoDomain` or `openIdProvider` on an existing client.** Both are constructor-only, like every other option; there is no setter and no per-`signIn()` override. For a new domain, build a new client and `dispose()` the superseded one.

## Using II during local development

**Default: use mainnet II from the local network.** With `icp-cli >= 0.2.4` the local network trusts the mainnet subnet's signatures, so delegations from `https://id.ai` work against a locally deployed backend. Construct the client with no `identityProvider`.

**Fallback: a local II,** only for fully offline development or a specific II build. Add `ii: true` to the local network in `icp.yaml`:

```yaml
networks:
  - name: local
    mode: managed
    ii: true
```

II is then served at `http://id.ai.localhost:8000`, with the same canister IDs. No canister entry is needed in your project. Pass the local root key:

```javascript
const authClient = new AuthClient({
  identityProvider: {
    authorizeUrl: "http://id.ai.localhost:8000/authorize",
    canisterId: "rdmx6-jaaaa-aaaaa-aaadq-cai",
  },
  agentOptions: { rootKey: canisterEnv?.IC_ROOT_KEY },
});
```

## Frontend: Sign-In Flow

Framework-agnostic; adapt the DOM parts.

```javascript
import { AuthClient } from "@icp-sdk/auth/client";
import { HttpAgent, Actor } from "@icp-sdk/core/agent";
import { safeGetCanisterEnv } from "@icp-sdk/core/agent/canister-env";

// The ic_env cookie carries the root key and canister IDs, locally and on mainnet.
const canisterEnv = safeGetCanisterEnv();

// Mainnet II is the default. derivationOrigin, openIdProvider, ssoDomain,
// stateStorage, transport, prompt, and hint are also constructor options.
const authClient = new AuthClient();

async function signIn() {
  try {
    // Optional session bounds: signIn({ maxTimeToIdle, maxTimeToLive }), in ns.
    return await authClient.signIn();
  } catch (error) {
    console.error("Sign-in failed:", error);
    throw error;
  }
}

// Ends the session at II: every tab of this origin is signed out.
async function signOut() {
  await authClient.signOut();
}

// No host: the default resolves correctly locally, on mainnet, and on custom domains.
async function createAuthenticatedActor(identity, canisterId, idlFactory) {
  const agent = await HttpAgent.create({ identity, rootKey: canisterEnv?.IC_ROOT_KEY });
  return Actor.createActor(idlFactory, { agent, canisterId });
}

// Wrapped in a function: Vite 6 and earlier reject top-level await by default.
async function init() {
  // isAuthenticated() is sync; getIdentity() is async.
  if (authClient.isAuthenticated()) {
    const identity = await authClient.getIdentity();
    const actor = await createAuthenticatedActor(identity, canisterId, idlFactory);
  }

  // getStatus(): 'signed-in' | 'signed-in-elsewhere' | 'expired' | 'signed-out'.
  // subscribe() fires on any change, including in another tab.
  authClient.subscribe(() => render(authClient.getStatus()));
}

init();
```

**Lifecycle.** One client for the page, or one per component: both read and write the same sign-in. A client a view owns is disposed with it: `dispose()` releases its listeners, subscription, and scheduled refresh, and is **not** a sign-out.

## One-click sign-in

`openIdProvider` (`'google'`, `'apple'`, `'microsoft'`) or `ssoDomain` (an organization's domain) skips II's method screen. They are mutually exclusive (a type error, and a throw at construction) and constructor-only.

```javascript
const google = new AuthClient({ openIdProvider: "google" });
const acme = new AuthClient({ ssoDomain: "acme.com" });
```

### Checking an organization's domain

A client built with `ssoDomain` checks its own domain through II as soon as it is constructed and reports the result like the session: a synchronous snapshot from `getSsoStatus()`, change notifications from `subscribe()`. No exceptions, no `AbortSignal`.

```typescript
type SsoStatus =
  | { state: "checking" }
  | { state: "available"; name?: string }      // name from the org's file: "Continue with Acme Corp"
  | { state: "invalid"; reason: string }       // not a domain: show reason, the user fixes the input
  | { state: "unavailable"; retryAfter?: Date; reason?: string }; // no SSO there, or failing; reason is II's, when given
```

Checking while the user types:

```javascript
let client;
let timer;

input.addEventListener("input", () => {
  client?.dispose();  // also stops the old client's check
  client = undefined; // Continue never signs in to the old domain
  showSpinner();

  clearTimeout(timer); // debounce: one client per pause, not per keystroke
  timer = setTimeout(() => {
    const next = new AuthClient({ ssoDomain: input.value }); // never throws for the domain
    next.subscribe(() => render(next.getSsoStatus()));
    render(next.getSsoStatus());
    client = next;
  }, 300);
});

function render(sso) {
  switch (sso.state) {
    case "checking":    return showSpinner();
    case "available":   return enableContinue(sso.name);
    case "invalid":     return showNotADomain(sso.reason);
    case "unavailable": return showUnavailable(sso.retryAfter, sso.reason);
  }
}

// Synchronous in the click handler: never await the check first.
continueButton.addEventListener("click", () => {
  client?.signIn().then(showApp, showSignInError);
});
```

- A superseded client is disposed before it can publish, so stale results never render. Debounce the input as above: building a client per keystroke churns clients and checks.
- `refreshSsoStatus()` re-runs the check for a "Try again" button. While `retryAfter` is in the future, II answers `unavailable` again at once with no new fetch, so disable the button and show a countdown ("Try again in 2 min"). It does nothing on an `invalid` client: the user fixes the input, which builds a new client. A client never re-checks by itself.
- `signIn()` proceeds in every state: II resolves the domain itself and shows its own loading and error screens, for an `invalid` value too. A closed popup or failed authentication rejects in any state.
- `invalid` follows II's own rules: at least two labels of 1 to 63 letters, digits, or hyphens, no hyphen at either end, no `--` in a label's third and fourth places (punycode `xn--` aside), at most 253 characters, and a port only on a loopback host (`localhost`, `127.0.0.1`, or a name under `.localhost`). Its `reason` names every problem found.
- The check warms II's cache, so `signIn()` on the same client starts fast.

How the organization sets up its side (OIDC client, the `ii-openid-configuration` file, per-app access, the limits that reject the file, caching): `references/enterprise-sso.md`.

## Identity attributes

When the backend needs more than the principal (e.g. a verified email), II returns a signed attribute bundle alongside the delegation. The backend exposes two methods: `_internet_identity_sign_in_start` mints a nonce, `_internet_identity_sign_in_finish` verifies the bundle. The `identity-attributes` library adds both: the `mo:identity-attributes` mixin in Motoko, and the `#[identity_attributes]` attribute in Rust (`references/rust-identity-attributes.md`). Both return the same Candid types, so the frontend is the same against either.

### Keys

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

### Frontend

```javascript
import { AuthClient } from "@icp-sdk/auth/client";
import { AttributesIdentity } from "@icp-sdk/core/identity";
import { HttpAgent, Actor } from "@icp-sdk/core/agent";
import { safeGetCanisterEnv } from "@icp-sdk/core/agent/canister-env";
import { Principal } from "@icp-sdk/core/principal";

const II_PRINCIPAL = "rdmx6-jaaaa-aaaaa-aaadq-cai";
const rootKey = safeGetCanisterEnv()?.IC_ROOT_KEY;

async function signInWithAttributes(authClient, canisterId, idl) {
  // Anonymous handle, used only to mint the nonce.
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

### Backend: Motoko

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
        # Required, comma-separated.
        frontend_origins: "https://your-app.icp.net"
        # Optional, comma-separated; omit to reject all sso:* keys.
        trusted_sso_domains: "your-org.com"
```

Unset `trusted_attribute_signers` rejects every bundle as untrusted; unset `frontend_origins` makes `_internet_identity_sign_in_finish` return `#err(#FrontendOriginsNotConfigured)`. The error variants (`#NoAttributes`, `#MalformedCandid`, `#FrontendOriginMismatch`, `#Stale`, `#UnknownNonce`, `#AmbiguousAttribute`, `#UntrustedSsoSource`, `#MixedSsoSources`) tell the frontend whether to retry with a fresh nonce or surface a bug.

## Serving an app at more than one origin

II derives a principal per **origin**, so `https://<canister-id>.icp.net` and `https://shop.example.com` are two different users. Pick **one** derivation origin (the canister address: custom domains can change, the canister address cannot) and list the others as alternative origins. Pin it before an origin has users: repointing an origin with existing sign-ins orphans every account made under it.

1. The alternative origin passes `derivationOrigin`; the primary origin does not:

   ```js
   const authClient = new AuthClient({ derivationOrigin: "https://<canister-id>.icp.net" });
   ```

2. The derivation origin serves `/.well-known/ii-alternative-origins` (in the static-site build, `dir/.well-known/ii-alternative-origins`):

   ```json
   { "alternativeOrigins": ["https://shop.example.com"] }
   ```

   At most **100** entries, origins only (no trailing slash, no path). Over the cap, II rejects the **entire list** ("has too many entries: To prevent misuse at most 100 alternative origins are allowed"): every alternative origin stops authenticating, not just the extras.

3. With `@dfinity/static-site`, add a `_headers` block (the file has no extension, and certified assets set no CORS header by default):

   ```
   /.well-known/ii-alternative-origins
     Content-Type: application/json
     Access-Control-Allow-Origin: *
   ```

Sharing one sign-in across sibling subdomains builds on this: `references/shared-sessions.md`.

## App metadata on the sign-in screen

Serve `/.well-known/ii-app-metadata` (`{ "name", "description", "logo" }`, all optional) on the derivation origin, with CORS on the document and the logo, and II shows your app's name, tagline, and logo next to the origin. `name` at most 40 and `description` at most 120 code points; `logo` a relative URL to a same-origin raster image (no SVG). One invalid field invalidates the whole document. Full rules: `references/app-metadata.md`.

## Notifications

Your canister can notify a signed-in user while the app is closed. II owns the push subscriptions, so there is no push service, no VAPID keys, and no device tokens in the app. Three pieces, all required; leaving one out produces silence rather than an error.

**Consent**, in the frontend. Needs `@icp-sdk/auth` 11.1.0 or later:

```javascript
const { granted } = await authClient.requestNotificationConsent();   // opens II; signs in if needed
const { granted } = await authClient.getNotificationConsentStatus(); // query, no screen
await authClient.revokeNotificationConsent();
```

All three answer a **record**, not a bare boolean. `granted: false` is the user's refusal, not a failure. Ask from a click: the ceremony renders, so it cannot run under `prompt: 'none'`.

**The sender list.** Serve `/.well-known/ii-notification-senders` on the derivation origin, naming the canisters allowed to notify for it: `{ "senders": ["ryjl3-tyaaa-aaaaa-aaaba-cai"] }`. At most 10, and cached, so a change is not instant. Without it every send is refused, silently.

**Sending**, with the `identity-notifications` library (crates.io for Rust, Mops for Motoko, which needs moc 2.0.0 or later), then `send(recipient, { title, body, url, key, ... })`. Rust wires `endpoints!()` and three `MemoryId`s into `init`, and calls `init` again from `post_upgrade`; Motoko's mixin needs neither and nothing on upgrade. Configuration is environment variables (`notification_sender`, `notification_origin`), not init arguments.

`key` is what a notification is *about*: sending again under the same key updates it rather than adding another, and it is what `dismiss` names, so derive it from something the caller cannot choose. `urgency` schedules against the origin's other traffic and is not a rendering hint.

The app addresses a user and nothing finer: where a notification reaches them is II's and the user's to manage. II composes what is shown, so publishing `/.well-known/ii-app-metadata` (see above) is what names the app on its notifications too. `send` neither traps nor awaits, so nothing comes back to branch on; `metrics()` is where a notification's fate shows up. Full rules: `references/notifications.md`.

## Backend: Access Control

Anonymous-principal rejection, role guards, and caller binding in async functions are not II-specific: see the **canister-security** skill.
