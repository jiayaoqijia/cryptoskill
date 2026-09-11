## Description:

Scores pump.fun Solana token contract addresses for snipe safety by analyzing dev wallet history, social links, liquidity, and holder concentration, returning a 0-100 score and SNIPE/CAUTION/AVOID verdict.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ultranumblol](https://clawhub.ai/user/ultranumblol)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this skill to evaluate a pump.fun token contract address before trading by requesting a token-risk score, verdict, and signal breakdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The SNIPE/CAUTION/AVOID verdict can be mistaken for a guarantee of trading safety.

Mitigation: Treat scores as advisory trading information and perform independent review before buying or selling tokens.

Risk: The web UI, payment handling, and mutable dependency instructions create installation and hosting risk.

Mitigation: Review before installing or hosting, prefer JSON/API or CLI output until web UI metadata rendering is fixed, pin Python and npm dependencies, and use only a trusted x402 facilitator/payment endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ultranumblol/skills/pumpfun-sniper)
- [Skill README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON API or CLI scoring response with concise text guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a token contract address; self-hosted scoring works best with HELIUS_API_KEY; hosted scoring may require x402 payment.]

## Skill Version(s):

1.0.0 (source: server release evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
