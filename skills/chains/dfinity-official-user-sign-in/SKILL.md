---
name: user-sign-in
description: "Add Internet Identity sign-in to a frontend or canister: passkey and OpenID (Google, Apple, Microsoft) sign-in with @icp-sdk/auth, sending users to an organization's SSO with ssoDomain, the client lifecycle, and local development. Also covers the primary origin an app's principals are permanently tied to: electing it, setting derivationOrigin, the ii-alternative-origins and ii-derivation-origin documents, and the ii-app-metadata document that names the app on the sign-in screen. Use when adding sign-in, login, auth, passkeys or Internet Identity to an app, when an app gains a custom domain or a sibling app, or when the same user arrives as a different principal on two origins. For a verified email or name in the backend use user-attributes; to notify users use user-notifications; to set up an organization's own SSO use organization-sign-in. Do NOT use for wallet or ICRC signer flows (use wallet-integration) or for an agent or CLI signing in as a user (use agent-web-identity)."
license: Apache-2.0
compatibility: "icp-cli >= 0.2.4, Node.js >= 22"
metadata:
  title: User Sign-In
  category: Auth
---

# User Sign-In

## What This Is

Internet Identity (II) is the Internet Computer's native authentication system. Users sign in to II-powered apps with passkeys, with an OpenID account (Google, Apple, Microsoft), or through their organization's own SSO; no usernames or passwords. Each user gets a unique principal per app origin, preventing cross-app tracking.

## Prerequisites

- `@icp-sdk/auth@^11` with `@icp-sdk/core@^6`. **Pin both majors together.** auth 11 and 10 peer `@icp-sdk/core@^6`; auth 9 peers `^5`.

## Canister IDs

| Canister | ID | URL | Purpose |
|---|---|---|---|
| Internet Identity (backend) | `rdmx6-jaaaa-aaaaa-aaadq-cai` |  | What sign-in runs against; signs attribute bundles |
| Internet Identity (frontend) | `uqzsh-gqaaa-aaaaq-qaada-cai` | `https://id.ai` | Serves the sign-in UI; `authorizeUrl` points here |

Both IDs are identical on mainnet and on a local network. Hardcode them.

## Mistakes That Break Your Build

1. **Wrong II URL for the environment.** `authorizeUrl` points at the **frontend** canister: `https://id.ai/authorize` on mainnet, `http://id.ai.localhost:8000/authorize` for a local II (`ii: true`). The URL is used verbatim, so include `/authorize`: `https://id.ai` opens the II home page and never returns a delegation.
2. **Passing `identityProvider` as a string, or half of it.** It is an object, `{ authorizeUrl, canisterId }`, both required together; a string or `URL` throws a `TypeError`. Omit the option entirely to get mainnet II, which is what most apps want.
3. **Top-level `await` in frontend code.** Vite 6 and earlier target `es2020`-era browsers by default, which have no top-level await, so the build fails; Vite 7 allows it. Wrap the setup in an `async function init()` (or a framework lifecycle hook). Do NOT change `build.target` to `esnext` to make it compile.
4. **Treating `maxTimeToLive` as the lifetime of the signing key.** It bounds the **session** at II, and `maxTimeToIdle` ends a session nobody uses; the delegation your calls are signed with is short-lived and replaced by the client. Leave both unset unless the app has its own policy: II applies seven days idle and thirty days in total.
5. **Not awaiting `signIn()` or skipping the `try`/`catch`.** `signIn()` rejects when the user closes the popup or authentication fails.
6. **`shouldFetchRootKey` or `fetchRootKey()` in browser code.** The `ic_env` cookie (set by the frontend canister or the Vite dev server) carries the root key as `IC_ROOT_KEY`: pass it as `rootKey` to `HttpAgent.create()` and leave `host` unset. Fetching the root key at runtime lets a man-in-the-middle substitute a fake one on mainnet.
7. **Getting `2vxsx-fae` as the principal.** That is the anonymous principal: authentication silently failed. Usual causes: a wrong `authorizeUrl` (especially missing `/authorize`), an unhandled `signIn()` rejection, or reading the identity before `signIn()` resolved. `getIdentity()` throws `SessionNotHeldError` (not an anonymous identity) when a sign-in exists that this origin holds no credential for.
8. **Passing the principal as an argument.** The backend reads the caller from the IC protocol: `msg.caller` in Motoko, `ic_cdk::api::msg_caller()` in Rust. An argument is whatever the caller typed and proves nothing. Role guards and anonymous-principal rejection are in the `canister-security` skill.
9. **Letting the first origin with users be one you can lose.** The origin an account is created under is permanent, so settle whether this app will have siblings before it has users: see "Your app's identity is its primary origin". What is *not* a mistake: setting `derivationOrigin` to the origin you are already served at is a validated no-op, not an error. II compares the two in canonical form and skips validation entirely, which is also why `ic0.app`, `icp0.io` and `icp.net` are interchangeable and a single-origin app needs no configuration at all.
10. **Sharing a cookie domain without a shared `derivationOrigin`.** A cookie does not produce a shared principal: without one primary origin authorized for every subdomain, the shared record names an account the reading origin can never hold, and `/reauth` bounces the user forever. Elect the primary origin first, then load `single-sign-in`.
11. **A silent re-issue without `hint`, on the default transport, or to an undeclared callback.** `prompt: 'none'` without `hint` fails with `InteractionRequiredError` (`reason` `account_selection_required`) when II holds more than one session, and with no user gesture it needs `transport: 'redirect'` to a route declared in `/.well-known/ii-auth-callbacks`. The `single-sign-in` skill builds this `/reauth` route.
12. **Serving `/.well-known/ii-app-metadata` on the wrong origin, without CORS, or with one bad field.** One invalid field invalidates the whole document. See "App metadata on the sign-in screen".
13. **Calling `signIn()` in a worker, or awaiting `ready()` in a page.** A worker only reads the sign-in, and `signIn()` and `signOut()` throw there. A page never needs `ready()`. See "In a web or service worker".

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

