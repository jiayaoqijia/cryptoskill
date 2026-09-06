## Description: <br>
Provides OKX Onchain OS workflows for token risk checks, DApp phishing detection, transaction and signature scans, and approval review guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to run or guide OKX Onchain OS security checks before interacting with tokens, DApps, transactions, signatures, and token approvals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to install or update a local OKX Onchain OS CLI from a remote release. <br>
Mitigation: Require explicit approval before any installer runs and verify release checksums before using the installed binary. <br>
Risk: Wallet-connected revoke, contract-call, broadcast, or swap paths can affect user assets. <br>
Mitigation: Require explicit approval before using the active wallet address or executing any transaction-related command. <br>
Risk: Broad wallet portfolio inspection can expose sensitive holdings or addresses when only a narrow check is needed. <br>
Mitigation: For simple token or URL checks, prefer explicit contract addresses or URLs instead of scanning an entire wallet portfolio. <br>


## Reference(s): <br>
- [Risk Approval Monitoring](references/risk-approval-monitoring.md) <br>
- [Risk Domain Detection](references/risk-domain-detection.md) <br>
- [Risk Token Detection](references/risk-token-detection.md) <br>
- [Risk Transaction Detection](references/risk-transaction-detection.md) <br>
- [OKX Web3](https://web3.okx.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/ok-james-01/okx-security) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and security recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk verdicts, warnings, approval review steps, and explicit user-confirmation prompts before sensitive actions.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
