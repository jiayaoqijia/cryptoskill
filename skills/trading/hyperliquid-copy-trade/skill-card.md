## Description:

Automate copy trading on Hyperliquid via Coinpilot to discover, investigate, and mirror top on-chain traders in real time with low execution latency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alannkl](https://clawhub.ai/user/alannkl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure a trusted local agent runtime for Coinpilot, discover Hyperliquid lead wallets, start or stop copy-trading subscriptions, adjust risk settings, and inspect subscription performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a Coinpilot API key and multiple wallet private keys in a local credentials file.

Mitigation: Use a trusted local runtime, keep ~/.coinpilot/coinpilot.json owner-readable only, never paste secrets into chat, and avoid committing credential files.

Risk: Live copy-trading actions can move funds and expose configured wallets to trading losses.

Mitigation: Use wallets funded only for this strategy, confirm balances and subscription settings before state-changing actions, and apply stop loss, take profit, leverage, and margin limits appropriate to the user's risk tolerance.

Risk: Coinpilot receives wallet private keys for API authentication and experimental copy-trading routes.

Mitigation: Install only when the user trusts Coinpilot and its infrastructure with control of the configured wallets, and do not store unrelated funds or permissions on those wallets.

Risk: Unpinned or unexpected installation sources can change the runtime behavior reviewed here.

Mitigation: Prefer pinned installation sources and verify the release version and file hashes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alannkl/skills/coinpilot-hyperliquid-copy-trade)
- [Coinpilot skill repository homepage](https://github.com/coinpilot-labs/skills)
- [Coinpilot documentation](https://docs.coinpilot.com/)
- [Coinpilot API reference](references/coinpilot-api.md)
- [Coinpilot credentials format](references/coinpilot-json.md)
- [Hyperliquid info endpoints](references/hyperliquid-api.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger serialized Coinpilot and Hyperliquid API calls through the bundled Node.js CLI when the user has configured local credentials.]

## Skill Version(s):

1.0.7 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
