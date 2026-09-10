## Description:

Execute perpetual trades on Ostium, Aster, and Avantis via Maxxit's Lazy Trading API, and trade Indian stocks through Zerodha Kite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhi152003](https://clawhub.ai/user/abhi152003)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this skill to research markets, inspect balances and positions, place or close trades, manage TP/SL settings, run predefined strategy scripts, and interact with ZK-verified alpha listings through Maxxit-supported venues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place leveraged trades, close positions, adjust TP/SL settings, spend agent-wallet USDC, and execute purchased alpha.

Mitigation: Require explicit confirmation for every payment, order, cancellation, close, TP/SL change, and Alpha execution; review or disable autonomous strategy scripts before use.

Risk: Trading credentials and delegated wallet permissions could be exposed or misused in untrusted environments.

Mitigation: Keep MAXXIT_API_KEY and trading credentials out of untrusted environments, verify the installer, and set MAXXIT_API_URL only to the trusted Maxxit origin.

Risk: Automated strategies rely on external market data and local signal rules that may produce poor or stale trading decisions.

Mitigation: Use test or low-risk settings first, apply collateral and leverage limits, monitor executions, and review generated signals before allowing live trades.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abhi152003/skills/maxxit-lazy-trading)
- [Maxxit App](https://maxxit.ai)
- [Lazy Trading setup](https://maxxit.ai/lazy-trading)
- [Binance Klines API](https://api.binance.com/api/v3/klines)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with inline shell commands, API call examples, and generated trading actions when executed by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses MAXXIT_API_KEY and MAXXIT_API_URL; some Zerodha flows also use Kite credentials.]

## Skill Version(s):

1.2.20 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
