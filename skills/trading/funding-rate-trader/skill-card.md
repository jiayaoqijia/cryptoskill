## Description:

Crypto funding rate arbitrage strategy. Scan negative funding rates, auto-trade with stop-loss/take-profit. No API key needed for scanning, Binance API for trading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to scan Binance Futures funding rates, identify negative-rate opportunities, and optionally run scripts that place and monitor leveraged futures positions using local Binance API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The trader command can place leveraged Binance Futures orders using local API keys, which can create immediate financial exposure and loss.

Mitigation: Use restricted Binance API keys without withdrawal permissions, test with dry-run or testnet settings first, and run live trading only after confirming the leverage, position size, stop-loss, and take-profit settings.

Risk: The skill stores Binance API credentials in a local file under the user's home directory.

Mitigation: Protect the credential file with strict filesystem permissions and rotate keys if the file may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dagangtj/skills/funding-rate-trader)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON credential configuration, and terminal output from Node.js scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands call Binance Futures APIs; scanning can run without API keys, while trading and monitoring require local Binance API credentials.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
