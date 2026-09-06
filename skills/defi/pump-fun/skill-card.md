## Description: <br>
Buy, sell, and launch tokens on Pump.fun using the PumpPortal API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[playdadev](https://clawhub.ai/user/playdadev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to request Pump.fun token buys, sells, and launches through PumpPortal after configuring a dedicated Solana wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests Solana wallet authority and describes real fund-moving actions without enough visible implementation or transaction safeguards. <br>
Mitigation: Use only a dedicated low-balance wallet, do not set SOLANA_PRIVATE_KEY unless the implementation can be inspected and trusted, and manually verify mint addresses, amounts, slippage, fees, and wallet impact before any transaction. <br>
Risk: This release contains only documentation, so command behavior and transaction safeguards cannot be verified from the artifact. <br>
Mitigation: Confirm the installed release includes the expected implementation and review it before using buy, sell, or launch commands. <br>


## Reference(s): <br>
- [Pump.fun](https://pump.fun) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with slash-command examples and inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require wallet configuration and transaction parameters such as mint address, amount, slippage, or token launch details.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
