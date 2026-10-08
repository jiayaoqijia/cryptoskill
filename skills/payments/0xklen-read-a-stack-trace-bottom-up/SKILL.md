---
name: read-a-stack-trace-bottom-up
description: Use when a crash prints a traceback or exception dump. Reads it in the order the machine produced it and extracts the first frame in your code, avoiding misdirection by the wrapper.
---

# Read a Stack Trace Bottom-Up

Traces are printed top-down but executed bottom-up. Reading only the loud final line sends you to the wrong file; the first frame in your own code is where the trail starts.

## Procedure

1. Locate the exception type and message on the last line — that is the *symptom*, not the location.
2. Scan for the deepest frame inside your own source (`src/`, your package name). That frame is where execution entered code you control.
3. Read `most recent call last` in Python or top-of-list in Java: execution flowed from the outer entry point *down* to the throw site. Reconstruct the call chain in that direction.
4. Take the first *your-code* frame and the frame below it — the caller passing the bad argument or the callee returning the bad value is usually the real defect.
5. If a framework wrapper dominates the trace, enable the inner trace: `RUST_BACKTRACE=full`, `NODE_OPTIONS=--stack-trace-limit=100`, or `PYTHONFAULTHANDLER=1` for a C-level crash.
6. For a `KeyError`/`NullPointerException`/segfault, go to the frame and print the *actual* runtime value at that line before editing anything.
7. Note the exact exception class — `KeyError` vs `AttributeError` names a different bug — and search the codebase for where it can be raised.
8. If the trace is truncated ("... 20 frames hidden"), raise the limit rather than guessing the omitted frames.

## Pitfalls

- Fixing the line the message points at when it is a `raise`/`unwrap` that merely reports a value computed upstream.
- Reading the last frame (the throw site) as the cause when it is the detection point.
- Ignoring a `Caused by:` chain in Java and fixing the outer exception's symptom.
- Treating a framework's generic 500 handler frame as product code.
- Trusting a minified JS stack without a source map; add `--enable-source-maps` or use the map.
- Assuming frames are in your language when a native frame is interleaved (`<native>` / `??`).

## Verification

    python3 -c "import traceback,sys; ..." 2>&1 | awk '/src\//{print; exit}'
    # prints the first application frame; visit that file:line and inspect the value there

    node --enable-source-maps app.js 2>&1 | grep -n 'at ' | head -3
    # passes when frames name your source files and line numbers, not bundle offsets

Report to the user: the exception class, the first frame in your code, and the value found at that line.
