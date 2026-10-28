"""Content indexes over mature DEX decoding; no target execution or task state."""
import base64
from contextlib import contextmanager
import hashlib
import importlib.metadata
import io
import json
import os
from pathlib import Path
import re
import sqlite3
import sys
import tempfile
import zipfile

sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'re-dynamic/scripts'))
from _re_evidence import canonical, sha, read_file, fingerprint, regular

SCHEMA='dsh-dex-index-v1'
TABLES={'inputs','sources','methods','instructions','refs'}


def proto(v):
    if isinstance(v,(tuple,list)):v=''.join(v)
    if not isinstance(v,str):raise ValueError('Decoder returned an unknown prototype shape')
    v=''.join(v.split())
    if not v.startswith('(') or ')' not in v:raise ValueError('Decoder returned an invalid method prototype')
    return v


def signature(cls,name,descriptor):return cls+'->'+name+proto(descriptor)


def insert(con,table,data,**fields):
    if table not in TABLES:raise ValueError('Unknown index table')
    keys=[*fields,'data'];values=[*fields.values(),canonical(data).decode()]
    return con.execute('INSERT INTO '+table+'('+','.join(keys)+') VALUES('+','.join('?' for _ in keys)+')',values).lastrowid


def decode(con,blob,source_id):
    from androguard.core.dex import DEX,Operand,Kind
    d=DEX(blob);method_count=instruction_count=ref_count=0
    for cls in d.get_classes():
        for m in cls.get_methods():
            sig=signature(m.get_class_name(),m.get_name(),m.get_descriptor());mid=sha(canonical({'source':source_id,'signature':sig}))
            code=m.get_code();raw=bytes(code.get_bc().get_raw()) if code is not None else b''
            code_off=m.get_code_off() if code is not None else None
            # Standard code_item header is 16 bytes. Export coordinates only
            # after checking the decoder's entire instruction bytes against input.
            start=code_off+16 if code is not None else None
            matched=start is not None and len(raw)>0 and start+len(raw)<=len(blob) and len(raw)==code.get_insns_size()*2 and blob[start:start+len(raw)]==raw
            data={'id':mid,'source_id':source_id,'signature':sig,'class':m.get_class_name(),'name':m.get_name(),
                  'prototype':proto(m.get_descriptor()),'dex_method_index':m.get_method_idx(),'access_flags':m.get_access_flags(),'has_code':code is not None,
                  'code_item_offset_bytes':hex(code_off) if code_off is not None else None,
                  'instructions_file_offset_bytes':hex(start) if matched else None,'code_bytes':len(raw),
                  'code_sha256':sha(raw) if code is not None else None,'file_coordinates_verified':matched,
                  'authority':'static encoded declaration; not proof of runtime reachability or dispatch'}
            insert(con,'methods',data,id=mid,source=source_id,signature=sig);method_count+=1
            if code is None:continue
            for off,ins in m.get_instructions_idx():
                if off%2 or ins.get_length()%2:raise ValueError('Decoder returned non-code-unit aligned instruction')
                raw_ins=bytes(ins.get_raw())
                if raw[off:off+len(raw_ins)]!=raw_ins:raise ValueError('Decoder instruction bytes differ from code span')
                operands=ins.get_operands(off)
                row={'method_id':mid,'offset_bytes':off,'offset_code_units':off//2,
                     'file_offset_bytes':hex(start+off) if matched else None,'length_bytes':len(raw_ins),
                     'opcode':ins.get_name(),'operands':ins.get_output(off),'raw_hex':raw_ins.hex()}
                insert(con,'instructions',row,method=mid,offset=off);instruction_count+=1
                for operand in operands:
                    tag=int(operand[0])
                    if tag<int(Operand.KIND):continue
                    kind=tag-int(Operand.KIND);index=operand[1]
                    if kind==int(Kind.METH):
                        cls_name,name,desc=d.get_cm_method(index);target=signature(cls_name,name,desc);relation='call'
                    elif kind==int(Kind.FIELD):
                        cls_name,typ,name=d.get_cm_field(index);target=cls_name+'->'+name+':'+typ;relation='field'
                    elif kind==int(Kind.STRING):target=d.get_cm_string(index);relation='string'
                    elif kind==int(Kind.TYPE):target=d.get_cm_type(index);relation='type'
                    else:target=str(operand[2:] if len(operand)>2 else index);relation='uninterpreted_operand'
                    ref={'source_method':mid,'source_signature':sig,'kind':relation,'target':target,'offset_bytes':off,
                         'offset_code_units':off//2,'opcode':ins.get_name(),'file_offset_bytes':row['file_offset_bytes'],
                         'runtime_dispatch_verified':False,'authority':'encoded operand; candidate definitions are not actual runtime dispatch'}
                    insert(con,'refs',ref,method=mid,kind=relation,target=target);ref_count+=1
    return {'methods':method_count,'instructions':instruction_count,'references':ref_count}


