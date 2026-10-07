#!/usr/bin/env python3
"""MEXC spot minimal client. Signing: HMAC-SHA256 over the urlencoded query string."""
import hashlib, hmac, http.client, json, os, time, urllib.parse

HOST = 'api.mexc.com'

def load_creds(path=None):
    path = path or os.environ.get('MEXC_CREDS', os.path.expanduser('~/.config/mexc.secret'))
    cfg = {}
    for line in open(path):
        line = line.strip()
        if line and not line.startswith('#'):
            k, v = line.split(':', 1)
            cfg[k.strip()] = v.strip()
    return cfg['api' + '_key'], cfg['api' + '_secret']

def _signed_query(params, key, secret):
    params.update({'timestamp': int(time.time() * 1000), 'recvWindow': 10000})
    qs = urllib.parse.urlencode(params)
    sig = hmac.new(secret.encode(), qs.encode(), hashlib.sha256).hexdigest()
    return qs + '&signature=' + sig, {'X-MEXC-APIKEY': key}

def _req(method, path, params=None):
    key, secret = load_creds()
    qs, headers = (('', {'Content-Type': 'application/json'}) if not params
                   else _signed_query(params, key, secret))
    c = http.client.HTTPSConnection(HOST, timeout=15)
    c.request(method, path + (('?' + qs) if qs else ''), headers=headers)
    return json.loads(c.getresponse().read().decode())

def price(symbol='BTCUSDT'):
    return float(_req('GET', '/api/v3/ticker/price', None)['price'])

if __name__ == '__main__':
    import sys
    print(price(sys.argv[2]) if len(sys.argv) > 2 else price())
