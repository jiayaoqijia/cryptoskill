# Threshold Signatures in Motoko

The Motoko version of the canister in SKILL.md. It exposes the same Candid interface (`public_key`, `sign`, variant names `ed25519`, `bip340secp256k1`, `ecdsaSecp256k1`, `ecdsaSecp256r1`) but returns `#ok` / `#err`. Type-checked with mo:core 2.7, the `ic` package 5.0.0 and 6.0.0, and `sha2` 0.3.2.

```bash
mops add ic && mops add sha2   # one package per command, never in parallel
```

```motoko
import { ic } "mo:ic";
import Call "mo:ic/Call";
import Error "mo:core/Error";
import Principal "mo:core/Principal";
import Runtime "mo:core/Runtime";
import Text "mo:core/Text";
import Sha256 "mo:sha2/Sha256";

persistent actor {
  public type Scheme = { #ed25519; #bip340secp256k1; #ecdsaSecp256k1; #ecdsaSecp256r1 };

  // Read once at first install and kept across upgrades: a different key name
  // means different keys and addresses, so treat it as permanent.
  let keyName : Text = Runtime.envVar<system>("THRESHOLD_KEY_NAME") ?? "key_1";

  // Versioned, per-user derivation path. Never let callers choose the path.
  func userPath(user : Principal) : [Blob] = ["user-v1".encodeUtf8(), user.toBlob()];

  // Public key of the caller's key. Free, but a cross-subnet call: cache it.
  public shared ({ caller }) func public_key(scheme : Scheme) : async { #ok : Blob; #err : Text } {
    if (caller.isAnonymous()) return #err "anonymous caller";
    let derivation_path = userPath(caller);
    try {
      let { public_key } = switch (scheme) {
        case (#ed25519) {
          await ic.schnorr_public_key({ canister_id = null; derivation_path; key_id = { algorithm = #ed25519; name = keyName } });
        };
        case (#bip340secp256k1) {
          await ic.schnorr_public_key({ canister_id = null; derivation_path; key_id = { algorithm = #bip340secp256k1; name = keyName } });
        };
        case (#ecdsaSecp256k1) {
          await ic.ecdsa_public_key({ canister_id = null; derivation_path; key_id = { curve = #secp256k1; name = keyName } });
        };
        case (#ecdsaSecp256r1) {
          await ic.ecdsa_public_key({ canister_id = null; derivation_path; key_id = { curve = #secp256r1; name = keyName } });
        };
      };
      #ok public_key;
    } catch (e) {
      #err(e.message());
    };
  };

  // Signs with the caller's own key. Call.signWith* attach the exact fee
  // (ic0.cost_sign_with_*) and trap on an unknown key name.
  public shared ({ caller }) func sign(scheme : Scheme, message : Blob) : async { #ok : Blob; #err : Text } {
    if (caller.isAnonymous()) return #err "anonymous caller";
    let derivation_path = userPath(caller);
    try {
      let { signature } = switch (scheme) {
        // Schnorr and Ed25519 sign the message itself, not a hash of it.
        case (#ed25519) {
          await Call.signWithSchnorr({ message; derivation_path; key_id = { algorithm = #ed25519; name = keyName }; aux = null });
        };
        case (#bip340secp256k1) {
          await Call.signWithSchnorr({ message; derivation_path; key_id = { algorithm = #bip340secp256k1; name = keyName }; aux = null });
        };
        // ECDSA signs a 32-byte hash: SHA-256 here; Keccak-256 for Ethereum, the sighash for Bitcoin.
        case (#ecdsaSecp256k1) {
          await Call.signWithEcdsa({ message_hash = Sha256.fromBlob(#sha256, message); derivation_path; key_id = { curve = #secp256k1; name = keyName } });
        };
        case (#ecdsaSecp256r1) {
          await Call.signWithEcdsa({ message_hash = Sha256.fromBlob(#sha256, message); derivation_path; key_id = { curve = #secp256r1; name = keyName } });
        };
      };
      #ok signature; // 64 bytes for every scheme
    } catch (e) {
      // A rejected call signed nothing (queue full, cycles, bad args); retry later.
      // SYS_UNKNOWN / CANISTER_ERROR: a signature may still exist.
      #err(e.message());
    };
  };
};
```

`persistent actor` compiles on moc 1 without `--default-persistent-actors`; moc 2 accepts it with warning M0217 (redundant `persistent`), or write a bare `actor` if you only target moc 2. `keyName` is a persistent `let`, so `THRESHOLD_KEY_NAME` is read only at first install; changing it later has no effect short of a reinstall. Set it in `icp.yaml` exactly as in SKILL.md. Use `Call.trySignWithEcdsa` / `Call.trySignWithSchnorr` to get `#err(#invalidKeyName)` instead of a trap. `ic` 6.x needs `moc` >= 2.1.0; `ic` 5.0.0 works with `moc` >= 1.4.0. Never hardcode the fee: Motoko code copied from older examples attaches `10_000_000_000` cycles, which only covers `test_key_1`.
