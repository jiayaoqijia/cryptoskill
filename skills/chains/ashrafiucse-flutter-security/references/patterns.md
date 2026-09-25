# Pattern Library — flutter-security

| Sink | Dangerous | Safe | Notes |
|---|---|---|---|
| Prefs storage | `SharedPreferences.getInstance` then `setString('token', ...)` | `FlutterSecureStorage` read/write | SUBSTRING TRAP: `encryptedSharedPreferences:` option contains the token — anchor on `.getInstance`; dependency presence alone is not a finding |
| File storage | `File(...).writeAsString(token)` in app docs dir | secure storage; encrypted container | check WHAT value, not just the call |
| SQLite | `db.insert('session', {'token': ...})` | no credential columns; OS-level encryption (SQLCipher) | sqflite DB is plaintext |
| Cert bypass (global) | `HttpOverrides.global` + `badCertificateCallback => true` | default validation | kills TLS for every client → Critical |
| Cert bypass (dio) | `onHttpClientCreate` → `client.badCertificateCallback = ... => true` | default; pinning (badCert comparing SPKI hashes) | per-client Critical |
| Cleartext | `http://` URL constants | `https://` | localhost-in-dev is the near-miss |
| WebView JS | `JavascriptMode.unrestricted` | `JavascriptMode.disabled` (static content) | unrestricted alone ≠ finding — trace the channel |
| JS bridge | `addJavaScriptChannel('Name', onMessageReceived: ...)` reaching pay/file/token ops | no channel; channel with origin check + validated messages | Critical with external URL |
| Channel outbound | `invokeMethod(userControlledNameOrArgs)` | const method allowlist + regex shape check | deep link feeding invoke = other-app persona |
| Channel inbound | `call.arguments['path']` forwarded to native sinks | validate shape/source before forward | plugin boundary is trusted, callers aren't |
| Deep link route | `pushNamed(uri.path)` / `pushNamed('/$screen')` from `getInitialLink()` | allowlist map lookup; parse+validate params | any app fires the scheme |
| Build secrets | `--dart-define=API_KEY=...` in committed scripts/CI | CI secret store injecting at build | reader `String.fromEnvironment` is not the leak |
| Randomness | `Random()` for tokens/OTP | `Random.secure()` | check what the value protects |
| Hashing | `md5.convert`, `sha1.convert` on passwords | server-side argon2/bcrypt; sha256+ for non-security | checksum uses = verified-safe |
| Log leakage | ungated `print`/`debugPrint` of headers/tokens | kDebugMode gate; redacting logger | Medium default |
