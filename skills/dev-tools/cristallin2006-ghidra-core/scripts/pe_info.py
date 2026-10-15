import sys, struct, math, collections

p = sys.argv[1]
d = open(p, 'rb').read()
print('size', len(d))
print('dos magic', d[:2])
pe = struct.unpack_from('<I', d, 0x3c)[0]
print('e_lfanew', hex(pe))
print('pe sig', d[pe:pe+4])
mach, nsec = struct.unpack_from('<HH', d, pe+4)
print('machine', hex(mach), 'nsections', nsec)
ts = struct.unpack_from('<I', d, pe+8)[0]
import datetime
print('timestamp', ts, datetime.datetime.utcfromtimestamp(ts))
opt = pe + 24
magic = struct.unpack_from('<H', d, opt)[0]
print('opt magic', hex(magic), 'PE32+' if magic == 0x20b else 'PE32')
is64 = magic == 0x20b
ep = struct.unpack_from('<I', d, opt+16)[0]
print('entry RVA', hex(ep))
# ImageBase: PE32+ -> opt+24 (QWORD); PE32 -> opt+28 (opt+24 是 BaseOfData, DWORD)
ib = opt + 24 if is64 else opt + 28
print('imagebase', hex(struct.unpack_from('<Q' if is64 else '<I', d, ib)[0]))
print('sectionalign', hex(struct.unpack_from('<I', d, opt+32)[0]))
print('filealign', hex(struct.unpack_from('<I', d, opt+36)[0]))
print('sizeofimage', hex(struct.unpack_from('<I', d, opt+56)[0]))
print('subsystem', struct.unpack_from('<H', d, opt+68)[0])
print('dllchar', hex(struct.unpack_from('<H', d, opt+70)[0]))
ddoff = opt + (112 if is64 else 96)
names = ['export','import','resource','exception','security','basereloc','debug','arch','globalptr','tls','loadconfig','boundimport','iat','delayimport','clr','reserved']
for i, n in enumerate(names):
    rva, sz = struct.unpack_from('<II', d, ddoff + i*8)
    if rva or sz:
        print('dir %-12s rva=%#x size=%#x' % (n, rva, sz))
# sections
sh = opt + struct.unpack_from('<H', d, pe+20)[0]
print('--- sections ---')
secs = []
for i in range(nsec):
    o = sh + i*40
    nm = d[o:o+8].rstrip(b'\0')
    vsz, va, rsz, ro = struct.unpack_from('<IIII', d, o+8)
    ch = struct.unpack_from('<I', d, o+36)[0]
    raw = d[ro:ro+rsz] if rsz else b''
    ent = 0.0
    if raw:
        c = collections.Counter(raw)
        ent = -sum((v/len(raw))*math.log2(v/len(raw)) for v in c.values())
    print('%-10s VA=%#010x VS=%#08x RAW=%#08x RS=%#08x CH=%#010x entropy=%.3f' % (nm.decode('latin1'), va, vsz, ro, rsz, ch, ent))
    secs.append((nm.decode('latin1'), va, vsz, ro, rsz, ch))

def rva2off(rva):
    for nm, va, vsz, ro, rsz, ch in secs:
        if va <= rva < va + max(vsz, rsz):
            return ro + (rva - va)
    return None

# imports
print('--- imports ---')
io = rva2off(struct.unpack_from('<I', d, ddoff+8)[0])
if io:
    n = 0
    while True:
        ilt, ts_, fc, name_rva, iat = struct.unpack_from('<IIIII', d, io + n*20)
        if name_rva == 0:
            break
        no = rva2off(name_rva)
        dll = d[no:d.index(b'\0', no)].decode('latin1')
        thunk = rva2off(ilt or iat)
        funcs = []
        k = 0
        # PE32+: ILT/IAT entries are 8-byte QWORDs; PE32: 4-byte DWORDs.
        # Reading 8-byte thunks as DWORDs makes the trailing zero high-half look
        # like the terminator, silently truncating the list to 1 entry.
        TW = 8 if is64 else 4
        ORDBIT = 1 << (63 if is64 else 31)
        ORDMASK = 0xffff
        while thunk:
            t = struct.unpack_from('<Q' if is64 else '<I', d, thunk+k*TW)[0]
            if t == 0:
                break
            if t & ORDBIT:
                funcs.append('ord#%d' % (t & ORDMASK))
            else:
                fo = rva2off(t & 0xffffffff)
                funcs.append(d[fo+2:d.index(b'\0', fo+2)].decode('latin1'))
            k += 1
        print('%s (%d): %s' % (dll, len(funcs), ', '.join(funcs)))
        n += 1
        if n > 40:
            break
