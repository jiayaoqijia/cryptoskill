## Description:

Buy, sell, and launch tokens on Pump.fun using the PumpPortal API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[playdadev](https://clawhub.ai/user/playdadev)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to direct an agent to buy, sell, and launch Pump.fun tokens through PumpPortal. The skill requires a Solana private key and may cause real mainnet trading activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent authority to buy, sell, or launch Pump.fun tokens using a Solana private key.

Mitigation: Use only a dedicated Solana trading wallet with limited funds and do not provide a private key unless that authority is intended.

Risk: Commands may execute real Pump.fun mainnet transactions and the evidence does not show clear irreversible-transaction warnings or confirmation controls.

Mitigation: Review the runtime for confirmation prompts or dry-run support before using real funds, and start with small test amounts.

## Reference(s):

- [Pump.fun](https://pump.fun)
- [ClawHub Skill Page](https://clawhub.ai/playdadev/skills/pump-fun)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with command syntax and environment variable configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SOLANA_PRIVATE_KEY; optional SOLANA_RPC_URL, PUMP_PRIORITY_FEE, and PUMP_DEFAULT_SLIPPAGE settings are documented.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
