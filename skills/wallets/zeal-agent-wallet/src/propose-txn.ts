import { readFileSync } from 'fs'
import { dirname, join } from 'path'
import { fileURLToPath } from 'url'
import {
    encodeAbiParameters,
    encodePacked,
    getAddress,
    isAddress,
    isHex,
    keccak256,
    parseAbiParameters,
} from 'viem'
import { privateKeyToAccount } from 'viem/accounts'

import { CONFIG_PATH, WALLET_PATH, ZEAL_API_BASE } from './constants'

type Network = {
    name: string
    safeNetworkId: string
    chainId: number
}

const SAFE_TX_TYPEHASH = keccak256(
    encodePacked(
        ['string'],
        [
            'SafeTx(address to,uint256 value,bytes data,uint8 operation,uint256 safeTxGas,uint256 baseGas,uint256 gasPrice,address gasToken,address refundReceiver,uint256 nonce)',
        ]
    )
)

const DOMAIN_SEPARATOR_TYPEHASH = keccak256(
    encodePacked(
        ['string'],
        ['EIP712Domain(uint256 chainId,address verifyingContract)']
    )
)

const ZERO_ADDRESS = '0x0000000000000000000000000000000000000000' as const

const getArg = (args: string[], flag: string): string | null => {
    const idx = args.indexOf(flag)
    return idx !== -1 && idx + 1 < args.length ? args[idx + 1] : null
}

const loadNetworks = (): Network[] => {
    const scriptDir =
        typeof __dirname !== 'undefined'
            ? __dirname
            : dirname(fileURLToPath(import.meta.url))

    const networksPath = join(scriptDir, '..', 'networks.json')
    const file: {
        networks: Network[]
    } = JSON.parse(readFileSync(networksPath, 'utf-8'))
    return file.networks
}

const parseArgs = () => {
    const args = process.argv.slice(2)

    const toRaw = getArg(args, '--to')
    if (!toRaw || !isAddress(toRaw)) {
        console.error('--to must be a valid address')
        process.exit(1)
    }

    const value = getArg(args, '--value')
    if (!value) {
        console.error('--value is required (in wei)')
        process.exit(1)
    }

    const data = getArg(args, '--data')
    if (!data || !isHex(data)) {
        console.error('--data is required (hex-encoded)')
        process.exit(1)
    }

    const network = getArg(args, '--network')
    if (!network) {
        console.error('--network is required')
        process.exit(1)
    }

    const operationStr = getArg(args, '--operation')
    if (!operationStr || (operationStr !== '0' && operationStr !== '1')) {
        console.error(
            '--operation is required (0 for Call, 1 for DelegateCall)'
        )
        process.exit(1)
    }

    const operation = operationStr === '1' ? (1 as const) : (0 as const)

    const origin = getArg(args, '--origin')
    if (!origin) {
        console.error('--origin is required (description of the transaction)')
        process.exit(1)
    }
    if (origin.length > 200) {
        console.error('--origin must be 200 characters or fewer')
        process.exit(1)
    }

    return {
        to: getAddress(toRaw),
        value,
        data: data as `0x${string}`,
        network,
        operation,
        origin,
    }
}

const computeDomainSeparator = (
    chainId: number,
    safeAddress: `0x${string}`
): `0x${string}` => {
    return keccak256(
        encodeAbiParameters(parseAbiParameters('bytes32, uint256, address'), [
            DOMAIN_SEPARATOR_TYPEHASH,
            BigInt(chainId),
            safeAddress,
        ])
    )
}

const computeSafeTxHash = (
    domainSeparator: `0x${string}`,
    params: {
        to: `0x${string}`
        value: bigint
        data: `0x${string}`
        operation: number
        safeTxGas: bigint
        baseGas: bigint
        gasPrice: bigint
        gasToken: `0x${string}`
        refundReceiver: `0x${string}`
        nonce: bigint
    }
): `0x${string}` => {
    const safeTxHashData = keccak256(
        encodeAbiParameters(
            parseAbiParameters(
                'bytes32, address, uint256, bytes32, uint8, uint256, uint256, uint256, address, address, uint256'
            ),
            [
                SAFE_TX_TYPEHASH,
                params.to,
                params.value,
                keccak256(params.data),
                params.operation,
                params.safeTxGas,
                params.baseGas,
                params.gasPrice,
                params.gasToken,
                params.refundReceiver,
                params.nonce,
            ]
        )
    )

    return keccak256(
        encodePacked(
            ['bytes1', 'bytes1', 'bytes32', 'bytes32'],
            ['0x19', '0x01', domainSeparator, safeTxHashData]
        )
    )
}

