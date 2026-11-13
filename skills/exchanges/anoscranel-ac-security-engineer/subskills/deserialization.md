---
name: deserialization
domain: security-hardening/deserialization
trigger: Parsing any serialized data from an untrusted source — API payloads, queue messages, cookies, files, agent tool inputs — and needing to do it without executing attacker code.
anti_trigger: Generic schema validation of well-formed input (subskills/input-output.md); upload handling (subskills/file-upload.md).
scope: Unsafe deserialisation and parser hardening (XXE, YAML)
status: seedling
---

# Deserialization

## Standard

- OWASP Deserialization Cheat Sheet: the safest choice is not to accept serialized objects from untrusted sources; use a pure data format such as JSON; only deserialize signed data (integrity check); restrict allowed types to an allow-list (https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html).
- OWASP ASVS 5.0: **1.5.1** XML parsers restrictive, external entities disabled (XXE) (L1); **1.5.2** deserialisation of untrusted data enforces safe input handling — an allow-list of object types, and "deserialization mechanisms that are explicitly defined as insecure must not be used with untrusted input" (L2); **1.5.3** parsers for the same data type parse consistently (L3).
- CWE-502 mitigations: sign/seal the data (e.g. HMAC); populate a new object rather than deserialising; make sensitive fields transient; avoid unnecessary types and allow-list classes — noting "new gadgets are constantly being discovered, so this alone is not a sufficient mitigation".
- OWASP Top 10 2025 A08 (Software or Data Integrity Failures) is the owning category.

## Decision rules

1. JSON with a schema is the default for untrusted data. Native object deserialisation of untrusted data is the bug class.
2. Where a format with types is unavoidable: allow-list the permitted classes, sign the payload (HMAC) and verify before parsing.
3. Language-safe APIs: `.NET` — `BinaryFormatter` is dangerous, set `TypeNameHandling.None`; `Python` — `pickle` load/loads is unsafe on untrusted data, use `yaml.safe_load`; `PHP` — replace `unserialize()` with `json_decode()`; `Java` — restrict `ObjectInputStream` via a class filter (`resolveClass` look-ahead; JEP 290 `ObjectInputFilter` ⚠️ name from recall, the cheat-sheet extraction named `resolveClass` + SerialKiller).
4. XML: disable external entities and DTD processing entirely — that is XXE (CWE-611), not just deserialisation.
5. Parser consistency: all services parsing the same type must parse it the same way (ambiguous parsing becomes a smuggling channel).
6. CWE-502 notes no per-language safe-API table; the per-language guidance is the OWASP cheat sheet's.

## Procedure

1. Find every parse of untrusted data: request bodies, message queues, cookies, file contents, tool inputs.
2. Replace native deserialisation with JSON plus a schema (subskills/input-output.md).
3. Where typed formats must stay: sign the payload with HMAC, verify with constant-time compare, then parse with a class allow-list.
4. Configure the parser library: XXE off, DTDs off, depth and size limits on, strict JSON interop.
5. Never let a "trusted/internal" channel bypass the rule — queues and service meshes carry the same untrusted bytes.
6. Add a test: a crafted payload (gadget chain, XXE entity, typed object) must be rejected, not executed.

## Anti-patterns

- `pickle.loads`, `ObjectInputStream`, `BinaryFormatter` or `unserialize()` on request data.
- `TypeNameHandling.All` (or equivalent) on JSON.NET-style serializers.
- XML parsers with external entities enabled "temporarily".
- An internal endpoint that skips validation because "only our services call it".

## Done checklist

- [ ] Every untrusted-data parse point inventoried.
- [ ] Native object deserialisation removed or allow-listed and signed.
- [ ] XXE and DTDs disabled in every XML parser.
- [ ] Parser depth and size limits set.
- [ ] Crafted-payload rejection tests exist per entry point.
- [ ] No internal channel bypasses the rule.

## Sources

- Primary: OWASP Deserialization Cheat Sheet; OWASP ASVS 5.0 1.5.1–1.5.3; CWE-502.
- <https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html>
- <https://owasp.org/Top10/>
