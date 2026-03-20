/**
 * Uniswap V4 Universal Router ABI encoding helpers.
 *
 * Action bytes from official Actions.sol (@uniswap/v4-periphery).
 * Verified against: https://github.com/Uniswap/v4-periphery/blob/main/src/libraries/Actions.sol
 *
 * Fixes C-02 from PhD review: SETTLE_ALL = 0x0c (not 0x0b).
 */

import { AbiCoder, keccak256 } from "ethers";

const abi = AbiCoder.defaultAbiCoder();

// ── V4 Action Constants (from Actions.sol) ──────────────────────────
export const Actions = {
  SWAP_EXACT_IN_SINGLE:  0x06,
  SWAP_EXACT_IN:         0x07,
  SWAP_EXACT_OUT_SINGLE: 0x08,
  SWAP_EXACT_OUT:        0x09,
  DONATE:                0x0a,
  SETTLE:                0x0b,
  SETTLE_ALL:            0x0c,
  SETTLE_PAIR:           0x0d,
  TAKE:                  0x0e,
  TAKE_ALL:              0x0f,
  TAKE_PORTION:          0x10,
  TAKE_PAIR:             0x11,
  CLOSE_CURRENCY:        0x12,
  CLEAR_OR_TAKE:         0x13,
  SWEEP:                 0x14,
  WRAP:                  0x15,
  UNWRAP:                0x16,
} as const;

// ── Universal Router Command ────────────────────────────────────────
/** V4_SWAP command byte for Universal Router execute(). */
export const UR_COMMAND_V4_SWAP = 0x10;

// ── PoolKey Types ───────────────────────────────────────────────────
export interface PoolKey {
  currency0: string;
  currency1: string;
  fee: number;
  tickSpacing: number;
  hooks: string;
}

const ADDRESS_ZERO = "0x0000000000000000000000000000000000000000";

/**
 * Compute V4 Pool ID = keccak256(abi.encode(PoolKey)).
 */
export function computePoolId(key: PoolKey): string {
  const encoded = abi.encode(
    ["address", "address", "uint24", "int24", "address"],
    [key.currency0, key.currency1, key.fee, key.tickSpacing, key.hooks]
  );
  return keccak256(encoded);
}

/**
 * Encode SWAP_EXACT_IN_SINGLE params.
 *
 * Solidity struct:
 *   (PoolKey poolKey, bool zeroForOne, uint128 amountIn, uint128 amountOutMinimum, bytes hookData)
 */
export function encodeSwapExactInSingle(
  key: PoolKey,
  zeroForOne: boolean,
  amountIn: bigint,
  amountOutMin: bigint,
  hookData: string = "0x"
): string {
  return abi.encode(
    ["(address,address,uint24,int24,address)", "bool", "uint128", "uint128", "bytes"],
    [
      [key.currency0, key.currency1, key.fee, key.tickSpacing, key.hooks],
      zeroForOne,
      amountIn,
      amountOutMin,
      hookData,
    ]
  );
}

/**
 * Encode SETTLE_ALL params: (Currency currency, uint256 maxAmount).
 */
export function encodeSettleAll(currency: string, maxAmount: bigint): string {
  return abi.encode(["address", "uint256"], [currency, maxAmount]);
}

/**
 * Encode TAKE_ALL params: (Currency currency, uint256 minAmount).
 */
export function encodeTakeAll(currency: string, minAmount: bigint): string {
  return abi.encode(["address", "uint256"], [currency, minAmount]);
}

/**
 * Encode TAKE params: (Currency currency, address recipient, uint256 amount).
 *
 * Note: setting amount=0 (ActionConstants.OPEN_DELTA) takes the full positive delta
 * for that currency.
 */
export function encodeTake(
  currency: string,
  recipient: string,
  amount: bigint
): string {
  return abi.encode(["address", "address", "uint256"], [currency, recipient, amount]);
}

/**
 * Build complete V4_SWAP input for Universal Router execute().
 *
 * Default action sequence: SWAP_EXACT_IN_SINGLE + SETTLE_ALL + TAKE_ALL
 *
 * For custom recipients, use TAKE (amount=0 = OPEN_DELTA) to take the full credit
 * owed to the router and send it to `recipient`.
 */
