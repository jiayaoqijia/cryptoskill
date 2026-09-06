## Description: <br>
Propose transactions to a Zeal Wallet. Use when the user wants to set up an agent as a Zeal Wallet signer, propose transactions, or manage a delegate wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nicvaniek](https://clawhub.ai/user/Nicvaniek) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External wallet users and agents use this skill to create or reuse a local agent wallet, connect it to a Zeal Wallet, submit transaction proposals on supported networks, and remove the local Zeal Wallet configuration when disconnecting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates or reuses a persistent local private key for the agent wallet. <br>
Mitigation: Protect ~/.zeal-agent-wallet/wallet.json as a secret, avoid exposing it in chat or logs, and remove or rotate the delegate permission if the key may be compromised. <br>
Risk: The skill can submit transaction proposals without a built-in user confirmation step. <br>
Mitigation: Require explicit approval before every proposal, including recipient, value, calldata meaning, network, operation type, and purpose. <br>
Risk: DelegateCall proposals and unclear calldata can create high-impact wallet risk even when execution still requires owner approval. <br>
Mitigation: Use DelegateCall only when the user has independently verified the contract behavior, calldata, and revocation path in Zeal or Safe. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Nicvaniek/zeal-agent-wallet) <br>
- [Zeal API base](https://api.zeal.app) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local wallet and configuration files under ~/.zeal-agent-wallet and submits transaction proposals through the Zeal API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; package.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
