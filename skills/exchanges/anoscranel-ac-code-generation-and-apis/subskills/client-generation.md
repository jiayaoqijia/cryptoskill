---
name: client-generation
domain: software-engineering/client-generation
trigger: "Using a generated API client and knowing what it does and does not promise."
anti_trigger: "Not for hand-designed public APIs, and not for SDK surface design."
scope: "Generated API clients and what their surface promises."
status: seedling
---

# Client generation

## Standard

A generated client turns a contract into methods: each operation becomes a callable function with typed inputs and outputs. The value is the elimination of hand-written request plumbing, and the limit is exactly the same: the client knows the shape of each call, and knows nothing about its behaviour. A method generated from a contract will happily construct the request it was generated to construct; whether the server honours it, how it fails, and what a retry does to a non-idempotent operation are properties of the contract and the runtime wiring.

Two decisions attach to a generated client. First, whether its call retry and timeout behaviour suits the operations it carries: a client-wide default is convenient and wrong for a mix of reads and writes, and some generators bake in an unsafe default. Second, where the boundary sits between the generated file and the application's wrapper: consumers should depend on a thin, owned wrapper so a regeneration can change the generated layer without rewriting call sites.

Primary source: <https://www.openapis.org/>.

## Decision rules

- Record what the generated client covers: all operations, or a chosen subset.
- Record the retry, timeout, and authentication defaults the generator bakes in.
- Verify per-operation whether idempotency assumptions are safe for any configured retries.
- Wrap the generated client behind an owned interface so regeneration does not touch call sites.
- Record the generator version alongside the contract version the client came from.
- Validate against a running server, not just a contract: generated tests against a stub prove only the stub.

## Procedure

1. Generate the client from the contract and record generator and contract versions.
2. Inspect the generated defaults for retry, timeout, and auth.
3. Correct or override unsafe defaults per operation class.
4. Wrap the client in an owned interface.
5. Run the generated request tests against a real or recorded server, not a stub.
6. Record the results and the wrapper boundary.

## Anti-patterns

- Accepting generator defaults for retry on non-idempotent operations.
- Calling the generated client directly through the application.
- Generating all operations when a subset is used, exposing more breakage surface.
- Testing against a stub and calling the contract validated.
- Regenerating without checking the diff of the generated surface.

## Done checklist

- [ ] Generator and contract versions recorded.
- [ ] Defaults inspected and corralled.
- [ ] Idempotency of retries verified.
- [ ] Owned wrapper in place.
- [ ] Validated against a real server.
- [ ] Regeneration diff process recorded.

## Sources

- OpenAPI specification: <https://www.openapis.org/>
- HTTP method idempotency semantics: <https://www.rfc-editor.org/rfc/rfc9110>
- SDK design practice: <https://martinfowler.com/articles/practical-guide-pact.html>
