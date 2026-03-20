/**
 * Unit tests for V4 encoding helpers.
 * Tests pool ID computation, action bytes, ABI encoding correctness.
 */
import { describe, it, expect } from "vitest";
import { keccak256, AbiCoder } from "ethers";
import {
  computePoolId,
  makePoolKey,
  Actions,
  decodeSlot0,
  computePoolStateSlot,
  encodeSwapExactInSingle,
  encodeSettleAll,
  encodeTakeAll,
  encodeTake,
  buildV4SwapInput,
} from "../../src/lib/v4-encoding.js";

const abi = AbiCoder.defaultAbiCoder();
const ADDR_ZERO = "0x0000000000000000000000000000000000000000";
const USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
const RECIPIENT = "0x1111111111111111111111111111111111111111";

describe("Actions constants", () => {
  // Verified against official Actions.sol from @uniswap/v4-periphery
  it("SWAP_EXACT_IN_SINGLE = 0x06", () => expect(Actions.SWAP_EXACT_IN_SINGLE).toBe(0x06));
  it("SWAP_EXACT_IN = 0x07", () => expect(Actions.SWAP_EXACT_IN).toBe(0x07));
  it("SWAP_EXACT_OUT_SINGLE = 0x08", () => expect(Actions.SWAP_EXACT_OUT_SINGLE).toBe(0x08));
  it("SETTLE = 0x0b (NOT SETTLE_ALL)", () => expect(Actions.SETTLE).toBe(0x0b));
  it("SETTLE_ALL = 0x0c (NOT SETTLE)", () => expect(Actions.SETTLE_ALL).toBe(0x0c));
  it("TAKE = 0x0e", () => expect(Actions.TAKE).toBe(0x0e));
  it("TAKE_ALL = 0x0f", () => expect(Actions.TAKE_ALL).toBe(0x0f));
  it("WRAP = 0x15", () => expect(Actions.WRAP).toBe(0x15));
  it("UNWRAP = 0x16", () => expect(Actions.UNWRAP).toBe(0x16));
});

describe("computePoolId", () => {
  it("computes correct pool ID for ETH/USDC fee=500 ts=10", () => {
    const key = makePoolKey(ADDR_ZERO, USDC, 500, 10);
    const poolId = computePoolId(key);

    // Manual computation for verification
    const encoded = abi.encode(
      ["address", "address", "uint24", "int24", "address"],
      [ADDR_ZERO, USDC, 500, 10, ADDR_ZERO]
    );
    const expected = keccak256(encoded);
    expect(poolId).toBe(expected);
  });

  it("different fee → different pool ID", () => {
    const id1 = computePoolId(makePoolKey(ADDR_ZERO, USDC, 500, 10));
    const id2 = computePoolId(makePoolKey(ADDR_ZERO, USDC, 3000, 60));
    expect(id1).not.toBe(id2);
  });

  it("pool ID is 32 bytes hex", () => {
    const id = computePoolId(makePoolKey(ADDR_ZERO, USDC, 500, 10));
    expect(id).toMatch(/^0x[0-9a-f]{64}$/);
  });
});

describe("computePoolStateSlot", () => {
  it("uses mapping slot 6 (verified against StateLibrary.sol)", () => {
    const poolId = computePoolId(makePoolKey(ADDR_ZERO, USDC, 500, 10));
    const slot = computePoolStateSlot(poolId);

    const encoded = abi.encode(["bytes32", "uint256"], [poolId, 6]);
    const expected = keccak256(encoded);
    expect(slot).toBe(expected);
  });

  it("returns 32 bytes hex", () => {
    const poolId = "0x" + "ab".repeat(32);
    const slot = computePoolStateSlot(poolId);
    expect(slot).toMatch(/^0x[0-9a-f]{64}$/);
  });
});