def build(inputs,output,max_input=512*1024*1024,max_dex=128*1024*1024):
    # Optional dependency is imported only for explicit indexing, never discovery.
    from loguru import logger
    logger.disable('androguard')
    import androguard.core.dex
    output=Path(output).absolute();output.parent.mkdir(parents=True,exist_ok=True)
    if output.exists() or output.is_symlink():raise ValueError('Index output already exists; use a new artifact path')
    fd,tmp=tempfile.mkstemp(prefix='.dex-index-',dir=output.parent);os.close(fd)
    con=sqlite3.connect(tmp)
    try:
        con.executescript('PRAGMA journal_mode=DELETE; CREATE TABLE meta(key TEXT PRIMARY KEY,data TEXT);'
          'CREATE TABLE inputs(rowid INTEGER PRIMARY KEY,data TEXT);'
          'CREATE TABLE sources(rowid INTEGER PRIMARY KEY,id TEXT UNIQUE,data TEXT);'
          'CREATE TABLE methods(rowid INTEGER PRIMARY KEY,id TEXT UNIQUE,source TEXT,signature TEXT,data TEXT);'
          'CREATE TABLE instructions(rowid INTEGER PRIMARY KEY,method TEXT,offset INTEGER,data TEXT);'
          'CREATE TABLE refs(rowid INTEGER PRIMARY KEY,method TEXT,kind TEXT,target TEXT,data TEXT);'
          'CREATE INDEX method_signatures ON methods(signature);CREATE INDEX method_sources ON methods(source);'
          'CREATE INDEX instructions_method ON instructions(method,offset);CREATE INDEX refs_target ON refs(kind,target);CREATE INDEX refs_method ON refs(method);')
        failures=0;seen=set()
        def source(blob,locator,error=None):
            nonlocal failures
            sid=sha(canonical(locator));data={**locator,'id':sid,'dex_sha256':sha(blob) if blob is not None else None,'bytes':len(blob) if blob is not None else None,'state':'indexed'}
            if sid in seen:return
            seen.add(sid);con.execute('SAVEPOINT dex_source')
            try:
                if error:raise ValueError(error)
                counts=decode(con,blob,sid);data.update(counts)
                con.execute('RELEASE dex_source')
            except Exception as e:
                con.execute('ROLLBACK TO dex_source');con.execute('RELEASE dex_source');failures+=1
                data.update(state='parse_failed',error=type(e).__name__+': '+str(e),indexed_methods=0)
            insert(con,'sources',data,id=sid)
        for path in inputs:
            blob=read_file(path,max_input);container=sha(blob)
            inventory={'input_sha256':container,'path':str(Path(path).absolute()),'bytes':len(blob),
                       'selection':'raw DEX or all ZIP entries ending .dex; no recursive archive/opaque-payload discovery'}
            if zipfile.is_zipfile(io.BytesIO(blob)):
                entries=0
                with zipfile.ZipFile(io.BytesIO(blob)) as z:
                    for ordinal,info in enumerate(z.infolist()):
                        if info.is_dir() or not info.filename.lower().endswith('.dex'):continue
                        entries+=1;locator={'container_sha256':container,'entry':info.filename,'zip_ordinal':ordinal,'zip_header_offset_bytes':hex(info.header_offset)}
                        try:
                            if info.file_size>max_dex:raise ValueError('DEX exceeds explicit per-entry byte budget; not partially decoded')
                            with z.open(info) as stream:data=stream.read(max_dex+1)
                            if len(data)!=info.file_size or len(data)>max_dex:raise ValueError('DEX short read or expansion budget exceeded')
                            source(data,locator)
                        except (OSError,ValueError,RuntimeError,zipfile.BadZipFile) as e:source(None,locator,str(e))
                inventory['selected_entries']=entries
                if not entries:failures+=1;inventory['state']='no_selected_dex'
            else:
                source(blob if len(blob)<=max_dex else None,{'container_sha256':container,'entry':'<raw>','zip_ordinal':None,'zip_header_offset_bytes':None},'DEX exceeds per-entry byte budget' if len(blob)>max_dex else None)
            insert(con,'inputs',inventory)
        counts={t:con.execute('SELECT COUNT(*) FROM '+t).fetchone()[0] for t in TABLES}
        meta={'schema':SCHEMA,'decoder':{'name':'androguard','version':importlib.metadata.version('androguard')},'counts':counts,
              'coverage':'partial' if failures else 'selected_entries_indexed','failures':failures,
              'runtime_dispatch_verified':False,'target_accepted':None,
              'limitations':['Static operands only; reflection, loaders and virtual dispatch can remain unresolved','No device access, native execution, Ghidra writes or task state updates']}
        con.execute('INSERT INTO meta VALUES(?,?)',('manifest',canonical(meta).decode()));con.commit();con.close();con=None
        os.chmod(tmp,0o600);os.link(tmp,output)
        return {**meta,'index':str(output),'snapshot':file_hash(output)}
    finally:
        if con is not None:con.close()
        Path(tmp).unlink(missing_ok=True)


