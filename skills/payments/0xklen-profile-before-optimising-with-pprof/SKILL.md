---
name: profile-before-optimising-with-pprof
description: Use when a slow service invites a speculative fix — captures CPU and heap profiles under load and names the owning function before any code is changed.
---

# Profile before optimising

Intuition about performance is wrong most of the time. Collect a profile under real load, read the flamegraph, name the function that owns the time or the allocation, then edit one thing and re-measure. Measure, change, measure.

## Procedure

1. Expose the profiler on an internal interface only:
       import _ "net/http/pprof"
       go func(){ log.Println(http.ListenAndServe("127.0.0.1:6060", nil)) }()
   Never bind pprof to `0.0.0.0` in production; it leaks memory contents and is a DoS vector.

2. Capture under representative load, never on an idle box:
       go tool pprof -seconds=30 -output=cpu.pb.gz http://127.0.0.1:6060/debug/pprof/profile
       go tool pprof -output=heap.pb.gz http://127.0.0.1:6060/debug/pprof/heap

3. Read the top of the graph before editing any code:
       go tool pprof -top -nodecount=20 cpu.pb.gz
   The function with the highest `flat` time at a node you own is the target.

4. Separate GC pressure from retention with `-alloc_space` vs `-inuse_space`. High `alloc_space` with low `inuse_space` means short-lived object churn (fix: pooling/reuse); high `inuse_space` means a genuine retention leak — switch to the memory-leak skill.

5. Form one hypothesis, change one line, recapture under identical load. A change that moves p99 by < 5% is noise; keep the commit but do not claim a win.

6. Record before/after as numbers: p50/p99 latency, CPU cores, `allocs/op` from `go test -bench=. -benchmem`. Benchmarks without `-benchmem` hide the allocation story.

7. For Python, use a live sampler with no code change: `py-spy record -o prof.svg --pid <pid> --duration 30` then `py-spy top --pid <pid>` to watch in real time.

## Pitfalls

- Optimising the wrong layer: the flamegraph shows 60% in `json.Unmarshal` because the handler decodes a body it never reads — remove the call, not the decoder.
- Profiling a single request or a cold start; the code path under sustained load differs once pools are warm and branches flip.
- `-seconds=30` too short to catch a job that runs every 5 minutes — capture across at least one full cycle.
- Trusting a micro-benchmark whose result the compiler eliminates; assign the result to a package-level `var sink`.

## Verification

    go tool pprof -top -nodecount=5 cpu.pb.gz | head -8
    go test -run=NONE -bench=BenchmarkHotPath -benchmem ./... | tail -2

Report: the named hotspot and its percentage of CPU, the single code change, and before/after p99 and allocs/op showing at least a 5% improvement.
