# Constitution Section Index

Routing table into the mirrored constitutional text. Read this file first, identify the
sections the action engages, then read only those line ranges. Never load the whole document.

The text lives in the registered `Cardano Constitution` source, one directory per enacted
version:

```
../../docs/sources/cardano-constitution/cardano-constitution-2/cardano-constitution-2.txt.md
```

Version and currency: see `constitution-meta.md`. Upstream version directories are immutable
once enacted — an amendment arrives as a new sibling directory (`cardano-constitution-3/`),
never as an edit to this file — so the line numbers below are stable for this version. If a
newer version directory exists, stop and follow `constitution-meta.md`.

## How to read a section

Each row gives the line where a section starts; the next row bounds it. Use `Read` with
`offset` set to the start line and `limit` covering the range. If a line number does not land
on the expected heading, recover by `Grep`-ing the full title from the Title column — full
titles are unique, but bare section numbers are not (every Article has a "Section 1").

Heading format in the document: articles and appendices are bold-only lines
(`**ARTICLE II. ...**`), their sections are `### **Section N ...**`, and appendix subsections
are `### **N. ...**`.

| Reference | Title | Line |
|-----------|-------|------|
| Preamble | PREAMBLE | 4 |
| Defined Terms | DEFINED TERMS | 39 |
| Article I | CARDANO BLOCKCHAIN TENETS AND GUARDRAILS | 89 |
| Article I.1 | Section 1 Guiding Tenets | 92 |
| Article I.2 | Section 2 Implementation of Guardrails | 136 |
| Article II | COMMUNITY AND GOVERNANCE | 154 |
| Article II.1 | Section 1 The Cardano Community | 157 |
| Article II.2 | Section 2 Participation Rights of ada owners | 171 |
| Article II.3 | Section 3 Decentralized Governance Framework | 203 |
| Article II.4 | Section 4 Delegated Representatives | 215 |
| Article II.5 | Section 5 Stake Pool Operators | 229 |
| Article II.6 | Section 6 Governance Action Standards | 235 |
| Article II.7 | Section 7 "Treasury Withdrawals" Action Standards | 257 |
| Article III | CONSTITUTIONAL COMMITTEE | 292 |
| Article III.1 | Section 1 Role and Scope | 295 |
| Article III.2 | Section 2 Composition and Terms | 311 |
| Article III.3 | Section 3 Election Process, No Confidence and Removal | 321 |
| Article III.4 | Section 4 Transparency and Conduct | 338 |
| Article IV | AMENDMENT PROCESS | 355 |
| Article IV.1 | Section 1 Amendment Rules | 358 |
| Appendix I | CARDANO BLOCKCHAIN GUARDRAILS | 367 |
| Appendix I.1 | 1. Introduction | 370 |
| Appendix I.2 | 2. Guardrails and Guidelines on "Parameter Update" actions | 673 |
| Appendix I.2.1 | 2.1. Critical Protocol Parameters | 694 |
| Appendix I.2.2 | 2.2. Economic Parameters | 767 |
| Appendix I.2.3 | 2.3. Network Parameters | 1062 |
| Appendix I.2.4 | 2.4. Technical/Security Parameters | 1293 |
| Appendix I.2.5 | 2.5. Governance Parameters | 1467 |
| Appendix I.2.6 | 2.6. Monitoring and Reversion of Parameter Changes | 1689 |
| Appendix I.2.7 | 2.7. Non-Updatable Protocol Parameters | 1716 |
| Appendix I.3 | 3. Guardrails and Guidelines on "Treasury Withdrawals" Actions | 1723 |
| Appendix I.4 | 4. Guardrails and Guidelines on "Hard Fork Initiation" actions | 1742 |
| Appendix I.5 | 5. Guardrails and Guidelines on "Update Committee" actions | 1791 |
| Appendix I.6 | 6. Guardrails and Guidelines on "New Constitution" actions | 1802 |
| Appendix I.7 | 7. Guardrails and Guidelines on "No Confidence" actions | 1816 |
| Appendix I.8 | 8. Guardrails and Guidelines on "Info" actions | 1825 |
| Appendix I.9 | 9. List of Protocol Parameter Groups | 1834 |
| Appendix II | SUPPORTING GUIDANCE | 1913 |
| Appendix II.1 | 1. Framing Notes | 1921 |
| Appendix II.2 | 2. Other Guidance | 1952 |

The document ends at line 1961.
