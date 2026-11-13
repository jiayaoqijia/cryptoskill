---
name: async-runtimes
domain: software-engineering/async-runtimes
trigger: "Understanding what an async executor does with your tasks."
anti_trigger: "Not for choosing a runtime, and not for distributed execution."
scope: "Executors, scheduling, and the assumptions async breaks."
status: seedling
---

# Async runtimes

## Standard

An async runtime multiplexes many tasks onto fewer threads, suspending each task at an await and resuming it when its I/O completes. The benefit is concurrency without a thread per connection; the cost is that the two guarantees thread-based code silently enjoyed — no other task runs between your statements unless you let it, and your stack frame persists until you return — both weaken. Between your two synchronous statements the runtime runs arbitrary other tasks, so every interleaving that a thread pool permits is now possible inside a function.

The failure modes follow. Blocking the executor — a synchronous sleep, a CPU-bound loop, a lock wait — freezes every task on that thread, a problem threads never had. Task starvation follows unfair scheduling: a long queue of ready tasks behind one runtime-managed dispatch point delays work that a thread-per-connection system would have started immediately. And executor-visible state — thread-local storage, connection pools sized to threads — no longer maps to tasks, so pool exhaustion and stale-context bugs appear in code that was correct before the migration.

Primary sources: <https://martinfowler.com/> and <https://tokio.rs/>.

## Decision rules

- Record the runtime's model: cooperative scheduling on N threads, and what N is.
- Record where CPU-bound work runs: a separate pool, never the executor threads.
- Record every blocking call on the async path and its move to blocking threads.
- Record pool sizing against tasks, not threads, and against each pool's wait tolerance.
- Record the runtime's fairness behaviour for head-of-line scenarios.
- Record what happens when a task panics or the runtime shuts down.

## Procedure

1. Identify the runtime model and its thread count.
2. Audit the async path for blocking calls and move them.
3. Size pools for task concurrency with stated assumptions.
4. Identify thread-local assumptions and replace them with task context.
5. Test with a deliberately slow task mixed into a fast queue and observe starvation.
6. Record the shutdown and panic behaviour.

## Anti-patterns

- A synchronous sleep or file read inside an async task, stalling its thread.
- CPU-bound work executed inline, starving every task on the worker.
- Pools sized to the thread count in a runtime with thousands of tasks.
- Thread-local context read from a task that migrated threads between awaits.
- Blocking-lock acquisition inside async code, invisible in review but fatal on one thread.

## Done checklist

- [ ] Runtime model and thread count recorded.
- [ ] Blocking calls audited and moved.
- [ ] Pools sized against tasks.
- [ ] Thread-local assumptions removed.
- [ ] Starvation tested with a slow task.
- [ ] Shutdown and panic behaviour recorded.

## Sources

- Async architecture patterns: <https://martinfowler.com/>
- Executor design: <https://tokio.rs/>
- Concurrency literature: <https://dl.acm.org/>
