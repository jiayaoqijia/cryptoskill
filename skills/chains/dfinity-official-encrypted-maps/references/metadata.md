# EncryptedMaps with per-value metadata

Sometimes you need **plaintext metadata** alongside each encrypted value — e.g. a password's tags, URL, and modification history that the backend can index and the UI can show without decrypting. The pattern: keep the encrypted value in the library's store, keep the metadata in your own stable map, and make the two move together.

Use the **control-plane variant** of the generator: it emits the vetKD-key, access-control, and map-name endpoints (and the state + lifecycle hooks), but **omits the value read/write endpoints** so you own them. This prevents the library's raw value mutators from desyncing your metadata rows.

**Order matters:** call the library's value operation first — it performs the access-control check — and only then touch your metadata store. If the caller lacks rights, the library call errors and your metadata is left untouched.

## Rust — `custom_value_endpoints`

```rust
// Generates state, lifecycle hooks, control-plane endpoints, and the
// with_encrypted_maps / with_encrypted_maps_mut accessors — but NO value endpoints.
ic_vetkeys::export_encrypted_maps_canister!(
    "password_manager_with_metadata_app",
    [memory(0), memory(1), memory(2), memory(3)],
    custom_value_endpoints,
);

#[ic_cdk::update]
fn insert_encrypted_value_with_metadata(
    map_owner: Principal,
    map_name: ByteBuf,
    map_key: ByteBuf,
    value: EncryptedMapValue,
    tags: Vec<String>,
    url: String,
) -> Result<Option<(EncryptedMapValue, PasswordMetadata)>, String> {
    let caller = ic_cdk::api::msg_caller();
    let map_name = bytebuf_to_blob(map_name)?;
    let map_id = (map_owner, map_name);
    let map_key = bytebuf_to_blob(map_key)?;

    // Access-control check happens inside the library call, so it comes first:
    // if the caller may not write, the metadata store is left untouched.
    let opt_prev_value = with_encrypted_maps_mut(|maps| {
        maps.insert_encrypted_value(caller, map_id, map_key, value)
    })?;

    Ok(METADATA.with_borrow_mut(|metadata| {
        let key = (map_owner, map_name, map_key);
        let new_meta = metadata.get(&key)
            .map(|m| m.update(caller, tags.clone(), url.clone()))
            .unwrap_or(PasswordMetadata::new(caller, tags, url));
        opt_prev_value.zip(metadata.insert(key, new_meta))
    }))
}
```

`with_encrypted_maps` / `with_encrypted_maps_mut` are free functions the macro generates that give you a closure over the `EncryptedMaps` instance. `PasswordMetadata` is your own `Storable` type. A `remove_encrypted_value_with_metadata` and a `get_encrypted_values_for_map_with_metadata` (pairing each value with its metadata row) follow the same shape.

## Motoko — `EncryptedMapsControlPlaneCanister`

```motoko
import EncryptedMapsControlPlaneCanister "mo:ic-vetkeys/encrypted_maps/ControlPlaneCanister";
import EncryptedMaps "mo:ic-vetkeys/encrypted_maps/EncryptedMaps";
import Types "mo:ic-vetkeys/Types";
import Runtime "mo:core/Runtime";

persistent actor PasswordManagerWithMetadata {
  transient let keyName = Runtime.envVar<system>("VETKD_KEY_NAME") ?? "test_key_1";

  let encryptedMapsState = EncryptedMaps.newEncryptedMapsState<Types.AccessRights>(
    { curve = #bls12_381_g2; name = keyName },
    "password_manager_with_metadata_app",
  );

  // Control-plane mixin: brings `encryptedMaps`, `ByteBuf` and `Result` into scope
  // and the control-plane endpoints, but NONE of the value read/write endpoints.
  include EncryptedMapsControlPlaneCanister(encryptedMapsState);

  public type PasswordMetadata = {
    creation_date : Nat64;
    last_modification_date : Nat64;
    number_of_modifications : Nat64;
    last_modified_principal : Principal;
    tags : [Text];
    url : Text;
  };

  public shared (msg) func insert_encrypted_value_with_metadata(
    map_owner : Principal,
    map_name : ByteBuf,
    map_key : ByteBuf,
    value : ByteBuf,
    tags : [Text],
    url : Text,
  ) : async Result<?(ByteBuf, PasswordMetadata), Text> {
    // Access-control check happens inside the library call, so it comes first.
    switch (encryptedMaps.insertEncryptedValue(msg.caller, (map_owner, map_name.inner), map_key.inner, value.inner)) {
      case (#err(e)) { #Err(e) };
      case (#ok(optPrevValue)) {
        let metadataKey = (map_owner, map_name.inner, map_key.inner);
        let metadataValue = switch (metadata.get(compareMetadataKeys, metadataKey)) {
          case (null) { newPasswordMetadata(msg.caller, tags, url) };
          case (?existing) { updatePasswordMetadata(existing, msg.caller, tags, url) };
        };
        metadata := metadata.add(compareMetadataKeys, metadataKey, metadataValue);
        // ... return the previous (value, metadata) pair ...
      };
    };
  };
};
```

The mixin brings `encryptedMaps` (the `EncryptedMaps` instance), `ByteBuf` (a record with an `.inner : Blob` field — unwrap with `.inner`), and `Result` (`#Ok`/`#Err`) into scope. Metadata is stored in an actor-owned `mo:core/pure/Map`.

## Additional References

- The base skill: `encrypted-maps` SKILL.md
- Canonical examples: `motoko/vetkeys/password_manager_with_metadata`, `rust/vetkeys/password_manager_with_metadata` in [dfinity/examples](https://github.com/dfinity/examples/tree/master/rust/vetkeys)
