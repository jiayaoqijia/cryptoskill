---
name: keep-container-filesystem-ephemeral
description: Use when an app silently stores state on the container's writable layer and loses it on restart. Moves any data that must survive to a volume or external service and treats the container layer as disposable.
---

# Keep the Container Filesystem Ephemeral

The writable layer belongs to the container instance: recreating the container (a deploy, a reschedule, an image update) discards it. Data written there looks persistent during a normal `docker restart` and vanishes on `docker rm` or pod rescheduling, which is how "it worked for weeks then lost everything" happens.

## Procedure

1. Inventory what the app writes outside its declared mounts. Run a fresh container, exercise it, then diff:
   `docker diff <container>` lists `A`/`C` changes in the writable layer — those are unmanaged state.
2. For anything under those paths that must persist, mount a volume or claim at that exact path:
   - Docker: `-v appdata:/var/lib/app`.
   - Kubernetes: a `PersistentVolumeClaim` mounted at `/var/lib/app`, backed by a real `StorageClass`.
3. For a single-pod stateful workload use a `StatefulSet` so the PVC and the pod identity survive reschedules, plus a `volumeClaimTemplates` block rather than a bare `Deployment` with a shared PVC.
4. For data that only needs to survive within a pod's life (caches, temp), use `emptyDir` and accept it is lost on restart — that is the correct choice when it truly is regenerable.
5. For state that must survive the whole cluster, prefer an external service (object store, managed DB) over a volume; a volume binds the pod to a node/zone.
6. Set the PVC access mode deliberately: `ReadWriteOnce` is per-node; `ReadWriteMany` needs a filesystem that supports it (NFS, CephFS), not the common `ebs`/`pd` classes.
7. Test the restart, do not assume: write a marker, recreate the container, read it back.

## Pitfalls

- `docker restart` preserves the writable layer, so a restart test falsely "proves" persistence; only `docker rm`/pod recreation exposes the loss. Recreate, do not restart.
- A bind mount from the host (`-v /host/data:/app/data`) persists on one node but the same path on another node is a different directory — an implicit node affinity that breaks on reschedule.
- A `Deployment` with one shared PVC across replicas makes every replica write the same files; use a `StatefulSet`.
- Logs written to a file on the layer fill the node's disk and are lost on restart; log to stdout instead.
- SQLite or LevelDB on a network filesystem has locking that is unreliable over NFS; keep embedded DBs on a real block volume or use a client/server DB.
- `emptyDir` with a `sizeLimit` that the app exceeds evicts the pod; an unbounded `emptyDir` on the node's disk can fill it.
- Migrating from an external service to a volume later requires a backfill; choose the persistence boundary before launch, not after.

## Verification

    docker run -d -v appdata:/data --name a app:x
    docker exec a sh -c 'echo marker > /data/probe'
    docker rm -f a
    docker run --rm -v appdata:/data app:x cat /data/probe   # marker

The marker survives full container recreation, and `docker diff` on a running instance shows nothing outside declared mounts. Report the paths that were relocated to volumes.
