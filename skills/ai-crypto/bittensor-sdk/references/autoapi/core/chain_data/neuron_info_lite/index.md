# bittensor.core.chain_data.neuron_info_lite &#8212; Bittensor SDK Docs  documentation

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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/chain_data/neuron_info_lite/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/chain_data/neuron_info_lite/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../_sources/autoapi/bittensor/core/chain_data/neuron_info_lite/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.chain_data.neuron_info_lite

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`NeuronInfoLite`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite>)
      * [`NeuronInfoLite.get_null_neuron()`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.get_null_neuron>)
      * [`NeuronInfoLite.list_from_vec_u8()`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.list_from_vec_u8>)
      * [`NeuronInfoLite.active`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.active>)
      * [`NeuronInfoLite.axon_info`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.axon_info>)
      * [`NeuronInfoLite.coldkey`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.coldkey>)
      * [`NeuronInfoLite.consensus`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.consensus>)
      * [`NeuronInfoLite.dividends`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.dividends>)
      * [`NeuronInfoLite.emission`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.emission>)
      * [`NeuronInfoLite.get_null_neuron()`](<#id0>)
      * [`NeuronInfoLite.hotkey`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.hotkey>)
      * [`NeuronInfoLite.incentive`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.incentive>)
      * [`NeuronInfoLite.is_null`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.is_null>)
      * [`NeuronInfoLite.last_update`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.last_update>)
      * [`NeuronInfoLite.netuid`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.netuid>)
      * [`NeuronInfoLite.prometheus_info`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.prometheus_info>)
      * [`NeuronInfoLite.stake`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.stake>)
      * [`NeuronInfoLite.stake_dict`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.stake_dict>)
      * [`NeuronInfoLite.total_stake`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.total_stake>)
      * [`NeuronInfoLite.uid`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.uid>)
      * [`NeuronInfoLite.validator_permit`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.validator_permit>)
      * [`NeuronInfoLite.validator_trust`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.validator_trust>)



# bittensor.core.chain_data.neuron_info_lite[#](<#module-bittensor.core.chain_data.neuron_info_lite> "Link to this heading")

## Classes[#](<#classes> "Link to this heading")

[`NeuronInfoLite`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite> "bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite") | NeuronInfoLite is a dataclass representing neuron metadata without weights and bonds.  
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite> "Link to this definition")
    

Bases: [`bittensor.core.chain_data.info_base.InfoBase`](<../info_base/index.html#bittensor.core.chain_data.info_base.InfoBase> "bittensor.core.chain_data.info_base.InfoBase")

NeuronInfoLite is a dataclass representing neuron metadata without weights and bonds.

Variables:
    

  * **hotkey** – The hotkey string for the neuron.

  * **coldkey** – The coldkey string for the neuron.

  * **uid** – A unique identifier for the neuron.

  * **netuid** – Network unique identifier for the neuron.

  * **active** – Indicates whether the neuron is active.

  * **stake** – The stake amount associated with the neuron.

  * **stake_dict** – Mapping of coldkey to the amount staked to this Neuron.

  * **total_stake** – Total amount of the stake.

  * **emission** – The emission value of the neuron.

  * **incentive** – The incentive value of the neuron.

  * **consensus** – The consensus value of the neuron.

  * **validator_trust** – Validator trust value of the neuron.

  * **dividends** – Dividends associated with the neuron.

  * **last_update** – Timestamp of the last update.

  * **validator_permit** – Indicates if the neuron has a validator permit.

  * **prometheus_info** – Prometheus information associated with the neuron.

  * **axon_info** – Axon information associated with the neuron.

  * **is_null** – Indicates whether the neuron is null.




get_null_neuron()[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.get_null_neuron> "Link to this definition")
    

Returns a NeuronInfoLite object representing a null neuron.

Return type:
    

[NeuronInfoLite](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite> "bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite")

list_from_vec_u8()[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.list_from_vec_u8> "Link to this definition")
    

Decodes a bytes object into a list of NeuronInfoLite instances.

active: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.active> "Link to this definition")
    

