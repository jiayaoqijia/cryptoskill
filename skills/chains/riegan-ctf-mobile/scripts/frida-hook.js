/**
 * frida-hook.js — universal Frida starting point for Android CTF apps.
 *
 * Run (spawn, from the repo root):
 *   scripts/ctf frida -U -f com.example.app -l skills/ctf-mobile/scripts/frida-hook.js
 * Attach to the frontmost app:
 *   scripts/ctf frida -U -F -l skills/ctf-mobile/scripts/frida-hook.js
 * (Ancient frida-tools builds additionally wanted --no-pause; current ones
 * auto-resume after loading.)
 *
 * Sections (trim to what the challenge needs — every hook is individually
 * guarded so one missing/renamed class never kills the rest):
 *   1. Java: Build fingerprint rewrite, exec/ProcessBuilder sniffing,
 *      SystemProperties answers, File.exists root-path filter.
 *   2. TLS unpinning: conscrypt TrustManagerImpl + okhttp3 CertificatePinner.
 *   3. Native: libc access()/faccessat() root-path hiding.
 *
 * Preceded by a config block of match lists to edit per challenge after reading
 * the app in jadx. Discovery snippets at the bottom.
 */

'use strict';

// ---- config: match lists (edit per challenge) --------------------------------
var TAG = '[hook]';

// Paths a root detector typically stats/execs. Add what jadx shows it probing.
var ROOT_PATHS = [
    '/system/bin/su', '/system/xbin/su', '/sbin/su', '/su/bin/su',
    '/system/app/Superuser.apk', '/data/adb/magisk', '/sbin/magisk',
    'supersu', 'xposed', 'busybox', 'magisk'
];

// Command fragments that mark a Runtime.exec()/ProcessBuilder call as a root probe.
var ROOT_CMD_HINTS = ['su', 'which su', 'busybox', 'magisk', 'xbin', 'daemonsu'];

// System properties read by root/emulator detection -> value we answer with.
// null means "answer: property unset".
var PROP_ANSWERS = {
    'ro.build.tags': 'release-keys',
    'ro.debuggable': '0',
    'ro.secure': '1',
    'ro.kernel.qemu': '0',          // emulator detection
    'qemu.hw.mainkeys': '0',
    'init.svc.qemud': null,
    'init.svc.qemu-props': null
};

// Optional: fake a real-device fingerprint when the app string-compares it.
var FAKE_FINGERPRINT = null; // e.g. 'google/redfin/redfin:13/TQ3A.230901.001/...'

// ---- helpers -----------------------------------------------------------------
function log(msg) { console.log(TAG + ' ' + msg); }

function hitsList(s, list) {
    if (!s) return false;
    for (var i = 0; i < list.length; i++) {
        if (s.indexOf(list[i]) !== -1) return true;
    }
    return false;
}

