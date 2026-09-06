// fetch-solana.cjs
// Discover PancakeSwap Solana CLMM positions and farm positions, output pending rewards.
//
// Environment variables:
//   SOL_WALLET  — base58 Solana public key (required)

'use strict'

const {
  getMultipleAccountsInfo,
  PositionInfoLayout,
  parseTokenAccountResp,
  PositionUtils,
  Raydium,
  JupTokenType,
  TickUtils,
  TickArrayLayout,
  API_URLS,
} = require('@pancakeswap/solana-core-sdk')
const { Connection, PublicKey } = require('@solana/web3.js')
const { TOKEN_PROGRAM_ID, TOKEN_2022_PROGRAM_ID } = require('@solana/spl-token')
const BN = require('bn.js')

const address = process.env.SOL_WALLET
const PANCAKE_CLMM_PROGRAM_ID = new PublicKey('HpNfyc2Saw7RKkQd8nEL4khUcuPhQ7WwY1B2qjx8jxFq')
const POSITION_SEED = Buffer.from('position', 'utf8')
const urlConfigs = {
  ...API_URLS,
  BASE_HOST: process.env.NEXT_PUBLIC_EXPLORE_API_ENDPOINT ?? API_URLS.BASE_HOST,
  POOL_LIST: '/cached/v1/pools/info/list',
  MINT_PRICE: '/cached/v1/tokens/price',
  INFO: '/cached/v1/pools/stats/overview',
  POOL_SEARCH_BY_ID: '/cached/v1/pools/info/ids',
  POOL_POSITION_LINE: '/cached/v1/pools/line/position',
  POOL_LIQUIDITY_LINE: '/cached/v1/pools/line/liquidity',
  POOL_TVL_LINE: '/cached/v1/pools/line/tvl',
  POOL_KEY_BY_ID: '/cached/v1/pools/info/ids',
  BIRDEYE_TOKEN_PRICE: '/cached/v1/tokens/birdeye/defi/multi_price',
  TOKEN_LIST: 'https://api-v3.raydium.io/mint/list',
  PCS_TOKEN_LIST: 'https://tokens.pancakeswap.finance/pancakeswap-solana-default.json',
}

async function getTokenBalances(connection, owner) {
  const [solAccountResp, tokenAccountResp, token2022Resp] = await Promise.all([
    connection.getAccountInfo(owner),
    connection.getTokenAccountsByOwner(owner, { programId: TOKEN_PROGRAM_ID }),
    connection.getTokenAccountsByOwner(owner, {
      programId: TOKEN_2022_PROGRAM_ID,
    }),
  ])

  const tokenAccountData = parseTokenAccountResp({
    owner,
    solAccountResp,
    tokenAccountResp: {
      context: tokenAccountResp.context,
      value: [...tokenAccountResp.value, ...token2022Resp.value],
    },
  })

  const tokenAccountMap = new Map()
  tokenAccountData.tokenAccounts.forEach((tokenAccount) => {
    const mintStr = tokenAccount.mint?.toBase58()
    if (!tokenAccountMap.has(mintStr)) {
      tokenAccountMap.set(mintStr, [tokenAccount])
      return
    }
    tokenAccountMap.get(mintStr).push(tokenAccount)
  })

  tokenAccountMap.forEach((tokenAccount) => {
    tokenAccount.sort((a, b) => (a.amount.lt(b.amount) ? 1 : -1))
  })

  return tokenAccountMap
}

async function fetchPoolInfos(poolIds) {
  const timestamp = Date.now()

  const apiBaseUrl = 'https://sol-explorer.pancakeswap.com/api'
  const searchUrl = '/cached/v1/pools/info/ids'
  const response = await fetch(`${apiBaseUrl}${searchUrl}?ids=${poolIds.join(',')}`)

  const poolInfo = await response.json()

  return poolInfo.data.map((pool) => {
    let isFarming = false
    if (pool.rewardDefaultInfos && pool.rewardDefaultInfos.length > 0) {
      isFarming = pool.rewardDefaultInfos.some(
        (reward) => Number(reward.endTime ?? 0) * 1000 > timestamp && reward.perSecond > 0,
      )
    }
    return { ...pool, isFarming }
  })
}

const getTickArrayAddress = (props) =>
  TickUtils.getTickArrayAddressByTick(
    new PublicKey(props.pool.programId),
    new PublicKey(props.pool.id),
    props.tickNumber,
    props.pool.config.tickSpacing,
  )

