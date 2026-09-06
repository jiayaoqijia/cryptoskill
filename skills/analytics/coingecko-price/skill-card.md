## Description: <br>
Queries cryptocurrency prices, market rankings, 24-hour changes, and coin search results through the CoinGecko API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ouyangAbel](https://clawhub.ai/user/ouyangAbel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to search cryptocurrencies and retrieve current price, market-cap ranking, and 24-hour change data from CoinGecko. Prices are reference data and not financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms, coin IDs, and currency codes are sent to CoinGecko. <br>
Mitigation: Avoid entering private or sensitive information in cryptocurrency search, coin ID, or currency fields. <br>
Risk: CoinGecko's free API may rate-limit requests. <br>
Mitigation: Wait and retry later when the API reports excessive request frequency. <br>
Risk: Cryptocurrency prices can be volatile and may be inappropriate as sole decision inputs. <br>
Mitigation: Treat returned prices as reference data, not financial advice. <br>


## Reference(s): <br>
- [CoinGecko API documentation](https://www.coingecko.com/api/documentation) <br>
- [ClawHub skill page](https://clawhub.ai/ouyangAbel/coingecko-price) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, API calls] <br>
**Output Format:** [Plain text command output with price, ranking, search result, and error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls CoinGecko's public API; query terms, coin IDs, and currency codes are sent to CoinGecko.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
