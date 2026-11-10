---
name: organization-sign-in
description: "Set up an organization's own single sign-on for Internet Identity, so staff sign in to II-powered apps against Okta, Entra ID, Google Workspace or Auth0. Nothing registers with II: it discovers the configuration from /.well-known/ii-openid-configuration on the organization's domain. Covers the OIDC client, the discovery file and every field, per-app clients including salted-hash keys, gate_all_apps, stable_identifier_claim, the limits that reject the whole file, and II's caching windows. Use when an organization wants its employees to sign in with its own identity provider, when II offers no SSO for a domain that has published the file, or when an edit to that file has not taken effect yet. This is the organization's side, done by whoever administers the domain. For an app sending users there with ssoDomain, load user-sign-in. Do NOT use for signing in to II with a personal Google, Apple or Microsoft account, which is ordinary OpenID and needs none of this."
license: Apache-2.0
compatibility: "an OIDC provider (Okta, Entra ID, Google Workspace or Auth0), HTTPS hosting for the organization's domain"
metadata:
  title: Organization Sign-In
  category: Auth
---

# Organization Sign-In

## What this is, and who does it

Internet Identity (II) authenticates an organization's staff against its own OpenID Connect provider (Okta, Entra ID, Google Workspace, Auth0). Nothing is registered with Internet Identity: it discovers the configuration from one file on the organization's domain.

This is work an organization's IT administrator does once, on the organization's own domain and identity provider. It is not app code, and no app can do it. The app side is one constructor option, `new AuthClient({ ssoDomain: "acme.com" })`, documented in the `user-sign-in` skill along with the `getSsoStatus()` check that tells an app whether a domain has SSO at all.

## 1. Register an OIDC client

In the identity provider, create an OIDC web application:

| Setting | Value |
|---|---|
| Redirect URI | `https://id.ai/callback` |
| Grant types | Authorization Code and Implicit (hybrid): II requests `response_type=code id_token` with `response_mode=form_post` |
| ID token | Allowed with the implicit grant |
| Access token | Not needed |
| Scopes | `openid`, `profile`, `email` |

## 2. Publish the discovery file

Serve it over HTTPS at exactly `https://<domain>/.well-known/ii-openid-configuration`:

```json
{
  "client_id": "0oaDEFAULT",
  "openid_configuration": "https://acme.okta.com/.well-known/openid-configuration",
  "name": "Acme Corp",
  "session_max_age_seconds": 28800,
  "app_clients": {
    "https://payroll.acme.com": "0oaPAYROLL"
  },
  "gate_all_apps": false,
  "stable_identifier_claim": "sub"
}
```

| Field | Required | Default | Meaning |
|---|---|---|---|
| `client_id` | yes |  | The client from step 1 |
| `openid_configuration` | yes |  | The provider's OIDC discovery URL |
| `name` | no | the domain | Label on the sign-in screen, and `available.name` from `getSsoStatus()` |
| `session_max_age_seconds` | no | `28800` (8 hours) | How long a sign-in through this domain stays valid; also caps an app's own session length |
| `app_clients` | no | none | Maps an app's exact origin, or a salted hash of it, to that app's own client |
| `gate_all_apps` | no | `false` | `true` refuses apps not listed in `app_clients` |
| `stable_identifier_claim` | no | `sub` | A claim that is the same for one person across all the organization's clients (Entra ID: `oid`, since its `sub` differs per client) |

No CORS header is required: Internet Identity fetches the file server-side, and `@icp-sdk/auth` 11.x checks a domain through II (`getSsoStatus()`), not from the browser. `isValidSsoDomain()` in 10.x and earlier fetched the file cross-origin, so keep `Access-Control-Allow-Origin: *` on it while any app on an older major still signs in through this domain.

The domain users enter is a bare domain such as `acme.com`, not `https://acme.com`, `acme.com/`, or a path.

## Per-app access

Give an app its own OIDC client, assign the allowed groups or users to that client in the provider (on Entra ID also set "Assignment required" to Yes), and add one `app_clients` line keyed by the app's exact origin. A trailing slash, a path, or a different scheme does not match, and the app then silently falls back to the organization's client.

To list an app without naming it in the public file, key it by a salted hash: `sha256(origin || salt)` as hex, then `:`, then the salt as hex:

```bash
origin=https://payroll.acme.com
salt=$(openssl rand -hex 8)
hash=$(printf %s "$origin$salt" | openssl dgst -sha256 -r | cut -d' ' -f1)
echo "$hash:$salt"
```

Cleartext and hashed keys can be mixed in one file. Changing `stable_identifier_claim` on a live domain changes how identities key onto anchors: treat it as a migration, not a config tweak.

## Limits: one bad value rejects the whole file

Internet Identity rejects the entire file, not just the offending field, when any of these is exceeded. SSO is then unavailable for the whole domain (`getSsoStatus()` reads `unavailable`):

- the file larger than 64 KiB (the same limit applies to the provider's OIDC discovery document);
- more than 100 `app_clients` entries;
- an `app_clients` key or client id longer than 255 bytes;
- `app_clients` keys and client ids together longer than 16 KiB;
- `client_id`, `name`, or `stable_identifier_claim` longer than 255 bytes;
- `session_max_age_seconds` of `0` or above `2592000` (30 days); it is rejected, not clamped;
- in the OIDC discovery document: `issuer`, `jwks_uri`, or `authorization_endpoint` longer than 255 bytes.

## When changes take effect

Internet Identity caches each domain's discovery result:

- fresh for 1 hour; after that, the next sign-in through the domain starts a refresh and is served the cached result while it runs;
- kept for 7 days past freshness, so a domain signed in through within the week starts from the cache;
- a refresh that fails stops serving the old result 1 hour past freshness, then backs off (60 s, doubling) before retrying.

So removing an `app_clients` entry or enabling `gate_all_apps` applies after the next refresh, normally within an hour of active use; the first sign-in after a quiet period is checked against the cached result while the refresh runs. The provider's signing keys (JWKS) are cached separately for at most 1 hour past freshness, so key rotation is picked up within that window.

## What an organization cannot assert

**No `verified_email` under `sso:`.** An organization's SSO cannot produce a verified email. Its `sso:<domain>:email` is asserted by the organization's own provider, so an app trusts it only for domains it lists.
