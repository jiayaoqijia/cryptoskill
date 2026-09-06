## Description: <br>
Monitor Bitfinex lending (funding) performance via API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reed1898](https://clawhub.ai/user/reed1898) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to check Bitfinex funding wallet balances, active funding credits, and recent funding interest without opening the Bitfinex app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Bitfinex API credentials for authenticated account reporting. <br>
Mitigation: Use a dedicated read-only Bitfinex API key limited to wallet, funding, and ledger/history reads. <br>
Risk: Over-permissioned exchange credentials could expose trading, transfer, or withdrawal capabilities beyond the monitor's reporting purpose. <br>
Mitigation: Do not grant trading, transfer, or withdrawal permissions to the API key used with this skill. <br>


## Reference(s): <br>
- [Bitfinex API Notes](references/api-notes.md) <br>
- [Bitfinex API](https://api.bitfinex.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text summary or JSON emitted by a local Python command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to USD/fUSD and supports currency, lookback days, and JSON output options.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
