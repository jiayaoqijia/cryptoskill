---
name: flutter-security
description: Audits Flutter/Dart mobile apps — tokens outside flutter_secure_storage (SharedPreferences/plaintext files/sqflite), certificate-validation bypass (badCertificateCallback, HttpOverrides global, Dio onHttpClientCreate), cleartext http endpoints, WebView JavaScript bridges fed external URLs, unvalidated platform-channel args both directions, deep-link route injection, secrets in --dart-define build flags and Dart source, insecure Random() for tokens, md5/sha1 password hashing. Use when the project has pubspec.yaml with a flutter SDK entry or lib/*.dart code.
license: MIT
---

# Flutter Security

Dart-side shapes for Flutter apps. The platform manifest half (Android
exported components, iOS ATS) stays with `../mobile-security/SKILL.md` —
run both for a Flutter repo; this skill owns what lives in `lib/`, build
scripts, and pubspec.

## Step 0 — Detect

```bash
rg -n "flutter" -g 'pubspec.yaml' ; rg --files -g '*.dart' | head -5
rg -n "flutter_secure_storage|shared_preferences|sqflite" -g 'pubspec.yaml'
```

Record: secure-storage package present? dio/http in use? WebView? uni_links
/deep links? Platform channels? Obfuscated release builds?

## Step 1 — Storage census (persona: device thief / rooted device / backup extractor)

```bash
rg -n "SharedPreferences\.getInstance" -g '*.dart'
rg -n "writeAsString\(|writeAsStringSync\(" -g '*.dart'
rg -n "openDatabase\(|db\.insert\(|db\.execute\(" -g '*.dart'
```

Census discipline: list EVERY hit, disposition each (credential-class value →
finding; theme/locale/flags → verified-safe). Credential-class values are
tokens, keys, passwords, PII, session state. Stored outside
`flutter_secure_storage` → High (SharedPreferences is a plaintext XML file;
sqflite is an unencrypted sqlite DB; app-documents files are world-readable
to anything with the device).

- SUBSTRING TRAP: `encryptedSharedPreferences: true` is the flutter_secure_storage
  Android OPTION and contains the token `SharedPreferences` — anchor on
  `.getInstance` call sites, never the bare token.
- The dependency being in pubspec is NOT a finding — non-sensitive prefs are
  legitimate. The finding is WHAT value is stored.
- Fix: `const FlutterSecureStorage(aOptions: AndroidOptions(encryptedSharedPreferences: true), iOptions: IOSOptions(accessibility: KeychainAccessibility.first_unlock))`.

## Step 2 — Certificate validation & cleartext

```bash
rg -n "badCertificateCallback|onBadCertificate" -g '*.dart'
rg -n "HttpOverrides" -g '*.dart'
rg -n "onHttpClientCreate" -g '*.dart'
rg -n "http://" -g '*.dart'
```

- `badCertificateCallback ... => true` behind `HttpOverrides.global` →
  **Critical**: kills TLS validation for EVERY HttpClient in the app — MITM
  harvests the auth token on any hostile network.
- Same callback inside a single client's `onHttpClientCreate` (dio adapter
  shape) → Critical for that client's traffic.
- `http://` endpoint constants → Medium (downgrade/MITM), Critical when the
  request carries the auth header. `http://localhost` in test/main-dev
  files is the common safe near-miss — disposition explicitly.
- Pinning absence on token-carrying clients → informational note
  (defense-in-depth; mobile MITM requires position).

## Step 3 — WebView bridges

```bash
rg -n "JavascriptMode\.unrestricted|setJavaScriptMode" -g '*.dart'
rg -n "addJavaScriptChannel\(" -g '*.dart'
rg -n "loadRequest\(|loadHtmlString\(|loadUrl\(" -g '*.dart'
```

Every `JavascriptChannel` registration is a Dart API exposed to the page:
trace what its `onMessageReceived` does (payment ops, file access, token
read → Critical when the URL is external/attacker-influenced). unrestricted
JS + external URL + bridge = the classic chain; check the URL source
(constant vs controller/navigation-delegate vs intent/deep-link).

## Step 4 — Platform channels (trust boundary both directions)

```bash
rg -n "invokeMethod\(" -g '*.dart'
rg -n "setMethodCallHandler\(" -g '*.dart'
rg -n "call\.arguments" -g '*.dart'
```

- Outbound: what feeds the method NAME and arguments? A deep-link string as
  the method name (`invokeMethod(action)`) lets another app choose the
  native method → High.
- Inbound: `call.arguments['...']` used unvalidated (paths, SQL, commands
  forwarded to native) → High — the native side trusts the plugin.
- Safe shape: const allowlist of method names + shape check
  (regex/parse) on arguments before invoke/forward.

## Step 5 — Deep links & route injection

```bash
rg -n "getInitialLink|linkStream|appLinks" -g '*.dart'
rg -n "pushNamed\(" -g '*.dart'
```

Any other app on the device can fire the scheme. Deep-link path or query
reaching `pushNamed` / route generation without an allowlist map → High
(route injection: private screens, checkout with attacker `amount`).
Canonicalize + map through a const allowlist; treat query params as hostile
input, not config.

## Step 6 — Secrets in the build & source

```bash
rg -n "dart-define" -g '*.sh' -g '*.yaml' -g '*.yml' -g 'Makefile' -g '*.gradle'
rg -n -i "api[_-]?key|secret|token|password" -g '*.dart' | rg -v "test|example|fake" | head -20
rg -n "print\(|debugPrint\(" -g '*.dart' | head -20
```

- `--dart-define=API_KEY=...` committed in build scripts or CI config → High: the flag
  lands in release binaries, extractable from the APK/IPA. The Dart-side
  `String.fromEnvironment` READER is not the leak — the committed value is.
- Hardcoded keys in Dart source → Critical (report via
  `../secrets-detection/SKILL.md` classes too).
- Ungated `print`/`debugPrint` of headers/tokens in non-dev code → Medium;
  wrap in `if (kDebugMode)` at minimum, better: structured logger with
  redaction.

## Step 7 — Crypto

```bash
rg -n "Random\(\)" -g '*.dart'
rg -n "md5\.|sha1\." -g '*.dart'
```

- `Random()` (dart:math, non-CSPRNG) feeding tokens/ids/OTP → High
  (guessable). Safe: `Random.secure()`. Check what the random value
  PROTECTS, not just that it exists.
- `md5.convert`/`sha1.convert` on passwords → Critical; on non-security
  checksums (cache keys, etags) → verified-safe, note it.

## Step 8 — Build & release hygiene

```bash
rg -n "flutter build" -g '*.sh' -g '*.yaml' -g 'Makefile' 2>/dev/null
```

Release builds without `--obfuscate --split-debug-info` → informational
(hardening). Debug banners/symbols shipped to prod → Low.

## Dependencies

pubspec.lock is a Pub manifest: `../dependency-vulns/SKILL.md` (osv_scan)
already parses it — no duplicate scanning here. Unpinned pubspec.yaml =
Low (reproducibility).

## Reporting

Severity table as in steps. Fixes are short: exact widget/store code for
the secure-storage shape, allowlist map for routes, `Random.secure()`.
Cross-reference: manifest findings → `../mobile-security/SKILL.md`;
key-value secrets → `../secrets-detection/SKILL.md`; dep CVEs →
`../dependency-vulns/SKILL.md`.
