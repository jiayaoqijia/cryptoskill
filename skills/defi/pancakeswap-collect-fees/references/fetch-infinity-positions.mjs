// fetch-infinity-positions.mjs
// Fetch all PancakeSwap Infinity (v4) CL and Bin positions for a wallet,
// compute pending fees for CL positions, and compute token amounts for Bin positions.
//
// Environment variables:
//   WALLET    — 0x wallet address (required)
//   CHAIN_ID  — numeric chain ID (required)
//   RPC       — JSON-RPC endpoint URL (required)

import {
  CLPoolManagerAbi,
  CLPositionManagerAbi,
  INFI_CL_POOL_MANAGER_ADDRESSES,
  INFI_CL_POSITION_MANAGER_ADDRESSES,
} from '@pancakeswap/infinity-sdk'
import { createPublicClient, encodeAbiParameters, http, keccak256 } from 'viem'
import { base, bsc } from 'viem/chains'

// ─── Chain config ────────────────────────────────────────────────────────────

const CHAIN_MAP = {
  56: bsc,
  8453: base,
}

const CHAIN_NAME_MAP = {
  56: 'bsc',
  8453: 'base',
}

const chainId = Number(process.env.CHAIN_ID)
const chain = CHAIN_MAP[chainId]
if (!chain) {
  const supported = Object.keys(CHAIN_MAP).join(', ')
  throw new Error(`Unsupported CHAIN_ID: ${chainId}. Supported chain IDs: ${supported}`)
}

const chainName = CHAIN_NAME_MAP[chainId]

const WALLET = process.env.WALLET
if (!/^0x[0-9a-fA-F]{40}$/.test(WALLET)) {
  throw new Error(`Invalid WALLET address: ${WALLET}`)
}

const RPC = process.env.RPC

// ─── Contract addresses (same on BSC and Base) ────────────────────────────────

const CL_POSITION_MANAGER = INFI_CL_POSITION_MANAGER_ADDRESSES[chainId]
const CL_POOL_MANAGER = INFI_CL_POOL_MANAGER_ADDRESSES[chainId]

// ─── Utilities ────────────────────────────────────────────────────────────────

const Q128 = 2n ** 128n
const MOD = 2n ** 256n

function computePoolId(poolKey) {
  // keccak256 of ABI-encoded poolKey (6 slots: currency0, currency1, hooks, poolManager, fee, bytes32 parameters)
  return keccak256(
    encodeAbiParameters(
      [
        { name: 'currency0', type: 'address' },
        { name: 'currency1', type: 'address' },
        { name: 'hooks', type: 'address' },
        { name: 'poolManager', type: 'address' },
        { name: 'fee', type: 'uint24' },
        { name: 'parameters', type: 'bytes32' },
      ],
      [
        poolKey.currency0,
        poolKey.currency1,
        poolKey.hooks,
        poolKey.poolManager,
        poolKey.fee,
        poolKey.parameters,
      ],
    ),
  )
}

function feeGrowthInside(fgGlobal, fgOutLower, fgOutUpper, tickLower, tickUpper, currentTick) {
  const fgBelow = currentTick >= tickLower ? fgOutLower : (fgGlobal - fgOutLower + MOD) % MOD
  const fgAbove = currentTick < tickUpper ? fgOutUpper : (fgGlobal - fgOutUpper + MOD) % MOD
  return (fgGlobal - fgBelow - fgAbove + MOD * 2n) % MOD
}

// ─── Explorer API pagination ──────────────────────────────────────────────────

async function fetchAllPages(urlBase) {
  const rows = []
  let after = ''
  do {
    const url = `${urlBase}?before=&after=${after}`
    const res = await fetch(url)
    if (!res.ok) throw new Error(`Explorer API error ${res.status}: ${url}`)
    const data = await res.json()
    rows.push(...(data.rows ?? []))
    if (!data.hasNextPage) break
    after = data.endCursor ?? ''
  } while (true)
  return rows
}

// ─── Main ─────────────────────────────────────────────────────────────────────

const client = createPublicClient({ chain, transport: http(RPC) })
const EXPLORER = 'https://explorer.pancakeswap.com/api/cached/pools/positions'

// ── Part 1: CL Positions ──────────────────────────────────────────────────────

const clRows = await fetchAllPages(`${EXPLORER}/infinityCl/${chainName}/${WALLET}`)
const activeCLRows = clRows.filter((r) => r.liquidity !== '0')

const clPositions = []

