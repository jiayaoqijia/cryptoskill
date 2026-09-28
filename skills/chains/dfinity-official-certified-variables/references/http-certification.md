# HTTP Certification for Custom `http_request` Canisters

For canisters serving HTTP responses directly from `http_request`, responses must be certified so the HTTP gateway can verify them. Below is a complete, minimal canister that serves one certified response at `/hello` and a certified 404 for every other path. Every path the gateway can request needs a certified response; an uncertified 404 or error is rejected with `backend_response_verification`:

**Cargo.toml dependencies:**

```toml
[dependencies]
candid = "0.10"
ic-cdk = "0.20"
ic-http-certification = "4"
```

**Certifying and serving the response:**

```rust
use ic_cdk::{init, post_upgrade, query};
use ic_http_certification::{
    utils::add_v2_certificate_header, DefaultCelBuilder, DefaultResponseCertification,
    HttpCertification, HttpCertificationPath, HttpCertificationTree, HttpCertificationTreeEntry,
    HttpRequest, HttpResponse, CERTIFICATE_EXPRESSION_HEADER_NAME,
};
use std::cell::RefCell;

const PATH: &str = "/hello";

// A certified response: the tree path it is certified under, the response, and its certification.
type Certified = (HttpCertificationPath<'static>, HttpResponse<'static>, HttpCertification);

thread_local! {
    static TREE: RefCell<HttpCertificationTree> = RefCell::new(HttpCertificationTree::default());
    // [0] = the response for PATH, [1] = the 404 served for every other path.
    static CERTIFIED: RefCell<Vec<Certified>> = RefCell::new(Vec::new());
}

fn certify() {
    let cel = DefaultCelBuilder::response_only_certification()
        .with_response_certification(DefaultResponseCertification::certified_response_headers(vec![
            "Content-Type",
        ]))
        .build();
    // The IC-CertificateExpression header must be part of every response that gets certified.
    let headers = vec![
        ("Content-Type".to_string(), "text/plain".to_string()),
        (CERTIFICATE_EXPRESSION_HEADER_NAME.to_string(), cel.to_string()),
    ];
    let responses = vec![
        (HttpCertificationPath::exact(PATH), HttpResponse::ok(b"hello".to_vec(), headers.clone()).build()),
        // A wildcard path covers every URL without a more specific entry, so the 404 is certified too.
        (HttpCertificationPath::wildcard("/"), HttpResponse::not_found(b"not found".to_vec(), headers).build()),
    ];

    let certified: Vec<Certified> = responses
        .into_iter()
        .map(|(path, response)| {
            let certification = HttpCertification::response_only(&cel, &response, None).unwrap();
            (path, response, certification)
        })
        .collect();

    TREE.with_borrow_mut(|tree| {
        for (path, _, certification) in &certified {
            tree.insert(&HttpCertificationTreeEntry::new(path, certification));
        }
        ic_cdk::api::certified_data_set(tree.root_hash());
    });
    CERTIFIED.with_borrow_mut(|c| *c = certified);
}

#[init]
fn init() {
    certify();
}

// The tree lives on the heap and is wiped on upgrade: rebuild it and re-set the root hash.
#[post_upgrade]
fn post_upgrade() {
    certify();
}

#[query]
fn http_request(req: HttpRequest) -> HttpResponse<'static> {
    let request_path = req.get_path().unwrap_or_default();
    let index = if request_path == PATH { 0 } else { 1 };
    let (path, mut response, certification) = CERTIFIED.with_borrow(|c| c[index].clone());
    // The witness proves this entry is the one that applies to the requested path.
    let witness = TREE.with_borrow(|tree| {
        tree.witness(&HttpCertificationTreeEntry::new(&path, &certification), &request_path)
            .unwrap()
    });
    add_v2_certificate_header(
        &ic_cdk::api::data_certificate().expect("http_request must be a query"),
        &mut response,
        &witness,
        &path.to_expr_path(),
    );
    response
}

ic_cdk::export_candid!();
```

`response_only_certification` certifies the response regardless of request details; use `DefaultCelBuilder::full_certification()` with `HttpCertification::full` when request headers or query parameters must be bound too. For many or dynamic responses (JSON APIs, fallbacks, skipping certification, upgrading to update calls), follow the [ic-http-certification docs](https://docs.rs/ic-http-certification) and the [http-certification examples](https://github.com/dfinity/response-verification/tree/main/examples/http-certification). Their project setup uses dfx, but the canister code applies unchanged. For static files served from your own Rust canister, `ic-asset-certification` builds on this crate.

## Checking it

```bash
# Local: take the gateway URL from the running network (its port is not always 8000)
GATEWAY=$(icp network status --json | jq -r .gateway_url)
curl -s -D - "${GATEWAY}hello?canisterId=CANISTER_ID"
# Mainnet
curl -s -D - https://CANISTER_ID.icp.net/hello
```

Expected: `200` for `/hello` and a certified `404` for any other path, both with `IC-Certificate` and `IC-CertificateExpression` headers. A response that fails verification comes back as JSON with `"error_type": "backend_response_verification"`. The `raw` host (`CANISTER_ID.raw.icp.net`, locally `CANISTER_ID.raw.localhost`) skips verification, so it serves even a broken certification: do not test there.
