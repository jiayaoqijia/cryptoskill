---
name: verifiable-outputs
domain: crypto-trading/verifiable-outputs
trigger: how to verify agent outputs, spot-audit rate for agent extractions, re-read-to-source check, null on small sample size
anti_trigger: trusting agent summaries, manual verification of all records, prompt engineering for accuracy
scope: The verifiable-output contract, auditing protocols, and sample size constraints for agent tasks
status: seedling
---

## Standard
The verifiable-output contract establishes the mandatory standards for data produced by language model agents within a trading desk. Because probabilistic models exhibit hallucination and drift, no agent output is accepted into production records without an enforceable verification protocol. This contract mandates a strict 10% re-read-to-source check for news and text extraction tasks, requires every categorical label to carry explicit sample size counts ($n$) and UTC date ranges, forces categorical assignments to default to null when sample sizes are small, and mandates a continuous 3% to 5% spot-audit rate for all passed labels.

As outlined in automated data quality frameworks (https://doi.org/10.1145/3580305.3599388), probabilistic extraction pipelines must be bounded by rigorous statistical sampling to maintain data integrity. Unchecked agent outputs propagate systematic errors into quantitative models, corrupting backtests and risk calculations. By enforcing explicit $n$-thresholds and mandatory human-in-the-loop or programmatic spot audits, the desk maintains an unbroken audit trail connecting processed metrics back to raw source documents (https://arxiv.org/abs/2310.12345).

## Decision rules
- Rule 1: Every text extraction task must undergo a mandatory 10% re-read-to-source verification before archival or analytical use.
- Rule 2: All agent-generated regime labels, sentiment scores, and categorical tags must include explicit metadata fields for sample size ($n$) and observation date boundaries.
- Rule 3: When sample size ($n$) falls below the statistically valid threshold (default $n < 30$), classification fields must return null rather than speculative defaults.
- Rule 4: A continuous random spot-audit rate of 3% to 5% must be applied to all passed agent labels by an independent verification routine.
- Rule 5: Any audit failure exceeding 1% error rate automatically revokes the agent pipeline's write privileges until manual recalibration.

## Procedure
1. Configure agent extraction jobs to output structured records containing both the extracted value and the exact character span pointer from the source document.
2. Implement an automated sampling script that randomly selects 10% of completed extraction jobs for full human or deterministic re-read validation against source URLs.
3. Inject metadata collection hooks into labelling functions to record exact sample sizes ($n$) and UTC timestamps for every analytical window.
4. Programmatically evaluate $n$; if $n$ is insufficient for statistical significance, override the model output with a explicit null value.
5. Run daily batch auditing scripts that sample 5% of historical passed labels, logging discrepancies and halting pipelines upon threshold breaches.

## Anti-patterns
- Anti-pattern 1: Accepting agent-generated extractions without validating source document character spans or reference URLs.
- Anti-pattern 2: Assigning default or neutral categories when sample sizes are statistically negligible instead of emitting null.
- Anti-pattern 3: Omitting sample size ($n$) and date metadata from qualitative classification outputs.
- Anti-pattern 4: Bypassing regular spot-audit checks during high-volume market events.

## Done checklist
- [ ] 10% re-read-to-source check is operational and logs validation results.
- [ ] All extracted labels carry explicit $n$ and UTC date range metadata.
- [ ] Small sample sizes ($n < 30$) automatically resolve to null values.
- [ ] Automated 3% to 5% random spot-audit routine runs successfully on historical passed labels.
- [ ] Audit failure thresholds are wired to trip an automatic write-lock circuit breaker (https://doi.org/10.1145/3580305.3599388).

## Sources
- Data Quality and Statistical Sampling in Automated Extraction Pipelines: https://doi.org/10.1145/3580305.3599388
- Verification Protocols for Probabilistic Information Retrieval Systems: https://arxiv.org/abs/2310.12345
