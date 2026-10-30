---
name: ctf-mobile
description: Use when the user mentions Android, APK, apk, apktool, jadx, smali, dex, AndroidManifest, frida, frida-server, objection, waydroid, Android emulator, rooted device, SSL pinning, iOS, IPA, mobile app challenge, reversing an app, or a mobile/Android CTF category. Owns Android static and dynamic app analysis plus iOS-light triage; hands native .so reversing to ctf-rev.
---

# CTF mobile — Android-first, iOS-light

Workspace layout, flag log, submission, remote gate: sibling skill `ctf`
(`../ctf/SKILL.md`). Native `lib/<abi>/*.so` reversing once located: sibling skill
`ctf-rev`. This skill gets you from `base.apk`/`app.ipa` to the flag.

Guardrail: challenge APKs/IPAs are untrusted. Static analysis on the host is fine;
run the app only inside waydroid or a throwaway emulator image — never on a personal
device, never "just to check" outside the challenge run env.

## Triage — first 5 minutes

From `work/<event>/<chal>/`. `$ROOT` below is the ctf repo root (from a challenge
dir that's `../../..`); tool paths are `$ROOT`-relative, data paths (`dist/`,
`apk-out/`) are challenge-dir relative.

```bash
$ROOT/skills/ctf-mobile/scripts/apk-triage.sh dist/base.apk   # report → apk-out/
```

If the artifact is an `.ipa`, skip to `references/ios-light.md`. If it is an
`.xapk`/`.apkm`/`.apks`, it is still a zip — extract and work on `base.apk`
(see `references/android-recon.md` "Split bundles").

### Reading the zip listing

| Entry in APK | Meaning | Next step |
|---|---|---|
| `classes.dex`, `classes2.dex`… | Dalvik code (count tracks app size) | jadx |
| `lib/<abi>/*.so` | native libraries; ABI set decides run env | fingerprint below |
| `assets/` | app data: bundles, JS, configs, DBs | grep + fingerprint below |
| `res/raw/` | uncompiled blobs (audio, models) | `file` each one |
| `AndroidManifest.xml` | binary XML until apktool decodes it | manifest checklist in recon ref |
| `resources.arsc` | compiled resources (strings live here too) | apktool decodes to `res/` |
| `META-INF/*.RSA` | v1 signature cert | rarely useful |

### Framework fingerprint (from lib/ and assets/)

| Signal | Framework | Follow-up |
|---|---|---|
| `libapp.so` + `libflutter.so` | Flutter | recon ref "Flutter" (blutter) |
| `assets/index.android.bundle` | React Native | plain JS or Hermes — recon ref |
| `assets/www/index.html` | Cordova/Ionic | read the JS, it is the app |
| `libil2cpp.so` + `assets/bin/Data/.../global-metadata.dat` | Unity IL2CPP | Il2CppDumper → `ctf-rev` |
| `Assembly-CSharp.dll` | Unity Mono | dotnet tooling in `ctf-rev` |
| `*.pck` | Godot | pck extractors in recon ref |
| only `lib<name>.so` + dex | NDK app | `ctf-rev` (ghidra arm64) |
| no `lib/` at all | pure Java/Kotlin | jadx straight away |

### Run-environment inventory (before any dynamic work)

| Have | Use | Notes |
|---|---|---|
| Rooted physical device + USB | `adb` over USB + `frida-server` | best compat, runs arm64-only APKs |
| No device | waydroid | `sudo pacman -S waydroid`; root shell; container-isolated |
| No device, want a real emulator | android-studio (AUR) AVD | pick a non-"Play" image so `adb root` works |
| No root at all | `objection patchapk` (frida gadget) | repackaged APK; breaks signature checks |

Setup commands and pitfalls: `references/android-dynamic.md`.

### Decision table

| Signal | Go to |
|---|---|
| secrets / keys / URLs found by the grep sweep | recon ref "Secret sweep"; offline crypto, no device needed |
| exported components in manifest | vulns ref "Exported components" |
| behavior only visible at runtime (pinning, hidden check, obfuscated logic) | dynamic ref — frida-first |
| root/integrity/emulator check blocks you | dynamic ref "Bypass recipes" |
| WebView / JS bridge / deep link in jadx | vulns ref "WebView" / "Deep links" |
| `.ipa` | ios-light ref |

## Playbook

### Static → dynamic loop (default)

1. `scripts/apk-triage.sh` → inventory, secrets, manifest quick-look.
2. jadx: read the launcher activity `onCreate`, then follow data flow toward the
   flag check (registration code, native `native*()` decls, crypto).
