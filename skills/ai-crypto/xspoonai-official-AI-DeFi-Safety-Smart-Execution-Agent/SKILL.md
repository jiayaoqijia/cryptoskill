# AI DeFi Safety & Smart Execution Agent

## Skill Overview
The **AI DeFi Safety & Smart Execution Agent** is an AI-powered Web3 skill that transforms a user’s DeFi intent (such as token swaps) into a **safe, simulated, and explainable execution plan**.  
Instead of blindly executing transactions, the agent evaluates token risks, simulates execution paths, scores safety, and provides a clear recommendation before any on-chain action is taken.

---

## Core Capabilities

### 1. DeFi Intent Understanding
The skill accepts high-level user intent such as:
- Swap token X to token Y
- Specify chain and amount
- Optional slippage and risk tolerance

This allows non-technical users or agents to express actions in a simple, human-readable format.

---

### 2. Token Safety & Risk Analysis
For the involved tokens, the agent analyzes:
- Liquidity depth
- Holder concentration
- Honeypot / blacklist behavior (heuristic or API-based)
- Centralization risks (admin privileges, pause/mint indicators)

The result is a structured list of risk flags and an intermediate token risk assessment.

---

### 3. Swap Simulation & Execution Feasibility
Before recommending execution, the skill:
- Simulates the swap route (DEX aggregation or heuristic simulation)
- Estimates expected output
- Evaluates slippage impact
- Estimates gas cost
- Flags potential MEV or instability risks

This ensures the action is **feasible and transparent** before execution.

---

### 4. Safety Scoring & Verdict Engine
All signals are aggregated into a single **Safety Score (0–100)** with a clear verdict:
- **SAFE** (80–100)
- **CAUTION** (50–79)
- **DANGEROUS** (<50)

This allows both humans and agents to make quick, informed decisions.

---

### 5. AI Explainability Layer
An AI reasoning layer converts technical risk signals into **plain-English explanations**, answering:
- Why the action is safe or risky
- What the primary dangers are
- What the user should be careful about

This makes the skill accessible even to non-expert users.

---

## Input Schema (Example)

```json
{
  "action": "swap",
  "from_token": "USDC",
  "to_token": "ETH",
  "amount": 500,
  "chain": "Arbitrum",
  "max_slippage": 1.0,
  "risk_tolerance": "medium"
}
```
