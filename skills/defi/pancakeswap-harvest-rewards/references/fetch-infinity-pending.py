import json, sys, os, time
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

CHAIN_IDS = {'bsc': 56, 'base': 8453}

DISTRIBUTOR = {
    56:   '0xEA8620aAb2F07a0ae710442590D649ADE8440877',
    8453: '0xEA8620aAb2F07a0ae710442590D649ADE8440877',
}
RPC = {
    56:   'https://bsc-dataseed.binance.org/',
    8453: 'https://mainnet.base.org',
}

CHAIN = os.environ.get('CHAIN', 'bsc').lower()
if CHAIN not in CHAIN_IDS:
    print(f'ERROR: Infinity farms are only available on: {", ".join(CHAIN_IDS)}')
    sys.exit(1)

CHAIN_ID = CHAIN_IDS[CHAIN]
CURRENT_TS = int(time.time())


def get_claimed(rpc_url, contract, token_addr, user_addr):
    selector = '0xc253b5da' # claimedAmounts
    pad = lambda a: a[2:].lower().zfill(64)
    data = selector + pad(token_addr) + pad(user_addr)
    payload = {
        'jsonrpc': '2.0', 'id': 1, 'method': 'eth_call',
        'params': [{'to': contract, 'data': data}, 'latest']
    }
    r = requests.post(rpc_url, json=payload, timeout=15)
    r.raise_for_status()
    result = r.json().get('result', '0x0')
    return int(result, 16)

print(f'Chain: {CHAIN} (chain ID {CHAIN_ID})')
print(f'Wallet: {YOUR_ADDRESS}')
print()

url = f'https://infinity.pancakeswap.com/farms/users/{CHAIN_ID}/{YOUR_ADDRESS}/{CURRENT_TS}'
try:
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    data = r.json()
except Exception as e:
    print(f'ERROR: Failed to fetch Infinity rewards: {e}')
    sys.exit(1)

claims = data.get('rewards', [])
if not claims:
    print('No claimable Infinity rewards found.')
    sys.exit(0)

distributor = DISTRIBUTOR[CHAIN_ID]
rpc_url = RPC[CHAIN_ID]

print('| Reward Token | Pending Amount (wei) | Merkle Proof Available |')
print('|--------------|----------------------|------------------------|')
for c in claims:
    token = c.get('rewardTokenAddress', '?')
    total = int(c.get('totalRewardAmount', 0))
    claimed = get_claimed(rpc_url, distributor, token, YOUR_ADDRESS)
    pending = total - claimed
    if pending <= 0:
        continue
    print(f'| {token} | {pending} | Yes |')
