#!/usr/bin/env python3
"""
v4_read.py — Read Uniswap V4 pool state via extsload on PoolManager.
Usage:
  python3 v4_read.py pool-info --token0 <addr> --token1 <addr> [--fee 3000] [--tick-spacing 60] [--chain base] [--rpc <url>]
  python3 v4_read.py find-pool --token0 <addr> --token1 <addr> [--chain base]
"""
import subprocess, json, sys, argparse

ADDR_ZERO = "0x" + "0" * 40

CHAINS = {
    "base": {
        "pool_manager": "0x498581fF718922c3f8e6A244956aF099B2652b2b",
        "rpc": "https://mainnet.base.org",
    },
    "ethereum": {
        "pool_manager": "0x000000000004444c5dc75cB358380D2e3dE08A90",
        "rpc": "https://eth.llamarpc.com",
    },
}

# Pool mapping slot in PoolManager storage
POOLS_MAPPING_SLOT = 6

# Common fee tiers: (fee, tickSpacing)
FEE_TIERS = [
    (500, 10),
    (3000, 60),
    (10000, 200),
    (100, 1),
    (8388608, 200),  # dynamic fee
]


def cast(*args, rpc=None):
    """Run a cast command and return stdout."""
    cmd = ["cast"] + list(args)
    if rpc:
        cmd += ["--rpc-url", rpc]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
    if r.returncode != 0:
        return None
    return r.stdout.strip()


def sort_tokens(t0, t1):
    """Sort tokens by address (V4 requirement: currency0 < currency1)."""
    if t0.lower() < t1.lower():
        return t0, t1
    return t1, t0


def compute_pool_id(currency0, currency1, fee, tick_spacing, hooks=ADDR_ZERO):
    """Compute V4 pool ID = keccak256(abi.encode(PoolKey))."""
    encoded = cast(
        "abi-encode",
        "f(address,address,uint24,int24,address)",
        currency0, currency1, str(fee), str(tick_spacing), hooks,
    )
    if not encoded:
        return None
    return cast("keccak", encoded)


def compute_state_slot(pool_id, mapping_slot=POOLS_MAPPING_SLOT):
    """Compute storage slot for pool state = keccak256(poolId . mappingSlot)."""
    encoded = cast("abi-encode", "f(bytes32,uint256)", pool_id, str(mapping_slot))
    if not encoded:
        return None
    return cast("keccak", encoded)


def read_extsload(pool_manager, slot, rpc):
    """Read a storage slot via extsload on the PoolManager."""
    result = cast(
        "call", pool_manager,
        "extsload(bytes32)(bytes32)",
        slot,
        rpc=rpc,
    )
    return result


def decode_slot0(raw_hex):
    """
    Decode packed Slot0 from a bytes32.
    Slot0 layout (LSB first):
      uint160 sqrtPriceX96   (bits 0-159)
      int24   tick           (bits 160-183)
      uint24  protocolFee    (bits 184-207)
      uint24  lpFee          (bits 208-231)
    """
    val = int(raw_hex, 16)
    sqrt_price = val & ((1 << 160) - 1)
    tick_raw = (val >> 160) & ((1 << 24) - 1)
    tick = tick_raw if tick_raw < (1 << 23) else tick_raw - (1 << 24)
    protocol_fee = (val >> 184) & ((1 << 24) - 1)
    lp_fee = (val >> 208) & ((1 << 24) - 1)
    return {
        "sqrtPriceX96": str(sqrt_price),
        "tick": tick,
        "protocolFee": protocol_fee,
        "lpFee": lp_fee,
    }


def read_liquidity(pool_manager, pool_id_slot, rpc):
    """Read liquidity from Pool.State (offset +3 from base slot in storage)."""
    # Pool.State layout: slot0(1) + feeGrowthGlobal0(1) + feeGrowthGlobal1(1) + liquidity(1)
    base = int(pool_id_slot, 16)
    liq_slot = hex(base + 3)
    raw = read_extsload(pool_manager, liq_slot, rpc)
    if not raw:
        return "0"
    return str(int(raw, 16))


def get_token_info(token, rpc):
    """Get symbol and decimals for a token."""
    if token == ADDR_ZERO:
        return {"symbol": "ETH", "decimals": 18}
    sym = cast("call", token, "symbol()(string)", rpc=rpc) or "???"
    sym = sym.strip().strip('"')
    dec = cast("call", token, "decimals()(uint8)", rpc=rpc) or "18"
    try:
        dec = int(dec)
    except ValueError:
        dec = 18
    return {"symbol": sym, "decimals": dec}


def find_pool(token0, token1, chain_cfg, hooks=ADDR_ZERO):
    """Try common fee tiers and return the first pool found."""
    c0, c1 = sort_tokens(token0, token1)
    rpc = chain_cfg["rpc"]
    pm = chain_cfg["pool_manager"]

    for fee, ts in FEE_TIERS:
        pool_id = compute_pool_id(c0, c1, fee, ts, hooks)
        if not pool_id:
            continue
        state_slot = compute_state_slot(pool_id)
        if not state_slot:
            continue
        raw = read_extsload(pm, state_slot, rpc)
        if not raw or int(raw, 16) == 0:
            continue
        slot0 = decode_slot0(raw)
        if int(slot0["sqrtPriceX96"]) == 0:
            continue
        liquidity = read_liquidity(pm, state_slot, rpc)
        return {
            "poolId": pool_id,
            "currency0": c0,
            "currency1": c1,
            "fee": fee,
            "tickSpacing": ts,
            "hooks": hooks,
            "slot0": slot0,
            "liquidity": liquidity,
        }
    return None


