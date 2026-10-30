# Android static recon — from APK to understanding

All commands assume you are in the challenge dir with the APK in `dist/`.
Static analysis only — nothing here executes challenge code.

## 1. APK is a zip — first contact

```bash
file dist/base.apk                 # "Zip archive data" expected
unzip -l dist/base.apk | head -50  # overview
unzip -Z1 dist/base.apk > file-list.txt   # plain names, one per line
sha256sum dist/base.apk            # record in notes.md
```

Quick counts from `file-list.txt`:

```bash
grep -cE '^classes[0-9]*\.dex$' file-list.txt   # dex count
grep -oE '^lib/[^/]+/' file-list.txt | sort -u  # ABIs present (arm64-v8a, armeabi-v7a, x86, x86_64)
grep -E '^assets/' file-list.txt | head -30     # app data
grep -E '^res/raw/' file-list.txt               # raw blobs — `file` each
```

ABI note: an APK with only `arm64-v8a`/`armeabi-v7a` libs will not run on an x86_64
emulator/waydroid image unless the image ships ARM translation (libhoudini /
ndk_translation — not guaranteed). Pure-Java APKs run anywhere. Check before
choosing a run environment (`references/android-dynamic.md`).

## 2. Split bundles (.xapk / .apkm / .apks)

All are zip containers of several APKs. `unzip` them, analyze `base.apk` — but keep
the splits: resources/other dex often live in `split_config.*.apk`. To install on a
device: `adb install-multiple base.apk split_config.arm64_v8a.apk ...`.

## 3. apktool — manifest, resources, smali

```bash
sudo pacman -S apktool        # once
apktool d dist/base.apk -o apk-tool/
```

What you get:

| Path | Content |
|---|---|
| `AndroidManifest.xml` | decoded manifest (readable XML) |
| `res/`, `assets/` | decoded resources incl. `res/values/strings.xml`, xml configs |
| `smali*/, `smali_classes2/` … | dalvik bytecode (per-dex) — greppable |
| `apktool.yml` | apktool metadata |

Resources-only pass (fast, no smali): `apktool d -s dist/base.apk -o apk-tool/`.

### Manifest checklist (the CTF attack surface)

```bash
M=apk-tool/AndroidManifest.xml
grep -Eo 'package="[^"]+"' "$M"
grep -E 'android:debuggable|android:allowBackup|usesCleartextTraffic|networkSecurityConfig' "$M"
grep -nE '<(activity|service|receiver|provider)' "$M"
grep -nE 'android:exported="true"' "$M"
grep -Eo 'android:scheme="[^"]+"' "$M"          # deep-link schemes
grep -Eo '<uses-permission [^>]+>' "$M"
grep -Eo 'android:authorities="[^"]+"' "$M"     # content provider ids
```

Reading notes:

- `android:exported`: targeting SDK 31+ forces an explicit value on components with
  intent-filters. Below that, an intent-filter **implies exported** — a component with
  `<intent-filter>` and no `exported="false"` is reachable even without the attribute.
- `debuggable="true"` → `adb shell run-as <pkg> ...` reads the app's private data
  without root (see vulns ref).
- `networkSecurityConfig` → trust anchors / user CAs (see vulns ref "Cert issues").
- Provider `authorities` = the string in `content://<authority>/...`.

## 4. jadx — dex to readable Java

```bash
# one-time install: download the release zip, needs Java 11+ (host has 21)
mkdir -p ~/tools && cd ~/tools
curl -LO https://github.com/skylot/jadx/releases/latest/download/jadx.zip
unzip jadx.zip -d jadx          # creates bin/jadx, bin/jadx-gui, lib/
~/tools/jadx/bin/jadx -d jadx-out dist/base.apk      # batch decompile
~/tools/jadx/bin/jadx-gui dist/base.apk               # interactive, has search
```

jadx-gui beats batch for CTF: full-text search (`Ctrl+Shift+F` in newer builds),
xref navigation, "find usage". Batch output is greppable:

```bash
grep -rn 'SecretKeySpec\|IvParameterSpec\|Cipher.getInstance' jadx-out/sources
grep -rn 'addJavascriptInterface\|setJavaScriptEnabled' jadx-out/sources
grep -rn 'getParcelableExtra\|PendingIntent' jadx-out/sources
grep -rn 'http://' jadx-out/sources                   # cleartext endpoints
grep -rn 'Log\.[devwi](' jadx-out/sources | head -40  # logging of secrets
```

First files to open: the launcher activity from the manifest
(`<category android:name="android.intent.category.LAUNCHER"/>`), any `*Application`
subclass, and the biggest package under the app's own namespace.

Smali (apktool) vs jadx: use jadx for reading, smali for confirming exact bytecode
when decompilation lies (jadx sometimes produces pseudo-code that does not match).

## 5. Secret sweep (the whole APK tree)

`scripts/apk-triage.sh` runs this automatically; the pattern list for manual sweeps:

