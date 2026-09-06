## Description: <br>
Scores pump.fun Solana token contract addresses for snipe safety using dev-wallet history, social links, liquidity, and holder-concentration signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ultranumblol](https://clawhub.ai/user/ultranumblol) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to assess pump.fun token contract addresses before trading. It returns a 0-100 score, SNIPE/CAUTION/AVOID verdict, and signal breakdown across dev-wallet, social-link, liquidity, and holder-concentration checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token addresses and a Helius API key may be sent to external crypto data providers. <br>
Mitigation: Use a dedicated API key, avoid submitting sensitive token data, and confirm external data-sharing is acceptable before use. <br>
Risk: The hosted scoring flow can authorize a paid x402 request. <br>
Mitigation: Require explicit user approval before an agent runs x402 pay commands or any command that authorizes payment. <br>
Risk: The web UI renders API response content into the page. <br>
Mitigation: Avoid using the web UI with untrusted token data until the rendering issue is fixed; prefer CLI or API JSON output for agent workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ultranumblol/pumpfun-sniper) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [Hosted scoring endpoint](https://pumpfun-sniper-production.up.railway.app/score?ca=TOKEN_CA) <br>
- [Package homepage](https://github.com/ultranumblol/pumpfun-sniper) <br>
- [Package support URL](https://github.com/ultranumblol/pumpfun-sniper/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and JSON scoring responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and HELIUS_API_KEY for best self-hosted results; the hosted /score endpoint may require x402 payment.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
