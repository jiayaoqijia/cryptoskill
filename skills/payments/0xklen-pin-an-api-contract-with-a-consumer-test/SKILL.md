---
name: pin-an-api-contract-with-a-consumer-test
description: Use when a provider team can silently change a response your client depends on — record the consumer's real expectations as a pact and verify the provider against it in CI.
---

# Pin an API contract with a consumer test

Unit tests mock the provider, so they pass while production breaks. A consumer-driven contract records what your client actually needs and fails the provider build when it stops honoring it.

## Procedure

1. Declare the exact request the consumer makes and the fields it reads:
```python
from pact import Consumer, Provider
pact = Consumer("checkout-web").has_pact_with(Provider("orders-api"))
(pact.given("order 42 exists")
     .upon_receiving("a request for order 42")
     .with_request("GET", "/orders/42")
     .will_respond_with(200, body={"id": 42, "status": "paid"}))
```
2. Run the consumer tests against the mock provider Pact generates — this proves the consumer needs only what it declares:
```
pytest tests/consumer/ -q && ls pacts/checkout-web-orders-api.json
```
3. Parse the response into a typed model so undeclared fields cannot silently become requirements:
```python
class Order(BaseModel):      # pydantic
    id: int
    status: Literal["paid", "pending"]
```
Add body fields to the model only when the code reads them.
4. Publish the pact to the broker:
```
pact-broker publish pacts/ --consumer-app-version=$(git rev-parse --short HEAD) --broker-base-url=$BROKER
```
5. Verify on the provider side against a real, seeded instance:
```
pact-provider-verifier --provider-base-url=http://localhost:8080 \
  --pact-broker-base-url=$BROKER --provider-app-version=$(git rev-parse --short HEAD)
```
Required: all interactions verified, exit 0.
6. Gate deployment:
```
pact-broker can-i-deploy --pacticipant checkout-web --version $(git rev-parse --short HEAD) --to-environment production
```
7. Run consumer tests on every client PR and provider verification on every provider PR so a break is caught on whichever side moved.

## Pitfalls

- A pact asserting the whole response body makes the provider unable to add fields; assert only consumed fields.
- Verifying against a stubbed provider is not verification. Point `--provider-base-url` at a real seeded instance.
- Contracts drift if the client model is "just in case" broad. Keep it to fields the code reads.
- `can-i-deploy` needs both versions published; a missing publish fails open. Fail closed if the broker call errors.

## Verification

```
pact-broker can-i-deploy --pacticipant checkout-web --version $(git rev-parse --short HEAD) --to-environment production
```
Passes = prints `Computer says yes`. Report: "checkout-web 3f9a1c can-i-deploy=yes against orders-api, 4 interactions verified."
