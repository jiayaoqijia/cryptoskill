---
name: cache-embeddings-by-content-hash
description: Use when re-ingesting a corpus re-pays to embed unchanged text. Keys an on-disk embedding cache by model, text hash and preprocessing so unchanged chunks are never re-embedded.
---

# Cache Embeddings by Content Hash

Embedding is the slowest and most expensive part of ingest, and most of a corpus does not change between runs. Cache vectors keyed by everything that affects the vector, so an unchanged chunk costs a dict lookup.

## Procedure

1. Build the cache key from every input that changes the vector: `sha256(model_id + "\x00" + preprocessing_version + "\x00" + text)`.
2. Store the cache as a local store keyed by that hash — SQLite (`embeddings.db`, table `key TEXT PRIMARY KEY, vec BLOB`) or a parquet file.
3. On ingest, look up the key first; only embed misses, then write them back.
4. Include the preprocessing version, so changing the heading-prefix rule invalidates the cache.
5. Include the query-side rewrite in the key only if you cache query embeddings; document and query keys are separate namespaces.
6. Shard or batch the misses (32-256 per call) to use the GPU and reduce per-call overhead.
7. Report the hit rate per ingest; a low hit rate on a mostly-unchanged corpus means the key includes something volatile (a timestamp).
8. Never key on list position or filename alone — a renamed file with identical text is a hit.
9. Back the cache with the same discipline as the index: it is derived, regenerable, and safe to delete.
10. Evict by LRU or by source, but never evict an entry whose chunks are still live and unique, or the next ingest re-pays for it.

11. Store the cache read/write wrapper as one function so no ingest path can bypass it.

## Pitfalls

- Keying on the text only, so a model upgrade reuses vectors from the old model and corrupts the index.
- Letting the key include a timestamp or run id, giving a 0% hit rate that looks like a working cache.
- Storing floats as text, which bloats the cache tenfold and slows load past the embedding it saves.
- Caching query embeddings and document embeddings under the same key space.
- Deleting the cache to "clean up" and forcing a full re-embed on the next run.
- Ignoring the cache on the write path but reading it on the read path, so the two disagree.

- A parallel ingest writing the same key from two workers and racing on the last write.
- Reusing a cache built for one normalisation setting after the normalisation changes.

## Verification

    sqlite3 embeddings.db "select count(*) from embeddings;"
    python3 ingest.py --cache embeddings.db --report   # prints hits, misses, hit rate
    # passes when a second ingest of unchanged docs shows >95% hit rate and identical vectors

Report to the user: embedding calls saved, hit rate, and the model/preprocessing version the cache is bound to.