async function getRewardInfo(connection, raydium, position) {
  const result = await raydium.clmm.getPoolInfoFromRpc(position.poolId)

  const tickArrayLowerAddress = getTickArrayAddress({
    pool: result.poolInfo,
    tickNumber: position.tickLower,
  })
  const tickArrayUpperAddress = getTickArrayAddress({
    pool: result.poolInfo,
    tickNumber: position.tickUpper,
  })

  const tickLowerData = await connection.getAccountInfo(tickArrayLowerAddress)
  const tickUpperData = await connection.getAccountInfo(tickArrayUpperAddress)
  if (!tickLowerData || !tickUpperData) {
    throw new Error('Tick array account not found')
  }

  const tickArrayLower = TickArrayLayout.decode(tickLowerData.data)
  const tickArrayUpper = TickArrayLayout.decode(tickUpperData.data)

  const tickLowerState =
    tickArrayLower.ticks[
      TickUtils.getTickOffsetInArray(position.tickLower, result.computePoolInfo.tickSpacing)
    ]
  const tickUpperState =
    tickArrayUpper.ticks[
      TickUtils.getTickOffsetInArray(position.tickUpper, result.computePoolInfo.tickSpacing)
    ]

  const fees = PositionUtils.GetPositionFeesV2(
    result.computePoolInfo,
    position,
    tickLowerState,
    tickUpperState,
  )
  const rewards = PositionUtils.GetPositionRewardsV2(
    result.computePoolInfo,
    position,
    tickLowerState,
    tickUpperState,
  )

  return {
    feeAmount0: fees.tokenFeeAmountA,
    feeAmount1: fees.tokenFeeAmountB,
    rewardAmounts: rewards,
  }
}

async function main() {
  const owner = new PublicKey(address)
  const connection = new Connection('https://api.mainnet-beta.solana.com', 'confirmed')

  const raydium = await Raydium.load({
    connection,
    owner,
    urlConfigs,
    jupTokenType: JupTokenType.Strict,
    logRequests: false,
    disableFeatureCheck: true,
    disableLoadToken: true,
    loopMultiTxStatus: true,
    blockhashCommitment: 'finalized',
  })

  const tokenAccountData = await getTokenBalances(connection, owner)

  const tokensData = Array.from(tokenAccountData.values())
    .flat()
    .filter((token) => token.amount.eq(new BN(1)))

  const keys = tokensData.map((token) => {
    const [publicKey] = PublicKey.findProgramAddressSync(
      [POSITION_SEED, token.mint.toBuffer()],
      PANCAKE_CLMM_PROGRAM_ID,
    )
    return publicKey
  })

  const res = await getMultipleAccountsInfo(connection, keys)

  const parsedInfo = res
    // .flat()
    .map((info) => {
      if (!info) return null
      return PositionInfoLayout.decode(info.data)
    })
    .filter((info) => !!info)

  const poolInfos = await fetchPoolInfos(parsedInfo.map((i) => i.poolId.toBase58()))

  // Dont parallelize because of rate limits
  const rewardInfos = []
  for (let i = 0; i < parsedInfo.length; i++) {
    const rewardInfo = await getRewardInfo(connection, raydium, parsedInfo[i])
    rewardInfos.push(rewardInfo)
  }

  const positions = parsedInfo
    .map((pos, i) => {
      const poolInfo = poolInfos.find((p) => p.id === pos.poolId.toBase58())
      const rewardInfo = rewardInfos[i]

      // if (rewardInfo.feeAmount0.isZero() && rewardInfo.feeAmount1.isZero()) {
      //   return null;
      // }

      return {
        poolId: pos.poolId.toBase58(),
        token0: poolInfo.mintA.address,
        token1: poolInfo.mintB.address,
        fee: poolInfo.feeRate,
        tokensOwed0: rewardInfo.feeAmount0.toString(),
        tokensOwed1: rewardInfo.feeAmount1.toString(),
        farmReward: rewardInfo.rewardAmounts[0].toString(),
        tickLower: pos.tickLower,
        tickUpper: pos.tickUpper,
        liquidity: pos.liquidity.toString(),
      }
    })
    .filter(Boolean) // Only positions with non-zero amounts

  console.log(JSON.stringify(positions, null, 2))
}

main().catch((err) => {
  console.error(err)
  process.exit(1)
})
