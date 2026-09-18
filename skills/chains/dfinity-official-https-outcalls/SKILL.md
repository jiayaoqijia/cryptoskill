---
name: https-outcalls
description: "Make HTTPS requests from canisters to external web APIs. Covers replicated, non-replicated and flexible outcalls, transform functions for consensus, both cycle pricing versions (legacy and pay-as-you-go via ic0.cost_http_request_v2), response size limits, and idempotency patterns. Use when a canister needs to call an external API, fetch data from the web, make HTTP requests, choose a pricing_version, or use flexible_http_request. Do NOT use for EVM/Ethereum calls — use evm-rpc instead."
license: Apache-2.0
compatibility: "icp-cli >= 0.2.2; pricing version 2 and flexible outcalls need ic-cdk >= 0.20.3 with ic-cdk-management-canister >= 0.2.0 (Rust only)"
metadata:
  title: HTTPS Outcalls
  category: Integration
---

# HTTPS Outcalls

## What This Is

HTTPS outcalls allow canisters to make HTTP requests to external web services directly from on-chain code. In the default **replicated** mode, every node on the subnet makes the same request and all of them must agree on the response. A transform function strips non-deterministic fields (timestamps, request IDs, ordering) so that every replica sees an identical response and can reach consensus.

Two other modes avoid that agreement step: **non-replicated** (`is_replicated = false`, one node makes the request) and **flexible** (`flexible_http_request`, a committee of nodes return their individual responses). See [Outcall modes](#outcall-modes).

## Support matrix

| | Rust | Motoko |
|---|---|---|
| Package | `ic-cdk` **0.20.3+** with `ic-cdk-management-canister` **0.2+** | `ic` **4.x** (mops), which requires `core` **2.5.0+** and `moc` **1.4.0+** |
| Entry point | `HttpRequest::new(url)` builder, `.send()` | `Call.httpRequest(args)` |
| Pricing version 1 (legacy) | only by pinning `ic-cdk-management-canister` **0.1**, or calling `aaaaa-aa` directly with `ic_cdk::api::cost_http_request` | **yes**, this is what `Call.httpRequest` does |
| Pricing version 2 (pay-as-you-go) | **yes**, the builder always selects it | — (**not available**, needs an unreleased `moc`) |
| `flexible_http_request` | **yes**, `FlexibleHttpRequest::new(url)` | — (**not available**, same reason) |
| `subnet_self_node_count` | `ic_cdk::api::subnet_self_node_count()` | — (**not available**, same reason) |

Read this before writing code; what is available depends on the language and the dependency versions in the project. **Motoko code today is version 1 only**, and consistently so. The published `ic` 4.x `HttpRequestArgs` has no `pricing_version` field, Candid omits the absent optional, and the replica reads it as version 1 — which is exactly what `Call.httpRequest` funds. Nothing to work around; just do not expect version 2 economics from Motoko yet.

For Rust the right code depends on which of three worlds the project is in. `ic-cdk` 0.19 has `ic_cdk::management_canister::http_request(&args)` (version 1; the module was removed in 0.20). `ic-cdk` 0.20 with `ic-cdk-management-canister` 0.1 has `ic_cdk_management_canister::http_request(&args)` (version 1). `ic-cdk` 0.20.3+ with `ic-cdk-management-canister` 0.2 has the builders, and is **version 2 only**: 0.2.0 removed the free `http_request` and the builder hard-codes `pricing_version: Some(2)` with no opt-out, so upgrading the crate *is* the migration. Rust also needs `serde_json` for JSON parsing.

**Which version to write.** Version 1 is deprecated and version 2 is the direction, so *new* Rust code should use the 0.2 builders. But do **not** bump a project's pinned versions in order to migrate it as a side effect of an unrelated task: 0.2 is a breaking change (it deletes the free `http_request` and `HttpRequestArgs` gains a required field), so the upgrade is the caller's decision. Write correct code for the line the project is actually on, and tell them the upgrade exists.

## Canister IDs

HTTPS outcalls use the IC management canister:

| Name | Canister ID | Used For |
|------|-------------|----------|
| Management canister | `aaaaa-aa` | The `http_request` and `flexible_http_request` management call targets |

You do not deploy anything extra. The management canister is built into every subnet.

## Mistakes That Break Your Build

1. **Forgetting the transform function.** In **replicated** mode, without a transform the raw HTTP response often differs between replicas (different headers, different ordering in JSON fields, timestamps). Consensus fails and the call is rejected. ALWAYS provide one there. In **non-replicated** and **flexible** mode it is optional *for consensus*, because each node's own response is delivered. Whether to set one there is a tradeoff. **No transform reserves nothing for it** (the instruction term defaults to 0, not to the query limit), which is the cheapest configuration available. Adding one defaults that term to the full query limit, so you must also declare `with_expected_transform_instructions`. What it buys back is the delivery fee, charged per byte on the **transformed** size: every byte stripped lowers the bill, so what decides it is how much there is worth stripping (bulky headers yes, a response that is already mostly payload no). The reservation floors that term at about 1 KB, so `get_cost()` understates the saving on a small response. Two non-cycle reasons can decide it anyway: in flexible mode the combined 2 MiB budget is measured after the transform, so smaller responses mean fewer get dropped, and reconciling is impossible if per-node noise makes every response distinct.

2. **Not attaching cycles to the call.** On a normal Application subnet, HTTPS outcalls are not free — the calling canister must attach cycles to cover the cost, and attaching zero fails the call. Both Motoko and Rust have wrappers that compute and attach the required cycles automatically: in Motoko, use `await Call.httpRequest(args)` from the `ic` mops package (`import Call "mo:ic/Call"`); in Rust, use the `HttpRequest` builder's `.send()` from `ic-cdk-management-canister` 0.2. Which pricing version you get depends on the wrapper: Motoko's `Call.httpRequest` prices version 1 with `ic0.cost_http_request(request_size, max_response_bytes)`, while Rust's `HttpRequest::send()` prices version 2 with `ic0.cost_http_request_v2`. Both are cost-schedule aware, so the same wrapper attaches the correct amount on any subnet type. **Under version 2 the up-front check is against the base fee only**, so an under-sized attachment is *not* rejected at call time: the call runs with tighter per-node limits and can fail partway, after the remote server was already contacted. See `references/pricing-version-2.md`. On a **cloud engine** (`CloudEngine` subnet), that amount is always 0 by design; do not "fix" a working outcall by attaching a hardcoded non-zero fee there — see the `cloud-engine-canisters` skill.

3. **Using HTTP instead of HTTPS.** The IC only supports HTTPS outcalls. Plain HTTP URLs are rejected. The target server must have a valid TLS certificate.

4. **Sizing `max_response_bytes` against the expected body — the limit is not body-only.** The spec defines the size of an HTTP request or response as *the total number of bytes representing the names and values of HTTP headers and the HTTP body*. Response **headers count against `max_response_bytes`**, and a real API commonly sends 1–2 KB of response headers (a unique request id, `Date`, the rate-limit family, CDN headers) before a single byte of body — against a tight cap that is a large share of the budget. Size the cap for **headers + body as they arrive from the server**, then add margin. The failure mode is total: the call fails every time rather than returning a truncated response. The maximum is 2MB = `2_000_000` bytes (decimal, not 2^21), and the same headers-plus-body definition caps the **request** you send at `2_000_000` bytes.

5. **Expecting the transform function to shrink an oversized response under the cap.** The cap is enforced **twice**: once on the raw response as it arrives from the server (headers first, then the body against what remains), and again on the transform's Candid-encoded **output**, which includes serialization overhead. Stripping headers in the transform cannot rescue a raw response that already exceeded the cap, because that first check fails before the transform ever runs. It *can* keep the transform's own output under the cap — worth doing when the transform would otherwise echo the headers back and its encoded output would exceed the limit. Both checks compare against the **same** `max_response_bytes` value, which is why a raw response that only just fits can still fail after the transform: the Candid overhead is added on top. So: size `max_response_bytes` for the raw response, and keep the transform's output small; never set a tight cap on the theory that stripping headers afterwards will make an oversized response fit.

6. **Ignoring the header limits.** Independent of `max_response_bytes`, the spec caps HTTP requests and responses at **64 headers**, **8 KiB** per header name or value, and **48 KiB** for all header names and values combined. The URL must not exceed **8192** bytes. On the request side these are enforced when the replica decodes your arguments, so an over-limit request never leaves the subnet and fails with `InvalidManagementPayload` — e.g. `Deserialize error: The number of elements exceeds maximum allowed 64` — rather than with any HTTP-looking error. If you send no `user-agent` header the IC adds `user-agent: ic/1.0`, and that added header does not count toward these limits.

7. **Omitting `max_response_bytes`.** Under **version 1**, if you do not set it the system assumes the maximum (2MB) and charges cycles accordingly — roughly 20.85 billion cycles on a 13-node subnet. Under **version 2** it no longer sets the price, but it is still the default for the `raw_response_bytes` expectation, so omitting it reserves for 2MB: 34.0 billion cycles rather than 5.3 billion for a 4,000-byte cap. Either way, always set it to a reasonable upper bound for your expected response (see pitfall 4 for what counts toward it).

8. **Non-idempotent POST requests without caution.** Because multiple replicas make the same request, a POST endpoint that is not idempotent (e.g., "create order") will be called N times (once per replica, typically 13 on a 13-node subnet). Use idempotency keys, or design endpoints to handle duplicate requests, or set `is_replicated = ?false` (Rust: `.non_replicated()`), which has a single node send the request and removes the rate-limit pressure entirely — at the cost of trusting that node not to observe or modify the response.

9. **Not handling outcall failures.** External servers can be down, slow, or return errors. Always handle the error case. There are **two distinct timeouts**, and neither traps — both come back as rejects (in Motoko the `await` raises a catchable `Error`; in Rust the wrapper returns `Err`):
   - The remote server does not respond within **30 seconds**: `SysFatal`, message `Timeout expired`.
   - The subnet does not produce a response within **60 seconds**: `SysTransient`, message `Canister http request timed out`. This one is normally the retryable one; the exception is a version 2 call that is under-funded *and* missing a node's report (see `references/pricing-version-2.md`).

10. **Calling localhost or private IPs.** HTTPS outcalls can only reach public internet endpoints. Localhost, 10.x.x.x, 192.168.x.x, and other private ranges are blocked.

11. **Forgetting the `Host` header.** Some API endpoints require the `Host` header to be explicitly set. The IC does not automatically set this from the URL.

12. **Leaving the version 2 expectations unset.** Anything you do not declare is *reserved* at its maximum: a 60-second round trip, and a transform running to the full query instruction limit. For a 4,000-byte cap that is around 5.3 billion cycles held, nearly all of it the transform reserve, against about 112 million once you declare `with_expected_transform_instructions` and `with_expected_roundtrip_time_ms`. Declare those two. Leave `raw_response_bytes` alone, because the server decides it; lower `max_response_bytes` instead if the byte terms dominate. Declare `with_expected_transformed_response_bytes` when your transform bounds its own output, which is the one case where the cap cannot be the lever. The *charge* is unaffected by any of this unless the smaller budget actually cuts the call short. `references/pricing-version-2.md` has the figures, the per-resource reasoning, and the failure modes.

13. **Expecting to reach version 1 through `ic-cdk-management-canister` 0.2.** You cannot. The builder is the only path the crate offers, it hard-codes `pricing_version: Some(2)`, and there is no `with_pricing_version`. `HttpRequest::from_args` looks like the escape hatch and is not: it is the documented way to migrate an existing call site, and it **silently overwrites `pricing_version` with 2**, so args that deliberately set 1 change version when you pass them through it. To stay on version 1, pin `ic-cdk-management-canister` 0.1, or call `aaaaa-aa` directly and price with `ic_cdk::api::cost_http_request`, which is still present in 0.20.3.

14. **Setting `pricing_version` by hand and funding it with the wrong cost function.** The field and the attachment have to agree. Set `pricing_version = 2` while attaching a `cost_http_request` (version 1) amount and the call is *accepted*, because the up-front check is only the base fee — it then runs on a smaller per-node allowance than version 2 intended and can fail partway. The reverse, a version 1 call funded with a `cost_http_request_v2` amount, is rejected outright with `http_request request sent with <X> cycles, but <Y> cycles are required.`, because version 1 wants the whole `max_response_bytes` up front. Let the wrapper set both: Rust's `HttpRequest::send()` pairs version 2 with `cost_http_request_v2`, and Motoko's `Call.httpRequest` pairs version 1 with `cost_http_request`. Note also that the replica *filters* an unrecognised version to version 1 with no error, so a bogus value fails as a funding mismatch rather than as a validation error.

15. **Hardcoding `total_requests` for a flexible outcall.** `total_requests` must not exceed the subnet size, which differs per subnet (13 or 34 on mainnet). Derive it:
    ```rust
    // WRONG, even when you want five nodes: 5 may exceed the subnet size.
    let replication = ReplicationCounts { total_requests: 5, min_responses: 3, max_responses: 5 };

    // RIGHT: ask for five, but never more than the subnet has.
    let total_requests = subnet_self_node_count().min(5);
    let min_responses = total_requests / 2 + 1;
    ```

    Also handle **any** count between `min_responses` and `max_responses` in the success arm — fewer than `max_responses` is a normal success, not a degraded one — and check each response's `status` separately, because no node had to agree with any other. See `references/flexible-outcalls.md`.

## Outcall modes

Replicated and non-replicated are selected by `is_replicated`; flexible is a separate method.

| | Replicated (default) | Non-replicated (`is_replicated = false`) | Flexible (`flexible_http_request`) |
|---|---|---|---|
| Who sends it | All N nodes | One node chosen by the system | A committee of `total_requests` nodes |
| What you get | One agreed response | That node's response | Between `min_responses` and `max_responses` responses |
| Transform | Required in practice | Optional, often still worth it | Optional, often still worth it |
| Pricing | Version 1 or 2 | Version 1 or 2 | Always version 2 |
| Extra methods | `GET`, `HEAD`, `POST` | plus `PUT`, `DELETE`, `PATCH` | plus those when `total_requests`, `min_responses` and `max_responses` are all equal |
| Risk | N simultaneous requests trip API rate limits | That node could observe or modify the response | Reconciling the responses is your job |

Use replicated when you need the integrity guarantee consensus gives, non-replicated for rate-limited APIs and non-idempotent POSTs, and flexible when the data changes faster than nodes could ever agree on it.

## Implementation

### Motoko

Import both the wrapper and the types from the `ic` mops package: `import Call "mo:ic/Call"` and `import IC "mo:ic/Types"`. `Call.httpRequest` computes and attaches the required cycles.

**This is pricing version 1.** Motoko has no version 2 path and no flexible outcalls yet (see the support matrix). Everything below is correct and supported; it is simply the legacy pricing model.

```motoko
import Blob "mo:core/Blob";
import Nat "mo:core/Nat";
import Text "mo:core/Text";
import Call "mo:ic/Call";
import IC "mo:ic/Types";

persistent actor {

  // Transform function: strips headers so all replicas see the same response for consensus.
  // MUST be a `shared query` function.
  public query func transform({
    context : Blob;
    response : IC.HttpRequestResult;
  }) : async IC.HttpRequestResult {
    {
      response with headers = []; // Strip headers -- they often contain non-deterministic values
    };
  };

  // GET request: fetch a JSON API
  public func getIcpPriceUsd() : async Text {
    let url = "https://api.coingecko.com/api/v3/simple/price?ids=internet-computer&vs_currencies=usd";

    let request : IC.HttpRequestArgs = {
      url = url;
      // Always set — omitting defaults to 2MB and charges accordingly.
      // Budget for response headers + body: the cap covers both, and the
      // transform cannot bring an oversized response back under it.
      max_response_bytes = ?(10_000 : Nat64);
      headers = [
        { name = "User-Agent"; value = "ic-canister" },
      ];
      body = null;
      method = #get;
      transform = ?{
        function = transform;
        context = Blob.fromArray([]);
      };
      is_replicated = null;
    };

    // Call.httpRequest computes and attaches the required cycles automatically
    let response = await Call.httpRequest(request);

    switch (Text.decodeUtf8(response.body)) {
      case (?text) { text };
      case (null) { "Response is not valid UTF-8" };
    };
  };

  // POST transform: also discards the body, because httpbin.org echoes the
  // sender's IP in "origin", which differs across replicas.
  public query func transformPost({
    context : Blob;
    response : IC.HttpRequestResult;
  }) : async IC.HttpRequestResult {
    {
      response with
      headers = [];
      body = Blob.fromArray([]);
    };
  };

  // POST request: send JSON data
  public func postData(jsonPayload : Text) : async Text {
    let url = "https://httpbin.org/post";

    let request : IC.HttpRequestArgs = {
      url = url;
      max_response_bytes = ?(50_000 : Nat64);
      headers = [
        { name = "Content-Type"; value = "application/json" },
        { name = "User-Agent"; value = "ic-canister" },
        // Idempotency key: prevents duplicate processing if multiple replicas hit the endpoint
        { name = "Idempotency-Key"; value = "unique-request-id-12345" },
      ];
      body = ?Text.encodeUtf8(jsonPayload);
      method = #post;
      transform = ?{
        function = transformPost;
        context = Blob.fromArray([]);
      };
      is_replicated = null;
    };

    // Call.httpRequest computes and attaches the required cycles automatically
    let response = await Call.httpRequest(request);

    if (response.status == 200) {
      "POST successful (status 200)";
    } else {
      "POST failed with status " # Nat.toText(response.status);
    };
  };
};
```

### Rust

```toml
# Cargo.toml
[package]
name = "https_outcalls_backend"
version = "0.1.0"
edition = "2024"

[lib]
crate-type = ["cdylib"]

[dependencies]
ic-cdk = "0.20"
ic-cdk-management-canister = "0.2"
candid = "0.10"
serde = { version = "1", features = ["derive"] }
serde_json = "1"
```

```rust
use ic_cdk_management_canister::{
    transform_context_from_query, HttpMethod, HttpRequest, HttpRequestResult, TransformArgs,
};
use ic_cdk::{query, update};

/// Transform function: strips non-deterministic headers so all replicas agree.
/// MUST be a #[query] function.
#[query(hidden = true)]
fn transform(args: TransformArgs) -> HttpRequestResult {
    HttpRequestResult {
        status: args.response.status,
        body: args.response.body,
        headers: vec![], // Strip all headers for consensus
        // If you need specific headers, filter them here:
        // headers: args.response.headers.into_iter()
        //     .filter(|h| h.name.to_lowercase() == "content-type")
        //     .collect(),
    }
}

/// GET request: Fetch JSON from an external API
#[update]
async fn fetch_price() -> String {
    let url = "https://api.coingecko.com/api/v3/simple/price?ids=internet-computer&vs_currencies=usd";

    // The builder always selects pricing version 2. `.send()` prices the call
    // with ic0.cost_http_request_v2 and attaches that amount.
    let request = HttpRequest::new(url)
        .with_method(HttpMethod::GET)
        // Budget for response headers + body: the cap covers both, and the
        // transform cannot bring an oversized response back under it.
        .with_max_response_bytes(10_000)
        .with_header("User-Agent", "ic-canister")
        .with_transform(transform_context_from_query("transform".to_string(), vec![]))
        // Unset expectations reserve the worst case: a 60s round trip and a
        // transform running to the full 5-billion-instruction query limit.
        // Declaring them holds far fewer cycles. See pitfall 12.
        .with_expected_roundtrip_time_ms(10_000)
        .with_expected_transform_instructions(1_000_000);

    match request.send().await {
        Ok(response) => {
            let body = String::from_utf8(response.body)
                .unwrap_or_else(|_| "Invalid UTF-8 in response".to_string());

            if response.status != candid::Nat::from(200u64) {
                return format!("HTTP error: status {}", response.status);
            }

            body
        }
        Err(err) => {
            format!("HTTP outcall failed: {:?}", err)
        }
    }
}

/// POST transform: strips headers AND body, because httpbin.org echoes the
/// sender's IP in "origin", which differs across replicas.
#[query(hidden = true)]
fn transform_post(args: TransformArgs) -> HttpRequestResult {
    HttpRequestResult {
        status: args.response.status,
        body: vec![],
        headers: vec![],
    }
}

/// POST request: Send JSON data to an external API
#[update]
async fn post_data(json_payload: String) -> String {
    let url = "https://httpbin.org/post";

    let request = HttpRequest::new(url)
        .with_method(HttpMethod::POST)
        .with_max_response_bytes(50_000)
        .with_header("Content-Type", "application/json")
        .with_header("User-Agent", "ic-canister")
        // Idempotency key: prevents duplicate processing across replicas
        .with_header("Idempotency-Key", "unique-request-id-12345")
        .with_body(json_payload.into_bytes())
        .with_transform(transform_context_from_query("transform_post".to_string(), vec![]))
        .with_expected_roundtrip_time_ms(10_000)
        .with_expected_transform_instructions(1_000_000);
    // Replicated, so every node POSTs: hence the idempotency key above, and
    // `transform_post`. `.non_replicated()` would send it once instead and make
    // both unnecessary, at the cost of trusting that one node (pitfall 8).

    match request.send().await {
        Ok(response) => {
            if response.status == candid::Nat::from(200u64) {
                "POST successful (status 200)".to_string()
            } else {
                format!("POST failed with status {}", response.status)
            }
        }
        Err(err) => {
            format!("HTTP outcall failed: {:?}", err)
        }
    }
}
```

### Cycle Cost Estimation

There are two pricing versions. Version 1 is the replica default and is deprecated; version 2 ("pay-as-you-go") charges for the resources a call consumes instead of the bytes it reserves. **Motoko is version 1 only; Rust with `ic-cdk-management-canister` 0.2 is version 2 only.** Version 1, which follows, is still the replica default; for version 2 in full, including the reservation mechanics and its distinct failure modes, read `references/pricing-version-2.md`.

The `ic0.cost_http_request` system API computes the exact cycle cost at runtime, so canisters do not need to hard-code the formula. `Call.httpRequest` from the `ic` mops package (Motoko) calls it internally and attaches the required cycles automatically; on the Rust side the same is true of the free `http_request` in `ic-cdk-management-canister` 0.1, or `ic_cdk::management_canister::http_request` on ic-cdk 0.19. For manual use: in Motoko, `Prim.costHttpRequest(requestSize, maxResponseBytes)` (via `import Prim "mo:⛔"`); in Rust, `ic_cdk::api::cost_http_request(request_size, max_res_bytes)`.

`request_size` is the sum of byte lengths of the URL, all header names and values, the body, the transform function name, and the transform context.

For reference, the underlying formula on a 13-node subnet (n = 13) is:

```text
Base cost:                      49_140_000 cycles  (= (3_000_000 + 60_000*13) * 13)
+ per request byte:              5_200 cycles      (= 400 * 13)
+ per max_response_bytes byte:  10_400 cycles      (= 800 * 13)

IMPORTANT: Under version 1 the charge is against max_response_bytes, NOT the
actual response size. Under version 2 it is the reverse: the charge follows
the bytes that arrive, the round-trip time and the transform instructions.
Omitting max_response_bytes assumes the 2MB maximum (2_000_000 bytes) and costs
49_140_000 + 10_400 * 2_000_000 = 20_849_140_000 cycles (~20.85B), plus the
per-request-byte term.
```

Under version 1, unused cycles are refunded when the call returns, so over-budgeting is **safe but not free**. Under version 2 it is not merely wasteful: the attachment beyond the base fee is the per-node allowance, which sets each node's response deadline and transform instruction limit, so a margin is permission to spend rather than idle reserve. Version 2 refunds also arrive asynchronously, with a node that never reported returning its allowance about a minute after the response. Attached cycles leave the canister's spendable balance for the *duration* of the call, so a hand-attached margin directly caps how many outcalls the canister can have in flight before it runs out of balance. For a canister making one outcall per user action, that margin is a concurrency limit. This is why both wrappers attach the exact computed amount rather than a round number — as the `ic` mops package puts it: *"Only minimal amount of cycles are added to the call. This helps the canister to make more calls in parallel without running out of cycles."*

Do not hand-attach a buffer "to be safe". Call the wrapper, or compute the exact cost with `Prim.costHttpRequest` / `ic_cdk::api::cost_http_request` and attach that. Under version 1, the way to lower the cost of an outcall is a tighter `max_response_bytes`, never a larger attachment. Under version 2 the price follows what the call consumes; the round trip and the transform are governed by their `with_expected_*` setters, and size is still governed by `max_response_bytes`, which now sizes the reservation rather than the price.

This formula applies on a normal **Application subnet**. It does not apply on a **cloud engine** (`CloudEngine` subnet): there, `ic0.cost_http_request` returns 0 regardless of `request_size` or `max_response_bytes`, because engines run under a free cost schedule. Load the `cloud-engine-canisters` skill for the engine's call rules before writing or debugging outcall code that will run there.

## Deploy & Test

### Local Deployment

```bash
icp network start -d
icp deploy backend
```

Note: HTTPS outcalls work on the local replica. icp-cli proxies the requests through the local HTTP gateway. Flexible outcalls run locally too, but every response comes from the same single node, so reconciliation never sees disagreement there.

### Mainnet Deployment

```bash
icp canister status backend -e ic && icp deploy -e ic backend   # check balance, then deploy
```

## Verify It Works

```bash
# 1. GET outcall. Expected: '("{\"internet-computer\":{\"usd\":12.34}}")', price varies.
icp canister call backend getIcpPriceUsd '()'   # Motoko example above
icp canister call backend fetch_price '()'      # Rust example above

# 2. POST outcall. Expected: httpbin.org echoing your data back.
icp canister call backend postData '("{\"test\": \"hello\"}")'    # Motoko
icp canister call backend post_data '("{\"test\": \"hello\"}")'   # Rust

# 4. Balance should have decreased. Under version 2 it keeps settling for about
#    a minute afterwards as per-node refunds arrive, so re-read before judging.
icp canister status backend

# 5. Error handling: add a function calling a non-existent domain and verify it
#    returns an error rather than trapping.
```

### Debugging Outcall Failures

If an outcall fails:

```bash
# Check the replica log for detailed error messages
# Local: icp output shows errors inline
# Mainnet: check the canister logs

# Exact reject messages from the replica (match on these, not on paraphrases):
#
# "Timeout expired"                                                     [SysFatal]
#     The remote server did not respond within 30s.
#
# "Canister http request timed out"                                  [SysTransient]
#     The subnet did not produce a response within 60s. Normally retryable.
#     Under version 2 it can also mean under-funding, but only when a node went
#     silent AND the remaining contributors cannot fund delivery without it;
#     then a retry just times out again. See references/pricing-version-2.md.
#
# "Deadline Exceeded"                                                [SysTransient]
#     The adapter did not answer the replica within its 60s deadline. Rarer
#     than the two above: the adapter's own 30s timeout usually fires first.
#
# "No consensus could be reached. Replicas had different responses.
#  Details: request_id: <id>, hashes: <...>"                         [SysTransient]
#     Transform is missing or not stripping enough non-determinism.
#
# There are THREE distinct size-limit messages, all [SysFatal], because response
# headers are counted against max_response_bytes BEFORE the body is read:
#
# "Header size exceeds specified response size limit <N>"
#     The response headers ALONE exceeded max_response_bytes.
#
# "Http body exceeds size limit of <N> bytes."
#     The body exceeded the allowance REMAINING after header bytes were
#     subtracted. Note the message prints the full cap <N>, not the remainder,
#     so the body that failed can be well under <N>. Do not read this message
#     as "my body is too big" -- it means headers + body are too big.
#
# "Transformed http response exceeds limit: <N>"
#     The Candid-encoded output of your transform exceeded max_response_bytes.
#
#     Raising max_response_bytes fixes all three. Stripping headers in the
#     transform fixes ONLY this last one: the first two are checked before
#     the transform runs.
#
# "http_request request sent with <X> cycles, but <Y> cycles are required."
#                                                              [CanisterReject]
#     Attached less than the computed cost. Use the wrapper rather than a
#     hand-picked number. Version 1 only: version 2 checks just the base fee up
#     front and fails later instead, as one of the next two.
#
# "Insufficient cycles"                                        [CanisterReject]
#     Version 2: a node exhausted its own per-node allowance. Ordinary response
#     content, so it reaches the canister only if a quorum produce the same
#     reject; otherwise it becomes a divergence.
#
# "Out of cycles: <k> of the assigned replicas reported a collective spend of
#  <n> cycles, leaving <m> cycles of the attached payment (after base fee
#  deduction). Delivering a response would cost at least <min> cycles."
#                                                              [CanisterReject]
#     Version 2 pooled shortfall: the nodes agreed, but what they left unspent
#     does not cover putting the response in a block. Raise the reservation.
```

### Transform Debugging

If you get "no consensus could be reached" errors, your transform function is not making responses identical. Common culprits:

1. **Response headers differ** -- strip ALL headers in the transform
2. **JSON field ordering differs** -- parse and re-serialize the JSON in the transform
3. **Timestamps in response body** -- extract only the fields you need

For a typed JSON parser and a transform that normalizes field ordering, see `references/json-responses.md`.

## Additional References

- **`references/pricing-version-2.md`** — the pay-as-you-go model: what it charges, the four expectations and their defaults, why they fund one pooled per-node budget, the reject messages for an under-funded call, and what to check before migrating.
- **`references/json-responses.md`** — parsing a typed JSON body with `serde_json`, and a transform that re-serializes to normalize field ordering for consensus.
- **`references/flexible-outcalls.md`** — `flexible_http_request` in full: replication counts derived from `subnet_self_node_count`, a compiling example, reconciliation strategies and their threat model, the four `global_error` values, the two separate size limits, why a local run never shows disagreement, and whether a transform pays for itself.
- Load `cloud-engine-canisters` for canisters running on a cloud engine, including why outcall cost drops to 0 there and why outcalls must never be routed through the engine's console proxy.
