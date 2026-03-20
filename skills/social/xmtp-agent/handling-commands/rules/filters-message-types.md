---
title: Filter by message type
impact: HIGH
tags: filters, message types, type safety
---

## Filter by message type

Use built-in filters to check message types instead of manual type checking.

**Available filters:**

```typescript
import { filter } from "@xmtp/agent-sdk";

// Check message types
filter.isText(ctx.message)
filter.isReaction(ctx.message)
filter.isReply(ctx.message)
filter.isAttachment(ctx.message)

// Check content
filter.hasDefinedContent(ctx.message)

// Check sender
filter.fromSelf(ctx.message, ctx.client)
```

**Example usage:**

```typescript
import { filter } from "@xmtp/agent-sdk";

agent.on("message", async (ctx) => {
  // Filter for specific message types to prevent infinite loops
  if (
    filter.hasDefinedContent(ctx.message) &&
    !filter.fromSelf(ctx.message, ctx.client) &&
    filter.isText(ctx.message)
  ) {
    await ctx.conversation.sendText("Valid text message received");
  }
});
```

**Short import alias:**

```typescript
import { f } from "@xmtp/agent-sdk";

if (f.isText(ctx.message)) {
  // Handle text message
}
```
