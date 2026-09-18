# Flexible HTTPS Outcalls

`flexible_http_request` is a separate management canister method in which a committee of nodes each
make the request and the canister receives their **individual** responses, instead of one the subnet
reached consensus on. Reconciling them is the canister's job.

Use it when the data changes faster than the nodes could ever agree on it, so replicated mode would
fail consensus. The tradeoff is cost against trust: a committee of three costs less than one of 13
and is correspondingly easier for a single node to skew.

**Rust only.** Requires `ic-cdk-management-canister >= 0.2.0` and `ic-cdk >= 0.20.3`. The Motoko
`ic` package has no equivalent, which needs a `moc` carrying the `subnetSelfNodeCount` primitive.
Always priced with version 2; there is no `pricing_version` field.

## Replication counts

```rust
pub struct ReplicationCounts {
    pub min_responses: u32,   // the fewest a successful outcall may carry; decides when it returns
    pub max_responses: u32,   // the most the caller will accept
    pub total_requests: u32,  // how many nodes issue the request
}
```

The caller must ensure `0 <= min_responses <= max_responses <= total_requests` and
`1 <= total_requests <= N`, where `N` is the subnet size. **Do not hardcode `total_requests`**: a
value above `N` is invalid, and `N` differs per subnet (13 or 34 on mainnet, and a local replica
reports 13). Derive it:

```rust
use ic_cdk::api::subnet_self_node_count;

let total_requests = subnet_self_node_count().min(5);
let min_responses = total_requests / 2 + 1;   // a strict majority of the committee
```

There is no Motoko equivalent of `subnet_self_node_count` until a `moc` exposing the
`subnetSelfNodeCount` primitive ships.

Leaving `replication` unset uses the endpoint's own defaults: `floor(2 * N / 3) + 1` for
`min_responses`, and `N` for both `max_responses` and `total_requests`.

## Working example

```rust
use candid::{CandidType, Nat};
use ic_cdk::api::subnet_self_node_count;
use ic_cdk_management_canister::{
    FlexibleHttpRequest, FlexibleHttpRequestResult, HttpRequestResult, ReplicationCounts,
};

#[derive(CandidType)]
struct Tally { value: String, count: u32 }

#[ic_cdk::update]
async fn fetch_server_time() -> Result<Vec<Tally>, String> {
    let total_requests = subnet_self_node_count().min(5);
    let min_responses = total_requests / 2 + 1;

    // No transform, which also means nothing is reserved for running one. The
    // response is a ~30-byte timestamp, so there is nothing worth stripping.
    // With bulky headers or unused JSON fields, reconsider.
    let result = FlexibleHttpRequest::new("https://postman-echo.com/time/now")
        .with_max_response_bytes(1_000)
        .with_replication(ReplicationCounts { total_requests, min_responses, max_responses: total_requests })
        .with_expected_roundtrip_time_ms(10_000)
        .send()
        .await
        .map_err(|err| format!("Outcall failed: {err}"))?;

    match result {
        // Any count between min_responses and max_responses is a normal success.
        FlexibleHttpRequestResult::Ok(responses) => Ok(reconcile(&responses)),
        FlexibleHttpRequestResult::Err(err) => Err(format!(
            "Fewer than {min_responses} responses: {:?}, {}",
            err.global_error, err.message
        )),
    }
}

// Each response carries its own status, because no node had to agree with any
// other. Tally the distinct bodies, most common first.
fn reconcile(responses: &[HttpRequestResult]) -> Vec<Tally> {
    let mut tally: Vec<Tally> = Vec::new();
    for r in responses.iter().filter(|r| r.status == Nat::from(200u32)) {
        let value = String::from_utf8_lossy(&r.body).to_string();
        match tally.iter_mut().find(|t| t.value == value) {
            Some(e) => e.count += 1,
            None => tally.push(Tally { value, count: 1 }),
        }
    }
    tally.sort_by(|a, b| b.count.cmp(&a.count));
    tally
}
```

## Handling the result

`FlexibleHttpRequestResult` is `Ok(Vec<HttpRequestResult>)` or `Err(FlexibleHttpRequestErr)`.
**Both arms are delivered as a reply, not a reject.** Only failures detected before the requests go
out, such as invalid arguments or too few attached cycles for the base fee, arrive as rejects.

Rules for the success arm:

- Handle **any** count between `min_responses` and `max_responses`. Fewer than `max_responses` is a
  normal success, not a degraded one.
- The responses do not identify which node produced them, and their order is unspecified. Treat them
  as an unordered multiset.
- Check each response's `status` separately. No node had to agree with any other, so one can be a
  500 while the rest are 200.
- Pick a reconciliation rule a minority of nodes cannot skew. A majority tally is the usual choice;
  taking the first response defeats the point of asking several.

The error arm carries `global_error`, `node_details` and `message`. `global_error` is one of:

| Value | Meaning |
|---|---|
| `timeout` | Fewer than `min_responses` collected before a system timeout |
| `out_of_cycles` | What the nodes left unspent no longer covers delivering any result still possible |
| `responses_too_large` | No combination of at least `min_responses` responses fits the total limit |
| `too_many_rejects` | More than `total_requests - min_responses` nodes rejected, so `min_responses` successes are now unreachable |

