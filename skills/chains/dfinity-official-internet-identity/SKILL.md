---
name: internet-identity
description: "Integrate Internet Identity authentication. Covers passkey and OpenID sign-in flows, delegation handling, principal-per-app isolation, and the /.well-known/ii-app-metadata document that shows your app's name, description, and logo on the sign-in screen. Use when adding sign-in, login, auth, passkeys, or Internet Identity to a frontend or canister. Do NOT use for wallet integration or ICRC signer flows — use wallet-integration instead."
license: Apache-2.0
compatibility: "icp-cli >= 0.2.4, Node.js >= 22, moc >= 1.6.0"
metadata:
  title: Internet Identity
  category: Auth
---

# Internet Identity Authentication

## What This Is

Internet Identity (II) is the Internet Computer's native authentication system. Users authenticate into II-powered apps either with passkeys stored in their devices or through OpenID accounts (e.g., Google, Apple, Microsoft) -- no usernames or passwords required. Each user gets a unique principal per app, preventing cross-app tracking.

## Prerequisites

- `@icp-sdk/auth` (>= 9.0.0), `@icp-sdk/core` (>= 5.3.0) (`AttributesIdentity` was added in core v5.3.0)
- For the Motoko backend example: `mo:identity-attributes` >= 0.4.0 (mops) — the mixin that injects the two sign-in methods and verifies the bundle for you. It pulls in `mo:core` >= 2.5.0 and requires `moc` >= 1.6.0 for the `include` mixin.

## Canister IDs

| Canister | ID | URL | Purpose |
|----------|------------|-----|---------|
| Internet Identity (backend) | `rdmx6-jaaaa-aaaaa-aaadq-cai` |  | Manages user keys and authentication logic |
| Internet Identity (frontend) | `uqzsh-gqaaa-aaaaq-qaada-cai` | `https://id.ai` | Serves the II web app; identity provider URL points here |

## Mistakes That Break Your Build

1. **Using the wrong II URL for the environment.** `authorizeUrl` must point to the **frontend** canister (`uqzsh-gqaaa-aaaaq-qaada-cai`), not the backend. Mainnet uses `https://id.ai/authorize`. Local-only II (when `ii: true` is set in `icp.yaml`) uses `http://id.ai.localhost:8000/authorize`. Both canister IDs are well-known and identical on mainnet and local replicas — hardcode them rather than doing a dynamic lookup.

2. **Passing `identityProvider` as a URL string, or naming only half of it.** In 9.x it is an object — `{ authorizeUrl, canisterId }` — and both fields are required together: the page a ceremony renders at and the canister that mints delegations are separate facts, and neither is derived from the other. A string or a `URL` throws a `TypeError`. Omit the option entirely to get mainnet Internet Identity, which is what most apps want. The URL is used verbatim, so include the `/authorize` path: `https://id.ai` opens the II home page and never returns a delegation.

3. **Treating `maxTimeToLive` as the lifetime of the key the frontend signs with.** In 9.x it bounds the **session** at Internet Identity, and `maxTimeToIdle` ends a session nobody has used; the delegation your calls are signed with is short-lived and replaced for you. Leave both unset unless the app has a policy of its own — the provider applies seven days of idleness and thirty days in total. Bound them where the data is sensitive, not to keep key material fresh.

4. **Not awaiting `signIn()` or skipping the `try`/`catch`.** `authClient.signIn()` returns a promise that rejects when the user closes the popup or authentication fails. Without `await` and a `catch`, those failures are silently swallowed.

5. **Using `shouldFetchRootKey` or `fetchRootKey()` instead of the `ic_env` cookie.** The `ic_env` cookie (set by the frontend canister or the Vite dev server) already contains the root key as `IC_ROOT_KEY`. Pass it via the `rootKey` option to `HttpAgent.create()` — this works in both local and production environments without environment branching. See the icp-cli skill's `references/binding-generation.md` for the pattern. Never call `fetchRootKey()` — it fetches the root key from the replica at runtime, which lets a man-in-the-middle substitute a fake key on mainnet.

6. **Getting `2vxsx-fae` as the principal after sign-in.** That is the anonymous principal -- it means authentication silently failed. Common causes: a wrong `authorizeUrl` on the `AuthClient` constructor (especially missing `/authorize`), an unhandled rejection from `signIn()`, or reading `getIdentity()` before `signIn()` resolved. Note that `getIdentity()` throws `SessionNotHeldError` rather than handing back an anonymous identity when a sign-in exists that this origin holds no credential for.

7. **Passing principal as string to backend.** The `AuthClient` gives you an `Identity` object. Backend canister methods receive the caller principal automatically via the IC protocol -- you do not pass it as a function argument. The caller principal is available on the backend via `shared(msg) { msg.caller }` in Motoko or `ic_cdk::api::msg_caller()` in Rust. For backend access control patterns, see the **canister-security** skill.

8. **Adding `derivationOrigin` or `ii-alternative-origins` to handle the official gateway domains (`ic0.app`, `icp0.io`, `icp.net`).** Internet Identity canonicalizes all three official canister gateway domains to one form during delegation (`icp.net` is the current default for new frontend canisters, replacing `icp0.io`), so a canister served at any of them produces the same principal. Do not add `derivationOrigin` or `ii-alternative-origins` configuration to handle this — it will break authentication. If a user reports getting a different principal, the cause is almost certainly a different passkey or device, not the domain. (A genuine second origin — a custom domain — is a different situation and *does* need this configuration: see "Serving an app at more than one origin".)

