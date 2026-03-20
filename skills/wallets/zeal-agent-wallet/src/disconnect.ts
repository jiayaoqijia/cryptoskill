import { existsSync, unlinkSync } from 'fs'

import { CONFIG_PATH } from './constants'

const main = () => {
    if (!existsSync(CONFIG_PATH)) {
        console.log('No Safe configuration found. Already disconnected.')
        return
    }

    unlinkSync(CONFIG_PATH)
    console.log('Disconnected. Safe configuration removed.')
    console.log('Run setup again to connect to a Safe.')
}

main()