// ---- 1. Java layer -----------------------------------------------------------
Java.perform(function () {

    // 1a. Build fingerprint: report, then hide test-keys/oddities.
    try {
        var Build = Java.use('android.os.Build');
        log('Build.MODEL=' + Build.MODEL.value +
            ' TAGS=' + Build.TAGS.value +
            ' FINGERPRINT=' + Build.FINGERPRINT.value +
            ' HARDWARE=' + Build.HARDWARE.value);
        Build.TAGS.value = 'release-keys';
        if (FAKE_FINGERPRINT) Build.FINGERPRINT.value = FAKE_FINGERPRINT;
    } catch (e) {
        log('Build: ' + e);
    }

    // 1b. Runtime.exec / ProcessBuilder: log every shell-out; root probes get
    //     reported here. To make a probe FAIL instead of just logging, throw
    //     inside the implementation (commented below) — some detectors treat a
    //     successful-but-wrong result differently from an exception.
    try {
        var RuntimeC = Java.use('java.lang.Runtime');
        RuntimeC.exec.overload('java.lang.String').implementation = function (cmd) {
            var sus = hitsList(cmd, ROOT_CMD_HINTS);
            log('exec("' + cmd + '")' + (sus ? '  <== root probe' : ''));
            return this.exec(cmd);
            // To block instead:
            // throw Java.use('java.io.IOException').$new('exec blocked: ' + cmd);
        };
        RuntimeC.exec.overload('[Ljava.lang.String;').implementation = function (cmd) {
            var line = '';
            for (var i = 0; i < cmd.length; i++) line += cmd[i] + ' ';
            log('exec([' + line.trim() + '])' +
                (hitsList(line, ROOT_CMD_HINTS) ? '  <== root probe' : ''));
            return this.exec(cmd);
        };
    } catch (e) {
        log('Runtime.exec: ' + e);
    }
    try {
        var PB = Java.use('java.lang.ProcessBuilder');
        PB.start.overload().implementation = function () {
            log('ProcessBuilder: ' + this.command());
            return this.start();
        };
    } catch (e) {
        log('ProcessBuilder: ' + e);
    }

    // 1c. SystemProperties.get: feed the detector its expected answers.
    try {
        var SP = Java.use('android.os.SystemProperties');
        SP.get.overload('java.lang.String').implementation = function (key) {
            var real = this.get(key);
            if (Object.prototype.hasOwnProperty.call(PROP_ANSWERS, key)) {
                log('prop ' + key + ': ' + real + ' -> ' + PROP_ANSWERS[key]);
                return PROP_ANSWERS[key];
            }
            return real;
        };
        SP.get.overload('java.lang.String', 'java.lang.String').implementation =
            function (key, def) {
                if (Object.prototype.hasOwnProperty.call(PROP_ANSWERS, key)) {
                    log('prop2 ' + key + ' -> ' + PROP_ANSWERS[key]);
                    return PROP_ANSWERS[key];
                }
                return this.get(key, def);
            };
    } catch (e) {
        log('SystemProperties: ' + e);
    }

    // 1d. File.exists: hide root-related paths. NOTE: this runs for every
    //     File.exists() in the process — if the app hammers it, expect lag and
    //     consider narrowing to the exact paths jadx shows.
    try {
        var File = Java.use('java.io.File');
        File.exists.implementation = function () {
            var p = this.getAbsolutePath();
            if (hitsList(p, ROOT_PATHS)) {
                log('File.exists(' + p + ') -> false');
                return false;
            }
            return this.exists();
        };
    } catch (e) {
        log('File.exists: ' + e);
    }

    // 1e. Signature/integrity stub: apps that compare PackageManager signatures
    //     (GET_SIGNATURES) or an APK hash detect repackaged builds here.
    //     Two-step recipe:
    //       1) run with only logging: find the comparator in jadx (grep for
    //          `signatures` / MessageDigest) and log both sides;
    //       2) return the expected value from the hook.
    // Placeholder on purpose — the exact PackageInfo path varies by app:
    //   try {
    //     var PM = Java.use('android.app.ApplicationPackageManager');
    //     PM.getPackageInfo.overload('java.lang.String', 'int').implementation =
    //       function (pkg, flags) {
    //         var pi = this.getPackageInfo(pkg, flags);
    //         // log(pi.signatures.value) on first run; then rewrite before return
    //         return pi;
    //       };
    //   } catch (e) { log('signature stub: ' + e); }

    // 2. TLS unpinning (Java side).
    // 2a. conscrypt TrustManagerImpl — the system TLS stack on Android; covers
    //     HttpsURLConnection, most custom SSLSocketFactory setups.
    try {
        var TMI = Java.use('com.android.org.conscrypt.TrustManagerImpl');
        TMI.checkServerTrusted.overloads.forEach(function (m) {
            m.implementation = function () {
                log('TrustManagerImpl.checkServerTrusted bypassed');
                if (m.returnType.name === 'void') return;        // verifier form
                return Java.use('java.util.ArrayList').$new();   // list-returning form
            };
        });
    } catch (e) {
        log('TrustManagerImpl: ' + e);
    }

    // 2b. OkHttp 3.x pinning (void check(...)).
    try {
        var CP = Java.use('okhttp3.CertificatePinner');
        CP.check.overloads.forEach(function (m) {
            m.implementation = function (host) {
                log('okhttp CertificatePinner.check(' + host + ') bypassed');
            };
        });
    } catch (e) {
        log('okhttp3.CertificatePinner: ' + e);
    }

    // 2c. OkHttp 4.x internal (Kotlin) check$okhttp — returns a List.
    try {
        var CP4 = Java.use('okhttp3.CertificatePinner');
        CP4['check$okhttp'].implementation = function (host) {
            log('okhttp4 check$okhttp(' + host + ') bypassed');
            return Java.use('java.util.Collections').emptyList();
        };
    } catch (e) {
        log('okhttp4 check$okhttp: ' + e);
    }

    // 2d. Per-app stacks (TrustManagerImpl misses these — add what jadx shows):
    //     - custom X509TrustManager classes: hook their checkServerTrusted.
    //     - Volley/HurlStack, Flutter (see blutter output), native BoringSSL:
    //       use httptoolkit/frida-interception-and-unpinning (its native-tls-hook
    //       handles BoringSSL; see android-dynamic.md §6).

    log('Java hooks installed');
});

// ---- 3. native layer ---------------------------------------------------------
(function () {
    var libc = Process.findModuleByName('libc.so');
    if (!libc) {
        log('libc.so not found — native hooks skipped');
        return;
    }

    // access(path, mode) / faccessat(dirfd, path, mode, flags): the C-level
    // "does <root path> exist" probe used by native root checks.
    ['access', 'faccessat'].forEach(function (fname) {
        var addr = libc.findExportByName(fname);
        if (addr === null) return;
        Interceptor.attach(addr, {
            onEnter: function (args) {
                var pathPtr = (fname === 'faccessat') ? args[1] : args[0];
                try { this.path = pathPtr.readCString(); }
                catch (e) { this.path = null; }
            },
            onLeave: function (retval) {
                if (hitsList(this.path, ROOT_PATHS)) {
                    log('native ' + fname + '(' + this.path + ') -> -1');
                    retval.replace(-1);
                }
            }
        });
        log('hooked libc.' + fname);
    });
})();

// ---- quick discovery snippets (paste into the frida REPL or append here) ------
// List classes matching a keyword:
//   Java.enumerateLoadedClasses({
//     onMatch: function (n) { if (n.indexOf('ctf') !== -1) log(n); },
//     onComplete: function () {}
//   });
// Grab a live instance and dump fields:
//   Java.choose('com.example.ctf.SecretHolder', {
//     onMatch: function (i) { log('instance: ' + i); log('field=' + i.key.value); },
//     onComplete: function () {}
//   });
// Call a static decryptor with an id seen in jadx:
//   Java.perform(function () {
//     var D = Java.use('com.example.a.b.c');
//     log(D.a(1337));
//   });
