## Description: <br>
Assist with Bitcoin transactions, wallets, Lightning, and security decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill for practical Bitcoin wallet, transaction, Lightning Network, fee, privacy, and scam-avoidance guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bitcoin addresses or transaction IDs queried through mempool.space may be revealed to that public service. <br>
Mitigation: Avoid querying addresses or transaction IDs that should not be linked to the user's usage. <br>
Risk: Bitcoin and Lightning guidance can affect irreversible transactions if copied into wallet actions without review. <br>
Mitigation: Review destination addresses, fees, confirmations, and hardware-wallet device prompts before broadcasting transactions. <br>


## Reference(s): <br>
- [mempool.space transaction API](https://mempool.space/api/tx/{txid}) <br>
- [mempool.space address API](https://mempool.space/api/address/{address}) <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/bitcoin) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only guidance; no credentials, persistence, or wallet actions were identified in the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