| Pattern (ERE) | Meaning |
|---|---|
| `AKIA[0-9A-Z]{16}` | AWS access key id |
| `AIza[0-9A-Za-z_-]{35}` | Google/Firebase API key |
| `ghp_[0-9A-Za-z]{36}` | GitHub classic PAT |
| `xox[baprs]-[0-9A-Za-z-]{10,}` | Slack token |
| `sk_live_[0-9a-zA-Z]{20,}` | Stripe live secret key |
| `-----BEGIN [A-Z ]*PRIVATE KEY-----` | embedded private key |
| `eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.` | JWT (header.payload.) |
| `https?://[A-Za-z0-9._~:/?#@!$&*+,;=%-]+` | endpoints (dedupe with `sort -u`) |
| `(api[_-]?key|apikey|secret|token|passw(or)?d)["' ]*[:=]` | named secrets (grep `-i`) |
| `firebaseio\.com|firebaseapp\.com|appspot\.com` | Firebase footprint |
| `[a-zA-Z0-9_]{2,16}\{[^}]{4,}\}` | CTF flag wrapper |

Where to grep: the extracted tree (`unzip` output incl. dex/so with `grep -a`),
`jadx-out/`, `apk-tool/res/values/strings.xml`, `apk-tool/res/xml/*.xml`
(FileProvider paths, network security config). Base64 blobs are only worth chasing
when their name/context implies a key (e.g. `ENCRYPT_KEY = "..."`).

## 6. Firebase / google-services.json

`assets/google-services.json` (or `res/values/values.xml` entries after apktool)
hands you `project_id`, `api_key/current_api_key`, `database_url`,
`storage_bucket`. Probes (REMOTE GATE — ask before touching the network):

```bash
curl -s "https://<project_id>.firebaseio.com/.json?shallow=true"   # open RTDB?
curl -s "https://<project_id>.firebaseio.com/flag/.json"           # direct guess
curl -s "https://storage.googleapis.com/<bucket>"                  # listable bucket?
```

Open rules (common CTF gift) leak the whole DB; `401/permission denied` means rules
hold. Also try `https://<project_id>-default-rtdb.<region>.firebasedatabase.app/.json`
for newer projects.

## 7. Native libraries → hand to ctf-rev

```bash
for so in apk-tool/lib/arm64-v8a/*.so; do file "$so"; nm -D "$so" 2>/dev/null | head; done
```

- JNI exports are named `Java_com_example_pkg_ClassName_methodName` — map them to
  the Java side in jadx, then reverse the body in ghidra (`ctf-rev`).
- `strings -n 8 libfoo.so | grep -aiE 'flag|key|http'` first; many CTF natives leak.
- Anything deeper (stripped, obfuscated, custom VM) is `ctf-rev` territory — link
  `../ctf-rev/SKILL.md` in notes and stop duplicating work here.

## 8. Framework-specific paths

| Framework | Recognize by | Extract logic with |
|---|---|---|
| Flutter | `lib/<abi>/libapp.so` (Dart AOT snapshot) + `libflutter.so` | blutter (`github.com/worawit/blutter`): arm64 only, needs the matching Dart SDK bits per its README; emits class dumps + asm + a frida script. Dart snapshot version must match — check the `--snapshot-version` string in `libflutter.so`. |
| React Native (JSC) | `assets/index.android.bundle`, plain JS | read it: `js-beautify` or just search it — logic, endpoints, secrets in the clear |
| React Native (Hermes) | bundle starts with Hermes bytecode (magic `c6 1f bc 03`), `strings` mostly useless | hbctool / hermes-dec (`github.com/P1sec/hermes-dec`) disassemble; or hook at runtime with frida (dart/JS runtime strings) |
| Cordova/Ionic | `assets/www/index.html` + JS | the `www/` tree is the app — read JS |
| Unity IL2CPP | `lib/<abi>/libil2cpp.so` + `assets/bin/Data/Managed/Metadata/global-metadata.dat` | Il2CppDumper (`github.com/Perfare/Il2CppDumper`, runs on .NET) → dummy DLLs + script.json → decompile DLLs with `ctf-rev` dotnet tooling |
| Unity Mono | `assets/bin/Data/Managed/Assembly-CSharp.dll` | straight to `ctf-rev` dotnet (ILSpy family) |
| Godot | `assets/*.pck` (or `.pck` appended to the exe-style so) | pck extractors: GodotPckTool; gdsdecomp recovers scripts/scenes |
| React Native alternatives, KMP, etc. | dex-only or JS in assets | jadx + asset JS |

## 9. Obfuscation recovery

- **ProGuard/R8**: classes become `a.b.c`. If the challenge ships `mapping.txt`
  (sometimes inside the APK or in the dist zip), map names back by hand — grep
  `mapping.txt` for the obfuscated name seen in jadx. Logic still reads fine without
  the map; only names are gone. String constants are NOT obfuscated by ProGuard.
- **String encryption**: a class with a big `switch` or a `byte[]`/XOR table plus a
  static `String decrypt(int)` is the usual tell. Two options:
  1. Reimplement in Python (works when it is plain XOR/base64 — see vulns ref crypto).
  2. Let the app decrypt for you under frida — static methods are callable directly:
     ```js
     Java.perform(function () {
       var D = Java.use('com.example.a.b.c');
       console.log(D.a(1337));   // run the decryptor on an id you saw in jadx
     });
     ```
- **Resources.arsc strings**: apktool decodes them into `res/values/strings.xml`;
  grep there, not just in dex.
- Kotlin specifics: `companion object` consts are inlined at call sites — grep the
  literal, not the field name. `lateinit` crashes on missing intent extras are a
  hint you're expected to send that extra.
