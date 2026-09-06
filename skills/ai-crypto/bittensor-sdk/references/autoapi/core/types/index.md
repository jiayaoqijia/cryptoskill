# bittensor.core.types &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.core.errors](<../errors/index.html>)
        * [bittensor.core.extrinsics](<../extrinsics/index.html>)
        * [bittensor.core.metagraph](<../metagraph/index.html>)
        * [bittensor.core.settings](<../settings/index.html>)
        * [bittensor.core.stream](<../stream/index.html>)
        * [bittensor.core.subtensor](<../subtensor/index.html>)
        * [bittensor.core.synapse](<../synapse/index.html>)
        * [bittensor.core.tensor](<../tensor/index.html>)
        * [bittensor.core.threadpool](<../threadpool/index.html>)
        * [bittensor.core.types](<#>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/types/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/types/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/core/types/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.types

##  Contents 

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`AxonServeCallParams`](<#bittensor.core.types.AxonServeCallParams>)
      * [`AxonServeCallParams.as_dict()`](<#bittensor.core.types.AxonServeCallParams.as_dict>)
      * [`AxonServeCallParams.certificate`](<#bittensor.core.types.AxonServeCallParams.certificate>)
      * [`AxonServeCallParams.coldkey`](<#bittensor.core.types.AxonServeCallParams.coldkey>)
      * [`AxonServeCallParams.copy()`](<#bittensor.core.types.AxonServeCallParams.copy>)
      * [`AxonServeCallParams.hotkey`](<#bittensor.core.types.AxonServeCallParams.hotkey>)
      * [`AxonServeCallParams.ip`](<#bittensor.core.types.AxonServeCallParams.ip>)
      * [`AxonServeCallParams.ip_type`](<#bittensor.core.types.AxonServeCallParams.ip_type>)
      * [`AxonServeCallParams.netuid`](<#bittensor.core.types.AxonServeCallParams.netuid>)
      * [`AxonServeCallParams.placeholder1`](<#bittensor.core.types.AxonServeCallParams.placeholder1>)
      * [`AxonServeCallParams.placeholder2`](<#bittensor.core.types.AxonServeCallParams.placeholder2>)
      * [`AxonServeCallParams.port`](<#bittensor.core.types.AxonServeCallParams.port>)
      * [`AxonServeCallParams.protocol`](<#bittensor.core.types.AxonServeCallParams.protocol>)
      * [`AxonServeCallParams.version`](<#bittensor.core.types.AxonServeCallParams.version>)
    * [`BlockInfo`](<#bittensor.core.types.BlockInfo>)
      * [`BlockInfo.explorer`](<#bittensor.core.types.BlockInfo.explorer>)
      * [`BlockInfo.extrinsics`](<#bittensor.core.types.BlockInfo.extrinsics>)
      * [`BlockInfo.hash`](<#bittensor.core.types.BlockInfo.hash>)
      * [`BlockInfo.header`](<#bittensor.core.types.BlockInfo.header>)
      * [`BlockInfo.number`](<#bittensor.core.types.BlockInfo.number>)
      * [`BlockInfo.timestamp`](<#bittensor.core.types.BlockInfo.timestamp>)
    * [`CommitmentOfResponse`](<#bittensor.core.types.CommitmentOfResponse>)
      * [`CommitmentOfResponse.block`](<#bittensor.core.types.CommitmentOfResponse.block>)
      * [`CommitmentOfResponse.deposit`](<#bittensor.core.types.CommitmentOfResponse.deposit>)
      * [`CommitmentOfResponse.info`](<#bittensor.core.types.CommitmentOfResponse.info>)
    * [`CrowdloansResponse`](<#bittensor.core.types.CrowdloansResponse>)
      * [`CrowdloansResponse.call`](<#bittensor.core.types.CrowdloansResponse.call>)
      * [`CrowdloansResponse.cap`](<#bittensor.core.types.CrowdloansResponse.cap>)
      * [`CrowdloansResponse.contributors_count`](<#bittensor.core.types.CrowdloansResponse.contributors_count>)
      * [`CrowdloansResponse.creator`](<#bittensor.core.types.CrowdloansResponse.creator>)
      * [`CrowdloansResponse.deposit`](<#bittensor.core.types.CrowdloansResponse.deposit>)
      * [`CrowdloansResponse.end`](<#bittensor.core.types.CrowdloansResponse.end>)
      * [`CrowdloansResponse.finalized`](<#bittensor.core.types.CrowdloansResponse.finalized>)
      * [`CrowdloansResponse.funds_account`](<#bittensor.core.types.CrowdloansResponse.funds_account>)
      * [`CrowdloansResponse.min_contribution`](<#bittensor.core.types.CrowdloansResponse.min_contribution>)
      * [`CrowdloansResponse.raised`](<#bittensor.core.types.CrowdloansResponse.raised>)
      * [`CrowdloansResponse.target_address`](<#bittensor.core.types.CrowdloansResponse.target_address>)
    * [`DynamicInfoResponse`](<#bittensor.core.types.DynamicInfoResponse>)
      * [`DynamicInfoResponse.alpha_in`](<#bittensor.core.types.DynamicInfoResponse.alpha_in>)
      * [`DynamicInfoResponse.alpha_in_emission`](<#bittensor.core.types.DynamicInfoResponse.alpha_in_emission>)
      * [`DynamicInfoResponse.alpha_out`](<#bittensor.core.types.DynamicInfoResponse.alpha_out>)
      * [`DynamicInfoResponse.alpha_out_emission`](<#bittensor.core.types.DynamicInfoResponse.alpha_out_emission>)
      * [`DynamicInfoResponse.blocks_since_last_step`](<#bittensor.core.types.DynamicInfoResponse.blocks_since_last_step>)
      * [`DynamicInfoResponse.emission`](<#bittensor.core.types.DynamicInfoResponse.emission>)
      * [`DynamicInfoResponse.last_step`](<#bittensor.core.types.DynamicInfoResponse.last_step>)
      * [`DynamicInfoResponse.moving_price`](<#bittensor.core.types.DynamicInfoResponse.moving_price>)
      * [`DynamicInfoResponse.netuid`](<#bittensor.core.types.DynamicInfoResponse.netuid>)
      * [`DynamicInfoResponse.network_registered_at`](<#bittensor.core.types.DynamicInfoResponse.network_registered_at>)
      * [`DynamicInfoResponse.owner_coldkey`](<#bittensor.core.types.DynamicInfoResponse.owner_coldkey>)
      * [`DynamicInfoResponse.owner_hotkey`](<#bittensor.core.types.DynamicInfoResponse.owner_hotkey>)
      * [`DynamicInfoResponse.pending_alpha_emission`](<#bittensor.core.types.DynamicInfoResponse.pending_alpha_emission>)
      * [`DynamicInfoResponse.pending_root_emission`](<#bittensor.core.types.DynamicInfoResponse.pending_root_emission>)
      * [`DynamicInfoResponse.price`](<#bittensor.core.types.DynamicInfoResponse.price>)
      * [`DynamicInfoResponse.subnet_identity`](<#bittensor.core.types.DynamicInfoResponse.subnet_identity>)
      * [`DynamicInfoResponse.subnet_name`](<#bittensor.core.types.DynamicInfoResponse.subnet_name>)
      * [`DynamicInfoResponse.subnet_volume`](<#bittensor.core.types.DynamicInfoResponse.subnet_volume>)
      * [`DynamicInfoResponse.tao_in`](<#bittensor.core.types.DynamicInfoResponse.tao_in>)
      * [`DynamicInfoResponse.tao_in_emission`](<#bittensor.core.types.DynamicInfoResponse.tao_in_emission>)
      * [`DynamicInfoResponse.tempo`](<#bittensor.core.types.DynamicInfoResponse.tempo>)
      * [`DynamicInfoResponse.token_symbol`](<#bittensor.core.types.DynamicInfoResponse.token_symbol>)
    * [`ExtrinsicResponse`](<#bittensor.core.types.ExtrinsicResponse>)
      * [`ExtrinsicResponse.as_dict()`](<#bittensor.core.types.ExtrinsicResponse.as_dict>)
      * [`ExtrinsicResponse.data`](<#bittensor.core.types.ExtrinsicResponse.data>)
      * [`ExtrinsicResponse.error`](<#bittensor.core.types.ExtrinsicResponse.error>)
      * [`ExtrinsicResponse.extrinsic`](<#bittensor.core.types.ExtrinsicResponse.extrinsic>)
      * [`ExtrinsicResponse.extrinsic_fee`](<#bittensor.core.types.ExtrinsicResponse.extrinsic_fee>)
      * [`ExtrinsicResponse.extrinsic_function`](<#bittensor.core.types.ExtrinsicResponse.extrinsic_function>)
      * [`ExtrinsicResponse.extrinsic_receipt`](<#bittensor.core.types.ExtrinsicResponse.extrinsic_receipt>)
      * [`ExtrinsicResponse.from_exception()`](<#bittensor.core.types.ExtrinsicResponse.from_exception>)
      * [`ExtrinsicResponse.message`](<#bittensor.core.types.ExtrinsicResponse.message>)
      * [`ExtrinsicResponse.mev_extrinsic`](<#bittensor.core.types.ExtrinsicResponse.mev_extrinsic>)
      * [`ExtrinsicResponse.success`](<#bittensor.core.types.ExtrinsicResponse.success>)
      * [`ExtrinsicResponse.transaction_alpha_fee`](<#bittensor.core.types.ExtrinsicResponse.transaction_alpha_fee>)
      * [`ExtrinsicResponse.transaction_tao_fee`](<#bittensor.core.types.ExtrinsicResponse.transaction_tao_fee>)
      * [`ExtrinsicResponse.unlock_wallet()`](<#bittensor.core.types.ExtrinsicResponse.unlock_wallet>)
      * [`ExtrinsicResponse.with_log()`](<#bittensor.core.types.ExtrinsicResponse.with_log>)
    * [`NeuronCertificateResponse`](<#bittensor.core.types.NeuronCertificateResponse>)
      * [`NeuronCertificateResponse.algorithm`](<#bittensor.core.types.NeuronCertificateResponse.algorithm>)
      * [`NeuronCertificateResponse.public_key`](<#bittensor.core.types.NeuronCertificateResponse.public_key>)
    * [`PositionResponse`](<#bittensor.core.types.PositionResponse>)
      * [`PositionResponse.fees_alpha`](<#bittensor.core.types.PositionResponse.fees_alpha>)
      * [`PositionResponse.fees_tao`](<#bittensor.core.types.PositionResponse.fees_tao>)
      * [`PositionResponse.id`](<#bittensor.core.types.PositionResponse.id>)
      * [`PositionResponse.liquidity`](<#bittensor.core.types.PositionResponse.liquidity>)
      * [`PositionResponse.netuid`](<#bittensor.core.types.PositionResponse.netuid>)
      * [`PositionResponse.tick_high`](<#bittensor.core.types.PositionResponse.tick_high>)
      * [`PositionResponse.tick_low`](<#bittensor.core.types.PositionResponse.tick_low>)
    * [`PrometheusServeCallParams`](<#bittensor.core.types.PrometheusServeCallParams>)
      * [`PrometheusServeCallParams.ip`](<#bittensor.core.types.PrometheusServeCallParams.ip>)
      * [`PrometheusServeCallParams.ip_type`](<#bittensor.core.types.PrometheusServeCallParams.ip_type>)
      * [`PrometheusServeCallParams.netuid`](<#bittensor.core.types.PrometheusServeCallParams.netuid>)
      * [`PrometheusServeCallParams.port`](<#bittensor.core.types.PrometheusServeCallParams.port>)
      * [`PrometheusServeCallParams.version`](<#bittensor.core.types.PrometheusServeCallParams.version>)
    * [`Salt`](<#bittensor.core.types.Salt>)
    * [`SubnetIdentityResponse`](<#bittensor.core.types.SubnetIdentityResponse>)
      * [`SubnetIdentityResponse.additional`](<#bittensor.core.types.SubnetIdentityResponse.additional>)
      * [`SubnetIdentityResponse.description`](<#bittensor.core.types.SubnetIdentityResponse.description>)
      * [`SubnetIdentityResponse.discord`](<#bittensor.core.types.SubnetIdentityResponse.discord>)
      * [`SubnetIdentityResponse.github_repo`](<#bittensor.core.types.SubnetIdentityResponse.github_repo>)
      * [`SubnetIdentityResponse.logo_url`](<#bittensor.core.types.SubnetIdentityResponse.logo_url>)
      * [`SubnetIdentityResponse.subnet_contact`](<#bittensor.core.types.SubnetIdentityResponse.subnet_contact>)
      * [`SubnetIdentityResponse.subnet_name`](<#bittensor.core.types.SubnetIdentityResponse.subnet_name>)
      * [`SubnetIdentityResponse.subnet_url`](<#bittensor.core.types.SubnetIdentityResponse.subnet_url>)
    * [`SubtensorMixin`](<#bittensor.core.types.SubtensorMixin>)
      * [`SubtensorMixin.add_args()`](<#bittensor.core.types.SubtensorMixin.add_args>)
      * [`SubtensorMixin.chain_endpoint`](<#bittensor.core.types.SubtensorMixin.chain_endpoint>)
      * [`SubtensorMixin.config()`](<#bittensor.core.types.SubtensorMixin.config>)
      * [`SubtensorMixin.help()`](<#bittensor.core.types.SubtensorMixin.help>)
      * [`SubtensorMixin.log_verbose`](<#bittensor.core.types.SubtensorMixin.log_verbose>)
      * [`SubtensorMixin.network`](<#bittensor.core.types.SubtensorMixin.network>)
      * [`SubtensorMixin.setup_config()`](<#bittensor.core.types.SubtensorMixin.setup_config>)
    * [`UIDs`](<#bittensor.core.types.UIDs>)
    * [`Weights`](<#bittensor.core.types.Weights>)



# bittensor.core.types[#](<#module-bittensor.core.types> "Link to this heading")

## Attributes[#](<#attributes> "Link to this heading")

[`Salt`](<#bittensor.core.types.Salt> "bittensor.core.types.Salt") |   
---|---  
[`UIDs`](<#bittensor.core.types.UIDs> "bittensor.core.types.UIDs") |   
[`Weights`](<#bittensor.core.types.Weights> "bittensor.core.types.Weights") |   
  
## Classes[#](<#classes> "Link to this heading")

[`AxonServeCallParams`](<#bittensor.core.types.AxonServeCallParams> "bittensor.core.types.AxonServeCallParams") |   
---|---  
[`BlockInfo`](<#bittensor.core.types.BlockInfo> "bittensor.core.types.BlockInfo") | Class that holds information about a blockchain block.  
[`CommitmentOfResponse`](<#bittensor.core.types.CommitmentOfResponse> "bittensor.core.types.CommitmentOfResponse") | dict() -> new empty dictionary  
[`CrowdloansResponse`](<#bittensor.core.types.CrowdloansResponse> "bittensor.core.types.CrowdloansResponse") | dict() -> new empty dictionary  
[`DynamicInfoResponse`](<#bittensor.core.types.DynamicInfoResponse> "bittensor.core.types.DynamicInfoResponse") | dict() -> new empty dictionary  
[`ExtrinsicResponse`](<#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse") | A standardized response container for handling the extrinsic results submissions and related operations in the SDK.  
[`NeuronCertificateResponse`](<#bittensor.core.types.NeuronCertificateResponse> "bittensor.core.types.NeuronCertificateResponse") | dict() -> new empty dictionary  
[`PositionResponse`](<#bittensor.core.types.PositionResponse> "bittensor.core.types.PositionResponse") | dict() -> new empty dictionary  
[`PrometheusServeCallParams`](<#bittensor.core.types.PrometheusServeCallParams> "bittensor.core.types.PrometheusServeCallParams") | Prometheus serve chain call parameters.  
[`SubnetIdentityResponse`](<#bittensor.core.types.SubnetIdentityResponse> "bittensor.core.types.SubnetIdentityResponse") | dict() -> new empty dictionary  
[`SubtensorMixin`](<#bittensor.core.types.SubtensorMixin> "bittensor.core.types.SubtensorMixin") | Helper class that provides a standard way to create an ABC using  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.types.AxonServeCallParams(_version_ , _ip_ , _port_ , _ip_type_ , _netuid_ , _hotkey_ , _coldkey_ , _protocol_ , _placeholder1_ , _placeholder2_ , _certificate_)[#](<#bittensor.core.types.AxonServeCallParams> "Link to this definition")
    

Parameters:
    

  * **version** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **ip** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **port** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **ip_type** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **netuid** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **hotkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

  * **coldkey** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"))

  * **protocol** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **placeholder1** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **placeholder2** ([_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"))

  * **certificate** (_Optional_ _[_[_bittensor.utils.Certificate_](<../../utils/index.html#bittensor.utils.Certificate> "bittensor.utils.Certificate") _]_)




as_dict()[#](<#bittensor.core.types.AxonServeCallParams.as_dict> "Link to this definition")
    

Returns a dict representation of this object. If self.certificate is None, it is not included in this.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

certificate[#](<#bittensor.core.types.AxonServeCallParams.certificate> "Link to this definition")
    

coldkey[#](<#bittensor.core.types.AxonServeCallParams.coldkey> "Link to this definition")
    

copy()[#](<#bittensor.core.types.AxonServeCallParams.copy> "Link to this definition")
    

Return type:
    

[AxonServeCallParams](<#bittensor.core.types.AxonServeCallParams> "bittensor.core.types.AxonServeCallParams")

hotkey[#](<#bittensor.core.types.AxonServeCallParams.hotkey> "Link to this definition")
    

ip[#](<#bittensor.core.types.AxonServeCallParams.ip> "Link to this definition")
    

ip_type[#](<#bittensor.core.types.AxonServeCallParams.ip_type> "Link to this definition")
    

netuid[#](<#bittensor.core.types.AxonServeCallParams.netuid> "Link to this definition")
    

placeholder1[#](<#bittensor.core.types.AxonServeCallParams.placeholder1> "Link to this definition")
    

placeholder2[#](<#bittensor.core.types.AxonServeCallParams.placeholder2> "Link to this definition")
    

port[#](<#bittensor.core.types.AxonServeCallParams.port> "Link to this definition")
    

protocol[#](<#bittensor.core.types.AxonServeCallParams.protocol> "Link to this definition")
    

version[#](<#bittensor.core.types.AxonServeCallParams.version> "Link to this definition")
    

class bittensor.core.types.BlockInfo[#](<#bittensor.core.types.BlockInfo> "Link to this definition")
    

Class that holds information about a blockchain block.

This class encapsulates all relevant information about a block in the blockchain, including its number, hash, timestamp, and contents.

Variables:
    

  * **number** – The block number.

  * **hash** – The corresponding block hash.

  * **timestamp** – The timestamp of the block (based on the Timestamp.Now extrinsic).

  * **header** – The raw block header returned by the node RPC.

  * **extrinsics** – The list of extrinsics included in the block.

  * **explorer** – The link to block explorer service.




explorer: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.BlockInfo.explorer> "Link to this definition")
    

extrinsics: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[#](<#bittensor.core.types.BlockInfo.extrinsics> "Link to this definition")
    

hash: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.BlockInfo.hash> "Link to this definition")
    

header: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[#](<#bittensor.core.types.BlockInfo.header> "Link to this definition")
    

number: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.BlockInfo.number> "Link to this definition")
    

timestamp: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.types.BlockInfo.timestamp> "Link to this definition")
    

class bittensor.core.types.CommitmentOfResponse[#](<#bittensor.core.types.CommitmentOfResponse> "Link to this definition")
    

Bases: `TypedDict`

dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object’s

> (key, value) pairs

dict(iterable) -> new dictionary initialized as if via:
    

d = {} for k, v in iterable:

> d[k] = v

dict([**](<#id1>)kwargs) -> new dictionary initialized with the name=value pairs
    

in the keyword argument list. For example: dict(one=1, two=2)

Initialize self. See help(type(self)) for accurate signature.

block: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.CommitmentOfResponse.block> "Link to this definition")
    

deposit: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.CommitmentOfResponse.deposit> "Link to this definition")
    

info: _CommitmentFields[#](<#bittensor.core.types.CommitmentOfResponse.info> "Link to this definition")
    

class bittensor.core.types.CrowdloansResponse[#](<#bittensor.core.types.CrowdloansResponse> "Link to this definition")
    

Bases: `TypedDict`

dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object’s

> (key, value) pairs

dict(iterable) -> new dictionary initialized as if via:
    

d = {} for k, v in iterable:

> d[k] = v

dict([**](<#id3>)kwargs) -> new dictionary initialized with the name=value pairs
    

in the keyword argument list. For example: dict(one=1, two=2)

Initialize self. See help(type(self)) for accurate signature.

call: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.types.CrowdloansResponse.call> "Link to this definition")
    

cap: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.CrowdloansResponse.cap> "Link to this definition")
    

contributors_count: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.CrowdloansResponse.contributors_count> "Link to this definition")
    

creator: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.CrowdloansResponse.creator> "Link to this definition")
    

deposit: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.CrowdloansResponse.deposit> "Link to this definition")
    

end: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.CrowdloansResponse.end> "Link to this definition")
    

finalized: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.types.CrowdloansResponse.finalized> "Link to this definition")
    

funds_account: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.CrowdloansResponse.funds_account> "Link to this definition")
    

min_contribution: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.CrowdloansResponse.min_contribution> "Link to this definition")
    

raised: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.CrowdloansResponse.raised> "Link to this definition")
    

target_address: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.CrowdloansResponse.target_address> "Link to this definition")
    

class bittensor.core.types.DynamicInfoResponse[#](<#bittensor.core.types.DynamicInfoResponse> "Link to this definition")
    

Bases: `TypedDict`

dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object’s

> (key, value) pairs

dict(iterable) -> new dictionary initialized as if via:
    

d = {} for k, v in iterable:

> d[k] = v

dict([**](<#id5>)kwargs) -> new dictionary initialized with the name=value pairs
    

in the keyword argument list. For example: dict(one=1, two=2)

Initialize self. See help(type(self)) for accurate signature.

alpha_in: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.alpha_in> "Link to this definition")
    

alpha_in_emission: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.alpha_in_emission> "Link to this definition")
    

alpha_out: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.alpha_out> "Link to this definition")
    

alpha_out_emission: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.alpha_out_emission> "Link to this definition")
    

blocks_since_last_step: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.blocks_since_last_step> "Link to this definition")
    

emission: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.emission> "Link to this definition")
    

last_step: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.last_step> "Link to this definition")
    

moving_price: scalecodec.utils.math.FixedPoint[#](<#bittensor.core.types.DynamicInfoResponse.moving_price> "Link to this definition")
    

netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.netuid> "Link to this definition")
    

network_registered_at: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.network_registered_at> "Link to this definition")
    

owner_coldkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.owner_coldkey> "Link to this definition")
    

owner_hotkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.owner_hotkey> "Link to this definition")
    

pending_alpha_emission: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.pending_alpha_emission> "Link to this definition")
    

pending_root_emission: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.pending_root_emission> "Link to this definition")
    

price: NotRequired[[bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")][#](<#bittensor.core.types.DynamicInfoResponse.price> "Link to this definition")
    

subnet_identity: [SubnetIdentityResponse](<#bittensor.core.types.SubnetIdentityResponse> "bittensor.core.types.SubnetIdentityResponse")[#](<#bittensor.core.types.DynamicInfoResponse.subnet_identity> "Link to this definition")
    

subnet_name: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")][#](<#bittensor.core.types.DynamicInfoResponse.subnet_name> "Link to this definition")
    

subnet_volume: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.subnet_volume> "Link to this definition")
    

tao_in: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.tao_in> "Link to this definition")
    

tao_in_emission: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.tao_in_emission> "Link to this definition")
    

tempo: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.DynamicInfoResponse.tempo> "Link to this definition")
    

token_symbol: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")][#](<#bittensor.core.types.DynamicInfoResponse.token_symbol> "Link to this definition")
    

class bittensor.core.types.ExtrinsicResponse[#](<#bittensor.core.types.ExtrinsicResponse> "Link to this definition")
    

A standardized response container for handling the extrinsic results submissions and related operations in the SDK.

This class is designed to give developers a consistent way to represent the outcome of an extrinsic call — whether it succeeded or failed — along with useful metadata for debugging, logging, or higher-level business logic.

The object also implements tuple-like behavior:
    

  * Iteration yields `(success, message)`.

  * Indexing is supported: `response[0] -> success`, `response[1] -> message`.

  * `len(response)` returns 2.




Variables:
    

  * **success** – Indicates if the extrinsic execution was successful.

  * **message** – A status or informational message returned from the execution (e.g., “Successfully registered subnet”).

  * **extrinsic_function** – The SDK extrinsic or external function name that was executed (e.g., “add_stake_extrinsic”).

  * **extrinsic** – The raw extrinsic object used in the call, if available. This is a `GenericExtrinsic` instance containing the full payload and metadata of the submitted extrinsic, including call section, method, signer, signature, parameters, and encoded bytes. Useful for inspecting or reconstructing the exact transaction submitted to the chain.

  * **extrinsic_fee** – The fee charged by the extrinsic, if available.

  * **extrinsic_receipt** – The receipt object of the submitted extrinsic. This is an `ExtrinsicReceipt` instance that contains the most detailed execution data available, including the block number and hash, triggered events, extrinsic index, execution phase, and other low-level details. This allows deep debugging or post-analysis of on-chain execution.

  * **mev_extrinsic** – The extrinsic object of the revealed (decrypted and executed) MEV Shield extrinsic. This is populated when using MEV Shield protection (`with_mev_protection=True`) and contains the execution details of the second extrinsic that decrypts and executes the originally encrypted call. Contains triggered events, block information, and other execution metadata. Set to `None` for non-MEV Shield transactions or when the revealed extrinsic receipt is not available.

  * **transaction_tao_fee** – TAO fee charged by the transaction in TAO (e.g., fee for add_stake), if available.

  * **transaction_alpha_fee** – Alpha fee charged by the transaction (e.g., fee for transfer_stake), if available.

  * **error** – Captures the underlying exception if the extrinsic failed, otherwise None.

  * **data** – Arbitrary data returned from the extrinsic, such as decoded events, balance or another extra context.




Instance methods:
    

as_dict: Returns a dictionary representation of this object. with_log: Returns itself but with logging message.

Class methods:
    

from_exception: Checks if error is raised or return ExtrinsicResponse accordingly. unlock_wallet: Checks if keypair is unlocked and can be used for signing the extrinsic.

Example

import bittensor as bt

subtensor = bt.SubtensorApi(“local”) wallet = bt.Wallet(“alice”)

response = subtensor.subnets.register_subnet(alice_wallet) print(response)

ExtrinsicResponse:
    

success: True message: Successfully registered subnet extrinsic_function: register_subnet_extrinsic extrinsic: {‘account_id’: ‘0xd43593c715fdd31c… transaction_fee: τ1.0 extrinsic_receipt: Extrinsic Receipt data of of the submitted extrinsic mev_extrinsic: None transaction_tao_fee: τ1.0 transaction_alpha_fee: 1.0β error: None data: None

success, message = response print(success, message)

True Successfully registered subnet

print(response[0]) True print(response[1]) ‘Successfully registered subnet’

as_dict()[#](<#bittensor.core.types.ExtrinsicResponse.as_dict> "Link to this definition")
    

Represents this object as a dictionary.

Return type:
    

[dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")

data: [Any](<../chain_data/proxy/index.html#bittensor.core.chain_data.proxy.ProxyType.Any> "bittensor.core.chain_data.proxy.ProxyType.Any") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)") = None[#](<#bittensor.core.types.ExtrinsicResponse.data> "Link to this definition")
    

error: [Exception](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)") = None[#](<#bittensor.core.types.ExtrinsicResponse.error> "Link to this definition")
    

extrinsic: scalecodec.types.GenericExtrinsic | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)") = None[#](<#bittensor.core.types.ExtrinsicResponse.extrinsic> "Link to this definition")
    

extrinsic_fee: [bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)") = None[#](<#bittensor.core.types.ExtrinsicResponse.extrinsic_fee> "Link to this definition")
    

extrinsic_function: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)") = None[#](<#bittensor.core.types.ExtrinsicResponse.extrinsic_function> "Link to this definition")
    

extrinsic_receipt: AsyncExtrinsicReceipt | ExtrinsicReceipt | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)") = None[#](<#bittensor.core.types.ExtrinsicResponse.extrinsic_receipt> "Link to this definition")
    

classmethod from_exception(_raise_error_ , _error_)[#](<#bittensor.core.types.ExtrinsicResponse.from_exception> "Link to this definition")
    

Check if error is raised and return ExtrinsicResponse accordingly. :param raise_error: Raises a relevant exception rather than returning False if unsuccessful. :param error: Exception raised during extrinsic execution.

Returns:
    

Extrinsic Response with False checks whether to raise an error or simply return the instance.

Parameters:
    

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)"))

  * **error** ([_Exception_](<https://docs.python.org/3/library/exceptions.html#Exception> "\(in Python v3.14\)"))



Return type:
    

[ExtrinsicResponse](<#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

message: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)") = None[#](<#bittensor.core.types.ExtrinsicResponse.message> "Link to this definition")
    

mev_extrinsic: AsyncExtrinsicReceipt | ExtrinsicReceipt | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)") = None[#](<#bittensor.core.types.ExtrinsicResponse.mev_extrinsic> "Link to this definition")
    

success: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)") = True[#](<#bittensor.core.types.ExtrinsicResponse.success> "Link to this definition")
    

transaction_alpha_fee: [bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)") = None[#](<#bittensor.core.types.ExtrinsicResponse.transaction_alpha_fee> "Link to this definition")
    

transaction_tao_fee: [bittensor.utils.balance.Balance](<../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)") = None[#](<#bittensor.core.types.ExtrinsicResponse.transaction_tao_fee> "Link to this definition")
    

classmethod unlock_wallet(_wallet_ , _raise_error =False_, _unlock_type ='coldkey'_, _nonce_key =None_)[#](<#bittensor.core.types.ExtrinsicResponse.unlock_wallet> "Link to this definition")
    

Check if keypair is unlocked and return ExtrinsicResponse accordingly.

Parameters:
    

  * **wallet** (_bittensor_wallet.Wallet_) – Bittensor Wallet instance.

  * **raise_error** ([_bool_](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")) – Raises a relevant exception rather than returning False if unsuccessful.

  * **unlock_type** ([_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")) – The key type, ‘coldkey’ or ‘hotkey’. Or ‘both’ to check both.

  * **nonce_key** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – Key used for generating nonce in extrinsic function.



Returns:
    

Extrinsic Response is used to check if the key is unlocked.

Return type:
    

[ExtrinsicResponse](<#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

Note

When an extrinsic is signed with the coldkey but internally references or uses the hotkey, both keypairs must be validated. Passing unlock_type=’both’ ensures that authentication is performed against both the coldkey and hotkey.

with_log(_level ='error'_)[#](<#bittensor.core.types.ExtrinsicResponse.with_log> "Link to this definition")
    

Logs provided message with provided level.

Parameters:
    

**level** (_Literal_ _[__'trace'__,__'debug'__,__'info'__,__'warning'__,__'error'__,__'success'__]_) – Logging level represented as “trace”, “debug”, “info”, “warning”, “error”, “success” uses to logging message.

Returns:
    

ExtrinsicResponse instance.

Return type:
    

[ExtrinsicResponse](<#bittensor.core.types.ExtrinsicResponse> "bittensor.core.types.ExtrinsicResponse")

class bittensor.core.types.NeuronCertificateResponse[#](<#bittensor.core.types.NeuronCertificateResponse> "Link to this definition")
    

Bases: `TypedDict`

dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object’s

> (key, value) pairs

dict(iterable) -> new dictionary initialized as if via:
    

d = {} for k, v in iterable:

> d[k] = v

dict([**](<#id7>)kwargs) -> new dictionary initialized with the name=value pairs
    

in the keyword argument list. For example: dict(one=1, two=2)

Initialize self. See help(type(self)) for accurate signature.

algorithm: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.NeuronCertificateResponse.algorithm> "Link to this definition")
    

public_key: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.NeuronCertificateResponse.public_key> "Link to this definition")
    

class bittensor.core.types.PositionResponse[#](<#bittensor.core.types.PositionResponse> "Link to this definition")
    

Bases: `TypedDict`

dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object’s

> (key, value) pairs

dict(iterable) -> new dictionary initialized as if via:
    

d = {} for k, v in iterable:

> d[k] = v

dict([**](<#id9>)kwargs) -> new dictionary initialized with the name=value pairs
    

in the keyword argument list. For example: dict(one=1, two=2)

Initialize self. See help(type(self)) for accurate signature.

fees_alpha: scalecodec.utils.math.FixedPoint[#](<#bittensor.core.types.PositionResponse.fees_alpha> "Link to this definition")
    

fees_tao: scalecodec.utils.math.FixedPoint[#](<#bittensor.core.types.PositionResponse.fees_tao> "Link to this definition")
    

id: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.PositionResponse.id> "Link to this definition")
    

liquidity: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.PositionResponse.liquidity> "Link to this definition")
    

netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.PositionResponse.netuid> "Link to this definition")
    

tick_high: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.PositionResponse.tick_high> "Link to this definition")
    

tick_low: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.PositionResponse.tick_low> "Link to this definition")
    

class bittensor.core.types.PrometheusServeCallParams[#](<#bittensor.core.types.PrometheusServeCallParams> "Link to this definition")
    

Bases: `TypedDict`

Prometheus serve chain call parameters.

Initialize self. See help(type(self)) for accurate signature.

ip: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.PrometheusServeCallParams.ip> "Link to this definition")
    

ip_type: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.PrometheusServeCallParams.ip_type> "Link to this definition")
    

netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.PrometheusServeCallParams.netuid> "Link to this definition")
    

port: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.PrometheusServeCallParams.port> "Link to this definition")
    

version: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.types.PrometheusServeCallParams.version> "Link to this definition")
    

bittensor.core.types.Salt[#](<#bittensor.core.types.Salt> "Link to this definition")
    

class bittensor.core.types.SubnetIdentityResponse[#](<#bittensor.core.types.SubnetIdentityResponse> "Link to this definition")
    

Bases: `TypedDict`

dict() -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object’s

> (key, value) pairs

dict(iterable) -> new dictionary initialized as if via:
    

d = {} for k, v in iterable:

> d[k] = v

dict([**](<#id11>)kwargs) -> new dictionary initialized with the name=value pairs
    

in the keyword argument list. For example: dict(one=1, two=2)

Initialize self. See help(type(self)) for accurate signature.

additional: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.SubnetIdentityResponse.additional> "Link to this definition")
    

description: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.SubnetIdentityResponse.description> "Link to this definition")
    

discord: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.SubnetIdentityResponse.discord> "Link to this definition")
    

github_repo: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.SubnetIdentityResponse.github_repo> "Link to this definition")
    

logo_url: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.SubnetIdentityResponse.logo_url> "Link to this definition")
    

subnet_contact: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.SubnetIdentityResponse.subnet_contact> "Link to this definition")
    

subnet_name: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.SubnetIdentityResponse.subnet_name> "Link to this definition")
    

subnet_url: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.SubnetIdentityResponse.subnet_url> "Link to this definition")
    

class bittensor.core.types.SubtensorMixin[#](<#bittensor.core.types.SubtensorMixin> "Link to this definition")
    

Bases: [`abc.ABC`](<https://docs.python.org/3/library/abc.html#abc.ABC> "\(in Python v3.14\)")

Helper class that provides a standard way to create an ABC using inheritance.

classmethod add_args(_parser_ , _prefix =None_)[#](<#bittensor.core.types.SubtensorMixin.add_args> "Link to this definition")
    

Adds command-line arguments to the provided ArgumentParser for configuring the Subtensor settings.

Parameters:
    

  * **parser** ([_argparse.ArgumentParser_](<https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser> "\(in Python v3.14\)")) – The ArgumentParser object to which the Subtensor arguments will be added.

  * **prefix** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – An optional prefix for the argument names. If provided, the prefix is prepended to each argument name.




Arguments added:
    

–subtensor.network: The Subtensor network flag. Possible values are ‘finney’, ‘test’, ‘archive’, and
    

‘local’. Overrides the chain endpoint if set.

–subtensor.chain_endpoint: The Subtensor chain endpoint flag. If set, it overrides the network flag. –subtensor._mock: If true, uses a mocked connection to the chain.

Example

parser = argparse.ArgumentParser() Subtensor.add_args(parser)

chain_endpoint: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.SubtensorMixin.chain_endpoint> "Link to this definition")
    

static config()[#](<#bittensor.core.types.SubtensorMixin.config> "Link to this definition")
    

Creates and returns a Bittensor configuration object.

Returns:
    

A Bittensor configuration object configured with arguments added by the subtensor.add_args method.

Return type:
    

[bittensor.core.config.Config](<../config/index.html#bittensor.core.config.Config> "bittensor.core.config.Config")

classmethod help()[#](<#bittensor.core.types.SubtensorMixin.help> "Link to this definition")
    

Print help to stdout.

log_verbose: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.types.SubtensorMixin.log_verbose> "Link to this definition")
    

network: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.types.SubtensorMixin.network> "Link to this definition")
    

static setup_config(_network_ , _config_)[#](<#bittensor.core.types.SubtensorMixin.setup_config> "Link to this definition")
    

Sets up and returns the configuration for the Subtensor network and endpoint.

This method determines the appropriate network and chain endpoint based on the provided network string or
    

configuration object. It evaluates the network and endpoint in the following order of precedence: 1\. Provided network string. 2\. Configured chain endpoint in the config object. 3\. Configured network in the config object. 4\. Default chain endpoint. 5\. Default network.

Parameters:
    

  * **network** (_Optional_ _[_[_str_](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)") _]_) – The name of the Subtensor network. If None, the network and endpoint will be determined from the config object.

  * **config** ([_bittensor.core.config.Config_](<../config/index.html#bittensor.core.config.Config> "bittensor.core.config.Config")) – The configuration object containing the network and chain endpoint settings.



Returns:
    

A tuple containing the formatted WebSocket endpoint URL and the evaluated network name.

Return type:
    

[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

bittensor.core.types.UIDs[#](<#bittensor.core.types.UIDs> "Link to this definition")
    

bittensor.core.types.Weights[#](<#bittensor.core.types.Weights> "Link to this definition")
    

[ __ previous bittensor.core.threadpool ](<../threadpool/index.html> "previous page") [ next bittensor.extras __](<../../extras/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`AxonServeCallParams`](<#bittensor.core.types.AxonServeCallParams>)
      * [`AxonServeCallParams.as_dict()`](<#bittensor.core.types.AxonServeCallParams.as_dict>)
      * [`AxonServeCallParams.certificate`](<#bittensor.core.types.AxonServeCallParams.certificate>)
      * [`AxonServeCallParams.coldkey`](<#bittensor.core.types.AxonServeCallParams.coldkey>)
      * [`AxonServeCallParams.copy()`](<#bittensor.core.types.AxonServeCallParams.copy>)
      * [`AxonServeCallParams.hotkey`](<#bittensor.core.types.AxonServeCallParams.hotkey>)
      * [`AxonServeCallParams.ip`](<#bittensor.core.types.AxonServeCallParams.ip>)
      * [`AxonServeCallParams.ip_type`](<#bittensor.core.types.AxonServeCallParams.ip_type>)
      * [`AxonServeCallParams.netuid`](<#bittensor.core.types.AxonServeCallParams.netuid>)
      * [`AxonServeCallParams.placeholder1`](<#bittensor.core.types.AxonServeCallParams.placeholder1>)
      * [`AxonServeCallParams.placeholder2`](<#bittensor.core.types.AxonServeCallParams.placeholder2>)
      * [`AxonServeCallParams.port`](<#bittensor.core.types.AxonServeCallParams.port>)
      * [`AxonServeCallParams.protocol`](<#bittensor.core.types.AxonServeCallParams.protocol>)
      * [`AxonServeCallParams.version`](<#bittensor.core.types.AxonServeCallParams.version>)
    * [`BlockInfo`](<#bittensor.core.types.BlockInfo>)
      * [`BlockInfo.explorer`](<#bittensor.core.types.BlockInfo.explorer>)
      * [`BlockInfo.extrinsics`](<#bittensor.core.types.BlockInfo.extrinsics>)
      * [`BlockInfo.hash`](<#bittensor.core.types.BlockInfo.hash>)
      * [`BlockInfo.header`](<#bittensor.core.types.BlockInfo.header>)
      * [`BlockInfo.number`](<#bittensor.core.types.BlockInfo.number>)
      * [`BlockInfo.timestamp`](<#bittensor.core.types.BlockInfo.timestamp>)
    * [`CommitmentOfResponse`](<#bittensor.core.types.CommitmentOfResponse>)
      * [`CommitmentOfResponse.block`](<#bittensor.core.types.CommitmentOfResponse.block>)
      * [`CommitmentOfResponse.deposit`](<#bittensor.core.types.CommitmentOfResponse.deposit>)
      * [`CommitmentOfResponse.info`](<#bittensor.core.types.CommitmentOfResponse.info>)
    * [`CrowdloansResponse`](<#bittensor.core.types.CrowdloansResponse>)
      * [`CrowdloansResponse.call`](<#bittensor.core.types.CrowdloansResponse.call>)
      * [`CrowdloansResponse.cap`](<#bittensor.core.types.CrowdloansResponse.cap>)
      * [`CrowdloansResponse.contributors_count`](<#bittensor.core.types.CrowdloansResponse.contributors_count>)
      * [`CrowdloansResponse.creator`](<#bittensor.core.types.CrowdloansResponse.creator>)
      * [`CrowdloansResponse.deposit`](<#bittensor.core.types.CrowdloansResponse.deposit>)
      * [`CrowdloansResponse.end`](<#bittensor.core.types.CrowdloansResponse.end>)
      * [`CrowdloansResponse.finalized`](<#bittensor.core.types.CrowdloansResponse.finalized>)
      * [`CrowdloansResponse.funds_account`](<#bittensor.core.types.CrowdloansResponse.funds_account>)
      * [`CrowdloansResponse.min_contribution`](<#bittensor.core.types.CrowdloansResponse.min_contribution>)
      * [`CrowdloansResponse.raised`](<#bittensor.core.types.CrowdloansResponse.raised>)
      * [`CrowdloansResponse.target_address`](<#bittensor.core.types.CrowdloansResponse.target_address>)
    * [`DynamicInfoResponse`](<#bittensor.core.types.DynamicInfoResponse>)
      * [`DynamicInfoResponse.alpha_in`](<#bittensor.core.types.DynamicInfoResponse.alpha_in>)
      * [`DynamicInfoResponse.alpha_in_emission`](<#bittensor.core.types.DynamicInfoResponse.alpha_in_emission>)
      * [`DynamicInfoResponse.alpha_out`](<#bittensor.core.types.DynamicInfoResponse.alpha_out>)
      * [`DynamicInfoResponse.alpha_out_emission`](<#bittensor.core.types.DynamicInfoResponse.alpha_out_emission>)
      * [`DynamicInfoResponse.blocks_since_last_step`](<#bittensor.core.types.DynamicInfoResponse.blocks_since_last_step>)
      * [`DynamicInfoResponse.emission`](<#bittensor.core.types.DynamicInfoResponse.emission>)
      * [`DynamicInfoResponse.last_step`](<#bittensor.core.types.DynamicInfoResponse.last_step>)
      * [`DynamicInfoResponse.moving_price`](<#bittensor.core.types.DynamicInfoResponse.moving_price>)
      * [`DynamicInfoResponse.netuid`](<#bittensor.core.types.DynamicInfoResponse.netuid>)
      * [`DynamicInfoResponse.network_registered_at`](<#bittensor.core.types.DynamicInfoResponse.network_registered_at>)
      * [`DynamicInfoResponse.owner_coldkey`](<#bittensor.core.types.DynamicInfoResponse.owner_coldkey>)
      * [`DynamicInfoResponse.owner_hotkey`](<#bittensor.core.types.DynamicInfoResponse.owner_hotkey>)
      * [`DynamicInfoResponse.pending_alpha_emission`](<#bittensor.core.types.DynamicInfoResponse.pending_alpha_emission>)
      * [`DynamicInfoResponse.pending_root_emission`](<#bittensor.core.types.DynamicInfoResponse.pending_root_emission>)
      * [`DynamicInfoResponse.price`](<#bittensor.core.types.DynamicInfoResponse.price>)
      * [`DynamicInfoResponse.subnet_identity`](<#bittensor.core.types.DynamicInfoResponse.subnet_identity>)
      * [`DynamicInfoResponse.subnet_name`](<#bittensor.core.types.DynamicInfoResponse.subnet_name>)
      * [`DynamicInfoResponse.subnet_volume`](<#bittensor.core.types.DynamicInfoResponse.subnet_volume>)
      * [`DynamicInfoResponse.tao_in`](<#bittensor.core.types.DynamicInfoResponse.tao_in>)
      * [`DynamicInfoResponse.tao_in_emission`](<#bittensor.core.types.DynamicInfoResponse.tao_in_emission>)
      * [`DynamicInfoResponse.tempo`](<#bittensor.core.types.DynamicInfoResponse.tempo>)
      * [`DynamicInfoResponse.token_symbol`](<#bittensor.core.types.DynamicInfoResponse.token_symbol>)
    * [`ExtrinsicResponse`](<#bittensor.core.types.ExtrinsicResponse>)
      * [`ExtrinsicResponse.as_dict()`](<#bittensor.core.types.ExtrinsicResponse.as_dict>)
      * [`ExtrinsicResponse.data`](<#bittensor.core.types.ExtrinsicResponse.data>)
      * [`ExtrinsicResponse.error`](<#bittensor.core.types.ExtrinsicResponse.error>)
      * [`ExtrinsicResponse.extrinsic`](<#bittensor.core.types.ExtrinsicResponse.extrinsic>)
      * [`ExtrinsicResponse.extrinsic_fee`](<#bittensor.core.types.ExtrinsicResponse.extrinsic_fee>)
      * [`ExtrinsicResponse.extrinsic_function`](<#bittensor.core.types.ExtrinsicResponse.extrinsic_function>)
      * [`ExtrinsicResponse.extrinsic_receipt`](<#bittensor.core.types.ExtrinsicResponse.extrinsic_receipt>)
      * [`ExtrinsicResponse.from_exception()`](<#bittensor.core.types.ExtrinsicResponse.from_exception>)
      * [`ExtrinsicResponse.message`](<#bittensor.core.types.ExtrinsicResponse.message>)
      * [`ExtrinsicResponse.mev_extrinsic`](<#bittensor.core.types.ExtrinsicResponse.mev_extrinsic>)
      * [`ExtrinsicResponse.success`](<#bittensor.core.types.ExtrinsicResponse.success>)
      * [`ExtrinsicResponse.transaction_alpha_fee`](<#bittensor.core.types.ExtrinsicResponse.transaction_alpha_fee>)
      * [`ExtrinsicResponse.transaction_tao_fee`](<#bittensor.core.types.ExtrinsicResponse.transaction_tao_fee>)
      * [`ExtrinsicResponse.unlock_wallet()`](<#bittensor.core.types.ExtrinsicResponse.unlock_wallet>)
      * [`ExtrinsicResponse.with_log()`](<#bittensor.core.types.ExtrinsicResponse.with_log>)
    * [`NeuronCertificateResponse`](<#bittensor.core.types.NeuronCertificateResponse>)
      * [`NeuronCertificateResponse.algorithm`](<#bittensor.core.types.NeuronCertificateResponse.algorithm>)
      * [`NeuronCertificateResponse.public_key`](<#bittensor.core.types.NeuronCertificateResponse.public_key>)
    * [`PositionResponse`](<#bittensor.core.types.PositionResponse>)
      * [`PositionResponse.fees_alpha`](<#bittensor.core.types.PositionResponse.fees_alpha>)
      * [`PositionResponse.fees_tao`](<#bittensor.core.types.PositionResponse.fees_tao>)
      * [`PositionResponse.id`](<#bittensor.core.types.PositionResponse.id>)
      * [`PositionResponse.liquidity`](<#bittensor.core.types.PositionResponse.liquidity>)
      * [`PositionResponse.netuid`](<#bittensor.core.types.PositionResponse.netuid>)
      * [`PositionResponse.tick_high`](<#bittensor.core.types.PositionResponse.tick_high>)
      * [`PositionResponse.tick_low`](<#bittensor.core.types.PositionResponse.tick_low>)
    * [`PrometheusServeCallParams`](<#bittensor.core.types.PrometheusServeCallParams>)
      * [`PrometheusServeCallParams.ip`](<#bittensor.core.types.PrometheusServeCallParams.ip>)
      * [`PrometheusServeCallParams.ip_type`](<#bittensor.core.types.PrometheusServeCallParams.ip_type>)
      * [`PrometheusServeCallParams.netuid`](<#bittensor.core.types.PrometheusServeCallParams.netuid>)
      * [`PrometheusServeCallParams.port`](<#bittensor.core.types.PrometheusServeCallParams.port>)
      * [`PrometheusServeCallParams.version`](<#bittensor.core.types.PrometheusServeCallParams.version>)
    * [`Salt`](<#bittensor.core.types.Salt>)
    * [`SubnetIdentityResponse`](<#bittensor.core.types.SubnetIdentityResponse>)
      * [`SubnetIdentityResponse.additional`](<#bittensor.core.types.SubnetIdentityResponse.additional>)
      * [`SubnetIdentityResponse.description`](<#bittensor.core.types.SubnetIdentityResponse.description>)
      * [`SubnetIdentityResponse.discord`](<#bittensor.core.types.SubnetIdentityResponse.discord>)
      * [`SubnetIdentityResponse.github_repo`](<#bittensor.core.types.SubnetIdentityResponse.github_repo>)
      * [`SubnetIdentityResponse.logo_url`](<#bittensor.core.types.SubnetIdentityResponse.logo_url>)
      * [`SubnetIdentityResponse.subnet_contact`](<#bittensor.core.types.SubnetIdentityResponse.subnet_contact>)
      * [`SubnetIdentityResponse.subnet_name`](<#bittensor.core.types.SubnetIdentityResponse.subnet_name>)
      * [`SubnetIdentityResponse.subnet_url`](<#bittensor.core.types.SubnetIdentityResponse.subnet_url>)
    * [`SubtensorMixin`](<#bittensor.core.types.SubtensorMixin>)
      * [`SubtensorMixin.add_args()`](<#bittensor.core.types.SubtensorMixin.add_args>)
      * [`SubtensorMixin.chain_endpoint`](<#bittensor.core.types.SubtensorMixin.chain_endpoint>)
      * [`SubtensorMixin.config()`](<#bittensor.core.types.SubtensorMixin.config>)
      * [`SubtensorMixin.help()`](<#bittensor.core.types.SubtensorMixin.help>)
      * [`SubtensorMixin.log_verbose`](<#bittensor.core.types.SubtensorMixin.log_verbose>)
      * [`SubtensorMixin.network`](<#bittensor.core.types.SubtensorMixin.network>)
      * [`SubtensorMixin.setup_config()`](<#bittensor.core.types.SubtensorMixin.setup_config>)
    * [`UIDs`](<#bittensor.core.types.UIDs>)
    * [`Weights`](<#bittensor.core.types.Weights>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.