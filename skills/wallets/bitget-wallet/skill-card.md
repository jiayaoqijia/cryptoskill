## Description: <br>
Interact with Bitget Wallet API for crypto market data, token info, swap quotes, and security audits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karryzhang](https://clawhub.ai/user/karryzhang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers, agent builders, and crypto users use this skill to query token data, assess token security, obtain swap and order quotes, and prepare or submit user-confirmed Bitget Wallet transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support real crypto swap workflows, transaction submission, and private-key signing paths. <br>
Mitigation: Use it only for intended trading workflows, require explicit user confirmation before signing or submitting, and prefer an external wallet or hardware signer that displays the exact transaction. <br>
Risk: The signing helper relies on API-provided hashes for some order flows. <br>
Mitigation: Treat API-provided-hash signing as high risk; verify order details, chain IDs, contract targets, wallet address, fees, and expected token transfers before signing. <br>
Risk: Runtime self-update instructions from a moving branch can change skill behavior after installation. <br>
Mitigation: Review updates through the normal platform release process and inspect changes to endpoints, dependencies, credential handling, and signing behavior before use. <br>
Risk: Unfamiliar tokens may be honeypots, taxed tokens, upgradeable contracts, or otherwise unsafe to trade. <br>
Mitigation: Run the security audit workflow before interacting with unfamiliar tokens and surface high-risk findings before recommending or executing any swap. <br>


## Reference(s): <br>
- [Bitget Wallet API documentation](https://web3.bitget.com/en/docs) <br>
- [Bitget Wallet Skill on ClawHub](https://clawhub.ai/karryzhang/bitget-wallet-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured JSON returned by helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces human-readable market, audit, quote, signing, and transaction-status guidance for agent-mediated crypto workflows.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata; artifact frontmatter reports 2026.3.5-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
