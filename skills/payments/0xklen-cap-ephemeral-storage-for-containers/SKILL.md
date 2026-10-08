---
name: cap-ephemeral-storage-for-containers
description: Use when a container filling local disk evicts its pod or its node. Sets ephemeral-storage requests and limits plus log rotation so a runaway writer is stopped before it takes the node down.
---

# Cap Ephemeral Storage for a Container

Local disk is a shared, finite node resource. A container that writes unbounded files to its writable layer, `emptyDir` or `/var/log` exhausts the node's disk, and the kubelet evicts pods (`DiskPressure`) or the node falls over. A storage limit plus rotation turns that into one evicted pod.

## Procedure

1. Measure real usage: `kubectl exec <pod> -- du -sh /tmp /var/log /data 2>/dev/null` and `kubectl describe node <n> | grep -A5 'Allocated resources'` for ephemeral-storage.
2. Set requests and limits on ephemeral storage, defined as writable layer + `emptyDir` + container logs:
   ```yaml
   resources:
     requests: { ephemeral-storage: "1Gi" }
     limits:   { ephemeral-storage: "2Gi" }
   ```
3. Bound each `emptyDir` explicitly so one mount cannot eat the limit:
   `emptyDir: { sizeLimit: 500Mi }` — exceeding it evicts the pod instead of the node.
4. Cap container logs at the runtime level so they count against a known budget:
   Docker `--log-opt max-size=10m --log-opt max-file=5`; containerd `max_container_log_line_size` and a log rotation config.
5. Move genuinely large or long-lived data off the node: an object store or a PVC with a `StorageClass`, so ephemeral storage stays for scratch.
6. Alert before the limit: on `kubelet_evictions` with reason `EphemeralStorage` and on node filesystem usage > 85%.
7. For a `tmpfs` `/tmp`, remember tmpfs counts against memory, not ephemeral storage — set both.

## Pitfalls

- Ephemeral-storage accounting includes container logs; a chatty app can hit the limit with almost no app writes, so fix log rotation first.
- The kubelet's `imagefs`/`nodefs` thresholds can evict on the node's `/var/lib/kubelet`, not only your container's limit; a neighbour filling disk still evicts you.
- `emptyDir` with no `sizeLimit` and no container limit is unbounded: the first pod to fill the node takes everyone down.
- A writable layer write is not visible as a `du` inside the container's mounts — `docker diff` and the node's overlay dir are where it shows.
- Eviction under `DiskPressure` ignores limits and evicts the lowest-priority pods first; set `priorityClassName` so critical pods survive.
- `ephemeral-storage` requests below actual usage cause `FailedScheduling` on nodes that could fit, or eviction when the accounting overshoots.
- Deleting a large file inside a container frees nothing until the process closes the descriptor; a deleted-but-open log keeps counting.

## Verification

    kubectl get pod <p> -o jsonpath='{.status.containerStatuses[0].restartCount}'
    kubectl get events --field-selector reason=Evicted | grep EphemeralStorage

Under a write-flood test, only the offending pod is evicted (reason `EphemeralStorage`), the node stays healthy, and other pods show no restart. Report the limit versus observed peak and the eviction reason.
