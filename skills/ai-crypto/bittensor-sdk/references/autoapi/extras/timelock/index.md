# bittensor.extras.timelock &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo-dark-mode.svg) ](<../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../index.html>) __
    * [bittensor](<../../index.html>) __
      * [bittensor.core](<../../core/index.html>) __
        * [bittensor.core.async_subtensor](<../../core/async_subtensor/index.html>)
        * [bittensor.core.axon](<../../core/axon/index.html>)
        * [bittensor.core.chain_data](<../../core/chain_data/index.html>)
        * [bittensor.core.config](<../../core/config/index.html>)
        * [bittensor.core.dendrite](<../../core/dendrite/index.html>)
        * [bittensor.core.errors](<../../core/errors/index.html>)
        * [bittensor.core.extrinsics](<../../core/extrinsics/index.html>)
        * [bittensor.core.metagraph](<../../core/metagraph/index.html>)
        * [bittensor.core.settings](<../../core/settings/index.html>)
        * [bittensor.core.stream](<../../core/stream/index.html>)
        * [bittensor.core.subtensor](<../../core/subtensor/index.html>)
        * [bittensor.core.synapse](<../../core/synapse/index.html>)
        * [bittensor.core.tensor](<../../core/tensor/index.html>)
        * [bittensor.core.threadpool](<../../core/threadpool/index.html>)
        * [bittensor.core.types](<../../core/types/index.html>)
      * [bittensor.extras](<../index.html>) __
        * [bittensor.extras.dev_framework](<../dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../subtensor_api/index.html>)
        * [bittensor.extras.timelock](<#>)
      * [bittensor.utils](<../../utils/index.html>) __
        * [bittensor.utils.axon_utils](<../../utils/axon_utils/index.html>)
        * [bittensor.utils.balance](<../../utils/balance/index.html>)
        * [bittensor.utils.btlogging](<../../utils/btlogging/index.html>)
        * [bittensor.utils.easy_imports](<../../utils/easy_imports/index.html>)
        * [bittensor.utils.formatting](<../../utils/formatting/index.html>)
        * [bittensor.utils.liquidity](<../../utils/liquidity/index.html>)
        * [bittensor.utils.networking](<../../utils/networking/index.html>)
        * [bittensor.utils.registration](<../../utils/registration/index.html>)
        * [bittensor.utils.subnets](<../../utils/subnets/index.html>)
        * [bittensor.utils.version](<../../utils/version/index.html>)
        * [bittensor.utils.weight_utils](<../../utils/weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/extras/timelock/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/extras/timelock/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/extras/timelock/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.extras.timelock

##  Contents 

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`decrypt()`](<#bittensor.extras.timelock.decrypt>)
    * [`encrypt()`](<#bittensor.extras.timelock.encrypt>)
    * [`wait_reveal_and_decrypt()`](<#bittensor.extras.timelock.wait_reveal_and_decrypt>)



# bittensor.extras.timelock[#](<#module-bittensor.extras.timelock> "Link to this heading")

This module provides functionality for TimeLock Encryption (TLE), a mechanism that encrypts data such that it can only be decrypted after a specific amount of time (expressed in the form of Drand rounds). It includes functions for encryption, decryption, and handling the decryption process by waiting for the reveal round. The logic is based on Drand QuickNet.

Main Functions:
    

  * encrypt: Encrypts data and returns the encrypted data along with the reveal round.

  * decrypt: Decrypts the provided encrypted data when the reveal round is reached.

  * wait_reveal_and_decrypt: Waits for the reveal round and decrypts the encrypted data.




Example

``python from bittensor import timelock data = "From Cortex to Bittensor" encrypted_data, reveal_round = timelock.encrypt(data, n_blocks=5) decrypted_data = timelock.wait_reveal_and_decrypt(encrypted_data) ``

Example with custom data:
    

[``](<#id1>)[`](<#id3>)python import pickle from dataclasses import dataclass

from bittensor import timelock

@dataclass class Person:

> name: str age: int

# get instance of your data x_person = Person(“X Lynch”, 123)

# get bytes of your instance byte_data = pickle.dumps(x_person)

# get TLE encoded bytes encrypted, reveal_round = timelock.encrypt(byte_data, 1)

# wait when reveal round appears in Drand QuickNet and get decrypted data decrypted = timelock.wait_reveal_and_decrypt(encrypted_data=encrypted)

# convert bytes into your instance back x_person_2 = pickle.loads(decrypted)

# make sure initial and decoded instances are the same assert x_person == x_person_2 [``](<#id5>)[`](<#id7>)

Note: For handling fast-block nodes, set the block_time parameter to 0.25 seconds during encryption.

## Functions[#](<#functions> "Link to this heading")

[`decrypt`](<#bittensor.extras.timelock.decrypt> "bittensor.extras.timelock.decrypt")(encrypted_data[, no_errors, return_str]) | Decrypts encrypted data using TimeLock Decryption  
---|---  
[`encrypt`](<#bittensor.extras.timelock.encrypt> "bittensor.extras.timelock.encrypt")(data, n_blocks[, block_time]) | Encrypts data using TimeLock Encryption  
[`wait_reveal_and_decrypt`](<#bittensor.extras.timelock.wait_reveal_and_decrypt> "bittensor.extras.timelock.wait_reveal_and_decrypt")(encrypted_data[, ...]) | Waits for reveal round and decrypts data using TimeLock Decryption.  
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.extras.timelock.decrypt(_encrypted_data_ , _no_errors =True_, _return_str =False_)[#](<#bittensor.extras.timelock.decrypt> "Link to this definition")
    

Decrypts encrypted data using TimeLock Decryption

Parameters:
    

  * **encrypted_data** ([_bytes_](<../dev_framework/calls/non_sudo_calls/index.html#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes")) – Encrypted data to be decrypted.

  * **no_errors** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, no errors will be raised during decryption.

  * **return_str** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – convert decrypted data to string if True.



Returns:
    

Decrypted data, when reveled round is reached.

Return type:
    

decrypted_data

Usage:
    

# default usage decrypted_data = decrypt(encrypted_data)

# passing no_errors=False for raising errors during decryption decrypted_data = decrypt(encrypted_data, no_errors=False)

# passing return_str=True for returning decrypted data as string decrypted_data = decrypt(encrypted_data, return_str=True)

bittensor.extras.timelock.encrypt(_data_ , _n_blocks_ , _block_time =12.0_)[#](<#bittensor.extras.timelock.encrypt> "Link to this definition")
    

Encrypts data using TimeLock Encryption

Parameters:
    

  * **data** (_Union_ _[_[_bytes_](<../dev_framework/calls/non_sudo_calls/index.html#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes") _,_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – Any bytes data to be encrypted.

  * **n_blocks** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")) – Number of blocks to encrypt.

  * **block_time** (_Union_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _,_[_float_](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)") _]_) – Time in seconds for each block.



Returns:
    

A tuple containing the encrypted data and reveal TimeLock reveal round.

Return type:
    

[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

Raises:
    

**PyValueError** – If failed to encrypt data.

Usage:
    

data = “From Cortex to Bittensor”

# default usage encrypted_data, reveal_round = encrypt(data, 10)

# passing block_time for fast-blocks node encrypted_data, reveal_round = encrypt(data, 15, block_time=0.25)

encrypted_data, reveal_round = encrypt(data, 5)

Note

For using this function with fast-blocks node you need to set block_time to 0.25 seconds. data, round = encrypt(data, n_blocks, block_time=0.25)

bittensor.extras.timelock.wait_reveal_and_decrypt(_encrypted_data_ , _reveal_round =None_, _no_errors =True_, _return_str =False_)[#](<#bittensor.extras.timelock.wait_reveal_and_decrypt> "Link to this definition")
    

Waits for reveal round and decrypts data using TimeLock Decryption.

Parameters:
    

  * **encrypted_data** ([_bytes_](<../dev_framework/calls/non_sudo_calls/index.html#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes")) – Encrypted data to be decrypted.

  * **reveal_round** (_Optional_ _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]_) – Reveal round to wait for. If None, will be parsed from encrypted data.

  * **no_errors** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – If True, no errors will be raised during decryption.

  * **return_str** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – convert decrypted data to string if True.



Raises:
    

  * [**struct.error**](<https://docs.python.org/3/library/struct.html#struct.error> "\(in Python v3.14\)") – If failed to parse reveal round from encrypted data.

  * [**TypeError**](<https://docs.python.org/3/library/exceptions.html#TypeError> "\(in Python v3.14\)") – If reveal_round is None or wrong type.

  * [**IndexError**](<https://docs.python.org/3/library/exceptions.html#IndexError> "\(in Python v3.14\)") – If provided encrypted_data does not contain reveal round.



Returns:
    

Decrypted data.

Return type:
    

[bytes](<../dev_framework/calls/non_sudo_calls/index.html#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes")

Usage:
    

import bittensor as bt encrypted, reveal_round = bt.timelock.encrypt(“Cortex is power”, 3)

[ __ previous bittensor.extras.subtensor_api.wallets ](<../subtensor_api/wallets/index.html> "previous page") [ next bittensor.utils __](<../../utils/index.html> "next page")

__Contents

  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`decrypt()`](<#bittensor.extras.timelock.decrypt>)
    * [`encrypt()`](<#bittensor.extras.timelock.encrypt>)
    * [`wait_reveal_and_decrypt()`](<#bittensor.extras.timelock.wait_reveal_and_decrypt>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.