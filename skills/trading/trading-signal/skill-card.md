## Description:

Retrieves on-chain Smart Money buy/sell signals with trigger price, current price, max gain, exit rate, token tags, and chain filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[awessh](https://clawhub.ai/user/awessh)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve and summarize Binance Web3 Smart Money signals for BSC and Solana so they can monitor market activity and evaluate potential trades as informational data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can surface speculative crypto trading signals that may be mistaken for financial advice.

Mitigation: Treat outputs as informational market data only and verify independently before making any trade.

Risk: The skill calls a Binance Web3 public endpoint and may summarize live market-related data from that service.

Mitigation: Install only if that external network behavior is acceptable for the agent environment.

Risk: Signals can become stale or timed out, and high exit rates may indicate an expired signal.

Mitigation: Check signal status, timestamps, current price, and exit rate before relying on any displayed signal.

## Reference(s):

- [ClawHub Trading Signal Skill](https://clawhub.ai/awessh/skills/trading-signal)
- [Binance Web3 Smart Money Signals API](https://web3.binance.com/bapi/defi/v1/public/wallet-direct/buw/wallet/web/signal/smart-money)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include paginated Smart Money signal data, chain filters, price fields, token tags, and informational risk caveats.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
