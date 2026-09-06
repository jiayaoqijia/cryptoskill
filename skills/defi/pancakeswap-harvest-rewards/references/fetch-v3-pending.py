import json, sys, os
try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'requests'])
    import requests

YOUR_ADDRESS = os.environ.get('YOUR_ADDRESS', '')
if not YOUR_ADDRESS or not YOUR_ADDRESS.startswith('0x') or len(YOUR_ADDRESS) != 42:
    print('ERROR: Set YOUR_ADDRESS env var to a valid 0x address')
    sys.exit(1)

CHAIN_CONFIGS = {
    'bsc':     ('https://bsc-rpc.publicnode.com',          '0x556B9306565093C855AEA9AE92A594704c2Cd59e'),
    'eth':     ('https://ethereum-rpc.publicnode.com',     '0x556B9306565093C855AEA9AE92A594704c2Cd59e'),
    'arbitrum':('https://arb1.arbitrum.io/rpc',            '0x5e09ACf80C0296740eC5d6F643005a4ef8DaA694'),
    'base':    ('https://mainnet.base.org',                '0xC6A2Db661D5a5690172d8eB0a7DEA2d3008665A3'),
    'zksync':  ('https://mainnet.era.zksync.io',           '0x4c615E78c5fCA1Ad31e4d66eb0D8688d84307463'),
    'zkevm':   ('https://zkevm-rpc.com',                   '0xe9c7f3196ab8c09f6616365e8873daeb207c0391'),
    'linea':   ('https://rpc.linea.build',                 '0x22E2f236065B780FA33EC8C4E58b99ebc8B55c57'),
}

CHAIN = os.environ.get('CHAIN', 'bsc').lower()
if CHAIN not in CHAIN_CONFIGS:
    print(f'ERROR: Unknown chain "{CHAIN}". Valid options: {", ".join(CHAIN_CONFIGS)}')
    sys.exit(1)

RPC, MASTERCHEF_V3 = CHAIN_CONFIGS[CHAIN]

print(f'Chain: {CHAIN}')

def eth_call(to, data):
    r = requests.post(RPC, json={
        'jsonrpc': '2.0', 'id': 1, 'method': 'eth_call',
        'params': [{'to': to, 'data': data}, 'latest']
    }, timeout=15)
    result = r.json().get('result', '0x')
    return result if result and result != '0x' else None

def pad_address(addr):
    return addr.lower().replace('0x', '').zfill(64)

def pad_uint(n):
    return hex(n).replace('0x', '').zfill(64)

# Get balance of V3 positions staked in MasterChef v3
bal_result = eth_call(MASTERCHEF_V3, '0x70a08231' + pad_address(YOUR_ADDRESS))
balance = int(bal_result, 16) if bal_result else 0

print(f'V3 positions staked in MasterChef v3: {balance}')
if balance == 0:
    print('No V3 positions staked.')
    sys.exit(0)

# Enumerate token IDs via tokenOfOwnerByIndex
token_ids = []
for i in range(balance):
    data = '0x2f745c59' + pad_address(YOUR_ADDRESS) + pad_uint(i)
    result = eth_call(MASTERCHEF_V3, data)
    if result:
        token_ids.append(int(result, 16))

# Query pendingCake for each token ID
cake_price = 0
try:
    r = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=pancakeswap-token&vs_currencies=usd', timeout=5)
    cake_price = r.json().get('pancakeswap-token', {}).get('usd', 0)
except Exception:
    pass

print()
print('| Token ID | Pending CAKE (wei) | Pending CAKE | USD Value |')
print('|----------|-------------------|--------------|-----------|')
for token_id in token_ids:
    # pendingCake
    result = eth_call(MASTERCHEF_V3, '0xce5f39c6' + pad_uint(token_id))
    pending_wei = int(result, 16) if result else 0
    pending_cake = pending_wei / 1e18
    if pending_cake <= 0:
        continue
    usd = pending_cake * cake_price if cake_price else 0
    usd_str = f'${usd:.2f}' if cake_price else 'N/A'
    print(f'| {token_id} | {pending_wei} | {pending_cake:.6f} CAKE | {usd_str} |')
