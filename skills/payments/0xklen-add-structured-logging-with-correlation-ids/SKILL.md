---
name: add-structured-logging-with-correlation-ids
description: Use when logs are unsearchable during an incident — converts free-text output to JSON carrying a trace_id, request_id, service and level on every line.
---

# Structured logging with correlation IDs

Free-text logs fail exactly when you need them: at 3 a.m., searching for the one request that failed. Emit JSON with stable keys and carry a `trace_id` from the edge so a single search reconstructs the whole request across services.

## Procedure

1. Pick one encoder per language and use it everywhere: Python `structlog` with `JSONRenderer`; Go `slog.NewJSONHandler(os.Stdout, nil)`; Node `pino`. Never mix `print` and the logger in the same process.

2. Emit these required keys on every record: `ts` (RFC3339 with ms), `level`, `service`, `version`, `trace_id`, `span_id`, `request_id`, `msg`, `event`. Domain data goes in top-level keys, never interpolated into `msg`.

3. Configure base context once at process start:
       structlog.configure(processors=[structlog.contextvars.merge_contextvars,
           structlog.processors.add_log_level,
           structlog.processors.TimeStamper(fmt="iso"),
           structlog.processors.JSONRenderer()])
       structlog.contextvars.bind_contextvars(service="checkout", version=os.getenv("GIT_SHA"))

4. Bind the request id in the outermost middleware and clear it on exit so a pooled worker does not leak it into the next request:
       token = structlog.contextvars.bind_contextvars(request_id=headers.get("x-request-id") or uuid4().hex)
       try: ... finally: structlog.contextvars.unbind_contextvars("request_id")

5. Treat levels as a budget: DEBUG off in prod, INFO for state changes (order placed, deploy), WARN for handled-but-unexpected (retry succeeded on attempt 3), ERROR only for conditions that page a human. If an ERROR line maps to no alert, demote it.

6. Never log secrets or PII: no `Authorization`, cookie, `password`, card numbers, full emails. Enforce with a pre-commit regex over message templates.

7. Log to stdout only; the platform collects and rotates. Do not open file handles inside a container.

8. Sample high-volume debug deterministically on request id (`if hash(req_id) % 100 == 0`) and always emit full records for errors.

## Pitfalls

- Stack traces stringified into `msg`: the exception class, message and frames become unsearchable. Put `error.type`, `error.message` and `stack` in separate keys.
- Binding context vars outside request scope in a thread/goroutine pool, so the next request inherits the previous `request_id`.
- Different key names per service (`user_id`, `userId`, `uid`), making a cross-service join impossible.
- Logging the whole request body and leaking a bearer token into the log store.

## Verification

    rg -o '"trace_id":"[0-9a-f]+"' app.log | sort -u | wc -l    # equals distinct request count
    python -c 'import json;[json.loads(l) for l in open("app.log")]'   # every line parses

Report: N lines all parse as JSON, `jq -e 'has("trace_id")'` is true for 100% of records, and one `trace_id` search returns the full path across services.
