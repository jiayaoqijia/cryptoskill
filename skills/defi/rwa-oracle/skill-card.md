## Description: <br>
Fetch real-world asset (RWA) data and proof-of-reserve status from the QXMP Oracle for tokenized assets, reserve proofs, valuations, portfolio statistics, and proof freshness without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PRQELT](https://clawhub.ai/user/PRQELT) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to query public QXMP/QELT real-world asset oracle data, report proof-of-reserve freshness, summarize portfolio statistics, and inspect individual tokenized mining assets. It supports read-only API lookups and optional on-chain verification references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Asset values and proof-of-reserve claims come from an external oracle and are not independent financial assurance. <br>
Mitigation: Treat reported values as external oracle data, cite proof timestamps and freshness status, and avoid presenting the data as audited financial advice. <br>
Risk: Proof data may be stale when latestProof.isFresh is false or when the proof is outside the expected update window. <br>
Mitigation: Report stale status plainly, include proof age when available, and avoid fabricating timestamps, values, or freshness claims. <br>
Risk: The public API can rate limit requests. <br>
Mitigation: Use short-lived caching and respect HTTP 429 Retry-After guidance before retrying. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/PRQELT/qelt-rwa-oracle) <br>
- [QXMP homepage](https://qxmp.ai) <br>
- [QXMP Oracle API base](https://api.qxmp.ai/api/v1/rwa) <br>
- [QXMP Oracle Asset Reference](references/asset-types.md) <br>
- [QXMP Oracle Smart Contracts](references/contracts.md) <br>
- [OracleController on QELTScan](https://qeltscan.ai/address/0xB2a332dE80923134393306808Fc2CFF330de03bA) <br>
- [ProofOfReserveV3 on QELTScan](https://qeltscan.ai/address/0x6123287acBf0518E0bD7F79eAcAaFa953e10a768) <br>
- [DynamicRegistryV2 on QELTScan](https://qeltscan.ai/address/0xd00cD3a986746cf134756464Cb9Eaf024DF110fB) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with API response summaries and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public API lookups; no API key required; values and proof freshness should be reported from live oracle responses.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
