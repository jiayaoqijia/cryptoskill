## Description:

aaveclaw enables agents to interact with Aave V3 on the Base Sepolia testnet for WETH collateral, USDC borrowing and repayment, collateral withdrawal, position health checks, and test-token minting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chainyoda](https://clawhub.ai/user/chainyoda)

### License/Terms of Use:


## Use Case:

Developers and users working on Base Sepolia use this skill to check Aave lending health, mint test WETH or USDC, deposit WETH collateral, borrow or repay USDC, and withdraw collateral through guided shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a raw wallet private key and can sign blockchain transactions.

Mitigation: Install only with a dedicated Base Sepolia test wallet that holds no mainnet or valuable assets, and protect any key file with strict local permissions.

Risk: Deposit, borrow, repay, withdraw, faucet, wrapping, and approval commands submit real testnet transactions.

Mitigation: Confirm requested amounts, verify the network and contract addresses before use, and check the health factor before and after state-changing operations.

Risk: The approval flow can grant unlimited token approval.

Mitigation: Review or change the unlimited approval behavior before adapting this skill for production networks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chainyoda/skills/aaveclaw)
- [Base Sepolia RPC endpoint](https://sepolia.base.org)
- [Base Sepolia explorer](https://sepolia.basescan.org)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal output and Markdown guidance with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transaction links, token balances, and Aave account health summaries.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
