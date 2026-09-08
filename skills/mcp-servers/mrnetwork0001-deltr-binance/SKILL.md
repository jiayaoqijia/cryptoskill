---
name: deltr-binance
description: Use Deltr to scan the Binance USDS-M Futures vs PancakeSwap V3 (BNB Chain) basis and funding, size a delta-neutral hedge (long DEX spot, short perp), and route it through a deterministic zero-LLM risk gate via Deltr's MCP tools or CLI. Paper mode by default (no keys); Binance Futures testnet with keys; an opt-in LIVE mode that places real mainnet orders and a real on-chain leg signed by the Binance Agentic Wallet. Deltr never holds a private key.
version: 1.0.0
license: MIT
metadata:
  version: 1.0.0
  author: mrnetwork0001
  openclaw:
    requires:
      bins:
        - python3
        - node
    install:
      - kind: shell
        label: Install Deltr (Python venv + Node deps)
        script: |
          set -e
          DELTR_HOME="${DELTR_HOME:-$HOME/.deltr}"
          if [ -d "$DELTR_HOME/.git" ]; then git -C "$DELTR_HOME" pull --ff-only; else git clone https://github.com/mrnetwork0001/Deltr.git "$DELTR_HOME"; fi
          cd "$DELTR_HOME"
          python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt
          npm ci --silent
---

# Deltr — delta-neutral CEX <-> DEX hedging on Binance (skill)

## Overview

Deltr watches the basis between PancakeSwap V3 (BNB Chain mainnet quotes) and the Binance USDS-M
Futures mark price plus the funding rate, prices the **full round trip** (DEX fee, impact, gas, perp
slippage, taker fees twice) over an explicit funding horizon (default 72 h), and proposes a paired
hedge: long BNB on the DEX, short the same quantity on the perp. Every order passes a deterministic,
zero-LLM risk gate (19 ordered checks, pure Python, a measured median of 1.5 to 2.5 µs across runs) before it
leaves the process. Use it for data & analysis (`scan`, `explain`) or for the two-phase trading flow
(`propose` -> `execute`).

What this agent never does:

* arm real money by accident. Modes are `paper` (keyless, simulated fills on real mainnet prices),
  `testnet` (real Binance Futures **testnet** perp leg; simulated DEX leg) and `live` (REAL MONEY:
  real mainnet perp orders posted as a maker, plus a real on-chain leg). LIVE is opt-in six times
  over and refuses to start unless all of `DELTR_MODE=live`, both mainnet credentials,
  `BINANCE_API_ENV=mainnet`, `DELTR_LIVE_ACK`, the on-chain opt-in, and an installed and signed-in
  wallet CLI are present, naming the first one missing. No tool or command changes the mode;
* hold, read, store or sign with a private key. The on-chain leg is delegated to the Binance
  Agentic Wallet CLI, which keeps custody, applies its own limits and does the signing;
* cross the spread by default. In LIVE the perp leg is post-only (GTX); an unfilled maker order is a
  failure that reverses the other leg, never a silent skip;
* withdraw or transfer funds — there is no such code path;
* execute from free text — `deltr_prompt` only proposes; execution needs a `plan_id` and, in
  testnet, `confirm: true`;
* retry a veto — a VETO is deterministic and final for the same inputs;
* hide a loss — positions are marked to close (net of the exit round trip) and a naked leg after a
  failed reversal is booked, badged and blocks new entries until an operator unwinds it.

## Preflight

```bash
bash scripts/deltr.sh status          # JSON: mode, venues (with feed ages), equity, drawdown, gate median
```

