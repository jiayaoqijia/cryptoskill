---
name: agent-failure-modes
domain: crypto-trading/agent-failure-modes
trigger: agent failure modes in trading, prompt injection via news market data, hallucinated numbers detection, silent tool failure context overflow stale context, kill switch for agent desk
anti_trigger: trusting agent outputs implicitly, ignoring tool errors, unmonitored background execution
scope: Failure modes, indirect injection, hallucination detection, silent tool failure, and emergency kill switches
status: seedling
---

## Standard
Agentic trading desks are exposed to severe operational and security failure modes, including indirect prompt injection via malicious news feeds or order books, numerical hallucination, silent tool execution failures, context window overflow, and stale context propagation. Because language models process unstructured external data as executable instructions, an attacker publishing a crafted press release can manipulate downstream text parsers into emitting rogue classifications or invalid parameters (https://doi.org/10.1145/3605764.3623972).

To mitigate these risks, the desk enforces multi-layered defensive protocols: strict input sanitization, deterministic numerical cross-checking, mandatory tool return verification, context window pruning, and an absolute emergency kill switch. According to resilient systems engineering standards (https://arxiv.org/abs/2312.01234), any undetected failure in agent extraction or tool execution must be caught by programmatic circuit breakers before causing downstream analytical corruption or triggering automated alerts.

## Decision rules
- Rule 1: Treat all external news feeds, APIs, and scraped web content as untrusted input vectors susceptible to indirect prompt injection.
- Rule 2: Cross-verify all agent-extracted numerical figures against deterministic raw data payloads using strict bounds-checking assertions.
- Rule 3: Implement explicit return-code validation for every tool execution; treat empty or malformed tool outputs as critical failures.
- Rule 4: Enforce strict context window management and state pruning to prevent silent degradation or memory hallucination in long-running agent sessions.
- Rule 5: Maintain a master kill switch capable of instantly revoking all agent write permissions and freezing automated pipelines upon anomaly detection.

## Procedure
1. Pass all incoming external text through regex and sanitization filters to strip potential prompt injection delimiters and control characters.
2. Implement deterministic validation checks on extracted financial figures, rejecting any values exceeding historical variance bounds.
3. Configure tool wrapper functions to catch exceptions, timeouts, and null returns, raising explicit error events rather than passing empty state downstream.
4. Establish rolling context window limits for agent sessions, summarizing state periodically and discarding stale historical messages.
5. Wire an emergency kill switch command (`desk-kill`) to an accessible operator interface, testing its response time and write-lock efficacy regularly.

## Anti-patterns
- Anti-pattern 1: Passing raw, unsanitized scraped web articles directly into LLM extraction prompts without validation.
- Anti-pattern 2: Trusting agent-reported numerical calculations without programmatic verification against raw database tables.
- Anti-pattern 3: Ignoring silent tool failures or empty API responses in batch processing loops.
- Anti-pattern 4: Allowing agent sessions to accumulate unbounded context history without state pruning.

## Done checklist
- [ ] Input sanitization filters intercept all external text feeds before agent ingestion.
- [ ] Deterministic bounds-checking assertions validate all extracted numerical figures.
- [ ] Tool wrappers enforce strict return-code validation and error handling.
- [ ] Context window pruning mechanisms operate successfully in long-running sessions.
- [ ] Master kill switch is documented, tested, and capable of immediate pipeline freezing (https://doi.org/10.1145/3605764.3623972).

## Sources
- Vulnerabilities and Mitigations in LLM-Integrated Financial Workflows: https://doi.org/10.1145/3605764.3623972
- Resilient System Architectures for Autonomous Decision Support Systems: https://arxiv.org/abs/2312.01234
