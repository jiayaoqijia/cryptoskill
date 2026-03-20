---
title: Download and decrypt attachments
impact: CRITICAL
tags: attachments, download, decrypt, receive
---

## Download and decrypt attachments

Use the `attachment` event and `downloadRemoteAttachment` to receive files.

**Basic receiver:**

```typescript
import { downloadRemoteAttachment } from "@xmtp/agent-sdk/util";

agent.on("attachment", async (ctx) => {
  const attachment = await downloadRemoteAttachment(
    ctx.message.content,
    agent
  );
  
  console.log(`Filename: ${attachment.filename}`);
  console.log(`MIME type: ${attachment.mimeType}`);
  console.log(`Size: ${attachment.data.byteLength} bytes`);
});
```

**Save to disk:**

```typescript
import fs from "fs";

agent.on("attachment", async (ctx) => {
  const attachment = await downloadRemoteAttachment(
    ctx.message.content,
    agent
  );
  
  fs.writeFileSync(`./downloads/${attachment.filename}`, attachment.data);
  await ctx.conversation.sendText(`Saved: ${attachment.filename}`);
});
```

**How it works:**

1. The SDK receives the remote attachment message
2. `downloadRemoteAttachment` fetches the encrypted file from the URL
3. The file is decrypted using the keys in the message
4. You receive the decrypted file content
