## Description: <br>
DefiLlama API provides CLI access to DefiLlama data including TVL, stablecoins, prices, yields, volumes, fees, perps, unlocks, bridges, ETFs, narratives, token liquidity, main page, DAT, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poploli2](https://clawhub.ai/user/poploli2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to retrieve DefiLlama market, protocol, yield, bridge, ETF, and token data from a command-line workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send DEFILLAMA_API_KEY to DefiLlama through the pinned defillama-sdk dependency and may consume API quota. <br>
Mitigation: Set DEFILLAMA_API_KEY only when intentionally using Pro endpoints and monitor use against the relevant DefiLlama API plan. <br>
Risk: The skill executes through uv with a pinned third-party SDK dependency. <br>
Mitigation: Install only in environments where running uv and defillama-sdk==0.1.4 is acceptable, and review dependency policy before deployment. <br>


## Reference(s): <br>
- [DefiLlama](https://defillama.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/poploli2/defillama-api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv; optional DEFILLAMA_API_KEY enables Pro endpoints.] <br>

## Skill Version(s): <br>
0.1.0 (source: evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
