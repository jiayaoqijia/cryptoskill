---
name: Raydium
description: >
  Audit Raydium liquidity positions before capital is deployed.
  Analyze pool depth, concentration, liquidity quality, structural risks,
  and parameter changes so users can make cleaner LP decisions.
version: 1.0.0
---

# Raydium

> **Do not add liquidity to a pool you have not interrogated.**

Raydium is a protocol-truth-enforcer skill for liquidity decisions.

This skill is designed for users who want to evaluate Raydium pools before adding liquidity, moving size, or treating a pool as trustworthy.

Use this skill when you need to:
- assess whether a Raydium pool looks healthy enough for LP deployment
- evaluate liquidity depth and concentration risk
- detect structural weakness before adding capital
- reason about pool quality, not just APR or hype
- review whether a pool looks durable, shallow, manipulated, or fragile

This skill does NOT:
- execute trades
- add or remove liquidity
- connect to Raydium contracts or wallets
- guarantee pool safety
- replace smart contract review or formal DeFi risk assessment

---

## What This Skill Does

Raydium helps:
- examine the quality of a liquidity pool before capital is deployed
- evaluate whether apparent liquidity is deep, thin, or misleading
- identify concentration, slippage, or fragility risks
- reason about pool structure in plain language
- separate attractive-looking pools from trustworthy pools

---

## Best Use Cases

- pre-LP audit before adding liquidity
- pool quality review for Solana LP strategies
- concentration-risk review
- slippage-risk screening
- evaluating whether pool depth can support intended size
- reviewing whether a pool is too shallow, too unstable, or too dependent on narrow conditions

---

## What to Provide

Useful input includes:
- pool pair
- intended capital size
- visible pool depth
- recent activity or fee information
- whether the pool uses concentrated liquidity
- any known concerns about token quality, volatility, or parameter changes
- what the user is optimizing for: yield, stability, or execution quality

If information is incomplete, this skill should state what is missing instead of pretending the pool can be fully assessed.

---

## Standard Output Format

RAYDIUM POOL ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━
Pool: [Pair]
Intent: [Provide liquidity / assess pool / screen risk]

LIQUIDITY TRUTH
━━━━━━━━━━━━━━━━━━━━━━━━━━
Depth Quality: [Strong / Moderate / Thin / Fragile]
Concentration Risk: [Low / Medium / High]
Execution Risk: [Low / Medium / High]

MAIN CONCERNS
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ [Depth concern]
⚠️ [Concentration concern]
⚠️ [Token / volatility concern]
⚠️ [Structural uncertainty]

WHY THIS MATTERS
━━━━━━━━━━━━━━━━━━━━━━━━━━
- [How the pool may behave under size or volatility]
- [Why apparent TVL may or may not equal usable liquidity]
- [Where LP capital is most exposed]

RECOMMENDED ROUTE
━━━━━━━━━━━━━━━━━━━━━━━━━━
- [Deploy now / deploy smaller / monitor first / avoid]

NEXT CHECK
━━━━━━━━━━━━━━━━━━━━━━━━━━
- [What should be verified before capital is added]

---

## Protocol Truth Principles

- apparent liquidity is not the same as usable liquidity
- LP yield without depth quality can be deceptive
- concentrated liquidity can improve capital efficiency while increasing range and positioning risk
- thin pools punish size disproportionately
- protocol familiarity does not remove pair-level risk
- never confuse activity with resilience

---

## Risk Review Lens

When evaluating a Raydium pool, focus on:
- how much liquidity actually supports the intended trade or LP size
- whether liquidity is concentrated in a narrow active range
- whether the underlying pair is structurally unstable
- whether the pool looks durable under volatility
- whether the user's size is too large relative to usable depth

---

## Execution Protocol (for AI agents)

When user asks about a Raydium pool, follow this sequence:

### Step 1: Parse the setup
Extract:
- token pair
- intended size
- purpose (LP / screening / execution)
- any visible depth or activity data
- user objective (yield / lower risk / execution quality)

### Step 2: Assess pool quality
Review:
- depth
- concentration
- volatility exposure
- structural fragility
- pair-level risk

### Step 3: Identify weak points
Flag:
- shallow depth
- concentrated active liquidity
- unstable or low-trust token pair
- size that may be too large for the pool
- missing information that prevents confidence

### Step 4: Translate into decision language
Return:
- whether the pool looks robust enough
- where the main risks are
- what size or caution adjustment is appropriate
- whether the user should deploy, reduce size, watch, or avoid

### Step 5: Guardrails
If the assessment depends on missing on-chain details:
- say so clearly
- do not fake precision
- recommend further verification before deployment

---

## Activation Rules (for AI agents)

### Use this skill when the user asks about:
- Raydium pool quality
- whether to add liquidity
- LP risk on Raydium
- pool depth
- concentrated liquidity risk
- slippage or liquidity concerns on Raydium

### Do NOT use this skill when:
- user wants trade execution
- user wants wallet or contract interaction
- user wants guaranteed safety
- user asks for direct smart contract verification not available in the prompt

### If context is ambiguous
Ask:
"Do you want a pool-risk and liquidity-quality assessment, or are you asking how to execute a trade?"

---

## Boundaries

This skill supports analytical review of Raydium liquidity decisions.

It does not replace:
- smart contract audit
- wallet security review
- formal DeFi risk underwriting
- tax or legal advice
