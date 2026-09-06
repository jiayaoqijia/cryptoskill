# bittensor.core.extrinsics.utils &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../../_static/logo-dark-mode.svg) ](<../../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../../index.html>) __
    * [bittensor](<../../../index.html>) __
      * [bittensor.core](<../../index.html>) __
        * [bittensor.core.async_subtensor](<../../async_subtensor/index.html>)
        * [bittensor.core.axon](<../../axon/index.html>)
        * [bittensor.core.chain_data](<../../chain_data/index.html>)
        * [bittensor.core.config](<../../config/index.html>)
        * [bittensor.core.dendrite](<../../dendrite/index.html>)
        * [bittensor.core.errors](<../../errors/index.html>)
        * [bittensor.core.extrinsics](<../index.html>)
        * [bittensor.core.metagraph](<../../metagraph/index.html>)
        * [bittensor.core.settings](<../../settings/index.html>)
        * [bittensor.core.stream](<../../stream/index.html>)
        * [bittensor.core.subtensor](<../../subtensor/index.html>)
        * [bittensor.core.synapse](<../../synapse/index.html>)
        * [bittensor.core.tensor](<../../tensor/index.html>)
        * [bittensor.core.threadpool](<../../threadpool/index.html>)
        * [bittensor.core.types](<../../types/index.html>)
      * [bittensor.extras](<../../../extras/index.html>) __
        * [bittensor.extras.dev_framework](<../../../extras/dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../../../extras/subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../../extras/timelock/index.html>)
      * [bittensor.utils](<../../../utils/index.html>) __
        * [bittensor.utils.axon_utils](<../../../utils/axon_utils/index.html>)
        * [bittensor.utils.balance](<../../../utils/balance/index.html>)
        * [bittensor.utils.btlogging](<../../../utils/btlogging/index.html>)
        * [bittensor.utils.easy_imports](<../../../utils/easy_imports/index.html>)
        * [bittensor.utils.formatting](<../../../utils/formatting/index.html>)
        * [bittensor.utils.liquidity](<../../../utils/liquidity/index.html>)
        * [bittensor.utils.networking](<../../../utils/networking/index.html>)
        * [bittensor.utils.registration](<../../../utils/registration/index.html>)
        * [bittensor.utils.subnets](<../../../utils/subnets/index.html>)
        * [bittensor.utils.version](<../../../utils/version/index.html>)
        * [bittensor.utils.weight_utils](<../../../utils/weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/extrinsics/utils/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/extrinsics/utils/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/extrinsics/utils/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.extrinsics.utils

##  Contents 

  * [Attributes](<#attributes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`MEV_HOTKEY_USAGE_WARNING`](<#bittensor.core.extrinsics.utils.MEV_HOTKEY_USAGE_WARNING>)
    * [`apply_pure_proxy_data()`](<#bittensor.core.extrinsics.utils.apply_pure_proxy_data>)
    * [`compute_coldkey_hash()`](<#bittensor.core.extrinsics.utils.compute_coldkey_hash>)
    * [`get_event_data_by_event_name()`](<#bittensor.core.extrinsics.utils.get_event_data_by_event_name>)
    * [`get_mev_shielded_ciphertext()`](<#bittensor.core.extrinsics.utils.get_mev_shielded_ciphertext>)
    * [`get_old_stakes()`](<#bittensor.core.extrinsics.utils.get_old_stakes>)
    * [`get_transfer_fn_params()`](<#bittensor.core.extrinsics.utils.get_transfer_fn_params>)
    * [`resolve_mev_shield_period()`](<#bittensor.core.extrinsics.utils.resolve_mev_shield_period>)
    * [`sudo_call_extrinsic()`](<#bittensor.core.extrinsics.utils.sudo_call_extrinsic>)
    * [`verify_coldkey_hash()`](<#bittensor.core.extrinsics.utils.verify_coldkey_hash>)



# bittensor.core.extrinsics.utils[#](<#module-bittensor.core.extrinsics.utils> "Link to this heading")

Module with helper functions for extrinsics.

## Attributes[#](<#attributes> "Link to this heading")

[`MEV_HOTKEY_USAGE_WARNING`](<#bittensor.core.extrinsics.utils.MEV_HOTKEY_USAGE_WARNING> "bittensor.core.extrinsics.utils.MEV_HOTKEY_USAGE_WARNING") |   
---|---  
  
## Functions[#](<#functions> "Link to this heading")

[`apply_pure_proxy_data`](<#bittensor.core.extrinsics.utils.apply_pure_proxy_data> "bittensor.core.extrinsics.utils.apply_pure_proxy_data")(response, triggered_events, ...) | Apply pure proxy data to the response object.  
---|---  
[`compute_coldkey_hash`](<#bittensor.core.extrinsics.utils.compute_coldkey_hash> "bittensor.core.extrinsics.utils.compute_coldkey_hash")(keypair) | Computes BlakeTwo256 hash of a coldkey AccountId.  
[`get_event_data_by_event_name`](<#bittensor.core.extrinsics.utils.get_event_data_by_event_name> "bittensor.core.extrinsics.utils.get_event_data_by_event_name")(events, event_name) | Extracts event data from triggered events by event ID.  
[`get_mev_shielded_ciphertext`](<#bittensor.core.extrinsics.utils.get_mev_shielded_ciphertext> "bittensor.core.extrinsics.utils.get_mev_shielded_ciphertext")(signed_ext, ...) | Encrypts a signed extrinsic for MEV Shield submission.  
[`get_old_stakes`](<#bittensor.core.extrinsics.utils.get_old_stakes> "bittensor.core.extrinsics.utils.get_old_stakes")(wallet, hotkey_ss58s, netuids, all_stakes) | Retrieve the previous staking balances for a wallet's hotkeys across given netuids.  
[`get_transfer_fn_params`](<#bittensor.core.extrinsics.utils.get_transfer_fn_params> "bittensor.core.extrinsics.utils.get_transfer_fn_params")(amount, destination_ss58, ...) | Helper function to get the transfer call function and call params, depending on the value and keep_alive flag  
[`resolve_mev_shield_period`](<#bittensor.core.extrinsics.utils.resolve_mev_shield_period> "bittensor.core.extrinsics.utils.resolve_mev_shield_period")(period) | Return effective era period for MEV Shield extrinsics.  
[`sudo_call_extrinsic`](<#bittensor.core.extrinsics.utils.sudo_call_extrinsic> "bittensor.core.extrinsics.utils.sudo_call_extrinsic")(subtensor, wallet, call_function, ...) | Execute a sudo call extrinsic.  
[`verify_coldkey_hash`](<#bittensor.core.extrinsics.utils.verify_coldkey_hash> "bittensor.core.extrinsics.utils.verify_coldkey_hash")(keypair, expected_hash) | Verifies that a coldkey SS58 address matches the expected BlakeTwo256 hash.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.core.extrinsics.utils.MEV_HOTKEY_USAGE_WARNING = 'MeV Shield cannot be used with hotkey-signed extrinsics. The transaction will fail because the...[#](<#bittensor.core.extrinsics.utils.MEV_HOTKEY_USAGE_WARNING> "Link to this definition")
    

bittensor.core.extrinsics.utils.apply_pure_proxy_data(_response_ , _triggered_events_ , _block_number_ , _extrinsic_idx_ , _raise_error_)[#](<#bittensor.core.extrinsics.utils.apply_pure_proxy_data> "Link to this definition")
    

Apply pure proxy data to the response object.

Parameters:
    

  * **response** ([_bittensor.core.types.ExtrinsicResponse_](<../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")) – The response object to update.

  * **triggered_events** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")) – The triggered events of the transaction.

  * **block_number** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The block number of the transaction.

  * **extrinsic_idx** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – The index of the extrinsic in the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to raise an error if the data cannot be applied successfully.



Returns:
    

True if the data was applied successfully, False otherwise.

Return type:
    

[bittensor.core.types.ExtrinsicResponse](<../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

bittensor.core.extrinsics.utils.compute_coldkey_hash(_keypair_)[#](<#bittensor.core.extrinsics.utils.compute_coldkey_hash> "Link to this definition")
    

Computes BlakeTwo256 hash of a coldkey AccountId.

This function extracts the AccountId (32-byte public key) from an SS58 address and computes its BlakeTwo256 hash. The hash is used in coldkey swap announcements to verify the new coldkey address when executing the swap.

Parameters:
    

**keypair** (_bittensor_wallet.Keypair_) – keypair for getting hash.

Returns:
    

Hex string with 0x prefix representing the BlakeTwo256 hash of the AccountId.

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

Notes

  * The hash is computed from the AccountId (public key bytes), not from the SS58 string.

  * This matches the hash computation used in the Subtensor runtime.

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




bittensor.core.extrinsics.utils.get_event_data_by_event_name(_events_ , _event_name_)[#](<#bittensor.core.extrinsics.utils.get_event_data_by_event_name> "Link to this definition")
    

Extracts event data from triggered events by event ID.

Searches through a list of triggered events and returns the attributes dictionary for the first event matching the specified event_id.

Parameters:
    

  * **events** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")) – List of event dictionaries, typically from ExtrinsicReceipt.triggered_events. Each event should have an “module_id”. “event_id” key and an “attributes” key.

  * **event_name** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The events identifier to search for (e.g. “mevShield.EncryptedSubmitted”, etc).



Returns:
    

The attributes dictionary of the matching event, or None if no matching event is found.

Return type:
    

Optional[[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")]

bittensor.core.extrinsics.utils.get_mev_shielded_ciphertext(_signed_ext_ , _ml_kem_768_public_key_)[#](<#bittensor.core.extrinsics.utils.get_mev_shielded_ciphertext> "Link to this definition")
    

Encrypts a signed extrinsic for MEV Shield submission.

This function extracts the raw extrinsic bytes and encrypts them using ML-KEM-768 + XChaCha20Poly1305 with the twox_128 key hash prepended for on-chain validation.

Parameters:
    

  * **signed_ext** (_scalecodec.types.GenericExtrinsic_) – The signed GenericExtrinsic object representing the inner call to be encrypted and executed.

  * **ml_kem_768_public_key** ([_bytes_](<../../../extras/dev_framework/calls/non_sudo_calls/index.html#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes")) – The ML-KEM-768 public key bytes (1184 bytes) from NextKey storage.



Returns:
    

[key_hash(16)][u16 kem_len LE][kem_ct][nonce24][aead_ct]

Return type:
    

The encrypted ciphertext bytes in wire format

bittensor.core.extrinsics.utils.get_old_stakes(_wallet_ , _hotkey_ss58s_ , _netuids_ , _all_stakes_)[#](<#bittensor.core.extrinsics.utils.get_old_stakes> "Link to this definition")
    

Retrieve the previous staking balances for a wallet’s hotkeys across given netuids.

This function searches through the provided staking data to find the stake amounts for the specified hotkeys and netuids associated with the wallet’s coldkey. If no match is found for a particular hotkey and netuid combination, a default balance of zero is returned.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet containing the coldkey to compare with stake data.

  * **hotkey_ss58s** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – List of hotkey SS58 addresses for which stakes are retrieved.

  * **netuids** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – List of network unique identifiers (netuids) corresponding to the hotkeys.

  * **all_stakes** ([_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[__bittensor.core.chain_data.StakeInfo_ _]_) – A collection of all staking information to search through.



Returns:
    

A list of Balances, each representing the stake for a given hotkey and netuid.

Return type:
    

[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")]

bittensor.core.extrinsics.utils.get_transfer_fn_params(_amount_ , _destination_ss58_ , _keep_alive_)[#](<#bittensor.core.extrinsics.utils.get_transfer_fn_params> "Link to this definition")
    

Helper function to get the transfer call function and call params, depending on the value and keep_alive flag provided.

Parameters:
    

  * **amount** (_Optional_ _[_[_bittensor.utils.balance.Balance_](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") _]_) – the amount of Tao to transfer. None if transferring all.

  * **destination_ss58** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – the destination SS58 of the transfer

  * **keep_alive** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – whether to enforce a retention of the existential deposit in the account after transfer.



Returns:
    

tuple[call function, call params]

Return type:
    

[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), Union[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")]]]

bittensor.core.extrinsics.utils.resolve_mev_shield_period(_period_)[#](<#bittensor.core.extrinsics.utils.resolve_mev_shield_period> "Link to this definition")
    

Return effective era period for MEV Shield extrinsics.

MEV Shield extrinsics must use a short-lived era. If period is omitted or exceeds the MEV limit, the maximum allowed MEV period is applied.

Parameters:
    

**period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The period to resolve.

Returns:
    

The effective period (in blocks).

Return type:
    

[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")

bittensor.core.extrinsics.utils.sudo_call_extrinsic(_subtensor_ , _wallet_ , _call_function_ , _call_params_ , _call_module ='AdminUtils'_, _sign_with ='coldkey'_, _use_nonce =False_, _nonce_key ='hotkey'_, _*_ , _period =None_, _raise_error =False_, _wait_for_inclusion =True_, _wait_for_finalization =True_, _root_call =False_)[#](<#bittensor.core.extrinsics.utils.sudo_call_extrinsic> "Link to this definition")
    

Execute a sudo call extrinsic.

Parameters:
    

  * **subtensor** ([_bittensor.core.subtensor.Subtensor_](<../../subtensor/index.html#bittensor.core.subtensor.Subtensor> "bittensor.core.subtensor.Subtensor")) – The Subtensor instance.

  * **wallet** (_bittensor_wallet.Wallet_) – The wallet instance.

  * **call_function** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The call function to execute.

  * **call_params** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")) – The call parameters.

  * **call_module** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The call module.

  * **sign_with** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The keypair to sign the extrinsic with.

  * **use_nonce** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to use a nonce.

  * **nonce_key** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The key to use for the nonce.

  * **period** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – The number of blocks during which the transaction will remain valid after it’s submitted. If the transaction is not included in a block within that number of blocks, it will expire and be rejected. You can think of it as an expiration date for the transaction.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **wait_for_inclusion** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the inclusion of the transaction.

  * **wait_for_finalization** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Whether to wait for the finalization of the transaction.

  * **root_call** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – False, if the subnet owner makes a call.



Returns:
    

The result object of the extrinsic execution.

Return type:
    

[ExtrinsicResponse](<../../types/index.html#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

bittensor.core.extrinsics.utils.verify_coldkey_hash(_keypair_ , _expected_hash_)[#](<#bittensor.core.extrinsics.utils.verify_coldkey_hash> "Link to this definition")
    

Verifies that a coldkey SS58 address matches the expected BlakeTwo256 hash.

This function computes the hash of the coldkey AccountId and compares it with the expected hash. Used to verify that the new coldkey address in a swap announcement matches the announced hash.

Parameters:
    

  * **keypair** (_bittensor_wallet.Keypair_) – keypair whose hash needs to be verified.

  * **expected_hash** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – Expected BlakeTwo256 hash (hex string with 0x prefix).



Returns:
    

True if the computed hash matches the expected hash, False otherwise.

Return type:
    

[bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")

Notes

  * Both hashes are compared in lowercase to handle case differences.

  * See: <<https://docs.learnbittensor.org/keys/coldkey-swap>>




[ __ previous bittensor.core.extrinsics.unstaking ](<../unstaking/index.html> "previous page") [ next bittensor.core.extrinsics.weights __](<../weights/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`MEV_HOTKEY_USAGE_WARNING`](<#bittensor.core.extrinsics.utils.MEV_HOTKEY_USAGE_WARNING>)
    * [`apply_pure_proxy_data()`](<#bittensor.core.extrinsics.utils.apply_pure_proxy_data>)
    * [`compute_coldkey_hash()`](<#bittensor.core.extrinsics.utils.compute_coldkey_hash>)
    * [`get_event_data_by_event_name()`](<#bittensor.core.extrinsics.utils.get_event_data_by_event_name>)
    * [`get_mev_shielded_ciphertext()`](<#bittensor.core.extrinsics.utils.get_mev_shielded_ciphertext>)
    * [`get_old_stakes()`](<#bittensor.core.extrinsics.utils.get_old_stakes>)
    * [`get_transfer_fn_params()`](<#bittensor.core.extrinsics.utils.get_transfer_fn_params>)
    * [`resolve_mev_shield_period()`](<#bittensor.core.extrinsics.utils.resolve_mev_shield_period>)
    * [`sudo_call_extrinsic()`](<#bittensor.core.extrinsics.utils.sudo_call_extrinsic>)
    * [`verify_coldkey_hash()`](<#bittensor.core.extrinsics.utils.verify_coldkey_hash>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.   

  *[*]: Keyword-only parameters separator (PEP 3102)