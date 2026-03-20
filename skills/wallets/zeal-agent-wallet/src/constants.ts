import { join } from 'path'
import { homedir } from 'os'

export const ZEAL_API_BASE = 'https://api.zeal.app'

export const CONFIG_DIR = join(homedir(), '.zeal-agent-wallet')
export const WALLET_PATH = join(CONFIG_DIR, 'wallet.json')
export const CONFIG_PATH = join(CONFIG_DIR, 'config.json')
