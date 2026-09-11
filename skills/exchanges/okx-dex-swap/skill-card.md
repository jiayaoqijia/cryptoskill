## Description:

Guides agents through OKX OnchainOS DEX aggregation workflows for token quotes, approvals, unsigned swap calldata, and user-confirmed swap broadcasts across supported chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for OKX-aggregated token swap quotes, transaction preparation, and explicitly confirmed swap execution. It is intended for venue-unspecified swaps and redirects named DApp workflows to a protocol-specific skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare approvals and broadcast real token swaps, which can cause fund loss if token addresses, amounts, slippage, wallet selection, or override flags are wrong.

Mitigation: Require explicit user confirmation for fund-action steps, verify token addresses and quote details before execution, block honeypot buys, and re-quote stale prices before broadcasting.

Risk: The pre-flight flow may install or update the onchainos CLI from OKX GitHub releases before use.

Mitigation: Use the installer only from a trusted OKX release path, verify installer and binary checksums, and stop on any hash mismatch.

Risk: Failure diagnostics can include wallet addresses, token pairs, transaction hashes, amounts, and other transaction details.

Mitigation: Share diagnostic summaries only when the user accepts disclosure of those wallet and transaction details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ok-james-01/skills/okx-dex-swap)
- [OKX Web3](https://web3.okx.com)
- [OKX DEX Aggregator API Reference](https://web3.okx.com/onchainos/dev-docs/trade/dex-api-reference)
- [CLI command reference](references/cli-reference.md)
- [Swap troubleshooting](references/troubleshooting.md)
- [Pre-flight checks](_shared/preflight.md)
- [Chain support](_shared/chain-support.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and transaction summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include token address choices, quote summaries, risk warnings, calldata fields, transaction hashes, explorer follow-up guidance, and diagnostic summaries.]

## Skill Version(s):

3.1.3 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
