---
name: detect-data-races-with-thread-sanitizer
description: Use when shared mutable state across threads is suspected — builds and runs the binary under ThreadSanitizer and triages every reported race as real until proven otherwise.
---

# Detect data races with ThreadSanitizer

A race is a correctness bug that passes tests and then corrupts state under production concurrency. ThreadSanitizer is the only reliable detector: build an instrumented binary, drive the real concurrent path, and treat every report as a genuine bug.

## Procedure

1. Build instrumented: Go `go test -race ./...` or `go build -race`; C/C++/Rust `-fsanitize=thread -g -O1`. TSan needs `-g` and light optimisation to resolve frames.

2. Run the real concurrent workload, not a toy unit test — TSan only reports a race it observes:
       go test -race -run TestConcurrentPlaceOrder -count=10 ./...
   `-count=10` raises the odds of hitting the interesting interleaving.

3. Read the report top-down. The header names `Write at 0x... by goroutine N` and `Previous read at 0x... by goroutine M`; the shared address both touch is the subject under investigation.

4. Classify the pattern: unsynchronised shared field; a map read concurrent with a write (in Go this is a fatal crash, not just a report); `WaitGroup`/channel misuse; a copied slice header so two `append`s diverge onto separate backing arrays.

5. Fix with the cheapest correct tool in order: stop sharing (copy the value), message-pass over a channel, then a mutex or atomic. Do not reach for one global lock first — it serialises the hot path.

6. Use `atomic.Int64` for counters and a mutex-guarded or `sync.Map` for shared maps; a plain Go `map` written from two goroutines aborts the process.

7. Re-run `-race -count=50` until clean, then make a `-race` run a required CI gate so the race cannot silently return.

## Pitfalls

- Declaring a race "benign". There is no benign race: the program's result is unspecified, and it will surface as corruption under a different CPU or scheduler.
- Running TSan only on a small test while the race lives in a boot-time background goroutine — start the real service under `-race` for a soak.
- Forgetting that `-race` changes timing and disables some CGO paths, hiding the very race you chase. Keep a non-race run too.
- A report whose accessing goroutine is the runtime or GC usually means a pointer to a stack object escaped across goroutines.

## Verification

    go test -race -count=50 ./... 2>&1 | tail -3
    grep -c 'DATA RACE' /tmp/race-run.log     # must be 0

Report: the shared address, the two stacks that touched it, the synchronisation added, and a clean `-race -count=50` run with the gate now enforced in CI.
