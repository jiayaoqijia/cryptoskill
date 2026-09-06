## Description: <br>
Operates Breeze x402 payment-gated endpoints for balance checks, deposits, and withdrawals on Solana. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keeganthomp](https://clawhub.ai/user/keeganthomp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to check Breeze balances, build deposit or withdrawal transactions, and execute x402-paid API calls from a funded Solana wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live Solana wallet private keys and can sign or broadcast transactions. <br>
Mitigation: Install only with a dedicated low-balance wallet, never a primary wallet, and review recipient, amount, and network before allowing signing or broadcast. <br>
Risk: Generated .env or wallet-backup.json files may contain private key material. <br>
Mitigation: Secure or avoid these files, keep them out of version control, and do not print or return raw secret values. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/keeganthomp/breeze-x402-payment-api) <br>
- [Breeze](https://breeze.baby) <br>
- [Breeze x402 API](https://x402.breeze.baby) <br>
- [agent-using-x402 example](https://github.com/anagrambuild/breeze-agent-kit/tree/main/apps/examples/agent-using-x402) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, command examples, and transaction or balance summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Solana transaction signatures and explorer URLs after successful deposit or withdrawal actions.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
