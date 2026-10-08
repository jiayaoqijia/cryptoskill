---
name: version-a-public-api
description: Use when exposing an HTTP or RPC API to external consumers. Chooses a versioning scheme and makes additive-only changes safe without breaking existing clients.
---

# Version a Public API

Once a client ships, its API surface is frozen by that client's deployment cadence. Choose how versions are expressed before the first external caller, because retrofitting versioning breaks live integrations.

## Procedure

1. Pick one scheme and write it down:
   - **URI path** (`/v1/users`) — most visible, easy to route and document. Default choice.
   - **Header** (`Accept: application/vnd.acme.v2+json`) — keeps URLs stable but is invisible in logs and hard to curl by hand.
   - **Query** (`?api-version=2024-06-01`) — used by Azure-style date versions; good for date-based evolution.
2. Represent the version in code as a namespace or mounted router, not scattered `if version ==` branches: `app.include_router(v1.router, prefix="/v1")`.
3. Change rules inside a version: **additive only**. New optional fields, new endpoints, new enum values when clients tolerate unknown values. Never remove, rename, narrow a type, or change a default in place.
4. Make clients tolerant: document that unknown fields must be ignored, and that unknown enum values must pass through rather than error.
5. Publish a machine-readable contract — an OpenAPI/protobuf schema per version — and run contract tests so a change that violates the rules fails CI:
   `openapi-diff old.json new.json --fail-on incompatible`.
6. Keep old versions served concurrently; route by prefix to a versioned handler module that shares the core logic.
7. Announce the version in a `Version` response header or the schema's `info.version` so consumers can confirm what they hit.

## Pitfalls

- Versioning the endpoint but changing shared serialization globally breaks every version at once.
- Adding a required field is breaking even with a new version number if old clients call the same path.
- Returning a 404 for an unknown enum value makes adding a case a breaking change.
- Date-based versions imply a schema is immutable for that date; mutating one mid-flight destroys the contract.
- Clients that send no version and get the newest default will break on every release; require an explicit version or pin a stable default.

## Verification

    openapi-diff v1.json v2.json --fail-on incompatible && \
      curl -sS -H 'Accept: application/json' https://api.example.com/v1/users | jq '.data[0] | keys'

The diff exits 0 for the same major version, and a v1 request still returns v1 shapes after the v2 deploy.

Report: "Added /v2 with OpenAPI contract; `openapi-diff` reports no incompatible change within v2, and v1 responses are byte-compatible for existing clients."
