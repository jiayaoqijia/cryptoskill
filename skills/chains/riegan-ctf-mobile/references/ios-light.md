# iOS-light — what is actually doable on Linux

Honest scope: without a Mac and without a jailbroken device, iOS work is static
analysis plus data-file carving. Dynamic instrumentation (frida), keychain dumps and
FairPlay decryption all require a device. Plan accordingly: most iOS CTF challenges
that ship an `.ipa` expect static work, a bundled secret, or an encrypted archive
whose key is in the binary.

`$ROOT` = the ctf repo root, as in `references/android-dynamic.md`; `scripts/ctf`
is the repo's venv launcher.

| Want | Linux-only? | Path |
|---|---|---|
| unzip ipa, read bundle | yes | §1 |
| Info.plist (URL schemes, ATS, versions) | yes | §2 |
| strings / ObjC class names | yes | §3 |
| Mach-O analysis (archs, symbols, disasm) | yes (limited) | lief, ghidra via `ctf-rev` |
| Swift class dump like class-dump | no | class-dump is macOS tooling; Swift demangling is its own project — accept symbols+strings |
| sqlite/plist/other data files in bundle | yes | sqlite3, python plistlib |
| Encrypted-binary decryption (FairPlay) | no | needs jailbroken device (frida-ios-dump & friends) |
| keychain dump | no | needs jailbroken device |
| frida at runtime | jailbroken device, or repackage + sideload (§5) | messy on Linux |

## 1. ipa = zip

```bash
file dist/app.ipa                 # zip
unzip -l dist/app.ipa | head -40  # Payload/App.app/...
unzip -q dist/app.ipa -d ipa-out/
B=ipa-out/Payload/App.app         # adjust App name
ls -la "$B"
```

Interesting bundle entries: the main binary (`$B/App` — same name as the `.app`),
`embedded.mobileprovision`, `Info.plist`, `*.strings`/`*.car` resources, bundled
sqlite/db/json/plist data, `Frameworks/` (embedded dylibs — sometimes the whole
challenge), `Assets.car` (asset catalog; strings still leak names).

## 2. Info.plist on Linux (stdlib, no Mac tools)

```bash
scripts/ctf python - "$B/Info.plist" <<'PY'
import plistlib, sys, json
with open(sys.argv[1], 'rb') as f:
    p = plistlib.load(f)
for k in ('CFBundleIdentifier', 'CFBundleShortVersionString', 'MinimumOSVersion'):
    print(k, '=', p.get(k))
print('URL schemes:', [s.get('CFBundleURLSchemes')
                       for s in p.get('CFBundleURLTypes', [])])
ats = p.get('NSAppTransportSecurity')
if ats:
    print('ATS overrides:', json.dumps(ats, indent=1, default=str))
PY
```

`NSAllowsArbitraryLoads` / `NSAllowsLocalNetworking` in ATS = the app tolerates
cleartext/local endpoints (relevant if a device-side proxy story exists).
`embedded.mobileprovision` is a CMS-wrapped plist — crude but effective extraction:

```bash
strings "$B/embedded.mobileprovision" | sed -n '/<?xml/,/<\/plist>/p' > provisioning.plist
```

(that file only exists for dev-signed builds; App-Store builds ship none.)

## 3. Binary triage

```bash
file "$B/App"                       # "Mach-O universal binary" or single-arch
strings -n 8 "$B/App" | grep -aiE 'flag|ctf\{|key|token|http' | head -50
strings "$B/App" | grep -aE '^(NS|_TtC|__objc)' | head -40   # ObjC/Swift class names
```

Better structure via lief (already in the shared venv):

```bash
scripts/ctf python - "$B/App" <<'PY'
import lief, sys
fat = lief.MachO.parse(sys.argv[1])
for b in fat:
    print('cpu:', b.header.cpu_type, '  ncmds:', len(b.commands))
    syms = b.symbols
    print('symbols:', len(syms))
    for s in list(syms)[:40]:
        print('  ', s.name)
PY
```

ObjC selectors and class names live in `__objc_methname` / `__objc_classname`
sections even in App-Store builds — strings finds them; ghidra (Mach-O + Objective-C
support) takes it from there. Swift metadata is harder: symbol names carry type
info (`$s...` mangled) but don't expect class-dump quality. Deep binary work →
sibling skill `ctf-rev`.

## 4. Data files in the bundle

```bash
find "$B" -name '*.sqlite' -o -name '*.db' -o -name '*.plist' -o -name '*.json' | tee bundle-data.txt
sqlite3 <db> '.tables'; sqlite3 <db> '.dump' | head
grep -rIaE 'AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|eyJ[A-Za-z0-9_-]{8,}\.' "$B" ..
```

Same secret-pattern table as `references/android-recon.md` §5 — reuse it.

FairPlay check: if `lief`/ghidra show the `LC_ENCRYPTION_INFO` load command with
`cryptid == 1`, the main binary's text segment is encrypted and static disasm of it
is garbage until decrypted on a jailbroken device (frida-ios-dump and friends —
needs device + Apple tooling; on Linux you can only note it and pivot to other
artifacts: resources, data files, network captures if provided).

## 5. Dynamic, if you ever get a device

- frida on iOS needs a jailbroken device (add `https://build.frida.re` in
  Cydia/Sileo, install frida-server; then `frida-ps -Uai`, same host tooling as
  Android — see `references/android-dynamic.md`).
- No jailbreak → repackage the ipa with a frida gadget:
  1. unzip, copy `FridaGadget.dylib` (from frida releases, ios-universal) into
     `App.app/`, use `insert_dylib` (github.com/Tyilo/insert_dylib) to add it to the
     binary's load commands,
  2. ad-hoc sign everything with `ldid -S` — ldid runs on Linux (AUR package;
     not in official repos) and produces the entitlements-bearing pseudo-signature
     iOS checks at load; real distribution signing still needs macOS codesign,
  3. install to a device — which requires a provisioning profile that trusts your
     cert; on Linux that means an Apple developer account + a signing-service
     workflow (AltStore/SideStore family, or `ideviceinstaller` from the
     libimobiledevice suite if the device is dev-provisioned).
- Keychain dumps (keychain-dumper class of tools) and app-data pulls need a
  jailbroken device too — there is no Linux shortcut.

Reality check: if a challenge hands you an ipa on a Linux-only team box, the flag is
almost always in the static layer (bundled secret, plist/sqlite, weakly-obfuscated
string in the binary) or the challenge also provides a remote endpoint that
compensates. Exhaust §1–§4 before wishing for a Mac.

## 6. Toolbox (iOS additions)

| Tool | Install | Purpose |
|---|---|---|
| ldid | AUR (`paru -S ldid`) | ad-hoc codesigning on Linux |
| lief / plistlib | lief in shared venv; plistlib stdlib | Mach-O parsing; plists |
| sqlite | `sudo pacman -S sqlite` | bundle databases |
| insert_dylib | build from github.com/Tyilo/insert_dylib | add LC_LOAD_DYLIB for gadget |
| libimobiledevice suite | `sudo pacman -S libimobiledevice usbmuxd` (check what your image ships) | device comms, if any iOS hardware shows up |