9. **Generating the attribute nonce on the frontend.** The nonce passed to `requestAttributes` MUST come from a backend canister call. A frontend-generated nonce defeats replay protection: the canister cannot verify that the bundle's `implicit:nonce` is one it actually issued. Have the backend mint and return the nonce from `_internet_identity_sign_in_start` (the `mo:identity-attributes` mixin provides it in Motoko; you write it in Rust), and check it against the bundle's implicit fields when the user calls `_internet_identity_sign_in_finish`.

10. **Reading attribute data without verifying the signer.** The IC verifies the signature, not the identity of the signer — any canister can produce a valid bundle. The trusted signer is `rdmx6-jaaaa-aaaaa-aaadq-cai` (Internet Identity). The check looks different per language:
    - **Motoko**: use the `mo:identity-attributes` mixin. `include IdentityAttributes({ onVerified })` verifies the signer, origin, nonce, and freshness for you and runs `onVerified` only on a bundle that passes — configure `trusted_attribute_signers` and `frontend_origins` in `icp.yaml` (see "Backend: Reading Identity Attributes"). Don't hand-roll the ICRC-3 decode or the signer check on top of `mo:core/CallerAttributes` unless you need behavior the library doesn't cover.
    - **Rust**: there is no CDK wrapper yet. Always check `msg_caller_info_signer()` against the trusted issuer principal before reading `msg_caller_info_data()`. Skipping this lets an attacker canister forge attributes like `email = "admin@you.com"`.

11. **Substituting `{tid}` in the Microsoft scoped-key prefix.** The `microsoft` OpenID provider URL is the literal string `https://login.microsoftonline.com/{tid}/v2.0` — `{tid}` is part of the URL, not a tenant-ID placeholder you fill in. Bundle keys returned by `scopedKeys({ openIdProvider: 'microsoft' })` look like `openid:https://login.microsoftonline.com/{tid}/v2.0:email` exactly, and the backend must look up that literal key. Replacing `{tid}` with a tenant GUID will silently miss every attribute lookup.

12. **Treating `email` as verified.** `email` and `verified_email` are distinct keys.
    - `email` is the raw email string from the user's II-linked account. II does not check it. Treat it as user-supplied input.
    - `verified_email` is the same email as `email`, but only present when the source OpenID provider (e.g., Google) marked it as verified and II surfaced that signal through.
    Use `verified_email` for any access gating (admin allowlists, capability checks). Use `email` only for soft uses like contact info or mailing lists. Request both for fallback behaviour: both are returned with the same value when the source provider marked the email as verified, only `email` when it didn't.

13. **Sharing a cookie domain without a shared `derivationOrigin`.** Sibling subdomains only share a sign-in when they share a principal, and principals are per origin: without one derivation origin authorized for all of them, the shared record names an account the reading origin can never hold, so `/reauth` bounces the user back forever. Set the derivation origin first, then the cookie domain.

14. **A silent re-issue without `hint`, on the default transport, or to an undeclared callback.** `prompt: 'none'` asks the provider to answer from the session it holds. Without `hint`, a provider holding more than one session refuses rather than guessing — `InteractionRequiredError` with `reason` `account_selection_required` — so what you lose is the resume, not the user's identity: a mint for an unexpected account is rejected client-side as `AccountMismatchError`. The re-issue also runs on page load with no user gesture, so the default `window` transport is popup-blocked: use `transport: 'redirect'` on a route of its own, and declare that route in the origin's `/.well-known/ii-auth-callbacks`, or the redirect never comes back.

15. **Serving `/.well-known/ii-app-metadata` on the wrong origin, or without CORS.** II reads app metadata from the origin identities are derived for — your validated `derivationOrigin` when the request sets one, the request's own origin otherwise. A document published only on the alternative origin the user visits is never fetched. The document *and* the logo it points at are both read cross-origin, and they fail differently: without `Access-Control-Allow-Origin` on the document none of your metadata is used (II falls back to its curated entry if it ships one for your app, and to your origin alone otherwise), while an unreadable logo costs you the logo alone — the name and description still render. See "Showing your app's name, description, and logo on the sign-in screen".

16. **Assuming a bad field in `ii-app-metadata` is just dropped, or confusing a rejected logo with a rejected document.** One field that fails validation invalidates the **whole document**: none of your metadata is applied, not just the offending field (II then falls back to its curated entry if it ships one for your app, and to your origin alone otherwise). `name` is capped at 40 Unicode code points and `description` at 120, counted on the value as served. `logo` straddles the two failure modes — a URL that is not on the **same origin** as the document fails document validation and takes the whole document down with it, and that includes your own canister on a sibling gateway domain, since II may fetch the document from any of `ic0.app`, `icp0.io`, or `icp.net` (write the URL relative) — while an SVG (`image/svg+xml` is not accepted; serve a raster copy), an oversized image, or one that cannot be fetched or decoded costs you the logo alone.

## Using II during local development

**Default: use mainnet II from your local network.** Starting with `icp-cli >= 0.2.4`, the local network (pocket-ic, launched by `icp-cli-network-launcher`) is configured to trust the mainnet subnet's BLS signatures. Delegations signed by `https://id.ai` are accepted by your local replica, so both the sign-in flow *and* authenticated calls to a locally-deployed backend just work — no extra config in `icp.yaml`, no local II canister to manage, and the UI is the real one your users will see.

Construct the client with no `identityProvider` at all: mainnet Internet Identity is what it defaults to, and you're done.

### Fallback: deploy II locally

