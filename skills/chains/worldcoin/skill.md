---
name: Worldcoin
description: >
  Filter human-critical workflows using proof-of-human logic.
  Designed for identity-sensitive commercial decisions, anti-bot gating,
  and “real human required” checkpoints across proposals, leads, and approvals.
version: 1.0.0
---

# Worldcoin

> **In an AI-saturated world, not every click deserves your trust.**

Worldcoin is a human-verification decision skill for workflows where “real human required” matters.

This skill is inspired by proof-of-humanity logic:
not every action should be treated as equally trustworthy,
and not every response should be assumed to come from a real, decision-capable person.

Use this skill when you need to:
- decide whether a workflow step should require stronger human verification
- separate bot-risk from human-trust actions
- add “human checkpoint” logic to lead, proposal, approval, or access flows
- determine which actions should only happen after stronger identity confidence
- reduce spam, fake engagement, or synthetic participation in sensitive workflows

This skill does NOT:
- perform biometric verification
- connect to World ID, Orb, World App, or any external identity API
- replace legal identity checks, KYC, AML, or compliance review
- certify that a person is verified on any external network

---

## What This Skill Does

Worldcoin helps:
- identify where proof-of-human logic is useful
- classify workflow steps by human-trust sensitivity
- determine where anonymous access is acceptable vs where stronger verification is needed
- reduce approval, lead, or offer workflows being distorted by bots or fake actors
- design “human required” checkpoints for digital systems

---

## Best Use Cases

- filtering fake or low-trust inbound lead submissions
- deciding which proposal approvals should require stronger human confirmation
- gating voting, claiming, or reward flows
- anti-bot logic for creator or platform campaigns
- deciding where proof-of-human is commercially worth the friction
- designing trust layers for identity-sensitive products

---

## What to Provide

Useful input includes:
- the workflow being protected
- what action the user wants to secure
- what the main abuse risk is
- whether the risk is bots, duplicate identities, fake leads, or low-trust engagement
- what level of friction is acceptable
- what commercial or operational downside exists if fake actors get through

---

## Standard Output Format

WORLDCOIN ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━
Workflow: [What is being protected]
Main Risk: [Bot / fake human / duplicate / low-trust action]

HUMAN-TRUST SENSITIVITY
━━━━━━━━━━━━━━━━━━━━━━━━━━
Level: [Low / Medium / High / Critical]

WHY IT MATTERS
━━━━━━━━━━━━━━━━━━━━━━━━━━
- [Why stronger human verification may matter here]
- [What happens if fake actors get through]
- [What business or trust damage follows]

VERIFICATION THRESHOLD
━━━━━━━━━━━━━━━━━━━━━━━━━━
Recommended level:
- [Open access]
- [Soft human check]
- [Strong human-required gate]
- [Escalate to formal identity / compliance process]

TRADEOFFS
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ [Added friction]
⚠️ [Drop in conversion]
⚠️ [False negatives / accessibility concern]
⚠️ [Operational complexity]

RECOMMENDED NEXT STEP
━━━━━━━━━━━━━━━━━━━━━━━━━━
- [What checkpoint or policy to add next]

---

## Human Verification Principles

- not every workflow needs maximum identity friction
- stronger proof should be used where fake participation meaningfully distorts outcomes
- friction should match risk
- proof-of-human logic is different from legal identity logic
- commercial trust decisions should separate low-stakes participation from high-stakes approval
- never claim certainty where only probability exists

---

## Human Proxy Lens

Think of this skill as a **human proxy filter**.

Its job is not to verify people directly.  
Its job is to answer:

- **Where does this workflow break if non-human or duplicate actors get through?**
- **Where is “good enough” trust sufficient?**
- **Where is stronger proof of humanness worth the friction?**

---

## Execution Protocol (for AI agents)

When user asks about verification or human-trust workflow design, follow this sequence:

### Step 1: Parse the workflow
Extract:
- what the user is trying to protect
- who is interacting
- what action is being taken
- what abuse or fraud risk exists
- what trust level the workflow really needs

### Step 2: Classify risk
Classify the primary concern:
- bot volume
- duplicate participation
- fake lead quality
- false approvals
- reward abuse
- synthetic engagement distortion

### Step 3: Assess sensitivity
Determine whether the workflow is:
- low stakes
- medium stakes
- high stakes
- critical trust

### Step 4: Recommend trust layer
Choose the lightest acceptable level:
- open access
- soft gating
- stronger human verification gate
- escalate to formal identity / compliance process

### Step 5: Show tradeoffs
Explain:
- user friction
- conversion impact
- operational burden
- trust benefit

### Step 6: Guardrails
If the user needs regulated identity, financial compliance, or formal verification:
- say so clearly
- do not pretend proof-of-human equals legal identity
- recommend specialist or regulated review

---

## Activation Rules (for AI agents)

### Use this skill when the user asks about:
- proof of human
- anti-bot workflow design
- fake lead filtering
- identity-sensitive approvals
- real-human gating
- trust layers for digital actions
- duplicate participation risk
- synthetic engagement prevention

### Do NOT use this skill when:
- user needs actual biometric verification
- user needs direct World ID integration steps
- user needs KYC / AML / legal identity review
- user wants technical API implementation details that are not provided

### If context is ambiguous
Ask:
"Do you want help designing a human-verification decision layer, or do you need actual product/API integration?"

---

## Works Well With

- `@dpetcr/proposal` when approvals should only count after stronger human trust
- `@AGIstack/lead` when fake or low-trust inbound leads need filtering
- `@ethagent/xmoney` when rewards or monetization flows are vulnerable to fake participation

---

## Boundaries

This skill supports decision design for proof-of-human-style workflow logic.

It does not replace:
- biometric verification
- legal identity verification
- KYC / AML checks
- privacy review
- regulated compliance decisions

Use outputs as workflow design guidance, not as formal identity certification.
