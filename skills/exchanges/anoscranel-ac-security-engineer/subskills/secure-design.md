---
name: secure-design
domain: security-hardening/secure-design
trigger: "Designing or restructuring a system and needing the patterns that make it fail closed: trust boundaries, least privilege, safe defaults."
anti_trigger: "Enumerating threats for a design (subskills/threat-model.md); implementing a specific control such as authentication or authorization (subskills/authentication.md, subskills/authorization.md)."
scope: "Trust boundaries, least privilege, secure defaults, fail-closed"
status: "seedling"
---

# Secure Design

## Standard

- Saltzer & Schroeder 1975, *The Protection of Information in Computer Systems* — the design canon (https://doi.org/10.1109/proc.1975.9939).
- CISA/NSA *Shifting the Balance of Cybersecurity Risk* (2023): secure by design (security a core goal from the start) and secure by default (secure out of the box; security features at no extra cost) (https://www.cisa.gov/sites/default/files/2023-10/Shifting-the-Balance-of-Cybersecurity-Risk-Principles-and-Approaches-for-Secure-by-Design-Software.pdf).
- NIST SP 800-207 (zero trust architecture) for the never-trust-the-network stance.

## Decision rules

1. Everything crossing a trust boundary is untrusted input: browser→server, server→DB, your code→third-party API, LLM→tools. Draw the boundaries before writing code.
2. Deny by default. Permission is the exception; an unknown state is a denial.
3. Least privilege per component, not per user: each service, function and agent gets its own minimal credential.
4. Fail closed: a `try/except` that swallows a permission error is CWE-636 "not failing securely" (OWASP Top 10 A10:2025, https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/).
5. Complete mediation: every access to a protected object is checked, every time. "Logged-in" never means "authorised" (see subskills/authorization.md).
6. Economy of mechanism: one auth library, one crypto library, not three.
7. Defence in depth at small scale means two or three layers that fail independently and are cheap to keep — parameterised queries plus a restricted DB role beats ten overlapping controls nobody maintains.
8. For any AI feature, audit the lethal trifecta — access to private data + exposure to untrusted content + an external communication path — and cut one leg, usually egress (Simon Willison, 2025-06-16, https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/).

## Procedure

1. List every trust boundary in the system and mark it on the diagram (subskills/threat-model.md).
2. Assign each component a dedicated, minimally-scoped credential. No shared root keys.
3. Audit defaults: debug off in production, TLS on, MFA on by default, no default credentials, least-privilege DB and service roles.
4. For each boundary crossing, define the validation and encoding rule (subskills/input-output.md).
5. For AI features, write the trifecta analysis and record the removed leg in an ADR.
6. Record each security-significant decision as a one-page ADR with context, decision, alternatives and consequence-if-wrong (SSDF PO.1.2).

## Anti-patterns

- Secure-by-instructions: safe only if the operator configures it correctly.
- A single credential that both reads data and can exfiltrate it.
- Swallowing exceptions to keep a flow alive; roll partial work back instead.
- Bolting on controls after the architecture is frozen; A06 Insecure Design is a Top 10 category because design is where the fix is cheapest.

## Done checklist

- [ ] Every trust boundary is named and on the diagram.
- [ ] Each component has its own scoped credential.
- [ ] Defaults audit passes: no debug, no default credentials, TLS on, deny-by-default authz.
- [ ] Error paths roll back and never leak detail (CWE-209, CWE-636 checked).
- [ ] AI features carry a trifecta analysis with one leg removed.
- [ ] Security ADRs exist for each security-significant decision.

## Sources

- Primary: Saltzer & Schroeder 1975; CISA/NSA Shifting the Balance (2023); OWASP Top 10 2025 A06/A10; NIST SP 800-207; NIST SP 800-218; Willison lethal trifecta (2025).
- <https://shostack.org>
- <https://owasp.org/www-project-application-security-verification-standard/>
