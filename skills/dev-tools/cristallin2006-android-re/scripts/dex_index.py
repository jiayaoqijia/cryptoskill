#!/usr/bin/env python3
"""Optional DEX index, exact paged queries and explicit JADX class export."""
import argparse
import json
import os
import re
from pathlib import Path
import signal
import sqlite3
import subprocess
import sys
import time
import _android_tools as T
from _dex_index import build,query,document,definitions,canonical,read_file,sha,file_hash


def doctor():
    # Discovery is passive: no agpy() import probes, versions or adb queries.
    import re_lab
    paths=[sys.executable,os.path.expanduser('~/re-tools-venv/bin/python')]
    if os.environ.get('AGPY'):paths.append(os.environ['AGPY'])
    return {'mode':'passive','sdk':T.find_sdk(),'tools':{n:getattr(T,n)() for n in ('jadx','apkanalyzer','d8','dexdump','aapt2')},
            'interpreters':[re_lab.inspect_python(p) for p in dict.fromkeys(paths) if Path(p).is_file()],
            'commands_executed':0,'device_queries':0,'sample_parsed':False,'authority':'discovery only; missing paths are not proof of global absence'}


def decompile(path,cls,out,jadx=None,timeout=300,max_input=512*1024*1024):
    tool=jadx or T.jadx()
    if not tool:raise ValueError('JADX unavailable in configured discovery scope')
    if not cls or '\0' in cls:raise ValueError('Explicit class required')
    cls=cls[1:-1].replace('/','.') if cls.startswith('L') and cls.endswith(';') else cls
    if not re.fullmatch(r'[\w$][\w$.-]*',cls):raise ValueError('Use an exact dotted or descriptor class name; unsupported names remain available in the DEX index')
    blob=read_file(path,max_input);out=Path(out).absolute()
    if out.exists() or out.is_symlink():raise ValueError('Decompile output must be a new directory')
    out.mkdir(parents=True,mode=0o700);source=out/('input.apk' if blob[:2]==b'PK' else 'input.dex');source.write_bytes(blob)
    cmd=[tool,'--single-class',cls,'--single-class-output',str(out/'class.java'),str(source)]
    if str(tool).lower().endswith('.bat'):
        if any(re.search(r'[&|<>^%!\r\n]',str(arg)) for arg in cmd):raise ValueError('Windows batch backend cannot safely represent these arguments; use a native backend or a plain artifact path')
        cmd=[os.environ.get('COMSPEC','cmd.exe'),'/c',*cmd]
    code=None;timed_out=False
    with (out/'stdout.bin').open('wb') as stdout,(out/'stderr.bin').open('wb') as stderr:
        process=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=stdout,stderr=stderr,start_new_session=os.name!='nt')
        try:code=process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out=True
            if os.name!='nt':
                # wait(timeout) has not reaped this leader; its PID is reserved.
                try:os.killpg(process.pid,signal.SIGKILL)
                except ProcessLookupError:pass
            else:process.kill()
            code=process.wait()
    result={'schema':'dsh-jadx-class-export-v1','input_sha256':sha(blob),'class':cls,'tool':str(tool),
            'exit_code':code,'timed_out':timed_out,'files':[{'name':p.relative_to(out).as_posix(),'sha256':file_hash(p),'bytes':p.stat().st_size} for p in out.rglob('*') if p.is_file()],
            'state':'timed_out' if timed_out else 'exported_with_diagnostics' if code==0 and (out/'class.java').is_file() else 'failed',
            'semantic_correctness':'unverified; review diagnostics and relevant original bytecode','target_accepted':None,
            'cleanup_coverage':'invoked local CLI; Linux timeout kills its owned process group; no device or universal detached-process cleanup'}
    (out/'receipt.json').write_bytes(canonical(result));return result


def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__);actions=p.add_subparsers(dest='action',required=True)
    actions.add_parser('doctor')
    b=actions.add_parser('build');b.add_argument('--input',action='append',required=True);b.add_argument('--output',required=True);b.add_argument('--python');b.add_argument('--worker',action='store_true',help=argparse.SUPPRESS)
    b.add_argument('--max-input-bytes',type=int,default=512*1024*1024);b.add_argument('--max-dex-bytes',type=int,default=128*1024*1024)
    q=actions.add_parser('query');q.add_argument('--index',required=True);q.add_argument('--table',choices=['inputs','sources','methods','instructions','refs'],default='methods')
    for name in ('signature','method','kind','target','source'):q.add_argument('--'+name)
    q.add_argument('--after',type=int,default=0);q.add_argument('--limit',type=int,default=25);q.add_argument('--max-bytes',type=int,default=16384);q.add_argument('--snapshot')
    r=actions.add_parser('read-document');r.add_argument('--index',required=True);r.add_argument('--table',required=True);r.add_argument('--row',type=int,required=True);r.add_argument('--offset',type=int,default=0);r.add_argument('--max-bytes',type=int,default=8192);r.add_argument('--snapshot',required=True)
    d=actions.add_parser('definitions');d.add_argument('--index',required=True);d.add_argument('--signature',required=True);d.add_argument('--after',type=int,default=0);d.add_argument('--limit',type=int,default=25);d.add_argument('--max-bytes',type=int,default=16384);d.add_argument('--snapshot')
    j=actions.add_parser('decompile');j.add_argument('--input',required=True);j.add_argument('--class',dest='cls',required=True);j.add_argument('--output',required=True);j.add_argument('--jadx');j.add_argument('--timeout',type=float,default=300);j.add_argument('--max-input-bytes',type=int,default=512*1024*1024)
    args=p.parse_args(argv)
    try:
        if args.action=='doctor':result=doctor()
        elif args.action=='build':
            if args.max_dex_bytes<1 or args.max_input_bytes<1:raise ValueError('Positive byte budgets required')
            if not args.worker:
                interpreter=args.python or T.agpy()
                if not interpreter:raise ValueError('Androguard unavailable; configure --python/AGPY; existing static tools remain available')
                worker=[interpreter,str(Path(__file__).absolute()),'build','--worker','--output',args.output,'--max-input-bytes',str(args.max_input_bytes),'--max-dex-bytes',str(args.max_dex_bytes)]
                for path in args.input:worker.extend(['--input',path])
                return subprocess.run(worker).returncode
            result=build(args.input,args.output,args.max_input_bytes,args.max_dex_bytes)
        elif args.action=='query':result=query(args.index,args.table,args.after,args.limit,args.max_bytes,args.snapshot,args.signature,args.method,args.kind,args.target,args.source)
        elif args.action=='definitions':result=definitions(args.index,args.signature,args.snapshot,args.after,args.limit,args.max_bytes)
        elif args.action=='read-document':result=document(args.index,args.table,args.row,args.offset,args.max_bytes,args.snapshot)
        else:
            if not 0<args.timeout<365*86400:raise ValueError('Positive per-invocation wait budget required')
            result=decompile(args.input,args.cls,args.output,args.jadx,args.timeout,args.max_input_bytes)
        print(canonical({'ok':True,**result}).decode());return 0
    except (OSError,ValueError,TypeError,sqlite3.Error,ImportError) as e:
        print(canonical({'ok':False,'action':args.action,'error':str(e),'device_operations':0}).decode());return 2


if __name__=='__main__':raise SystemExit(main())