If no instance is running the wrapper runs `python main.py --once --json` (one tick, nothing
executes) and prints its `status` block. Start the full stack with `bash scripts/deltr.sh serve`
(dashboard http://127.0.0.1:8000, MCP at http://127.0.0.1:8000/mcp); `execute` and `unwind` need
that running instance because plans and positions live in it.

## Command routing

| Command | What it does | Executes? |
|---|---|---|
| `bash scripts/deltr.sh status` | status block (JSON) | no |
| `bash scripts/deltr.sh once --json` | one tick: market, edge waterfall, opportunity, sizing, plan, gate pre-check | no |
| `bash scripts/deltr.sh scan [n]` | latest opportunity + last `n` spread points | no |
| `bash scripts/deltr.sh explain [horizon_h]` | market + edge components + sizing for the horizon | no |
| `bash scripts/deltr.sh propose <capital_usd> [leverage]` | phase 1: size + gate pre-check -> `plan_id` (expires in 60 s, single-use) | no |
| `bash scripts/deltr.sh evaluate <capital_usd> <leverage>` | dry-run the gate: full check matrix with observed/limit (leverage above 3 is vetoed, never clamped) | no |
| `bash scripts/deltr.sh execute <plan_id> [--confirm]` | phase 2: re-price, re-gate, both legs with reverse-on-failure -> receipt | **yes** (paper fills, or a testnet perp order with `--confirm`) |
| `bash scripts/deltr.sh unwind <position_id\|all> [--confirm]` | reduce-only perp BUY then DEX sell | **yes** |
| `bash scripts/deltr.sh mcp` | stdio MCP transport in the same process as the dashboard | — |
| `bash scripts/deltr.sh serve [flags]` | `python main.py` (`--mode`, `--min-edge-bps`, `--replay`, `--auto`, `--port`) | — |

Flags, wrapper resolution and every JSON shape: [references/cli.md](references/cli.md).

## MCP tools

Deltr is itself an MCP server (streamable HTTP at `/mcp`, stdio with `--mcp`) with 22 tools and three
read-only resources; the two-phase pair is `deltr_propose_hedge` -> `deltr_execute_hedge(plan_id)`.
The table is generated from the server's own `tools/list`: [references/tools.md](references/tools.md).

## Risk model

Every order passes the gate; a VETO is deterministic and **final for the same inputs** — change
capital or leverage (or ask `deltr_explain_edge`) instead of retrying. Limits: max 3x leverage, max
2 % of equity at risk per trade, 3 % drawdown halt (sticky, survives restarts), price drift 20 bps at
execution, stale quotes 5 s, price sanity 100 bps. The 19 checks, thresholds and the measured latency:
[references/risk-model.md](references/risk-model.md).

## Auth

Same environment names as the official `binance` skill: `BINANCE_API_KEY`, `BINANCE_SECRET_KEY`,
`BINANCE_API_ENV=testnet` (put them in `.env` or the environment; `.env.example` is the template).
Keys are read only in `testnet` and `live` modes; `BINANCE_API_ENV=prod` is refused in every mode
(mainnet trading is spelled `BINANCE_API_ENV=mainnet` and needs the full LIVE opt-in); no command, banner,
log line, receipt or MCP activity row prints a key value — every surface reports `secrets_present`
only. Never paste a key into a prompt or a tool argument.

## CONFIRM semantics

In `testnet` and `live` modes `execute` and `unwind` require `--confirm` (`confirm: true` over MCP / REST),
mirroring `binance-cli`'s CONFIRM. Without it the plan is kept and the result says
`CONFIRM_REQUIRED`. Paper mode needs no confirmation. Stress scenarios that could touch a real order
(`dex_leg_fail`, `feed_stale`, `equity_shock`) are refused in testnet; the others are refused while
real orders are open.

## Outputs (JSON)

Every command and tool returns one JSON document: `status` -> `SystemStatus`; `once --json` -> the
tick document (`market`, `edge`, `components`, `horizon`, `opportunity`, `sizing`, `plan`,
`precheck`, `status`);
`propose` -> `{"plan_id", "plan", "proposal", "precheck", "expires_at", "message"}`; `execute` -> an
`ExecutionReceipt` with ordered trace `steps` and a `sha256` over plan + decision + fills; `unwind` -> a
list of receipts. Errors are `{"error": {"code", "message"}}`, never a stack trace. Read `precheck.code`
/ `precheck.checks[]` to explain a veto with its observed value and limit.

Notes for interpretation: amounts given in USDC are treated as USDT-equivalent for sizing (no
conversion leg; the result says so); funding figures come from the Binance Futures testnet and are
indicative; `drawdown_pct` is in percent.

## Disclaimer

Deltr is a technical demonstration and does not provide financial, investment, legal or tax advice.
Nothing it outputs is a recommendation to enter any position, and you are solely responsible for any
decision you make with it.