## In a web or service worker

From `@icp-sdk/auth` 11.2.0, a web worker or service worker reads its origin's sign-in with the same `AuthClient`:

```javascript
const authClient = new AuthClient();

// A service worker rejects top-level await: await inside a function or event handler.
async function createActor() {
  // The state loads from IndexedDB; until then the client reads as signed out.
  await authClient.ready();
  if (!authClient.isAuthenticated()) return undefined;
  const identity = await authClient.getIdentity();
  // No rootKey: a worker has no cookies, so the agent's built-in mainnet key applies.
  const agent = await HttpAgent.create({ identity });
  return Actor.createActor(idlFactory, { agent, canisterId });
}
```

- A worker has no `document.cookie`, so `safeGetCanisterEnv()` finds no `ic_env` there. On mainnet the agent's built-in root key is correct. Against a local network, a page passes `IC_ROOT_KEY` and the canister IDs to the worker with `postMessage`.
- A worker only reads. `signIn()` and `signOut()` throw there: signing in and out happens in a page. A session the worker cannot use is left for a page to end.
- Await `ready()` only in a worker. In a page the status is correct from construction, and waiting holds the page up on IndexedDB and a session restore for nothing.
- `ready()` rejects where restoring the session fails, as `getIdentity()` does.
- With `CookieStateStorage`, a sign-in this origin holds no credentials for reads as signed out in a worker, since the worker could not act on it.

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
  | { state: "available"; name?: string }      // name from the org's file
  | { state: "invalid"; reason: string }       // not a domain: the user fixes the input
  | { state: "unavailable"; retryAfter?: Date; reason?: string };
```

Checking while the user types, one client per pause rather than per keystroke. A superseded client is disposed before it can publish, so stale results never render:

```javascript
let client;
let timer;

input.addEventListener("input", () => {
  client?.dispose();  // also stops the old client's check
  client = undefined; // Continue never signs in to the old domain
  showSpinner();

  clearTimeout(timer); // debounce
  timer = setTimeout(() => {
    const next = new AuthClient({ ssoDomain: input.value }); // never throws for the domain
    next.subscribe(() => render(next.getSsoStatus()));
    render(next.getSsoStatus());
    client = next;
  }, 300);
});

