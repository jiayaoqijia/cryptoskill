---
name: web3-ux-feedback
description: >
  Analyzes web3 project landing pages and frontend UI to deliver structured UX
  feedback and actionable landing page redesign concepts grounded in the 5-part
  SaaS Messaging Framework. Evaluates visual design, web3-specific UI patterns
  (wallet connection, trust signals, jargon), messaging gaps, and generates
  copy-ready alternative landing page concepts with specific headlines, CTAs,
  and section content. Use when given a web3 project URL, screenshots, or
  description and feedback, marketing analysis, or landing page alternatives
  are needed.
---

# Web3 UX Feedback & Landing Page Messaging Skill

## When to Use This Skill

- User provides a web3 project URL, screenshots, or description and wants feedback
- Request involves "landing page review", "UX analysis", "messaging feedback", or "redesign concepts"
- User wants to understand why their web3 project isn't converting visitors
- User needs alternative landing page copy or redesign direction

## Instructions

### Why Frontend Only

An AI agent cannot safely execute wallet connections, real transactions, or smart
contract interactions. The frontend and landing page is the right scope because:

- Users decide within 5 seconds whether to stay — the landing page is the highest-leverage asset
- Improvements require no backend changes and can ship immediately
- Most web3 projects lose users at the landing page, not inside the app

---

### Core Framework: 5-Part SaaS Messaging Framework (Web3 Edition)

All messaging analysis runs through this framework:

| Part | Key Question | Maps To |
|------|-------------|---------|
| 1. Market | What's changing that makes this relevant now? | Hero context / urgency |
| 2. ICP | Who is this *specifically* for? | Headline targeting |
| 3. Competitive Alternatives | What else could they use today? | Differentiation / positioning |
| 4. Product | What can users *do* now they couldn't before? | Features section |
| 5. Value Proposition | What's the measurable outcome + social proof? | Benefits / CTA |

> **Key distinction:** Messaging = WHAT you say. Copy = HOW you say it.
> Evaluate whether the message is correct before evaluating how it's written.

---

### Step 1 — Gather Input

Identify from materials provided:
- Project type: DeFi, NFT, DAO, L2, GameFi, etc.
- Target audience: crypto native, newcomer, or institutional
- Project stage: pre-launch, MVP, or growth
- Materials: URL, screenshots, or description only

---

### Step 2 — UX/Frontend Evaluation

**First Impression (Above the Fold)**
- Does the hero communicate what this is within 5 seconds?
- Is the value proposition in the headline?
- Is the primary CTA visible without scrolling?
- Are trust signals visible? (audits, TVL, user count)

**Visual Design**
- Typography hierarchy (H1 → H2 → body)
- Color contrast — meets WCAG AA minimum?
- Brand consistency across elements
- White space and mobile responsiveness

**Web3-Specific UI (evaluate without executing)**
- Wallet connection CTA — clarity, placement, wallets listed?
- Gas/fee transparency — shown before connection required?
- Chain/network — which blockchain clearly stated?
- Jargon — are terms like "staking" or "liquidity" explained?
- Security signals — audits, team info, contract addresses findable?

**Navigation & Flow**
- Clear information architecture
- Primary vs. secondary CTA distinction
- Mobile menu usability
- Logical user journey for first-time visitors

**Immediate Red Flags**
- ⚠️ Wallet connection required to view basic information
- ⚠️ No explanation for newcomers (assumes DeFi literacy)
- ⚠️ Generic claims ("decentralized") without specifics
- ⚠️ Security/audit info buried in footer
- ⚠️ Every CTA says "Connect Wallet" — no value-oriented CTAs
- ⚠️ No mobile optimization

---

### Step 3 — Messaging Analysis

