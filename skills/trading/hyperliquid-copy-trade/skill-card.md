## Description: <br>
Automate copy trading on Hyperliquid via Coinpilot to discover, investigate, and mirror top on-chain traders in real time with low execution latency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alannkl](https://clawhub.ai/user/alannkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure a trusted local agent runtime for Coinpilot, discover Hyperliquid lead wallets, manage copy-trading subscriptions, adjust risk settings, and review performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles raw wallet private keys and can execute live trading actions. <br>
Mitigation: Use dedicated low-balance wallets, keep credentials in the fixed local file with strict permissions, and require user confirmation before start, stop, update, close, or recurring automation actions. <br>
Risk: A malicious or incorrect API destination could expose secrets or trading authority. <br>
Mitigation: Verify the Coinpilot API URL and allow only trusted Coinpilot endpoints before runtime use. <br>
Risk: Copy trading perpetuals can cause financial loss and does not provide financial advice. <br>
Mitigation: Review leader selection, allocation, leverage, stop-loss, and take-profit settings before enabling or changing subscriptions. <br>


## Reference(s): <br>
- [Coinpilot endpoints and auth](references/coinpilot-api.md) <br>
- [Credential format](references/coinpilot-json.md) <br>
- [Hyperliquid info endpoints](references/hyperliquid-api.md) <br>
- [Coinpilot documentation](https://docs.coinpilot.com/) <br>
- [Skill source homepage](https://github.com/coinpilot-labs/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local placeholder credentials file; live operations require user-provided local credentials and explicit trading intent.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
