## Description: <br>
Virtuals Protocol integration for OpenClaw. Create, manage and trade tokenized AI agents on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rojasjuniore](https://clawhub.ai/user/rojasjuniore) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to query Virtuals Protocol token and agent market data, inspect balances, configure wallet details, and get command-line guidance for creating or trading tokenized AI agents on Base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to store a raw wallet private key locally, and the security evidence says the resulting config should be treated as a recoverable secret. <br>
Mitigation: Do not enter a real or funded wallet private key; use a disposable wallet with minimal funds for testing and remove the local config when finished. <br>
Risk: The security evidence flags unclear mainnet/testnet behavior because the code uses Base mainnet despite testnet-only wording. <br>
Mitigation: Verify the network and contract addresses before running wallet, create, buy, or sell workflows, and avoid funded mainnet activity unless it is explicitly intended. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rojasjuniore/skills/virtuals) <br>
- [Virtuals Homepage](https://virtuals.io) <br>
- [Virtuals App](https://app.virtuals.io) <br>
- [Virtuals Agent Creation](https://fun.virtuals.io) <br>
- [Virtuals Whitepaper](https://whitepaper.virtuals.io) <br>
- [GAME SDK](https://github.com/game-by-virtuals/game-node) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet configuration guidance, market data summaries, contract addresses, and links to Virtuals resources.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
