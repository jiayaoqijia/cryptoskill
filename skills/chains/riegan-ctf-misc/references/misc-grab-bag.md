# Misc grab-bag — QR, documents, code systems, identifiers, formats, hardware

Everything here is a 5-to-30-minute technique. Table first, recipes after.

| Artifact / signal | Technique | Section |
|---|---|---|
| damaged/inverted/scaled QR | decode retries, repair, rebuild | QR |
| PDF with hidden layers/JS | text+object extraction | PDF |
| macOS `.plist`, base64 blobs | plistlib decode | Plists |
| dots/dashes | morse table | Code systems |
| numbers in pairs like `4 4 / 1 3` | tap code (Polybius) | Code systems |
| stick-figure arms | semaphore (ANBG table) | Code systems |
| colored maritime flags | ICS flag table | Code systems |
| UUID string | v1 → MAC + timestamp leak | Identifiers |
| ISBN with missing digit | checksum math | Identifiers |
| `38°53'21.7"N 77°02'08.5"W` etc. | GPS format conversion | Formats |
| file that is two files | tar/zip polyglot | Formats |
| `.v` file, SDR capture, logic trace | iverilog / rtl_433 / sigrok | Hardware |

## QR

Decode ladder (stop at first success), `zbarimg` is on this host (v0.23.95):

```bash
zbarimg --raw qr.png                      # plain decode
zbarimg --raw -Sdip 5 qr.png              # optional: try other scanner inits
python3 - <<'EOF'                         # repair variants, then re-run zbarimg per file
from PIL import Image
im = Image.open("qr.png").convert("L")
im.resize((im.width*4, im.height*4), Image.NEAREST).save("qr_big.png")   # upscale
im.point(lambda p: 255-p).save("qr_inv.png")                              # inverted
im.point(lambda p: 255 if p>128 else 0).save("qr_bw.png")                 # hard threshold
im.rotate(90).save("qr_rot90.png")
EOF
```

`PIL` (pillow) lives in the repo `.venv` (`scripts/setup.sh`); run via
`scripts/ctf python`.

Repair theory, in order of likelihood: (1) **quiet zone** — add a 4-module
white border; (2) **mask/pattern damage** — finder patterns (3 corners) must
be intact or reconstruction is guesswork; (3) **reversed modules**; (4)
**rotation/perspective**; (5) partial damage — Reed–Solomon covers
`floor((ec_level_chars)/2)` codeword errors, so up to ~25% damage can still
decode at level H: fix the *geometry* and let RS do the rest. Rebuilding the
image with the python `qrcode` module (documented: `uv pip install --python
.venv/bin/python qrcode`) from recovered module grid also works; grid =
sample each module center pixel after deskewing.

## PDF

```bash
pdftotext -layout file.pdf -              # text layer (host has poppler)
pdftotext -raw file.pdf -                 # different order, sometimes reveals hidden text
qpdf --qdf --show-object=1-10 file.pdf -  # raw objects; qpdf: sudo pacman -S qpdf
qpdf --show-xref file.pdf                 # object map — spot objects the viewer never shows
```

Checklist: text drawn white-on-white (`pdftotext` still extracts it — the
*renderer* hides it, not the file); objects beyond the xref the viewer uses;
embedded files (`/EmbeddedFile` — grep the qdf output); JavaScript
(`/JS`, `/JavaScript`); deleted-but-present pages (object present, xref stale).

## Plists and base64 blobs

macOS/xml or binary plists, common in mac forensics/misc:

```python
import plistlib, base64
data = plistlib.load(open("file.plist", "rb"))
# then walk: keys named Base64Data/Data are usually base64 of the real payload
open("out.bin","wb").write(base64.b64decode(data["Base64Data"]))
```

Generic base64 blob ladder: base64 → hex → gzip/zlib (starts `1f 8b` / `78 9c`)
→ try as image (`file out.bin`). `.venv` has pycryptodome for the rest.

## Code systems

Morse (ITU): `.- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. --
-. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --..`
digits: `1=·---- 2=··--- 3=···-- 4=····- 5=····· 6=-···· 7=--··· 8=---··
9=----· 0=-----`. Separator conventions: letter gap = single space (or `/` in
some writeups), word gap = `/` or 3 spaces — try both when decoding fails.

Tap code (5x5 Polybius, C and K share a cell):

```
     1   2   3   4   5
1    A   B   C/K D   E
2    F   G   H   I   J
3    L   M   N   O   P
4    Q   R   S   T   U
5    V   W   X   Y   Z
```

Pairs `<row><col>`, e.g. `4 4` = T. Delivered as knocks, x/y lists, or
"11 34"-style numbers.

Semaphore (verified against the ANBG chart): positions — down=6:00,
low=4:30(RH)/7:30(LH), out=3:00(RH)/9:00(LH), high=1:30(RH)/10:30(LH),
up=12:00; "across" = hand crosses the body midline.

