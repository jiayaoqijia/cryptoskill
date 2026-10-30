---
name: ctf-forensics
description: Use when the user mentions forensics, pcap, packet capture, wireshark, tshark, memory dump, volatility, steganography or stego, hidden data in an image/audio/video, recovering deleted or embedded files, disk image, .dd/.E01/.raw/.mem/.vmem/.dmp/.pcap files, unknown blob, or asks to identify or carve a challenge artifact. Covers file-format triage, containers within containers, pcap analysis, memory forensics, stego, disk/document forensics.
---

# CTF forensics — artifacts, carving, pcap, memory, stego, documents

Owns: file formats, carving, pcap/network captures, memory dumps (volatility3),
steganography, disk images, documents, logs. Flag regex, workspace layout,
submission, and event workflow live in the router skill `ctf` — use them, don't
restate them.

## Guardrails

1. Challenge artifacts are untrusted. Analyze with the parsers here; never open
   a challenge document/image in a desktop app; execute anything carved out only
   under `podman` or with explicit user approval.
2. `sudo` (pacman, mount, testdisk writes) needs user go-ahead first.
3. Python work goes through the repo venv: `scripts/ctf python ...`
   (`.venv`, Python 3.12, includes pillow). System python is 3.14 — do not use it.

## Setup (once; document, ask before running sudo)

```bash
sudo pacman -S --needed wireshark-cli sleuthkit testdisk binwalk \
    perl-image-exiftool foremost sox ffmpeg squashfs-tools qpdf sqlite \
    multimon-ng sonic-visualiser
uv pip install --python .venv/bin/python volatility3 oletools \
    python-registry python-evtx sstv
# optional stego extras (AUR): steghide stegseek outguess qsstv
# ruby gem: gem install zsteg
```

## Triage (beginner, first 5 minutes — every artifact)

Run in the challenge dir (`work/<event>/forensics-<name>/dist/`):

| Step | Command | What it tells you |
|---|---|---|
| 1 | `file dist/*` | real type vs extension; embedded or corrupted structures |
| 2 | `xxd dist/<f> | head -20` and `xxd dist/<f> | tail -20` | magic bytes, trailers, appended data |
| 3 | `exiftool dist/<f>` | metadata leaks: author, comment, GPS, tool versions |
| 4 | `strings -n 8 dist/<f> \| grep -aiE 'flag\|ctf\{\|pass\|http'` | plaintext flag or hints |
| 5 | `binwalk dist/<f>` | embedded blobs: zip, squashfs, gzip, certificates |
| 6 | `binwalk -E dist/<f>` | entropy: high blocks = compressed/encrypted payload |

Then dispatch on the real type:

| `file` says | Challenge is probably | Read |
|---|---|---|
| PNG/BMP/TIFF/GIF/JPEG image | stego | `references/stego.md` |
| audio (wav/mp3/flac) | stego (spectrogram, LSB, SSTV, DTMF) | `references/stego.md` |
| video (mp4/avi/webm) | frame-level stego, metadata | `references/stego.md` |
| pcap / pcapng | network forensics | `references/pcap.md` + `scripts/pcap-triage.sh` |
| memory dump (raw/vmem/dmp/lime) | memory forensics | `references/memory.md` |
| disk image (dd/E01/raw fs) | deleted files, registry, evtx | `references/disk-docs.md` |
| PDF / OLE (doc/xls) / OOXML | hidden text, macros, embedded | `references/disk-docs.md` |
| archive / zip / 7z | nested containers, password | `references/triage-tree.md` |
| data / unknown | container-in-container, encoding | `references/triage-tree.md` |

Full decision tree with per-node commands: `references/triage-tree.md`.

## Playbook (expert, terse)