def file_hash(path):
    f,before=regular(path,(1<<63)-1);h=hashlib.sha256()
    with f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
        if fingerprint(before)!=fingerprint(os.fstat(f.fileno())):raise ValueError('Index changed while hashing')
    return h.hexdigest()


@contextmanager
def opened(path,snapshot=None):
    p=Path(path).absolute()
    before=p.stat();digest=file_hash(p)
    if fingerprint(before)!=fingerprint(p.stat()):raise ValueError('Index changed before opening')
    if snapshot is not None and snapshot!=digest:raise ValueError('Index snapshot changed')
    con=sqlite3.connect(p.as_uri()+'?mode=ro&immutable=1',uri=True);con.row_factory=sqlite3.Row
    try:
        meta=json.loads(con.execute('SELECT data FROM meta WHERE key=?',('manifest',)).fetchone()[0])
        if meta['schema']!=SCHEMA:raise ValueError('Unsupported index schema')
        yield con,digest,meta
        if fingerprint(before)!=fingerprint(p.stat()):raise ValueError('Index changed during query')
    finally:con.close()


def query(path,table='methods',after=0,limit=25,max_bytes=16384,snapshot=None,signature_filter=None,method=None,kind=None,target=None,source=None):
    if table not in TABLES or type(after) is not int or after<0 or not 1<=limit<=1000 or not 1024<=max_bytes<=131072:raise ValueError('Invalid query/page options')
    clauses=['rowid>?'];params=[after]
    for key,value,allowed in [('signature',signature_filter,{'methods'}),('method',method,{'instructions','refs'}),('kind',kind,{'refs'}),('target',target,{'refs'}),('source',source,{'methods'})]:
        if value is not None:
            if table not in allowed:raise ValueError('Filter does not apply to this table: '+key)
            clauses.append(key+'=?');params.append(value)
    with opened(path,snapshot) as (con,digest,meta):
        rows=con.execute('SELECT rowid,data FROM '+table+' WHERE '+' AND '.join(clauses)+' ORDER BY rowid LIMIT ?',(*params,limit+1)).fetchall()
        result={'schema':SCHEMA,'snapshot':digest,'coverage':meta['coverage'],'items':[],'next':None,'authority':'query of selected static inputs; no runtime dispatch/absence proof'}
        for row in rows[:limit]:
            data=json.loads(row['data']);item={'row':row['rowid'],**data}
            if len(canonical(item))>max_bytes//2:
                item={'row':row['rowid'],'large_fields_omitted':True,'document':{'table':table,'row':row['rowid'],'snapshot':digest,'bytes':len(row['data'].encode())},
                      **{k:data[k] for k in ('id','source_id','method_id','kind','offset_bytes','state') if k in data}}
            if result['items'] and len(canonical({**result,'items':result['items']+[item]}))+128>max_bytes:break
            result['items'].append(item)
        if result['items'] and (len(rows)>len(result['items'])):result['next']=result['items'][-1]['row']
        if len(canonical(result))>max_bytes:raise ValueError('Page metadata exceeds byte budget; increase max-bytes')
        return result


def document(path,table,row,offset=0,max_bytes=8192,snapshot=None):
    if table not in TABLES or type(row) is not int or row<1 or type(offset) is not int or offset<0 or not 1<=max_bytes<=65536:raise ValueError('Invalid document page')
    with opened(path,snapshot) as (con,digest,_):
        value=con.execute('SELECT data FROM '+table+' WHERE rowid=?',(row,)).fetchone()
        if value is None:raise ValueError('Index row unavailable')
        body=value[0].encode()
        if offset>len(body):raise ValueError('Document offset outside exact row')
        chunk=body[offset:offset+max_bytes];end=offset+len(chunk)
        return {'snapshot':digest,'encoding':'base64','bytes':len(body),'offset':offset,'next':end if end<len(body) else None,'data':base64.b64encode(chunk).decode(),'sha256':sha(body)}


def definitions(path,target,snapshot=None,after=0,limit=25,max_bytes=16384):
    return query(path,'methods',after,limit,max_bytes,snapshot,signature_filter=target)
