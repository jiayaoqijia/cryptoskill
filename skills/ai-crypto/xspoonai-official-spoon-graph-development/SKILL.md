---
name: spoon-graph-development
description: Build StateGraph workflows with SpoonOS. Use when creating multi-step workflows, conditional routing, parallel execution, checkpointing, or multi-agent orchestration.
---

# Graph Development

Build workflow graphs using SpoonOS StateGraph.

## Quick Start

```python
from spoon_ai.graph import StateGraph, END
from typing import TypedDict

class MyState(TypedDict):
    counter: int
    result: str

async def process(state: MyState) -> dict:
    return {"counter": state["counter"] + 1}

graph = StateGraph(MyState)
graph.add_node("process", process)
graph.set_entry_point("process")
graph.add_edge("process", END)

app = graph.compile()
result = await app.invoke({"counter": 0, "result": ""})
```

## Scripts

| Script | Purpose |
|--------|---------|
| [basic_graph.py](scripts/basic_graph.py) | Simple linear workflow |
| [conditional_graph.py](scripts/conditional_graph.py) | Conditional routing |
| [parallel_graph.py](scripts/parallel_graph.py) | Parallel node execution |
| [checkpoint_graph.py](scripts/checkpoint_graph.py) | State persistence |

## References

| Reference | Content |
|-----------|---------|
| [patterns.md](references/patterns.md) | Common graph patterns |
| [parallel.md](references/parallel.md) | Parallel execution modes |

## Node Types

- **Function nodes**: `async def node(state) -> dict`
- **Agent nodes**: `SpoonReactMCP` instances
- **Subgraph nodes**: Nested `StateGraph`

## Edge Types

- **Direct**: `graph.add_edge("a", "b")`
- **Conditional**: `graph.add_conditional_edges("a", router, {...})`

## Best Practices

1. Use TypedDict for state schemas
2. Return only changed fields from nodes
3. Use checkpointing for long workflows
4. Implement timeout for external calls