def cmd_pool_info(args):
    chain_cfg = CHAINS[args.chain]
    if args.rpc:
        chain_cfg = {**chain_cfg, "rpc": args.rpc}

    t0 = ADDR_ZERO if args.token0.lower() in ("eth", "0x0") else args.token0
    t1 = ADDR_ZERO if args.token1.lower() in ("eth", "0x0") else args.token1

    if args.fee and args.tick_spacing:
        c0, c1 = sort_tokens(t0, t1)
        pool_id = compute_pool_id(c0, c1, args.fee, args.tick_spacing, args.hooks or ADDR_ZERO)
        if not pool_id:
            print(json.dumps({"success": False, "error": "Failed to compute pool ID"}))
            sys.exit(1)
        state_slot = compute_state_slot(pool_id)
        raw = read_extsload(chain_cfg["pool_manager"], state_slot, chain_cfg["rpc"])
        if not raw or int(raw, 16) == 0:
            print(json.dumps({"success": False, "error": "Pool not found or empty"}))
            sys.exit(1)
        slot0 = decode_slot0(raw)
        liquidity = read_liquidity(chain_cfg["pool_manager"], state_slot, chain_cfg["rpc"])
        result = {
            "poolId": pool_id,
            "currency0": c0,
            "currency1": c1,
            "fee": args.fee,
            "tickSpacing": args.tick_spacing,
            "hooks": args.hooks or ADDR_ZERO,
            "slot0": slot0,
            "liquidity": liquidity,
        }
    else:
        result = find_pool(t0, t1, chain_cfg, args.hooks or ADDR_ZERO)
        if not result:
            print(json.dumps({"success": False, "error": "No pool found for this pair"}))
            sys.exit(1)

    # Add token info
    rpc = chain_cfg["rpc"]
    t0_info = get_token_info(result["currency0"], rpc)
    t1_info = get_token_info(result["currency1"], rpc)

    output = {
        "success": True,
        "chain": args.chain,
        "poolId": result["poolId"],
        "token0": {**t0_info, "address": result["currency0"]},
        "token1": {**t1_info, "address": result["currency1"]},
        "fee": result["fee"],
        "tickSpacing": result["tickSpacing"],
        "hooks": result["hooks"],
        **result["slot0"],
        "liquidity": result["liquidity"],
    }
    print(json.dumps(output, indent=2))


def cmd_find_pool(args):
    chain_cfg = CHAINS[args.chain]
    if args.rpc:
        chain_cfg = {**chain_cfg, "rpc": args.rpc}

    t0 = ADDR_ZERO if args.token0.lower() in ("eth", "0x0") else args.token0
    t1 = ADDR_ZERO if args.token1.lower() in ("eth", "0x0") else args.token1
    c0, c1 = sort_tokens(t0, t1)
    rpc = chain_cfg["rpc"]
    pm = chain_cfg["pool_manager"]

    pools = []
    for fee, ts in FEE_TIERS:
        pool_id = compute_pool_id(c0, c1, fee, ts)
        if not pool_id:
            continue
        state_slot = compute_state_slot(pool_id)
        if not state_slot:
            continue
        raw = read_extsload(pm, state_slot, rpc)
        if not raw or int(raw, 16) == 0:
            continue
        slot0 = decode_slot0(raw)
        if int(slot0["sqrtPriceX96"]) == 0:
            continue
        liquidity = read_liquidity(pm, state_slot, rpc)
        pools.append({
            "poolId": pool_id,
            "fee": fee,
            "tickSpacing": ts,
            "liquidity": liquidity,
            **slot0,
        })

    print(json.dumps({"success": True, "chain": args.chain, "pools": pools}, indent=2))


if __name__ == "__main__":
    import os
    os.environ["PATH"] = os.path.expanduser("~/.foundry/bin") + ":" + os.environ.get("PATH", "")

    parser = argparse.ArgumentParser(description="Uniswap V4 pool reader")
    sub = parser.add_subparsers(dest="command")

    p_info = sub.add_parser("pool-info", help="Get pool state")
    p_info.add_argument("--token0", required=True)
    p_info.add_argument("--token1", required=True)
    p_info.add_argument("--fee", type=int)
    p_info.add_argument("--tick-spacing", type=int)
    p_info.add_argument("--hooks")
    p_info.add_argument("--chain", default="base")
    p_info.add_argument("--rpc")

    p_find = sub.add_parser("find-pool", help="Find all pools for a pair")
    p_find.add_argument("--token0", required=True)
    p_find.add_argument("--token1", required=True)
    p_find.add_argument("--chain", default="base")
    p_find.add_argument("--rpc")

    args = parser.parse_args()
    if args.command == "pool-info":
        cmd_pool_info(args)
    elif args.command == "find-pool":
        cmd_find_pool(args)
    else:
        parser.print_help()
        sys.exit(1)
