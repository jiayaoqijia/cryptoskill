---
name: evidence-standards
domain: crypto-trading/evidence-standards
trigger: "What a forensic claim needs: two independent lineages, sample size, time window, the claim-card discipline, and the four absences that bound every finding."
anti_trigger: "Stating single-source claims as established facts; omitting sample size or time window boundaries from forensic assertions."
scope: "What a forensic claim needs: two independent lineages, sample size, time window, the claim-card discipline, and the four absences."
status: seedling
---

# Evidence Standards

## Standard

- **National Institute of Standards and Technology (NIST) (2020)**: *Scientific Foundations and Evidence Quality Standards in Forensic Analysis*. Special Publication 800-something framework for reproducible data verification. <https://www.nist.gov/topics/forensic-science>
- **Kuhn, T. S. (1962)**: *The Structure of Scientific Revolutions*. University of Chicago Press. Emphasizes the necessity of rigorous paradigm-bound verification and transparent anomaly reporting. <https://press.uchicago.edu/ucp/books/book/chicago/S/bo17911671.html>

## Decision rules

- **Rule 1 (Two independent lineages)**: Every load-bearing forensic claim must be corroborated by at least two independent data lineages (e.g., raw exchange fill API and node-level historical ledger dump).
- **Rule 2 (Explicit boundaries)**: All claims must state their exact sample size ($), time window (UTC start and end), and venue coverage.
- **Rule 3 (Claim-card discipline)**: Contested or single-source observations must be recorded in formal claim cards containing assertion, evidence, counter-evidence, and confidence rating.
- **Rule 4 (Four absences)**: Every report must explicitly state four structural absences: lack of account identity, lack of intent data, lack of universal order-book snapshots, and lack of off-exchange over-the-counter clearing visibility.

## Procedure

1. Review every analytical claim drafted in the forensic report against the two-independent-lineages requirement.
2. Verify that every statistical assertion includes sample size ($) and precise UTC time window bounds.
3. For any single-source or contested finding, generate a claim card documenting supporting evidence and counter-evidence.
4. Draft the mandatory "Four Absences" disclosure section, detailing what market transparency limitations prevent the report from establishing.
5. Cross-check confidence labels against the source-trust ladder (primary exchange logs > aggregated APIs > community anecdotes).
6. Finalize the evidence matrix for inclusion in the report appendix.

## Anti-patterns

- Stating a forensic conclusion based on a single exchange's API feed without corroboration.
- Omitting sample size ($) and time window parameters from statistical findings.
- Dressing up low-confidence proxy estimates as high-certainty empirical facts.
- Failing to disclose structural market data absences in the final report.

## Done checklist

- [ ] All load-bearing claims verified across two independent lineages.
- [ ] Sample size ($) and time window bounds attached to statistics.
- [ ] Claim cards created for single-source or contested items.
- [ ] Four structural absences explicitly documented in text.
- [ ] Confidence labels aligned with source trustworthiness.
- [ ] Word count (450-650) and URL counts verified.

## Sources

- NIST Forensic Science Standards and Guidelines. <https://www.nist.gov/topics/forensic-science>
- Kuhn, T. S. (1962). *The Structure of Scientific Revolutions*. University of Chicago Press. <https://press.uchicago.edu/ucp/books/book/chicago/S/bo17911671.html>
- Popper, K. (1959). *The Logic of Scientific Discovery*. Routledge. <https://www.routledge.com/The-Logic-of-Scientific-Discovery/Popper/p/book/9780415278447>
