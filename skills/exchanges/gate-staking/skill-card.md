## Description:

Gate on-chain staking skill for querying staking positions, rewards, products, and order history, and for preparing confirmed stake, redeem, or mint actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to inspect Gate on-chain earn staking positions, rewards, available products, and staking history. With Gate MCP access and explicit confirmation, it can help submit stake, redeem, or mint actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit financial staking, redemption, or mint orders when granted Earn:Write permission.

Mitigation: Install only with a trusted Gate MCP setup and require a fresh Action Draft confirmation immediately before any write action.

Risk: Mutable external runtime rules and unresolved artifact ambiguity can make approval or execution behavior unclear.

Mitigation: Pin or vendor runtime rules, resolve the documented merge conflict, and review all stake, redeem, and mint paths before deployment.

Risk: Incorrect staking product, amount, coin, or side selection could lead to unintended financial actions.

Mitigation: Confirm product ID, side, amount, coin, lock period, and exchange-rate note with the user before submitting an order.

## Reference(s):

- [Gate Staking MCP Specification](references/mcp.md)
- [Gate Staking Assets](references/staking-assets.md)
- [Gate Staking Products](references/staking-coins.md)
- [Gate Staking List](references/staking-list.md)
- [Gate Staking Swap](references/staking-swap.md)
- [Gate Exchange Staking Scenario Index](references/scenarios.md)
- [Gate API v4 Documentation](https://www.gate.io/docs/developers/apiv4/)
- [Gate API Key Management](https://www.gate.io/myaccount/profile/api-key/manage)

## Skill Output:

**Output Type(s):** [Markdown, API calls, Guidance]

**Output Format:** [Markdown result summaries, staking action drafts, and confirmation or error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Gate MCP access and explicit user confirmation before stake, redeem, or mint execution.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
