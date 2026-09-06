## Description: <br>
Control a sandboxed MetaMask browser extension wallet for autonomous blockchain transactions with configurable permission guardrails, including spend limits, chain allowlists, protocol restrictions, and approval thresholds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andreolf](https://clawhub.ai/user/andreolf) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to operate a dedicated MetaMask browser wallet for dapp connections, token swaps, token transfers, message signing, balance checks, and transaction history while applying configured permission guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports irreversible crypto wallet actions while the available evidence does not include full setup code, package scripts, lockfile, or verified permission enforcement. <br>
Mitigation: Review before installing, use only a brand-new MetaMask wallet with very small funds, never use a main wallet or seed phrase, and do not rely on advertised spend limits or approval flow until the full source and enforcement logic are reviewed. <br>
Risk: The skill can sign arbitrary messages and submit transactions through a dedicated browser wallet. <br>
Mitigation: Keep the wallet isolated, restrict configured chains and protocols, require explicit user approval above low thresholds, and review logged transaction intent and outcomes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andreolf/skills/metamask-agent-wallet-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and command syntax] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet action commands, permission configuration guidance, and transaction logging examples.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