Apply each framework part to what is (or isn't) on the page:

**Part 1 — Market Context**
Is there a reason WHY this matters NOW? A market change or trend that creates
urgency? A high-level problem named explicitly?
- Missing → "Visitors don't understand urgency or why this project is timely"

**Part 2 — ICP**
Does the headline speak to a specific person?
```
❌ Too broad:  "For crypto users"
✅ Specific:   "For DeFi traders making 10+ swaps per week"
```

**Part 3 — Competitive Alternatives**
Does the page acknowledge what users do TODAY? Is differentiation explicit?

**Part 4 — Product Capabilities**
Apply the ladder — identify which level the page sits at:
```
Feature (weakest):    "We have multi-sig"
Capability (better):  "Require multiple approvals for treasury transactions"
Benefit (best):       "Your DAO funds stay safe even if one member's wallet is compromised"
```
Translate top 3 features up the ladder in the feedback.

**Part 5 — Value Proposition**
Check all four sub-elements:

| Sub-element | Check |
|-------------|-------|
| Functional benefits (time / money / complexity) | Present? Quantified? |
| Emotional benefits (safety, status, belonging) | Present? |
| Social proof (TVL, users, audits, testimonials) | Present? Specific? |
| Cost of inaction / Why now | Present? |

---

### Step 4 — Generate Landing Page Concepts

Create **2–3 complete concepts**, each with a different strategic angle:

| Angle | Best For |
|-------|----------|
| Power User | Crypto natives — lead with performance and control |
| Web3 Onboarding | Newcomers — lead with simplicity and safety |
| Trust First | DeFi/wallet projects — lead with audits and track record |
| Community Led | DAOs — lead with governance and shared ownership |
| Data Driven | Projects with strong TVL/volume metrics |

**Each concept must include complete copy — not descriptions of copy:**

```
Concept [Letter]: [Name]
Target: [Specific ICP]
Core message: [One sentence]

Hero:
  H1:            [5–10 word headline — outcome, not technology]
  H2:            [10–25 words — how it works + what user gets]
  Primary CTA:   [Action verb + outcome — NOT "Connect Wallet"]
  Secondary CTA: [Lower-commitment option]
  Trust line:    [Audit / TVL / user count beneath buttons]
  Visual:        [Specific description of hero image or animation]

Problem section:
  Headline: [Frame the painful status quo]
  3 pain points: [Icon + 4–6 word headline + 1–2 sentence user-perspective description]

Capabilities (3 entries):
  [Icon] [5–7 word capability headline]
  [15–20 word description of what user can do now]
  Powered by: [feature name]

Social proof:
  Primary metric: [Most impressive number]
  Supporting: [2–3 secondary numbers]
  Logos: [Audit firms first, then partners]

CTA strategy:
  Hero / Mid-page / Bottom / Sticky — different copy each time
  Lower-commitment path for wallet-hesitant users

Tone + visual:
  Voice: [3–5 adjectives]
  Aesthetic: [Color, layout, style direction]
  Avoid: [What NOT to do in this concept]
```

---

### Step 5 — Deliver Report

Structure output exactly as:

```markdown
# [Project Name] — Web3 UX & Messaging Feedback

## Executive Summary
[2–3 sentences: biggest opportunity + most critical fix]

## UX/Frontend Evaluation

### ✅ Strengths
[3–5 specific strengths + why they matter]

### 🚨 Critical Issues
[3–5 issues: Current / Impact / Fix / Priority: High|Medium|Low]

### ⚡ Quick Wins
[3–5 high-impact, low-effort changes]

## Messaging Analysis

### Part 1: Market Context
Status: Missing | Weak | Present | Strong
Current / Gap / Recommendation

### Part 2: ICP
[Same structure]

### Part 3: Competitive Alternatives
[Same structure]

### Part 4: Product Capabilities
[Same structure + feature → capability → benefit translations]

### Part 5: Value Proposition
[Sub-element table + Current / Gap / Recommendation]

### Headline Assessment
Current headline: "[exact copy]"
Assessment: [why it works or doesn't]
Alternatives:
1. "[Specific alternative headline]"
2. "[Specific alternative headline]"
3. "[Specific alternative headline]"

## Landing Page Redesign Concepts

### Concept A: [Name]
[Full structure per template above]

### Concept B: [Name]
[Full structure]

### Concept Comparison
[Table: Target / Tone / Leads with / Best if + recommendation]

## Prioritized Action Plan
[Table: Priority / Action / Impact / Effort / When]

## Competitive Inspiration
[2–3 successful web3 projects + what they do well on their landing page]
```

---

### Quality Checklist

Before delivering, confirm:
- [ ] Analyzed from a first-time visitor perspective, not a crypto expert
- [ ] All 5 framework parts evaluated with explicit gap analysis
- [ ] At least 2 complete concepts with actual copy (not descriptions of copy)
- [ ] Every recommendation is specific — exact words, not "improve the headline"
- [ ] Web3 trust signals flagged (audits, chain info, security)
- [ ] Mobile experience addressed
- [ ] "Why" explained for each recommendation

## Examples

**Example trigger:**
> "Can you review this DeFi protocol's landing page? The hero says 'The Future of Decentralized Finance' and the features are: Multi-chain support, Low fees, Fast execution, Secure protocol."

**What good output looks like:**
- Flags "The Future of Decentralized Finance" as generic — names 3 specific alternative headlines
- Identifies missing ICP — no target user in the headline
- Applies the feature → capability → benefit ladder to all 4 features
- Generates 2 complete redesign concepts with full hero copy, problem section, capabilities, social proof, and CTA strategy
- Prioritizes recommendations by impact/effort in a table

**Common anti-patterns to always flag:**

| Anti-pattern | Example | Fix |
|-------------|---------|-----|
| The Future of X | "The Future of DeFi" | Specific outcome claim |
| Feature dump | 20 features listed | Top 3 capabilities with benefits |
| Generic CTAs | "Connect Wallet" everywhere | Value-oriented CTAs per page section |
| Jargon wall | "Stake LP tokens in our AMM" | Plain language + optional tooltips |
| Trust gap | Audits buried in footer | Audit badge in hero section |
| Everyone & nobody | "For all crypto users" | Specific ICP in headline |