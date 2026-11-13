---
name: standards-map
domain: security-hardening/standards-map
trigger: "Asking which security standard applies, which edition is current, or what one governs — OWASP Top 10, ASVS levels, LLM/Agentic Top 10, NIST SSDF, EU CRA dates, EN 301 549."
anti_trigger: "Doing the governed work — building, fixing, triaging, or reviewing against a control; that craft sits outside this leaf (use ac-security-engineer)."
scope: "Edition and date of each security standard; what each governs; nothing about how to comply"
status: "seedling"
---

# Standards Map

## Standard

One lookup table per family: the standard, its current edition, and what it governs. Cite a primary URL per row; where none is carried, the row keeps a ⚠️ flag. Never state an edition this table cannot back.

### OWASP

| Standard | Current edition | Governs | Source |
|---|---|---|---|
| Top 10 | **2025** (2021 superseded) | The ten broadest web-app risk categories | https://owasp.org/Top10/2025/ |
| API Security Top 10 | **2023** — the only official API edition | API-specific risks | https://owasp.org/API-Security/editions/2023/en/0x04-release-notes |
| ASVS | **5.0.0** (2025-05-30): 14→17 chapters, every ID renumbered — v4 IDs are stale. ⚠️ a "~345 requirements" count circulates, not on the cited page | Verification requirements at three cumulative levels | https://asvs.dev |
| Top 10 for LLM Applications | **2025**: LLM01 Prompt Injection … LLM10 Unbounded Consumption | Risks in LLM-backed features | https://genai.owasp.org/llm-top-10/ |
| Top 10 for Agentic Applications | **Final 2025-12-09** ("for 2026"): ASI01 … ASI10. ⚠️ ASI list from agreeing secondaries | Risks in tool-calling agents | https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ |
| Automated Threats Handbook | **v1.30** (2026-03-17), OAT-001…OAT-021 | Automated-abuse vocabulary | https://owasp.org/www-project-automated-threats-to-web-applications/ |

### ASVS 5.0 levels

- **L1** — baseline, low assurance, black-box.
- **L2** — the target for apps holding personal data, moving money, or carrying business-critical functions. ⚠️ percentage splits are vendor-reported.
- **L3** — high assurance (medical, critical infrastructure).
- Chapters V1–V17 (https://asvs.dev). Picking a level is a business decision — outside this leaf.

### NIST and crypto

| Standard | Status | Governs | Source |
|---|---|---|---|
| SSDF, SP 800-218 | **v1.1 final (2022-02-03)**; v1.2 Rev.1 is an Initial Public Draft (2025-12-17), still Draft. Four practice groups | Secure development lifecycle practices | https://csrc.nist.gov/projects/ssdf/publications |
| SP 800-63B-4 | Final July 2025 | Digital identity | https://pages.nist.gov/800-63-4/ |
| FIPS 203 / 204 / 205 | Final 2024-08-13 | Post-quantum algorithms (ML-KEM, ML-DSA, SLH-DSA) | https://csrc.nist.gov/pubs/fips/203/final |
| IR 8547 | IPD only (2024-11-12); no final ⚠️ | PQC transition: 112-bit keys deprecated after 2030, disallowed after 2035 | https://csrc.nist.gov/pubs/ir/8547/ipd |
| SP 800-53 Rev 5 · 800-207 · 800-57 | Current per NIST CSRC | Controls · zero trust · key management | NIST CSRC pages (per entry) |

### Regulation

| Instrument | Dates that bind | Governs | Source |
|---|---|---|---|
| EU CRA, Regulation (EU) 2024/2847 | **Art. 14 reporting from 2026-09-11** (24 h early warning, 72 h notification; ⚠️ the severe-incident "one month" rests on secondaries); **full Regulation from 2027-12-11** (Art. 71(2), EUR-Lex primary) | Products with digital elements sold in the EU | https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R2847 |
| EN 301 549 | **V3.2.1** (2021, WCAG 2.1 AA) is OJ-cited with presumption of conformity today; V4.1.1 (2026-09-02, WCAG 2.2 AA) is **not yet OJ-cited** ⚠️ | ICT accessibility under the EAA | https://www.etsi.org/deliver/etsi_en/301500_301599/301549/ |

## Decision rules

Pick the row by the trigger phrase. Cite the edition the table carries; ⚠️-flagged rows keep the flag in the answer.

## Procedure

1. Match the question to a row. 2. Read back name, edition, scope, any ⚠️ flag. 3. Stop — the procedure lives in the craft skills.

## Anti-patterns

- Quoting the standard's procedures or checklists here.

## Done checklist

- [ ] Answer carries name + edition + flag exactly as the row states them.

## Sources

- Per-row URLs inline; editions checked against primary pages 2026-10.
- Also mapped: CWE Top 25 2025 · CISA KEV · NVD/CVSS 4.0 · CIS Docker Benchmark v1.8.0 · RFC 9116 `security.txt` · ISO/IEC 29147 (revision ⚠️).
- <https://owasp.org/Top10/>
- <https://csrc.nist.gov/pubs/sp/800/218/final>
