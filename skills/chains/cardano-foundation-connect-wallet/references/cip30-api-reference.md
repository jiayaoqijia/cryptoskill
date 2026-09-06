# CIP-30 dApp-Wallet Web Bridge API Reference

CIP-30 defines the standard interface for web-based dApps to interact with Cardano wallet browser extensions.

## Wallet Discovery

### `window.cardano`

The global injection point for Cardano wallets. Each wallet extension adds itself as a property:

```javascript
window.cardano.eternl     // Eternl wallet
window.cardano.lace       // Lace wallet
window.cardano.vespr      // Vespr wallet
window.cardano.typhon     // Typhon wallet
window.cardano.gerowallet // GeroWallet
window.cardano.nufi       // NuFi wallet
// ... keys vary per wallet -- enumerate Object.keys(window.cardano) instead
// of hardcoding a list, and check the live registry at cardano.org/apps.
// (Nami is sunset -- migrated into Lace; Flint is discontinued.)
```

### Wallet Properties (before enabling)

Each `window.cardano.<walletName>` object exposes:

| Property | Type | Description |
|---|---|---|
| `name` | `string` | Human-readable wallet name |
| `icon` | `string` | Base64-encoded wallet icon (data URI) |
| `apiVersion` | `string` | CIP-30 API version supported |
| `isEnabled()` | `Promise<boolean>` | Check if dApp is already authorized |
| `enable()` | `Promise<API>` | Request permission and get API object |
| `supportedExtensions` | `Extension[]` | List of supported CIP extensions (e.g., CIP-95) |

## Enabling a Wallet

### `enable(extensions?)`

Requests the user to grant access to the wallet. Returns the full API object on success.

```javascript
// Basic enable
const api = await window.cardano.eternl.enable();

// Enable with extensions (e.g., CIP-95 for governance)
const api = await window.cardano.eternl.enable({
  extensions: [{ cip: 95 }]
});
```

**Returns**: `Promise<API>` -- the wallet API object

**Throws**: If user rejects the connection request

**Notes**:
- Shows a popup in the wallet asking the user to connect
- The dApp never receives private keys
- Connection may persist across page reloads (wallet-dependent)

## API Methods

All methods below are available on the API object returned by `enable()`.

### `api.getNetworkId()`

Returns the network the wallet is connected to.

```javascript
const networkId = await api.getNetworkId();
// 0 = testnet (preview, preprod, or custom)
// 1 = mainnet
```

**Returns**: `Promise<number>`

### `api.getUtxos(amount?, paginate?)`

Returns a list of UTxOs controlled by the wallet.

```javascript
// Get all UTxOs
const utxos = await api.getUtxos();

// Get UTxOs sufficient for a specific amount (CBOR-encoded Value)
const utxos = await api.getUtxos(amountCbor);

// Paginate results
const utxos = await api.getUtxos(undefined, { page: 0, limit: 10 });
```

**Parameters**:
- `amount` (optional): CBOR hex string of a Value. If provided, returns UTxOs sufficient to cover this amount.
- `paginate` (optional): `{ page: number, limit: number }`

**Returns**: `Promise<string[] | null>` -- Array of CBOR hex-encoded UTxOs, or null if amount cannot be satisfied

### `api.getBalance()`

Returns the total balance of the wallet.

```javascript
const balanceCbor = await api.getBalance();
// Returns CBOR hex-encoded Value (lovelace + multi-assets)
```

**Returns**: `Promise<string>` -- CBOR hex-encoded Value

**Notes**: Includes all assets (ADA + tokens). Decode with a CBOR library or SDK.

### `api.getUsedAddresses(paginate?)`

Returns addresses that have been used (have appeared in transactions).

```javascript
const addresses = await api.getUsedAddresses();
// Returns array of CBOR hex-encoded addresses
```

**Parameters**:
- `paginate` (optional): `{ page: number, limit: number }`

**Returns**: `Promise<string[]>` -- Array of CBOR hex-encoded addresses

### `api.getUnusedAddresses()`

Returns addresses that have not been used yet.

```javascript
const addresses = await api.getUnusedAddresses();
```

**Returns**: `Promise<string[]>` -- Array of CBOR hex-encoded addresses

### `api.getChangeAddress()`

Returns an address to use for transaction change output.

```javascript
const changeAddress = await api.getChangeAddress();
// CBOR hex-encoded address
```

**Returns**: `Promise<string>` -- CBOR hex-encoded address

### `api.getRewardAddresses()`

Returns the wallet's reward/staking addresses.

```javascript
const rewardAddresses = await api.getRewardAddresses();
```

**Returns**: `Promise<string[]>` -- Array of CBOR hex-encoded reward addresses

### `api.signTx(tx, partialSign?)`

Requests the wallet to sign a transaction.

```javascript
// Full sign (wallet must own all required keys)
const witnessSet = await api.signTx(unsignedTxCbor, false);

// Partial sign (for multi-sig, wallet signs what it can)
const witnessSet = await api.signTx(unsignedTxCbor, true);
```

**Parameters**:
- `tx`: CBOR hex string of the unsigned transaction
- `partialSign` (optional, default `false`): If true, the wallet signs only with keys it owns and does not fail if it cannot provide all required signatures

