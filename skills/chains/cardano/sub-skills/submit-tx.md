# Submit a Transaction

## Steps

1. Receive the unsigned CBOR hex from the user or another tool.
2. Explain what the transaction will do in plain language.
3. Ask: "Would you like me to submit this transaction?"
4. Only on explicit confirmation, call `submit_transaction` with the CBOR.
5. Report the transaction hash on success.

## Example prompt

> "Submit this transaction: 84a400..."

## Example response

This transaction sends **50 ADA** to `addr1q...`. Would you like me to submit it?

*(After confirmation)*

Transaction submitted successfully.
- **Hash:** abc123...def
- **Time:** 2026-03-08T12:00:00Z
