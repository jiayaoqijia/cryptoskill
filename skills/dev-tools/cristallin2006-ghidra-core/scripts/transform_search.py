#!/usr/bin/env python3
"""Local finite byte-pipeline search. Standard library, no target execution.

search SPEC [--estimate] [--report NEW_FILE]; replay REPORT --rank N --output NEW_FILE
See ghidra-static/references/transform-pipelines.md for the explicit JSON contract.
"""
import argparse
from collections import OrderedDict
import hashlib
import itertools
import json
import os
from pathlib import Path
import sys

VERSION = '1.0.0'
IDENTITY = bytes(range(256))


class Unsupported(ValueError):
    pass


def sha(data):
    return hashlib.sha256(data).hexdigest()


def integer(value, name, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError('invalid '+name)
    return value


def fields(value, allowed, required=()):
    if not isinstance(value, dict) or set(value)-set(allowed) or set(required)-set(value):
        raise ValueError('invalid fields; expected '+','.join(allowed))


def hexbytes(value):
    if not isinstance(value, str):
        raise ValueError('hex must be a string')
    result = bytes.fromhex(value)
    if not result:
        raise ValueError('empty hex value')
    return result


def load_json(file):
    # Input grammar boundary, not a task/search time limit.
    with Path(file).open('rb') as stream:
        data = stream.read(1024*1024+1)
    if len(data) > 1024*1024:
        raise Unsupported('spec/report exceeds supported 1 MiB JSON size')
    def unique(pairs):
        obj = {}
        for key, value in pairs:
            if key in obj:
                raise ValueError('duplicate JSON field: '+key)
            obj[key] = value
        return obj
    return json.loads(data, object_pairs_hook=unique)


def source_data(source, directory, max_bytes):
    fields(source, ['path','hex','sha256','offset','length','basis'], [])
    if ('path' in source) == ('hex' in source):
        raise ValueError('source needs exactly one of path/hex')
    offset = integer(source.get('offset',0),'offset')
    if 'path' in source:
        if not isinstance(source['path'],str):
            raise ValueError('invalid source path')
        file = (directory/source['path']).resolve()
        with file.open('rb') as stream:
            raw = stream.read(max_bytes+1)
        public = {'path':str(file)}
    else:
        if not isinstance(source['hex'],str) or len(source['hex']) > max_bytes*3+1024:
            raise ValueError('hex input exceeds declared max_input_bytes')
        raw = hexbytes(source['hex']); public = {'hex':source['hex']}
    if len(raw)>max_bytes:
        raise ValueError('source exceeds declared max_input_bytes; extract an explicit region first')
    digest = sha(raw)
    if source.get('sha256',digest)!=digest:
        raise ValueError('source hash mismatch')
    length = integer(source.get('length',len(raw)-offset),'length',1)
    if offset+length>len(raw):
        raise ValueError('source slice outside input')
    public.update(sha256=digest,offset=offset,length=length,basis=source.get('basis'))
    return raw[offset:offset+length],public


def operation(value, size, inverse=False):
    if not isinstance(value,dict):
        raise ValueError('operation must be an object')
    name = value.get('op')
    allowed = {'xor':['key_hex','phase'], 'add':['value'], 'sub':['value'],
               'affine':['a','b'], 'rol':['count'], 'ror':['count'],
               'reverse':[], 'word_reverse':['size'], 'nibble_swap':[],
               'bit_reverse':[], 'index_xor':['a','b'], 'index_add':['a','b']}
    if name not in allowed:
        raise Unsupported('unsupported operation')
    fields(value,['op','basis']+allowed[name],['op'])
    result = {k:v for k,v in value.items() if k!='basis'}
    for key in allowed[name]:
        if key in ('key_hex','phase'):
            continue
        integer(result.get(key),name+'.'+key)
    if name=='xor':
        key = hexbytes(result.get('key_hex'))
        if len(key)>size:
            raise ValueError('key longer than selected data; declare an applicable region/key')
        phase = integer(result.get('phase',0),'phase')%len(key)
        key = key[phase:]+key[:phase]
        # A periodic-key identity is exact only for this declared byte sequence.
        for period in range(1,len(key)+1):
            if len(key)%period==0 and key==key[:period]*(len(key)//period):
                key=key[:period];break
        result = {'op':'xor','key_hex':key.hex(),'phase':0}
    elif name in ('add','sub'):
        result['value']%=256
        if inverse:
            result['op']='sub' if name=='add' else 'add'
    elif name=='affine':
        result['a']%=256;result['b']%=256
        if inverse:
            if result['a']%2==0:
                raise Unsupported('even affine multiplier has no unique byte inverse')
            a=pow(result['a'],-1,256)
            result.update(a=a,b=(-a*result['b'])%256)
    elif name in ('rol','ror'):
        result['count']%=8
        if inverse:
            result['op']='ror' if name=='rol' else 'rol'
    elif name=='word_reverse':
        if result['size'] not in (2,4,8) or size%result['size']:
            raise Unsupported('word_reverse requires aligned 2/4/8-byte groups')
    elif name.startswith('index_'):
        result['a']%=256;result['b']%=256
        if inverse and name=='index_add':
            result.update(a=(-result['a'])%256,b=(-result['b'])%256)
    return result


def apply_op(data,op):
    name=op['op']
    if name=='xor':
        key=bytes.fromhex(op['key_hex']);return bytes(b^key[i%len(key)] for i,b in enumerate(data))
    if name in ('add','sub'):
        delta=op['value']*(1 if name=='add' else -1)
        return bytes((b+delta)&255 for b in data)
    if name=='affine':return bytes((op['a']*b+op['b'])&255 for b in data)
    if name in ('rol','ror'):
        n=op['count'] if name=='rol' else (-op['count'])%8
        return bytes(((b<<n)|(b>>((8-n)%8)))&255 for b in data) if n else data
    if name=='reverse':return data[::-1]
    if name=='word_reverse':
        n=op['size'];return b''.join(data[i:i+n][::-1] for i in range(0,len(data),n))
    if name=='nibble_swap':return bytes(((b<<4)|(b>>4))&255 for b in data)
    if name=='bit_reverse':return bytes(int(f'{b:08b}'[::-1],2) for b in data)
    if name=='index_xor':return bytes(b^((op['a']*i+op['b'])&255) for i,b in enumerate(data))
    if name=='index_add':return bytes((b+op['a']*i+op['b'])&255 for i,b in enumerate(data))
    raise Unsupported('unsupported operation')


def canonical(chain):
    """Only compose adjacent, position-independent byte maps, over all 256 values.

    Periodic/index/layout operations are barriers. Never collapse stateful or
    index-dependent operations based on one sample output.
    """
    signature=[];mapping=IDENTITY
    def flush():
        nonlocal mapping
        if mapping!=IDENTITY:signature.append(('map',mapping.hex()))
        mapping=IDENTITY
    for op in chain:
        if op['op'] not in ('reverse','word_reverse','index_xor','index_add') and not (op['op']=='xor' and len(bytes.fromhex(op['key_hex']))>1):
            mapping=apply_op(mapping,op)
        else:
            flush();signature.append(('barrier',json.dumps(op,sort_keys=True)))
    flush()
    return tuple(signature)


def criteria_spec(value):
    fields(value,['prefix_hex','suffix_hex','length','sha256','ascii_case_insensitive'])
    if 'length' in value:integer(value['length'],'criteria.length')
    for key in ('prefix_hex','suffix_hex'):
        if key in value:hexbytes(value[key])
    if 'sha256' in value and (not isinstance(value['sha256'],str) or len(value['sha256'])!=64 or any(c not in '0123456789abcdef' for c in value['sha256'])):
        raise ValueError('invalid criteria hash')
    if type(value.get('ascii_case_insensitive',False)) is not bool:
        raise ValueError('invalid ASCII case setting')
    return value


def assess(data,criteria):
    tests={}
    fold=criteria.get('ascii_case_insensitive',False)
    target=data.lower() if fold else data
    for key,method in [('prefix_hex',bytes.startswith),('suffix_hex',bytes.endswith)]:
        if key in criteria:
            expected=bytes.fromhex(criteria[key]);tests[key]=method(target,expected.lower() if fold else expected)
    if 'length' in criteria:tests['length']=len(data)==criteria['length']
    if 'sha256' in criteria:tests['sha256']=sha(data)==criteria['sha256']
    printable=sum(b in (9,10,13) or 32<=b<127 for b in data)/len(data)
    try:data.decode('utf-8');utf8=True
    except UnicodeDecodeError:utf8=False
    magic=next((label for prefix,label in [(b'\x7fELF','ELF'),(b'MZ','MZ'),(b'PK\x03\x04','ZIP'),(b'\x89PNG\r\n\x1a\n','PNG'),(b'\x1f\x8b','gzip')] if data.startswith(prefix)),None)
    matches=all(tests.values()) if tests else None
    score=round(printable*10+int(utf8)*2+bool(magic)*20+sum(tests.values())*30+int(matches is True)*100,6)
    return {'matches_declared_criteria':matches,'score':score,'evidence':{'criteria':tests,'printable_ratio':round(printable,6),'valid_utf8':utf8,'magic_prefix':magic},'authority':'candidate only; no target execution or acceptance'}


def prepare(spec,directory):
    fields(spec,['version','source','width','direction','pipelines','criteria','budget','top'],['version','source','width','direction','pipelines','budget','top'])
    if type(spec['version']) is not int or spec['version']!=1 or type(spec['width']) is not int or spec['width']!=8:
        raise Unsupported('only version 1 byte-domain width=8 is supported')
    if spec['direction'] not in ('forward','inverse'):
        raise ValueError('direction must be forward or inverse')
    fields(spec['budget'],['max_input_bytes','max_paths','max_byte_ops','cache_entries'],['max_input_bytes','max_paths','max_byte_ops'])
    budget={k:integer(v,'budget.'+k,1) for k,v in spec['budget'].items()}
    budget.setdefault('cache_entries',1024)
    top=integer(spec['top'],'top',1)
    if top>1000 or budget['cache_entries']>100000:
        raise Unsupported('top limit 1000; equivalence-cache limit 100000')
    data,source=source_data(spec['source'],directory,budget['max_input_bytes'])
    if not isinstance(spec['pipelines'],list) or not spec['pipelines']:
        raise ValueError('nonempty pipeline alternatives required')
    alternatives=[];total=0;estimated_work=0
    for pipeline in spec['pipelines']:
        if not isinstance(pipeline,list) or len(pipeline)>64:
            raise Unsupported('pipeline must have at most 64 stages')
        stages=[];paths=1
        for stage in pipeline:
            if not isinstance(stage,list) or not stage:
                raise ValueError('each stage needs explicit finite operation alternatives')
            stages.append([operation(op,len(data),spec['direction']=='inverse') for op in stage]);paths*=len(stage)
        if spec['direction']=='inverse':stages.reverse()
        alternatives.append(stages);total+=paths
        estimated_work+=paths*len(stages)*(256+len(data))
    return data,source,alternatives,total,estimated_work,budget,top,criteria_spec(spec.get('criteria',{}))


def search(spec,directory=Path('.'),estimate=False):
    data,source,alternatives,total,work,budget,top,criteria=prepare(spec,directory)
    report={'ok':True,'version':VERSION,'status':'estimate' if estimate else 'complete','source':source,'width':8,'direction':spec['direction'],
            'declared_space':spec['pipelines'],'criteria':criteria,'budget':budget,
            'estimate':{'declared_paths':total,'upper_byte_work_units':work,'note':'includes 256-value canonical maps; not a wall-clock prediction'},
            'coverage':{'considered_paths':0,'evaluated_paths':0,'equivalence_skips':0,'cache_evictions':0,'byte_work_units':0,'pruned_paths':0},'candidates':[],
            'scope':'Only declared slices, chains and parameters. No inference of global impossibility or target acceptance.'}
    if estimate:return report
    coverage=report['coverage'];cache=OrderedDict();kept={};stop=None;match_count=0;evicted=False
    for stages in alternatives:
        for choice in itertools.product(*stages):
            if coverage['considered_paths']>=budget['max_paths']:
                stop='max_paths';break
            canonical_cost=256*len(choice)
            if coverage['byte_work_units']+canonical_cost>budget['max_byte_ops']:
                stop='max_byte_ops';break
            coverage['byte_work_units']+=canonical_cost
            signature=canonical(choice)
            if signature in cache:
                coverage['considered_paths']+=1;coverage['equivalence_skips']+=1;cache.move_to_end(signature);continue
            cost=len(data)*len(choice)
            if coverage['byte_work_units']+cost>budget['max_byte_ops']:
                stop='max_byte_ops';break
            coverage['byte_work_units']+=cost;coverage['considered_paths']+=1
            result=data
            for op in choice:result=apply_op(result,op)
            cache[signature]=True
            if len(cache)>budget['cache_entries']:cache.popitem(last=False);coverage['cache_evictions']+=1
            coverage['evaluated_paths']+=1
            candidate=assess(result,criteria);match_count+=candidate['matches_declared_criteria'] is True
            digest=sha(result)
            candidate.update(output_sha256=digest,length=len(result),chain=list(choice),canonical_sha256=sha(repr(signature).encode()))
            old=kept.get(digest)
            if old is None or len(candidate['chain'])<len(old['chain']):kept[digest]=candidate
            if len(kept)>top:
                worst=min(kept,key=lambda h:(kept[h]['matches_declared_criteria'] is True,kept[h]['score'],-len(kept[h]['chain']),h));del kept[worst];evicted=True
        if stop:break
    if stop:report.update(status='incomplete',stop_reason=stop)
    coverage['unconsidered_paths']=total-coverage['considered_paths']
    report['matched_evaluations']=match_count
    report['candidates']=sorted(kept.values(),key=lambda c:(c['matches_declared_criteria'] is True,c['score'],-len(c['chain']),c['output_sha256']),reverse=True)
    report['candidate_list_truncated']=evicted
    return report


def exclusive_write(file,data):
    descriptor=os.open(file,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(descriptor,'wb') as stream:stream.write(data)


def replay(report,rank,directory=Path('.')):
    if not isinstance(report,dict) or report.get('version')!=VERSION or report.get('width')!=8:
        raise Unsupported('unsupported replay report')
    candidate=report['candidates'][integer(rank,'rank',1)-1]
    data,_=source_data(report['source'],directory,report['budget']['max_input_bytes'])
    for item in candidate['chain']:data=apply_op(data,operation(item,len(data)))
    if sha(data)!=candidate['output_sha256']:
        raise ValueError('replay output hash mismatch')
    return data


def self_test():
    assert apply_op(bytes([0,1,128,255]),{'op':'rol','count':1})==bytes([0,2,1,255])
    assert apply_op(bytes([0,1,255]),{'op':'affine','a':3,'b':7})==bytes([7,10,4])
    assert apply_op(b'\x10\x80',{'op':'bit_reverse'})==b'\x08\x01'
    assert canonical([{'op':'xor','key_hex':'5a'},{'op':'xor','key_hex':'5a'}])==()
    return {'ok':True,'version':VERSION,'checks':'fixed byte vectors and exact map identity; independent regressions remain necessary'}


def main():
    ap=argparse.ArgumentParser(description=__doc__);sub=ap.add_subparsers(dest='action',required=True)
    scan=sub.add_parser('search');scan.add_argument('spec',type=Path);scan.add_argument('--estimate',action='store_true');scan.add_argument('--report',type=Path)
    run=sub.add_parser('replay');run.add_argument('report',type=Path);run.add_argument('--rank',type=int,required=True);run.add_argument('--output',type=Path,required=True)
    sub.add_parser('self-test');args=ap.parse_args()
    try:
        if args.action=='self-test':value=self_test()
        elif args.action=='replay':
            report=load_json(args.report);data=replay(report,args.rank,args.report.resolve().parent);exclusive_write(args.output,data)
            value={'ok':True,'output':str(args.output),'sha256':sha(data),'length':len(data),'authority':'replayed candidate; not target acceptance'}
        else:
            report=search(load_json(args.spec),args.spec.resolve().parent,args.estimate)
            value={k:v for k,v in report.items() if k not in ('declared_space','source','criteria','candidates')}
            value['candidates']=[{k:v for k,v in c.items() if k not in ('chain','evidence')} for c in report['candidates']]
            if args.report:
                encoded=json.dumps(report,ensure_ascii=False,indent=2).encode()
                if len(encoded)>1024*1024:raise Unsupported('report exceeds supported replay size; reduce top or domain description')
                exclusive_write(args.report,encoded);value['report']=str(args.report)
            value['note']='Full source/chain only in an explicitly requested report; no decoded bytes on stdout.'
        print(json.dumps(value,ensure_ascii=False));return 0
    except (ValueError,OSError,KeyError,IndexError,TypeError) as error:
        print(json.dumps({'ok':False,'status':'unsupported' if isinstance(error,Unsupported) else 'error','error':str(error)},ensure_ascii=False));return 2


if __name__=='__main__':
    for stream in (sys.stdout,sys.stderr):
        if stream.encoding and stream.encoding.lower() not in ('utf-8','utf8'):
            stream.reconfigure(encoding='utf-8')
    sys.exit(main())
