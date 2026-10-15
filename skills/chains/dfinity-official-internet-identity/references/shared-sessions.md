# Shared sessions across subdomains

`chat.example.com` and `hr.example.com` can share one sign-in: sign in on one and the others are signed in without a second visit to Internet Identity, and signing out on one signs the user out on all of them.

## 0. One derivation origin first

Principals are per origin, so every app must derive from **one** derivation origin, listed in that origin's `/.well-known/ii-alternative-origins` (see "Serving an app at more than one origin" in SKILL.md). Without it each subdomain gets its own principal and there is nothing to share; a shared cookie does not change that.

## 1. Share the record

Every app builds its client with the same derivation origin and the same cookie domain, so a sign-in on one writes a record the others read:

```javascript
import { AuthClient, CookieStateStorage, InteractionRequiredError } from "@icp-sdk/auth/client";

const clientOptions = {
  derivationOrigin: "https://auth.example.com",
  stateStorage: new CookieStateStorage({ domain: "example.com" }),
};
```

Choosing that domain means trusting every origin under it. Do not do it on a domain whose subdomains you do not control.

## 2. Acquire the sign-in on a `/reauth` route

An app that reads `signed-in-elsewhere` asks Internet Identity for its own credential for that account. It runs on page load with no user gesture, where a popup is blocked, so it uses `transport: "redirect"` on a route of its own, from a second client (`prompt` and `hint` are fixed when a client is built):

```javascript
// Runs on the /reauth route.
async function reauth() {
  const status = new AuthClient(clientOptions).getStatus();

  if (status.state !== "signed-in-elsewhere") {
    location.replace("/");
    return;
  }

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
      // Nothing to resume, so the shared record is stale: clear it, or every
      // app on the domain keeps sending the user back here.
      await authClient.signOut().catch(() => {});
    }
    location.replace("/");
  }
}

reauth();
```

Without `hint`, a provider holding more than one session refuses rather than guessing: `InteractionRequiredError` with `reason` `account_selection_required`. A mint for an unexpected account is rejected client-side as `AccountMismatchError`.

## 3. Declare the callback on every app origin

A redirect sign-in is delivered only to a callback the returning origin itself declares, so every app serves `/.well-known/ii-auth-callbacks` on its own origin (not once on the derivation origin), listing its own `/reauth`:

```json
{ "callbacks": ["https://chat.example.com/reauth"] }
```

The entry is matched exactly (the full URL, no fragment), and II reads the document cross-origin. With `@dfinity/static-site`, add a `_headers` block:

```
/.well-known/ii-auth-callbacks
  Content-Type: application/json
  Access-Control-Allow-Origin: *
```

Validation fails closed: undeclared, unreadable, or not exactly matching, and the sign-in never comes back. The route must also terminate locally: the response arrives in the URL fragment, and a `3xx` carrying none re-attaches it to wherever it forwards.

## 4. Pick it up on load, on every page

Every page, not only those requiring a sign-in, reads the status as it loads and hands `signed-in-elsewhere` to `/reauth` with the page to return to:

```javascript
const authClient = new AuthClient(clientOptions);
const status = authClient.getStatus();

// Only this state: signed-out and expired both mean a normal sign-in, and
// sending them to /reauth just bounces the user back.
if (status.state === "signed-in-elsewhere") {
  location.replace(`/reauth?next=${encodeURIComponent(location.pathname + location.search)}`);
}
```

## 5. Jump on load, ask afterwards

Once a page is open, the status of that same client can still turn `signed-in-elsewhere` (someone signs in on a sibling in another tab). Redirecting a page the user is working on throws away their work, so subscribe and offer the same redirect behind a button:

```javascript
authClient.subscribe(() => {
  if (authClient.getStatus().state === "signed-in-elsewhere") {
    showResumeDialog(() =>
      location.replace(`/reauth?next=${encodeURIComponent(location.pathname + location.search)}`),
    );
  }
});
```

## What ends a shared session

- `signOut()` ends the session at Internet Identity, clears this app's credentials, and removes the shared record. Siblings keep a delegation of their own until it expires (at most five minutes), then their next mint is refused and they read `signed-out`.
- `maxTimeToIdle` on `signIn()` ends the session when nobody uses any of the apps; omitted, Internet Identity applies seven days.
- A sign-in elsewhere replaces the browser's session: a sibling holding the old chain drops it on its next mint, leaves the shared record alone, and goes through `/reauth` silently.