// Synchronous in the click handler: never await the check first.
continueButton.addEventListener("click", () => {
  client?.signIn().then(showApp, showSignInError);
});
```

- `refreshSsoStatus()` re-runs the check for a "Try again" button. While `retryAfter` is in the future, II answers `unavailable` again at once with no new fetch, so disable the button and show a countdown. It does nothing on an `invalid` client, and a client never re-checks by itself.
- `signIn()` proceeds in every state: II resolves the domain itself and shows its own loading and error screens, for an `invalid` value too.
- `invalid` follows II's own rules: at least two labels of 1 to 63 letters, digits, or hyphens, no hyphen at either end, no `--` in a label's third and fourth places (punycode `xn--` aside), at most 253 characters, and a port only on a loopback host. Its `reason` names every problem found.
- The check warms II's cache, so `signIn()` on the same client starts fast.

The organization's own side of this, which is the OIDC client, the `ii-openid-configuration` file, per-app access, the limits that reject the file and the caching windows, is the `organization-sign-in` skill.

## Your app's identity is its primary origin

Internet Identity derives a principal per origin. Nothing in the sign-in flow above sets one, and that is correct: with no `derivationOrigin`, principals derive from the origin you are served at, which for a new app is its canister address. You already have an app identity, and it is already anchored on something nobody can take away.

You reach for `derivationOrigin` only when that stops being enough, which happens in exactly two situations: the app gains a second origin, usually a custom domain, or it gains a sibling app whose users have to be the same people. Both are below.

### Decide before your first sign-in

The origin an account is created under cannot be changed afterwards: repointing it orphans every account made there. So the question to settle before shipping is not "do I have a custom domain yet" but **is this one app, or the first of several?**

- **One app.** Nothing to do. The canister address is the identity, now and later. Adding a domain later is handled below and costs nothing.
- **The first of several.** Create the canister that will serve the primary origin before the first app ships, and point that app at it from its first deploy.

You do not need to know what the suite will contain. The `ii-alternative-origins` list grows as each app ships; what cannot change is which origin the list lives on.

### Adding a domain

A custom domain is a second origin, so left alone it is a second set of users. Keep the identity on the canister address and let the domain derive against it.

1. The domain passes `derivationOrigin`; the canister origin does not:

```javascript
const authClient = new AuthClient({ derivationOrigin: "https://<canister-id>.icp.net" });
```

2. The canister origin serves `/.well-known/ii-alternative-origins`:

```json
{ "alternativeOrigins": ["https://shop.example.com"] }
```

At most **100** entries, origins only (no trailing slash, no path). Over the cap II rejects the **entire list**, so every alternative origin stops authenticating, not just the extras. II canonicalizes `ic0.app`, `icp0.io` and `icp.net` to one form, so one entry per origin covers all three gateway spellings.

3. With `@dfinity/static-site`, add a `_headers` block (the file has no extension, and certified assets set no CORS header by default):

```
/.well-known/ii-alternative-origins
  Content-Type: application/json
  Access-Control-Allow-Origin: *
```

Pointing the derivation origin at the domain instead works, since II validates it like any other origin, but is not recommended. A domain can lapse, be sold or be rebranded, and every account derived from it goes with it. A canister address cannot be taken away.

### A suite that shares one sign-in

Apps that share a sign-in must share a principal, so they must all derive from one origin, and someone has to elect it. Elect the origin that represents the whole product rather than one app inside it, such as an app switcher, a landing page or an account portal. Failing that, elect a canister that exists only to serve the well-known documents.

Three properties make a good primary origin:

- **It is the front door.** `ii-app-metadata` is read from the primary origin, so the elected canister names the *whole suite* on every app's sign-in screen. Elect one product canister and every sibling signs in under that product's name.
- **It deploys first.** Nothing can derive against an origin that does not exist yet.
- **It is never retired.** It holds the suite's identity for as long as the accounts do. Principals derive from the origin, so the canister keeps its code and state at your discretion (an upgrade or a reinstall changes nothing, as long as it goes on serving the well-known documents); what it can never do is hand the role to a different canister id, because that is a different origin.

The user sees their own app's origin, not the primary one: II shows the origin being signed in to and reads only the name, description and logo from the primary origin.

Electing the origin is the whole of the decision; the rest of a single sign-in across the suite is a build. The cookie record, the `/reauth` route and the per-app `ii-auth-callbacks` document are in the `single-sign-in` skill, which assumes this section is already settled.

### Per environment

Canister ids differ per environment, so the primary origin does too. Bake it at build time from the environment's manifest rather than hardcoding one. Principals differ across environments as a result, which is expected.

### Both directions

Two well-known documents describe the same relation from opposite ends, and they have different readers:

| Document | Served at | Says | Read by |
|---|---|---|---|
| `ii-alternative-origins` | the primary origin | who may derive against me | Internet Identity, validating `derivationOrigin` |
| `ii-derivation-origin` | every app origin | which origin I derive from | an agent, which has no constructor to read |

II never reads the second: a browser passes `derivationOrigin` directly. It exists because an agent acting for the user has only a URL. Its body is the canonical `https://host` on one line, it is omitted when an app derives for its own visible origin, and **it must agree with what the client passes.** A missing or stale file hands an agent a different principal than the browser gives the same user, with no error.