| Letter | LH position; RH position | Letter | LH; RH |
|---|---|---|---|
| A / 1 | down; low | N | low; low |
| B / 2 | down; out | O | across high; out |
| C / 3 | down; high | P | up; out |
| D / 4 | down; up (or inverse) | Q | high; out |
| E / 5 | high; down | R | out; out |
| F / 6 | out; down | S | low; out |
| G / 7 | low; down | T | up; high |
| H / 8 | across low; out | U | high; high |
| I / 9 | across low; up | V | low; up |
| J | out; up | W | out; across high |
| K / 0 | up; low | X | low; across high |
| L | high; low | Y | out; high |
| M | out; low | Z | out; across low |

(Numerical sign = LH high, RH up; annul = LH low, RH high.)

Maritime signal flags (International Code of Signals; colors verified against
the standard table — left/right = hoist/fly):

| L | Flag | | L | Flag |
|---|---|---|---|---|
| A | swallowtail, white/blue halves; "diver down" | | N | blue/white 4x4 checker; "negative" |
| B | all-red swallowtail; dangerous cargo | | O | diagonal red(upper hoist)/yellow; "man overboard" |
| C | blue, red horizontal band edged white | | P | blue, white box ("Blue Peter") |
| D | yellow, wide blue horizontal band | | Q | all yellow ("yellow jack") |
| E | blue over red horizontal | | R | red, yellow cross |
| F | white, red diamond; "disabled" | | S | white, blue box |
| G | 6 vertical yellow/blue stripes; "need pilot" | | T | vertical red/white/blue |
| H | white/red vertical halves; "pilot aboard" | | U | red/white quarters; "running into danger" |
| I | yellow, black disc | | V | white, red saltire (X); "require assistance" |
| J | blue, white horizontal band; "fire" | | W | blue, red box edged white; "medical assist" |
| K | yellow/blue vertical halves; "wish to comm" | | X | white, blue cross |
| L | yellow/black quarters; "stop vessel" | | Y | diagonal yellow/red stripes; "dragging anchor" |
| M | blue, white saltire; "stopped" | | Z | four triangles: top yellow, hoist black, fly red, bottom blue; "need tug" |

## Identifiers

UUID v1 leaks **creation time and MAC** (verified decoder math):

```python
import uuid, datetime
u = uuid.UUID("xxxxxxxx-xxxx-1xxx-xxxx-xxxxxxxxxxxx")   # version nibble = 1
ticks = u.time_low | (u.time_mid << 32) | (u.time_hi_version << 48)  # 100ns since 1582-10-15
t = datetime.datetime(1582,10,15) + datetime.timedelta(microseconds=ticks//10)
mac = ":".join(f"{b:02x}" for b in u.node.to_bytes(6,"big"))         # node field = MAC (or random multicast if v4-style)
```

Other UUID versions: v3 = MD5-namespaced (brute the name), v4 = random,
v5 = SHA1-namespaced (brute with a wordlist via `uuid.uuid5(ns, guess)`).

ISBN checksums (verified):
- ISBN-13: `sum(digit * (1 if i%2==0 else 3)) % 10 == 0`; solve the missing
  digit algebraically (each position has a known weight).
- ISBN-10: `sum((10-i)*d_i) % 11 == 0`; last char may be `X` (=10). Missing
  digit: one linear equation, solve mod 11.

GPS formats — convert everything to decimal degrees (DD):
- DMS `38°53'21.7"N` → `38 + 53/60 + 21.7/3600` = 38.889...  (sign from hemisphere)
- DDM `38°53.36'N` → `38 + 53.36/60` (geocache/aviation standard)
- DD `38.889361` (what map sites want)
Trailing zeros in DDM minutes are significant for geohash-style precision
puzzles. Format-hint: 2-digit minutes → DDM; seconds present → DMS.

## Formats and polyglots

tar+zip polyglot (verified): `cat a.tar b.zip > poly.bin` — tar reads from
offset 0 and stops at its end-of-archive marker; zip readers scan the
End-Of-Central-Directory from the file tail. `tar -tf` and `7z l`/`unzip -l`
both list their own member from the same file. Reverse order
(`cat a.zip b.tar`) breaks tar (zip header at offset 0) unless the zip is
appended after with padding. Check both directions when a file misbehaves.

Quick triage for any file: `file`, `xxd | head`, `binwalk` (after install),
`7z l` — polyglots show up as "two formats disagree".

## Hardware-adjacent

| Signal | Tool | Note |
|---|---|---|
| ISM-band RF captures (433/868 MHz, `.cu8`/`.iq`) | `rtl_433` (needs RTL-SDR dongle; `sudo pacman -S rtl-sdr` + build rtl_433) | if no hardware: the challenge usually ships a capture file — `rtl_433 -r capture.cu8` still decodes offline |
| logic analyzer traces (`.sr`, `.sal`, `.vcd`) | sigrok/pulseview: `sudo pacman -S sigrok` | PulseView GUI in podman if needed; `sigrok-cli` for headless protocol decode |
| HDL puzzle (`.v` verilog) | iverilog: `sudo pacman -S iverilog`, then `iverilog -o sim.vvp top.v && vvp sim.vvp` | testbench usually provided; if not, write one that prints the flag condition |
| serial console captures | baudrate guessing (300..115200), 8N1 first; python `serial` in `.venv` | inverted-TTL logic: XOR bytes with 0xFF |

Radio/HDL puzzles without hardware: the capture file is the challenge;
decoding it locally is always allowed.
