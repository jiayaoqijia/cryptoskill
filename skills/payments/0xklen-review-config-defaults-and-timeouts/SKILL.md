---
name: review-config-defaults-and-timeouts
description: Use when a diff adds a timeout, retry count, limit, or config default. Checks the new value is safe when the operator never sets it and cannot cause an infinite loop or a silent cap.
---

# Review config defaults and timeouts

Defaults run in production before anyone reads the docs. A wrong default ships as production behaviour for every caller who never overrides it.

## Procedure

1. List new or changed configuration: `gh pr diff 482 | grep -nE '^\+.*(timeout|retry|retries|max_|limit|backoff|deadline|ttl)\s*[:=]'`.
2. For each, ask what happens when no one sets it. The default must be safe, not merely convenient: a zero timeout means never time out; an unset retry count often means the client default, which may be huge.
3. Check timeouts exist where a network call is added. An HTTP client with no timeout hangs a worker until the OS gives up — minutes, and it holds a connection the whole time.
4. Check the numbers are internally consistent: `max_retries=5` with `backoff=1s` and no jitter is a 31-second worst case per request; multiplied by concurrency it becomes a retry storm.
5. Verify limits have a stated unit and a comment: is `120` seconds or milliseconds? Ambiguous units are the most common config bug.
6. Confirm the value is overridable by environment for the deploy, not baked into source: `int(os.environ.get("TIMEOUT_MS", "3000"))`.
7. Check the config is validated at startup — a typo like `timout` silently falls back and the intended value never applies.

## Pitfalls

- A default of `0` for a "no limit" field, which the code reads as "expire immediately".
- A new retry loop on top of a client that already retries, squaring the attempts.
- A per-request timeout larger than the load balancer's, so the client waits past the point the connection is dead.
- A pagination `limit` default raised to fetch everything, turning a paginated endpoint into a full-table scan.

## Verification

    gh pr diff 482 | grep -nE '^\+.*(timeout|retry|deadline|ttl)\s*[:=]'
    # Start the app with no env overrides and assert the effective values:
    python -c "import config; print(config.TIMEOUT_MS, config.MAX_RETRIES)"

Report each new default, its unit, and the behaviour when unset. Any added network call without a finite timeout is blocking.

## Worked example

A client is constructed as `httpx.Client()` with no timeout, so a hung connection blocks a worker for the implicit default on every attempt. The fix names the value and its unit:
    TIMEOUT = float(os.environ.get("HTTP_TIMEOUT_S", "3.0"))
    httpx.Client(timeout=httpx.Timeout(TIMEOUT, connect=1.0))
The startup check prints `3.0` when no environment override is set, proving the default is the one intended.