Do not read `ii-alternative-origins` to discover the derivation origin. It is the inverse relation and there is no reverse lookup; used backwards it yields a plausible wrong principal rather than a failure.

### What the election also decides

Choosing the primary origin settles more than principals:

- the name, description and logo on every sign-in screen (`ii-app-metadata`);
- which canisters may notify, and the 10-sender cap they share (`ii-notification-senders`);
- the 100-entry budget in `ii-alternative-origins`, one per app origin.

`ii-auth-callbacks` is the exception: every app serves its own.

## App metadata on the sign-in screen

By default the sign-in screens identify an app by its **origin** alone. To also show a name, a short tagline and a logo, serve a JSON document at `/.well-known/ii-app-metadata`. Publishing it is permissionless: there is no list to join and no approval step. A valid document replaces the curated entry II still ships for a small set of known apps.

```json
{
  "name": "Example App",
  "description": "A short tagline shown on the sign-in screen",
  "logo": "/logo.png"
}
```

### Which origin serves it

II fetches it from the origin identities are derived for: the validated `derivationOrigin` when the auth request sets one, and the request's own origin otherwise. Publish it once on the primary origin and every alternative origin that origin certifies shows the same name, description and logo. A copy served only on the alternative origin the user visits is never read.

This also names the app on the notifications it sends, not only on the sign-in screen, and `ii-notification-senders` is read from the same origin by the same rule.

### Validation rules

All three fields are optional and unknown fields are ignored, so a document stays valid as II adds fields.

