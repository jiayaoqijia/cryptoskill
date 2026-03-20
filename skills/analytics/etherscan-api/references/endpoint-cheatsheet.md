# Endpoint Cheatsheet

Base:
- `GET https://api.etherscan.io/v2/api`

Common parameters:
- `apikey=<key>`
- `chainid=<network_chain_id>`
- `module=<module_name>`
- `action=<action_name>`

## Onchain Activities

Normal tx by address:
- `module=account&action=txlist`
- key params: `address,startblock,endblock,page,offset,sort`

Internal tx by address:
- `module=account&action=txlistinternal`
- key params: `address,startblock,endblock,page,offset,sort`

ERC20 transfers:
- `module=account&action=tokentx`
- key params: `address,contractaddress,startblock,endblock,page,offset,sort`

Event logs:
- `module=logs&action=getLogs`
- key params: `address,fromBlock,toBlock,page,offset`
- note: `offset` max is `1000` per query

## Contracts / Source / ABI

Get ABI:
- `module=contract&action=getabi`
- key params: `address`

Get source code metadata:
- `module=contract&action=getsourcecode`
- key params: `address`
- important response fields: `ABI,ContractName,ContractFileName,Proxy,Implementation`

Get deployer + creation tx:
- `module=contract&action=getcontractcreation`
- key params: `contractaddresses` (up to 5, comma-separated)

## Transaction Health

Execution status:
- `module=transaction&action=getstatus`
- key params: `txhash`

Receipt status:
- `module=transaction&action=gettxreceiptstatus`
- key params: `txhash`

## Parsing Rules

Response envelope:
- `status`: success flag (`"1"` usually success)
- `message`: summary string
- `result`: payload (object/array/string depending on endpoint)

If contract is proxy:
1. query source for proxy address
2. read `Implementation`
3. query ABI/source from implementation
4. decode runtime interactions using implementation ABI
