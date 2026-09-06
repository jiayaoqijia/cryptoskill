# bittensor.core.errors &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../_static/logo-dark-mode.svg) ](<../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../index.html>) __
    * [bittensor](<../../index.html>) __
      * [bittensor.core](<../index.html>) __
        * [bittensor.core.async_subtensor](<../async_subtensor/index.html>)
        * [bittensor.core.axon](<../axon/index.html>)
        * [bittensor.core.chain_data](<../chain_data/index.html>)
        * [bittensor.core.config](<../config/index.html>)
        * [bittensor.core.dendrite](<../dendrite/index.html>)
        * [bittensor.core.errors](<#>)
        * [bittensor.core.extrinsics](<../extrinsics/index.html>)
        * [bittensor.core.metagraph](<../metagraph/index.html>)
        * [bittensor.core.settings](<../settings/index.html>)
        * [bittensor.core.stream](<../stream/index.html>)
        * [bittensor.core.subtensor](<../subtensor/index.html>)
        * [bittensor.core.synapse](<../synapse/index.html>)
        * [bittensor.core.tensor](<../tensor/index.html>)
        * [bittensor.core.threadpool](<../threadpool/index.html>)
        * [bittensor.core.types](<../types/index.html>)
      * [bittensor.extras](<../../extras/index.html>) __
        * [bittensor.extras.dev_framework](<../../extras/dev_framework/index.html>)
        * [bittensor.extras.subtensor_api](<../../extras/subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../extras/timelock/index.html>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/errors/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/errors/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/core/errors/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.errors

##  Contents 

  * [Attributes](<#attributes>)
  * [Exceptions](<#exceptions>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`BalanceTypeError`](<#bittensor.core.errors.BalanceTypeError>)
    * [`BalanceUnitMismatchError`](<#bittensor.core.errors.BalanceUnitMismatchError>)
    * [`BlacklistedException`](<#bittensor.core.errors.BlacklistedException>)
    * [`ChainConnectionError`](<#bittensor.core.errors.ChainConnectionError>)
    * [`ChainError`](<#bittensor.core.errors.ChainError>)
      * [`ChainError.from_error()`](<#bittensor.core.errors.ChainError.from_error>)
    * [`ChainQueryError`](<#bittensor.core.errors.ChainQueryError>)
    * [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError>)
    * [`DelegateTakeTooHigh`](<#bittensor.core.errors.DelegateTakeTooHigh>)
    * [`DelegateTakeTooLow`](<#bittensor.core.errors.DelegateTakeTooLow>)
    * [`DelegateTxRateLimitExceeded`](<#bittensor.core.errors.DelegateTxRateLimitExceeded>)
    * [`DuplicateChild`](<#bittensor.core.errors.DuplicateChild>)
    * [`HotKeyAccountNotExists`](<#bittensor.core.errors.HotKeyAccountNotExists>)
    * [`IdentityError`](<#bittensor.core.errors.IdentityError>)
    * [`InternalServerError`](<#bittensor.core.errors.InternalServerError>)
    * [`InvalidChild`](<#bittensor.core.errors.InvalidChild>)
    * [`InvalidRequestNameError`](<#bittensor.core.errors.InvalidRequestNameError>)
    * [`MaxAttemptsException`](<#bittensor.core.errors.MaxAttemptsException>)
    * [`MaxSuccessException`](<#bittensor.core.errors.MaxSuccessException>)
    * [`MetadataError`](<#bittensor.core.errors.MetadataError>)
    * [`NominationError`](<#bittensor.core.errors.NominationError>)
    * [`NonAssociatedColdKey`](<#bittensor.core.errors.NonAssociatedColdKey>)
    * [`NotDelegateError`](<#bittensor.core.errors.NotDelegateError>)
    * [`NotEnoughStakeToSetChildkeys`](<#bittensor.core.errors.NotEnoughStakeToSetChildkeys>)
    * [`NotRegisteredError`](<#bittensor.core.errors.NotRegisteredError>)
    * [`NotVerifiedException`](<#bittensor.core.errors.NotVerifiedException>)
    * [`PostProcessException`](<#bittensor.core.errors.PostProcessException>)
    * [`PriorityException`](<#bittensor.core.errors.PriorityException>)
    * [`ProportionOverflow`](<#bittensor.core.errors.ProportionOverflow>)
    * [`RegistrationError`](<#bittensor.core.errors.RegistrationError>)
    * [`RegistrationNotPermittedOnRootSubnet`](<#bittensor.core.errors.RegistrationNotPermittedOnRootSubnet>)
    * [`RunException`](<#bittensor.core.errors.RunException>)
    * [`SHIELD_VALIDATION_ERRORS`](<#bittensor.core.errors.SHIELD_VALIDATION_ERRORS>)
    * [`StakeError`](<#bittensor.core.errors.StakeError>)
    * [`SubnetNotExists`](<#bittensor.core.errors.SubnetNotExists>)
    * [`SynapseDendriteNoneException`](<#bittensor.core.errors.SynapseDendriteNoneException>)
      * [`SynapseDendriteNoneException.message`](<#bittensor.core.errors.SynapseDendriteNoneException.message>)
    * [`SynapseException`](<#bittensor.core.errors.SynapseException>)
      * [`SynapseException.message`](<#bittensor.core.errors.SynapseException.message>)
      * [`SynapseException.synapse`](<#bittensor.core.errors.SynapseException.synapse>)
    * [`SynapseParsingError`](<#bittensor.core.errors.SynapseParsingError>)
    * [`TakeError`](<#bittensor.core.errors.TakeError>)
    * [`TooManyChildren`](<#bittensor.core.errors.TooManyChildren>)
    * [`TransferError`](<#bittensor.core.errors.TransferError>)
    * [`TxRateLimitExceeded`](<#bittensor.core.errors.TxRateLimitExceeded>)
    * [`UnknownSynapseError`](<#bittensor.core.errors.UnknownSynapseError>)
    * [`UnstakeError`](<#bittensor.core.errors.UnstakeError>)
    * [`map_shield_error()`](<#bittensor.core.errors.map_shield_error>)



# bittensor.core.errors[#](<#module-bittensor.core.errors> "Link to this heading")

## Attributes[#](<#attributes> "Link to this heading")

[`SHIELD_VALIDATION_ERRORS`](<#bittensor.core.errors.SHIELD_VALIDATION_ERRORS> "bittensor.core.errors.SHIELD_VALIDATION_ERRORS") |   
---|---  
  
## Exceptions[#](<#exceptions> "Link to this heading")

[`BalanceTypeError`](<#bittensor.core.errors.BalanceTypeError> "bittensor.core.errors.BalanceTypeError") | Raised when a Balance object receives an invalid type.  
---|---  
[`BalanceUnitMismatchError`](<#bittensor.core.errors.BalanceUnitMismatchError> "bittensor.core.errors.BalanceUnitMismatchError") | Raised when Balance objects with different units are used in operations.  
[`BlacklistedException`](<#bittensor.core.errors.BlacklistedException> "bittensor.core.errors.BlacklistedException") | This exception is raised when the request is blacklisted.  
[`InternalServerError`](<#bittensor.core.errors.InternalServerError> "bittensor.core.errors.InternalServerError") | This exception is raised when the requested function fails on the server. Indicates a server error.  
[`InvalidRequestNameError`](<#bittensor.core.errors.InvalidRequestNameError> "bittensor.core.errors.InvalidRequestNameError") | This exception is raised when the request name is invalid. Usually indicates a broken URL.  
[`MaxAttemptsException`](<#bittensor.core.errors.MaxAttemptsException> "bittensor.core.errors.MaxAttemptsException") | Raised when the POW Solver has reached the max number of attempts.  
[`MaxSuccessException`](<#bittensor.core.errors.MaxSuccessException> "bittensor.core.errors.MaxSuccessException") | Raised when the POW Solver has reached the max number of successful solutions.  
[`NotVerifiedException`](<#bittensor.core.errors.NotVerifiedException> "bittensor.core.errors.NotVerifiedException") | This exception is raised when the request is not verified.  
[`PostProcessException`](<#bittensor.core.errors.PostProcessException> "bittensor.core.errors.PostProcessException") | This exception is raised when the response headers cannot be updated.  
[`PriorityException`](<#bittensor.core.errors.PriorityException> "bittensor.core.errors.PriorityException") | This exception is raised when the request priority is not met.  
[`RunException`](<#bittensor.core.errors.RunException> "bittensor.core.errors.RunException") | This exception is raised when the requested function cannot be executed. Indicates a server error.  
[`SynapseDendriteNoneException`](<#bittensor.core.errors.SynapseDendriteNoneException> "bittensor.core.errors.SynapseDendriteNoneException") | Common base class for all non-exit exceptions.  
[`SynapseException`](<#bittensor.core.errors.SynapseException> "bittensor.core.errors.SynapseException") | Common base class for all non-exit exceptions.  
[`SynapseParsingError`](<#bittensor.core.errors.SynapseParsingError> "bittensor.core.errors.SynapseParsingError") | This exception is raised when the request headers are unable to be parsed into the synapse type.  
[`UnknownSynapseError`](<#bittensor.core.errors.UnknownSynapseError> "bittensor.core.errors.UnknownSynapseError") | This exception is raised when the request name is not found in the Axon's forward_fns dictionary.  
  
## Classes[#](<#classes> "Link to this heading")

[`ChainConnectionError`](<#bittensor.core.errors.ChainConnectionError> "bittensor.core.errors.ChainConnectionError") | Error for any chain connection related errors.  
---|---  
[`ChainError`](<#bittensor.core.errors.ChainError> "bittensor.core.errors.ChainError") | Base error for any chain related errors.  
[`ChainQueryError`](<#bittensor.core.errors.ChainQueryError> "bittensor.core.errors.ChainQueryError") | Error for any chain query related errors.  
[`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError") | Error for any chain transaction related errors.  
[`DelegateTakeTooHigh`](<#bittensor.core.errors.DelegateTakeTooHigh> "bittensor.core.errors.DelegateTakeTooHigh") | Delegate take is too high.  
[`DelegateTakeTooLow`](<#bittensor.core.errors.DelegateTakeTooLow> "bittensor.core.errors.DelegateTakeTooLow") | Delegate take is too low.  
[`DelegateTxRateLimitExceeded`](<#bittensor.core.errors.DelegateTxRateLimitExceeded> "bittensor.core.errors.DelegateTxRateLimitExceeded") | A transactor exceeded the rate limit for delegate transaction.  
[`DuplicateChild`](<#bittensor.core.errors.DuplicateChild> "bittensor.core.errors.DuplicateChild") | Duplicate child when setting children.  
[`HotKeyAccountNotExists`](<#bittensor.core.errors.HotKeyAccountNotExists> "bittensor.core.errors.HotKeyAccountNotExists") | The hotkey does not exist.  
[`IdentityError`](<#bittensor.core.errors.IdentityError> "bittensor.core.errors.IdentityError") | Error raised when an identity transaction fails.  
[`InvalidChild`](<#bittensor.core.errors.InvalidChild> "bittensor.core.errors.InvalidChild") | Attempting to set an invalid child for a hotkey on a network.  
[`MetadataError`](<#bittensor.core.errors.MetadataError> "bittensor.core.errors.MetadataError") | Error raised when metadata commitment transaction fails.  
[`NominationError`](<#bittensor.core.errors.NominationError> "bittensor.core.errors.NominationError") | Error raised when a nomination transaction fails.  
[`NonAssociatedColdKey`](<#bittensor.core.errors.NonAssociatedColdKey> "bittensor.core.errors.NonAssociatedColdKey") | Request to stake, unstake or subscribe is made by a coldkey that is not associated with the hotkey account.  
[`NotDelegateError`](<#bittensor.core.errors.NotDelegateError> "bittensor.core.errors.NotDelegateError") | Error raised when a hotkey you are trying to stake to is not a delegate.  
[`NotEnoughStakeToSetChildkeys`](<#bittensor.core.errors.NotEnoughStakeToSetChildkeys> "bittensor.core.errors.NotEnoughStakeToSetChildkeys") | The parent hotkey doesn't have enough own stake to set childkeys.  
[`NotRegisteredError`](<#bittensor.core.errors.NotRegisteredError> "bittensor.core.errors.NotRegisteredError") | Error raised when a neuron is not registered, and the transaction requires it to be.  
[`ProportionOverflow`](<#bittensor.core.errors.ProportionOverflow> "bittensor.core.errors.ProportionOverflow") | Proportion overflow when setting children.  
[`RegistrationError`](<#bittensor.core.errors.RegistrationError> "bittensor.core.errors.RegistrationError") | Error raised when a neuron registration transaction fails.  
[`RegistrationNotPermittedOnRootSubnet`](<#bittensor.core.errors.RegistrationNotPermittedOnRootSubnet> "bittensor.core.errors.RegistrationNotPermittedOnRootSubnet") | Operation is not permitted on the root subnet.  
[`StakeError`](<#bittensor.core.errors.StakeError> "bittensor.core.errors.StakeError") | Error raised when a stake transaction fails.  
[`SubnetNotExists`](<#bittensor.core.errors.SubnetNotExists> "bittensor.core.errors.SubnetNotExists") | The subnet does not exist.  
[`TakeError`](<#bittensor.core.errors.TakeError> "bittensor.core.errors.TakeError") | Error raised when an increase / decrease take transaction fails.  
[`TooManyChildren`](<#bittensor.core.errors.TooManyChildren> "bittensor.core.errors.TooManyChildren") | Too many children MAX 5.  
[`TransferError`](<#bittensor.core.errors.TransferError> "bittensor.core.errors.TransferError") | Error raised when a transfer transaction fails.  
[`TxRateLimitExceeded`](<#bittensor.core.errors.TxRateLimitExceeded> "bittensor.core.errors.TxRateLimitExceeded") | Default transaction rate limit exceeded.  
[`UnstakeError`](<#bittensor.core.errors.UnstakeError> "bittensor.core.errors.UnstakeError") | Error raised when an unstake transaction fails.  
  
## Functions[#](<#functions> "Link to this heading")

[`map_shield_error`](<#bittensor.core.errors.map_shield_error> "bittensor.core.errors.map_shield_error")(raw_message) | Map a raw shield validation error to a human-readable description.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

exception bittensor.core.errors.BalanceTypeError[#](<#bittensor.core.errors.BalanceTypeError> "Link to this definition")
    

Bases: [`Exception`](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)")

Raised when a Balance object receives an invalid type.

Initialize self. See help(type(self)) for accurate signature.

exception bittensor.core.errors.BalanceUnitMismatchError[#](<#bittensor.core.errors.BalanceUnitMismatchError> "Link to this definition")
    

Bases: [`Exception`](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)")

Raised when Balance objects with different units are used in operations.

Initialize self. See help(type(self)) for accurate signature.

exception bittensor.core.errors.BlacklistedException(_message ='Synapse Exception'_, _synapse =None_)[#](<#bittensor.core.errors.BlacklistedException> "Link to this definition")
    

Bases: [`SynapseException`](<#bittensor.core.errors.SynapseException> "bittensor.core.errors.SynapseException")

This exception is raised when the request is blacklisted.

Initialize self. See help(type(self)) for accurate signature.

Parameters:
    

**synapse** (_Optional_ _[_[_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse") _]_)

class bittensor.core.errors.ChainConnectionError[#](<#bittensor.core.errors.ChainConnectionError> "Link to this definition")
    

Bases: [`ChainError`](<#bittensor.core.errors.ChainError> "bittensor.core.errors.ChainError")

Error for any chain connection related errors.

class bittensor.core.errors.ChainError[#](<#bittensor.core.errors.ChainError> "Link to this definition")
    

Bases: `async_substrate_interface.errors.SubstrateRequestException`

Base error for any chain related errors.

classmethod from_error(_error_)[#](<#bittensor.core.errors.ChainError.from_error> "Link to this definition")
    

class bittensor.core.errors.ChainQueryError[#](<#bittensor.core.errors.ChainQueryError> "Link to this definition")
    

Bases: [`ChainError`](<#bittensor.core.errors.ChainError> "bittensor.core.errors.ChainError")

Error for any chain query related errors.

class bittensor.core.errors.ChainTransactionError[#](<#bittensor.core.errors.ChainTransactionError> "Link to this definition")
    

Bases: [`ChainError`](<#bittensor.core.errors.ChainError> "bittensor.core.errors.ChainError")

Error for any chain transaction related errors.

class bittensor.core.errors.DelegateTakeTooHigh[#](<#bittensor.core.errors.DelegateTakeTooHigh> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Delegate take is too high.

class bittensor.core.errors.DelegateTakeTooLow[#](<#bittensor.core.errors.DelegateTakeTooLow> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Delegate take is too low.

class bittensor.core.errors.DelegateTxRateLimitExceeded[#](<#bittensor.core.errors.DelegateTxRateLimitExceeded> "Link to this definition")
    

Bases: [`TxRateLimitExceeded`](<#bittensor.core.errors.TxRateLimitExceeded> "bittensor.core.errors.TxRateLimitExceeded")

A transactor exceeded the rate limit for delegate transaction.

class bittensor.core.errors.DuplicateChild[#](<#bittensor.core.errors.DuplicateChild> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Duplicate child when setting children.

class bittensor.core.errors.HotKeyAccountNotExists[#](<#bittensor.core.errors.HotKeyAccountNotExists> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

The hotkey does not exist.

class bittensor.core.errors.IdentityError[#](<#bittensor.core.errors.IdentityError> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Error raised when an identity transaction fails.

exception bittensor.core.errors.InternalServerError(_message ='Synapse Exception'_, _synapse =None_)[#](<#bittensor.core.errors.InternalServerError> "Link to this definition")
    

Bases: [`SynapseException`](<#bittensor.core.errors.SynapseException> "bittensor.core.errors.SynapseException")

This exception is raised when the requested function fails on the server. Indicates a server error.

Initialize self. See help(type(self)) for accurate signature.

Parameters:
    

**synapse** (_Optional_ _[_[_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse") _]_)

class bittensor.core.errors.InvalidChild[#](<#bittensor.core.errors.InvalidChild> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Attempting to set an invalid child for a hotkey on a network.

exception bittensor.core.errors.InvalidRequestNameError[#](<#bittensor.core.errors.InvalidRequestNameError> "Link to this definition")
    

Bases: [`Exception`](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)")

This exception is raised when the request name is invalid. Usually indicates a broken URL.

Initialize self. See help(type(self)) for accurate signature.

exception bittensor.core.errors.MaxAttemptsException[#](<#bittensor.core.errors.MaxAttemptsException> "Link to this definition")
    

Bases: [`Exception`](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)")

Raised when the POW Solver has reached the max number of attempts.

Initialize self. See help(type(self)) for accurate signature.

exception bittensor.core.errors.MaxSuccessException[#](<#bittensor.core.errors.MaxSuccessException> "Link to this definition")
    

Bases: [`Exception`](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)")

Raised when the POW Solver has reached the max number of successful solutions.

Initialize self. See help(type(self)) for accurate signature.

class bittensor.core.errors.MetadataError[#](<#bittensor.core.errors.MetadataError> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Error raised when metadata commitment transaction fails.

class bittensor.core.errors.NominationError[#](<#bittensor.core.errors.NominationError> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Error raised when a nomination transaction fails.

class bittensor.core.errors.NonAssociatedColdKey[#](<#bittensor.core.errors.NonAssociatedColdKey> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Request to stake, unstake or subscribe is made by a coldkey that is not associated with the hotkey account.

class bittensor.core.errors.NotDelegateError[#](<#bittensor.core.errors.NotDelegateError> "Link to this definition")
    

Bases: [`StakeError`](<#bittensor.core.errors.StakeError> "bittensor.core.errors.StakeError")

Error raised when a hotkey you are trying to stake to is not a delegate.

class bittensor.core.errors.NotEnoughStakeToSetChildkeys[#](<#bittensor.core.errors.NotEnoughStakeToSetChildkeys> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

The parent hotkey doesn’t have enough own stake to set childkeys.

class bittensor.core.errors.NotRegisteredError[#](<#bittensor.core.errors.NotRegisteredError> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Error raised when a neuron is not registered, and the transaction requires it to be.

exception bittensor.core.errors.NotVerifiedException(_message ='Synapse Exception'_, _synapse =None_)[#](<#bittensor.core.errors.NotVerifiedException> "Link to this definition")
    

Bases: [`SynapseException`](<#bittensor.core.errors.SynapseException> "bittensor.core.errors.SynapseException")

This exception is raised when the request is not verified.

Initialize self. See help(type(self)) for accurate signature.

Parameters:
    

**synapse** (_Optional_ _[_[_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse") _]_)

exception bittensor.core.errors.PostProcessException(_message ='Synapse Exception'_, _synapse =None_)[#](<#bittensor.core.errors.PostProcessException> "Link to this definition")
    

Bases: [`SynapseException`](<#bittensor.core.errors.SynapseException> "bittensor.core.errors.SynapseException")

This exception is raised when the response headers cannot be updated.

Initialize self. See help(type(self)) for accurate signature.

Parameters:
    

**synapse** (_Optional_ _[_[_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse") _]_)

exception bittensor.core.errors.PriorityException(_message ='Synapse Exception'_, _synapse =None_)[#](<#bittensor.core.errors.PriorityException> "Link to this definition")
    

Bases: [`SynapseException`](<#bittensor.core.errors.SynapseException> "bittensor.core.errors.SynapseException")

This exception is raised when the request priority is not met.

Initialize self. See help(type(self)) for accurate signature.

Parameters:
    

**synapse** (_Optional_ _[_[_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse") _]_)

class bittensor.core.errors.ProportionOverflow[#](<#bittensor.core.errors.ProportionOverflow> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Proportion overflow when setting children.

class bittensor.core.errors.RegistrationError[#](<#bittensor.core.errors.RegistrationError> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Error raised when a neuron registration transaction fails.

class bittensor.core.errors.RegistrationNotPermittedOnRootSubnet[#](<#bittensor.core.errors.RegistrationNotPermittedOnRootSubnet> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Operation is not permitted on the root subnet.

exception bittensor.core.errors.RunException(_message ='Synapse Exception'_, _synapse =None_)[#](<#bittensor.core.errors.RunException> "Link to this definition")
    

Bases: [`SynapseException`](<#bittensor.core.errors.SynapseException> "bittensor.core.errors.SynapseException")

This exception is raised when the requested function cannot be executed. Indicates a server error.

Initialize self. See help(type(self)) for accurate signature.

Parameters:
    

**synapse** (_Optional_ _[_[_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse") _]_)

bittensor.core.errors.SHIELD_VALIDATION_ERRORS[#](<#bittensor.core.errors.SHIELD_VALIDATION_ERRORS> "Link to this definition")
    

class bittensor.core.errors.StakeError[#](<#bittensor.core.errors.StakeError> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Error raised when a stake transaction fails.

class bittensor.core.errors.SubnetNotExists[#](<#bittensor.core.errors.SubnetNotExists> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

The subnet does not exist.

exception bittensor.core.errors.SynapseDendriteNoneException(_message ='Synapse Dendrite is None'_, _synapse =None_)[#](<#bittensor.core.errors.SynapseDendriteNoneException> "Link to this definition")
    

Bases: [`SynapseException`](<#bittensor.core.errors.SynapseException> "bittensor.core.errors.SynapseException")

Common base class for all non-exit exceptions.

Initialize self. See help(type(self)) for accurate signature.

Parameters:
    

**synapse** (_Optional_ _[_[_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse") _]_)

message = 'Synapse Dendrite is None'[#](<#bittensor.core.errors.SynapseDendriteNoneException.message> "Link to this definition")
    

exception bittensor.core.errors.SynapseException(_message ='Synapse Exception'_, _synapse =None_)[#](<#bittensor.core.errors.SynapseException> "Link to this definition")
    

Bases: [`Exception`](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)")

Common base class for all non-exit exceptions.

Initialize self. See help(type(self)) for accurate signature.

Parameters:
    

**synapse** (_Optional_ _[_[_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse") _]_)

message = 'Synapse Exception'[#](<#bittensor.core.errors.SynapseException.message> "Link to this definition")
    

synapse = None[#](<#bittensor.core.errors.SynapseException.synapse> "Link to this definition")
    

exception bittensor.core.errors.SynapseParsingError[#](<#bittensor.core.errors.SynapseParsingError> "Link to this definition")
    

Bases: [`Exception`](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)")

This exception is raised when the request headers are unable to be parsed into the synapse type.

Initialize self. See help(type(self)) for accurate signature.

class bittensor.core.errors.TakeError[#](<#bittensor.core.errors.TakeError> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Error raised when an increase / decrease take transaction fails.

class bittensor.core.errors.TooManyChildren[#](<#bittensor.core.errors.TooManyChildren> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Too many children MAX 5.

class bittensor.core.errors.TransferError[#](<#bittensor.core.errors.TransferError> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Error raised when a transfer transaction fails.

class bittensor.core.errors.TxRateLimitExceeded[#](<#bittensor.core.errors.TxRateLimitExceeded> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Default transaction rate limit exceeded.

exception bittensor.core.errors.UnknownSynapseError(_message ='Synapse Exception'_, _synapse =None_)[#](<#bittensor.core.errors.UnknownSynapseError> "Link to this definition")
    

Bases: [`SynapseException`](<#bittensor.core.errors.SynapseException> "bittensor.core.errors.SynapseException")

This exception is raised when the request name is not found in the Axon’s forward_fns dictionary.

Initialize self. See help(type(self)) for accurate signature.

Parameters:
    

**synapse** (_Optional_ _[_[_bittensor.core.synapse.Synapse_](<../synapse/index.html#bittensor.core.synapse.Synapse> "bittensor.core.synapse.Synapse") _]_)

class bittensor.core.errors.UnstakeError[#](<#bittensor.core.errors.UnstakeError> "Link to this definition")
    

Bases: [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError> "bittensor.core.errors.ChainTransactionError")

Error raised when an unstake transaction fails.

bittensor.core.errors.map_shield_error(_raw_message_)[#](<#bittensor.core.errors.map_shield_error> "Link to this definition")
    

Map a raw shield validation error to a human-readable description.

Checks the message against known Custom error codes from CheckShieldedTxValidity, then falls back to detecting a generic `"invalid"` subscription status. Returns the original message unchanged if nothing matches.

Parameters:
    

**raw_message** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

Return type:
    

[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")

[ __ previous bittensor.core.dendrite ](<../dendrite/index.html> "previous page") [ next bittensor.core.extrinsics __](<../extrinsics/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Exceptions](<#exceptions>)
  * [Classes](<#classes>)
  * [Functions](<#functions>)
  * [Module Contents](<#module-contents>)
    * [`BalanceTypeError`](<#bittensor.core.errors.BalanceTypeError>)
    * [`BalanceUnitMismatchError`](<#bittensor.core.errors.BalanceUnitMismatchError>)
    * [`BlacklistedException`](<#bittensor.core.errors.BlacklistedException>)
    * [`ChainConnectionError`](<#bittensor.core.errors.ChainConnectionError>)
    * [`ChainError`](<#bittensor.core.errors.ChainError>)
      * [`ChainError.from_error()`](<#bittensor.core.errors.ChainError.from_error>)
    * [`ChainQueryError`](<#bittensor.core.errors.ChainQueryError>)
    * [`ChainTransactionError`](<#bittensor.core.errors.ChainTransactionError>)
    * [`DelegateTakeTooHigh`](<#bittensor.core.errors.DelegateTakeTooHigh>)
    * [`DelegateTakeTooLow`](<#bittensor.core.errors.DelegateTakeTooLow>)
    * [`DelegateTxRateLimitExceeded`](<#bittensor.core.errors.DelegateTxRateLimitExceeded>)
    * [`DuplicateChild`](<#bittensor.core.errors.DuplicateChild>)
    * [`HotKeyAccountNotExists`](<#bittensor.core.errors.HotKeyAccountNotExists>)
    * [`IdentityError`](<#bittensor.core.errors.IdentityError>)
    * [`InternalServerError`](<#bittensor.core.errors.InternalServerError>)
    * [`InvalidChild`](<#bittensor.core.errors.InvalidChild>)
    * [`InvalidRequestNameError`](<#bittensor.core.errors.InvalidRequestNameError>)
    * [`MaxAttemptsException`](<#bittensor.core.errors.MaxAttemptsException>)
    * [`MaxSuccessException`](<#bittensor.core.errors.MaxSuccessException>)
    * [`MetadataError`](<#bittensor.core.errors.MetadataError>)
    * [`NominationError`](<#bittensor.core.errors.NominationError>)
    * [`NonAssociatedColdKey`](<#bittensor.core.errors.NonAssociatedColdKey>)
    * [`NotDelegateError`](<#bittensor.core.errors.NotDelegateError>)
    * [`NotEnoughStakeToSetChildkeys`](<#bittensor.core.errors.NotEnoughStakeToSetChildkeys>)
    * [`NotRegisteredError`](<#bittensor.core.errors.NotRegisteredError>)
    * [`NotVerifiedException`](<#bittensor.core.errors.NotVerifiedException>)
    * [`PostProcessException`](<#bittensor.core.errors.PostProcessException>)
    * [`PriorityException`](<#bittensor.core.errors.PriorityException>)
    * [`ProportionOverflow`](<#bittensor.core.errors.ProportionOverflow>)
    * [`RegistrationError`](<#bittensor.core.errors.RegistrationError>)
    * [`RegistrationNotPermittedOnRootSubnet`](<#bittensor.core.errors.RegistrationNotPermittedOnRootSubnet>)
    * [`RunException`](<#bittensor.core.errors.RunException>)
    * [`SHIELD_VALIDATION_ERRORS`](<#bittensor.core.errors.SHIELD_VALIDATION_ERRORS>)
    * [`StakeError`](<#bittensor.core.errors.StakeError>)
    * [`SubnetNotExists`](<#bittensor.core.errors.SubnetNotExists>)
    * [`SynapseDendriteNoneException`](<#bittensor.core.errors.SynapseDendriteNoneException>)
      * [`SynapseDendriteNoneException.message`](<#bittensor.core.errors.SynapseDendriteNoneException.message>)
    * [`SynapseException`](<#bittensor.core.errors.SynapseException>)
      * [`SynapseException.message`](<#bittensor.core.errors.SynapseException.message>)
      * [`SynapseException.synapse`](<#bittensor.core.errors.SynapseException.synapse>)
    * [`SynapseParsingError`](<#bittensor.core.errors.SynapseParsingError>)
    * [`TakeError`](<#bittensor.core.errors.TakeError>)
    * [`TooManyChildren`](<#bittensor.core.errors.TooManyChildren>)
    * [`TransferError`](<#bittensor.core.errors.TransferError>)
    * [`TxRateLimitExceeded`](<#bittensor.core.errors.TxRateLimitExceeded>)
    * [`UnknownSynapseError`](<#bittensor.core.errors.UnknownSynapseError>)
    * [`UnstakeError`](<#bittensor.core.errors.UnstakeError>)
    * [`map_shield_error()`](<#bittensor.core.errors.map_shield_error>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.