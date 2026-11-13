---
name: api-design
domain: software-engineering/api-design
trigger: "\"Design this endpoint\", \"REST or GraphQL or gRPC\", \"what should the error response look like\", \"add pagination\", \"make this POST safe to retry\", \"write the OpenAPI spec\"."
anti_trigger: "Changing or retiring a contract that clients already use (subskills/api-versioning.md); internal module interfaces; authN/authZ controls (out of this tree)."
scope: "Public API style, resource and error model, pagination, idempotency, OpenAPI"
status: "seedling"
---

# API Design

## Standard

- **OpenAPI Specification** (https://spec.openapis.org) is the contract of record for HTTP APIs. Protobuf (https://protobuf.dev) for gRPC.
- **HTTP semantics**: RFC 9110. GET, HEAD, PUT, DELETE are idempotent (§9.2.2). POST is not.
- **Errors**: RFC 9457 Problem Details (2023, obsoletes RFC 7807): `application/problem+json` with `type`, `title`, `status`, `detail`, `instance` (https://www.rfc-editor.org/info/rfc9457).
- **Idempotency-Key** header: IETF draft-ietf-httpapi-idempotency-key-header. ⚠️ Draft, not an RFC. Adopt the semantics, not a dependency.
- **Style guides**: Google AIPs (https://google.aip.dev; AIP-131–136 standard methods, AIP-158 pagination, AIP-193 errors), Microsoft REST Guidelines, Zalando guidelines.
- **Lint**: Spectral for OpenAPI, Buf for Protobuf.

## Decision rules

1. Style: REST + OpenAPI for public and partner APIs. gRPC for internal typed service-to-service calls and streaming. GraphQL when many clients need different shapes of one graph; budget for N+1 and query cost control.
2. Resources are plural nouns (`/orders/{id}`). Verbs come from HTTP methods. Custom actions use AIP-136 style (`POST /orders/{id}:cancel`).
3. Status codes: 200/201/204 success; 400 malformed; 401 unauthenticated; 403 forbidden; 404 not found; 409 conflict; 422 valid syntax but failed rules; 429 throttled with `Retry-After`; 5xx server fault. Never return 200 with an error body.
4. Every error uses one RFC 9457 shape. `type` is a stable URI clients can branch on.
5. Every mutating POST accepts `Idempotency-Key`. Same key + same payload → same stored response. Same key + different payload → 409.
6. List endpoints paginate from day one. Use opaque cursor tokens (`page_token`, `next_page_token`) with a server-capped `page_size`. Offset pagination only for small, static sets.
7. New fields are optional with a default that keeps old behaviour.
8. One casing per API; timestamps RFC 3339 UTC; money as integer minor units plus currency.
9. Design-first for public APIs. Code-first is fine if the spec is generated and committed.

## Procedure

1. List resources, fields and relations from the spec.
2. Write `openapi.yaml`: paths, methods, request and response schemas, one `Problem` schema.
3. Per operation, record: idempotent? paginated? auth scope? rate limit?
4. Add `Idempotency-Key` to mutating POSTs. Store key, payload hash and response for a set window. ⚠️ Window length is per-org (e.g. Stripe 24 h, vendor-specific).
5. Add pagination parameters to every list.
6. Lint: `npx @stoplight/spectral-cli lint openapi.yaml`. Fix all errors.
7. Generate stubs, client types and reference docs from the spec.
8. Write contract tests that check the running server matches the spec.
9. Review the spec with one consumer, then commit it as the breaking-change baseline.

## Anti-patterns

- 200 with `{"error": …}`; a different error shape per endpoint.
- Unbounded lists; retry-unsafe POST with no key.
- Database columns leaked as API fields; spec and code that drift.

## Done checklist

- [ ] OpenAPI spec committed and lint-clean.
- [ ] One RFC 9457 error schema used everywhere.
- [ ] Mutating POSTs take `Idempotency-Key`.
- [ ] All lists paginated with a cap.
- [ ] Contract tests pass.
- [ ] Docs generated from the spec.

## Sources

- <https://martinfowler.com/articles/richardsonMaturityModel.html>
- <https://dspace.mit.edu/bitstream/handle/1721.1/155197/3639477.3639713.pdf>
- <https://ilirivezaj.com/insights/api-first-development>
- https://www.rfc-editor.org/info/rfc9457 · https://google.aip.dev
