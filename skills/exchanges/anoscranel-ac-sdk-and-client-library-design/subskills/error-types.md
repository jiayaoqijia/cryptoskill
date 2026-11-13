---
name: error-types
domain: software-engineering/error-types
trigger: "Designing the errors a client library throws."
anti_trigger: "Not for HTTP status code design, and not for logging strategy."
scope: "Errors a caller can act on, and the information they must carry."
status: seedling
---

# Error types

## Standard

A caller can only handle what it can distinguish. A library that throws a single error type with a message forces every caller to parse strings, which breaks the moment the message changes. A library that throws a small hierarchy separating retryable from terminal, and authentication from validation, lets a caller write handling that survives a version upgrade.

The information an error carries matters as much as its type. A retryable error should carry a suggestion of when to retry, since the library knows and the caller does not. A validation error should carry the field, since otherwise the caller must parse the server's prose. A request identifier should be attached to every error, because it is the only thing that makes a support conversation resolvable.

Primary sources: <https://www.rfc-editor.org/rfc/rfc9457> and <https://www.rfc-editor.org/rfc/rfc9110>.

## Decision rules

- Record the error hierarchy and the distinction each level encodes.
- Record which errors are retryable and whether the error carries a retry-after hint.
- Record the fields carried: status, code, request identifier, field, and cause.
- Record whether errors wrap the underlying cause, since losing it makes diagnosis impossible.
- Record the message's stability, which should be unstable, and the code's, which should be stable.
- Record how errors surface in each language idiom, since a thrown exception and a returned result are different promises.

## Procedure

1. List the failure modes the library can produce.
2. Group them into types by what a caller would do differently.
3. Record the fields each type carries.
4. Record retryability and any retry-after hint.
5. Record cause chaining and request identifiers.
6. Write the hierarchy with its distinctions.

## Anti-patterns

- One error type with a message the caller must parse.
- A code that changes between releases while callers switch on it.
- Retryable and terminal failures conflated, so callers retry forever or give up early.
- A request identifier absent, making support conversations guesswork.
- Losing the underlying cause when wrapping.

## Done checklist

- [ ] Hierarchy recorded.
- [ ] Retryability recorded per type.
- [ ] Fields recorded.
- [ ] Cause chaining recorded.
- [ ] Message and code stability recorded.
- [ ] Idiomatic surfacing recorded.

The error's stability also decides how callers switch on it: a code intended for programmatic handling must be treated as part of the public surface and versioned accordingly, while a message is free to change, and conflating the two is what produces callers that break on a typo fix.


## Sources

- Problem details for HTTP APIs: <https://www.rfc-editor.org/rfc/rfc9457>
- HTTP semantics: <https://www.rfc-editor.org/rfc/rfc9110>
- Error handling context: <https://www.w3.org/>
