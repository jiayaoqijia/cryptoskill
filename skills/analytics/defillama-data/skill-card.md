## Description:

Provides CLI access to DefiLlama data for TVL, stablecoins, coin prices, yields, volumes, fees, perps, unlocks, bridges, ETFs, narratives, token liquidity, main page, DAT, and meta datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poploli2](https://clawhub.ai/user/poploli2)

### License/Terms of Use:


## Use Case:

Developers and data analysts use this skill to query DefiLlama DeFi market and protocol datasets from an agent-controlled command line. It supports both public endpoints and Pro endpoints when a DefiLlama API key is supplied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a uv-based Python CLI that contacts DefiLlama services.

Mitigation: Run it in a constrained environment and review commands before execution.

Risk: Pro endpoints may use a DefiLlama Pro API key.

Mitigation: Provide only the DefiLlama key needed for the task, preferably through DEFILLAMA_API_KEY or --api-key for that invocation.

Risk: User-facing documentation and help text are primarily in Chinese.

Mitigation: Confirm command meanings and parameters before using the output in workflows that require English-language review.

## Reference(s):

- [DefiLlama](https://defillama.com/)
- [ClawHub Skill Page](https://clawhub.ai/poploli2/skills/defillama-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON-producing CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [CLI responses are printed as pretty JSON by default, with compact JSON available through --compact.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
