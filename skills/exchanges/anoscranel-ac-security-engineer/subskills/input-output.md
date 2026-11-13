---
name: input-output
domain: security-hardening/input-output
trigger: Handling any data that enters or leaves the program — user input, headers, uploads, webhooks, third-party responses, LLM output — and deciding how to validate and encode it.
anti_trigger: Fixing one specific interpreter bug such as SQL injection (subskills/injection.md); browser-executed attacks like XSS (subskills/browser-security.md).
scope: Allow-list validation, contextual output encoding, canonicalisation
status: seedling
---

# Input Validation and Output Encoding

## Standard

- OWASP Proactive Controls C3: Validate All Input & Handle Exceptions (v4, 2024) — validation happens server-side, on trusted infrastructure, as a positive (allow-list) model (https://top10proactive.owasp.org/the-top-10/c3-validate-input-and-handle-exceptions/).
- OWASP Input Validation Cheat Sheet (https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html) and Mass Assignment Cheat Sheet.
- OWASP ASVS 5.0: V1.1.1 canonicalise once before validation; V1.2.1 contextual output encoding; V2 Validation & Business Logic (https://asvs.dev).
- "Untrusted by default" covers request headers, cookies, file uploads, webhook bodies, third-party API responses and LLM output — OWASP API Top 10 API10 (Unsafe Consumption of APIs).

## Decision rules

1. Allow-list, never deny-list: define expected type, length, range, format and charset; reject everything else. Deny-lists fail against encodings, Unicode and novel syntax.
2. Schema validation is the concrete tool: one schema per input (Zod, Pydantic, JSON Schema, OpenAPI) with **unknown fields rejected** — that rejects mass assignment too.
3. Validation reduces attack surface; it never replaces output encoding or parameterisation.
4. Canonicalise before validating: decode once, then check the decoded form.
5. Every error response is generic to the user and detailed in the server log with a correlation ID (A10:2025).

## Procedure

1. List every input channel of the feature: body, query, headers, cookies, files, webhook payloads, third-party responses, model output.
2. Write one schema per channel. Anchor every regex; use enums for fixed sets.
3. Validate server-side on every request, before any business logic runs.
4. Reject unknown fields; never bind a request body straight onto an ORM entity.
5. Define the output encoding rule per sink: HTML body, attribute, JavaScript, URL and CSS each need their own encoding (OWASP XSS Prevention Cheat Sheet; subskills/browser-security.md).
6. Route failures to one global handler that logs the truth and returns a minimal message.

## Anti-patterns

- Deny-lists ("block `<script>`, `'`, `--`").
- Client-side-only validation; it is a UX affordance, not a control.
- Trusting the `Content-Type` header or a filename extension as the file's real type.
- Treating an LLM's output, or a "trusted partner's" webhook, as already safe.

## Done checklist

- [ ] Every input channel has a named schema.
- [ ] Validation runs server-side, before business logic.
- [ ] Unknown fields are rejected everywhere.
- [ ] Each output sink has its contextual encoding defined.
- [ ] Canonicalisation happens once, before validation.
- [ ] Global error handler logs detail and returns a generic message.

## Sources

- Primary: OWASP Proactive Controls C3; OWASP Input Validation, Mass Assignment and XSS Prevention Cheat Sheets; OWASP ASVS 5.0 V1/V2; OWASP Top 10 2025 A05/A10; OWASP API Security Top 10 2023 API10.
- <https://cheatsheetseries.owasp.org>
- <https://owasp.org/www-project-application-security-verification-standard/>