describe("decodeSlot0", () => {
  it("decodes zero as empty pool", () => {
    const { sqrtPriceX96, tick, protocolFee, lpFee } = decodeSlot0(0n);
    expect(sqrtPriceX96).toBe(0n);
    expect(tick).toBe(0);
    expect(protocolFee).toBe(0);
    expect(lpFee).toBe(0);
  });

  it("decodes positive tick correctly", () => {
    // sqrtPriceX96=1000, tick=100, protocolFee=0, lpFee=500
    const sqrtPrice = 1000n;
    const tickVal = 100n;
    const lpFeeVal = 500n;
    const packed = sqrtPrice | (tickVal << 160n) | (lpFeeVal << 208n);
    const { sqrtPriceX96, tick, lpFee } = decodeSlot0(packed);
    expect(sqrtPriceX96).toBe(1000n);
    expect(tick).toBe(100);
    expect(lpFee).toBe(500);
  });

  it("decodes negative tick (sign extension from int24)", () => {
    // tick = -200006 stored as two's complement in 24 bits
    const tickRaw = (1 << 24) + (-200006); // two's complement
    const packed = BigInt(tickRaw) << 160n;
    const { tick } = decodeSlot0(packed);
    expect(tick).toBe(-200006);
  });
});

describe("encodeSwapExactInSingle", () => {
  it("produces non-empty bytes", () => {
    const key = makePoolKey(ADDR_ZERO, USDC, 500, 10);
    const encoded = encodeSwapExactInSingle(key, true, 10n ** 16n, 0n);
    expect(encoded.length).toBeGreaterThan(2);
    expect(encoded.startsWith("0x")).toBe(true);
  });

  it("is decodable", () => {
    const key = makePoolKey(ADDR_ZERO, USDC, 500, 10);
    const encoded = encodeSwapExactInSingle(key, true, 10n ** 16n, 100n);
    // Should be valid ABI encoding — decode should not throw
    const decoded = abi.decode(
      ["(address,address,uint24,int24,address)", "bool", "uint128", "uint128", "bytes"],
      encoded
    );
    expect(decoded[1]).toBe(true); // zeroForOne
    expect(decoded[2]).toBe(10n ** 16n); // amountIn
    expect(decoded[3]).toBe(100n); // amountOutMin
  });
});

describe("encodeSettleAll / encodeTakeAll", () => {
  it("encodeSettleAll produces valid encoding", () => {
    const encoded = encodeSettleAll(ADDR_ZERO, 10n ** 18n);
    const decoded = abi.decode(["address", "uint256"], encoded);
    expect(decoded[0]).toBe(ADDR_ZERO);
    expect(decoded[1]).toBe(10n ** 18n);
  });

  it("encodeTakeAll produces valid encoding", () => {
    const encoded = encodeTakeAll(USDC, 25000000n); // 25 USDC
    const decoded = abi.decode(["address", "uint256"], encoded);
    expect(decoded[0]).toBe(USDC);
    expect(decoded[1]).toBe(25000000n);
  });
});

describe("buildV4SwapInput", () => {
  it("builds decodable V4 swap input", () => {
    const key = makePoolKey(ADDR_ZERO, USDC, 500, 10);
    const input = buildV4SwapInput(key, true, 10n ** 16n, 25000000n);

    // Outer encoding: (bytes actions, bytes[] params)
    const decoded = abi.decode(["bytes", "bytes[]"], input);
    const actions = decoded[0] as string;
    const params = decoded[1] as string[];

    // Actions should be 0x060c0f
    expect(actions).toBe("0x060c0f");

    // Should have 3 param entries
    expect(params.length).toBe(3);
  });

  it("settle currency matches swap direction (zeroForOne=true → settle currency0)", () => {
    const key = makePoolKey(ADDR_ZERO, USDC, 500, 10);
    const input = buildV4SwapInput(key, true, 10n ** 16n, 25000000n);
    const decoded = abi.decode(["bytes", "bytes[]"], input);
    const params = decoded[1] as string[];

    // Second param = SETTLE_ALL: should be currency0 (ADDR_ZERO for ETH→USDC)
    const settleDecoded = abi.decode(["address", "uint256"], params[1]);
    expect(settleDecoded[0]).toBe(ADDR_ZERO);

    // Third param = TAKE_ALL: should be currency1 (USDC)
    const takeDecoded = abi.decode(["address", "uint256"], params[2]);
    expect(takeDecoded[0]).toBe(USDC);
  });

  it("settle currency matches swap direction (zeroForOne=false → settle currency1)", () => {
    const key = makePoolKey(ADDR_ZERO, USDC, 500, 10);
    const input = buildV4SwapInput(key, false, 25000000n, 10n ** 16n);
    const decoded = abi.decode(["bytes", "bytes[]"], input);
    const params = decoded[1] as string[];

    // zeroForOne=false means USDC→ETH, settle currency1 (USDC), take currency0 (ETH)
    const settleDecoded = abi.decode(["address", "uint256"], params[1]);
    expect(settleDecoded[0]).toBe(USDC);
  });
});

