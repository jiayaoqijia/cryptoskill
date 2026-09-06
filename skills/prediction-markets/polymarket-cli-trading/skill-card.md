## Description: <br>
Trade prediction markets on Polymarket using the official polymarket CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lacymorrow](https://clawhub.ai/user/lacymorrow) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to research Polymarket prediction markets, prepare CLI commands for market data, manage orders and positions, and perform wallet or conditional token workflows with explicit confirmation for account-affecting actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help prepare commands that affect real-money Polymarket accounts. <br>
Mitigation: Require explicit user confirmation before every trade, cancellation, approval, wallet, bridge, split, merge, or redeem command. <br>
Risk: Private keys and API keys may be exposed if pasted into chat or shell history. <br>
Mitigation: Use wallet setup and environment handling that avoids displaying secrets, and never ask the agent to store or repeat private keys. <br>
Risk: The artifact documents a remote shell installer path. <br>
Mitigation: Prefer the Homebrew installation path, or independently review and verify any remote installer before running it. <br>
Risk: Incorrect token IDs, amounts, or market sides can lead to unintended trades. <br>
Mitigation: Show the exact command, market, token ID, side, price, and size for review before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lacymorrow/polymarket-cli-trading) <br>
- [Publisher profile](https://clawhub.ai/user/lacymorrow) <br>
- [Polymarket CLI](https://github.com/Polymarket/polymarket-cli) <br>
- [Polymarket documentation](https://docs.polymarket.com/) <br>
- [CLOB API documentation](https://docs.polymarket.com/developers/) <br>
- [Liquidity rewards](https://docs.polymarket.com/developers/market-makers/liquidity-rewards) <br>
- [Maker rebates program](https://docs.polymarket.com/developers/market-makers/maker-rebates-program) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-output command variants for scripting with the polymarket CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