if (activeCLRows.length > 0) {
  // Fetch on-chain position data for each tokenId
  const posResults = await client.multicall({
    contracts: activeCLRows.map((row) => ({
      address: CL_POSITION_MANAGER,
      abi: CLPositionManagerAbi,
      functionName: 'positions',
      args: [BigInt(row.id)],
    })),
  })

  // Collect unique pool IDs and their positions data
  const poolIdToPositions = new Map() // poolId -> [{ rowIdx, posData }]
  const positionData = []

  for (let i = 0; i < posResults.length; i++) {
    const result = posResults[i]
    if (result.status !== 'success') continue
    const pos = result.result
    const poolKey = pos[0]
    const poolId = computePoolId(poolKey)
    positionData.push({ rowIdx: i, pos, poolId, poolKey })
    if (!poolIdToPositions.has(poolId)) {
      poolIdToPositions.set(poolId, [])
    }
    poolIdToPositions.get(poolId).push(positionData.length - 1)
  }

  // Batch pool-level reads per unique pool (getFeeGrowthGlobals, getSlot0)
  // plus per-position tick reads (getPoolTickInfo for tickLower and tickUpper)
  const uniquePoolIds = [...poolIdToPositions.keys()]

  const poolCalls = uniquePoolIds.flatMap((poolId) => [
    {
      address: CL_POOL_MANAGER,
      abi: CLPoolManagerAbi,
      functionName: 'getFeeGrowthGlobals',
      args: [poolId],
    },
    {
      address: CL_POOL_MANAGER,
      abi: CLPoolManagerAbi,
      functionName: 'getSlot0',
      args: [poolId],
    },
  ])

  const tickCalls = positionData.flatMap((pd) => [
    {
      address: CL_POOL_MANAGER,
      abi: CLPoolManagerAbi,
      functionName: 'getPoolTickInfo',
      args: [pd.poolId, pd.pos[1]], // tickLower
    },
    {
      address: CL_POOL_MANAGER,
      abi: CLPoolManagerAbi,
      functionName: 'getPoolTickInfo',
      args: [pd.poolId, pd.pos[2]], // tickUpper
    },
  ])

  const [poolResults, tickResults] = await Promise.all([
    client.multicall({ contracts: poolCalls }),
    client.multicall({ contracts: tickCalls }),
  ])

  // Build poolId -> { fgGlobal0, fgGlobal1, currentTick } map
  const poolState = new Map()
  for (let i = 0; i < uniquePoolIds.length; i++) {
    const fgResult = poolResults[i * 2]
    const slot0Result = poolResults[i * 2 + 1]
    if (fgResult.status !== 'success' || slot0Result.status !== 'success') continue
    const [fg0, fg1] = fgResult.result
    const currentTick = slot0Result.result[1]
    poolState.set(uniquePoolIds[i], { fg0, fg1, currentTick })
  }

  // Compute pending fees for each position
  for (let i = 0; i < positionData.length; i++) {
    const { rowIdx, pos, poolId } = positionData[i]
    const state = poolState.get(poolId)
    if (!state) continue

    const tickLowerResult = tickResults[i * 2]
    const tickUpperResult = tickResults[i * 2 + 1]
    if (tickLowerResult.status !== 'success' || tickUpperResult.status !== 'success') continue

    console.log('tick results', tickLowerResult, tickUpperResult)

    const { feeGrowthOutside0X128: fgOutLower0, feeGrowthOutside1X128: fgOutLower1 } =
      tickLowerResult.result
    const { feeGrowthOutside0X128: fgOutUpper0, feeGrowthOutside1X128: fgOutUpper1 } =
      tickUpperResult.result

    const poolKey = pos[0]
    const tickLower = pos[1]
    const tickUpper = pos[2]
    const liquidity = pos[3]
    const fg0InsideLast = pos[4]
    const fg1InsideLast = pos[5]

    const fg0Inside = feeGrowthInside(
      state.fg0,
      fgOutLower0,
      fgOutUpper0,
      tickLower,
      tickUpper,
      state.currentTick,
    )
    const fg1Inside = feeGrowthInside(
      state.fg1,
      fgOutLower1,
      fgOutUpper1,
      tickLower,
      tickUpper,
      state.currentTick,
    )

    const pending0 = (((fg0Inside - fg0InsideLast + MOD) % MOD) * liquidity) / Q128
    const pending1 = (((fg1Inside - fg1InsideLast + MOD) % MOD) * liquidity) / Q128

    const row = activeCLRows[rowIdx]
    clPositions.push({
      id: row.id,
      token0: poolKey.currency0,
      token1: poolKey.currency1,
      tickLower: Number(tickLower),
      tickUpper: Number(tickUpper),
      liquidity: liquidity.toString(),
      pending0: pending0.toString(),
      pending1: pending1.toString(),
    })
  }
}

// ── Part 2: Bin Positions ─────────────────────────────────────────────────────
// The Explorer API returns per-bin reserve and share data directly — no on-chain
// calls are needed. Each row represents one pool; reserveOfBins[] contains the
// per-bin breakdown including userSharesOfBin.

const binRows = await fetchAllPages(`${EXPLORER}/infinityBin/${chainName}/poolsByOwner/${WALLET}`)

// Fetch pool metadata (token0/token1) for each unique poolId in parallel
const uniqueBinPoolIds = [...new Set(binRows.map((r) => r.poolId))]
const poolMetaResults = await Promise.all(
  uniqueBinPoolIds.map((poolId) =>
    fetch(`https://explorer.pancakeswap.com/api/cached/pools/infinityBin/${chainName}/${poolId}`)
      .then((r) => (r.ok ? r.json() : null))
      .catch(() => null),
  ),
)
const binPoolMeta = new Map()
for (let i = 0; i < uniqueBinPoolIds.length; i++) {
  const meta = poolMetaResults[i]
  binPoolMeta.set(uniqueBinPoolIds[i], {
    token0: meta?.token0?.id ?? null,
    token1: meta?.token1?.id ?? null,
  })
}

const binPositions = []

for (const row of binRows) {
  const poolId = row.poolId
  const { token0, token1 } = binPoolMeta.get(poolId) ?? {
    token0: null,
    token1: null,
  }

  for (const bin of row.reserveOfBins ?? []) {
    const userShares = BigInt(bin.userSharesOfBin ?? '0')
    if (userShares === 0n) continue

    const totalShares = BigInt(bin.totalShares)
    const reserveX = BigInt(bin.reserveX)
    const reserveY = BigInt(bin.reserveY)

    const amountX = totalShares > 0n ? (userShares * reserveX) / totalShares : 0n
    const amountY = totalShares > 0n ? (userShares * reserveY) / totalShares : 0n

    binPositions.push({
      poolId,
      token0,
      token1,
      binId: bin.binId,
      share: userShares.toString(),
      amountX: amountX.toString(),
      amountY: amountY.toString(),
    })
  }
}

// ── Output ────────────────────────────────────────────────────────────────────

console.log(JSON.stringify({ clPositions, binPositions }))