const fetchNonce = async (
    safeNetworkId: string,
    safeAddress: `0x${string}`
): Promise<bigint> => {
    const url = `${ZEAL_API_BASE}/proxy/stxs/${safeNetworkId}/api/v1/safes/${safeAddress}/multisig-transactions/?limit=1&ordering=-nonce`
    const res = await fetch(url)

    if (!res.ok) {
        throw new Error(
            `Failed to fetch transactions: ${res.status} ${res.statusText}`
        )
    }

    const body = (await res.json()) as { results: { nonce: number }[] }

    if (body.results.length === 0) {
        return 0n
    }

    return BigInt(body.results[0].nonce) + 1n
}

const submitTransactionProposal = async (params: {
    safeNetworkId: string
    safeAddress: `0x${string}`
    to: `0x${string}`
    value: string
    data: `0x${string}`
    operation: number
    safeTxGas: string
    baseGas: string
    gasPrice: string
    gasToken: string
    refundReceiver: string
    nonce: string
    safeTxHash: string
    sender: string
    signature: string
    origin: string
}): Promise<void> => {
    const url = `${ZEAL_API_BASE}/api/safe-tx/${params.safeNetworkId}/propose/${params.safeAddress}`

    const body = {
        to: params.to,
        value: params.value,
        data: params.data,
        operation: params.operation,
        safeTxGas: params.safeTxGas,
        baseGas: params.baseGas,
        gasPrice: params.gasPrice,
        gasToken: params.gasToken,
        refundReceiver: params.refundReceiver,
        nonce: params.nonce,
        contractTransactionHash: params.safeTxHash,
        sender: params.sender,
        signature: params.signature,
        origin: params.origin,
    }

    const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    })

    if (!res.ok) {
        const text = await res.text()
        throw new Error(
            `Failed to submit transaction: ${res.status} ${res.statusText}\n${text}`
        )
    }
}

const main = async () => {
    const parsedArgs = parseArgs()

    const config = JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'))
    const wallet = JSON.parse(readFileSync(WALLET_PATH, 'utf-8'))
    const networks = loadNetworks()

    const network = networks.find((n) => n.name === parsedArgs.network)

    if (!network) {
        const available = networks.map((n) => n.name).join(', ')
        console.error(
            `Unknown network "${parsedArgs.network}". Available: ${available}`
        )
        process.exit(1)
    }

    const safeAddress = getAddress(config.safeAddress)
    const account = privateKeyToAccount(wallet.privateKey)

    const nonce = await fetchNonce(network.safeNetworkId, safeAddress)

    const txParams = {
        to: parsedArgs.to,
        value: BigInt(parsedArgs.value),
        data: parsedArgs.data,
        operation: parsedArgs.operation,
        safeTxGas: 0n,
        baseGas: 0n,
        gasPrice: 0n,
        gasToken: ZERO_ADDRESS,
        refundReceiver: ZERO_ADDRESS,
        nonce,
    }

    const domainSeparator = computeDomainSeparator(network.chainId, safeAddress)
    const safeTxHash = computeSafeTxHash(domainSeparator, txParams)

    const signature = await account.signMessage({
        message: { raw: safeTxHash },
    })

    // Adjust v value for Safe's expected format (add 4 to v for eth_sign)
    const sigBytes = Buffer.from(signature.slice(2), 'hex')
    sigBytes[64] = sigBytes[64] + 4
    const adjustedSignature = `0x${sigBytes.toString('hex')}` as `0x${string}`

    await submitTransactionProposal({
        safeNetworkId: network.safeNetworkId,
        safeAddress,
        to: txParams.to,
        value: txParams.value.toString(),
        data: txParams.data,
        operation: txParams.operation,
        safeTxGas: '0',
        baseGas: '0',
        gasPrice: '0',
        gasToken: ZERO_ADDRESS,
        refundReceiver: ZERO_ADDRESS,
        nonce: nonce.toString(),
        safeTxHash,
        sender: account.address,
        signature: adjustedSignature,
        origin: parsedArgs.origin,
    })

    console.log(`Transaction proposed successfully.`)
    console.log(`  Safe: ${safeAddress}`)
    console.log(`  Network: ${network.name}`)
    console.log(`  Nonce: ${nonce}`)
    console.log(`  SafeTxHash: ${safeTxHash}`)
}

main().catch((err) => {
    console.error(err)
    process.exit(1)
})
