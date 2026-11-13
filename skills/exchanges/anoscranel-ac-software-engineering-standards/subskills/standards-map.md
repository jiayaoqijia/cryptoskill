---
name: standards-map
domain: software-engineering/standards-map
trigger: "\"what is the standard for\", \"which standard applies\", \"which edition is current\", \"which SWEBOK/SSDF practice applies\"."
anti_trigger: "Doing the governed task itself — designing, coding, testing, shipping, hardening — is out of scope for this leaf. This leaf names the authority, never the procedure."
scope: "The standards that govern the software domain: names, editions, dates, what each governs"
status: "seedling"
---

# Standards Map

## Standard

One lookup table: the standard, its current edition and date, and what it governs. Where a date is not carried in the source corpus, the row says so; never state an edition this table cannot back.

| Standard | Edition and date | Governs |
|---|---|---|
| SWEBOK v4 | IEEE Computer Society, October 2024 | The lifecycle topic map for the whole domain (https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics) |
| ISO/IEC/IEEE 29148 | 2018 ⚠️ cited from common practice; the corpus does not carry the text | Requirements engineering: what a good requirement is |
| ISO/IEC 25010 | 2023 | The product quality model: nine characteristics. ⚠️ Rename-from-2011 mapping from secondaries; ISO text paywalled (https://www.iso.org/standard/78176.html) |
| SemVer | 2.0.0 | Version numbers: MAJOR.MINOR.PATCH (https://semver.org) |
| Conventional Commits | 1.0.0 | Commit subjects that drive version bumps (https://www.conventionalcommits.org/en/v1.0.0/) |
| Keep a Changelog | 1.1.0 | Changelog shape (https://keepachangelog.com/en/1.1.0/) |
| OpenAPI Specification | Current edition at https://spec.openapis.org; pin per project | HTTP API contracts |
| HTTP semantics | RFC 9110, June 2022 | Method behaviour and status codes |
| Problem Details | RFC 9457, 2023 (obsoletes RFC 7807) | API error bodies |
| Sunset / Deprecation headers | RFC 8594 / RFC 9745 | Retirement signals for HTTP APIs |
| WCAG | 2.2: W3C Recommendation, first published 5 October 2023, current dated version 12 December 2024 | Accessibility. WCAG 3.0 is a Working Draft (10 September 2026) — never cite it as a requirement |
| DTCG Format | 2025.10 | Design tokens; a stable W3C Community Group report, not a W3C Standard |
| IEEE 1044 | Current; date not carried in this corpus ⚠️ | Failure / fault / defect vocabulary |
| OpenTelemetry | CNCF-graduated, current at opentelemetry.io | Traces, metrics and logs |
| NIST SSDF | SP 800-218 v1.1, Final, 3 February 2022 | Secure-development practices in four groups. v1.2 is a draft; comments closed 30 January 2026 |
| IEC 62304 | Edition 1.1, 2015-06-26 (2006+AMD1:2015) | Medical device software lifecycle; stability date 2028. Edition 2 not published (stage ACD) |
| DO-178C | Current; year not carried in this corpus ⚠️ | Airborne software; objectives-based |
| AAMI TIR45 | 2023 | Agile device software inside the QMS, FDA-recognized |
| OWASP | Editions not carried in this corpus ⚠️ | Top 10 is awareness, not a test plan; ASVS Level 1/2/3 is the verifiable set |

## Decision rules

Pick the row by the trigger phrase. Cite the edition the table carries; ⚠️-flagged rows keep the flag in the answer.

## Procedure

1. Match the question to a row. 2. Read back name, edition, date, scope, any ⚠️ flag. 3. Stop — the procedure lives in the craft skills.

## Anti-patterns

- Stating an edition or date not in the table.
- Quoting the standard's procedures or checklists here.

## Done checklist

- [ ] Answer carries name + edition + date + flag exactly as the row states them.

## Sources

- Per-row URLs inline; SWEBOK v4 topic map: <https://www.computer.org/education/bodies-of-knowledge/software-engineering/topics>.
