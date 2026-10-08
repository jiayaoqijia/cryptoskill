---
name: tune-http-keep-alive-and-connection-pools
description: Use when throughput is capped by connection setup, or upstreams see too many idle connections in TIME_WAIT. Size keep-alive timeouts and client pool limits to the traffic pattern instead of leaving library defaults.
---

# Tune HTTP keep-alive and connection pools

Every new connection pays a TCP (and TLS) handshake. Reuse makes that free — until a server closes
idle keep-alives first and clients race to reconnect, or the pool is too small and requests queue for
a slot.

## Procedure

1. Check whether connections are actually being reused. On the server, count accept vs request rate:
   ```bash
   # connections accepted per second, from your web server metrics
   rate(nginx_connections_accepted[5m])   # should be far below request rate
   ```
2. Confirm the client is pooling. In Python, `requests` pools per `Session`, not per call:
   ```python
   import requests
   s = requests.Session()
   s.mount("https://", requests.adapters.HTTPAdapter(pool_connections=50, pool_maxsize=50))
   ```
   A new `requests.get()` per call opens a new connection every time.
3. Align timeouts so the client keeps the connection slightly *shorter* than the server, avoiding a
   race to use a connection the server just closed:
   ```nginx
   keepalive_timeout 65s;       # server side
   ```
   ```python
   adapter = requests.adapters.HTTPAdapter(pool_maxsize=50, max_retries=0)
   # client idle timeout ~55s, below the server's 65s
   ```
4. Size the pool to expected concurrency, not to total traffic. A pool of 50 sustains ~50 in-flight
   requests; more just queues:
   ```bash
   # in-flight requests ≈ arrival_rate × latency  (Little's Law)
   # 200 req/s × 0.05 s = 10 → pool of ~20 gives 2× headroom
   ```
5. Watch for ephemeral port exhaustion from churn — lots of TIME_WAIT to one destination:
   ```bash
   ss -tan state time-wait | grep ':443' | wc -l
   ```
6. For upstream proxies, enable upstream keep-alive so the proxy reuses backend connections too:
   ```nginx
   upstream app { server 10.0.1.5:8080; keepalive 32; }
   ```

## Pitfalls

- A new connection per request defeats pooling and burns ephemeral ports; a module-level `Session` is required.
- Server `keepalive_timeout` shorter than the client's idle assumption causes intermittent `Connection reset by peer`.
- Pool size below concurrency queues requests and looks like latency, not like an error.
- Pool size far above concurrency wastes upstream file descriptors and memory for no gain.
- A load balancer's idle timeout between client and server must be the shortest of the three, or one side reuses a dead connection.
- HTTP/1.1 `Connection: close` from one upstream response can disable reuse for the whole connection.
- TIME_WAIT is normal at modest counts; thousands to one host signals churn you should fix, not tune away.

## Verification

    ss -tan state time-wait | grep ':443' | wc -l
    rate(nginx_connections_accepted[5m])   # accepted << requests handled

Pass means accepted-connection rate stays well under request rate and TIME_WAIT counts are flat.
Report: "pool 50, client idle 55 s < server 65 s; accepted conns dropped 12k/min → 200/min."
