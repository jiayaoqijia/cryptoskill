## Description:

Provides Binance Spot requests through the Binance API, including authenticated endpoints that require an API key and secret key, with support for mainnet and testnet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sum-li](https://clawhub.ai/user/sum-li)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to query Binance Spot market and account endpoints and prepare signed spot trading requests against mainnet, testnet, or demo environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may access Binance Spot credentials and perform real trading actions.

Mitigation: Prefer testnet or demo, use least-privilege keys with withdrawals disabled and IP allowlisting, and require explicit confirmation before mainnet transactions.

Risk: Credential examples can lead users to persist API keys or secrets in plaintext files.

Mitigation: Use a dedicated secret manager for real keys and do not store secrets in TOOLS.md or repository files.

Risk: Incorrect timestamp, recvWindow, or signature handling can cause authenticated requests to fail.

Mitigation: Check Binance server time, sync the local clock, and keep recvWindow within the documented maximum.

## Reference(s):

- [Authentication reference](references/authentication.md)
- [ClawHub skill page](https://clawhub.ai/sum-li/skills/binance-spot-skill)
- [Binance API mainnet](https://api.binance.com)
- [Binance Spot testnet](https://testnet.binance.vision)
- [Binance demo API](https://demo-api.binance.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON API responses with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Authenticated endpoints require signed Binance API requests and may affect real spot trading accounts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
