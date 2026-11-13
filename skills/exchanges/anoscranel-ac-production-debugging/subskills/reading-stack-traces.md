---
name: reading-stack-traces
domain: software-engineering/reading-stack-traces
trigger: "Reading a stack trace from a language or runtime you did not write."
anti_trigger: "Not for symbolizing or opening core dumps (that is symbols-and-coredumps)."
scope: "What a trace actually says: frames, inlining, async frames, and the top of the stack."
status: seedling
---

# Reading stack traces

## Standard

A stack trace is a list of frames, newest first, and most of it is not yours. The habit that makes traces readable is starting from the top: the topmost application frame is where the failure met your code, and everything below it is the path the call took to get there. Library frames, runtime frames, and framework dispatch loops are context, not suspects.

Two distortions complicate the plain reading. Optimising compilers inline functions, so one source-level frame may be missing or merged, and the line number can be off by the size of the inlined body. Asynchronous runtimes do not keep a call stack across an await or a callback hop, so a trace taken at the moment of failure shows the scheduler, not the logical path that scheduled the work. Both distortions mean the trace is evidence about the machine state, and reconstructing the logical path is separate work.

## Decision rules

- Read the topmost frames first; identify the first frame in code you own.
- Classify the exception or signal before reading further: its type narrows the search.
- Note inlined or missing frames rather than trusting line numbers blindly.
- For async traces, look for the logical continuation in the log or trace ID, not the native stack.
- Record the runtime version and binary build alongside the trace; symbols are only valid for that build.
- Compare against a healthy trace from the same build if one exists.

## Procedure

1. Capture the trace verbatim with timestamps and thread identity.
2. Classify the failure type from the top frame.
3. Locate the first application-owned frame.
4. Note inlining or async gaps that break the apparent chain.
5. Match the binary build to the available symbols.
6. Write the reading: what the trace shows, and what it does not.

## Anti-patterns

- Reading from the bottom of the stack upward.
- Treating a framework dispatch frame as the cause.
- Trusting line numbers from an optimised build without question.
- Expecting an async trace to show the logical path.
- Copying a trace into a ticket without the build identifier.

## Done checklist

- [ ] Trace captured with build and runtime identifiers.
- [ ] Failure type classified.
- [ ] First owned frame identified.
- [ ] Inlining and async gaps noted.
- [ ] Symbols matched to the build.
- [ ] Written reading states what the trace does not show.

## Sources

- Error and exception semantics across runtimes: <https://docs.oracle.com/en/java/javase/21/>
- Python tracebacks and their reading: <https://docs.python.org/3/library/traceback.html>
- Chrome DevTools and async stack traces: <https://developer.chrome.com/docs/devtools>
