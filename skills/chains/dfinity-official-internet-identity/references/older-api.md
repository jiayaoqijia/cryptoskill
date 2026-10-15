# Older `@icp-sdk/auth` majors

SKILL.md targets `@icp-sdk/auth` 11.x. On an older major the same flow differs as follows.

## 10.x

The same API, except the SSO domain check:

- `isValidSsoDomain(domain, signal)` fetched `/.well-known/ii-openid-configuration` from the browser and returned a boolean; the organization had to serve it with `Access-Control-Allow-Origin: *`. 11.x removes it: a client built with `ssoDomain` checks the domain through Internet Identity and reports `getSsoStatus()`.
- `new AuthClient({ ssoDomain })` threw on a malformed domain; 11.x reports `{ state: 'invalid', reason }` from `getSsoStatus()` instead and never throws for the domain. 11.x also reports `invalid` for a port on any host other than a loopback host (`localhost`, `127.0.0.1`, `*.localhost`), and for a malformed name such as `foo..com` or `ab--cd.com`.

10.x peers `@icp-sdk/core@^6`.

## 9.x

The same API as 10.x. 10.x changed only its peer, from `@icp-sdk/core@^5` to `^6`, so 9.x is what you use if you are held on core 5. With core 6 a read-only session signs in instead of throwing "this session is read-only, which `@icp-sdk/auth` cannot act for yet".

## 8.x

What 9.x changed:

- `identityProvider` was a URL string; it is now `{ authorizeUrl, canisterId }`, and a string throws.
- `storage` and its `IdbStorage` / `LocalStorage` classes became `credentialStorage` with `IdbCredentialStorage` (the default), `LocalCredentialStorage`, `MemoryCredentialStorage`, and `SharedMemoryCredentialStorage`. `stateStorage` is new and holds the record of who is signed in, which is what makes tabs converge; `CookieStateStorage` extends that to sibling subdomains.
- `IdleManager` and its options (`idleOptions`, `onIdle`, `idleTimeout`, `disableIdle`) were removed. The session is bounded at Internet Identity instead, via `maxTimeToIdle` and `maxTimeToLive` on `signIn()`.
- `maxTimeToLive` bounded a delegation and capped every sign-in at 8 hours; it now bounds the session, and unset means the provider's own 30 days.
- `getStatus()`, `subscribe()`, `getPrincipal()`, and `dispose()` are new; the `identity`, `keyType`, and `targets` options are gone.

## 5.x

A callback-based API:

- `await AuthClient.create({...})` instead of `new AuthClient({...})`.
- `identityProvider` passed per call to `login({...})` rather than at construction.
- `authClient.login({ onSuccess, onError })`, which needs a promise wrapper.
- `authClient.logout()` instead of `authClient.signOut()`.
- `await authClient.isAuthenticated()` (async) instead of sync; `authClient.getIdentity()` (sync) instead of async.
- 5.x appends `/authorize` to the `identityProvider` URL, so passing `https://id.ai` works there.
- No `requestAttributes` / `AttributesIdentity`: the identity-attributes flow requires 7.x or later.

Upgrade when you can: the promise-based API is harder to misuse, and 9.x and later re-mint the delegation calls are signed with instead of keeping one key alive for the whole session.
