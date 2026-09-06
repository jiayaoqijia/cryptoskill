# Rule: Spec-First Investigation

## MANDATORY — This rule applies to EVERY conversation turn

When the user asks a question about **how existing functionality works**, **whether their understanding is correct**, **reports a bug**, or **directs you to look at specific code** — you MUST consult the specification BEFORE reading any implementation code.

## Trigger Patterns

Apply this rule when the user's message matches ANY of these patterns:

- "How does ... work?" / "How is ... implemented?" / "Explain how ..."
- "Is my understanding correct ...?" / "Am I right that ...?" / "Does it work like ...?"
- "I found a bug ..." / "There's an issue with ..." / "Something is wrong with ..."
- "Look at module ..." / "Look at the code in ..." / "Check the implementation of ..."
- "Refer to ... and answer ..." / "Based on the code in ..."
- "Why does ... behave this way?" / "What is the expected behavior of ...?"
- Any question that requires understanding the intended design or behavior of a feature

## Mandatory Workflow

### Step 1: Consult the Specification FIRST

Before reading ANY implementation code, invoke the `consult-spec` skill to consult SPEC.md about the functionality the user is asking about.

### Step 2: Investigate the Code

With the spec knowledge in mind, read and analyze the relevant implementation code. Focus on understanding what the code actually does.

### Step 3: Compare and Report

Compare the specification requirements with the actual implementation:

- **If they align**: Explain the functionality referencing both the spec requirements and the code that implements them.
- **If they contradict**: Explicitly highlight the discrepancy to the user. Present both sides clearly and ask: "The specification says X, but the code does Y. Which is the current source of truth — should the spec be updated, or is this a code bug?"

## Critical Rules

1. **NEVER skip Step 1.** Even if you think you already know the answer from previous context, the spec consultation ensures unbiased, authoritative grounding.
2. **NEVER rely solely on the spec.** The spec describes intent; the code describes reality. Always verify with actual code in Step 2.
3. **ALWAYS surface contradictions.** Discrepancies between spec and code are high-value findings. Never silently favor one over the other.
4. **Keep spec findings in mind** throughout the entire investigation. They frame your understanding of what the code *should* do.
