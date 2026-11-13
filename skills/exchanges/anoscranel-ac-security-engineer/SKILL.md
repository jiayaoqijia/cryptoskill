---
name: ac-security-engineer
license: MIT
description: "Hardens software against attack across the whole lifecycle. Use when threat-modelling a feature or system, reviewing a change for security defects, picking a verification target against OWASP ASVS, or fixing findings in input handling, injection, browser-side attacks, authentication, sessions and tokens, authorization, API security, secrets, cryptography, SSRF, file uploads or deserialization. Also covers supply-chain and CVE triage, security testing gates, LLM and agent tool security, privacy duties, abuse and rate limiting, security logging, incident first response and vulnerability disclosure. Not for writing prose documentation, building release pipelines, running infrastructure operations, or offensive penetration testing against systems the user does not own — those tasks sit outside application hardening."
metadata:
  domain: security-hardening
---

# Security Engineer

Application security, end to end: from "what can go wrong with this design" to
"we were breached, what now". Every leaf holds its full procedure — nothing here
hands work to another skill.

## When to use

Any task whose subject is an attacker: designing a system, reviewing a diff,
choosing a verification target, hardening an endpoint, triaging a CVE, storing a
secret, or cleaning up after an incident. Test phrase: "is this endpoint secure?"

## When not to use

Writing prose docs, building or fixing release pipelines, operating
infrastructure day to day, or attacking systems you do not own — no leaf here
covers them.

## The professional workflow

Threat-model the design → pick the verification level → build the defences
(validate input, encode output, parameterise, authenticate, authorise per
object, bound consumption) → store and rotate secrets → prove it with tests and
scans → log the right events → know the incident first hour before you need it.

## Precedence rule

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:`
> string is claimed by exactly one file in this tree; no leaf may widen a prohibition
> declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Task | Trigger |
|---|---|---|
| `subskills/00-rsi.md` | RSI event log | After any leaf in this skill fires |
| `subskills/threat-model.md` | Threat-model a system or feature | "What can go wrong here?" |
| `subskills/secure-design.md` | Design with trust boundaries and safe defaults | "How should this fail closed?" |
| `subskills/verification-level.md` | Choose and apply an ASVS verification target | "What level must this app meet?" |
| `subskills/input-output.md` | Validate input and encode output | "How do I handle untrusted data?" |
| `subskills/injection.md` | Stop SQL, command and template injection | "Make this query injection-proof" |
| `subskills/browser-security.md` | Defend the browser side: XSS, CSRF, headers, cookies | "Stop XSS or CSRF here" |
| `subskills/authentication.md` | Passwords, MFA, passkeys, recovery | "How do users log in and recover?" |
| `subskills/sessions-tokens.md` | Sessions, JWTs, OAuth tokens, webhooks | "How long should a session live?" |
| `subskills/authorization.md` | Enforce who may do what to each object | "Stop user A reading user B's data" |
| `subskills/api-security.md` | Harden an API against the API Top 10 | "Is this endpoint bounded and safe?" |
| `subskills/secrets.md` | Store, scan, rotate, respond to leaks | "Where does this key live? It leaked — now what?" |
| `subskills/crypto-use.md` | Use vetted cryptography correctly | "How do I encrypt this? Which hash?" |
| `subskills/ssrf.md` | Block server-side request forgery | "The server fetches a user URL — make it safe" |
| `subskills/file-upload.md` | Accept and serve uploads safely | "Let users upload files safely" |
| `subskills/deserialization.md` | Parse untrusted data safely | "This library deserialises — is that safe?" |
| `subskills/supply-chain.md` | Pin, sign and vet dependencies and builds | "Trust what I install and ship" |
| `subskills/cve-triage.md` | Prioritise vulnerable dependencies | "A dependency has a CVE — how urgent?" |
| `subskills/security-testing.md` | Gate code with security scans in CI | "Catch security bugs before merge" |
| `subskills/llm-prompt-injection.md` | Defend LLM features against injection | "Can a prompt hijack the model?" |
| `subskills/agent-tools.md` | Constrain what an agent's tools may do | "What may this agent call?" |
| `subskills/privacy-data.md` | Handle personal data lawfully | "My duties for this user data?" |
| `subskills/abuse-rate-limits.md` | Rate-limit and defeat automated abuse | "Bots hammer signup — throttle" |
| `subskills/security-logging.md` | Log security events, never secrets | "What events must I log and alert on?" |
| `subskills/security-incident.md` | First hour of a suspected breach | "We were breached — what first?" |
| `subskills/vuln-disclosure.md` | Receive and handle external reports | "A researcher reported a bug — process?" |
| `subskills/cloud-iac.md` | Harden cloud accounts and IaC | "Is this cloud account and IaC safe?" |
| `subskills/containers.md` | Build and run containers safely | "Harden this image and runtime" |
| `subskills/security-review.md` | Review one diff against the target level | "Is this change safe to merge?" |

## Hard lines (human-gated acts)

Propose, never execute: deploying to production, deleting data, dropping schema,
force-pushing, publishing, sending or submitting, releasing a version, rotating
or revoking credentials, disclosing a vulnerability externally, or claiming
authorship of AI-generated text.

## Sources

- OWASP Top 10 — **2025 edition current** (announced 2025-11-06, final Jan 2026); 2021 superseded. https://owasp.org/Top10/2025/
- OWASP API Security Top 10 — **2023 current; no newer official edition**. https://owasp.org/API-Security/editions/2023/en/0x04-release-notes
- OWASP ASVS 5.0.0 (2025-05-30): 14→17 chapters, full renumbering, v4 IDs stale; L2 the target for personal or payment data. https://asvs.dev
- OWASP Top 10 for LLM Applications 2025 and Top 10 for Agentic Applications (final 2025-12-09). ⚠️ the Agentic list was read from secondaries.
- NIST SP 800-53 Rev 5, SP 800-207, SP 800-63B-4 (final July 2025), SP 800-218 SSDF (1.1 final; 1.2 draft), SP 800-57, FIPS 203/204/205, IR 8547.
- CWE Top 25 2025 and the CISA KEV list; NVD/CVSS 4.0 for scoring.

See Also: each leaf names its siblings where a boundary sits.