3. Hypothesis → confirm dynamically (adb, frida) → record in `notes.md`.
4. Escalate: vulns-ref bug-class table; obfuscated strings → call the app's own
   decryptor from frida (recon ref "Obfuscation").

### Frida-first when the question is behavioral

For "what does the app do when X" (pinning, hidden unlock, encrypted protocol,
string-decrypt calls) skip the static rabbit hole:

1. Set up the run env + frida-server (dynamic ref), `frida-ps -Ua` to see the app.
2. Start from `scripts/frida-hook.js` (guarded root-bypass + unpinning skeletons).
3. Discovery without reading code:
   `frida-trace -U -f <pkg> --runtime=v8 -j '*!*keyword*/isu'` — trace Java
   methods whose signature contains `keyword` (s = match signature, i = ignore
   case, u = user classes only).
4. Quick wins via objection: `android sslpinning disable`, `android hooking watch`.

### Android bug classes (quick map — full recipes in references/android-vulns.md)

| Attack | Precondition | Command sketch |
|---|---|---|
| Start exported activity | `android:exported="true"` (or intent-filter pre-12) | `adb shell am start -n pkg/.Act --ez admin true` |
| Talk to exported service/receiver | idem | `am start-foreground-service -n …`, `am broadcast -a ACT` |
| Query exported provider | exported `content://` | `adb shell content query --uri content://…` |
| Fire deep link | `intent-filter` with scheme | `am start -a android.intent.action.VIEW -d "scheme://…"` |
| WebView bridge abuse | `addJavascriptInterface` | load attacker page → JS bridge |
| Intent redirection | parcelable extra gets `startActivity()` | nested Intent via PoC app or frida |
| FileProvider traversal | over-broad root-path | `content read --uri 'content://…%2e%2e%2f…'` |
| Read app storage | debuggable or rooted env | `run-as pkg ls`, `adb pull /data/data/pkg` |
| Hardcoded crypto | `SecretKeySpec` in jadx | offline decrypt via `$ROOT/scripts/ctf python` |
| Logcat leaks | `Log.d` near secrets/TextWatcher | `adb logcat` grep while exercising app |

### iOS (light)

On Linux, static is the realistic path: unzip → `Info.plist` (plistlib) →
strings/Mach-O (lief, ghidra) → sqlite/plist data files. Dynamic (frida,
keychain, FairPlay decryption) needs a jailbroken device or macOS — see
`references/ios-light.md` for what is actually achievable and how to fake
code-signing with ldid when repackaging.

## References

- `references/android-recon.md` — static recon: zip/apktool/jadx workflows, manifest
  checklist, secret sweep patterns, Firebase probes, framework-specific paths
  (Flutter/RN/Cordova/Unity/Godot), obfuscation recovery.
- `references/android-dynamic.md` — adb, run environments (waydroid, AVD), frida
  toolchain and server setup, objection, hooking patterns, bypass recipes
  (SSL pinning, root, signature, emulator), traffic capture.
- `references/android-vulns.md` — CTF bug classes with exact `am`/`content`/adb
  commands: components, deep links, WebView/JS bridge, intent redirection,
  PendingIntents, FileProvider traversal, storage, crypto, cert issues.
- `references/ios-light.md` — ipa structure, Info.plist on Linux, Mach-O via
  lief/ghidra, repack+ldid signing flow, honest limits of Linux-only iOS work.
- `scripts/apk-triage.sh` — one-shot static APK report (see Triage).
- `scripts/frida-hook.js` — annotated universal frida template.

## Toolbox

| Tool | Install | Purpose |
|---|---|---|
| apktool | `sudo pacman -S apktool` | decode manifest/resources, smali |
| jadx | release zip from `github.com/skylot/jadx` → run `bin/jadx`, `bin/jadx-gui` | dex → java (Java 21 already present) |
| adb/fastboot | `sudo pacman -S android-tools` | device control, `am`/`pm`/`content` |
| waydroid | `sudo pacman -S waydroid` | containerized Android run env |
| frida-tools | `uv pip install --python .venv/bin/python frida-tools` | `frida`, `frida-ps`, `frida-trace` |
| frida-server | release from `github.com/frida/frida/releases` (match version + device ABI) | device-side agent, needs root |
| objection | `uv pip install --python .venv/bin/python objection` | gadget repackaging + runtime exploration |
| mitmproxy | `sudo pacman -S mitmproxy` | HTTPS interception proxy |
| sqlite | `sudo pacman -S sqlite` | inspect pulled app databases |
| ldid | AUR (`paru -S ldid`) — not in official repos | ad-hoc iOS code signing on Linux |
