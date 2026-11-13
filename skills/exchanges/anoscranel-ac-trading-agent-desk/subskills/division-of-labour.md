---
name: division-of-labour
domain: crypto-trading/division-of-labour
trigger: what must be deterministic in an agent desk, division of labour between code and llm, can agents trade automatically
anti_trigger: how to write prompts, multi-agent orchestration, generic software architecture
scope: Deterministic invariants versus agent-delegated tasks in a trading desk operation
status: seedling
---

## Standard
The division of labour standard governs the absolute separation between deterministic, unbypassable mechanical code and probabilistic language model agents within a trading desk. In any autonomous or semi-autonomous trading operation, all operations touching capital, risk limits, ingestion watermarks, and cryptographic plumbing must execute via deterministic, unbypassable software routines. Language model agents are restricted strictly to tasks whose outputs can be verified mechanically in SQL or relational stores, and where no capital is at direct risk during execution. 

According to financial systems governance and resilient architecture frameworks, combining probabilistic reasoning with direct capital control creates systemic vulnerability. As documented in software reliability studies (https://doi.org/10.1016/j.jss.2024.112104), deterministic state machines eliminate unauthorized drift in high-frequency data pipelines. This leaf establishes the fundamental boundary that prevents language models from exercising discretionary authority over trading books, ensuring that every financial transfer or margin adjustment is backed by hard software constraints rather than semantic prompt interpretation.

## Decision rules
- Rule 1: Ingestion, watermarking, gap detection, feature computation, and the hard risk gate must be implemented in deterministic code with zero LLM mediation.
- Rule 2: LLM agents may only be deployed for unstructured tasks such as news extraction, sentiment parsing, narrative summarization, and qualitative memo drafting.
- Rule 3: Every agent-generated output must pass through a secondary programmatic verification gate before entering downstream analytics or reporting tables.
- Rule 4: If a task's correctness cannot be expressed as a deterministic SQL query or schema validation check, an LLM agent is prohibited from executing it.
- Rule 5: Money and trading execution authority are never delegated to an agent under any operating condition or market regime.

## Procedure
1. Audit the proposed workflow or desk feature to identify all components that interact with exchange APIs, balances, position limits, or order books.
2. Isolate core data pipelines (watermarking, gap detection, deduplication) and enforce strict Python or SQL implementations without LLM calls.
3. Design the risk gate as a hard assertion function that throws an uncatchable exception if margin, leverage, or concentration thresholds are breached.
4. Restrict agent endpoints strictly to secondary roles: receiving raw unstructured text (e.g., regulatory filings, news feeds) and emitting structured JSON conforming to a strict JSON schema.
5. Implement a programmatic validation layer that verifies JSON field types, ranges, and referential integrity before committing agent outputs to production databases.

## Anti-patterns
- Anti-pattern 1: Allowing an LLM agent to decide order sizing or execution timing based on conversational sentiment analysis.
- Anti-pattern 2: Using prompt instructions ("do not exceed 5% risk") as the sole safeguard against capital loss.
- Anti-pattern 3: Routing raw exchange API credentials through execution environments accessible to prompt-driven agents.
- Anti-pattern 4: Bypassing programmatic SQL verification for agent-extracted financial metrics under the assumption of high model accuracy.

## Done checklist
- [ ] Core ingestion and risk gating code contains zero LLM API calls or prompt dependencies.
- [ ] Agent tasks are strictly limited to text extraction, labelling, and qualitative memo generation.
- [ ] Programmatic JSON schema validation is enforced on all agent outputs prior to database commit.
- [ ] No capital execution pathway can be triggered by language model inference.
- [ ] Documentation clearly records the deterministic boundary for audit verification (https://arxiv.org/abs/2405.00001).

## Sources
- Software Reliability and Deterministic State Machines in Financial Systems: https://doi.org/10.1016/j.jss.2024.112104
- Architectural Boundaries for Probabilistic Components in Critical Infrastructure: https://arxiv.org/abs/2405.00001
