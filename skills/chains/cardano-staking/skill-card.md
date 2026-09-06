## Description: <br>
Check stake delegation and available ADA rewards for the connected wallet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adacapo21](https://clawhub.ai/user/adacapo21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check whether a connected Cardano wallet is delegated to a stake pool and to report available ADA staking rewards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a wallet seed phrase through the associated MCP package even though the described task is a read-only rewards lookup. <br>
Mitigation: Do not provide a real seed phrase unless the MCP package has been audited and trusted; prefer a read-only public stake address or equivalent method where available. <br>
Risk: A seed phrase can control wallet funds if exposed to an untrusted dependency or runtime. <br>
Mitigation: Use a dedicated low-value wallet for testing and keep production wallet credentials out of agent and MCP environments. <br>


## Reference(s): <br>
- [Cardano Staking ClawHub release](https://clawhub.ai/adacapo21/cardano-staking) <br>
- [Staking Concepts](references/concepts.md) <br>
- [Staking MCP Tools Reference](references/mcp-tools.md) <br>
- [Check Stake Delegation](sub-skills/check-delegation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown text with delegation status and ADA reward values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports poolId as a bech32 pool identifier and availableAdaRewards in ADA.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
