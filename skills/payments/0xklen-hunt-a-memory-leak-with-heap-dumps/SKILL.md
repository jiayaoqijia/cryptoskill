---
name: hunt-a-memory-leak-with-heap-dumps
description: Use when resident memory climbs steadily and never falls — diffs two heap profiles to find the growing retainer instead of guessing at caches, and proves the plateau after the fix.
---

# Hunt a memory leak with heap dumps

A leak is memory retained by something still reachable. Prove it by diffing two heap snapshots taken minutes apart under steady load: the type that grows is the retainer. Raising the limit only delays the OOM.

## Procedure

1. Confirm it is a leak rather than a cache warming up. Sample RSS at constant traffic:
       while true; do ps -o rss= -p $PID; sleep 60; done
   Monotonic growth past warmup with no plateau is a leak; a plateau is a bounded cache.

2. Capture two heap profiles five minutes apart under the same load:
       go tool pprof -output=h1.pb.gz http://127.0.0.1:6060/debug/pprof/heap
       sleep 300
       go tool pprof -output=h2.pb.gz http://127.0.0.1:6060/debug/pprof/heap

3. Diff them — only the delta matters:
       go tool pprof -base=h1.pb.gz -inuse_space -top -nodecount=20 h2.pb.gz
   The top frame is the allocator holding the growth.

4. For a JVM, take `jmap -dump:live,format=b,file=h1.hprof <pid>` twice, open both in Eclipse MAT, run Leak Suspects, and compare dominator trees.

5. Classify the retainer by pattern: an unbounded map keyed by user id with no TTL; goroutines blocked on a channel that never drains; a `[]byte` buffer grown and never trimmed; listener/observer registrations never removed; a `context` stored in a long-lived struct.

6. Falsify alternatives with a targeted experiment before fixing: hit the suspect endpoint 1000 times, recapture, and show the retainer's `inuse_space` grew roughly linearly with calls. Growth tied to a specific path excludes the other suspects.

7. Fix, then prove the plateau: run 30 minutes at load and require RSS to stay within 5% across the last ten samples.

## Pitfalls

- Reading `alloc_space` and calling it a leak: it counts all allocation ever and grows by definition. Only `inuse_space` measures retention.
- A "leak" that is really the GC not having run — force `runtime.GC()` (Go) or `System.gc()` (JVM) and re-read `inuse` before concluding.
- Fixing the symptom by shrinking payloads to slow the growth while the unbounded map remains.
- One snapshot at one instant: without a diff you cannot separate the working set from the leak.

## Verification

    go tool pprof -base=h1.pb.gz -inuse_space h2.pb.gz <<< 'top5'
    ps -o rss= -p $PID    # last 10 one-minute samples within 5% after the fix

Report: the retainer type, its growth rate in MB/hour before the fix, and the RSS plateau after with the sampling window that proves it.
