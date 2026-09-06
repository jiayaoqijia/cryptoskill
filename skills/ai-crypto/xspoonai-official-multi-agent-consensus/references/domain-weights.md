# Domain-Specific Weights

## Smart Contract Security
- Anthropic: weight 1.2 (strong at reasoning about edge cases)
- OpenAI: weight 1.0 (balanced analysis)
- DeepSeek: weight 1.1 (strong at code pattern recognition)
- Consensus mode: **conservative** (any risk flag → report it)

## DeFi Protocol Analysis
- Focus on: reentrancy, oracle manipulation, flash loan vectors
- Consensus mode: **union** (merge all findings)

## General Analysis
- Equal weights across providers
- Consensus mode: **majority vote**

## Adding New Domains

To add a new domain, define:
1. Provider weights (based on empirical performance)
2. Consensus mode (conservative / union / majority / diversity)
3. Domain-specific focus areas
4. Risk threshold adjustment (if applicable)
