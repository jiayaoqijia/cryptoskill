## Description:

Multi-timeframe crypto technical analysis with scored trading signals, structured trade plans, and position sizing via Binance public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eplt](https://clawhub.ai/user/eplt)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to analyze Binance-listed cryptocurrency pairs, generate directional signal summaries, and produce structured trade plans with position sizing. It is intended as decision support and does not execute trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading signals, entries, stops, and position sizes may be mistaken for financial advice or treated as automatic trading instructions.

Mitigation: Treat outputs as decision support only, validate the market context independently, and apply user-controlled risk management before acting.

Risk: The skill installs third-party Python dependencies and fetches public market data at runtime.

Mitigation: Install in an isolated environment where possible, consider pinning dependency versions, and account for public API availability or rate-limit issues.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/eplt/skills/binance-signal-engine)
- [Binance Signal Engine Reference Guide](references/guide.md)
- [Binance Public API Endpoint](https://api.binance.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Human-readable command-line summary or structured JSON report with signal, trade plan, position size, and backtest row sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from public market data and local calculations; no exchange orders are placed.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
