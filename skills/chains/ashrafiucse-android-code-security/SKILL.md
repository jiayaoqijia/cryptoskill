---
name: android-code-security
description: Audits native Android app code in Kotlin AND Java — tokens outside EncryptedSharedPreferences/Keystore, local SQLi via execSQL/rawQuery interpolation, TLS bypass in code (empty X509TrustManager, always-true HostnameVerifier, OkHttp trust-all), WebView @JavascriptInterface methods reaching sensitive ops with external URLs, deep-link intent.getStringExtra into startActivity/Class.forName, PendingIntent without FLAG_IMMUTABLE, hardcoded SecretKeySpec, Cipher.getInstance("AES") ECB default, MD5/SHA-1, seeded SecureRandom, token Log.d leakage, committed google-services.json keys. Use when the project has app/src/main Kotlin or Java code with an Android build.gradle.
license: MIT
---

# Android Code Security (Kotlin + Java)

App-code shapes for native Android. The manifest/platform half (exported
components, allowBackup, cleartext policy, network security config) stays
with `../mobile-security/SKILL.md` — run both; this skill owns what lives in
`app/src/main/**`. Sibling: `../flutter-security/SKILL.md` (same classes,
Dart shapes).

Kotlin and Java share every platform API — most rules fire on both with one
grep; the divergent shapes (lambdas vs anonymous classes, string templates vs
concatenation) get their own pattern lines below.

## Step 0 — Detect

```bash
rg --files -g 'build.gradle*' -g '*.kt' -g '*.java' | head -5
rg -n "com.android.application" -g 'build.gradle*'
rg --files -g 'google-services.json'
```

Record: security-crypto (EncryptedSharedPreferences) present? OkHttp/Retrofit?
WebView? Kotlin-only or mixed with Java legacy files?

## Step 1 — Storage census (persona: device thief / rooted / adb backup)

```bash
rg -n "getSharedPreferences\(" -g '*.kt' -g '*.java' app/src/
rg -n "writeText\(|FileOutputStream\(" -g '*.kt' -g '*.java' app/src/
rg -n "SQLiteOpenHelper|execSQL\(|rawQuery\(" -g '*.kt' -g '*.java' app/src/
```

Census discipline: every hit dispositioned (credential-class → finding;
theme/flags → verified-safe). Credential-class = tokens, keys, passwords,
PII. Plaintext SharedPreferences is world-readable to anything with the
device/userdata. Safe shape: `EncryptedSharedPreferences.create(...)` with a
`MasterKey` — presence alone doesn't clean a hit of `getSharedPreferences`
on a DIFFERENT name; check which store the token write targets.

## Step 2 — Local SQLi (the app's own DB)

```bash
rg -n 'execSQL\(.*\$' -g '*.kt' app/src/        # Kotlin string templates
rg -n 'execSQL\(.*\+' -g '*.kt' -g '*.java' app/src/   # concatenation (both langs)
rg -n 'rawQuery\(.*(\$|\+)' -g '*.kt' -g '*.java' app/src/
```

Interpolated/concatenated values = injection; the local DB often mirrors
server data and is readable by backups. Safe: bind args —
`execSQL(sql, arrayOf(v))`, `rawQuery(sql, selectionArgs)`. Note: SQL
literals legitimately contain parens (`VALUES (?)`, `WHERE (a AND b)`) —
the vuln signal is `$`/`+` reaching the statement, not parens. Trace the
value: deeplink/intent-controlled input raises severity (other-app persona).

## Step 3 — TLS bypass in code

```bash
rg -n 'checkServerTrusted[^{]*\{\}' -g '*.kt' -g '*.java' app/src/
rg -n 'HostnameVerifier\s*\{[^}]*true' -g '*.kt' app/src/
rg -n -A1 "boolean verify" -g '*.java' app/src/   # Java twin is TWO lines: signature, then `return true;`
rg -n "http://" -g '*.kt' -g '*.java' app/src/
```

- Empty-body `checkServerTrusted` (Kotlin `override fun ...() {}` or Java
  anonymous class) → **Critical** when wired into a client (look for
  `sslSocketFactory(...)` nearby). The empty method IS the trust kill.
- Always-true verifier (lambda or `verify → return true`) → Critical.
- `http://` constants → Medium; Critical when auth headers ride the request.
  localhost/test-config is the common safe near-miss — disposition it.