export function buildV4SwapInput(
  key: PoolKey,
  zeroForOne: boolean,
  amountIn: bigint,
  amountOutMin: bigint,
  recipient?: string
): string {
  // Actions:
  // - default: 0x06 (SWAP_EXACT_IN_SINGLE) + 0x0c (SETTLE_ALL) + 0x0f (TAKE_ALL)
  // - custom recipient: 0x06 + 0x0c + 0x0e (TAKE)
  const actions = recipient ? "0x060c0e" : "0x060c0f";

  // Determine settle/take currencies based on swap direction
  const settleCurrency = zeroForOne ? key.currency0 : key.currency1;
  const takeCurrency = zeroForOne ? key.currency1 : key.currency0;

  const swapParams = encodeSwapExactInSingle(
    key,
    zeroForOne,
    amountIn,
    amountOutMin
  );
  const settleParams = encodeSettleAll(settleCurrency, amountIn);
  const takeParams = recipient
    ? encodeTake(takeCurrency, recipient, 0n)
    : encodeTakeAll(takeCurrency, amountOutMin);

  // Encode V4_SWAP input: (bytes actions, bytes[] params)
  return abi.encode(
    ["bytes", "bytes[]"],
    [actions, [swapParams, settleParams, takeParams]]
  );
}

/**
 * Build full Universal Router execute() calldata.
 * commands = 0x10 (V4_SWAP), inputs = [v4SwapInput], deadline = timestamp.
 */
export function buildExecuteCalldata(
  key: PoolKey,
  zeroForOne: boolean,
  amountIn: bigint,
  amountOutMin: bigint,
  deadline: bigint,
  recipient?: string
): { commands: string; inputs: string[]; deadline: bigint } {
  const v4Input = buildV4SwapInput(key, zeroForOne, amountIn, amountOutMin, recipient);
  return {
    commands: "0x10",
    inputs: [v4Input],
    deadline,
  };
}

/**
 * Encode QuoteExactSingleParams for V4Quoter.quoteExactInputSingle().
 *
 * struct QuoteExactSingleParams {
 *   PoolKey poolKey;
 *   bool zeroForOne;
 *   uint128 exactAmount;
 *   bytes hookData;
 * }
 */
export function encodeQuoteExactInputSingle(
  key: PoolKey,
  zeroForOne: boolean,
  exactAmount: bigint
): string {
  return abi.encode(
    ["(address,address,uint24,int24,address)", "bool", "uint128", "bytes"],
    [
      [key.currency0, key.currency1, key.fee, key.tickSpacing, key.hooks],
      zeroForOne,
      exactAmount,
      "0x",
    ]
  );
}

/**
 * Decode packed Slot0 from a bytes32 value (from extsload or StateView).
 *
 * Layout (LSB-first):
 *   uint160 sqrtPriceX96   bits 0-159
 *   int24   tick            bits 160-183
 *   uint24  protocolFee     bits 184-207
 *   uint24  lpFee           bits 208-231
 */
export function decodeSlot0(raw: bigint): {
  sqrtPriceX96: bigint;
  tick: number;
  protocolFee: number;
  lpFee: number;
} {
  const sqrtPriceX96 = raw & ((1n << 160n) - 1n);
  let tickRaw = Number((raw >> 160n) & ((1n << 24n) - 1n));
  if (tickRaw >= 1 << 23) tickRaw -= 1 << 24; // sign extension
  const protocolFee = Number((raw >> 184n) & ((1n << 24n) - 1n));
  const lpFee = Number((raw >> 208n) & ((1n << 24n) - 1n));
  return { sqrtPriceX96, tick: tickRaw, protocolFee, lpFee };
}

/**
 * Compute storage slot for pool state in PoolManager.
 * slot = keccak256(abi.encode(poolId, POOLS_MAPPING_SLOT))
 * POOLS_MAPPING_SLOT = 6 (verified against StateLibrary.sol).
 */
export function computePoolStateSlot(poolId: string): string {
  const POOLS_MAPPING_SLOT = 6;
  const encoded = abi.encode(["bytes32", "uint256"], [poolId, POOLS_MAPPING_SLOT]);
  return keccak256(encoded);
}

/**
 * Build a default PoolKey with hooks = address(0).
 */
export function makePoolKey(
  currency0: string,
  currency1: string,
  fee: number,
  tickSpacing: number,
  hooks: string = ADDRESS_ZERO
): PoolKey {
  return { currency0, currency1, fee, tickSpacing, hooks };
}
