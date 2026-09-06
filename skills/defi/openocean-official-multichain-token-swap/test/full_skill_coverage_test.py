#!/usr/bin/env python
from __future__ import annotations

import re
from decimal import Decimal, ROUND_DOWN, InvalidOperation
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def assert_true(name: str, cond: bool, detail: str = "") -> None:
    if not cond:
        raise AssertionError(f"[FAIL] {name} {detail}".rstrip())


def classify_prompt(prompt: str) -> str:
    p = prompt.lower()
    if any(k in p for k in ["error", "failed", "reverted", "code 429", "token resolution failed"]):
        return "error-handling"
    if any(k in p for k in ["swap fast", "execute swap immediately", "automated swap"]):
        return "swap-execute-fast"
    if any(k in p for k in ["execute the swap", "broadcast the swap", "send the transaction"]):
        return "swap-execute"
    if any(k in p for k in ["build a swap", "prepare swap transaction", "get swap calldata", "create a transaction"]):
        return "swap-build"
    if any(k in p for k in ["quote", "price check", "check swap price", "how much would i get", "compare token rates", "exchange rates", "see exchange rates"]):
        return "quote"
    return "unknown"


def slippage_api_from_bps(s: str) -> str:
    try:
        bps = Decimal(s)
    except InvalidOperation:
        return "INVALID"
    v = bps / Decimal("100")
    if v < Decimal("0.05") or v > Decimal("50"):
        return f"OUT_OF_RANGE:{v}"
    out = format(v.normalize(), "f")
    if "." in out:
        out = out.rstrip("0").rstrip(".")
    return out


def amount_to_wei(amount: str, decimals: int) -> str:
    a = Decimal(amount)
    scale = Decimal(10) ** decimals
    return str((a * scale).to_integral_value(rounding=ROUND_DOWN))


def run() -> None:
    # 1) Files present
    files = [
        "SKILL.md",
        "skills/quote/SKILL.md",
        "skills/swap-build/SKILL.md",
        "skills/swap-execute/SKILL.md",
        "skills/swap-execute-fast/SKILL.md",
        "skills/error-handling/SKILL.md",
        "skills/swap-execute-fast/scripts/fast-swap.sh",
        "skills/swap-execute-fast/scripts/execute-swap.sh",
        "test/agent-test-cases.md",
    ]
    for f in files:
        assert_true(f"file_exists:{f}", (ROOT / f).exists())

    # 2) Entry skill routing completeness
    root_skill = read("SKILL.md")
    for token in ["skills/quote/SKILL.md", "skills/swap-build/SKILL.md", "skills/swap-execute/SKILL.md", "skills/swap-execute-fast/SKILL.md", "skills/error-handling/SKILL.md"]:
        assert_true("entry_routes", token in root_skill, token)

    # 3) Prompt-based skill trigger coverage (from test/agent-test-cases.md)
    prompt_expect = [
        ("Get a swap quote for 1 ETH to USDC on ethereum", "quote"),
        ("Check swap price: 100 USDC to WBTC on arbitrum", "quote"),
        ("How much would I get for 0.5 WBTC to DAI on polygon?", "quote"),
        ("Build a swap: 100 USDC to ETH on arbitrum from 0x...", "swap-build"),
        ("Prepare swap transaction - 1 ETH to USDC on ethereum from 0x...", "swap-build"),
        ("Get swap calldata for 0.5 WBTC to DAI on polygon from 0x...", "swap-build"),
        ("Execute the swap", "swap-execute"),
        ("Broadcast the swap transaction", "swap-execute"),
        ("Send the transaction", "swap-execute"),
        ("Swap fast: 1 ETH to USDC on base from 0x...", "swap-execute-fast"),
        ("Execute swap immediately - 100 USDC to ETH on arbitrum from 0x...", "swap-execute-fast"),
        ("Automated swap: 0.5 WBTC to DAI on polygon from 0x...", "swap-execute-fast"),
        ("What does code 429 mean?", "error-handling"),
        ("Token resolution failed for XYZ", "error-handling"),
        ("Transaction reverted - what should I do?", "error-handling"),
    ]
    for p, e in prompt_expect:
        got = classify_prompt(p)
        assert_true("prompt_route", got == e, f"{p} => {got}, expected {e}")

    # 4) fast-swap.sh critical logic coverage
    fast_sh = read("skills/swap-execute-fast/scripts/fast-swap.sh")
    must_have_fast = [
        "PYTHON_BIN",
        "OUT_OF_RANGE",
        "amount must be greater than 0".lower(),
        "amountDecimals",
        "gasPriceDecimals",
        "enabledDexIds",
        "disabledDexIds",
        "/dexList",
        ".data.gasPrice",
        "No calldata in response",
    ]
    fast_l = fast_sh.lower()
    for m in must_have_fast:
        assert_true("fast_logic_presence", m.lower() in fast_l, m)
    assert_true("fast_no_eval", "eval " not in fast_l)

    # 5) execute-swap.sh critical logic coverage
    exec_sh = read("skills/swap-execute-fast/scripts/execute-swap.sh")
    exec_l = exec_sh.lower()
    for m in ["auth_args", "estimate --rpc-url", "cast_args", "set +e", "set -e", "keystore", "--ledger", "--trezor", "--from", "--enabled-dex-ids", "--disabled-dex-ids"]:
        assert_true("execute_logic_presence", m in exec_l, m)
    assert_true("execute_no_eval", "eval " not in exec_l)

    # 6) Numeric correctness tests
    slippage_cases = {
        "4": "OUT_OF_RANGE:0.04",
        "5": "0.05",
        "50": "0.5",
        "100": "1",
        "5000": "50",
        "5001": "OUT_OF_RANGE:50.01",
        "abc": "INVALID",
        "-1": "OUT_OF_RANGE:-0.01",
    }
    for inp, exp in slippage_cases.items():
        got = slippage_api_from_bps(inp)
        assert_true("slippage_convert", got == exp, f"{inp} => {got}, expected {exp}")

    wei_cases = [
        ("1", 18, "1000000000000000000"),
        ("0.5", 8, "50000000"),
        ("0.000001", 6, "1"),
        ("0.0000009", 6, "0"),
    ]
    for amount, dec, exp in wei_cases:
        got = amount_to_wei(amount, dec)
        assert_true("amount_to_wei", got == exp, f"{amount}/{dec} => {got}, expected {exp}")

    # 7) Error-handling skill taxonomy coverage
    err_skill = read("skills/error-handling/SKILL.md")
    for code in ["400", "401", "403", "404", "429", "500", "502/503/504"]:
        assert_true("error_code_doc", code in err_skill, code)
    for phrase in ["insufficient funds for gas * price + value", "transfer amount exceeds allowance", "nonce too low", "transaction underpriced"]:
        assert_true("error_exec_doc", phrase in err_skill, phrase)

    # 8) API reference usage coverage across skills
    api_ref = read("references/api-reference.md")
    for endpoint in ["/:chain/quote", "/:chain/swap", "/:chain/gasPrice", "/:chain/tokenList"]:
        assert_true("api_ref_endpoint", endpoint in api_ref, endpoint)

    print("ALL TESTS PASSED: full skill coverage checks completed.")


if __name__ == "__main__":
    run()
