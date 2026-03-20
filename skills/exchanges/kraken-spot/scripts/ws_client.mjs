#!/usr/bin/env node

import { readFileSync } from "node:fs";

function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

const args = process.argv.slice(2);
let url = "";
let timeoutMs = 10000;
let maxMessages = 1;
const messages = [];

for (let i = 0; i < args.length; i += 1) {
  const arg = args[i];
  switch (arg) {
    case "--url":
      url = args[++i] ?? "";
      break;
    case "--timeout-ms":
      timeoutMs = Number(args[++i] ?? "10000");
      break;
    case "--max-messages":
      maxMessages = Number(args[++i] ?? "1");
      break;
    case "--message-json":
      messages.push(args[++i] ?? "");
      break;
    case "--message-file":
      messages.push(readFileSync(args[++i] ?? "", "utf8"));
      break;
    default:
      fail(`unknown arg: ${arg}`);
  }
}

if (!url) {
  fail("missing --url");
}

if (!Number.isFinite(timeoutMs) || timeoutMs < 1) {
  fail("invalid --timeout-ms");
}

if (!Number.isFinite(maxMessages) || maxMessages < 1) {
  fail("invalid --max-messages");
}

const ws = new WebSocket(url);
let seen = 0;
let done = false;

const timer = setTimeout(() => {
  if (!done) {
    done = true;
    ws.close();
  }
}, timeoutMs);

ws.addEventListener("open", () => {
  for (const message of messages) {
    ws.send(message);
  }
});

ws.addEventListener("message", (event) => {
  process.stdout.write(`${event.data}\n`);
  seen += 1;
  if (seen >= maxMessages && !done) {
    done = true;
    clearTimeout(timer);
    ws.close();
  }
});

ws.addEventListener("error", (event) => {
  clearTimeout(timer);
  if (done) {
    return;
  }
  done = true;
  fail(`websocket error: ${event.message ?? "unknown"}`);
});

ws.addEventListener("close", () => {
  clearTimeout(timer);
  if (!done) {
    done = true;
  }
  process.exit(0);
});
