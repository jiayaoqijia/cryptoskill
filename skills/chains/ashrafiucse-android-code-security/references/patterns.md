# Pattern Library — android-code-security

| Sink | Dangerous | Safe | Notes |
|---|---|---|---|
| Prefs storage | `getSharedPreferences("session", MODE_PRIVATE)` holding tokens | `EncryptedSharedPreferences.create(...)` + `MasterKey` | plaintext XML; check WHICH store the credential write targets — a secure store elsewhere doesn't clean a plaintext hit |
| File storage | `File(filesDir, "tokens.txt").writeText(...)` | EncryptedSharedPreferences; Keystore-wrapped file keys | |
| SQLite write | `execSQL("INSERT ... ('$token')")` (Kotlin `$` template) | `execSQL(sql, arrayOf(v))` bind args | SQL literals contain parens legitimately — the vuln signal is `$`/`+`, not parens |
| SQLite write (Java) | `execSQL("... '" + token + "'")` | `execSQL(sql, new Object[]{ v })` | same class, concat shape |
| Trust manager | `checkServerTrusted(...) {}` empty body (Kotlin override or Java anonymous) | default trust; pinning | the empty method IS the kill switch — verify wiring via `sslSocketFactory(` |
| Hostname verifier | `HostnameVerifier { _, _ -> true }` / `verify(...) { return true; }` | CertificatePinner; verify against expected host | two syntax shapes, one class |
| Cleartext | `http://` URL constants | `https://` | localhost-test is the near-miss; Critical with auth header |
| JS bridge | `addJavascriptInterface` + `@JavascriptInterface fun pay/readFile` | no bridge; bridge with validated methods + fixed origin | open every @JavascriptInterface BODY — the manifest skill stops at existence |
| WebView URL | `loadUrl(url)` variable | `loadUrl("https://fixed...")` constant | variable from intent/deeplink = third-party page |
| Component injection | `getStringExtra("screen")` → `Class.forName("...$target")` → `startActivity` | allowlist map on `intent.data.lastPathSegment` | any app names any in-app class |
| Pending intent | `PendingIntent.getActivity(this, 0, intent, 0)` | `..., PendingIntent.FLAG_IMMUTABLE)` | check the LAST arg — same call both ways |
| Symmetric key | `SecretKeySpec(hardcodedBytes, "AES")` | AndroidKeyStore `KeyGenParameterSpec` | APK-extractable, never rotatable |
| Cipher mode | `Cipher.getInstance("AES")` | `"AES/GCM/NoPadding"` | bare "AES" = ECB default |
| Digest | `getInstance("MD5")` / `getInstance("SHA-1")` | SHA-256+ | severity by what it protects |
| Randomness | `SecureRandom().setSeed(constant)` | unseeded `SecureRandom()` | predictable OTP/token source |
| Logcat | `Log.d("AUTH", "token: $authToken")` | `if (BuildConfig.DEBUG) Log.d(TAG, staticMsg)` | token in message = the leak |
| Build artifact | google-services.json `current_key` committed | CI-injected; restricted key | Medium baseline, check restrictions |
