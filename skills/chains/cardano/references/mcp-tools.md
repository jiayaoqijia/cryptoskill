# Transaction MCP Tools Reference

## submit_transaction

Sign and submit a Cardano transaction from the connected wallet.

**Input:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `cbor` | `string` | Yes | Unsigned Cardano transaction in CBOR hex |

**Output:**

| Field | Type | Description |
|-------|------|-------------|
| `transactionHash` | `string` | Hash of the submitted transaction |
| `timestamp` | `number` | Millisecond timestamp of submission |

**Errors:** Returns an error message if signing or submission fails (e.g. insufficient funds, invalid CBOR).
