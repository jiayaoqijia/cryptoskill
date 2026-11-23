#!/usr/bin/env python3
"""Keyless Solana RPC: reconstruct a wallet's position + PnL in ONE token.

Usage:
    python3 solana_wallet_token_pnl.py <WALLET> <MINT> [--sol-usd 117.67] [--price-usd 0.00045792] [--limit 40]

Answers the same question as `gmgn-cli portfolio holdings` (which needs GMGN_PRIVATE_KEY):
what the wallet bought, for how much, what it still holds, and the resulting PnL.
No API key, no signature, read-only.

Built + verified 1 Oct 2026 on a real wallet (HOURS: 2 buys + 2 partial sells in 8 minutes).
The per-accountIndex pairing below is the fix for a bug that silently reported "+0.00" for
every transaction -- do not "simplify" it back to sum(post.values()) - sum(pre.values()).
"""
import json
import sys
import time
import urllib.request

RPCS = [
    "https://solana-rpc.publicnode.com",
    "https://api.mainnet-beta.solana.com",
    "https://solana.drpc.org",
]
SPL = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"          # classic SPL
TOKEN2022 = "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"    # Token-2022


def rpc(method, params, tries=6, pause=1.0):
    """Rotate the endpoint ladder with backoff -- one 429 must not fail the run."""
    last = None
    for i in range(tries):
        url = RPCS[i % len(RPCS)]
        body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
        try:
            req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
            out = json.loads(urllib.request.urlopen(req, timeout=30).read())
            if "result" in out:
                time.sleep(pause)
                return out
            last = out.get("error")
        except Exception as exc:                     # 429 / 5xx / flake
            last = exc
        time.sleep(2 + 2 * i)
    raise SystemExit("RPC failed after %d tries on %s: %s" % (tries, method, last))


def my_atas(wallet, mint):
    """The wallet's own token accounts for this mint -- attribution depends on these."""
    atas = []
    for prog in (SPL, TOKEN2022):
        res = rpc("getTokenAccountsByOwner",
                  [wallet, {"programId": prog}, {"encoding": "jsonParsed"}], pause=0.4)
        for acc in res.get("result", {}).get("value", []):
            info = acc["account"]["data"]["parsed"]["info"]
            if info["mint"] == mint:
                atas.append(acc["pubkey"])
    return atas


def legs(wallet, mint, atas, limit):
    sigs = rpc("getSignaturesForAddress", [wallet, {"limit": limit}])["result"]
    rows = []
    for s in sigs:
        tx = rpc("getTransaction", [s["signature"],
                                   {"encoding": "jsonParsed",
                                    "maxSupportedTransactionVersion": 0}]).get("result")
        if not tx or not tx.get("meta"):
            continue                                  # dropped / failed tx
        meta = tx["meta"]
        keys = [k["pubkey"] for k in tx["transaction"]["message"]["accountKeys"]]
        i_w = keys.index(wallet) if wallet in keys else None
        d_sol = ((meta["postBalances"][i_w] - meta["preBalances"][i_w]) / 1e9) if i_w is not None else 0.0
        pre = {b["accountIndex"]: float(b["uiTokenAmount"]["uiAmountString"])
               for b in (meta.get("preTokenBalances") or []) if b.get("mint") == mint}
        post = {b["accountIndex"]: float(b["uiTokenAmount"]["uiAmountString"])
                for b in (meta.get("postTokenBalances") or []) if b.get("mint") == mint}
        for idx in sorted(set(pre) | set(post)):
            delta = post.get(idx, 0.0) - pre.get(idx, 0.0)   # PAIR PER INDEX
            if abs(delta) < 0.5:
                continue
            owner = keys[idx] if idx < len(keys) else "?"
            if owner not in [wallet] + atas:                 # venue vault / pool -> not the user
                continue
            rows.append({"t": s["blockTime"], "d": delta, "sol": d_sol,
                         "bal": post.get(idx, 0.0), "sig": s["signature"]})
    rows.sort(key=lambda r: r["t"] or 0)
    return rows


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    wallet, mint = sys.argv[1], sys.argv[2]
    opt = {"--sol-usd": None, "--price-usd": None, "--limit": 40}
    for i, a in enumerate(sys.argv):
        if a in opt and i + 1 < len(sys.argv):
            opt[a] = int(sys.argv[i + 1]) if a == "--limit" else float(sys.argv[i + 1])

    atas = my_atas(wallet, mint)
    print("# wallet %s\n# mint   %s\n# ATA    %s"
          % (wallet, mint, ", ".join(atas) or "none (no balance in this mint)"))
    rows = legs(wallet, mint, atas, opt["--limit"])
    if not rows:
        print("no legs in the last %d signatures -- widen --limit or re-check the mint"
              % opt["--limit"])
        return

    t_in = sum(r["d"] for r in rows if r["d"] > 0)
    t_out = -sum(r["d"] for r in rows if r["d"] < 0)
    sol_out = -sum(r["sol"] for r in rows if r["d"] > 0)
    sol_in = sum(r["sol"] for r in rows if r["d"] < 0)
    open_tk = t_in - t_out
    avg_entry = (sol_out / t_in) if t_in else 0.0
    realized_sol = sol_in - t_out * avg_entry

    for r in rows:
        tstr = time.strftime("%d %b %H:%M", time.localtime(r["t"])) if r["t"] else "unknown"
        print("%s  %-4s %15.2f  SOL %+.6f  bal %14.2f  %s"
              % (tstr, "BUY" if r["d"] > 0 else "SELL", r["d"], r["sol"], r["bal"], r["sig"][:14]))

    print("\nbought %15.2f tok for %10.6f SOL" % (t_in, sol_out))
    print("sold   %15.2f tok for %10.6f SOL" % (t_out, sol_in))
    print("open   %15.2f tok" % open_tk)
    print("avg entry %10.4fe-06 SOL" % (avg_entry * 1e6))
    if t_out:
        print("avg exit  %10.4fe-06 SOL" % ((sol_in / t_out) * 1e6))
    print("realized  %10.6f SOL" % realized_sol)

    sol_usd, price_usd = opt["--sol-usd"], opt["--price-usd"]
    if sol_usd and price_usd:
        price_sol = price_usd / sol_usd
        print("\n# USD at SOL $%.2f (ONE dated conversion -- never per-leg with a remembered rate)" % sol_usd)
        print("avg entry $%.8f | market $%.8f | vs entry %+.1f%%"
              % (avg_entry * sol_usd, price_usd,
                 100 * (price_usd / (avg_entry * sol_usd) - 1) if avg_entry else 0))
        val = open_tk * price_usd
        cost = sol_out * sol_usd
        pnl = val + sol_in * sol_usd - cost
        print("position $%.2f (%.6f SOL) | cost $%.2f | realized $%.2f | PnL $%+.2f (%+.1f%%)"
              % (val, open_tk * price_sol, cost, sol_in * sol_usd,
                 pnl, 100 * (pnl / cost) if cost else 0))
        print("cost basis of the open part: $%.2f" % (open_tk * avg_entry * sol_usd))
    else:
        print("\n# pass --sol-usd and --price-usd for the USD table")


if __name__ == "__main__":
    main()