- Safe: default trust + `CertificatePinner` for token-carrying clients.

## Step 4 — WebView bridge depth

```bash
rg -n "addJavascriptInterface|@JavascriptInterface" -g '*.kt' -g '*.java' app/src/
rg -n "loadUrl\((url|target|[a-z]+Url)" -g '*.kt' -g '*.java' app/src/
rg -n "javaScriptEnabled = true|setJavaScriptEnabled\(true\)" -g '*.kt' -g '*.java' app/src/
```

`../mobile-security/SKILL.md` flags bridge existence from the manifest side;
HERE you open every `@JavascriptInterface` method body: file reads, payment,
token access, intent launching → Critical when the URL is external
(deeplink/intent-sourced). `loadUrl(` with a constant https string is the
safe near-miss; a variable is the vuln shape.

## Step 5 — Intent & deep-link flow (persona: any other app on the device)

```bash
rg -n "getStringExtra\(|getData\(|getParcelableExtra\(" -g '*.kt' -g '*.java' app/src/
rg -n "Class\.forName|setComponent\(|setPackage\(" -g '*.kt' -g '*.java' app/src/
rg -n "PendingIntent\.getActivity\(" -g '*.kt' -g '*.java' app/src/
```

- External string → `Class.forName`/`setComponent` → `startActivity` = the
  app instantiates any class another app names (private activities,
  side-effectful receivers) → High.
- `PendingIntent.getActivity(ctx, req, intent, 0)` — flags=0 = MUTABLE
  pending intent → High (hijack/rewrite by other apps pre-12 semantics).
  Safe: `PendingIntent.FLAG_IMMUTABLE` in the flags argument — same call,
  flags differ; check the LAST argument, not the call itself.
- Route allowlist maps (`intent.data.lastPathSegment` → const map) = safe shape.

## Step 6 — Crypto

```bash
rg -n "SecretKeySpec\(" -g '*.kt' -g '*.java' app/src/
rg -n 'Cipher\.getInstance\("AES"\)' -g '*.kt' -g '*.java' app/src/
rg -n 'getInstance\("(MD5|SHA-1)"\)' -g '*.kt' -g '*.java' app/src/
rg -n "setSeed\(" -g '*.kt' -g '*.java' app/src/
```

- `SecretKeySpec(hardcodedBytes, "AES")` → Critical: key extractable from
  APK, never rotatable. Safe: AndroidKeyStore `KeyGenParameterSpec`.
- `Cipher.getInstance("AES")` → ECB default → High.
  `"AES/GCM/NoPadding"` = safe.
- MD5/SHA-1: severity by what it protects (fingerprint/ticket = Medium;
  password/token = Critical).
- `setSeed(constant)` on SecureRandom → High — predictable OTPs/tokens.

## Step 7 — Secrets artifacts & logcat

```bash
rg -n "current_key|api_key" -g 'google-services.json'
rg -n 'Log\.[dvi]\([^)]*[Tt]oken' -g '*.kt' -g '*.java' app/src/
rg -n -i "(api[_-]?key|secret|token)\s*=\s*\"[^\"]{8,}" -g '*.kt' -g '*.java' -g 'strings.xml' -g 'build.gradle*'
```

- google-services.json `current_key` (AIza…) committed → Medium baseline:
  check Firebase key restrictions + which APIs are enabled before rating
  higher; unrestricted keys are attacker-budget risks.
- Token values in `Log.d/v/i` → Medium (logcat: adb, bug reports, vendor
  crash dumps). `if (BuildConfig.DEBUG)` gate + static message = safe.
- Hardcoded key assignments → route via `../secrets-detection/SKILL.md`.

## Step 8 — Dependencies & build hygiene

`build.gradle` deps: dependency-vulns' osv_scan parses `gradle.lockfile`
(maven ecosystem) — plain `implementation` coordinates need manual OSV
lookup by group:artifact:version; note as limitation in the report.
`minifyEnabled false` in release + no resource obfuscation → informational.

## Reporting

Severity table as in steps. Fixes are short: EncryptedSharedPreferences
create-call, bind-args execSQL, FLAG_IMMUTABLE, Keystore keygen. Manifest
findings → `../mobile-security/SKILL.md`; Flutter equivalents →
`../flutter-security/SKILL.md`; dep CVEs → `../dependency-vulns/SKILL.md`.
