# Sentry Tracing

- **Unbounded background trace volume**: For unlock, polling, reconnect or fan-out instrumentation, estimate added spans at normal and retry load. Record sampling/deduplication and expected baseline impact before enabling the trace. Reuse an existing trace when it already measures the work.

Every async flow that affects perceived performance carries a named Sentry trace from the trace reference (mobile `docs/perps/perps-sentry-reference.md`); no ad hoc trace names or missing end calls.

- **New screen without `usePerpsMeasurement`** — every new view needs a Sentry performance trace with appropriate `conditions` for when data is loaded.
- **Missing error context** — `Logger.error()` calls without `{ feature: 'perps', context: 'ClassName.method', provider, network }`. Sentry filtering depends on these fields.
- **Missing `ensureError()` wrapper** — catching errors without `ensureError(error)` before passing to `Logger.error()`. Non-Error objects crash Sentry reporting.
- **New trace without TraceName enum** — hardcoded trace name strings instead of adding to `TraceName` enum in `app/util/trace.ts`.
- **Missing `endTrace` in finally block** — `trace()` started but `endTrace()` not in a `finally` block. Orphaned traces leak in Sentry.
