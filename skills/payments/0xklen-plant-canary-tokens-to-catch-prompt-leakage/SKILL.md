---
name: plant-canary-tokens-to-catch-prompt-leakage
description: Use when you want to detect whether your system prompt, memory, or secrets leak into outputs. Seed unique canary strings and check every outbound surface for them.
---

# Plant canary tokens to catch prompt leakage

You cannot tell a prompt leaked unless you know what could only have come from your prompt. A canary is a high-entropy string that exists nowhere else, so its appearance anywhere else is proof of disclosure.

## Procedure

1. Generate canaries no tokenizer or crawler would produce by accident: `python3 -c "import secrets;print('CANARY-'+secrets.token_hex(12))"` twice — one for the system prompt, one for memory.

2. Place each canary at a distinct scope so a hit tells you what leaked: one in the system prompt header, one in a tool description, one in a retrieved document, one in `.env`.

3. Record the canary-to-scope map in a file you never send anywhere: `printf 'system: %s\nmemory: %s\n' "$A" "$B" >> ~/.canaries`.

4. Scan every outbound surface for the strings: model replies, tool calls, logs, HTTP requests, and rendered pages.

       grep -rFn -f ~/.canaries ~/.hermes/logs/ workspace/output/

5. Also check the wire: `sudo tcpdump -A -i any 'tcp port 443' -c 2000 | grep -F -f ~/.canaries`.

6. Rotate after any confirmed hit and after a fixed interval (daily is typical), because a canary that appeared once is burned. Regenerate and re-grep.

7. Treat any hit as a disclosure incident: identify the channel, stop it, then re-issue the canary in a narrower scope.

## Pitfalls

- A canary reused across scopes cannot localise the leak; use one string per scope.
- Low-entropy canaries ("token-1") appear by chance in logs and train false alarms; use 24+ hex chars.
- Storing the map where the model can read it defeats the purpose; keep it outside context.
- Checking only the final reply misses leaks through tool arguments and image URLs.

## Verification

    grep -rFn -f ~/.canaries ~/.hermes/logs/ ; echo "exit $?"   # exit 1 = no canary found = pass

Report: "N canaries planted across scopes <list>; hits none|at <surface>; last rotation <time>."
