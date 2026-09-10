## Description:

Assist with Bitcoin transactions, wallets, Lightning, and security decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and agents use this skill for concise Bitcoin wallet, transaction, Lightning Network, fee, privacy, and scam-avoidance guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet or transaction guidance can affect irreversible Bitcoin transfers.

Mitigation: Users should verify destination addresses on trusted devices and never share seed phrases or private keys.

Risk: Public block explorer lookups may disclose queried addresses or transaction IDs to the service.

Mitigation: Users should consider the privacy impact before querying public APIs and avoid unnecessary address reuse.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/bitcoin)
- [mempool.space Transaction API](https://mempool.space/api/tx/{txid})
- [mempool.space Address API](https://mempool.space/api/address/{address})

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls]

**Output Format:** [Markdown with inline shell commands and API endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only guidance; no credentials or executable helper scripts were detected.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
