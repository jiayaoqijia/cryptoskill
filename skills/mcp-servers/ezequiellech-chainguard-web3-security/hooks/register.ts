import type { Register } from 'claude-code'

const RAW_EVM_KEY_NET_RE = /(?:curl|wget|nc|http)\b[^\n]*(?:0x[a-fA-F0-9]{64})/
const RAW_CLI_PRIVKEY_RE = /--private-key\s+0x[a-fA-F0-9]{64}/
const MAX_ERC20_APPROVE_RE = /095ea7b3[0-9a-fA-F]{64}f{64}/i
const TROJAN_BIDI_RE = /[\u202A-\u202E\u2066-\u2069]/
const ZERO_WIDTH_RE = /[\u200B-\u200D\uFEFF]/

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const r = await next(e)
    $.ui.log(`chainguard-web3-firewall active in ${e.cwd}`)
    return r
  })

  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    const cmd = typeof e.command === 'string' ? e.command : ''
    if (TROJAN_BIDI_RE.test(cmd) || ZERO_WIDTH_RE.test(cmd)) {
      return { deny: 'ChainGuard blocked hidden zero-width or Trojan-Source Unicode in Bash command.' }
    }
    if (RAW_EVM_KEY_NET_RE.test(cmd)) {
      return { deny: 'ChainGuard blocked potential raw EVM private key exfiltration over network.' }
    }
    if (RAW_CLI_PRIVKEY_RE.test(cmd)) {
      return { deny: 'ChainGuard blocked plaintext --private-key flag; use encrypted Foundry keystore (--account).' }
    }
    if (MAX_ERC20_APPROVE_RE.test(cmd)) {
      return { deny: 'ChainGuard blocked unlimited ERC-20 max approve calldata; scope allowance to exact amount.' }
    }
    return next(e)
  })
}
