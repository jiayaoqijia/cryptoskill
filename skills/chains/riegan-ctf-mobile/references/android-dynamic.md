# Android dynamic analysis — run env, frida, objection, bypasses

Run challenge apps only in waydroid or a throwaway emulator image; endpoints you
discover still fall under the router's remote gate (`../ctf/SKILL.md`).
`$ROOT` = the ctf repo root (from a challenge dir under `work/` that's `../../..`);
`scripts/ctf` below means `$ROOT/scripts/ctf` (venv launcher, puts `.venv/bin` on PATH).

## 1. adb basics

```bash
sudo pacman -S android-tools     # adb, fastboot
adb devices -l                   # list
adb install -r dist/base.apk     # -r reinstall/replace
adb shell pm path com.example.ctf     # where the installed apk lives (pull it back with adb pull)
adb shell pm list packages -f | grep -i ctf   # find package name
adb shell dumpsys package com.example.ctf | less   # granted perms, components, version
adb logcat -c && adb logcat | grep -aiE 'flag|secret|token|password|exception'
adb pull /data/data/com.example.ctf pulled/    # needs root (§2) or debuggable (vulns ref)
adb push local /data/local/tmp/remote
adb reverse tcp:8080 tcp:8080    # device's localhost:8080 == host's 8080 (proxy setups)
```

Useful extras: `scrcpy` (`sudo pacman -S scrcpy`) mirrors+controls a USB device;
`adb shell monkey -p com.example.ctf -v 500` blurs through activities — watch logcat.

## 2. Run environments

| Env | Setup | Root | Best for |
|---|---|---|---|
| Rooted physical device | USB debugging on; maybe Magisk | `su` | arm64-only APKs, realism |
| waydroid (recommended) | `sudo pacman -S waydroid` | root shell built-in | everything else on this host |
| AVD via android-studio (AUR) | heavy GUI install | `adb root` on non-Play images | when waydroid kernel/GPU issues |

### waydroid

```bash
sudo pacman -S waydroid
# kernel: needs binder/binderfs — mainline >= 5.18 ships it (per Waydroid docs);
# otherwise linux-zen or the binder_linux-dkms AUR module.
sudo waydroid init -s GAPPS     # or plain `sudo waydroid init` (vanilla is fine for CTF)
sudo systemctl start waydroid-container
waydroid show-full-ui           # first boot takes a while
waydroid app install dist/base.apk
waydroid shell                  # root shell inside the container
```

ADB into it: inside the Android UI enable Developer options (tap Build number 7x)
and USB debugging, then from the host:

```bash
adb connect 192.168.240.112:5555    # default waydroid container IP
```

`waydroid shell` is already root, so frida-server runs without any Magisk.

Caveats: x86_64 image — arm-only native libs need the image's ARM translation
(often absent); GPU/clipboard quirks are known. Still the fastest path on this host.

### Android Studio AVD (heavier)

android-studio from AUR; then headless with the SDK tools it installs
(`$ANDROID_HOME` = `~/Android/Sdk` by default):

```bash
sdkmanager "system-images;android-34;google_apis;x86_64"
avdmanager create avd -n ctf -k "system-images;android-34;google_apis;x86_64"
emulator -avd ctf -writable-system     # $ANDROID_HOME/emulator/emulator
```

Image choice matters: "Google APIs" and plain AOSP images allow `adb root`;
"Google Play" images do not.

## 3. frida toolchain

Host side (Python agent in the shared venv):

```bash
uv pip install --python .venv/bin/python frida-tools
# gives: frida, frida-ps, frida-trace, frida-ls-devices; run via scripts/ctf frida ...
```

Device side — frida-server, run as root. Requires a rooted device, waydroid, or an
emulator image where `adb root` works:

```bash
adb shell getprop ro.product.cpu.abi        # e.g. arm64-v8a → matching server build
frida --version                             # host frida-tools version V
# download from https://github.com/frida/frida/releases/download/<V>/frida-server-<V>-android-arm64.xz
xz -d frida-server-*-android-arm64.xz
adb push frida-server-*-android-arm64 /data/local/tmp/frida-server
adb shell chmod 755 /data/local/tmp/frida-server
adb shell                                    # then, as root:
  /data/local/tmp/frida-server &             # (waydroid/`adb root` shell is root;
                                             #  on devices: su -c /data/local/tmp/frida-server)
frida-ps -U                                  # verify: device processes listed
```

Version match: server and tools should share the version; big major/minor skew
breaks the protocol. Arch notes: no `frida-server` package needed — use the release
binary. If `frida-ps -U` hangs, adbd restart (`adb kill-server && adb start-server`)
fixes most stuck-usb cases.

## 4. Hooking (modern API)

Any frida >= 12 uses `Java.perform` (the old `Dalvik.perform` form is pre-12; do not
copy it from ancient writeups). Skeleton — full annotated template in
`../scripts/frida-hook.js`:

```js
Java.perform(function () {
  var Check = Java.use('com.example.ctf.FlagChecker');
  Check.verify.overload('java.lang.String').implementation = function (s) {
    var r = this.verify(s);                  // call the original
    console.log('[+] verify("' + s + '") = ' + r);
    return true;                             // or force the result
  };
});
```

| Task | API |
|---|---|
| pick overloaded method | `M.f.overload('java.lang.String', 'int')` |
| enumerate loaded classes | `Java.enumerateLoadedClasses({onMatch: fn, onComplete: fn})` |
| grab a live instance | `Java.choose('com.example.X', {onMatch: fn, onComplete: fn})` |
| call static app code | `Java.use('com.a.Enc').decrypt('Cg==')` (static methods only) |
| read/write static fields | `Klass.FIELD.value` |
| native function hook | `Interceptor.attach(Module.findExportByName(null, 'open'), {...})` |

Run it:

```bash
scripts/ctf frida -U -f com.example.ctf -l solve.js     # spawn (auto-resumes on current tools;
                                                        #  ancient frida-tools needed --no-pause)
scripts/ctf frida -U -F -l solve.js                     # attach to frontmost app
scripts/ctf frida-ps -Ua                                # list installed+running apps
```

Trace without reading code first:

```bash
frida-trace -U -f com.example.ctf --runtime=v8 -j '*!*certificate*/isu'
# s=match signature, i=ignore case, u=user classes only (official frida example uses
# exactly this form). Native/JNI side: frida-trace -U -f com.example.ctf -i 'Java_*'
```

## 5. objection (frida with a console)

```bash
uv pip install --python .venv/bin/python objection
```

On a rooted env with frida-server running:

```bash
scripts/ctf objection -g com.example.ctf explore
```

Inside the session:

```
android sslpinning disable
android root disable
android hooking list classes
android hooking search classes ctf
android hooking watch class com.example.ctf.FlagChecker
android hooking watch class_method com.example.ctf.FlagChecker.verify --dump-args --dump-backtrace
exit
```

No root at all → gadget repackaging:

```bash
objection patchapk -s base.apk     # → base.objection.apk (embeds frida gadget)
adb install base.objection.apk
```

- Needs Java plus Android SDK build-tools (`zipalign`, `apksigner`) on PATH.
- Launch the patched app: it pauses on a gadget splash until a client attaches, then
  `objection -g com.example.ctf explore` (if it cannot find the target, check
  `frida-ps -U` — the gadget process may show as `Gadget`).
- Caveats: repackaging re-signs the APK — signature checks/integrity checks inside
  the app will fire; heavily obfuscated/resource-fused APKs sometimes fail to build.
  That failure is itself information: fall back to frida-server + manual hooks.

## 6. Bypass recipes

### SSL pinning (tiered)

1. objection: `android sslpinning disable` — covers common stacks, do this first.
2. `../scripts/frida-hook.js` §TLS — conscrypt `TrustManagerImpl` + okhttp3
   `CertificatePinner` skeletons; extend per app.
3. Universal artillery: httptoolkit's scripts
   (`github.com/httptoolkit/frida-interception-and-unpinning`) — pinning + root
   detect + proxy redirect + CA injection all at once:

   ```bash
   git clone https://github.com/httptoolkit/frida-interception-and-unpinning
   cd frida-interception-and-unpinning
   $EDITOR config.js                       # CERT_PEM, PROXY_HOST, PROXY_PORT
   frida -U -l ./config.js -l ./android/android-certificate-unpinning.js \
          -l ./android/android-disable-root-detection.js -f com.example.ctf
   ```

4. Without pinning, plain interception just needs a proxy + trusted CA: run
   `mitmproxy` (`sudo pacman -S mitmproxy`) on the host, `adb reverse tcp:8080
   tcp:8080`, point the app/device proxy at `127.0.0.1:8080`. Android 7+ ignores
   user-installed CAs for app traffic by default — install mitmproxy's CA into the
   system store on a rooted env:

   ```bash
   adb root && adb remount                       # emulator/waydroid
   h=$(openssl x509 -inform PEM -subject_hash_old -in mitmproxy-ca-cert.cer | head -1)
   adb push mitmproxy-ca-cert.cer /system/etc/security/cacerts/$h.0
   ```

   Or the app itself may declare `networkSecurityConfig` trusting user CAs (check the
   vulns ref "Cert issues" — then the plain user-store install suffices).

### Root detection

Typical checks → hook each layer (`../scripts/frida-hook.js` has the skeleton):

| Check | Hook |
|---|---|
| `Runtime.exec("which su")`, `ProcessBuilder` | log/neutralize exec; return failure |
| `File.exists("/system/xbin/su")`, magisk paths | filter `File.exists` |
| `Build.TAGS` == "test-keys", FINGERPRINT | overwrite `Build.TAGS.value = 'release-keys'` |
| `SystemProperties.get("ro.debuggable"...)` | answer table in the script |
| native `access("/sbin/su")` | `Interceptor` on libc `access`/`faccessat` |
| Magisk/supersu packages installed | PackageManager hooks; httptoolkit's `android-disable-root-detection.js` covers package probes too |

If the device runs Magisk for real, prefer Magisk's own denylist for the target
package and only patch what still fires (log each hit, fix, repeat).

### Integrity / signature checks

App fetches its own signature via `PackageManager.getPackageInfo(..., GET_SIGNATURES)`
and compares a hash → detects objection repackaging and hooks on some paths.
Recipe: hook first and only log, capture the *expected* value the app compares
against (it is usually hardcoded in dex — grep jadx for `signatures` / MessageDigest
use), then hardcode the hook to return it. `../scripts/frida-hook.js` §signature
marks the spot.

### Emulator detection

Checks: `ro.kernel.qemu`, goldfish/ranchu in `Build.HARDWARE`/`FINGERPRINT`,
`/dev/qemu_pipe`, all-zero IMEI, missing sensors. Bypass = the SystemProperties
answer table + Build field rewrites in `frida-hook.js`. waydroid often passes
natively (real kernel, normal-ish props) — prefer it when a challenge is emulator-
sensitive.

## 7. Traffic and files while live

```bash
adb logcat -c && adb logcat | grep -ai ctf        # watch during every manual step
adb shell run-as com.example.ctf ls -la files/    # if debuggable
sqlite3 pulled/databases/app.sqlite '.tables' && sqlite3 pulled/databases/app.sqlite 'select * from secrets;'
```

Screenshot/dump UI state between steps (`adb exec-out screencap -p > step.png`) —
cheap evidence for `notes.md` and writeups.
