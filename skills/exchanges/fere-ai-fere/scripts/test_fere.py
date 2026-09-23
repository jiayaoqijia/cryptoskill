#!/usr/bin/env python3
"""test_fere.py — <30 s smoke test for the /fere skill. Spends no money.

    python3 scripts/test_fere.py            # offline checks + live read path
    python3 scripts/test_fere.py --offline  # no network (sentinel, key codec, units)

The live path registers a THROWAWAY agent into a temp keyring (free, 200 credits,
no funds), reads chains/credits/holdings/security, and runs one dryrun swap that is
EXPECTED to fail on balance — that failure is the pass condition.
Run this first whenever Fere "seems broken"; it separates their outage from your bug.
"""
from __future__ import annotations

import argparse
import base64
import os
import sys
import tempfile
import time
import uuid
from decimal import Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

FAILS: list[str] = []


def check(name: str, cond: bool, detail: str = "") -> None:
    print(f"{'ok  ' if cond else 'FAIL'} {name}{(' — ' + detail) if detail else ''}")
    if not cond:
        FAILS.append(name)


def offline(fere) -> None:
    fere.assert_sentinel()
    check("evm sentinel is 42 chars of e/E", len(fere.EVM_NATIVE) == 42)
    check("chain table ids", fere.chain("rh")["id"] == 4663
          and fere.chain("sol")["id"] == 7565164 and fere.chain(8453)["name"] == "base")

    seed = os.urandom(32)
    for aid in ("agent_abc123def456", None):
        s = fere.encode_key(seed, aid)
        got_seed, got_id = fere.decode_key(s)
        check(f"key round-trip (agent_id={'yes' if aid else 'no'})",
              got_seed == seed and got_id == aid, f"{len(s)} chars")
    bad = fere.encode_key(seed, "agent_x")
    bad = bad[:-2] + ("aa" if not bad.endswith("aa") else "bb")
    try:
        fere.decode_key(bad)
        check("corrupt key rejected", False)
    except ValueError:
        check("corrupt key rejected", True)

    addr, dec, stable = fere.resolve_token(fere.chain("base"), "USDC")
    check("USDC on Base resolves with 6 decimals", dec == 6 and addr.startswith("0x8335") and stable)
    check("token case is preserved (Solana mints are case-sensitive)",
          fere.resolve_token(fere.chain("solana"), "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")[0]
          == "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v")
    check("native is NOT a dollar stable (so --usd cannot mean token units)",
          fere.resolve_token(fere.chain("base"), "native")[2] is False)
    check("BNB ships no unverified stable shortcut", fere.chain("bnb")["stable"] == {})
    check("sci-notation units parse (holdings send '2.065E-15')",
          fere.hunits({"tokens_bought": "2.065E-15"}) == Decimal("2.065E-15"))
    check("null wei field does not explode (Hyperliquid rows send null)",
          fere.hunits({"tokens_bought": "0.0096", "amount_in_wei_or_lamports": None})
          == Decimal("0.0096"))
    check("holdings key lowercases EVM, keeps Solana case",
          fere.hkey({"chain_id": 8453, "base_address": "0xABC"}) == (8453, "0xabc")
          and fere.hkey({"chain_id": 7565164, "base_address": "So1X"}) == (7565164, "So1X"))


def live(fere) -> None:
    t0 = time.time()
    import httpx
    r = httpx.get(f"{fere.BASE}/v1/chains", trust_env=True, timeout=20)
    ids = {c["chain_id"] for c in r.json().get("chains", [])}
    check("GET /v1/chains (no auth)", r.status_code == 200 and {"8453", "7565164", "4663"} <= ids,
          f"{len(ids)} chains")

    name = f"skilltest-{uuid.uuid4().hex[:8]}"
    seed = os.urandom(32)
    ag = fere.Agent(name, base64.b64encode(seed).decode())
    api = fere.Api(ag)
    reg = fere.body(api.raw("POST", "/v1/auth/register",
                            json={"agent_name": name, "public_key": ag.pub_b64}))
    check("POST /v1/auth/register", bool(reg.get("challenge")))
    ver = fere.body(api.raw("POST", "/v1/auth/verify", json={
        "registration_id": reg["registration_id"], "challenge": reg["challenge"],
        "signature": ag.sign_b64(reg["challenge"])}))
    ag.agent_id = ver.get("agent_id")
    check("POST /v1/auth/verify -> agent_id", bool(ag.agent_id))
    if not ag.agent_id:
        return

    tok = api.bearer()
    check("POST /v1/auth/token -> agt_ bearer", tok.startswith("agt_"))
    w = api.get("/v1/wallets")
    addrs = {x["chain_type"]: x["address"] for x in w.get("wallets", [])}
    check("GET /v1/wallets -> 1 EVM + 1 Solana", {"evm", "solana"} <= set(addrs),
          f"provisioning={w.get('provisioning')}")
    cr = api.get("/v1/credits")
    check("GET /v1/credits", isinstance(cr.get("credits_available"), (int, float)),
          f"{cr.get('credits_available')} on a fresh agent")
    h = api.get("/v1/holdings")
    check("GET /v1/holdings", isinstance(h.get("holdings"), list))
    hr = api.get("/v1/holdings", params=fere.HOLDINGS_REFRESH)
    check("GET /v1/holdings?event=wallet-refresh (fresh read, not the saved answer)",
          hr.get("_status") == 200 and isinstance(hr.get("holdings"), list))
    sec = api.post("/v1/security/check", {"tokens": [
        {"chain_id": 8453, "token_address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"}]})
    st = (sec.get("results") or [{}])[0].get("status")
    check("POST /v1/security/check (Base USDC)", st == "passed", f"status={st}")

    sw = api.post("/v1/swap?wait=true&timeout=90", {
        "chain_id_in": 8453, "chain_id_out": 8453,
        "token_in": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        "token_out": fere.EVM_NATIVE, "amount": "5000000", "dryrun": True})
    task = fere.wait_task(api, sw["task_id"]) if sw.get("task_id") else {}
    err = str((task.get("result") or {}).get("error", ""))
    check("dryrun swap fails on balance (expected on an unfunded agent)",
          "balance validation failed" in err.lower(), err[:70])
    check("'message' is a constant and lies next to a failure",
          sw.get("message") == "Swap task queued successfully" and sw.get("status") == "failure")
    api.close()
    print(f"\nlive path: {time.time() - t0:.1f}s  (throwaway agent {ag.agent_id}, never funded)")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--offline", action="store_true", help="skip every network call")
    a = p.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        os.environ["FERE_HOME"] = tmp          # never touch the real keyring
        import fere
        offline(fere)
        if not a.offline:
            live(fere)
    print("\n" + ("ALL PASS" if not FAILS else f"{len(FAILS)} FAILED: {', '.join(FAILS)}"))
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main())
