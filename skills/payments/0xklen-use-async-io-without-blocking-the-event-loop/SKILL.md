---
name: use-async-io-without-blocking-the-event-loop
description: Use when an async service shows latency equal to a dependency's response time — find the blocking call on the event loop and move it to a thread or process pool.
---

# Use async I/O without blocking the event loop

In async runtimes (Node, Python asyncio), one synchronous call blocks every other request on that loop. The signature is stark: p99 latency tracks an unrelated operation's duration, and throughput does not improve when that dependency gets faster.

## Procedure

1. Detect the block. Python: set `PYTHONASYNCIODEBUG=1` and `loop.slow_callback_duration = 0.05`, or watch an event-loop-lag metric. Node: a latency histogram around `setImmediate`, plus `--trace-warnings`.
2. Find synchronous calls on async paths: `requests`, `urllib`, `time.sleep`, direct file reads, `subprocess.run`, CPU-heavy loops, and high-cost `bcrypt` or `hashlib` on large inputs.
3. Move blocking I/O to a thread pool, wrapping the call:
```python
await loop.run_in_executor(None, blocking_fn, arg)
await asyncio.to_thread(requests.get, url)
```
   Or switch to a native async client: `httpx.AsyncClient`, `aiofiles`, `asyncpg`.
4. Move CPU-bound work to a *process* pool, not a thread pool — the GIL serializes Python bytecode across threads:
```python
loop.run_in_executor(ProcessPoolExecutor(), crunch, data)
```
5. For Node, drop to a worker thread or child process for CPU work; `fs.readFileSync` and `crypto.pbkdf2Sync` block the whole server.
6. Treat event-loop lag as a first-class metric (`event_loop_lag_seconds`) and alert when it exceeds a few tens of milliseconds; lag is the direct measure of blocking.
7. Profile with a live sampler (`py-spy`, `--prof`) to name the blocking function rather than guessing.

## Pitfalls

- Calling `asyncio.run` inside a running loop, which raises "loop already running" — a symptom of a sync library in disguise.
- Using a thread pool for CPU work and expecting speedup; the GIL serializes it.
- Covering the symptom with a bigger thread pool instead of removing the blocking call.
- A synchronous ORM or driver in an async framework; a thread pool cannot fully hide it.
- Missing `await` on a coroutine, so it never runs and returns a coroutine object.
- Blocking in a startup hook or signal handler, delaying the whole process before it serves anything.

## Verification

    curl -s localhost:9090/metrics | grep event_loop_lag_seconds
    python -X dev -c "import asyncio; asyncio.get_event_loop().slow_callback_duration = 0.05"
    # pass: lag p99 < 50ms under load; throughput scales when the dependency speeds up

Report the blocking call found, where it was moved (thread vs process pool), the loop-lag metric before and after, and the throughput change.
