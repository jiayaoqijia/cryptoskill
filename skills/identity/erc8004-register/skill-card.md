## Description: <br>
Register AI agents on-chain, update metadata, validate registrations, and auto-fix broken profiles via the ERC-8004 Identity Registry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aetherstacey](https://clawhub.ai/user/aetherstacey) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to register, inspect, update, validate, and repair ERC-8004 agent identity records across supported EVM networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool requests wallet signing authority and can submit blockchain transactions. <br>
Mitigation: Use a dedicated low-value wallet and install only when comfortable granting the tool signing authority. <br>
Risk: Register, update, and fix actions can change on-chain agent records. <br>
Mitigation: Verify the selected chain and registry address before state-changing commands, and use dry-run behavior where available before applying fixes. <br>
Risk: Info, validate, and self-check actions may contact RPC providers, Agentscan, and metadata-supplied URLs. <br>
Mitigation: Treat these as networked actions and avoid running them where external lookups of wallet or agent metadata would be inappropriate. <br>


## Reference(s): <br>
- [ERC-8004 Registration v1](https://eips.ethereum.org/EIPS/eip-8004#registration-v1) <br>
- [ClawHub skill page](https://clawhub.ai/aetherstacey/erc8004-register) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce blockchain transaction hashes, explorer links, validation findings, and proposed metadata changes.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