`node_details` reports what individual nodes did, each with a `report` of resources used and an
optional `error` whose `code` is a diagnostic string, **not** a fixed enumeration. Do not branch on
it. Every field of the report is optional and an implementation may leave the whole report empty, so
do not rely on it to diagnose a failure. Which nodes appear depends on the error: `timeout` carries
none, `too_many_rejects` lists the rejecting nodes, and `responses_too_large` and `out_of_cycles`
list every node whose response the system had.

## Reconciling the responses

This is the obligation flexible mode transfers to your canister, and it is a security decision, not
a formatting one. The subnet does not validate the responses against each other: a faulty or
malicious node can return whatever it likes, and you will receive it alongside the honest ones. With
the default counts, `min_responses` is `floor(2 * N / 3) + 1`, so up to a third of the committee can
be wrong and the call still succeeds.

Pick a rule that a minority cannot skew, and that works for **any** count in
`[min_responses, max_responses]`.

| Data shape | Rule | Why |
|---|---|---|
| A number (price, rate, count) | **median** | A minority of outliers cannot move it. A *mean* can be dragged arbitrarily by one node. |
| A discrete value (status, id, enum, a normalised body) | **majority / mode** | Needs the responses normalised first, or per-node noise makes every one distinct. |
| A set or list | **intersection**, or items present in a majority of responses | Union lets one node inject entries. |
| Something you only need once, integrity not required | none: use **non-replicated** instead | Cheaper, and a committee buys nothing if you are going to trust the first answer. |

Three ways to get it wrong:

- **Taking `responses[0]`.** The order is unspecified, so this is trusting an arbitrary node while
  paying for a committee.
- **Requiring unanimity, or requiring `max_responses` responses.** Fewer than `max_responses` is a
  normal success, so a rule that needs all of them will fail routinely.
- **Averaging.** One node reporting `1e30` destroys a mean. Use the median.

If no rule is satisfied (no majority, too few responses to be meaningful), treat it as a failure and
return an error rather than picking a response to proceed with. The point of asking several nodes is
to be able to detect exactly that case.

## Two size limits, not one

`max_response_bytes` bounds **each node's own** response, at up to 2MB = `2_000_000` bytes (decimal).

Separately, the responses delivered **together** must fit **2 MiB = `2_097_152` bytes** in total,
measured on the combined encoded size after the transform. When they do not all fit, fewer are
returned, down to `min_responses`. The call fails with `responses_too_large` only when even the
smallest `min_responses` responses exceed the limit together.

So a committee of 13 with `max_response_bytes = 1_000_000` cannot deliver 13 responses: budget the
per-node cap against the combined limit divided by `min_responses`.

The builder already knows this: for a flexible call, the default `transformed_response_bytes`
expectation is capped at the block budget divided by `min_responses`, rounded up, rather than at
`max_response_bytes + 1_024`. Responses larger than that average could not be delivered together
anyway, so reserving for them would only withhold cycles. Declaring
`with_expected_transformed_response_bytes` from what your transform actually emits still helps when
it emits far less than that cap, which is the usual case for an extract.

## Testing locally

Flexible outcalls run on the local replica, which reports a node count of 13, so the committee
arithmetic behaves as on mainnet. But every response comes from the same single node, so they are
all identical: a local run exercises the call and the shape of your reconciliation code without ever
producing the disagreement that reconciliation exists for. Cover the disagreeing case with unit
tests on `reconcile` itself.

## Whether to set a transform, with the arithmetic

A transform is optional here, as in non-replicated mode, because each node's own response is
delivered and nothing is reconciled by consensus. Whether it pays for itself is arithmetic, and the
two sides are much further apart than they look.

**No transform reserves nothing for one.** `transform_instructions` defaults to 0 when there is no
transform, rather than to the query limit. That is the cheapest configuration available.

**Adding one defaults that term to the full query instruction limit**, which dominates the
reservation for any small request: it is the largest single term by a wide margin. If you add a
transform you must declare `with_expected_transform_instructions`, sized to what the transform
actually does.

**What a transform buys back** is the delivery fee, charged per delivered byte on the size *after*
the transform. A delivered byte costs far more than a transform instruction, so stripping bytes wins
comfortably once there are bytes worth stripping.

Charge and reservation behave differently here, and conflating them is easy. The **charge** is
linear in the bytes delivered with no lower bound, so every byte you strip is money saved. The
**reservation** floors that term at about 1 KB, so shrinking an already-small response does not hold
fewer cycles. What decides it is therefore how many bytes there are to remove, not whether the
result lands under the floor.

| How much a transform would strip | Verdict |
|---|---|
| Little: the response is mostly payload already | **Skip it.** Small saving on the bill, no saving on the reservation, and you would add the instruction term. |
| A lot: bulky headers, or JSON fields you do not need | **Add it, and declare the instruction expectation.** The per-byte delivery saving is the dominant term. |
| A lot, expectation not declared | **Worst of both.** The full query-limit reserve dwarfs any delivery saving. |

Confirm with `get_cost()` on both shapes rather than trusting the rule of thumb. Note that
`get_cost()` shows you the *reservation*, where the floor applies, so it understates what a
transform saves on a small response.

Two reasons that are not about cycles at all, and can decide it on their own:

- **It gets you more responses.** The combined 2 MiB limit is measured after the transform, so
  smaller responses mean fewer get dropped and the count stays nearer `max_responses` instead of
  being trimmed toward `min_responses`.
- **It makes reconciliation possible.** Tallying raw responses is defeated by per-node noise: a
  `Date` header or an echoed caller IP makes every response distinct, so a majority vote finds no
  majority.