**Returns**: `Promise<string>` -- CBOR hex-encoded TransactionWitnessSet

**Throws**: If user rejects signing, or if `partialSign` is false and wallet cannot provide all signatures

**Notes**:
- Shows transaction details to user for review
- User must explicitly approve
- The wallet adds its witness to the transaction
- For multi-sig flows, set `partialSign: true`

### `api.submitTx(tx)`

Submits a signed transaction to the network via the wallet's connection.

```javascript
const txHash = await api.submitTx(signedTxCbor);
// Returns transaction hash as hex string
```

**Parameters**:
- `tx`: CBOR hex string of the signed (assembled) transaction

**Returns**: `Promise<string>` -- Transaction hash (hex)

**Throws**: If the transaction is invalid or submission fails

**Notes**:
- The wallet submits through its own node/backend
- The dApp does not need its own submit endpoint
- Some wallets may show a confirmation dialog

### `api.signData(addr, payload)`

Signs arbitrary data with the wallet's key (CIP-8 message signing).

```javascript
const signature = await api.signData(addressCbor, payloadHex);
// Returns { signature, key }
```

**Parameters**:
- `addr`: CBOR hex-encoded address (used to select signing key)
- `payload`: Hex-encoded data to sign

**Returns**: `Promise<{ signature: string, key: string }>` -- COSE_Sign1 signature and COSE_Key

**Notes**:
- Used for authentication, message signing, proof of ownership
- Does not create a transaction
- Follows CIP-8 message signing standard

### `api.getCollateral(params)` — DEPRECATED

Returns UTxOs suitable for use as collateral (for Plutus script transactions).

**Deprecated in CIP-30**: since CIP-40 (collateral return, Babbage era), any
UTxO can serve as collateral with the excess returned via a collateral-return
output, so this dedicated API is no longer needed. Modern SDKs (Mesh, Evolution,
Blaze) handle collateral in the transaction builder instead.

```javascript
const collateral = await api.getCollateral({ amount: cborCoin });
```

**Parameters**:
- `params`: `{ amount: cbor<Coin> }` -- CBOR-encoded Coin (not a decimal string)

**Returns**: `Promise<TransactionUnspentOutput[] | null>` -- CBOR hex-encoded UTxOs suitable for collateral

**Notes**:
- Prefer CIP-40 collateral return over this legacy call
- Some wallets still implement it; do not rely on it for new code

## CIP-95 Extensions (Governance)

CIP-95 extends CIP-30 with governance-specific methods. Available when enabled with `extensions: [{ cip: 95 }]`.

### `api.cip95.getPubDRepKey()`

Returns the wallet's public DRep key.

```javascript
const drepPubKey = await api.cip95.getPubDRepKey();
// Hex-encoded Ed25519 public key
```

**Returns**: `Promise<string>` -- Hex-encoded public key

### `api.cip95.getRegisteredPubStakeKeys()`

Returns public stake keys that are registered on-chain.

```javascript
const registeredKeys = await api.cip95.getRegisteredPubStakeKeys();
```

**Returns**: `Promise<string[]>` -- Array of hex-encoded public keys

### `api.cip95.getUnregisteredPubStakeKeys()`

Returns public stake keys that are not yet registered on-chain.

```javascript
const unregisteredKeys = await api.cip95.getUnregisteredPubStakeKeys();
```

**Returns**: `Promise<string[]>` -- Array of hex-encoded public keys

### Governance transactions via CIP-95

CIP-95 does not add new signing methods. Instead, governance transactions (DRep registration, voting, delegation) are built as regular transactions containing the appropriate certificates and voting procedures, then signed with `api.signTx()`.

The wallet uses the DRep key and stake keys internally when signing governance certificates.

## Data Encoding Notes

CIP-30 uses CBOR hex encoding for most data types:

| Data type | Encoding | Decode with |
|---|---|---|
| Address | CBOR hex | SDK or `@emurgo/cardano-serialization-lib` |
| UTxO | CBOR hex | SDK or serialization library |
| Value (balance) | CBOR hex | SDK or serialization library |
| Transaction | CBOR hex | SDK or serialization library |
| Witness set | CBOR hex | SDK or serialization library |

Using an SDK (Mesh, Evolution SDK) avoids manual CBOR decoding.

## Error Handling

Common error scenarios:

| Error | Cause | Handling |
|---|---|---|
| `APIError` (code: -1) | Wallet internal error | Retry or show error message |
| `APIError` (code: -2) | Invalid request | Check parameters |
| `APIError` (code: -3) | Refused by user | Show friendly message, allow retry |
| `APIError` (code: -4) | Account not set | User needs to configure wallet |
| `enable()` rejected | User clicked "Cancel" | Show connect button again |
| `signTx()` rejected | User rejected signing | Inform user tx was not signed |
| `submitTx()` failed | Invalid tx / network issue | Show error details, check tx validity |

## Browser Compatibility

- CIP-30 works in all major browsers (Chrome, Firefox, Brave, Edge)
- Wallet extensions must be installed in the browser
- `window.cardano` is not available in SSR (server-side rendering)
- Some wallets load asynchronously; poll or use `setTimeout` if not immediately available
- Mobile browsers generally do not support wallet extensions (use WalletConnect / CIP-45 instead)
