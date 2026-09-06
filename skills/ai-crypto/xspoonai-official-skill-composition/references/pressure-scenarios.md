# Pressure Scenarios — Skills TDD

> **Methodology**: RED → GREEN → REFACTOR
> Each scenario defines a user question, expected behavior, and baseline (without skill).

---

## Scenario 1: Multi-Domain DeFi Query

### Skill Under Test: `skill-composition`
### User Question: "Analyze DeFi protocol security and profitability"
### Expected Behavior:
- [x] Discover at least 2 relevant skills (security + finance domains)
- [x] Detect data-flow dependency: security analysis → profitability report
- [x] Generate Pipeline strategy (sequential, not parallel)
- [x] Confidence coverage ≥ 0.7
- [x] Output valid StateGraph JSON with `__start__` and `__end__` nodes

### Baseline (without skill):
Agent would attempt to answer directly without decomposing into sub-tasks,
missing the structured security → profitability pipeline.

### Test Input:
```json
{"query": "analyze DeFi protocol security and profitability", "provider": "openai"}
```

### Validation Criteria:
- `result.strategy` ∈ {"pipeline", "mixed_dag"}
- `result.skill_count` ≥ 2
- `result.graph.edges` contains at least one inter-skill edge

---

## Scenario 2: Independent Parallel Analysis

### Skill Under Test: `skill-composition`
### User Question: "Review code quality, check security, and audit gas usage"
### Expected Behavior:
- [x] Discover 3 independent skills (code quality, security, gas)
- [x] Detect NO data-flow dependencies between them
- [x] Generate Fan-out/Fan-in strategy (parallel execution)
- [x] Include `__aggregate__` node in graph
- [x] All 3 skills connect to `__start__` and `__aggregate__`

### Baseline (without skill):
Agent would run analyses sequentially, wasting time on independent tasks.

### Test Input:
```json
{
  "query": "review code quality, check security, and audit gas usage",
  "execution_mode": "auto"
}
```

### Validation Criteria:
- `result.strategy` == "fan_out_fan_in"
- `result.execution_mode` == "parallel"
- `result.graph.nodes` contains `__aggregate__`

---

## Scenario 3: Single Skill (No Composition Needed)

### Skill Under Test: `skill-composition`
### User Question: "Audit my smart contract"
### Expected Behavior:
- [x] Discover exactly 1 highly relevant skill
- [x] Generate Direct strategy (no composition)
- [x] Recommendation: COMPOSE (single skill is sufficient)
- [x] Graph has only: `__start__` → skill → `__end__`

### Baseline (without skill):
Agent would still attempt to find and compose multiple skills unnecessarily.

### Test Input:
```json
{"query": "audit my smart contract", "max_skills": 5}
```

### Validation Criteria:
- `result.strategy` == "direct"
- `result.skill_count` == 1
- `len(result.graph.edges)` == 2

---

## Scenario 4: No Skills Match (Graceful Failure)

### Skill Under Test: `skill-composition`
### User Question: "Make me a sandwich"
### Expected Behavior:
- [x] Return success: true with skill_count: 0
- [x] Recommendation: MANUAL_REVIEW
- [x] Include helpful message about broadening search
- [x] No error thrown, no empty graph crash

### Baseline (without skill):
Agent might hallucinate skill matches or crash on empty results.

### Test Input:
```json
{"query": "make me a sandwich"}
```

### Validation Criteria:
- `result.success` == true
- `result.skill_count` == 0
- `result.recommendation` == "MANUAL_REVIEW"

---

## Scenario 5: LLM Unavailable (Degradation)

### Skill Under Test: `skill-composition`
### User Question: "Find security and reporting skills"
### Expected Behavior:
- [x] Fall back to keyword + tag matching (no LLM)
- [x] Still discover relevant skills via heuristic layers
- [x] Tag-based dependency detection still works
- [x] Output valid StateGraph (lower confidence acceptable)

### Baseline (without skill):
Complete failure — no results without LLM.

### Test Input:
```json
{"query": "find security and reporting skills", "use_llm": false}
```

### Validation Criteria:
- `result.success` == true
- `result.skill_count` ≥ 1
- All matching done via keyword/tag layers only

---

## Running Tests

```bash
# Scenario 1: Pipeline detection
echo '{"query": "analyze DeFi protocol security and profitability"}' \
  | python scripts/skill_discovery.py \
  | python scripts/workflow_composer.py \
  | python -c "import json,sys; r=json.load(sys.stdin); assert r['strategy'] in ('pipeline','mixed_dag'), f'Expected pipeline, got {r[\"strategy\"]}'; print('✅ Scenario 1 PASSED')"

# Scenario 4: Graceful empty
echo '{"query": "make me a sandwich"}' \
  | python scripts/skill_discovery.py \
  | python scripts/workflow_composer.py \
  | python -c "import json,sys; r=json.load(sys.stdin); assert r['skill_count']==0; print('✅ Scenario 4 PASSED')"

# Scenario 5: No-LLM degradation
echo '{"query": "find security and reporting skills", "use_llm": false}' \
  | python scripts/skill_discovery.py \
  | python scripts/workflow_composer.py \
  | python -c "import json,sys; r=json.load(sys.stdin); assert r['success']; print('✅ Scenario 5 PASSED')"
```
