/**
 * Unit tests for validation module.
 * Tests input validation, BigInt parsing, address checks, slippage.
 */
import { describe, it, expect } from "vitest";
import {
  validateAddress,
  resolveTokenInput,
  parseAmount,
  parseSlippage,
  validateChain,
  applySlippage,
  sortCurrencies,
} from "../../src/lib/validation.js";

describe("validateAddress", () => {
  it("accepts valid checksummed address", () => {
    expect(validateAddress("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", "token")).toBe(
      "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
    );
  });

  it("accepts valid lowercase address", () => {
    expect(validateAddress("0x0000000000000000000000000000000000000000", "token")).toBe(
      "0x0000000000000000000000000000000000000000"
    );
  });

  it("rejects too short", () => {
    expect(() => validateAddress("0x833589fCD6eDb", "token")).toThrow("valid Ethereum address");
  });

  it("rejects too long", () => {
    expect(() =>
      validateAddress("0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913DEAD", "token")
    ).toThrow("valid Ethereum address");
  });

  it("rejects no 0x prefix", () => {
    expect(() =>
      validateAddress("833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", "token")
    ).toThrow("valid Ethereum address");
  });

  it("rejects injection attempts", () => {
    expect(() => validateAddress("0x$(touch /tmp/pwned)000000000000000000", "token")).toThrow();
    expect(() => validateAddress("foo;rm -rf /", "token")).toThrow();
  });
});

describe("resolveTokenInput", () => {
  it("ETH → address(0)", () => {
    expect(resolveTokenInput("ETH", "t")).toBe(
      "0x0000000000000000000000000000000000000000"
    );
  });

  it("eth (lowercase) → address(0)", () => {
    expect(resolveTokenInput("eth", "t")).toBe(
      "0x0000000000000000000000000000000000000000"
    );
  });

  it("0x0 → address(0)", () => {
    expect(resolveTokenInput("0x0", "t")).toBe(
      "0x0000000000000000000000000000000000000000"
    );
  });

  it("valid address passes through", () => {
    const addr = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
    expect(resolveTokenInput(addr, "t")).toBe(addr);
  });
});

describe("parseAmount", () => {
  it("parses valid integer", () => {
    expect(parseAmount("1000000000000000000", "amount")).toBe(1000000000000000000n);
  });

  it("parses 1", () => {
    expect(parseAmount("1", "amount")).toBe(1n);
  });

  it("rejects zero", () => {
    expect(() => parseAmount("0", "amount")).toThrow("> 0");
  });

  it("rejects decimal", () => {
    expect(() => parseAmount("0.01", "amount")).toThrow("non-negative integer");
  });

  it("rejects scientific notation", () => {
    expect(() => parseAmount("1e18", "amount")).toThrow("non-negative integer");
  });

  it("rejects negative", () => {
    expect(() => parseAmount("-1", "amount")).toThrow("non-negative integer");
  });

  it("rejects injection: bash arithmetic", () => {
    expect(() => parseAmount("a[$(touch /tmp/pwned)]", "amount")).toThrow(
      "non-negative integer"
    );
  });

  it("rejects values > uint128 max", () => {
    const tooBig = ((1n << 128n)).toString();
    expect(() => parseAmount(tooBig, "amount")).toThrow("uint128 max");
  });

  it("accepts uint128 max", () => {
    const max = ((1n << 128n) - 1n).toString();
    expect(parseAmount(max, "amount")).toBe((1n << 128n) - 1n);
  });
});

describe("parseSlippage", () => {
  it("parses 50 (0.5%)", () => {
    expect(parseSlippage("50")).toBe(50);
  });

  it("parses 0 (no slippage)", () => {
    expect(parseSlippage("0")).toBe(0);
  });

  it("rejects > 10000", () => {
    expect(() => parseSlippage("10001")).toThrow("0-10000");
  });

  it("rejects non-integer", () => {
    expect(() => parseSlippage("abc")).toThrow("non-negative integer");
  });

  it("rejects injection", () => {
    expect(() => parseSlippage("a[$(id)]")).toThrow("non-negative integer");
  });
});

describe("validateChain", () => {
  it("accepts base", () => expect(validateChain("base")).toBe("base"));
  it("accepts ethereum", () => expect(validateChain("ethereum")).toBe("ethereum"));
  it("accepts base-sepolia", () => expect(validateChain("base-sepolia")).toBe("base-sepolia"));
  it("rejects solana", () => expect(() => validateChain("solana")).toThrow("Unsupported chain"));
  it("rejects empty", () => expect(() => validateChain("")).toThrow("Unsupported chain"));
});

describe("applySlippage", () => {
  it("50 bps = 0.5% slippage", () => {
    // 1000 * (10000-50) / 10000 = 995
    expect(applySlippage(1000n, 50)).toBe(995n);
  });

  it("100 bps = 1% slippage", () => {
    expect(applySlippage(10000n, 100)).toBe(9900n);
  });

  it("returns ≥ 1 for small nonzero amounts", () => {
    expect(applySlippage(1n, 50)).toBe(1n);
  });

  it("returns 0 for zero input", () => {
    expect(applySlippage(0n, 50)).toBe(0n);
  });

  it("handles large amounts without overflow (BigInt)", () => {
    const big = 10n ** 30n;
    const result = applySlippage(big, 50);
    const expected = (big * 9950n) / 10000n;
    expect(result).toBe(expected);
  });
});

describe("sortCurrencies", () => {
  const ADDR_ZERO = "0x0000000000000000000000000000000000000000";
  const USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";

  it("ETH (address(0)) < USDC → zeroForOne=true when tokenIn=ETH", () => {
    const { currency0, currency1, zeroForOne } = sortCurrencies(ADDR_ZERO, USDC);
    expect(currency0).toBe(ADDR_ZERO);
    expect(currency1).toBe(USDC);
    expect(zeroForOne).toBe(true);
  });

  it("USDC → ETH: zeroForOne=false when tokenIn=USDC", () => {
    const { currency0, currency1, zeroForOne } = sortCurrencies(USDC, ADDR_ZERO);
    expect(currency0).toBe(ADDR_ZERO);
    expect(currency1).toBe(USDC);
    expect(zeroForOne).toBe(false);
  });

  it("rejects same token", () => {
    expect(() => sortCurrencies(USDC, USDC)).toThrow("different");
  });
});
