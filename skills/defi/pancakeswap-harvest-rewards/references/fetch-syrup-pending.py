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

RPC = 'https://bsc-rpc.publicnode.com'
PENDING_REWARD_SIG = '0xf40f0f52'

def pad_address(addr):
    return addr.lower().replace('0x', '').zfill(64)

def eth_call(to, data):
    r = requests.post(RPC, json={
        'jsonrpc': '2.0', 'id': 1, 'method': 'eth_call',
        'params': [{'to': to, 'data': data}, 'latest']
    }, timeout=15)
    result = r.json().get('result', '0x')
    return result if result and result != '0x' else None

pools_data = requests.get(
    'https://configs.pancakeswap.com/api/data/cached/syrup-pools?chainId=56&isFinished=false',
    timeout=10
).json()
pools = [p for p in pools_data if p['sousId'] != 0]

if not pools:
    print('No active Syrup Pools found.')
    sys.exit(0)

def get_token_price(address):
    try:
        r = requests.get(f'https://api.dexscreener.com/latest/dex/tokens/{address}', timeout=10)
        pairs = r.json().get('pairs', [])
        if pairs:
            return float(pairs[0].get('priceUsd', 0))
    except Exception:
        pass
    return 0

print('| Pool | Earn Token | Pending (raw) | Pending Amount | USD Value |')
print('|------|-----------|--------------|----------------|-----------|')
for pool in pools:
    pool_addr = pool['contractAddress']
    earn_sym = pool['earningToken']['symbol']
    earn_addr = pool['earningToken']['address']
    earn_dec = pool['earningToken']['decimals']
    data = PENDING_REWARD_SIG + pad_address(YOUR_ADDRESS)
    result = eth_call(pool_addr, data)
    raw = int(result, 16) if result else 0
    if raw == 0:
        continue
    amount = raw / (10 ** earn_dec)
    price = get_token_price(earn_addr)
    usd = amount * price if price else 0
    usd_str = f'${usd:.2f}' if price else 'N/A'
    print(f'| CAKE → {earn_sym} | {earn_sym} | {raw} | {amount:.6f} | {usd_str} |')
