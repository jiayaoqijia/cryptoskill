#!/usr/bin/env python3
"""Vault-DD probe: reconciliation + depositability + strategy/pool risk, from a saved vault JSON.

Assembled from calls verified 20 Sep 2026 on Krystal / Robinhood Chain 4663. Field names and
endpoints drift — this prints a KEY-OK/KEY-MISSING line first, so check that before trusting output.

Usage:
  1) Save the vault JSON (the API URL answers 403 to raw curl from the shell; fetch it through the
     render/extract proxy path instead, then write the JSON body to a file):
       curl -s "https://api.krystal.app/all/v1/vaults/4663/0x23aa...02ee" > /tmp/vault.json   # if it works
  2) python3 krystal_vault_probe.py /tmp/vault.json
  3) optional on-chain spot-check (needs the chain RPC; robinhood 4663 RPCs that worked:
     https://rpc.mainnet.chain.robinhood.com , https://robinhood-rpc.publicnode.com):
       python3 krystal_vault_probe.py /tmp/vault.json --rpc https://rpc.mainnet.chain.robinhood.com
"""
import json
import sys
import urllib.request


def jrpc(url, method, params):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        out = json.load(r)
    if "error" in out:
        raise RuntimeError(out["error"])
    return out.get("result")


def eth_call(rpc, to, data):
    return jrpc(rpc, "eth_call", [{"to": to, "data": data}, "latest"])


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    d = json.load(open(sys.argv[1]))
    rpc = sys.argv[sys.argv.index("--rpc") + 1] if "--rpc" in sys.argv else None

    keys = ["tvl", "pnl", "apr", "feeApr", "feeGenerated", "earning24h", "earning30d", "allowDeposit",
            "totalUser", "totalSupply", "owner", "vaultType", "isAutoFarmVault", "isAgentActivated",
            "riskScore", "copyCount", "totalCopyFeeUsd", "userPerformance", "strategies", "assets", "pools"]
    present = [k for k in keys if k in d]
    print("KEY-OK:", ",".join(present))
    print("KEY-MISSING:", ",".join(k for k in keys if k not in d) or "-")

    up = d.get("userPerformance") or {}
    dep = up.get("totalDepositValue") or 0
    wd = up.get("totalWithdrawValue") or 0
    tvl = d.get("tvl") or 0
    fees = d.get("feeGenerated") or 0
    net = dep - wd - tvl
    print("\n== depositability ==")
    if d.get("allowDeposit") is True and (d.get("totalUser") or 0) > 1:
        print("PUBLIC-ish vault: allowDeposit=True totalUser=%s -> others can deposit (check owner commission)"
              % d.get("totalUser"))
    else:
        print("PRIVATE vault: allowDeposit=%s totalUser=%s totalSupply=%s -> nobody else can deposit."
              % (d.get("allowDeposit"), d.get("totalUser"), d.get("totalSupply")))
        print("   => a promo link to this = showcase/ad, not an investable product. Test = create your OWN vault.")

    print("\n== cash flow (the only number that settles it) ==")
    print("deposits $%.2f  withdrawals $%.2f  tvl $%.2f  -> net $%.2f" % (dep, wd, tvl, net))
    print("feeGenerated $%.2f (24h $%.2f / 30d $%.2f)  |  panel pnl $%.2f  |  panel apr %s%%"
          % (fees, d.get("earning24h") or 0, d.get("earning30d") or 0, d.get("pnl") or 0, d.get("apr")))
    print("fee minus net_flow = $%.2f  <- what price/IL drag ate" % (fees - net))
    if d.get("earning24h") and tvl:
        print("FAQ formula (earning24h*365/liquidity) = %.0f%% -> if the apr field above disagrees,"
              " do NOT rank vaults by apr" % ((d["earning24h"]) * 365 / tvl * 100))

    st = d.get("strategies") or []
    if st:
        ages = sorted(s.get("ageInSecond", 0) for s in st) or [0]
        closed = sum(1 for s in st if s.get("status") == "CLOSED")
        tiers = {}
        for s in st:
            tiers[s.get("feeTierPercentage")] = tiers.get(s.get("feeTierPercentage"), 0) + 1
        print("\n== positions ==")
        print("%d strategies (%d CLOSED, %d open) | median age %.2f d -> ~%.1f rotations/day"
              % (len(st), closed, len(st) - closed, ages[len(ages) // 2] / 86400,
                 (len(st) / max(ages[len(ages) // 2] / 86400, 0.01))))
        print("fee tiers:", sorted(tiers.items(), key=lambda x: -x[1]))
        print("sum initialDepositValue $%.2f ; sum strategy pnl $%.2f"
              % (sum(s.get("initialDepositValue") or 0 for s in st), sum(s.get("pnl") or 0 for s in st)))
        print("open positions (print drawdown24h NEXT TO apr30d — that pair explains negative net flow):")
        for s in st:
            if s.get("status") == "CLOSED":
                continue
            p = s.get("pool") or {}
            print("  %-28s fee%s%% tvl $%-12.0f vol30d $%-14.0f apr30d %-9s drawdown24h %s%% pnl $%.2f"
                  % ("/".join(t.get("symbol", "?") for t in s.get("tokens", [])), p.get("fee"),
                     float(p.get("tvl") or 0), float(p.get("volume30d") or 0),
                     "%.0f" % (p.get("apr30d") or {}).get("apr", 0) if isinstance(p.get("apr30d"), dict) else "?",
                     round(p.get("drawdown24h") or 0, 1), s.get("pnl") or 0))

    if rpc:
        addr = (d.get("address") or d.get("vaultAddress") or d.get("id") or "").lower()
        print("\n== on-chain spot-check (rpc %s) ==" % rpc)
        try:
            nat = jrpc(rpc, "eth_getBalance", [addr, "latest"])
            print("native balance wei:", int(nat, 16), "(compare with the API's native asset row)")
            code = jrpc(rpc, "eth_getCode", [addr, "latest"])
            print("vault code bytes:", len(code[2:]) // 2,
                  "-> 45 bytes = EIP-1167 minimal proxy (read the implementation address from it)"
                  if len(code[2:]) // 2 == 45 else "")
        except Exception as e:  # noqa: BLE001
            print("rpc error:", e)
        for a in (d.get("assets") or [])[:15]:
            tok = a.get("token") or {}
            ta, dec, bal = tok.get("address"), tok.get("decimals"), a.get("balance")
            if not ta or bal is None:
                continue
            try:
                data = "0x70a08231" + "0" * 24 + addr[2:]
                got = int(eth_call(rpc, ta, data), 16)
                flag = "MATCH" if str(got) == str(bal) else "MISMATCH %s vs %s" % (got, bal)
                print("  %-10s %s  (dec %s)" % (tok.get("symbol"), flag, dec))
            except Exception as e:  # noqa: BLE001
                print("  %-10s eth_call failed: %s" % (tok.get("symbol"), e))
    return 0


if __name__ == "__main__":
    sys.exit(main())
