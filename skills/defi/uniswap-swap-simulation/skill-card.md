## Description:

Simulate and analyze Uniswap swaps including price impact, slippage, optimal routing, and gas estimation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

External developers and engineers use this skill to simulate proposed Uniswap swaps, compare routing options, and reason about price impact, slippage, gas cost, and MEV exposure before building or advising on swap execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README includes unpinned remote install commands that may execute mutable code.

Mitigation: Review the install path before running commands; prefer a pinned clawhub version and immutable Git commit or release tag.

Risk: Swap simulations and estimates can be mistaken for authority to execute trades or handle private wallet material.

Mitigation: Use the skill for simulation and risk analysis only, and keep private keys, seed phrases, and signing authority out of the workflow.

Risk: Large or high-impact swaps may face slippage, sandwich attacks, or execution-price changes between simulation and submission.

Mitigation: Check price impact, set explicit slippage and deadline controls, consider private RPCs for large swaps, and re-simulate close to execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/uniswap-swap-simulation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include quoted swap outputs, price-impact calculations, routing analysis, slippage guidance, gas estimates, and MEV risk notes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
