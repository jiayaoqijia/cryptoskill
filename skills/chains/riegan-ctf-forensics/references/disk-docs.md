# Disk images, registry, evtx, documents, logs

Sleuthkit workflow first (`sudo pacman -S sleuthkit testdisk`); the tools read
E01 directly (Arch's sleuthkit links libewf). Challenge images are untrusted:
work on copies in the challenge dir, never mount read-write.

## Partition walk — mmls → fls → icat

```bash
mmls -B disk.dd                  # partition map with sector offsets
# 0000:  000   Meta    000:001  Safety Table
# 0001:  001   Meta    ...
# 0002:  002   NTFS    2048 .. 204800   <- note the START column (sectors)
fsstat -o 2048 disk.dd           # filesystem details for that partition
fls -o 2048 -r -p disk.dd        # recursive full-path listing; * = deleted
fls -o 2048 -r -p disk.dd | grep -aiE 'flag|secret'    # cheap win
icat -o 2048 disk.dd 34567 > file.bin                 # extract by inode
```

`-o` takes the sector offset from mmls' start column. On NTFS, `fls` shows
both allocated and deleted (`*` prefix); `icat` recovers deleted inodes whose
blocks haven't been reused.

No partition table found (`mmls: Cannot determine partition type`): the image
may be a bare filesystem — try `fsstat disk.dd` directly, or it's a firmware
blob → `triage-tree.md`.

### Recover many files at once

```bash
tsk_recover -e -o 2048 disk.dd out_all/      # -e: allocated + deleted
tsk_recover -a -o 2048 disk.dd out_alloc/    # allocated only
```

### Unallocated space grep

```bash
blkls -o 2048 disk.dd > unalloc.bin          # raw unallocated blocks
strings -n 8 unalloc.bin | grep -aiE 'flag|ctf\{|passw'
binwalk unalloc.bin                          # or carve: foremost -i unalloc.bin -o carve/
```

### Mount (sudo gate — ask first) and alternatives

```bash
sudo mount -o ro,loop,offset=$((2048*512)) disk.dd /mnt    # read-only loop
# E01 via libewf (sudo gate):
sudo ewfmount image.E01 /mnt/ewf              # then mmls/mount the mounted raw
```

No sudo / no mount: `7z x disk.dd -odisk_out/` handles many images (incl.
some partitioned and VHD), or stay in sleuthkit (`fls`/`icat` covers browsing
and extraction without mounting).

### Repair and carve

- `testdisk disk.dd` — rebuild damaged partition tables (interactive, writes
  only when you confirm; sudo gate).
- `photorec disk.dd` — signature carving (photos, docs, archives) from
  damaged filesystems; in "File Opt" enable everything only when you must.

## Windows artifacts from a disk

### Registry hives offline — python-registry

```bash
uv pip install --python .venv/bin/python python-registry
```

```python
#!/usr/bin/env python3
# reg-dump.py <hive> <key path>  — prints values and subkeys
import sys
from Registry import Registry
reg = Registry.Registry(sys.argv[1])
key = reg.open(sys.argv[2].replace('/', '\\'))
for v in key.values():
    data = v.value()
    if isinstance(data, bytes):                 # REG_SZ etc. are UTF-16LE
        try: data = data.decode('utf-16-le').rstrip('\x00')
        except UnicodeDecodeError: data = repr(data)
    print(f"{v.name()} = {data}")
for sub in key.subkeys():
    print(f"[{sub.name()}]  ({sub.timestamp()})")
```

Hive locations on disk: `Windows/System32/config/{SAM,SYSTEM,SOFTWARE}`,
`Users/<user>/NTUSER.DAT`, `Windows/System32/config/USRCLASS.DAT`.

| Question | Hive | Key |
|---|---|---|
| Local users | SAM | `\SAM\Domains\Account\Users\Names` (and `...\Users\<RID>` F value for account metadata) |
| Computer name | SYSTEM | `\ControlSet00X\Control\ComputerName\ComputerName` (X from `\Select\Current`) |
| Last shutdown | SYSTEM | `\ControlSet00X\Control\Windows` (ShutdownTime, FILETIME) |
| Auto-start | SOFTWARE / NTUSER | `...\Windows\CurrentVersion\Run` (both SOFTWARE-wide and NTUSER per-user) |
| Typed paths/commands | NTUSER | `\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU` |
| Recent files | NTUSER | `...\Explorer\RecentDocs` (binary; UTF-16 names in values) |
| Search terms | NTUSER | `...\Explorer\WordWheelQuery` (MRUListEx + UTF-16 values) |
| Program usage | NTUSER | `...\Explorer\UserAssist\{GUID}\Count` (ROT13 key names) |
| USB devices | SYSTEM | `\ControlSet00X\Enum\USBSTOR` (make/serial) |
| Drive letters ↔ volumes | SYSTEM | `\MountedDevices` (\DosDevices\C: -> volume GUID) |

FILETIME → readable: `datetime(1601,1,1) + timedelta(microseconds=ft//10)`.

### Recycle bin ($I/$R pairs)

`$R<name>` holds the content, `$I<name>` the metadata (v2 layout, Win7+):
size at 0x08 (8B LE), deletion FILETIME at 0x10 (8B), name-length in chars at
0x18, original UTF-16 path at 0x1C.

```bash
scripts/ctf python - <<'EOF'
import struct, glob
for f in glob.glob('$RECYCLE.BIN/*/$I*'):
    d = open(f, 'rb').read()
    size = struct.unpack_from('<Q', d, 8)[0]
    nlen = struct.unpack_from('<H', d, 24)[0]
    path = d[28:28 + nlen * 2].decode('utf-16-le')
    print(f, size, path)
EOF
```

### evtx event logs

```bash
uv pip install --python .venv/bin/python python-evtx
scripts/ctf evtx_dump Security.evtx > sec.xml
grep -aiE 'flag|ctf\{' sec.xml
# targeted: logon events
grep -B2 -A6 'EventID="4624"\|EventID="4625"' sec.xml | head -80
```

Library route (per-record XML, filter EventID without a giant file):

```python
from Evtx.Evtx import Evtx
with Evtx('Security.evtx') as e:
    for r in e.records():
        x = r.xml()
        if '4624' in x or 'flag' in x.lower():
            print(x)
```

High-value IDs: 4624/4625 logon success/fail, 4688 process creation (command
lines), 4720 account created, 7045 service installed (System log).

### Browser history (sqlite)

```bash
sqlite3 'History' "SELECT url, title, datetime(last_visit_time/1000000-11644473600,'unixepoch') FROM urls ORDER BY last_visit_time DESC LIMIT 50;"
sqlite3 'History' "SELECT target_path, datetime(start_time/1000000-11644473600,'unixepoch') FROM downloads;"
sqlite3 places.sqlite "SELECT url, title, datetime(last_visit_date/1000000,'unixepoch') FROM moz_places ORDER BY last_visit_date DESC LIMIT 50;"
```

Chrome/Edge/Brave: `History` + `Downloads`; the 11644473600 shifts the 1601
epoch to unix. Firefox: `places.sqlite`. For locked/live profiles, copy the
DB file out first rather than reading it in place.

## Documents

### Office / OLE and OOXML macros — oletools

```bash
uv pip install --python .venv/bin/python oletools
scripts/ctf olevba challenge.doc           # also .docm/.xls/.xlsm/.pptm
scripts/ctf olevba -c challenge.docm       # macro source only
```

`olevba` prints auto-exec triggers, IOC strings, and the deobfuscated macro.
In macro code, hunt for: `AutoOpen/Workbook_Open/Document_Open`,
`Shell`/`WScript.Shell`, `CreateObject`, `WinExec`, `URLDownloadToFile`,
powershell/-enc/base64 blobs, `Environ`, document variables/host strings.
Embedded OLE package files: `scripts/ctf oleobj challenge.doc`.

### OOXML hidden content (docx/xlsx/pptx)

They're zip files — unzip and grep the XML:

```bash
7z x f.docx -odocx_x && grep -rniE 'flag|ctf\{|secret' docx_x/
# hidden text: white-on-white or <w:vanish/>
grep -rn 'FFFFFF\|w:vanish' docx_x/word/document.xml
# hidden sheets (xlsx): xl/workbook.xml sheet entries
grep -o '<sheet [^>]*state="[^"]*"' docx_x/xl/workbook.xml
# all cell strings incl. unused: xl/sharedStrings.xml
strings docx_x/xl/sharedStrings.xml | grep -i flag
```

Also check `word/settings.xml` (rsid leak), `docProps/` (author/company),
and `word/glossary/document.xml` (auto-text storage — a classic hiding spot).

### PDF

```bash
qpdf --qdf --object-streams=disable f.pdf flat.pdf   # decompress all streams
grep -aoE '/(EmbeddedFile|JavaScript|JS|OpenAction|Launch|AA|URI)[^0-9A-Za-z]' flat.pdf | sort | uniq -c
strings -n 6 flat.pdf | grep -aiE 'flag|ctf\{|http'
```

- `/EmbeddedFile` → carve the bytes between `stream` and `endstream`, then
  `file` the carve (or `binwalk flat.pdf`).
- `/OpenAction` + `/JS` → auto-running JavaScript; extract the JS string and
  read it (frequent flag-drop or a dropper URL).
- pdf-parser.py (Didier Stevens, single-file tool from the DidierStevensSuite
  GitHub repo; not on PyPI): `python pdf-parser.py -s flag flat.pdf` lists
  matching objects, `-o <n>` prints one object.
- peepdf exists on PyPI (0.4.2, 2015-era); it often fails to install on
  Python 3.12 — prefer the qpdf + pdf-parser.py route.
- Signature "forgery" PDFs: compare /ByteRange coverage; outside scope for
  most CTFs — check the ByteRange gap with `qpdf --qdf` output.

### Slack and wiped space

- File slack (rest of the last block) and $LogFile/$UsnJrnl (NTFS journals)
  carry deleted-name and timestamp residue: `fls -o 2048 -d disk.dd` lists
  deleted entries only, and `icat -o 2048 disk.dd <inode>-128-2`-style
  attribute streams when hunting named streams.
- Wiped-but-reallocated files still show in `$MFT` — `fls` then `icat` beats
  photorec when the filesystem is intact.

## Logs (plain challenge log files)

```bash
grep -aiE 'flag\{|ctf\{' access.log app.log
grep -a 'Accepted password' auth.log | head       # ssh logins
grep -a 'Failed password' auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -rn
# timeline: normalize timestamps, sort
grep -an 'user' auth.log | cut -d: -f1 | head     # then read around hits with sed -n 'X,Yp'
```

Correlate: log timestamps ↔ registry ShutdownTime ↔ browser history ↔ evtx
4624 events — one coherent story usually contains the flag.