describe("encodeTake", () => {
  it("produces valid ABI encoding with currency, recipient, amount", () => {
    const encoded = encodeTake(USDC, RECIPIENT, 25000000n);
    const decoded = abi.decode(["address", "address", "uint256"], encoded);
    expect(decoded[0]).toBe(USDC);
    expect(decoded[1]).toBe(RECIPIENT);
    expect(decoded[2]).toBe(25000000n);
  });

  it("encodes amount=0 (OPEN_DELTA) correctly", () => {
    const encoded = encodeTake(ADDR_ZERO, RECIPIENT, 0n);
    const decoded = abi.decode(["address", "address", "uint256"], encoded);
    expect(decoded[0]).toBe(ADDR_ZERO);
    expect(decoded[1]).toBe(RECIPIENT);
    expect(decoded[2]).toBe(0n);
  });
});

describe("buildV4SwapInput with recipient", () => {
  it("uses TAKE_ALL (0x060c0f) when no recipient specified", () => {
    const key = makePoolKey(ADDR_ZERO, USDC, 500, 10);
    const input = buildV4SwapInput(key, true, 10n ** 16n, 25000000n);
    const decoded = abi.decode(["bytes", "bytes[]"], input);
    expect(decoded[0]).toBe("0x060c0f");
  });

  it("uses TAKE (0x060c0e) when recipient specified", () => {
    const key = makePoolKey(ADDR_ZERO, USDC, 500, 10);
    const input = buildV4SwapInput(key, true, 10n ** 16n, 25000000n, RECIPIENT);
    const decoded = abi.decode(["bytes", "bytes[]"], input);
    expect(decoded[0]).toBe("0x060c0e");
  });

  it("TAKE params include recipient and amount=0 (OPEN_DELTA)", () => {
    const key = makePoolKey(ADDR_ZERO, USDC, 500, 10);
    const input = buildV4SwapInput(key, true, 10n ** 16n, 25000000n, RECIPIENT);
    const decoded = abi.decode(["bytes", "bytes[]"], input);
    const params = decoded[1] as string[];

    // Third param = TAKE: (currency, recipient, amount=0)
    const takeDecoded = abi.decode(["address", "address", "uint256"], params[2]);
    expect(takeDecoded[0]).toBe(USDC); // take currency (output)
    expect(takeDecoded[1]).toBe(RECIPIENT);
    expect(takeDecoded[2]).toBe(0n); // OPEN_DELTA
  });

  it("TAKE_ALL params use minAmount when no recipient", () => {
    const key = makePoolKey(ADDR_ZERO, USDC, 500, 10);
    const input = buildV4SwapInput(key, true, 10n ** 16n, 25000000n);
    const decoded = abi.decode(["bytes", "bytes[]"], input);
    const params = decoded[1] as string[];

    const takeDecoded = abi.decode(["address", "uint256"], params[2]);
    expect(takeDecoded[0]).toBe(USDC);
    expect(takeDecoded[1]).toBe(25000000n);
  });
});

describe("makePoolKey", () => {
  it("defaults hooks to address(0)", () => {
    const key = makePoolKey(ADDR_ZERO, USDC, 500, 10);
    expect(key.hooks).toBe(ADDR_ZERO);
  });

  it("accepts custom hooks", () => {
    const hook = "0x1234567890123456789012345678901234567890";
    const key = makePoolKey(ADDR_ZERO, USDC, 500, 10, hook);
    expect(key.hooks).toBe(hook);
  });
});
