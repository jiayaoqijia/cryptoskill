---
name: ton-blockchain
description: "Use when working with The Open Network (TON) blockchain, or when the user mentions TON-ecosystem terms the agent may not recognize—such as Tact, FunC, Tolk, Fift, TL-B, TVM, cells, BoC, Jettons, TEPs, TON Connect, workchains, shardchains, or liteservers. Provides a docs-first workflow for fetching and navigating TON documentation accurately, and covers smart contract development, transaction mechanics, wallet standards, token standards, Telegram Mini Apps, and infrastructure."
---

# TON Docs-first workflow

Prefer primary sources from TON Docs.

## 1) Read the orientation page first

Fetch and skim the TON Docs “start here” page to align terminology and the docs’ structure before making assumptions:

```bash
curl -fsSL https://docs.ton.org/llms/start-here/content.md
```

If the `.md` URL fails, try the HTML page:

```bash
curl -fsSL https://docs.ton.org/start-here
```

## 2) Discover available pages

Fetch `llms.txt` to get the authoritative list of TON Docs pages and then search within it for relevant sections/pages:

```bash
curl -fsSL https://docs.ton.org/llms.txt
```

Practical pattern:

```bash
curl -fsSL https://docs.ton.org/llms.txt | rg -n "<topic>|<keyword>" || true
```

(Use `grep -nE` instead of `rg` if ripgrep isn’t available.)

## 3) Pull only the pages you need

For any relevant page path from `llms.txt`, prefer the Markdown source by appending `/content.md` and prepending `/llms`:

```bash
curl -fsSL "https://docs.ton.org/llms/<page-path>/content.md"
```

If that 404s, try the path as-is (some entries may already include `.md` or may not support source rendering):

```bash
curl -fsSL "https://docs.ton.org/<page-path>"
```

## 4) Execute the task using the docs as ground truth

- Treat TON Docs as the primary reference; reconcile contradictions explicitly.
- When answering, mention which TON Docs pages you consulted (page titles/paths).
- If the user’s code/repo conventions conflict with TON Docs guidance, ask for clarification before proceeding.
