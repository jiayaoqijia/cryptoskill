# Common Graph Patterns

## Linear Pipeline

```python
graph.add_edge("input", "process")
graph.add_edge("process", "output")
graph.add_edge("output", END)
```

## Fan-Out / Fan-In

```python
# Fan out to parallel nodes
graph.add_edge("start", "worker_1")
graph.add_edge("start", "worker_2")
graph.add_edge("start", "worker_3")

# Fan in to aggregator
graph.add_edge("worker_1", "aggregate")
graph.add_edge("worker_2", "aggregate")
graph.add_edge("worker_3", "aggregate")
```

## Conditional Branching

```python
def router(state) -> str:
    if state["score"] > 0.8:
        return "high_quality"
    return "low_quality"

graph.add_conditional_edges(
    "evaluate",
    router,
    {"high_quality": "approve", "low_quality": "reject"}
)
```

## Loop with Exit Condition

```python
def should_continue(state) -> str:
    if state["iterations"] >= state["max_iterations"]:
        return "exit"
    if state["quality"] >= state["threshold"]:
        return "exit"
    return "continue"

graph.add_conditional_edges(
    "improve",
    should_continue,
    {"continue": "improve", "exit": END}
)
```

## Human-in-the-Loop

```python
graph.add_node("review", human_review_node)
graph.add_node("wait", wait_for_approval)

# Interrupt before review
graph.add_edge("process", "review")

# Configure interrupt points
app = graph.compile(interrupt_before=["review"])
```

## Subgraph Composition

```python
# Create subgraph
sub = StateGraph(SubState)
sub.add_node("a", node_a)
sub.add_node("b", node_b)

# Embed in parent
parent = StateGraph(ParentState)
parent.add_node("sub", sub.compile())
```
