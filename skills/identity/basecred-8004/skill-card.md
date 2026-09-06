## Description: <br>
Interactive ERC-8004 agent registration via chat. Guides users through a prefill form, shows draft, confirms, then registers on-chain using agent0-sdk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Callmedas69](https://clawhub.ai/user/Callmedas69) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to prefill, review, edit, and submit ERC-8004 agent registrations for on-chain identity records. It also supports related search, update, and feedback workflows through chat guidance and bundled scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use raw wallet private keys to sign blockchain transactions. <br>
Mitigation: Use a fresh low-balance wallet, keep .env files out of source control and logs, and run a dry run before signing. <br>
Risk: Registration and feedback actions can create persistent public on-chain or IPFS records. <br>
Mitigation: Review the exact chain, wallet, endpoints, metadata, and transaction intent before confirming; avoid sensitive or private metadata. <br>
Risk: Accidental duplicate agent registration may create additional on-chain records. <br>
Mitigation: Check for existing agents for the wallet first and prefer update workflows when an agent is already registered. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/Callmedas69/basecred-8004-registration) <br>
- [ERC-8004 Registry](https://8004.org) <br>
- [Supported Chains](references/chains.md) <br>
- [Agent0 SDK Reference](references/sdk-reference.md) <br>
- [agent0-sdk](https://github.com/agent0lab/agent0-ts) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Chat guidance with Markdown drafts, JSON registration templates, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can prepare registration, search, update, and feedback commands; on-chain actions require explicit confirmation and wallet credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
