---
name: PancakeSwap
description: >
  Audit PancakeSwap liquidity positions before capital is deployed.
  Evaluate depth, concentrated-liquidity setup, range risk, pool quality,
  and approval friction before users provide liquidity.
version: 1.0.0
---

# PancakeSwap

> **High APR is not the same thing as high-quality liquidity.**

PancakeSwap is a protocol-truth-enforcer skill for liquidity and pool-risk decisions.

This skill is designed for users who want to evaluate PancakeSwap liquidity setups before adding capital, especially where concentrated liquidity, fee tiers, or position structure can create hidden risk.

Use this skill when you need to:
- assess whether a PancakeSwap pool is worth providing liquidity to
- review V3-style concentrated liquidity risk
- reason about range exposure before capital is committed
- evaluate whether apparent returns justify pool and structure risk
- screen pool quality before LP deployment

This skill does NOT:
- execute trades
- add or remove liquidity
- connect to PancakeSwap smart contracts
- guarantee pool safety or yield stability
- replace smart contract review or formal risk assessment

---

## What This Skill Does

PancakeSwap helps:
- analyze pool structure before liquidity is deployed
- evaluate concentrated-liquidity range risk
- assess depth, accessibility, and fragility
- separate attractive APR from durable pool quality
- identify where LP strategy may be too optimistic

---

## Best Use Cases

- pre-LP review on PancakeSwap
- V3 range-risk screening
- fee-tier and pool-structure review
- evaluating whether a pool can support intended size
- auditing whether a position is too narrow, too exposed, or too fragile
- comparing risk of multiple LP opportunities

---

## What to Provide

Useful input includes:
- pool pair
- chain
- fee tier
- intended size
- whether the position is V2 / V3 / stable / concentrated
- intended price range if relevant
- visible depth, volume, or yield context
- what the user is optimizing for: fees, capital efficiency, lower risk, or passive exposure

If the user does not provide enough pool context, this skill should state what is missing.

---

## Standard Output Format

PANCAKESWAP POOL ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━
Pool: [Pair / Chain / Version]
Intent: [Provide liquidity / assess risk / compare pools]

POOL QUALITY
━━━━━━━━━━━━━━━━━━━━━━━━━━
Depth Quality: [Strong / Moderate / Thin / Fragile]
Range Risk: [Low / Medium / High]
Position Complexity: [Low / Medium / High]

MAIN CONCERNS
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ [Depth concern]
⚠️ [Range concern]
⚠️ [Fee-tier or structural concern]
⚠️ [Token / volatility concern]

WHY THIS MATTERS
━━━━━━━━━━━━━━━━━━━━━━━━━━
- [How this structure behaves if price leaves range]
- [Why concentrated liquidity may improve efficiency but increase management risk]
- [What the user is actually exposed to]

RECOMMENDED ROUTE
━━━━━━━━━━━━━━━━━━━━━━━━━━
- [Deploy now / widen range / reduce size / monitor / avoid]

NEXT CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━
- [What must be verified before adding capital]

---

## Protocol Truth Principles

- concentrated liquidity can improve capital efficiency while increasing active management risk
- a pool can look attractive while still being structurally fragile
- fee yield does not remove range risk
- narrower positioning increases the chance of inactive capital
- apparent TVL is not enough; usable and active liquidity matter
- never confuse APR display with durable LP quality

---

## Concentrated Liquidity Lens

Where concentrated liquidity is involved, ask:
- how narrow is the user’s planned range
- what happens if price exits the active zone
- how actively the position will need maintenance
- whether the user is truly optimizing for fees or unknowingly increasing management burden
- whether the fee tier actually matches expected volatility and activity

---

## Execution Protocol (for AI agents)

When user asks about a PancakeSwap pool, follow this sequence:

### Step 1: Parse the setup
Extract:
- pair
- chain
- pool version
- fee tier
- intended size
- intended range if applicable
- objective (yield / passive LP / capital efficiency / lower risk)

### Step 2: Assess pool and position quality
Review:
- depth
- range exposure
- fee-tier suitability
- structural fragility
- token volatility
- user maintenance burden

### Step 3: Identify weak points
Flag:
- narrow range risk
- shallow liquidity
- strategy mismatch
- high-maintenance position design
- insufficient information for confidence

### Step 4: Translate into decision language
Return:
- whether the pool and position structure look reasonable
- what the biggest risk is
- how to reduce avoidable fragility
- whether to deploy, widen, reduce, monitor, or avoid

### Step 5: Guardrails
If the assessment depends on missing pool or range details:
- say so clearly
- do not fake precision
- recommend further verification before deployment

---

## Activation Rules (for AI agents)

### Use this skill when the user asks about:
- PancakeSwap pool quality
- concentrated liquidity risk
- whether to add liquidity
- range risk
- fee tier risk
- LP structure on PancakeSwap

### Do NOT use this skill when:
- user wants trade execution
- user wants wallet or contract interaction
- user wants formal smart contract verification
- user wants guaranteed safety or yield outcomes

### If context is ambiguous
Ask:
"Do you want a pool-risk and liquidity-structure assessment, or are you asking how to execute a trade?"

---

## Boundaries

This skill supports analytical review of PancakeSwap liquidity decisions.

It does not replace:
- smart contract audit
- wallet security review
- formal DeFi underwriting
- tax or legal advice
