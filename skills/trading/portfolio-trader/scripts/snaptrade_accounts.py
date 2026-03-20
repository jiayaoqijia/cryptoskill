#!/usr/bin/env python3
import json
from snaptrade_common import load_config, get_client


def main():
    cfg = load_config()
    client = get_client(cfg)
    resp = client.account_information.list_user_accounts(user_id=cfg['user_id'], user_secret=cfg['user_secret'])
    accounts = getattr(resp, 'body', resp)

    out = []
    for a in accounts:
        if isinstance(a, dict):
            out.append({
                'id': a.get('id'),
                'name': a.get('name'),
                'number': a.get('number') or a.get('account_number'),
                'type': a.get('type'),
                'institution_name': a.get('institution_name') or a.get('brokerage_name')
            })
        else:
            out.append({
                'id': getattr(a, 'id', None),
                'name': getattr(a, 'name', None),
                'number': getattr(a, 'number', None),
                'type': getattr(a, 'type', None),
                'institution_name': getattr(a, 'institution_name', None)
            })
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
