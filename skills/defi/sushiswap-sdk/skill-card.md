## Description:

TypeScript SDK for interacting with the SushiSwap Aggregator and related primitives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xmasayoshi](https://clawhub.ai/user/0xmasayoshi)

### License/Terms of Use:


## Use Case:

Developers and integrators use this skill to add SushiSwap Aggregator support to TypeScript or JavaScript applications, including token primitives, quotes, and swap transaction generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Swap execution examples can lead an agent or developer to sign and broadcast real SushiSwap transactions from a private key.

Mitigation: Use only with explicit user approval, decoded transaction review, chain/router/spender/amount/slippage checks, simulation that verifies asset changes, pinned dependencies, and preferably a low-balance or test wallet.

Risk: The skill gives under-scoped guidance for signing mainnet swap transactions that can move real funds.

Mitigation: Review the skill carefully before installing and require transaction simulation and human approval before execution.

## Reference(s):

- [SushiSwap SDK Reference](references/REFERENCE.md)
- [ClawHub Skill Page](https://clawhub.ai/0xmasayoshi/skills/sushiswap-sdk)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SDK installation commands, typed SushiSwap API examples, and integration guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
