# bittensor.core.chain_data.neuron_info &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.core.chain_data](<../index.html>)
        * [bittensor.core.config](<../../config/index.html>)
        * [bittensor.core.dendrite](<../../dendrite/index.html>)
        * [bittensor.core.errors](<../../errors/index.html>)
        * [bittensor.core.extrinsics](<../../extrinsics/index.html>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/neuron_info/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/neuron_info/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/neuron_info/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.neuron_info

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`NeuronInfo`](<#bittensor.core.chain_data.neuron_info.NeuronInfo>)
      * [`NeuronInfo.active`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.active>)
      * [`NeuronInfo.axon_info`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.axon_info>)
      * [`NeuronInfo.bonds`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.bonds>)
      * [`NeuronInfo.coldkey`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.coldkey>)
      * [`NeuronInfo.consensus`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.consensus>)
      * [`NeuronInfo.dividends`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.dividends>)
      * [`NeuronInfo.emission`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.emission>)
      * [`NeuronInfo.from_weights_bonds_and_neuron_lite()`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.from_weights_bonds_and_neuron_lite>)
      * [`NeuronInfo.get_null_neuron()`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.get_null_neuron>)
      * [`NeuronInfo.hotkey`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.hotkey>)
      * [`NeuronInfo.incentive`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.incentive>)
      * [`NeuronInfo.is_null`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.is_null>)
      * [`NeuronInfo.last_update`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.last_update>)
      * [`NeuronInfo.netuid`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.netuid>)
      * [`NeuronInfo.prometheus_info`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.prometheus_info>)
      * [`NeuronInfo.stake`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.stake>)
      * [`NeuronInfo.stake_dict`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.stake_dict>)
      * [`NeuronInfo.total_stake`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.total_stake>)
      * [`NeuronInfo.uid`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.uid>)
      * [`NeuronInfo.validator_permit`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.validator_permit>)
      * [`NeuronInfo.validator_trust`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.validator_trust>)
      * [`NeuronInfo.weights`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.weights>)



# bittensor.core.chain_data.neuron_info[#](<#module-bittensor.core.chain_data.neuron_info> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`NeuronInfo`](<#bittensor.core.chain_data.neuron_info.NeuronInfo> "bittensor.core.chain_data.neuron_info.NeuronInfo") | Represents the metadata of a neuron including keys, UID, stake, rankings, and other attributes.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.neuron_info.NeuronInfo[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo> "Link to this definition")
    

Bases: [`bittensor.core.chain_data.info_base.InfoBase`](<../info_base/index.html#bittensor.core.chain_data.info_base.InfoBase> "bittensor.core.chain_data.info_base.InfoBase")

Represents the metadata of a neuron including keys, UID, stake, rankings, and other attributes.

Variables:
    

  * **hotkey** – The hotkey associated with the neuron.

  * **coldkey** – The coldkey associated with the neuron.

  * **uid** – The unique identifier for the neuron.

  * **netuid** – The network unique identifier for the neuron.

  * **active** – The active status of the neuron.

  * **stake** – The balance staked to this neuron.

  * **stake_dict** – A dictionary mapping coldkey to the amount staked.

  * **total_stake** – The total amount of stake.

  * **emission** – The emission rate.

  * **incentive** – The incentive value.

  * **consensus** – The consensus score.

  * **validator_trust** – The validation trust score.

  * **dividends** – The dividends value.

  * **last_update** – The timestamp of the last update.

  * **validator_permit** – Validator permit status.

  * **weights** – List of weights associated with the neuron.

  * **bonds** – List of bonds associated with the neuron.

  * **prometheus_info** – Information related to Prometheus.

  * **axon_info** – Information related to Axon.

  * **is_null** – Indicator if this is a null neuron.




active: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.active> "Link to this definition")
    

axon_info: [bittensor.core.chain_data.axon_info.AxonInfo](<../axon_info/index.html#bittensor.core.chain_data.axon_info.AxonInfo> "bittensor.core.chain_data.axon_info.AxonInfo") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)") = None[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.axon_info> "Link to this definition")
    

bonds: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]][#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.bonds> "Link to this definition")
    

coldkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.coldkey> "Link to this definition")
    

consensus: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.consensus> "Link to this definition")
    

dividends: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.dividends> "Link to this definition")
    

emission: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.emission> "Link to this definition")
    

