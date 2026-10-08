---
name: handle-sigterm-for-graceful-shutdown
description: Use when a container is killed after 10 seconds with in-flight requests dropped. Makes PID 1 forward SIGTERM to the app and the app stop accepting, finish, and exit inside the termination grace period.
---

# Handle SIGTERM for Graceful Shutdown

When a container is stopped, the runtime sends SIGTERM to PID 1 and after a grace period sends SIGKILL. If PID 1 is a shell that ignores or swallows the signal, or the app has no drain, requests in flight are cut and clients see connection resets during every deploy.

## Procedure

1. Make the app PID 1 with the exec form so it receives signals directly:
   `ENTRYPOINT ["node", "server.js"]` — not `CMD node server.js` through a shell, which does not forward SIGTERM to the child.
2. If a shell is unavoidable, use `exec`: `CMD ["sh", "-c", "exec node server.js"]`, or supervise with `tini` / `docker run --init`.
3. In the app, on SIGTERM: stop accepting new connections, let in-flight ones finish with a deadline, then exit 0.
   ```js
   process.on('SIGTERM', () => {
     server.close(() => process.exit(0));
     setTimeout(() => process.exit(1), 25000).unref();
   });
   ```
4. Set the grace period longer than the drain deadline but shorter than what callers tolerate:
   Kubernetes `terminationGracePeriodSeconds: 30`; Docker `docker stop -t 30`.
5. Remove the endpoint before draining so new traffic stops first. In Kubernetes the pod is marked terminating and removed from Service endpoints before SIGTERM for pods that are Ready; for slow drains add a `preStop` sleep so kube-proxy rules propagate:
   `preStop: { exec: { command: ["sh","-c","sleep 5"] } }`.
6. Keep-alive connections can hold the socket open after you stop accepting; close idle keep-alive connections explicitly or set a keep-alive timeout below the grace period.
7. Verify the exit code is 0 on a clean drain and that no request is dropped during a rolling restart.

## Pitfalls

- `CMD node server.js` runs via `/bin/sh -c`, so PID 1 is the shell and the SIGTERM is never delivered; the container is SIGKILLed after the grace period and every in-flight request dies.
- `terminationGracePeriodSeconds: 30` with a drain deadline of 60s guarantees a SIGKILL mid-drain; keep the deadline below the grace period.
- Graceful shutdown that waits for a connection pool to drain can hang past the grace period; always cap with a hard `setTimeout(... process.exit(1))`.
- A `preStop` sleep adds latency to every termination and does not help if the app is already not reading from its socket.
- A load balancer with a longer keep-alive than the drain window keeps sending to a closing socket; align the proxy idle timeout below the grace period.
- Long-lived streaming or WebSocket connections never finish on their own; close them explicitly after notifying the client.
- Exit 0 hides a drain that timed out — log when the forced-exit path is taken so it is visible.

## Verification

    docker run -d --name x app:x && docker stop -t 30 x
    docker inspect -f '{{.State.ExitCode}}' x      # 0
    docker logs x | grep -i 'shutdown complete'

A slow request issued during `docker stop` completes, the exit code is 0, and shutdown logs show the drain path. Report the exit code and whether any request was dropped.