Only use this if you need fully-offline dev or want to test against a specific II build. Add `ii: true` to the local network in your `icp.yaml`:

```yaml
networks:
  - name: local
    mode: managed
    ii: true
```

This deploys the II canisters automatically when the local network is started. The II frontend will be available at `http://id.ai.localhost:8000`, so the client is constructed with `identityProvider: { authorizeUrl: 'http://id.ai.localhost:8000/authorize', canisterId: 'rdmx6-jaaaa-aaaaa-aaadq-cai' }` — the canister id is the same locally, since system canisters keep their mainnet ids on the local network. No canister entry is needed in your project — II is not part of your project's canisters. For the full `icp.yaml` canister configuration, see the **icp-cli** and **static-site** skills.

### Frontend: Vanilla JavaScript/TypeScript Sign-In Flow

This is framework-agnostic. Adapt the DOM manipulation to your framework.

```javascript
import { AuthClient } from "@icp-sdk/auth/client";
import { HttpAgent, Actor } from "@icp-sdk/core/agent";
import { safeGetCanisterEnv } from "@icp-sdk/core/agent/canister-env";

// Read the ic_env cookie (set by the frontend canister or Vite dev server).
// Contains the root key and canister IDs — works in both local and production.
const canisterEnv = safeGetCanisterEnv();

// Mainnet Internet Identity is the default, so no identityProvider is needed:
// pocket-ic (icp-cli >= 0.2.4) trusts mainnet subnet signatures, so this works
// from local dev too. Pass { authorizeUrl, canisterId } only for a local II
// (`ii: true` in icp.yaml) or another deployment; both halves are required
// together, and a bare URL string throws.
//
// derivationOrigin, and openIdProvider for one-click sign-in
// ('google' | 'apple' | 'microsoft'), are also constructor options.
//
// Several clients may share an origin and read the same sign-in, so construct
// one where you need it and dispose of it when that view goes away.
const authClient = new AuthClient();

// Sign in: signIn() returns the new Identity directly and rejects if the user
// closes the popup or authentication fails. The session's bounds
// (maxTimeToIdle, maxTimeToLive) are optional; unset means Internet Identity's
// own, currently seven days idle and thirty days in total.
async function signIn() {
  try {
    const identity = await authClient.signIn();
    console.log("Signed in as:", identity.getPrincipal().toText());
    return identity;
  } catch (error) {
    console.error("Sign-in failed:", error);
    throw error;
  }
}

// Sign out, which ends the session at Internet Identity: every tab of this
// origin is signed out and the session cannot be resumed. Nothing to reset or
// reload here — the state changes, so the subscription below re-renders.
async function signOut() {
  await authClient.signOut();
}

// Create an authenticated agent and actor.
// Uses rootKey from the ic_env cookie — no shouldFetchRootKey or environment branching needed.
async function createAuthenticatedActor(identity, canisterId, idlFactory) {
  const agent = await HttpAgent.create({
    identity,
    host: window.location.origin,
    rootKey: canisterEnv?.IC_ROOT_KEY,
  });

  return Actor.createActor(idlFactory, { agent, canisterId });
}

// Initialization — wraps async setup in a function so this code works with
// any bundler target (Vite defaults to es2020 which lacks top-level await).
async function init() {
  // isAuthenticated() is sync; getIdentity() is async.
  if (authClient.isAuthenticated()) {
    const identity = await authClient.getIdentity();
    const actor = await createAuthenticatedActor(identity, canisterId, idlFactory);
    // Use actor to call backend methods
  }

  // Re-render when who is signed in here changes, including in another tab:
  // getStatus() is 'signed-in' | 'signed-in-elsewhere' | 'expired' |
  // 'signed-out', and the last three each want a different screen.
  authClient.subscribe(() => render(authClient.getStatus()));
}

init();
```

### The client's lifecycle

One client for the page, or one per component: both work, and they read and write
the same sign-in.

```javascript
// Page-lifetime: one client for the app, nothing to dispose. Views come and go,
// so each hands back the teardown for its own listener.
const authClient = new AuthClient();

function watchHeader() {
  const unsubscribe = authClient.subscribe(() => render(authClient.getStatus()));
  return unsubscribe; // when the header goes; the client carries on
}

// Component-lifetime: the client belongs to the view, so it goes with the view.
function openReauthDialog(principal) {
  const client = new AuthClient({ prompt: "none", hint: principal });
  return () => client.dispose(); // covers its subscription, and is not a sign-out
}
```

`prompt: "none"` with `hint` is a silent re-issue, which an app wants when a
sibling subdomain is already signed in: see "Sharing a sign-in across sibling
subdomains" below.

The client is browser-only, so under a server-rendering framework whatever owns it
must be client-rendered.

### Serving an app at more than one origin

II derives a principal per **origin**, so `https://<canister-id>.icp.net` and `https://shop.example.com` are two different users to the same person. To keep one account per person, pick **one** origin as the derivation origin and list the others as alternative origins.

Pick the **canister address** as the derivation origin. Custom domains can be changed or dropped; the canister address cannot.

**1. The alternative origin passes `derivationOrigin`.** The primary origin does *not* — it is only set on the other origins.

```js
const authClient = new AuthClient({
  derivationOrigin: "https://<canister-id>.icp.net",
});
```

**2. The derivation origin's canister serves the list.** Put the file at `dir/.well-known/ii-alternative-origins`:

```json
{ "alternativeOrigins": ["https://shop.example.com"] }
```

A maximum of **100** alternative origins can be listed. Entries are origins — no trailing slashes and no paths.

