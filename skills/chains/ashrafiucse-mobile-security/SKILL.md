---
name: mobile-security
description: Audits mobile app security — Android (AndroidManifest.xml: exported components, allowBackup, debuggable, cleartext traffic, network security config; WebView misconfigurations; hardcoded keys), iOS (Info.plist ATS exceptions, secrets in UserDefaults, keychain accessibility), and React Native/Flutter storage pitfalls. Use when the project contains AndroidManifest.xml, Info.plist, or Kotlin/Java/Swift/Dart/RN code.
license: MIT
---

# Mobile Security

## Step 0 — Detect

```bash
rg --files -g 'AndroidManifest.xml' -g 'Info.plist' -g '*.kt' -g '*.java' -g '*.swift' -g '*.m' -g '*.dart' -g 'pubspec.yaml' -g 'Podfile' -g 'app/build.gradle*' | head
```

## Step 1 — Android manifest

```bash
rg -n "android:exported|allowBackup|debuggable|usesCleartextTraffic|networkSecurityConfig|protectionLevel|grantUriPermissions" -g 'AndroidManifest.xml' -g '*.xml'
```

**Component census (don't eyeball):** enumerate exported components BY TYPE — agents reliably spot activities and providers while services/receivers get skipped. Four separate passes, one table row each:
```bash
rg -n "<activity[^>]*android:exported=\"true\"" -g 'AndroidManifest.xml'
rg -n "<service[^>]*android:exported=\"true\"" -g 'AndroidManifest.xml'
rg -n "<receiver[^>]*android:exported=\"true\"" -g 'AndroidManifest.xml'
rg -n "<provider[^>]*android:exported=\"true\"" -g 'AndroidManifest.xml'
```

| Flag | Finding | Severity |
|---|---|---|
| `android:allowBackup="true"` (or omitted — it's the default) | data extractable via `adb backup` | Medium |
| `android:debuggable="true"` in release manifest | debug bridge on prod devices | High |
| exported `activity`/`service`/`receiver`/`provider` without `android:permission` | component hijacking — any app invokes it | High |
| component with `<intent-filter>` and no explicit `exported` | filters imply exported (API ≤30 rules) | High |
| `usesCleartextTraffic="true"` / `cleartextTrafficPermitted="true"` | HTTP downgrade/MITM | Medium |
| custom permission `protectionLevel="normal"` guarding sensitive ops | any app can request it | Medium |
| exported `provider` + `grantUriPermissions` | URI grant to malicious apps | High |

Note: cleartext is blocked by default since API 28 — check `minSdkVersion`; below 28
without a `network_security_config` = de facto cleartext allowed.

## Step 2 — Android code

```bash
rg -n "addJavascriptInterface|setJavaScriptEnabled|setAllowFileAccess|loadUrl|setAllowUniversalAccessFromFileURLs" -g '*.kt' -g '*.java'
rg -n -i "(api[_-]?key|secret|token)\s*=\s*[\"'][^\"']{8,}" -g '*.kt' -g '*.java' -g 'strings.xml' -g 'build.gradle*'
```

- `addJavascriptInterface` + JS enabled → classic RCE bridge (High; Critical with file access + user URL)
- `loadUrl(intent.dataString)` / loading `http://` update URLs with JS on → High
- Hardcoded keys in code/`strings.xml`/`BuildConfig` → **Critical** (decompiling is trivial)
- `sharedPreferences` storing tokens unencrypted → Medium

## Step 3 — iOS

```bash
rg -n "NSAllowsArbitraryLoads|NSAllowsLocalNetworking|NSExceptionDomains" -g 'Info.plist'
rg -n "UserDefaults|kSecAttrAccessible|Keychain" -g '*.swift' -g '*.m' | head -20
```

- `NSAllowsArbitraryLoads=true` (ATS off) → Medium; `NSExceptionDomains` list → review each
- Tokens/PII in `UserDefaults` (plist, unencrypted, included in backups) → Medium/High
- Keychain items without `kSecAttrAccessible...ThisDeviceOnly` for sensitive items → Low/Medium
- Hardcoded secrets in Swift/ObjC → **Critical**

## Step 4 — Cross-platform

- React Native: tokens in `AsyncStorage` (unencrypted) → Medium; dev deps (`flipper`, `react-devtools-core`) reachable in release builds → Medium
- Flutter: tokens outside `flutter_secure_storage` → Medium; disabling certificate validation (`badCertificateCallback => true`) → High

## Reporting

Manifest findings cite the XML line; code findings cite `file:line`. Fixes are usually
one attribute (`allowBackup="false"`, `exported="false"` + permission) — give the exact line.
Cross-reference hardcoded keys with `../secrets-detection/SKILL.md` for rotation guidance.
