## Description:

Trade prediction markets on Polymarket using the official polymarket CLI for market research, order placement, order management, positions, order books, rewards, and conditional token operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lacymorrow](https://clawhub.ai/user/lacymorrow)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to operate Polymarket's official CLI for prediction market research, trading workflows, portfolio checks, rewards tracking, and on-chain conditional token actions. It is intended to propose and explain commands while requiring explicit confirmation for real-money operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents a pipe-to-shell installer for the Polymarket CLI.

Mitigation: Prefer the Homebrew installation path or a reviewed source build, and avoid executing remote installer scripts directly.

Risk: Private keys may be exposed if passed on the command line, stored in environment variables, or written to logs.

Mitigation: Use a dedicated low-balance trading wallet, avoid command-line private keys, minimize environment-variable exposure, and keep secrets out of logs.

Risk: Trading, approvals, cancellations, redemptions, wallet resets, and API-key mutations can affect real funds or account access.

Mitigation: Show the exact command, verify token IDs, amounts, approvals, and wallet context, then require explicit user confirmation before execution.

## Reference(s):

- [Polymarket CLI](https://github.com/Polymarket/polymarket-cli)
- [Polymarket Docs](https://docs.polymarket.com/)
- [CLOB API Docs](https://docs.polymarket.com/developers/)
- [Liquidity Rewards](https://docs.polymarket.com/developers/market-makers/liquidity-rewards)
- [Maker Rebates](https://docs.polymarket.com/developers/market-makers/maker-rebates-program)
- [ClawHub Skill Page](https://clawhub.ai/lacymorrow/skills/polymarket-cli-trading)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON-output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may invoke real-money trading, wallet approvals, cancellations, redemptions, API-key changes, and on-chain operations; the skill directs the agent to show exact commands and obtain user confirmation before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