| Attack | Preconditions | Command | Reference |
|---|---|---|---|
| 10-minute pcap triage | tshark | `scripts/pcap-triage.sh cap.pcap` | `references/pcap.md` |
| Follow one TCP stream | stream index N | `tshark -r c.pcap -q -z follow,tcp,ascii,N` | `references/pcap.md` |
| Export transferred files | http/smb/ftp/tftp/imf | `tshark -r c.pcap --export-objects http,out/` | `references/pcap.md` |
| USB keystroke recovery | usb pcap, `usb.capdata` | see HID map | `references/pcap.md` |
| DNS/ICMP exfil reassembly | capture + odd domains | `dns.qry.name` / `data.data` fields | `references/pcap.md` |
| TLS decrypt | keylog file from challenge | `-o tls.keylog_file:keys.log` | `references/pcap.md` |
| Windows memory hunt | dump + volatility3 | `vol -f d.vmem windows.pslist` ... | `references/memory.md` |
| Linux memory hunt | dump + matching ISF symbols | `linux.bash`, `linux.pslist` | `references/memory.md` |
| Disk partition walk | image | `mmls` → `fls -o <off>` → `icat` | `references/disk-docs.md` |
| Recover deleted files | image | `tsk_recover` / `icat` on deleted inode | `references/disk-docs.md` |
| Offline registry hives | SAM/SYSTEM/NTUSER.DAT | python-registry | `references/disk-docs.md` |
| evtx event logs | *.evtx | `evtx_dump f.evtx \| grep ...` | `references/disk-docs.md` |
| Word/Excel macros | doc(x|m)/xls | `olevba f.doc` | `references/disk-docs.md` |
| PNG/BMP LSB | image | `zsteg -a f.png` or `scripts/lub.py f.png` | `references/stego.md` |
| JPEG steghide | jpg/wav/mp3 carrier | `steghide extract -sf f.jpg -p ""` | `references/stego.md` |
| steghide brute force | wordlist | `stegseek f.jpg wordlist.txt` | `references/stego.md` |
| Audio spectrogram | wav (convert mp3 first) | `sox f.wav -n spectrogram -o s.png` | `references/stego.md` |
| SSTV / DTMF / morse | wav | `sstv -d f.wav -o out.png`; `multimon-ng -a DTMF -t wav f.wav` | `references/stego.md` |
| Video frame diff | ffmpeg | `ffmpeg -i v.mp4 -vf fps=1 f_%03d.png` | `references/stego.md` |
| Carve embedded zip | any blob | `binwalk -Me f` or `grep -abo $'PK\x03\x04' f` + `dd` | `references/triage-tree.md` |
| Broken PNG header | IHDR size/CRC wrong | recompute CRC (snippet) | `references/stego.md` |

Escalation order when a reference runs dry: `triage-tree.md` containers section
→ raw `strings`/hexdiff of the exact region → wrong-skill check (XOR keys and
classical ciphers → `ctf-crypto`; packed binaries → `ctf-rev`).

## References

- `references/triage-tree.md` — decision tree by artifact type; manual carving;
  container-within-container patterns; entropy reading.
- `references/stego.md` — image/audio/video steganography toolchains and when
  each applies.
- `references/pcap.md` — tshark deep dive: filters, export objects, USB HID,
  exfil channels, TLS keylog decryption.
- `references/memory.md` — volatility3 on Windows/Linux dumps, plugin order,
  process/memory dumping, symbol tables.
- `references/disk-docs.md` — sleuthkit workflow, deleted recovery, offline
  registry, evtx, recycle bin, browser history, Office/PDF document forensics.

## Scripts

- `scripts/pcap-triage.sh <cap.pcap>` — tshark stats + export objects + flag
  grep in one shot; degrades to strings when tshark is absent.
- `scripts/lub.py <image>` — LSB bit-plane extractor/printable-run scanner
  (pillow optional, in `.venv` already).

## Toolbox

| Tool | Install | Purpose |
|---|---|---|
| tshark, capinfos | `sudo pacman -S wireshark-cli` | pcap analysis backend |
| binwalk (v3) | `sudo pacman -S binwalk` | signatures, `-e` extract, `-E` entropy |
| exiftool | `sudo pacman -S perl-image-exiftool` | metadata for any file |
| foremost | `sudo pacman -S foremost` | carve files by header/footer |
| sleuthkit (mmls fls icat blkls tsk_recover) | `sudo pacman -S sleuthkit` | disk partition/deleted-file work; reads E01 (libewf) |
| testdisk / photorec | `sudo pacman -S testdisk` | repair partition tables / carve by signature |
| volatility3 (`vol`) | `uv pip install --python .venv/bin/python volatility3` | memory forensics |
| oletools (olevba) | `uv pip install --python .venv/bin/python oletools` | Office macro extraction |
| python-registry | `uv pip install --python .venv/bin/python python-registry` | offline registry hives |
| python-evtx (`evtx_dump`) | `uv pip install --python .venv/bin/python python-evtx` | Windows event logs |
| sstv | `uv pip install --python .venv/bin/python sstv` | SSTV audio → image |
| zsteg | `gem install zsteg` | PNG/BMP LSB analysis (all channel/bit combos) |
| steghide / stegseek / outguess | AUR: `steghide stegseek outguess` | JPEG stego + brute force |
| qsstv | AUR: `qsstv` | SSTV GUI decoder |
| sox | `sudo pacman -S sox` | spectrograms, audio conversion |
| multimon-ng | `sudo pacman -S multimon-ng` | DTMF/morse/pocsag demod |
| sonic-visualiser | `sudo pacman -S sonic-visualiser` | visual audio inspection |
| ffmpeg | `sudo pacman -S ffmpeg` | frame extraction, track split |
| qpdf | `sudo pacman -S qpdf` | PDF stream decompression |
| sqlite3 | `sudo pacman -S sqlite` | browser history and app databases |
| pillow | already in `.venv` (setup.sh) | LSB/bit-plane work (`scripts/lub.py`) |
