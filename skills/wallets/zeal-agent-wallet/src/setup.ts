import {
    existsSync,
    mkdirSync,
    readFileSync,
    writeFileSync,
    chmodSync,
} from 'fs'
import { isAddress, getAddress } from 'viem'
import { generatePrivateKey, privateKeyToAccount } from 'viem/accounts'

import { CONFIG_DIR, WALLET_PATH, CONFIG_PATH } from './constants'

const getArg = (args: string[], flag: string): string | null => {
    const idx = args.indexOf(flag)
    return idx !== -1 && idx + 1 < args.length ? args[idx + 1] : null
}

const parseArgs = (): { safeAddress: `0x${string}` } => {
    const args = process.argv.slice(2)
    const raw = getArg(args, '--safe')

    if (!raw || !isAddress(raw)) {
        console.error('Usage: npm run setup -- --safe <address>')
        process.exit(1)
    }

    return { safeAddress: getAddress(raw) }
}

const loadOrCreateWallet = () => {
    if (existsSync(WALLET_PATH)) {
        const existing = JSON.parse(readFileSync(WALLET_PATH, 'utf-8'))
        console.log('Reusing existing agent wallet.')
        return existing
    }

    const privateKey = generatePrivateKey()
    const account = privateKeyToAccount(privateKey)
    const wallet = { privateKey, address: account.address }

    writeFileSync(WALLET_PATH, JSON.stringify(wallet, null, 2), 'utf-8')
    chmodSync(WALLET_PATH, 0o600)
    console.log('Generated new agent wallet.')
    return wallet
}

const main = () => {
    const { safeAddress } = parseArgs()

    mkdirSync(CONFIG_DIR, { recursive: true })

    const wallet = loadOrCreateWallet()

    writeFileSync(
        CONFIG_PATH,
        JSON.stringify({ safeAddress }, null, 2),
        'utf-8'
    )

    console.log(`Agent address: ${wallet.address}`)
}

main()
