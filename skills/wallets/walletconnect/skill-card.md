## Description: <br>
Connect AI agents to user wallets as a WalletConnect v2 DApp so they can request transactions and signatures without handling private keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bevanding](https://clawhub.ai/user/bevanding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to connect an AI agent to a user-controlled wallet, request wallet-approved transactions or signatures, list sessions, and disconnect WalletConnect sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent WalletConnect sessions can retain transaction request capability after setup. <br>
Mitigation: Use a low-value or dedicated wallet, protect ~/.walletconnect-requester/, and disconnect sessions when work is complete. <br>
Risk: Transaction and signature prompts can authorize harmful actions if recipient, amount, chain, contract call, or message details are misunderstood. <br>
Mitigation: Verify every wallet prompt before approval and avoid enabling raw transaction signing unless it is explicitly required. <br>
Risk: WalletConnect URIs and local session data are sensitive because they can support session-based requests. <br>
Mitigation: Do not share WalletConnect URIs or session files, review audit logs before sharing them, and restrict local file permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bevanding/walletconnect-requester) <br>
- [Security Model](references/SECURITY.md) <br>
- [WalletConnect Cloud](https://cloud.walletconnect.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON-capable command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce WalletConnect URIs, QR code files, session listings, transaction hashes, and signatures through the bundled Node.js script.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
