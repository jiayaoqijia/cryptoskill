## Description: <br>
aaveclaw helps agents interact with Aave V3 on Base Sepolia testnet to mint test tokens, deposit WETH collateral, borrow or repay USDC, withdraw WETH, and check lending health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chainyoda](https://clawhub.ai/user/chainyoda) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use this skill to guide and execute Base Sepolia Aave V3 lending workflows, including test token minting, collateral deposits, USDC borrowing and repayment, WETH withdrawals, and health-factor checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a raw wallet private key and can sign state-changing Aave lending transactions. <br>
Mitigation: Use only a dedicated low-value Base Sepolia testnet wallet, prefer X402_PRIVATE_KEY from a controlled secret source, and review each approval, faucet, deposit, borrow, repay, and withdraw before execution. <br>
Risk: Borrowing can lower account health and create liquidation risk on the testnet lending position. <br>
Mitigation: Run health.sh before changes, ask the user for explicit amounts, and check the health factor after each state-changing operation; treat values below 1.5 as risky. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chainyoda/skills/aaveclaw) <br>
- [Base Sepolia explorer](https://sepolia.basescan.org) <br>
- [Base Sepolia RPC endpoint](https://sepolia.base.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and console transaction/account summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [State-changing commands can sign Base Sepolia testnet transactions and may print transaction hashes, balances, and health-factor summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
