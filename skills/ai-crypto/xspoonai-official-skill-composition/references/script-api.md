# Script API Reference

> I/O specifications for the Skill Composition Engine scripts.

## Protocol

Both scripts follow the **SpoonOS stdin/stdout JSON protocol**:

```
echo '<JSON input>' | python scripts/<script>.py
# → JSON output on stdout
# → Errors on stderr + exit code 1
```

Scripts can be piped together:

```
echo '<input>' | python scripts/skill_discovery.py | python scripts/workflow_composer.py
```

---

## skill_discovery.py

### Input

```json
{
  "query": "string (required) — user intent or task description",
  "skill_registry_path": "string (optional, default: '.') — path to scan for SKILL.md files",
  "max_skills": "integer (optional, default: 5, range: 1-10) — max skills to return",
  "provider": "string (optional, default: 'openai') — LLM provider: openai|anthropic|deepseek",
  "use_llm": "boolean (optional, default: true) — enable LLM semantic matching"
}
```

### Output

```json
{
  "success": true,
  "query": "original query",
  "registry_path": "/absolute/path/to/registry",
  "total_skills_scanned": 12,
  "matches_found": 3,
  "elapsed_ms": 1250,
  "provider": "openai",
  "use_llm": true,
  "matches": [
    {
      "skill_name": "Skill Name",
      "score": 0.92,
      "tier": "semantic|tag|keyword|none",
      "matched_keywords": ["keyword1", "keyword2"],
      "matched_tags": ["tag1", "tag2"],
      "semantic_reasoning": "LLM explanation of match quality",
      "metadata": {
        "description": "Skill description from SKILL.md",
        "version": "1.0.0",
        "author": "author-name",
        "tags": ["tag1", "tag2"],
        "composable": true,
        "file_path": "/path/to/SKILL.md",
        "scripts": ["script1.py", "script2.py"],
        "parameters": [
          {
            "name": "param_name",
            "type": "string",
            "required": true,
            "default": null,
            "description": "Parameter description"
          }
        ]
      }
    }
  ]
}
```

### Error Output

```json
{
  "error": "Missing required parameter: query"
}
```

---

## workflow_composer.py

### Input

Accepts the output of `skill_discovery.py` directly (pipe-compatible), or a manual input:

```json
{
  "query": "string (required) — user intent",
  "matches": "array (required) — skill matches from discovery or manual",
  "execution_mode": "string (optional, default: 'auto') — auto|sequential|parallel|mixed",
  "provider": "string (optional, default: 'openai') — LLM provider for dependency analysis",
  "use_llm": "boolean (optional, default: true) — enable LLM dependency analysis"
}
```

### Output

```json
{
  "success": true,
  "query": "original query",
  "skill_count": 3,
  "strategy": "pipeline|fan_out_fan_in|mixed_dag|direct",
  "execution_mode": "sequential|parallel|mixed",
  "graph": {
    "nodes": [
      {"id": "__start__", "type": "entry", "label": "Start"},
      {"id": "skill_node_id", "type": "skill", "label": "Skill Name", "scripts": [...], "parameters": [...]},
      {"id": "__aggregate__", "type": "aggregator", "label": "Aggregate Results"},
      {"id": "__end__", "type": "terminal", "label": "End"}
    ],
    "edges": [
      {"source": "__start__", "target": "skill_node_id"},
      {"source": "skill_node_id", "target": "__end__", "data_mapping": "description of data flow"}
    ],
    "entry_point": "__start__",
    "terminal_nodes": ["__end__"],
    "execution_mode": "sequential",
    "strategy": "pipeline",
    "state_schema": {
      "type": "object",
      "properties": {
        "query": {"type": "string"},
        "current_step": {"type": "string"},
        "completed_steps": {"type": "array"},
        "results": {"type": "object"},
        "errors": {"type": "array"}
      }
    },
    "estimated_steps": 3
  },
  "dependency_analysis": [
    {
      "source": "skill_a",
      "target": "skill_b",
      "type": "data_flow",
      "confidence": 0.85,
      "reasoning": "Skill A output feeds Skill B input"
    }
  ],
  "confidence": {
    "coverage": 0.885,
    "compatibility": 0.8,
    "recommendation": "COMPOSE|PARTIAL_COMPOSE|MANUAL_REVIEW"
  },
  "recommendation": "COMPOSE",
  "elapsed_ms": 450
}
```

### Error Output

```json
{
  "error": "Workflow composition failed: <details>"
}
```

---

## Node Types

| Type | ID Pattern | Description |
|------|-----------|-------------|
| `entry` | `__start__` | Graph entry point |
| `skill` | `<sanitized_name>` | Skill execution node |
| `aggregator` | `__aggregate__` | Fan-in result aggregation |
| `terminal` | `__end__` | Graph exit point |

## Edge Properties

| Property | Type | Description |
|----------|------|-------------|
| `source` | string | Source node ID |
| `target` | string | Target node ID |
| `condition` | string (optional) | Conditional routing expression |
| `data_mapping` | string (optional) | Description of data flowing along this edge |
