## Description:

Propose transactions to a Zeal Wallet. Use when the user wants to set up an agent as a Zeal Wallet signer, propose transactions, or manage a delegate wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nicvaniek](https://clawhub.ai/user/nicvaniek)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate an agent wallet, configure it for a Zeal Wallet, and submit signed transaction proposals that require approval in the Zeal app before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local agent private key is stored on disk and could authorize signed transaction proposals if exposed.

Mitigation: Install only in trusted environments, protect `~/.zeal-agent-wallet/wallet.json`, and never expose the file contents in chat or logs.

Risk: The skill can submit signed transaction proposals without explicit user confirmation.

Mitigation: Require the agent to show the destination, value, calldata, network, operation type, and purpose before every proposal.

Risk: DelegateCall or unknown calldata can be high risk even when final execution requires approval in the Zeal app.

Mitigation: Treat DelegateCall and unknown calldata as high risk and verify them independently before approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nicvaniek/skills/zeal-agent-wallet)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with inline shell commands and concise status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can create local wallet configuration, preserve a private key on disk, and submit signed transaction proposals through the Zeal API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
