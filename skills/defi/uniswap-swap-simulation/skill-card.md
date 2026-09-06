## Description: <br>
Simulate and analyze Uniswap swaps including price impact, slippage, optimal routing, and gas estimation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to simulate proposed Uniswap swaps, compare routes, estimate price impact, slippage, and gas, and reason about MEV exposure before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Swap simulations and route comparisons can be mistaken for guaranteed execution outcomes or trading advice. <br>
Mitigation: Treat outputs as estimates and verify current pool state, fees, route, slippage, and gas before making any transaction decision. <br>
Risk: Users may expose sensitive wallet material when working around DeFi workflows. <br>
Mitigation: Use only public token, pool, route, amount, chain, and RPC information; never provide seed phrases or private keys. <br>
Risk: Large or high-impact swaps can be exposed to MEV and sandwich attack risk. <br>
Mitigation: Consider private RPCs, deadline parameters, and conservative slippage limits for high-impact swaps. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wpank/uniswap-swap-simulation) <br>
- [README](artifact/README.md) <br>
- [Skill specification](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with TypeScript examples and parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides estimated swap outputs, price impact, slippage tolerance, routing, gas, and MEV considerations; results should be treated as estimates rather than trading advice.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