Going over the cap is not a truncation: II rejects the entire list with `has too many entries: To prevent misuse at most 100 alternative origins are allowed`, so **every** alternative origin stops authenticating, not just the ones past the limit.

**3. With `@dfinity/static-site`, add a `_headers` block.** `.well-known/` is uploaded automatically, but this file has no extension, so its media type is not `application/json`, and the certified-assets canister sets no CORS header by default. II needs both:

```
/.well-known/ii-alternative-origins
  Content-Type: application/json
  Access-Control-Allow-Origin: *
```

Do **not** reach for `.ic-assets.json5` — that is the legacy asset canister's config file, and the static-site recipe does not read or even upload it, so the headers would silently never apply. See the `static-site` skill.

**Order matters.** Pin the derivation origin before an origin has users. Repointing an origin that has already collected sign-ins orphans every account made under it.

### Sharing a sign-in across sibling subdomains

`chat.example.com` and `hr.example.com` can share one sign-in: sign in on one and
the others are signed in without a second visit to the provider, and signing out
on one signs the user out on all of them.

This builds on the section above. Every app must derive from **one** derivation
origin, listed in that origin's `ii-alternative-origins`, or each subdomain gets
its own principal and there is nothing to share. A shared cookie does not change
that. On top of it, two things:

**1. Share the record.** Every app builds its client with the same cookie domain,
so a sign-in on one writes a record the others read:

```javascript
import { AuthClient, CookieStateStorage, InteractionRequiredError } from "@icp-sdk/auth/client";

const clientOptions = {
  derivationOrigin: "https://auth.example.com",
  stateStorage: new CookieStateStorage({ domain: "example.com" }),
};
```

Choosing that domain means trusting every origin under it. Don't do it on a domain
whose subdomains you don't control.

**2. Acquire the sign-in where a sibling made it.** An app that reads
`signed-in-elsewhere` asks the provider for its own credential for that account,
on a route of its own:

```javascript
// /reauth — a route of its own, because this runs on page load with no user
// gesture, and a popup opened without one is blocked.
async function reauth() {
  const status = new AuthClient(clientOptions).getStatus();

  if (status.state !== "signed-in-elsewhere") {
    location.replace("/");
    return;
  }

  // A second client: prompt and hint are set when a client is built.
  const authClient = new AuthClient({
    ...clientOptions,
    transport: "redirect",
    prompt: "none",
    hint: status.principal, // answer for the account already signed in
  });

  try {
    await authClient.signIn({
      returnTo: new URLSearchParams(location.search).get("next") ?? "/",
    });
  } catch (error) {
    if (error instanceof InteractionRequiredError) {
      // The provider has nothing to resume, so the sign-in is stale: clear it,
      // or every app on the domain keeps sending the user back here.
      await authClient.signOut().catch(() => {});
    }
    location.replace("/");
  }
}

reauth();
```

**Each app origin declares the callback.** A redirect sign-in is delivered only to
a callback the returning origin itself declares, so every app serves
`/.well-known/ii-auth-callbacks` on its own origin, listing its own `/reauth`:

```json
{ "callbacks": ["https://chat.example.com/reauth"] }
```

One file per app origin, not one on the derivation origin. The entry is matched
exactly, so it must be the full URL with no fragment, and II reads the document
cross-origin, so serve it as `application/json` with CORS. With
`@dfinity/static-site`, that is another `_headers` block, for the same reason
`ii-alternative-origins` needs one:

```
/.well-known/ii-auth-callbacks
  Content-Type: application/json
  Access-Control-Allow-Origin: *
```

Validation fails closed: undeclared, unreadable, or not exactly matching, and the
sign-in never comes back. A declared callback also has to terminate locally, since
the response arrives in the URL fragment and a `3xx` that carries none re-attaches
it to wherever it forwards.

**3. Pick it up on load, on every page.** Not only the pages that require a
sign-in: a visitor who is already signed in on a sibling would otherwise land on
a public page here and see a signed-out header. Each page reads the status as it
loads and hands `signed-in-elsewhere` to `/reauth`, naming the page to come back
to, which is what makes the sharing automatic rather than something the user has
to click:

```javascript
// On load, on every page of the app.
const status = new AuthClient(clientOptions).getStatus();

// This state only: a sibling is signed in and this app can pick that up without
// asking the user anything. signed-out and expired both mean a normal sign-in,
// and sending those to /reauth just bounces the user back.
if (status.state === "signed-in-elsewhere") {
  location.replace(`/reauth?next=${encodeURIComponent(location.pathname + location.search)}`);
}
```

`/reauth` reads that `next` and passes it as `returnTo`, so the user lands back on
the page they asked for, signed in, having seen nothing.

**4. Jump on load, ask afterwards.** Step 3 redirects because the page has only
just started. Once a page is open the status can still turn `signed-in-elsewhere`,
when someone signs in on a sibling in another tab, and redirecting a page the user
is working on would throw away what they are doing. So subscribe, and offer the
same redirect behind a button:

```javascript
authClient.subscribe(() => {
  if (authClient.getStatus().state === "signed-in-elsewhere") {
    // A banner or dialog whose button runs the same redirect as step 3.
    showResumeDialog(() =>
      location.replace(`/reauth?next=${encodeURIComponent(location.pathname + location.search)}`),
    );
  }
});
```