classmethod from_weights_bonds_and_neuron_lite(_neuron_lite_ , _weights_as_dict_ , _bonds_as_dict_)[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.from_weights_bonds_and_neuron_lite> "Link to this definition")
    

Creates an instance of NeuronInfo from NeuronInfoLite and dictionaries of weights and bonds.

Parameters:
    

  * **neuron_lite** ([_bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite_](<../neuron_info_lite/index.html#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite> "bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite")) – A lite version of the neuron containing basic attributes.

  * **weights_as_dict** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _,_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _,_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]__]__]_) – A dictionary where the key is the UID and the value is a list of weight tuples associated with the neuron.

  * **bonds_as_dict** ([_dict_](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _,_[_list_](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)") _[_[_tuple_](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)") _[_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _,_[_int_](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)") _]__]__]_) – A dictionary where the key is the UID and the value is a list of bond tuples associated with the neuron.



Returns:
    

An instance of NeuronInfo populated with the provided weights and bonds.

Return type:
    

[NeuronInfo](<#bittensor.core.chain_data.neuron_info.NeuronInfo> "bittensor.core.chain_data.neuron_info.NeuronInfo")

static get_null_neuron()[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.get_null_neuron> "Link to this definition")
    

Returns a null NeuronInfo instance.

Return type:
    

[NeuronInfo](<#bittensor.core.chain_data.neuron_info.NeuronInfo> "bittensor.core.chain_data.neuron_info.NeuronInfo")

hotkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.hotkey> "Link to this definition")
    

incentive: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.incentive> "Link to this definition")
    

is_null: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)") = False[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.is_null> "Link to this definition")
    

last_update: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.last_update> "Link to this definition")
    

netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.netuid> "Link to this definition")
    

prometheus_info: [bittensor.core.chain_data.prometheus_info.PrometheusInfo](<../prometheus_info/index.html#bittensor.core.chain_data.prometheus_info.PrometheusInfo> "bittensor.core.chain_data.prometheus_info.PrometheusInfo") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)") = None[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.prometheus_info> "Link to this definition")
    

stake: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.stake> "Link to this definition")
    

stake_dict: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")][#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.stake_dict> "Link to this definition")
    

total_stake: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.total_stake> "Link to this definition")
    

uid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.uid> "Link to this definition")
    

validator_permit: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.validator_permit> "Link to this definition")
    

validator_trust: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.validator_trust> "Link to this definition")
    

weights: [list](<https://docs.python.org/3/library/stdtypes.html#list> "\(in Python v3.14\)")[[tuple](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")[[int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)"), [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")]][#](<#bittensor.core.chain_data.neuron_info.NeuronInfo.weights> "Link to this definition")
    

[ __ previous bittensor.core.chain_data.metagraph_info ](<../metagraph_info/index.html> "previous page") [ next bittensor.core.chain_data.neuron_info_lite __](<../neuron_info_lite/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`NeuronInfo`](<#bittensor.core.chain_data.neuron_info.NeuronInfo>)
      * [`NeuronInfo.active`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.active>)
      * [`NeuronInfo.axon_info`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.axon_info>)
      * [`NeuronInfo.bonds`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.bonds>)
      * [`NeuronInfo.coldkey`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.coldkey>)
      * [`NeuronInfo.consensus`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.consensus>)
      * [`NeuronInfo.dividends`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.dividends>)
      * [`NeuronInfo.emission`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.emission>)
      * [`NeuronInfo.from_weights_bonds_and_neuron_lite()`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.from_weights_bonds_and_neuron_lite>)
      * [`NeuronInfo.get_null_neuron()`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.get_null_neuron>)
      * [`NeuronInfo.hotkey`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.hotkey>)
      * [`NeuronInfo.incentive`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.incentive>)
      * [`NeuronInfo.is_null`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.is_null>)
      * [`NeuronInfo.last_update`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.last_update>)
      * [`NeuronInfo.netuid`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.netuid>)
      * [`NeuronInfo.prometheus_info`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.prometheus_info>)
      * [`NeuronInfo.stake`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.stake>)
      * [`NeuronInfo.stake_dict`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.stake_dict>)
      * [`NeuronInfo.total_stake`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.total_stake>)
      * [`NeuronInfo.uid`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.uid>)
      * [`NeuronInfo.validator_permit`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.validator_permit>)
      * [`NeuronInfo.validator_trust`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.validator_trust>)
      * [`NeuronInfo.weights`](<#bittensor.core.chain_data.neuron_info.NeuronInfo.weights>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.