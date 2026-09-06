## Description: <br>
Gate on-chain staking skill. Use when the user asks to stake POS coins, mint, or redeem staked assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to query Gate on-chain earn staking positions, rewards, products, and order history, and to draft stake, redeem, or mint actions through the Gate MCP server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit financial stake, redeem, or mint actions through an Earn:Write MCP permission. <br>
Mitigation: Install only with a trusted Gate MCP server, use the narrowest Gate API key possible with no withdrawal permission, and require a clear action draft plus immediate explicit user confirmation before every write action. <br>
Risk: Security evidence reports conflicting or under-scoped safety instructions. <br>
Mitigation: Review the skill before deployment and verify that every stake, redeem, or mint workflow enforces mandatory confirmation and result verification. <br>
Risk: Security evidence flags an unpinned remote runtime rule as a concern. <br>
Mitigation: Prefer a revised release that removes or pins the remote runtime rule before production deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gate-exchange/gate-exchange-staking) <br>
- [Gate Staking MCP Specification](references/mcp.md) <br>
- [Gate Staking Assets](references/staking-assets.md) <br>
- [Gate Staking Products](references/staking-coins.md) <br>
- [Gate Staking Orders and Rewards](references/staking-list.md) <br>
- [Gate Staking Swap](references/staking-swap.md) <br>
- [Gate Staking Scenarios](references/scenarios.md) <br>
- [Gate API v4 documentation](https://www.gate.io/docs/developers/apiv4/) <br>
- [Gate MCP setup](https://github.com/gateio/gate-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown responses with MCP tool calls, action drafts, confirmations, and staking result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Financial staking actions require immediate explicit user confirmation before execution; read-only queries can return positions, rewards, products, and order history.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