- `name` is at most 40 characters and `description` at most 120, counted in **Unicode code points on the value as served**, before whitespace collapsing. Collapsing is display-only and never rescues an over-long value.
- Each field must contain at least one visible character. A field holding only whitespace or invisible characters is rejected, not treated as absent.
- Rejected characters: control characters (other than the ASCII whitespace `\t`, `\n`, `\v`, `\f`, `\r`), `U+FEFF`, and the bidirectional embeddings and overrides `U+202A` to `U+202E`. Accepted: the marks `U+200E`, `U+200F`, `U+061C`, the isolates `U+2066` to `U+2069`, and the zero-width characters `U+200B` to `U+200D`. Isolates must be **balanced**: a field closes every isolate it opens and none it did not open.
- **One bad field invalidates the whole document.** None of it is applied (not half of it); II falls back to its curated entry if it ships one for the app, and to the origin alone otherwise. II logs the offending field to the browser console on the sign-in screen. A document carrying no field II recognises is ignored too.
- `logo` must be a **raster** image URL on the **same origin** as the document (relative URLs resolve against it), served as `image/png`, `image/jpeg`, `image/webp`, `image/gif`, or `image/avif`, at most 1 MiB and 4096 pixels per axis. `image/svg+xml` is rejected: serve a rasterised copy. II downloads the image (it is never hotlinked), redraws it at up to 512 pixels on its longest side (an animated image is flattened to its first frame), and renders that copy, so ship a roughly square PNG or WebP of about 512 pixels.
- **Write the logo URL relative** (`/logo.png`). II normalizes a canister gateway origin onto `ic0.app` and tries its `icp0.io` and `icp.net` twins in turn, so the document may be fetched from a sibling gateway domain of the same canister, and the same-origin check runs against whichever answered. An absolute URL pinned to one of them is cross-origin at the other two.
- Only the *shape* of `logo` (a non-empty URL on the document's own origin) is part of document validation. Once that passes, a logo that cannot be fetched or decoded, or that breaks the content-type, size, or dimension rules, costs the logo alone: the name and description still render.
- The document must not exceed 8 KiB, must be answered with `200`, and must not redirect (II follows redirects for neither the document nor the logo). II requests it without credentials and gives up after 10 seconds.

### CORS

The document and the logo are both read cross-origin, so both need CORS headers. With `@dfinity/static-site`, add them to the `_headers` file at the root of the build directory:

```
/.well-known/ii-app-metadata
  Content-Type: application/json
  Access-Control-Allow-Origin: *

/logo.png
  Access-Control-Allow-Origin: *
```

`.well-known/` is uploaded automatically, but the document has no file extension, so its media type must be set with the bare `Content-Type:` line.

Missing, unreachable, or invalid metadata never blocks sign-in. Publishing it verifies nothing about the app: II keeps showing the origin next to whatever the document provides, because the origin is the part users can check.

## Older `@icp-sdk/auth` majors

This skill targets `@icp-sdk/auth` 11.x. On an older major the same flow differs as follows.

### 11.1.x and earlier

`AuthClient` throws when constructed in a web worker or service worker, and has no `ready()`. Every older major below shares this.

### 10.x

No notification consent: `requestNotificationConsent`, `getNotificationConsentStatus` and `revokeNotificationConsent` arrive in 11.1.0. Earlier 11.x majors do not have them either.

Otherwise the same API, except the SSO domain check:

- `isValidSsoDomain(domain, signal)` fetched `/.well-known/ii-openid-configuration` from the browser and returned a boolean; the organization had to serve it with `Access-Control-Allow-Origin: *`. 11.x removes it: a client built with `ssoDomain` checks the domain through Internet Identity and reports `getSsoStatus()`.
- `new AuthClient({ ssoDomain })` threw on a malformed domain; 11.x reports `{ state: 'invalid', reason }` from `getSsoStatus()` instead and never throws for the domain. 11.x also reports `invalid` for a port on any host other than a loopback host (`localhost`, `127.0.0.1`, `*.localhost`), and for a malformed name such as `foo..com` or `ab--cd.com`.

### 9.x

The same API as 10.x, peering `@icp-sdk/core@^5`: use it if you are held on core 5. With core 6 a read-only session signs in instead of throwing "this session is read-only, which `@icp-sdk/auth` cannot act for yet".

### 8.x

What 9.x changed:

- `identityProvider` was a URL string; it is now `{ authorizeUrl, canisterId }`, and a string throws.
- `storage` and its `IdbStorage` / `LocalStorage` classes became `credentialStorage` with `IdbCredentialStorage` (the default), `LocalCredentialStorage`, `MemoryCredentialStorage`, and `SharedMemoryCredentialStorage`. `stateStorage` is new and holds the record of who is signed in, which is what makes tabs converge; `CookieStateStorage` extends that to sibling subdomains.
- `IdleManager` and its options (`idleOptions`, `onIdle`, `idleTimeout`, `disableIdle`) were removed. The session is bounded at Internet Identity instead, via `maxTimeToIdle` and `maxTimeToLive` on `signIn()`.
- `maxTimeToLive` bounded a delegation and capped every sign-in at 8 hours; it now bounds the session, and unset means the provider's own 30 days.
- `getStatus()`, `subscribe()`, `getPrincipal()`, and `dispose()` are new; the `identity`, `keyType`, and `targets` options are gone.

### 5.x

A callback-based API:

- `await AuthClient.create({...})` instead of `new AuthClient({...})`.
- `identityProvider` passed per call to `login({...})` rather than at construction.
- `authClient.login({ onSuccess, onError })`, which needs a promise wrapper.
- `authClient.logout()` instead of `authClient.signOut()`.
- `await authClient.isAuthenticated()` (async) instead of sync; `authClient.getIdentity()` (sync) instead of async.
- 5.x appends `/authorize` to the `identityProvider` URL, so passing `https://id.ai` works there.
- No `requestAttributes` / `AttributesIdentity`: the identity-attributes flow requires 7.x or later.

Upgrade when you can: the promise-based API is harder to misuse, and from 9.x the credentials a session's calls are signed with are short-lived and replaced for you, rather than one key being held for the session's whole length.

## Backend: Access Control

Anonymous-principal rejection, role guards, and caller binding in async functions are not II-specific: see the `canister-security` skill.

## Where to go next

- Load `single-sign-in` so a suite of apps on sibling subdomains needs one sign-in, once the primary origin above is elected.
- Load `user-attributes` for a verified email or display name in the backend.
- Load `user-notifications` to notify your users, even while the app is closed.
- Load `organization-sign-in` to set up an organization's own SSO, the side `ssoDomain` consumes.
- Load `canister-security` for anonymous-principal rejection and role guards.