The full walkthrough, including what ends a session on its own and what a sign-out
does to the siblings, is in the library's [shared sessions
guide](https://js.icp.build/auth/latest/shared-sessions/).

### Showing your app's name, description, and logo on the sign-in screen

By default the II sign-in screens identify your app by its **origin** alone. To have II also show a name, a short tagline, and a logo, serve a JSON document at `/.well-known/ii-app-metadata`. This is permissionless — there is no list to join and no approval step — and it supersedes the curated entry II still ships for a small set of known apps.

```json
{
  "name": "Example App",
  "description": "A short tagline shown on the sign-in screen",
  "logo": "/logo.png"
}
```

**Publish it on the derivation origin, not on every origin.** II fetches the document from the origin identities are derived for: your `derivationOrigin` once validated when the auth request sets one, and the request's own origin otherwise. Publish it once on the derivation origin and every alternative origin that origin certifies is presented with the same name, description, and logo — there is nothing to keep in sync. A copy served only on the alternative origin the user actually visits is never read.

All three fields are optional and unknown fields are ignored, so a document stays valid as II adds fields. The rules that decide whether yours is used:

- `name` is at most 40 characters and `description` at most 120, counted in **Unicode code points on the value as served** — before whitespace collapsing, which is display-only and never rescues an over-long value.
- Each field must contain at least one visible character. A field holding only whitespace or invisible characters is rejected, not treated as absent.
- Control characters (other than the ASCII whitespace `\t`, `\n`, `\v`, `\f`, `\r`), `U+FEFF`, and the bidirectional embeddings and overrides `U+202A`–`U+202E` are rejected: they can make rendered text read differently from what it contains. The characters mixed-direction and non-Latin names legitimately need are accepted — the marks `U+200E`, `U+200F`, `U+061C`, the isolates `U+2066`–`U+2069`, and the zero-width characters `U+200B`–`U+200D` — but isolates must be **balanced**: a field must close every isolate it opens and close none it did not open.
- **One bad field invalidates the whole document**, which is then ignored; the offending field is not dropped on its own. None of your document is applied rather than half of it; II then falls back to its curated entry if it ships one for your app, and to your origin alone otherwise. II logs which field is at fault to the browser console — check the console on the sign-in screen when metadata does not appear. A document carrying no field II recognises is likewise ignored; a valid one replaces the curated fallback entry wholesale.
- `logo` must be a **raster** image URL on the **same origin** as the document (relative URLs resolve against it), served as `image/png`, `image/jpeg`, `image/webp`, `image/gif`, or `image/avif`, at most 1 MiB, and at most 4096 pixels per axis. `image/svg+xml` is rejected — serve a rasterised copy of a vector logo. II downloads the image (it is never hotlinked), redraws it at up to 512 pixels on its longest side (an animated image is flattened to its first frame), and renders that copy, so a roughly square PNG or WebP of about 512 pixels is the right thing to ship. **Write the URL relative** (`/logo.png`): II normalizes a canister gateway origin onto `ic0.app` and tries its `icp0.io` and `icp.net` twins in turn, so the document may be fetched from a sibling gateway domain of the same canister — and the same-origin check below runs against whichever one answered. An absolute URL pinned to one of them is cross-origin at the other two.
- Only the *shape* of `logo` — a non-empty URL on the document's own origin — is part of the validation above. Once it passes, a logo that cannot be fetched or decoded, or that breaks the content-type, size, or dimension rules, costs you the logo alone: the name and description still render.
- The document must not exceed 8 KiB, must be answered with `200`, and must not redirect (II follows redirects for neither the document nor the logo). II requests it without credentials and gives up after 10 seconds.

**Both the document and the logo are read cross-origin, so both need CORS headers.** With `@dfinity/static-site`, extend the same `_headers` file used for alternative origins:

```
/.well-known/ii-app-metadata
  Content-Type: application/json
  Access-Control-Allow-Origin: *

/logo.png
  Access-Control-Allow-Origin: *
```

`.well-known/` is uploaded automatically, but this file has no extension either, so set its media type with the bare `Content-Type:` form. As above, `.ic-assets.json5` is the legacy asset canister's config and is not read by this recipe.

Missing, unreachable, or invalid metadata never blocks sign-in: the screen falls back to the curated entry, and to your origin alone otherwise. And because the file is under the sole control of the origin serving it, publishing it verifies nothing about your app — II keeps displaying the origin alongside whatever you provide, since the origin is the part users can actually check.

The normative rules, including a JSON Schema you can validate the document against in CI, are in the **App metadata** section of the [Internet Identity specification](https://docs.internetcomputer.org/references/internet-identity-spec/#app-metadata). The schema expresses every rule above except isolate balancing.

### Frontend: Requesting Identity Attributes

When the backend needs more than the user's principal (e.g., a verified email), Internet Identity can return signed attributes alongside the delegation. The flow is a two-method handshake on the backend: `_internet_identity_sign_in_start` mints a nonce, and `_internet_identity_sign_in_finish` verifies the bundle. In Motoko the `mo:identity-attributes` mixin provides both methods; in Rust you implement them by hand (see "Backend: Reading Identity Attributes"). The frontend below is identical against either backend.

#### Available attribute keys

`requestAttributes({ keys, nonce })` requires both `keys` and `nonce`: there is no default key set, you must pass an explicit list. The keys II currently accepts are:

| Key | What it IS | When to use |
|---|---|---|
| `name` | The user's display name from the II-linked account. | Personalisation in the UI. |
| `email` | The raw email string from the user's II-linked account. **II does not check it.** Treat as user-supplied input. | Mailing-list signups, contact email, anything where you don't gate access on the email. |
| `verified_email` | The same email as `email`, but only present when the source OpenID provider (e.g., Google) marked it as verified and II surfaced that signal. **The provider's verification is what makes it trustworthy.** | Access gating (e.g. an admin allowlist by email). Treat this as the only trustworthy email for authorisation. |

Request both `email` and `verified_email` if you want fallback behaviour: when the source provider marked the email as verified, both keys are present with the same value; when it didn't, only `email` is returned.

`scopedKeys({ openIdProvider, keys? })` rewrites the keys above into provider-scoped keys of the form `openid:<provider-url>:<key>`, so II returns the values from the linked OpenID account directly (with implicit consent, no extra prompt). Provider URLs:

| Provider | URL prefix in the bundle keys |
|---|---|
| `'google'` | `openid:https://accounts.google.com:` |
| `'apple'` | `openid:https://appleid.apple.com:` |
| `'microsoft'` | `openid:https://login.microsoftonline.com/{tid}/v2.0:` (the `{tid}` part is literal: do not substitute a tenant ID into it) |

The `keys` argument to `scopedKeys` is optional and defaults to `['name', 'email', 'verified_email']`. (`requestAttributes` itself has no default; the `scopedKeys` helper just builds the array you then pass to it.) Examples:

- `scopedKeys({ openIdProvider: 'google' })` &rarr; `['openid:https://accounts.google.com:name', 'openid:https://accounts.google.com:email', 'openid:https://accounts.google.com:verified_email']`
- `scopedKeys({ openIdProvider: 'google', keys: ['email'] })` &rarr; `['openid:https://accounts.google.com:email']`

The same `email` vs `verified_email` rule applies to scoped keys: use the verified variant when the email gates access.

```javascript
import { AuthClient } from "@icp-sdk/auth/client";
import { AttributesIdentity } from "@icp-sdk/core/identity";
import { HttpAgent, Actor } from "@icp-sdk/core/agent";
import { Principal } from "@icp-sdk/core/principal";

const II_PRINCIPAL = "rdmx6-jaaaa-aaaaa-aaadq-cai";

// `idl` and `canisterId` are your backend's interface factory and ID. The
// backend exposes _internet_identity_sign_in_start / _internet_identity_sign_in_finish.
async function signInWithAttributes(authClient, canisterId, idl) {
  // Anonymous handle, used only to mint the nonce.
  const anonymousAgent = await HttpAgent.create();
  const anonymousActor = Actor.createActor(idl, { agent: anonymousAgent, canisterId });

  // Mint the nonce, sign in, and request attributes in parallel. `nonce` is the
  // function that fetches it, called when the client needs the value, so the
  // request is in flight while the Internet Identity window opens and the user
  // still sees a single interaction. A frontend-generated nonce would defeat
  // replay protection — see Mistake #9.
  const signInPromise = authClient.signIn();
  const attributesPromise = authClient.requestAttributes({
    keys: ["name", "verified_email"], // library reads verified_email for its email field
    nonce: () => anonymousActor._internet_identity_sign_in_start(),
  });

  const identity = await signInPromise;
  const attributes = await attributesPromise;

  // Wrap the identity so the signed bundle travels as sender_info on each call.
  const verifiedAgent = await HttpAgent.create({
    identity: new AttributesIdentity({
      inner: identity,
      attributes,
      // The Internet Identity backend canister is the trusted attribute signer.
      signer: { canisterId: Principal.fromText(II_PRINCIPAL) },
    }),
  });
  const verifiedActor = Actor.createActor(idl, { agent: verifiedAgent, canisterId });

  // The backend verifies signer, origin, nonce, and freshness, then runs its
  // onVerified logic. Returns { ok } on success, { err } otherwise.
  const result = await verifiedActor._internet_identity_sign_in_finish();
  if ("err" in result) {
    throw new Error(`Attribute verification failed: ${JSON.stringify(result.err)}`);
  }
  return identity;
}
```

Each signed bundle carries three implicit fields the backend MUST verify:
- `implicit:nonce` — matches a single-use nonce the canister issued and consumes on sign-in, so a captured bundle cannot be replayed.
- `implicit:origin` — the frontend origin, preventing a malicious dapp from forwarding bundles to a different backend.
- `implicit:issued_at_timestamp_ns` — issuance time, letting the canister reject stale bundles even when the nonce is still valid.

For OpenID one-click sign-in, scope the attributes to the provider with the `scopedKeys` helper: authentication and attribute sharing happen in a single step (no extra prompt). Construct the client with `openIdProvider`, then swap the `keys` for the scoped forms. The rest of `signInWithAttributes` above is unchanged.

```javascript
import { AuthClient, scopedKeys } from "@icp-sdk/auth/client";

const authClient = new AuthClient({
  openIdProvider: "google",
});

// In signInWithAttributes, request the Google-scoped keys instead. They arrive
// in the bundle as e.g. "openid:https://accounts.google.com:verified_email",
// and the mo:identity-attributes library maps them onto the same name/email fields.
const attributesPromise = authClient.requestAttributes({
  keys: scopedKeys({ openIdProvider: "google", keys: ["name", "verified_email"] }),
  nonce: () => anonymousActor._internet_identity_sign_in_start(),
});
```

### Backend: Reading Identity Attributes

The backend exposes two methods the frontend calls: `_internet_identity_sign_in_start` (mints a nonce) and `_internet_identity_sign_in_finish` (verifies the wrapped bundle and runs your logic). The checks are the same in both languages — the bundle must be signed by a *trusted* signer, its `implicit:origin` must be one you allow, its `implicit:issued_at_timestamp_ns` must be fresh, and its `implicit:nonce` must be one you issued and have not consumed — but Motoko gets them from a library and Rust does them by hand.

**Always verify the signer.** The IC checks that the bundle is signed; it does not check *who* signed it. Any canister can produce a valid bundle. The trusted signer for II is `rdmx6-jaaaa-aaaaa-aaadq-cai`.

#### Motoko: the `mo:identity-attributes` mixin

Add the library to `mops.toml`:

```toml
[dependencies]
identity-attributes = "0.4.1"
core                = "2.5.0"

[toolchain]
moc = "1.6.0"
```

`include IdentityAttributes({ onVerified })` injects both sign-in methods and runs your `onVerified` callback only on a bundle that passes every check. It resolves the bundle to `{ name : ?Text; email : ?Text; sso : ?Text }` — `email` comes from the `verified_email` key (or its `openid:` / `sso:` scoped form), which is why the frontend requests `verified_email`. `sso` is the matched trusted domain when name/email came from `sso:` keys, otherwise `null`.

```motoko
import IdentityAttributes "mo:identity-attributes";
import Map "mo:core/Map";
import Principal "mo:core/Principal";

persistent actor {
  type Profile = { name : ?Text; email : ?Text; sso : ?Text };

  let profiles = Map.empty<Principal, Profile>();

  // Injects _internet_identity_sign_in_start / _internet_identity_sign_in_finish.
  // onVerified runs only on a bundle that passed the signer, origin, nonce, and
  // freshness checks.
  include IdentityAttributes({
    onVerified = func(caller, attrs) {
      profiles.add(caller, attrs);
    };
  });

  public query func getProfile(caller : Principal) : async ?Profile {
    profiles.get(caller)
  };
};
```

Configure the env vars in `icp.yaml` so `icp deploy` sets them on the canister:

```yaml
canisters:
  - name: backend
    settings:
      environment_variables:
        # II backend principal (required). List your local II principal too if tests run against it.
        trusted_attribute_signers: "rdmx6-jaaaa-aaaaa-aaadq-cai"
        # Allowed frontend origins, comma-separated (required).
        frontend_origins: "https://your-app.icp.net"
        # Trusted SSO domains, comma-separated (optional; omit to reject all sso:* keys).
        trusted_sso_domains: "your-org.com"
```

If `trusted_attribute_signers` is unset the bundle is rejected as untrusted; if `frontend_origins` is unset `_internet_identity_sign_in_finish` returns `#err(#FrontendOriginsNotConfigured)`. Both are the right behavior: an unconfigured canister must not trust attribute bundles. The method returns `Result<(), IdentityAttributesError>`; the error variants (`#NoAttributes`, `#MalformedCandid`, `#FrontendOriginMismatch`, `#Stale`, `#UnknownNonce`, `#AmbiguousAttribute`, `#UntrustedSsoSource`, `#MixedSsoSources`) tell the frontend whether to retry with a fresh nonce or surface a bug.

#### Rust: implement the same two methods by hand

There is no CDK wrapper yet (`ic-cdk >= 0.20.1`), so write the two methods yourself. `_internet_identity_sign_in_start` mints a nonce and stores it; `_internet_identity_sign_in_finish` checks the signer with `msg_caller_info_signer()`, decodes the ICRC-3 `Value::Map` from `msg_caller_info_data()`, and verifies origin, freshness, and the nonce before reading attributes. This mirrors what the Motoko library does internally. The bundle's entries are:

- `implicit:nonce` (Blob) — must match a nonce this canister minted and not yet consumed.
- `implicit:origin` (Text) — must match a trusted frontend origin.
- `implicit:issued_at_timestamp_ns` (Nat) — reject if outside your freshness window.
- The attribute keys you requested (e.g. `"verified_email"`, or the `openid:` / `sso:` scoped form).

```rust
use candid::{decode_one, CandidType, Deserialize, Principal};
use ic_cdk::api::{msg_caller, msg_caller_info_data, msg_caller_info_signer, time};
use ic_cdk::update;
use std::cell::RefCell;
use std::collections::HashSet;

const II_PRINCIPAL: &str = "rdmx6-jaaaa-aaaaa-aaadq-cai";
const TRUSTED_ORIGIN: &str = "https://your-app.icp.net";
const FRESHNESS_NS: u64 = 300_000_000_000; // 5 minutes

thread_local! {
    // Nonces issued by sign_in_start and consumed by sign_in_finish.
    static PENDING_NONCES: RefCell<HashSet<Vec<u8>>> = RefCell::new(HashSet::new());
}

// Mirrors the mo:identity-attributes Result so the frontend's `"err" in result`
// check works against either backend.
#[derive(CandidType)]
enum SignInResult {
    #[serde(rename = "ok")]
    Ok,
    #[serde(rename = "err")]
    Err(String),
}

#[derive(CandidType, Deserialize)]
enum Icrc3Value {
    Nat(candid::Nat),
    Int(candid::Int),
    Blob(Vec<u8>),
    Text(String),
    Array(Vec<Icrc3Value>),
    Map(Vec<(String, Icrc3Value)>),
}

fn lookup_text<'a>(entries: &'a [(String, Icrc3Value)], key: &str) -> Option<&'a str> {
    entries.iter().find_map(|(k, v)| match v {
        Icrc3Value::Text(s) if k == key => Some(s.as_str()),
        _ => None,
    })
}

fn lookup_blob<'a>(entries: &'a [(String, Icrc3Value)], key: &str) -> Option<&'a [u8]> {
    entries.iter().find_map(|(k, v)| match v {
        Icrc3Value::Blob(b) if k == key => Some(b.as_slice()),
        _ => None,
    })
}

fn lookup_nat<'a>(entries: &'a [(String, Icrc3Value)], key: &str) -> Option<&'a candid::Nat> {
    entries.iter().find_map(|(k, v)| match v {
        Icrc3Value::Nat(n) if k == key => Some(n),
        _ => None,
    })
}

// Mint a fresh nonce. The frontend calls this anonymously before sign-in.
#[update]
async fn _internet_identity_sign_in_start() -> Vec<u8> {
    let nonce = ic_cdk::management_canister::raw_rand()
        .await
        .expect("raw_rand failed");
    PENDING_NONCES.with_borrow_mut(|n| n.insert(nonce.clone()));
    nonce
}

// Runs every check the mo:identity-attributes mixin runs internally.
fn verified_attributes() -> Result<Vec<(String, Icrc3Value)>, String> {
    // 1. Trusted signer: the IC checks the signature, not who signed it.
    let trusted = Principal::from_text(II_PRINCIPAL).unwrap();
    if msg_caller_info_signer() != Some(trusted) {
        return Err("Untrusted attribute signer".to_string());
    }

    // 2. Decode the bundle as an ICRC-3 Value::Map.
    let value: Icrc3Value =
        decode_one(&msg_caller_info_data()).map_err(|_| "Malformed attribute bundle".to_string())?;
    let Icrc3Value::Map(entries) = value else {
        return Err("Expected attribute map".to_string());
    };

    // 3. Origin must be one we allow.
    let origin = lookup_text(&entries, "implicit:origin").ok_or("Missing origin")?;
    if origin != TRUSTED_ORIGIN {
        return Err(format!("Untrusted frontend origin: {origin}"));
    }

    // 4. Bundle must be fresh.
    let issued_at: u64 = lookup_nat(&entries, "implicit:issued_at_timestamp_ns")
        .ok_or("Missing timestamp")?
        .0
        .clone()
        .try_into()
        .map_err(|_| "Timestamp out of range".to_string())?;
    if time() > issued_at + FRESHNESS_NS {
        return Err("Bundle too old".to_string());
    }

    // 5. Nonce must be one we issued and have not consumed yet.
    let nonce = lookup_blob(&entries, "implicit:nonce").ok_or("Missing nonce")?;
    if !PENDING_NONCES.with_borrow_mut(|n| n.remove(nonce)) {
        return Err("Unknown or already-consumed nonce".to_string());
    }

    Ok(entries)
}

#[update]
fn _internet_identity_sign_in_finish() -> SignInResult {
    let entries = match verified_attributes() {
        Ok(entries) => entries,
        Err(e) => return SignInResult::Err(e),
    };

    // Your app logic. verified_email gates access — see Mistake #12.
    let Some(email) = lookup_text(&entries, "verified_email") else {
        return SignInResult::Err("Missing verified_email".to_string());
    };
    let caller = msg_caller();
    let name = lookup_text(&entries, "name");
    // e.g. persist a profile keyed by `caller` here.
    let _ = (caller, email, name);

    SignInResult::Ok
}
```

### Backend: Access Control

Backend access control (anonymous principal rejection, role guards, caller binding in async functions) is not II-specific — the same patterns apply regardless of authentication method. See the **canister-security** skill for complete Motoko and Rust examples.

## Older API notes

Everything above targets `@icp-sdk/auth` 9.x. On an older major the same flow differs:

**8.x** — what 9.x changed:

- `identityProvider` was a URL string; it is now `{ authorizeUrl, canisterId }`, and a string throws.
- `storage` and its `IdbStorage` / `LocalStorage` classes became `credentialStorage` with `IdbCredentialStorage` (the default), `LocalCredentialStorage`, `MemoryCredentialStorage` and `SharedMemoryCredentialStorage`. `stateStorage` is new and holds the record of who is signed in, which is what makes tabs converge; `CookieStateStorage` extends that to sibling subdomains.
- `IdleManager` and its options (`idleOptions`, `onIdle`, `idleTimeout`, `disableIdle`) were removed. The session is bounded at Internet Identity instead, via `maxTimeToIdle` and `maxTimeToLive` on `signIn()`.
- `maxTimeToLive` bounded a delegation and capped every sign-in at 8 hours; it now bounds the session, and unset means the provider's own 30 days.
- `getStatus()`, `subscribe()`, `getPrincipal()` and `dispose()` are new; the `identity`, `keyType` and `targets` options are gone.
- See the [v9 upgrade guide](https://js.icp.build/auth/latest/upgrading/v9/) for the full list.

**5.x** — a callback-based API:

- `await AuthClient.create({...})` instead of `new AuthClient({...})`
- `identityProvider` passed per-call to `login({...})` rather than at construction
- `authClient.login({ onSuccess, onError })` — promise wrapper required around it
- `authClient.logout()` instead of `authClient.signOut()`
- `await authClient.isAuthenticated()` (async) instead of sync
- `authClient.getIdentity()` (sync) instead of async
- 5.x auto-appends `/authorize` to the `identityProvider` URL, so you can pass just `https://id.ai`.
- No `requestAttributes` / `AttributesIdentity` support — the identity-attributes flow above requires 7.x or later.

Upgrade when you can: the promise-based API is harder to misuse, the callback variant has been removed, and 9.x re-mints the delegation your calls are signed with instead of leaving one key alive for the whole session.
