## Description: <br>
Generates crypto market intelligence reports with prices, sentiment, trending coins, Polymarket markets, and simple data-driven commentary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cassh100k](https://clawhub.ai/user/cassh100k) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and channel operators use this skill to generate one-command crypto market monitoring reports from public data sources for alpha channels or routine market review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reports depend on outbound calls to public crypto and prediction-market APIs, so data can be unavailable, stale, rate limited, or incomplete. <br>
Mitigation: Use generated reports for monitoring, review them before acting or sharing, and handle missing API data in any downstream workflow. <br>
Risk: Optional Telegram posting and cron examples can publish reports or write logs if configured by the user. <br>
Mitigation: Inspect or implement the Telegram helper before use, protect bot tokens, and add cron jobs only under an intended user account with controlled log paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cassh100k/crypto-alpha-scanner) <br>
- [CoinGecko simple price endpoint](https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,solana&vs_currencies=usd&include_24hr_change=true) <br>
- [CoinGecko trending endpoint](https://api.coingecko.com/api/v3/search/trending) <br>
- [Alternative.me Fear and Greed endpoint](https://api.alternative.me/fng/?limit=1) <br>
- [Polymarket Gamma markets endpoint](https://gamma-api.polymarket.com/markets?closed=false&limit=5&order=volume24hr&ascending=false) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text market report with optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public API responses at runtime; optional examples show file output, Telegram posting, and cron scheduling.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
