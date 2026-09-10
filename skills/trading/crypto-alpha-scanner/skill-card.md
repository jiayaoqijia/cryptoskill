## Description:

Automated crypto market intelligence - prices, sentiment, trending coins, and Polymarket hot markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cassh100k](https://clawhub.ai/user/cassh100k)

### License/Terms of Use:


## Use Case:

Developers, market operators, and crypto community teams use this skill to generate concise market monitoring reports covering major token prices, sentiment, trending coins, and active prediction markets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented hourly cron setup can create persistent execution without sufficient operational guardrails.

Mitigation: Prefer manual runs or a user-owned scheduler with a user-owned log path, log rotation, and a clear removal command.

Risk: Telegram publishing can expose market reports publicly or leak bot-token access if the destination and credentials are not controlled.

Mitigation: Verify the Telegram destination before posting and secure any bot token outside shared logs, shell history, and public files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cassh100k/skills/crypto-alpha-scanner)
- [CoinGecko simple price API](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true)
- [CoinGecko trending search API](https://api.coingecko.com/api/v3/search/trending)
- [Alternative.me Fear and Greed API](https://api.alternative.me/fng/?limit=1)
- [Polymarket Gamma markets API](https://gamma-api.polymarket.com/markets?closed=false&limit=5&order=volume24hr&ascending=false)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text market report with Markdown-style sections and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses live third-party market APIs at runtime; no API keys are required for the documented scanner.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
