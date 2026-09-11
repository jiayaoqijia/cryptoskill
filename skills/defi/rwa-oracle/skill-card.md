## Description:

QXMP Oracle helps agents fetch real-world asset data and proof-of-reserve status for tokenized mining assets on the QELT blockchain.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prqelt](https://clawhub.ai/user/prqelt)

### License/Terms of Use:


## Use Case:

Developers and external agents use this skill to query QXMP asset portfolios, individual asset records, proof freshness, and proof-of-reserve status. It supports read-only RWA lookup workflows through the public QXMP REST API and optional QELT on-chain references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts QXMP and QELT services when answering asset and proof questions.

Mitigation: Use it for public lookup workflows and avoid including confidential business context in asset lookup prompts.

Risk: Returned valuation and proof data could be stale or misused as financial advice.

Mitigation: Report proof freshness and timestamps exactly, warn when proofs are stale, and avoid treating returned valuations as financial advice.

Risk: QXMP API requests can be rate limited.

Mitigation: Respect HTTP 429 responses and Retry-After headers, and cache stable proof data briefly as described in the artifact.

## Reference(s):

- [QXMP homepage](https://qxmp.ai)
- [QXMP RWA API base](https://api.qxmp.ai/api/v1/rwa)
- [QXMP Oracle asset reference](artifact/references/asset-types.md)
- [QXMP Oracle smart contracts](artifact/references/contracts.md)
- [QXMP OracleController on QELTScan](https://qeltscan.ai/address/0xB2a332dE80923134393306808Fc2CFF330de03bA)
- [QXMP ProofOfReserveV3 on QELTScan](https://qeltscan.ai/address/0x6123287acBf0518E0bD7F79eAcAaFa953e10a768)
- [QXMP DynamicRegistryV2 on QELTScan](https://qeltscan.ai/address/0xd00cD3a986746cf134756464Cb9Eaf024DF110fB)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON response fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public API lookups; no credentials required.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
