---
name: eliminate-n-plus-one-queries
description: Use when a list endpoint issues one query per row and latency scales with page size — detect the loop, replace it with a set-based fetch, and pin the query count in a test.
---

# Eliminate N+1 queries

An endpoint that runs one query per item turns a 50-item page into 51 round trips. The fix always has the same shape: fetch the set once and join it in SQL or in memory. Then pin the count with a test so it cannot creep back.

## Procedure

1. Count queries per request before changing anything. Django: accumulate `django.db.connection.queries`; SQLAlchemy: listen on `before_cursor_execute`; Rails: the `bullet` gem.
2. Confirm the scaling signature: request the same endpoint with `?limit=10` and `?limit=100`. If query count grows roughly 10x, it is N+1.
3. Find the loop — any iteration that dereferences a lazy relation:
```bash
grep -rn "for .* in .*:" src/api/ | grep -iE "\.(all|filter|find|get)\("
```
4. Replace with a set-based load, or a single join:
```python
ids = {o.customer_id for o in orders}
by_id = Customer.objects.in_bulk(ids)      # one query
for o in orders:
    o.customer = by_id[o.customer_id]
```
5. Choose the ORM tool by relation shape: `select_related` / `includes` (a JOIN) for many-to-one, `prefetch_related` / `selectinload` (a second `IN` query) for one-to-many to avoid row multiplication.
6. For nested serializers or GraphQL, use a dataloader that batches per tick and dedupes keys so duplicate parents share one load.
7. Pin the whole request's count in a regression test:
```python
def test_list_orders_query_count(django_assert_num_queries):
    with django_assert_num_queries(2):
        client.get("/orders/?limit=50")
```

## Pitfalls

- Fixing one loop and leaving three; assert the count for the entire request, not for one query.
- `prefetch_related` on an unbounded relation loads every child — paginate the child set too.
- A dataloader that batches but does not dedupe keys re-runs for duplicate parents.
- Caching the child per-request hides N+1 from the test while the first request still pays for it.
- An eager `select_related` over a nullable FK emits a LEFT JOIN the planner cannot drive an index from on large tables.
- Counting queries in a test against an empty database, where the loop never executes.

## Verification

    pytest tests/test_query_counts.py -q
    # pass: one test per list endpoint with a fixed expected count,
    # and the count is identical at limit=10 and limit=100

Report the observed query count at two page sizes, the fetch strategy used, and the pinned count in the regression test.