axon_info: [bittensor.core.chain_data.axon_info.AxonInfo](<../axon_info/index.html#bittensor.core.chain_data.axon_info.AxonInfo> "bittensor.core.chain_data.axon_info.AxonInfo") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.axon_info> "Link to this definition")
    

coldkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.coldkey> "Link to this definition")
    

consensus: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.consensus> "Link to this definition")
    

dividends: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.dividends> "Link to this definition")
    

emission: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.emission> "Link to this definition")
    

static get_null_neuron()[#](<#id0> "Link to this definition")
    

Returns a null NeuronInfoLite instance.

Return type:
    

[NeuronInfoLite](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite> "bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite")

hotkey: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.hotkey> "Link to this definition")
    

incentive: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.incentive> "Link to this definition")
    

is_null: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)") = False[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.is_null> "Link to this definition")
    

last_update: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.last_update> "Link to this definition")
    

netuid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.netuid> "Link to this definition")
    

prometheus_info: [bittensor.core.chain_data.prometheus_info.PrometheusInfo](<../prometheus_info/index.html#bittensor.core.chain_data.prometheus_info.PrometheusInfo> "bittensor.core.chain_data.prometheus_info.PrometheusInfo") | [None](<https://docs.python.org/3/library/constants.html#None> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.prometheus_info> "Link to this definition")
    

stake: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.stake> "Link to this definition")
    

stake_dict: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")][#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.stake_dict> "Link to this definition")
    

total_stake: [bittensor.utils.balance.Balance](<../../../utils/balance/index.html#bittensor.utils.balance.Balance> "bittensor.utils.balance.Balance")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.total_stake> "Link to this definition")
    

uid: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.uid> "Link to this definition")
    

validator_permit: [bool](<https://docs.python.org/3/library/functions.html#bool> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.validator_permit> "Link to this definition")
    

validator_trust: [float](<https://docs.python.org/3/library/functions.html#float> "\(in Python v3.14\)")[#](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.validator_trust> "Link to this definition")
    

[ __ previous bittensor.core.chain_data.neuron_info ](<../neuron_info/index.html> "previous page") [ next bittensor.core.chain_data.prometheus_info __](<../prometheus_info/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`NeuronInfoLite`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite>)
      * [`NeuronInfoLite.get_null_neuron()`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.get_null_neuron>)
      * [`NeuronInfoLite.list_from_vec_u8()`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.list_from_vec_u8>)
      * [`NeuronInfoLite.active`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.active>)
      * [`NeuronInfoLite.axon_info`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.axon_info>)
      * [`NeuronInfoLite.coldkey`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.coldkey>)
      * [`NeuronInfoLite.consensus`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.consensus>)
      * [`NeuronInfoLite.dividends`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.dividends>)
      * [`NeuronInfoLite.emission`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.emission>)
      * [`NeuronInfoLite.get_null_neuron()`](<#id0>)
      * [`NeuronInfoLite.hotkey`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.hotkey>)
      * [`NeuronInfoLite.incentive`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.incentive>)
      * [`NeuronInfoLite.is_null`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.is_null>)
      * [`NeuronInfoLite.last_update`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.last_update>)
      * [`NeuronInfoLite.netuid`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.netuid>)
      * [`NeuronInfoLite.prometheus_info`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.prometheus_info>)
      * [`NeuronInfoLite.stake`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.stake>)
      * [`NeuronInfoLite.stake_dict`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.stake_dict>)
      * [`NeuronInfoLite.total_stake`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.total_stake>)
      * [`NeuronInfoLite.uid`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.uid>)
      * [`NeuronInfoLite.validator_permit`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.validator_permit>)
      * [`NeuronInfoLite.validator_trust`](<#bittensor.core.chain_data.neuron_info_lite.NeuronInfoLite.validator_trust>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.