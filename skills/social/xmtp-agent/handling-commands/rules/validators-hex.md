---
title: Use validHex for hex string validation
impact: CRITICAL
tags: validators, hex, type safety
---

## Use validHex for hex string validation

Use the `validHex` validator instead of type assertions to maintain runtime safety.

**Incorrect (type assertion):**

```typescript
// Bad: Using type assertions for hexadecimal strings
usdcHandler.getUSDCBalance(agentAddress as `0x${string}`);
```

**Correct (use validHex):**

```typescript
import { validHex } from "@xmtp/agent-sdk";

// Good: Using the validHex validator to guarantee hexadecimal strings
usdcHandler.getUSDCBalance(validHex(agentAddress));
```

**Why this matters:**

- Type assertions only work at compile time
- `validHex` validates at runtime and throws if invalid
- Prevents bugs from invalid hex strings reaching blockchain operations
