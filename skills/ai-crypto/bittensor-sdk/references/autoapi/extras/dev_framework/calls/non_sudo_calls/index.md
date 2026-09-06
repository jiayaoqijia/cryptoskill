# bittensor.extras.dev_framework.calls.non_sudo_calls &#8212; Bittensor SDK Docs  documentation

[Skip to main content](<#main-content>)

__Back to top __ `Ctrl`+`K`

[ ![Bittensor SDK Docs  documentation - Home](../../../../../../_static/logo.svg) ![Bittensor SDK Docs  documentation - Home](../../../../../../_static/logo-dark-mode.svg) ](<../../../../../../index.html>)

__ Search `Ctrl`+`K`

Table of Contents

  * [API Reference](<../../../../../index.html>) __
    * [bittensor](<../../../../index.html>) __
      * [bittensor.core](<../../../../core/index.html>) __
        * [bittensor.core.async_subtensor](<../../../../core/async_subtensor/index.html>)
        * [bittensor.core.axon](<../../../../core/axon/index.html>)
        * [bittensor.core.chain_data](<../../../../core/chain_data/index.html>)
        * [bittensor.core.config](<../../../../core/config/index.html>)
        * [bittensor.core.dendrite](<../../../../core/dendrite/index.html>)
        * [bittensor.core.errors](<../../../../core/errors/index.html>)
        * [bittensor.core.extrinsics](<../../../../core/extrinsics/index.html>)
        * [bittensor.core.metagraph](<../../../../core/metagraph/index.html>)
        * [bittensor.core.settings](<../../../../core/settings/index.html>)
        * [bittensor.core.stream](<../../../../core/stream/index.html>)
        * [bittensor.core.subtensor](<../../../../core/subtensor/index.html>)
        * [bittensor.core.synapse](<../../../../core/synapse/index.html>)
        * [bittensor.core.tensor](<../../../../core/tensor/index.html>)
        * [bittensor.core.threadpool](<../../../../core/threadpool/index.html>)
        * [bittensor.core.types](<../../../../core/types/index.html>)
      * [bittensor.extras](<../../../index.html>) __
        * [bittensor.extras.dev_framework](<../../index.html>)
        * [bittensor.extras.subtensor_api](<../../../subtensor_api/index.html>)
        * [bittensor.extras.timelock](<../../../timelock/index.html>)
      * [bittensor.utils](<../../../../utils/index.html>) __
        * [bittensor.utils.axon_utils](<../../../../utils/axon_utils/index.html>)
        * [bittensor.utils.balance](<../../../../utils/balance/index.html>)
        * [bittensor.utils.btlogging](<../../../../utils/btlogging/index.html>)
        * [bittensor.utils.easy_imports](<../../../../utils/easy_imports/index.html>)
        * [bittensor.utils.formatting](<../../../../utils/formatting/index.html>)
        * [bittensor.utils.liquidity](<../../../../utils/liquidity/index.html>)
        * [bittensor.utils.networking](<../../../../utils/networking/index.html>)
        * [bittensor.utils.registration](<../../../../utils/registration/index.html>)
        * [bittensor.utils.subnets](<../../../../utils/subnets/index.html>)
        * [bittensor.utils.version](<../../../../utils/version/index.html>)
        * [bittensor.utils.weight_utils](<../../../../utils/weight_utils/index.html>)



__

  * [ __ Repository ](<https://github.com/opentensor/btcli> "Source repository")
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/extras/dev_framework/calls/non_sudo_calls/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/extras/dev_framework/calls/non_sudo_calls/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../../../_sources/autoapi/bittensor/extras/dev_framework/calls/non_sudo_calls/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.extras.dev_framework.calls.non_sudo_calls

##  Contents 

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`ADD_LIQUIDITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY>)
      * [`ADD_LIQUIDITY.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.hotkey>)
      * [`ADD_LIQUIDITY.liquidity`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.liquidity>)
      * [`ADD_LIQUIDITY.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.netuid>)
      * [`ADD_LIQUIDITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.pallet>)
      * [`ADD_LIQUIDITY.tick_high`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.tick_high>)
      * [`ADD_LIQUIDITY.tick_low`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.tick_low>)
      * [`ADD_LIQUIDITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.wallet>)
    * [`ADD_PROXY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY>)
      * [`ADD_PROXY.delay`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY.delay>)
      * [`ADD_PROXY.delegate`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY.delegate>)
      * [`ADD_PROXY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY.pallet>)
      * [`ADD_PROXY.proxy_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY.proxy_type>)
      * [`ADD_PROXY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY.wallet>)
    * [`ADD_STAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE>)
      * [`ADD_STAKE.amount_staked`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE.amount_staked>)
      * [`ADD_STAKE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE.hotkey>)
      * [`ADD_STAKE.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE.netuid>)
      * [`ADD_STAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE.pallet>)
      * [`ADD_STAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE.wallet>)
    * [`ADD_STAKE_BURN`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN>)
      * [`ADD_STAKE_BURN.amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.amount>)
      * [`ADD_STAKE_BURN.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.hotkey>)
      * [`ADD_STAKE_BURN.limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.limit>)
      * [`ADD_STAKE_BURN.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.netuid>)
      * [`ADD_STAKE_BURN.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.pallet>)
      * [`ADD_STAKE_BURN.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.wallet>)
    * [`ADD_STAKE_LIMIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT>)
      * [`ADD_STAKE_LIMIT.allow_partial`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.allow_partial>)
      * [`ADD_STAKE_LIMIT.amount_staked`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.amount_staked>)
      * [`ADD_STAKE_LIMIT.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.hotkey>)
      * [`ADD_STAKE_LIMIT.limit_price`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.limit_price>)
      * [`ADD_STAKE_LIMIT.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.netuid>)
      * [`ADD_STAKE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.pallet>)
      * [`ADD_STAKE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.wallet>)
    * [`ANNOUNCE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE>)
      * [`ANNOUNCE.call_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE.call_hash>)
      * [`ANNOUNCE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE.pallet>)
      * [`ANNOUNCE.real`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE.real>)
      * [`ANNOUNCE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE.wallet>)
    * [`ANNOUNCE_COLDKEY_SWAP`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_COLDKEY_SWAP>)
      * [`ANNOUNCE_COLDKEY_SWAP.new_coldkey_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_COLDKEY_SWAP.new_coldkey_hash>)
      * [`ANNOUNCE_COLDKEY_SWAP.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_COLDKEY_SWAP.pallet>)
      * [`ANNOUNCE_COLDKEY_SWAP.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_COLDKEY_SWAP.wallet>)
    * [`ANNOUNCE_NEXT_KEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_NEXT_KEY>)
      * [`ANNOUNCE_NEXT_KEY.enc_key`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_NEXT_KEY.enc_key>)
      * [`ANNOUNCE_NEXT_KEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_NEXT_KEY.pallet>)
      * [`ANNOUNCE_NEXT_KEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_NEXT_KEY.wallet>)
    * [`APPLY_AUTHORIZED_UPGRADE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPLY_AUTHORIZED_UPGRADE>)
      * [`APPLY_AUTHORIZED_UPGRADE.code`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPLY_AUTHORIZED_UPGRADE.code>)
      * [`APPLY_AUTHORIZED_UPGRADE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPLY_AUTHORIZED_UPGRADE.pallet>)
      * [`APPLY_AUTHORIZED_UPGRADE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPLY_AUTHORIZED_UPGRADE.wallet>)
    * [`APPROVE_AS_MULTI`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI>)
      * [`APPROVE_AS_MULTI.call_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.call_hash>)
      * [`APPROVE_AS_MULTI.max_weight`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.max_weight>)
      * [`APPROVE_AS_MULTI.maybe_timepoint`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.maybe_timepoint>)
      * [`APPROVE_AS_MULTI.other_signatories`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.other_signatories>)
      * [`APPROVE_AS_MULTI.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.pallet>)
      * [`APPROVE_AS_MULTI.threshold`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.threshold>)
      * [`APPROVE_AS_MULTI.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.wallet>)
    * [`ASSOCIATE_EVM_KEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY>)
      * [`ASSOCIATE_EVM_KEY.block_number`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.block_number>)
      * [`ASSOCIATE_EVM_KEY.evm_key`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.evm_key>)
      * [`ASSOCIATE_EVM_KEY.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.netuid>)
      * [`ASSOCIATE_EVM_KEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.pallet>)
      * [`ASSOCIATE_EVM_KEY.signature`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.signature>)
      * [`ASSOCIATE_EVM_KEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.wallet>)
    * [`AS_DERIVATIVE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE>)
      * [`AS_DERIVATIVE.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE.call>)
      * [`AS_DERIVATIVE.index`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE.index>)
      * [`AS_DERIVATIVE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE.pallet>)
      * [`AS_DERIVATIVE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE.wallet>)
    * [`AS_MULTI`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI>)
      * [`AS_MULTI.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.call>)
      * [`AS_MULTI.max_weight`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.max_weight>)
      * [`AS_MULTI.maybe_timepoint`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.maybe_timepoint>)
      * [`AS_MULTI.other_signatories`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.other_signatories>)
      * [`AS_MULTI.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.pallet>)
      * [`AS_MULTI.threshold`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.threshold>)
      * [`AS_MULTI.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.wallet>)
    * [`AS_MULTI_THRESHOLD_1`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1>)
      * [`AS_MULTI_THRESHOLD_1.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1.call>)
      * [`AS_MULTI_THRESHOLD_1.other_signatories`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1.other_signatories>)
      * [`AS_MULTI_THRESHOLD_1.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1.pallet>)
      * [`AS_MULTI_THRESHOLD_1.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1.wallet>)
    * [`AUTHORIZE_UPGRADE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE>)
      * [`AUTHORIZE_UPGRADE.code_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE.code_hash>)
      * [`AUTHORIZE_UPGRADE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE.pallet>)
      * [`AUTHORIZE_UPGRADE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE.wallet>)
    * [`AUTHORIZE_UPGRADE_WITHOUT_CHECKS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE_WITHOUT_CHECKS>)
      * [`AUTHORIZE_UPGRADE_WITHOUT_CHECKS.code_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE_WITHOUT_CHECKS.code_hash>)
      * [`AUTHORIZE_UPGRADE_WITHOUT_CHECKS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE_WITHOUT_CHECKS.pallet>)
      * [`AUTHORIZE_UPGRADE_WITHOUT_CHECKS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE_WITHOUT_CHECKS.wallet>)
    * [`BATCH`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH>)
      * [`BATCH.calls`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH.calls>)
      * [`BATCH.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH.pallet>)
      * [`BATCH.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH.wallet>)
    * [`BATCH_ALL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_ALL>)
      * [`BATCH_ALL.calls`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_ALL.calls>)
      * [`BATCH_ALL.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_ALL.pallet>)
      * [`BATCH_ALL.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_ALL.wallet>)
    * [`BATCH_COMMIT_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS>)
      * [`BATCH_COMMIT_WEIGHTS.commit_hashes`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS.commit_hashes>)
      * [`BATCH_COMMIT_WEIGHTS.netuids`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS.netuids>)
      * [`BATCH_COMMIT_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS.pallet>)
      * [`BATCH_COMMIT_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS.wallet>)
    * [`BATCH_REVEAL_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS>)
      * [`BATCH_REVEAL_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.netuid>)
      * [`BATCH_REVEAL_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.pallet>)
      * [`BATCH_REVEAL_WEIGHTS.salts_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.salts_list>)
      * [`BATCH_REVEAL_WEIGHTS.uids_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.uids_list>)
      * [`BATCH_REVEAL_WEIGHTS.values_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.values_list>)
      * [`BATCH_REVEAL_WEIGHTS.version_keys`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.version_keys>)
      * [`BATCH_REVEAL_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.wallet>)
    * [`BATCH_SET_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS>)
      * [`BATCH_SET_WEIGHTS.netuids`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS.netuids>)
      * [`BATCH_SET_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS.pallet>)
      * [`BATCH_SET_WEIGHTS.version_keys`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS.version_keys>)
      * [`BATCH_SET_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS.wallet>)
      * [`BATCH_SET_WEIGHTS.weights`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS.weights>)
    * [`BURN`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN>)
      * [`BURN.keep_alive`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN.keep_alive>)
      * [`BURN.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN.pallet>)
      * [`BURN.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN.value>)
      * [`BURN.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN.wallet>)
    * [`BURNED_REGISTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER>)
      * [`BURNED_REGISTER.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER.hotkey>)
      * [`BURNED_REGISTER.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER.netuid>)
      * [`BURNED_REGISTER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER.pallet>)
      * [`BURNED_REGISTER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER.wallet>)
    * [`BURN_ALPHA`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA>)
      * [`BURN_ALPHA.amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA.amount>)
      * [`BURN_ALPHA.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA.hotkey>)
      * [`BURN_ALPHA.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA.netuid>)
      * [`BURN_ALPHA.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA.pallet>)
      * [`BURN_ALPHA.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA.wallet>)
    * [`CALL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL>)
      * [`CALL.data`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.data>)
      * [`CALL.dest`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.dest>)
      * [`CALL.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.gas_limit>)
      * [`CALL.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.pallet>)
      * [`CALL.storage_deposit_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.storage_deposit_limit>)
      * [`CALL.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.value>)
      * [`CALL.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.wallet>)
    * [`CALL`](<#id0>)
      * [`CALL.access_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.access_list>)
      * [`CALL.authorization_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.authorization_list>)
      * [`CALL.gas_limit`](<#id1>)
      * [`CALL.input`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.input>)
      * [`CALL.max_fee_per_gas`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.max_fee_per_gas>)
      * [`CALL.max_priority_fee_per_gas`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.max_priority_fee_per_gas>)
      * [`CALL.nonce`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.nonce>)
      * [`CALL.pallet`](<#id2>)
      * [`CALL.source`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.source>)
      * [`CALL.target`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.target>)
      * [`CALL.value`](<#id3>)
      * [`CALL.wallet`](<#id4>)
    * [`CALL_OLD_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT>)
      * [`CALL_OLD_WEIGHT.data`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.data>)
      * [`CALL_OLD_WEIGHT.dest`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.dest>)
      * [`CALL_OLD_WEIGHT.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.gas_limit>)
      * [`CALL_OLD_WEIGHT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.pallet>)
      * [`CALL_OLD_WEIGHT.storage_deposit_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.storage_deposit_limit>)
      * [`CALL_OLD_WEIGHT.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.value>)
      * [`CALL_OLD_WEIGHT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.wallet>)
    * [`CANCEL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL>)
      * [`CANCEL.index`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL.index>)
      * [`CANCEL.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL.pallet>)
      * [`CANCEL.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL.wallet>)
      * [`CANCEL.when`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL.when>)
    * [`CANCEL_AS_MULTI`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI>)
      * [`CANCEL_AS_MULTI.call_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.call_hash>)
      * [`CANCEL_AS_MULTI.other_signatories`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.other_signatories>)
      * [`CANCEL_AS_MULTI.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.pallet>)
      * [`CANCEL_AS_MULTI.threshold`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.threshold>)
      * [`CANCEL_AS_MULTI.timepoint`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.timepoint>)
      * [`CANCEL_AS_MULTI.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.wallet>)
    * [`CANCEL_NAMED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_NAMED>)
      * [`CANCEL_NAMED.id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_NAMED.id>)
      * [`CANCEL_NAMED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_NAMED.pallet>)
      * [`CANCEL_NAMED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_NAMED.wallet>)
    * [`CANCEL_RETRY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY>)
      * [`CANCEL_RETRY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY.pallet>)
      * [`CANCEL_RETRY.task`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY.task>)
      * [`CANCEL_RETRY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY.wallet>)
    * [`CANCEL_RETRY_NAMED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY_NAMED>)
      * [`CANCEL_RETRY_NAMED.id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY_NAMED.id>)
      * [`CANCEL_RETRY_NAMED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY_NAMED.pallet>)
      * [`CANCEL_RETRY_NAMED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY_NAMED.wallet>)
    * [`CLAIM_ROOT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLAIM_ROOT>)
      * [`CLAIM_ROOT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLAIM_ROOT.pallet>)
      * [`CLAIM_ROOT.subnets`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLAIM_ROOT.subnets>)
      * [`CLAIM_ROOT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLAIM_ROOT.wallet>)
    * [`CLEAR_COLDKEY_SWAP_ANNOUNCEMENT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_COLDKEY_SWAP_ANNOUNCEMENT>)
      * [`CLEAR_COLDKEY_SWAP_ANNOUNCEMENT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_COLDKEY_SWAP_ANNOUNCEMENT.pallet>)
      * [`CLEAR_COLDKEY_SWAP_ANNOUNCEMENT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_COLDKEY_SWAP_ANNOUNCEMENT.wallet>)
    * [`CLEAR_IDENTITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_IDENTITY>)
      * [`CLEAR_IDENTITY.identified`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_IDENTITY.identified>)
      * [`CLEAR_IDENTITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_IDENTITY.pallet>)
      * [`CLEAR_IDENTITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_IDENTITY.wallet>)
    * [`COMMIT_CRV3_MECHANISM_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS>)
      * [`COMMIT_CRV3_MECHANISM_WEIGHTS.commit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.commit>)
      * [`COMMIT_CRV3_MECHANISM_WEIGHTS.mecid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.mecid>)
      * [`COMMIT_CRV3_MECHANISM_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.netuid>)
      * [`COMMIT_CRV3_MECHANISM_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.pallet>)
      * [`COMMIT_CRV3_MECHANISM_WEIGHTS.reveal_round`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.reveal_round>)
      * [`COMMIT_CRV3_MECHANISM_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.wallet>)
    * [`COMMIT_MECHANISM_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS>)
      * [`COMMIT_MECHANISM_WEIGHTS.commit_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS.commit_hash>)
      * [`COMMIT_MECHANISM_WEIGHTS.mecid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS.mecid>)
      * [`COMMIT_MECHANISM_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS.netuid>)
      * [`COMMIT_MECHANISM_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS.pallet>)
      * [`COMMIT_MECHANISM_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS.wallet>)
    * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS>)
      * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.commit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.commit>)
      * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.commit_reveal_version`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.commit_reveal_version>)
      * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.mecid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.mecid>)
      * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.netuid>)
      * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.pallet>)
      * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.reveal_round`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.reveal_round>)
      * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.wallet>)
    * [`COMMIT_TIMELOCKED_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS>)
      * [`COMMIT_TIMELOCKED_WEIGHTS.commit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.commit>)
      * [`COMMIT_TIMELOCKED_WEIGHTS.commit_reveal_version`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.commit_reveal_version>)
      * [`COMMIT_TIMELOCKED_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.netuid>)
      * [`COMMIT_TIMELOCKED_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.pallet>)
      * [`COMMIT_TIMELOCKED_WEIGHTS.reveal_round`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.reveal_round>)
      * [`COMMIT_TIMELOCKED_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.wallet>)
    * [`COMMIT_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS>)
      * [`COMMIT_WEIGHTS.commit_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS.commit_hash>)
      * [`COMMIT_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS.netuid>)
      * [`COMMIT_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS.pallet>)
      * [`COMMIT_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS.wallet>)
    * [`CONTRIBUTE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE>)
      * [`CONTRIBUTE.amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE.amount>)
      * [`CONTRIBUTE.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE.crowdloan_id>)
      * [`CONTRIBUTE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE.pallet>)
      * [`CONTRIBUTE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE.wallet>)
    * [`CREATE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE>)
      * [`CREATE.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.call>)
      * [`CREATE.cap`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.cap>)
      * [`CREATE.deposit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.deposit>)
      * [`CREATE.end`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.end>)
      * [`CREATE.min_contribution`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.min_contribution>)
      * [`CREATE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.pallet>)
      * [`CREATE.target_address`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.target_address>)
      * [`CREATE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.wallet>)
    * [`CREATE`](<#id5>)
      * [`CREATE.access_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.access_list>)
      * [`CREATE.authorization_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.authorization_list>)
      * [`CREATE.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.gas_limit>)
      * [`CREATE.init`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.init>)
      * [`CREATE.max_fee_per_gas`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.max_fee_per_gas>)
      * [`CREATE.max_priority_fee_per_gas`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.max_priority_fee_per_gas>)
      * [`CREATE.nonce`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.nonce>)
      * [`CREATE.pallet`](<#id6>)
      * [`CREATE.source`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.source>)
      * [`CREATE.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.value>)
      * [`CREATE.wallet`](<#id7>)
    * [`CREATE2`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2>)
      * [`CREATE2.access_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.access_list>)
      * [`CREATE2.authorization_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.authorization_list>)
      * [`CREATE2.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.gas_limit>)
      * [`CREATE2.init`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.init>)
      * [`CREATE2.max_fee_per_gas`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.max_fee_per_gas>)
      * [`CREATE2.max_priority_fee_per_gas`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.max_priority_fee_per_gas>)
      * [`CREATE2.nonce`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.nonce>)
      * [`CREATE2.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.pallet>)
      * [`CREATE2.salt`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.salt>)
      * [`CREATE2.source`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.source>)
      * [`CREATE2.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.value>)
      * [`CREATE2.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.wallet>)
    * [`CREATE_PURE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE>)
      * [`CREATE_PURE.delay`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE.delay>)
      * [`CREATE_PURE.index`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE.index>)
      * [`CREATE_PURE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE.pallet>)
      * [`CREATE_PURE.proxy_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE.proxy_type>)
      * [`CREATE_PURE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE.wallet>)
    * [`DECREASE_TAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE>)
      * [`DECREASE_TAKE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE.hotkey>)
      * [`DECREASE_TAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE.pallet>)
      * [`DECREASE_TAKE.take`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE.take>)
      * [`DECREASE_TAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE.wallet>)
    * [`DISABLE_LP`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_LP>)
      * [`DISABLE_LP.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_LP.pallet>)
      * [`DISABLE_LP.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_LP.wallet>)
    * [`DISABLE_VOTING_POWER_TRACKING`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_VOTING_POWER_TRACKING>)
      * [`DISABLE_VOTING_POWER_TRACKING.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_VOTING_POWER_TRACKING.netuid>)
      * [`DISABLE_VOTING_POWER_TRACKING.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_VOTING_POWER_TRACKING.pallet>)
      * [`DISABLE_VOTING_POWER_TRACKING.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_VOTING_POWER_TRACKING.wallet>)
    * [`DISABLE_WHITELIST`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_WHITELIST>)
      * [`DISABLE_WHITELIST.disabled`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_WHITELIST.disabled>)
      * [`DISABLE_WHITELIST.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_WHITELIST.pallet>)
      * [`DISABLE_WHITELIST.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_WHITELIST.wallet>)
    * [`DISPATCH_AS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS>)
      * [`DISPATCH_AS.as_origin`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS.as_origin>)
      * [`DISPATCH_AS.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS.call>)
      * [`DISPATCH_AS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS.pallet>)
      * [`DISPATCH_AS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS.wallet>)
    * [`DISPATCH_AS_FALLIBLE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE>)
      * [`DISPATCH_AS_FALLIBLE.as_origin`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE.as_origin>)
      * [`DISPATCH_AS_FALLIBLE.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE.call>)
      * [`DISPATCH_AS_FALLIBLE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE.pallet>)
      * [`DISPATCH_AS_FALLIBLE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE.wallet>)
    * [`DISPUTE_COLDKEY_SWAP`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPUTE_COLDKEY_SWAP>)
      * [`DISPUTE_COLDKEY_SWAP.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPUTE_COLDKEY_SWAP.pallet>)
      * [`DISPUTE_COLDKEY_SWAP.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPUTE_COLDKEY_SWAP.wallet>)
    * [`DISSOLVE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE>)
      * [`DISSOLVE.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE.crowdloan_id>)
      * [`DISSOLVE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE.pallet>)
      * [`DISSOLVE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE.wallet>)
    * [`DISSOLVE_NETWORK`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK>)
      * [`DISSOLVE_NETWORK.coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK.coldkey>)
      * [`DISSOLVE_NETWORK.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK.netuid>)
      * [`DISSOLVE_NETWORK.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK.pallet>)
      * [`DISSOLVE_NETWORK.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK.wallet>)
    * [`ENABLE_VOTING_POWER_TRACKING`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENABLE_VOTING_POWER_TRACKING>)
      * [`ENABLE_VOTING_POWER_TRACKING.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENABLE_VOTING_POWER_TRACKING.netuid>)
      * [`ENABLE_VOTING_POWER_TRACKING.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENABLE_VOTING_POWER_TRACKING.pallet>)
      * [`ENABLE_VOTING_POWER_TRACKING.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENABLE_VOTING_POWER_TRACKING.wallet>)
    * [`ENSURE_UPDATED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENSURE_UPDATED>)
      * [`ENSURE_UPDATED.hashes`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENSURE_UPDATED.hashes>)
      * [`ENSURE_UPDATED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENSURE_UPDATED.pallet>)
      * [`ENSURE_UPDATED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENSURE_UPDATED.wallet>)
    * [`ENTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENTER>)
      * [`ENTER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENTER.pallet>)
      * [`ENTER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENTER.wallet>)
    * [`EXTEND`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.EXTEND>)
      * [`EXTEND.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.EXTEND.pallet>)
      * [`EXTEND.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.EXTEND.wallet>)
    * [`FAUCET`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET>)
      * [`FAUCET.block_number`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET.block_number>)
      * [`FAUCET.nonce`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET.nonce>)
      * [`FAUCET.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET.pallet>)
      * [`FAUCET.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET.wallet>)
      * [`FAUCET.work`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET.work>)
    * [`FINALIZE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FINALIZE>)
      * [`FINALIZE.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FINALIZE.crowdloan_id>)
      * [`FINALIZE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FINALIZE.pallet>)
      * [`FINALIZE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FINALIZE.wallet>)
    * [`FORCE_ADJUST_TOTAL_ISSUANCE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE>)
      * [`FORCE_ADJUST_TOTAL_ISSUANCE.delta`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE.delta>)
      * [`FORCE_ADJUST_TOTAL_ISSUANCE.direction`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE.direction>)
      * [`FORCE_ADJUST_TOTAL_ISSUANCE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE.pallet>)
      * [`FORCE_ADJUST_TOTAL_ISSUANCE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE.wallet>)
    * [`FORCE_BATCH`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_BATCH>)
      * [`FORCE_BATCH.calls`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_BATCH.calls>)
      * [`FORCE_BATCH.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_BATCH.pallet>)
      * [`FORCE_BATCH.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_BATCH.wallet>)
    * [`FORCE_ENTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ENTER>)
      * [`FORCE_ENTER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ENTER.pallet>)
      * [`FORCE_ENTER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ENTER.wallet>)
    * [`FORCE_EXIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXIT>)
      * [`FORCE_EXIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXIT.pallet>)
      * [`FORCE_EXIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXIT.wallet>)
    * [`FORCE_EXTEND`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXTEND>)
      * [`FORCE_EXTEND.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXTEND.pallet>)
      * [`FORCE_EXTEND.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXTEND.wallet>)
    * [`FORCE_RELEASE_DEPOSIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT>)
      * [`FORCE_RELEASE_DEPOSIT.account`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT.account>)
      * [`FORCE_RELEASE_DEPOSIT.block`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT.block>)
      * [`FORCE_RELEASE_DEPOSIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT.pallet>)
      * [`FORCE_RELEASE_DEPOSIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT.wallet>)
    * [`FORCE_SET_BALANCE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE>)
      * [`FORCE_SET_BALANCE.new_free`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE.new_free>)
      * [`FORCE_SET_BALANCE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE.pallet>)
      * [`FORCE_SET_BALANCE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE.wallet>)
      * [`FORCE_SET_BALANCE.who`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE.who>)
    * [`FORCE_SLASH_DEPOSIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT>)
      * [`FORCE_SLASH_DEPOSIT.account`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT.account>)
      * [`FORCE_SLASH_DEPOSIT.block`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT.block>)
      * [`FORCE_SLASH_DEPOSIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT.pallet>)
      * [`FORCE_SLASH_DEPOSIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT.wallet>)
    * [`FORCE_TRANSFER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER>)
      * [`FORCE_TRANSFER.dest`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER.dest>)
      * [`FORCE_TRANSFER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER.pallet>)
      * [`FORCE_TRANSFER.source`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER.source>)
      * [`FORCE_TRANSFER.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER.value>)
      * [`FORCE_TRANSFER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER.wallet>)
    * [`FORCE_UNRESERVE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE>)
      * [`FORCE_UNRESERVE.amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE.amount>)
      * [`FORCE_UNRESERVE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE.pallet>)
      * [`FORCE_UNRESERVE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE.wallet>)
      * [`FORCE_UNRESERVE.who`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE.who>)
    * [`IF_ELSE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE>)
      * [`IF_ELSE.fallback`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE.fallback>)
      * [`IF_ELSE.main`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE.main>)
      * [`IF_ELSE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE.pallet>)
      * [`IF_ELSE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE.wallet>)
    * [`INCREASE_TAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE>)
      * [`INCREASE_TAKE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE.hotkey>)
      * [`INCREASE_TAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE.pallet>)
      * [`INCREASE_TAKE.take`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE.take>)
      * [`INCREASE_TAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE.wallet>)
    * [`INSTANTIATE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE>)
      * [`INSTANTIATE.code_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.code_hash>)
      * [`INSTANTIATE.data`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.data>)
      * [`INSTANTIATE.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.gas_limit>)
      * [`INSTANTIATE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.pallet>)
      * [`INSTANTIATE.salt`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.salt>)
      * [`INSTANTIATE.storage_deposit_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.storage_deposit_limit>)
      * [`INSTANTIATE.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.value>)
      * [`INSTANTIATE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.wallet>)
    * [`INSTANTIATE_OLD_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT>)
      * [`INSTANTIATE_OLD_WEIGHT.code_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.code_hash>)
      * [`INSTANTIATE_OLD_WEIGHT.data`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.data>)
      * [`INSTANTIATE_OLD_WEIGHT.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.gas_limit>)
      * [`INSTANTIATE_OLD_WEIGHT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.pallet>)
      * [`INSTANTIATE_OLD_WEIGHT.salt`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.salt>)
      * [`INSTANTIATE_OLD_WEIGHT.storage_deposit_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.storage_deposit_limit>)
      * [`INSTANTIATE_OLD_WEIGHT.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.value>)
      * [`INSTANTIATE_OLD_WEIGHT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.wallet>)
    * [`INSTANTIATE_WITH_CODE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE>)
      * [`INSTANTIATE_WITH_CODE.code`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.code>)
      * [`INSTANTIATE_WITH_CODE.data`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.data>)
      * [`INSTANTIATE_WITH_CODE.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.gas_limit>)
      * [`INSTANTIATE_WITH_CODE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.pallet>)
      * [`INSTANTIATE_WITH_CODE.salt`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.salt>)
      * [`INSTANTIATE_WITH_CODE.storage_deposit_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.storage_deposit_limit>)
      * [`INSTANTIATE_WITH_CODE.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.value>)
      * [`INSTANTIATE_WITH_CODE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.wallet>)
    * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.code`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.code>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.data`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.data>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.gas_limit>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.pallet>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.salt`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.salt>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.storage_deposit_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.storage_deposit_limit>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.value>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.wallet>)
    * [`KILL_PREFIX`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX>)
      * [`KILL_PREFIX.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX.pallet>)
      * [`KILL_PREFIX.prefix`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX.prefix>)
      * [`KILL_PREFIX.subkeys`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX.subkeys>)
      * [`KILL_PREFIX.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX.wallet>)
    * [`KILL_PURE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE>)
      * [`KILL_PURE.ext_index`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.ext_index>)
      * [`KILL_PURE.height`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.height>)
      * [`KILL_PURE.index`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.index>)
      * [`KILL_PURE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.pallet>)
      * [`KILL_PURE.proxy_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.proxy_type>)
      * [`KILL_PURE.spawner`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.spawner>)
      * [`KILL_PURE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.wallet>)
    * [`KILL_STORAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_STORAGE>)
      * [`KILL_STORAGE.keys`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_STORAGE.keys>)
      * [`KILL_STORAGE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_STORAGE.pallet>)
      * [`KILL_STORAGE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_STORAGE.wallet>)
    * [`MIGRATE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MIGRATE>)
      * [`MIGRATE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MIGRATE.pallet>)
      * [`MIGRATE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MIGRATE.wallet>)
      * [`MIGRATE.weight_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MIGRATE.weight_limit>)
    * [`MODIFY_POSITION`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION>)
      * [`MODIFY_POSITION.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.hotkey>)
      * [`MODIFY_POSITION.liquidity_delta`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.liquidity_delta>)
      * [`MODIFY_POSITION.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.netuid>)
      * [`MODIFY_POSITION.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.pallet>)
      * [`MODIFY_POSITION.position_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.position_id>)
      * [`MODIFY_POSITION.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.wallet>)
    * [`MOVE_STAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE>)
      * [`MOVE_STAKE.alpha_amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.alpha_amount>)
      * [`MOVE_STAKE.destination_hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.destination_hotkey>)
      * [`MOVE_STAKE.destination_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.destination_netuid>)
      * [`MOVE_STAKE.origin_hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.origin_hotkey>)
      * [`MOVE_STAKE.origin_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.origin_netuid>)
      * [`MOVE_STAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.pallet>)
      * [`MOVE_STAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.wallet>)
    * [`NOTE_PREIMAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE>)
      * [`NOTE_PREIMAGE.bytes`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes>)
      * [`NOTE_PREIMAGE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.pallet>)
      * [`NOTE_PREIMAGE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.wallet>)
    * [`NOTE_STALLED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED>)
      * [`NOTE_STALLED.best_finalized_block_number`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED.best_finalized_block_number>)
      * [`NOTE_STALLED.delay`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED.delay>)
      * [`NOTE_STALLED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED.pallet>)
      * [`NOTE_STALLED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED.wallet>)
    * [`POKE_DEPOSIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT>)
      * [`POKE_DEPOSIT.call_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT.call_hash>)
      * [`POKE_DEPOSIT.other_signatories`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT.other_signatories>)
      * [`POKE_DEPOSIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT.pallet>)
      * [`POKE_DEPOSIT.threshold`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT.threshold>)
      * [`POKE_DEPOSIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT.wallet>)
    * [`POKE_DEPOSIT`](<#id8>)
      * [`POKE_DEPOSIT.pallet`](<#id9>)
      * [`POKE_DEPOSIT.wallet`](<#id10>)
    * [`PROXY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY>)
      * [`PROXY.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY.call>)
      * [`PROXY.force_proxy_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY.force_proxy_type>)
      * [`PROXY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY.pallet>)
      * [`PROXY.real`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY.real>)
      * [`PROXY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY.wallet>)
    * [`PROXY_ANNOUNCED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED>)
      * [`PROXY_ANNOUNCED.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.call>)
      * [`PROXY_ANNOUNCED.delegate`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.delegate>)
      * [`PROXY_ANNOUNCED.force_proxy_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.force_proxy_type>)
      * [`PROXY_ANNOUNCED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.pallet>)
      * [`PROXY_ANNOUNCED.real`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.real>)
      * [`PROXY_ANNOUNCED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.wallet>)
    * [`RECYCLE_ALPHA`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA>)
      * [`RECYCLE_ALPHA.amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA.amount>)
      * [`RECYCLE_ALPHA.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA.hotkey>)
      * [`RECYCLE_ALPHA.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA.netuid>)
      * [`RECYCLE_ALPHA.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA.pallet>)
      * [`RECYCLE_ALPHA.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA.wallet>)
    * [`REFUND`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REFUND>)
      * [`REFUND.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REFUND.crowdloan_id>)
      * [`REFUND.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REFUND.pallet>)
      * [`REFUND.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REFUND.wallet>)
    * [`REGISTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER>)
      * [`REGISTER.block_number`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.block_number>)
      * [`REGISTER.coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.coldkey>)
      * [`REGISTER.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.hotkey>)
      * [`REGISTER.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.netuid>)
      * [`REGISTER.nonce`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.nonce>)
      * [`REGISTER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.pallet>)
      * [`REGISTER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.wallet>)
      * [`REGISTER.work`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.work>)
    * [`REGISTER_LEASED_NETWORK`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK>)
      * [`REGISTER_LEASED_NETWORK.emissions_share`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK.emissions_share>)
      * [`REGISTER_LEASED_NETWORK.end_block`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK.end_block>)
      * [`REGISTER_LEASED_NETWORK.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK.pallet>)
      * [`REGISTER_LEASED_NETWORK.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK.wallet>)
    * [`REGISTER_LIMIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT>)
      * [`REGISTER_LIMIT.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT.hotkey>)
      * [`REGISTER_LIMIT.limit_price`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT.limit_price>)
      * [`REGISTER_LIMIT.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT.netuid>)
      * [`REGISTER_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT.pallet>)
      * [`REGISTER_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT.wallet>)
    * [`REGISTER_NETWORK`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK>)
      * [`REGISTER_NETWORK.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK.hotkey>)
      * [`REGISTER_NETWORK.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK.pallet>)
      * [`REGISTER_NETWORK.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK.wallet>)
    * [`REGISTER_NETWORK_WITH_IDENTITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY>)
      * [`REGISTER_NETWORK_WITH_IDENTITY.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY.hotkey>)
      * [`REGISTER_NETWORK_WITH_IDENTITY.identity`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY.identity>)
      * [`REGISTER_NETWORK_WITH_IDENTITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY.pallet>)
      * [`REGISTER_NETWORK_WITH_IDENTITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY.wallet>)
    * [`REJECT_ANNOUNCEMENT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT>)
      * [`REJECT_ANNOUNCEMENT.call_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT.call_hash>)
      * [`REJECT_ANNOUNCEMENT.delegate`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT.delegate>)
      * [`REJECT_ANNOUNCEMENT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT.pallet>)
      * [`REJECT_ANNOUNCEMENT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT.wallet>)
    * [`RELEASE_DEPOSIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT>)
      * [`RELEASE_DEPOSIT.account`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT.account>)
      * [`RELEASE_DEPOSIT.block`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT.block>)
      * [`RELEASE_DEPOSIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT.pallet>)
      * [`RELEASE_DEPOSIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT.wallet>)
    * [`REMARK`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK>)
      * [`REMARK.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK.pallet>)
      * [`REMARK.remark`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK.remark>)
      * [`REMARK.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK.wallet>)
    * [`REMARK_WITH_EVENT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK_WITH_EVENT>)
      * [`REMARK_WITH_EVENT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK_WITH_EVENT.pallet>)
      * [`REMARK_WITH_EVENT.remark`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK_WITH_EVENT.remark>)
      * [`REMARK_WITH_EVENT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK_WITH_EVENT.wallet>)
    * [`REMOVE_ANNOUNCEMENT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT>)
      * [`REMOVE_ANNOUNCEMENT.call_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT.call_hash>)
      * [`REMOVE_ANNOUNCEMENT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT.pallet>)
      * [`REMOVE_ANNOUNCEMENT.real`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT.real>)
      * [`REMOVE_ANNOUNCEMENT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT.wallet>)
    * [`REMOVE_CODE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_CODE>)
      * [`REMOVE_CODE.code_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_CODE.code_hash>)
      * [`REMOVE_CODE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_CODE.pallet>)
      * [`REMOVE_CODE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_CODE.wallet>)
    * [`REMOVE_KEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_KEY>)
      * [`REMOVE_KEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_KEY.pallet>)
      * [`REMOVE_KEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_KEY.wallet>)
    * [`REMOVE_LIQUIDITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY>)
      * [`REMOVE_LIQUIDITY.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY.hotkey>)
      * [`REMOVE_LIQUIDITY.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY.netuid>)
      * [`REMOVE_LIQUIDITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY.pallet>)
      * [`REMOVE_LIQUIDITY.position_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY.position_id>)
      * [`REMOVE_LIQUIDITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY.wallet>)
    * [`REMOVE_PROXIES`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXIES>)
      * [`REMOVE_PROXIES.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXIES.pallet>)
      * [`REMOVE_PROXIES.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXIES.wallet>)
    * [`REMOVE_PROXY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY>)
      * [`REMOVE_PROXY.delay`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY.delay>)
      * [`REMOVE_PROXY.delegate`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY.delegate>)
      * [`REMOVE_PROXY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY.pallet>)
      * [`REMOVE_PROXY.proxy_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY.proxy_type>)
      * [`REMOVE_PROXY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY.wallet>)
    * [`REMOVE_STAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE>)
      * [`REMOVE_STAKE.amount_unstaked`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE.amount_unstaked>)
      * [`REMOVE_STAKE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE.hotkey>)
      * [`REMOVE_STAKE.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE.netuid>)
      * [`REMOVE_STAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE.pallet>)
      * [`REMOVE_STAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE.wallet>)
    * [`REMOVE_STAKE_FULL_LIMIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT>)
      * [`REMOVE_STAKE_FULL_LIMIT.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT.hotkey>)
      * [`REMOVE_STAKE_FULL_LIMIT.limit_price`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT.limit_price>)
      * [`REMOVE_STAKE_FULL_LIMIT.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT.netuid>)
      * [`REMOVE_STAKE_FULL_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT.pallet>)
      * [`REMOVE_STAKE_FULL_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT.wallet>)
    * [`REMOVE_STAKE_LIMIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT>)
      * [`REMOVE_STAKE_LIMIT.allow_partial`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.allow_partial>)
      * [`REMOVE_STAKE_LIMIT.amount_unstaked`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.amount_unstaked>)
      * [`REMOVE_STAKE_LIMIT.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.hotkey>)
      * [`REMOVE_STAKE_LIMIT.limit_price`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.limit_price>)
      * [`REMOVE_STAKE_LIMIT.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.netuid>)
      * [`REMOVE_STAKE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.pallet>)
      * [`REMOVE_STAKE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.wallet>)
    * [`REPORT_EQUIVOCATION`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION>)
      * [`REPORT_EQUIVOCATION.equivocation_proof`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION.equivocation_proof>)
      * [`REPORT_EQUIVOCATION.key_owner_proof`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION.key_owner_proof>)
      * [`REPORT_EQUIVOCATION.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION.pallet>)
      * [`REPORT_EQUIVOCATION.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION.wallet>)
    * [`REPORT_EQUIVOCATION_UNSIGNED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED>)
      * [`REPORT_EQUIVOCATION_UNSIGNED.equivocation_proof`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED.equivocation_proof>)
      * [`REPORT_EQUIVOCATION_UNSIGNED.key_owner_proof`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED.key_owner_proof>)
      * [`REPORT_EQUIVOCATION_UNSIGNED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED.pallet>)
      * [`REPORT_EQUIVOCATION_UNSIGNED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED.wallet>)
    * [`REQUEST_PREIMAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REQUEST_PREIMAGE>)
      * [`REQUEST_PREIMAGE.hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REQUEST_PREIMAGE.hash>)
      * [`REQUEST_PREIMAGE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REQUEST_PREIMAGE.pallet>)
      * [`REQUEST_PREIMAGE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REQUEST_PREIMAGE.wallet>)
    * [`RESET_COLDKEY_SWAP`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RESET_COLDKEY_SWAP>)
      * [`RESET_COLDKEY_SWAP.coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RESET_COLDKEY_SWAP.coldkey>)
      * [`RESET_COLDKEY_SWAP.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RESET_COLDKEY_SWAP.pallet>)
      * [`RESET_COLDKEY_SWAP.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RESET_COLDKEY_SWAP.wallet>)
    * [`REVEAL_MECHANISM_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS>)
      * [`REVEAL_MECHANISM_WEIGHTS.mecid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.mecid>)
      * [`REVEAL_MECHANISM_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.netuid>)
      * [`REVEAL_MECHANISM_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.pallet>)
      * [`REVEAL_MECHANISM_WEIGHTS.salt`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.salt>)
      * [`REVEAL_MECHANISM_WEIGHTS.uids`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.uids>)
      * [`REVEAL_MECHANISM_WEIGHTS.values`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.values>)
      * [`REVEAL_MECHANISM_WEIGHTS.version_key`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.version_key>)
      * [`REVEAL_MECHANISM_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.wallet>)
    * [`REVEAL_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS>)
      * [`REVEAL_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.netuid>)
      * [`REVEAL_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.pallet>)
      * [`REVEAL_WEIGHTS.salt`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.salt>)
      * [`REVEAL_WEIGHTS.uids`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.uids>)
      * [`REVEAL_WEIGHTS.values`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.values>)
      * [`REVEAL_WEIGHTS.version_key`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.version_key>)
      * [`REVEAL_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.wallet>)
    * [`ROOT_DISSOLVE_NETWORK`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_DISSOLVE_NETWORK>)
      * [`ROOT_DISSOLVE_NETWORK.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_DISSOLVE_NETWORK.netuid>)
      * [`ROOT_DISSOLVE_NETWORK.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_DISSOLVE_NETWORK.pallet>)
      * [`ROOT_DISSOLVE_NETWORK.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_DISSOLVE_NETWORK.wallet>)
    * [`ROOT_REGISTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_REGISTER>)
      * [`ROOT_REGISTER.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_REGISTER.hotkey>)
      * [`ROOT_REGISTER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_REGISTER.pallet>)
      * [`ROOT_REGISTER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_REGISTER.wallet>)
    * [`SCHEDULE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE>)
      * [`SCHEDULE.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.call>)
      * [`SCHEDULE.maybe_periodic`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.maybe_periodic>)
      * [`SCHEDULE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.pallet>)
      * [`SCHEDULE.priority`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.priority>)
      * [`SCHEDULE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.wallet>)
      * [`SCHEDULE.when`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.when>)
    * [`SCHEDULE_AFTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER>)
      * [`SCHEDULE_AFTER.after`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.after>)
      * [`SCHEDULE_AFTER.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.call>)
      * [`SCHEDULE_AFTER.maybe_periodic`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.maybe_periodic>)
      * [`SCHEDULE_AFTER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.pallet>)
      * [`SCHEDULE_AFTER.priority`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.priority>)
      * [`SCHEDULE_AFTER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.wallet>)
    * [`SCHEDULE_GRANDPA_CHANGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE>)
      * [`SCHEDULE_GRANDPA_CHANGE.forced`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE.forced>)
      * [`SCHEDULE_GRANDPA_CHANGE.in_blocks`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE.in_blocks>)
      * [`SCHEDULE_GRANDPA_CHANGE.next_authorities`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE.next_authorities>)
      * [`SCHEDULE_GRANDPA_CHANGE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE.pallet>)
      * [`SCHEDULE_GRANDPA_CHANGE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE.wallet>)
    * [`SCHEDULE_NAMED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED>)
      * [`SCHEDULE_NAMED.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.call>)
      * [`SCHEDULE_NAMED.id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.id>)
      * [`SCHEDULE_NAMED.maybe_periodic`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.maybe_periodic>)
      * [`SCHEDULE_NAMED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.pallet>)
      * [`SCHEDULE_NAMED.priority`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.priority>)
      * [`SCHEDULE_NAMED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.wallet>)
      * [`SCHEDULE_NAMED.when`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.when>)
    * [`SCHEDULE_NAMED_AFTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER>)
      * [`SCHEDULE_NAMED_AFTER.after`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.after>)
      * [`SCHEDULE_NAMED_AFTER.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.call>)
      * [`SCHEDULE_NAMED_AFTER.id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.id>)
      * [`SCHEDULE_NAMED_AFTER.maybe_periodic`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.maybe_periodic>)
      * [`SCHEDULE_NAMED_AFTER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.pallet>)
      * [`SCHEDULE_NAMED_AFTER.priority`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.priority>)
      * [`SCHEDULE_NAMED_AFTER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.wallet>)
    * [`SCHEDULE_SWAP_COLDKEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_SWAP_COLDKEY>)
      * [`SCHEDULE_SWAP_COLDKEY.new_coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_SWAP_COLDKEY.new_coldkey>)
      * [`SCHEDULE_SWAP_COLDKEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_SWAP_COLDKEY.pallet>)
      * [`SCHEDULE_SWAP_COLDKEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_SWAP_COLDKEY.wallet>)
    * [`SERVE_AXON`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON>)
      * [`SERVE_AXON.ip`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.ip>)
      * [`SERVE_AXON.ip_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.ip_type>)
      * [`SERVE_AXON.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.netuid>)
      * [`SERVE_AXON.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.pallet>)
      * [`SERVE_AXON.placeholder1`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.placeholder1>)
      * [`SERVE_AXON.placeholder2`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.placeholder2>)
      * [`SERVE_AXON.port`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.port>)
      * [`SERVE_AXON.protocol`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.protocol>)
      * [`SERVE_AXON.version`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.version>)
      * [`SERVE_AXON.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.wallet>)
    * [`SERVE_AXON_TLS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS>)
      * [`SERVE_AXON_TLS.certificate`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.certificate>)
      * [`SERVE_AXON_TLS.ip`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.ip>)
      * [`SERVE_AXON_TLS.ip_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.ip_type>)
      * [`SERVE_AXON_TLS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.netuid>)
      * [`SERVE_AXON_TLS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.pallet>)
      * [`SERVE_AXON_TLS.placeholder1`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.placeholder1>)
      * [`SERVE_AXON_TLS.placeholder2`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.placeholder2>)
      * [`SERVE_AXON_TLS.port`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.port>)
      * [`SERVE_AXON_TLS.protocol`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.protocol>)
      * [`SERVE_AXON_TLS.version`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.version>)
      * [`SERVE_AXON_TLS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.wallet>)
    * [`SERVE_PROMETHEUS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS>)
      * [`SERVE_PROMETHEUS.ip`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.ip>)
      * [`SERVE_PROMETHEUS.ip_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.ip_type>)
      * [`SERVE_PROMETHEUS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.netuid>)
      * [`SERVE_PROMETHEUS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.pallet>)
      * [`SERVE_PROMETHEUS.port`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.port>)
      * [`SERVE_PROMETHEUS.version`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.version>)
      * [`SERVE_PROMETHEUS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.wallet>)
    * [`SET`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET>)
      * [`SET.now`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET.now>)
      * [`SET.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET.pallet>)
      * [`SET.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET.wallet>)
    * [`SET_AUTO_PARENT_DELEGATION_ENABLED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED>)
      * [`SET_AUTO_PARENT_DELEGATION_ENABLED.enabled`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED.enabled>)
      * [`SET_AUTO_PARENT_DELEGATION_ENABLED.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED.hotkey>)
      * [`SET_AUTO_PARENT_DELEGATION_ENABLED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED.pallet>)
      * [`SET_AUTO_PARENT_DELEGATION_ENABLED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED.wallet>)
    * [`SET_BASE_FEE_PER_GAS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BASE_FEE_PER_GAS>)
      * [`SET_BASE_FEE_PER_GAS.fee`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BASE_FEE_PER_GAS.fee>)
      * [`SET_BASE_FEE_PER_GAS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BASE_FEE_PER_GAS.pallet>)
      * [`SET_BASE_FEE_PER_GAS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BASE_FEE_PER_GAS.wallet>)
    * [`SET_BEACON_CONFIG`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG>)
      * [`SET_BEACON_CONFIG.config_payload`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG.config_payload>)
      * [`SET_BEACON_CONFIG.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG.pallet>)
      * [`SET_BEACON_CONFIG.signature`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG.signature>)
      * [`SET_BEACON_CONFIG.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG.wallet>)
    * [`SET_CHILDKEY_TAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE>)
      * [`SET_CHILDKEY_TAKE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE.hotkey>)
      * [`SET_CHILDKEY_TAKE.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE.netuid>)
      * [`SET_CHILDKEY_TAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE.pallet>)
      * [`SET_CHILDKEY_TAKE.take`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE.take>)
      * [`SET_CHILDKEY_TAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE.wallet>)
    * [`SET_CHILDREN`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN>)
      * [`SET_CHILDREN.children`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN.children>)
      * [`SET_CHILDREN.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN.hotkey>)
      * [`SET_CHILDREN.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN.netuid>)
      * [`SET_CHILDREN.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN.pallet>)
      * [`SET_CHILDREN.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN.wallet>)
    * [`SET_CODE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE>)
      * [`SET_CODE.code`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE.code>)
      * [`SET_CODE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE.pallet>)
      * [`SET_CODE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE.wallet>)
    * [`SET_CODE`](<#id11>)
      * [`SET_CODE.code_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE.code_hash>)
      * [`SET_CODE.dest`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE.dest>)
      * [`SET_CODE.pallet`](<#id12>)
      * [`SET_CODE.wallet`](<#id13>)
    * [`SET_CODE_WITHOUT_CHECKS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE_WITHOUT_CHECKS>)
      * [`SET_CODE_WITHOUT_CHECKS.code`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE_WITHOUT_CHECKS.code>)
      * [`SET_CODE_WITHOUT_CHECKS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE_WITHOUT_CHECKS.pallet>)
      * [`SET_CODE_WITHOUT_CHECKS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE_WITHOUT_CHECKS.wallet>)
    * [`SET_COLDKEY_AUTO_STAKE_HOTKEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY>)
      * [`SET_COLDKEY_AUTO_STAKE_HOTKEY.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY.hotkey>)
      * [`SET_COLDKEY_AUTO_STAKE_HOTKEY.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY.netuid>)
      * [`SET_COLDKEY_AUTO_STAKE_HOTKEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY.pallet>)
      * [`SET_COLDKEY_AUTO_STAKE_HOTKEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY.wallet>)
    * [`SET_COMMITMENT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT>)
      * [`SET_COMMITMENT.info`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT.info>)
      * [`SET_COMMITMENT.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT.netuid>)
      * [`SET_COMMITMENT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT.pallet>)
      * [`SET_COMMITMENT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT.wallet>)
    * [`SET_ELASTICITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ELASTICITY>)
      * [`SET_ELASTICITY.elasticity`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ELASTICITY.elasticity>)
      * [`SET_ELASTICITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ELASTICITY.pallet>)
      * [`SET_ELASTICITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ELASTICITY.wallet>)
    * [`SET_FEE_RATE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE>)
      * [`SET_FEE_RATE.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE.netuid>)
      * [`SET_FEE_RATE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE.pallet>)
      * [`SET_FEE_RATE.rate`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE.rate>)
      * [`SET_FEE_RATE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE.wallet>)
    * [`SET_HEAP_PAGES`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_HEAP_PAGES>)
      * [`SET_HEAP_PAGES.pages`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_HEAP_PAGES.pages>)
      * [`SET_HEAP_PAGES.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_HEAP_PAGES.pallet>)
      * [`SET_HEAP_PAGES.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_HEAP_PAGES.wallet>)
    * [`SET_IDENTITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY>)
      * [`SET_IDENTITY.identified`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.identified>)
      * [`SET_IDENTITY.info`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.info>)
      * [`SET_IDENTITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.pallet>)
      * [`SET_IDENTITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.wallet>)
    * [`SET_IDENTITY`](<#id14>)
      * [`SET_IDENTITY.additional`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.additional>)
      * [`SET_IDENTITY.description`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.description>)
      * [`SET_IDENTITY.discord`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.discord>)
      * [`SET_IDENTITY.github_repo`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.github_repo>)
      * [`SET_IDENTITY.image`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.image>)
      * [`SET_IDENTITY.name`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.name>)
      * [`SET_IDENTITY.pallet`](<#id15>)
      * [`SET_IDENTITY.url`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.url>)
      * [`SET_IDENTITY.wallet`](<#id16>)
    * [`SET_KEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_KEY>)
      * [`SET_KEY.new`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_KEY.new>)
      * [`SET_KEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_KEY.pallet>)
      * [`SET_KEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_KEY.wallet>)
    * [`SET_MAX_EXTRINSIC_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_EXTRINSIC_WEIGHT>)
      * [`SET_MAX_EXTRINSIC_WEIGHT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_EXTRINSIC_WEIGHT.pallet>)
      * [`SET_MAX_EXTRINSIC_WEIGHT.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_EXTRINSIC_WEIGHT.value>)
      * [`SET_MAX_EXTRINSIC_WEIGHT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_EXTRINSIC_WEIGHT.wallet>)
    * [`SET_MAX_PENDING_EXTRINSICS_NUMBER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_PENDING_EXTRINSICS_NUMBER>)
      * [`SET_MAX_PENDING_EXTRINSICS_NUMBER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_PENDING_EXTRINSICS_NUMBER.pallet>)
      * [`SET_MAX_PENDING_EXTRINSICS_NUMBER.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_PENDING_EXTRINSICS_NUMBER.value>)
      * [`SET_MAX_PENDING_EXTRINSICS_NUMBER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_PENDING_EXTRINSICS_NUMBER.wallet>)
    * [`SET_MAX_SPACE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_SPACE>)
      * [`SET_MAX_SPACE.new_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_SPACE.new_limit>)
      * [`SET_MAX_SPACE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_SPACE.pallet>)
      * [`SET_MAX_SPACE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_SPACE.wallet>)
    * [`SET_MECHANISM_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS>)
      * [`SET_MECHANISM_WEIGHTS.dests`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.dests>)
      * [`SET_MECHANISM_WEIGHTS.mecid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.mecid>)
      * [`SET_MECHANISM_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.netuid>)
      * [`SET_MECHANISM_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.pallet>)
      * [`SET_MECHANISM_WEIGHTS.version_key`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.version_key>)
      * [`SET_MECHANISM_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.wallet>)
      * [`SET_MECHANISM_WEIGHTS.weights`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.weights>)
    * [`SET_OLDEST_STORED_ROUND`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_OLDEST_STORED_ROUND>)
      * [`SET_OLDEST_STORED_ROUND.oldest_round`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_OLDEST_STORED_ROUND.oldest_round>)
      * [`SET_OLDEST_STORED_ROUND.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_OLDEST_STORED_ROUND.pallet>)
      * [`SET_OLDEST_STORED_ROUND.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_OLDEST_STORED_ROUND.wallet>)
    * [`SET_ON_INITIALIZE_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ON_INITIALIZE_WEIGHT>)
      * [`SET_ON_INITIALIZE_WEIGHT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ON_INITIALIZE_WEIGHT.pallet>)
      * [`SET_ON_INITIALIZE_WEIGHT.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ON_INITIALIZE_WEIGHT.value>)
      * [`SET_ON_INITIALIZE_WEIGHT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ON_INITIALIZE_WEIGHT.wallet>)
    * [`SET_PENDING_CHILDKEY_COOLDOWN`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_PENDING_CHILDKEY_COOLDOWN>)
      * [`SET_PENDING_CHILDKEY_COOLDOWN.cooldown`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_PENDING_CHILDKEY_COOLDOWN.cooldown>)
      * [`SET_PENDING_CHILDKEY_COOLDOWN.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_PENDING_CHILDKEY_COOLDOWN.pallet>)
      * [`SET_PENDING_CHILDKEY_COOLDOWN.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_PENDING_CHILDKEY_COOLDOWN.wallet>)
    * [`SET_REAL_PAYS_FEE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE>)
      * [`SET_REAL_PAYS_FEE.delegate`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE.delegate>)
      * [`SET_REAL_PAYS_FEE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE.pallet>)
      * [`SET_REAL_PAYS_FEE.pays_fee`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE.pays_fee>)
      * [`SET_REAL_PAYS_FEE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE.wallet>)
    * [`SET_RETRY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY>)
      * [`SET_RETRY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY.pallet>)
      * [`SET_RETRY.period`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY.period>)
      * [`SET_RETRY.retries`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY.retries>)
      * [`SET_RETRY.task`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY.task>)
      * [`SET_RETRY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY.wallet>)
    * [`SET_RETRY_NAMED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED>)
      * [`SET_RETRY_NAMED.id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED.id>)
      * [`SET_RETRY_NAMED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED.pallet>)
      * [`SET_RETRY_NAMED.period`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED.period>)
      * [`SET_RETRY_NAMED.retries`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED.retries>)
      * [`SET_RETRY_NAMED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED.wallet>)
    * [`SET_ROOT_CLAIM_TYPE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ROOT_CLAIM_TYPE>)
      * [`SET_ROOT_CLAIM_TYPE.new_root_claim_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ROOT_CLAIM_TYPE.new_root_claim_type>)
      * [`SET_ROOT_CLAIM_TYPE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ROOT_CLAIM_TYPE.pallet>)
      * [`SET_ROOT_CLAIM_TYPE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ROOT_CLAIM_TYPE.wallet>)
    * [`SET_STORAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORAGE>)
      * [`SET_STORAGE.items`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORAGE.items>)
      * [`SET_STORAGE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORAGE.pallet>)
      * [`SET_STORAGE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORAGE.wallet>)
    * [`SET_STORED_EXTRINSIC_LIFETIME`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORED_EXTRINSIC_LIFETIME>)
      * [`SET_STORED_EXTRINSIC_LIFETIME.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORED_EXTRINSIC_LIFETIME.pallet>)
      * [`SET_STORED_EXTRINSIC_LIFETIME.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORED_EXTRINSIC_LIFETIME.value>)
      * [`SET_STORED_EXTRINSIC_LIFETIME.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORED_EXTRINSIC_LIFETIME.wallet>)
    * [`SET_SUBNET_IDENTITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY>)
      * [`SET_SUBNET_IDENTITY.additional`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.additional>)
      * [`SET_SUBNET_IDENTITY.description`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.description>)
      * [`SET_SUBNET_IDENTITY.discord`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.discord>)
      * [`SET_SUBNET_IDENTITY.github_repo`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.github_repo>)
      * [`SET_SUBNET_IDENTITY.logo_url`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.logo_url>)
      * [`SET_SUBNET_IDENTITY.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.netuid>)
      * [`SET_SUBNET_IDENTITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.pallet>)
      * [`SET_SUBNET_IDENTITY.subnet_contact`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.subnet_contact>)
      * [`SET_SUBNET_IDENTITY.subnet_name`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.subnet_name>)
      * [`SET_SUBNET_IDENTITY.subnet_url`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.subnet_url>)
      * [`SET_SUBNET_IDENTITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.wallet>)
    * [`SET_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS>)
      * [`SET_WEIGHTS.dests`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.dests>)
      * [`SET_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.netuid>)
      * [`SET_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.pallet>)
      * [`SET_WEIGHTS.version_key`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.version_key>)
      * [`SET_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.wallet>)
      * [`SET_WEIGHTS.weights`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.weights>)
    * [`SET_WHITELIST`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WHITELIST>)
      * [`SET_WHITELIST.new`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WHITELIST.new>)
      * [`SET_WHITELIST.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WHITELIST.pallet>)
      * [`SET_WHITELIST.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WHITELIST.wallet>)
    * [`START_CALL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.START_CALL>)
      * [`START_CALL.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.START_CALL.netuid>)
      * [`START_CALL.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.START_CALL.pallet>)
      * [`START_CALL.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.START_CALL.wallet>)
    * [`STORE_ENCRYPTED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.STORE_ENCRYPTED>)
      * [`STORE_ENCRYPTED.encrypted_call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.STORE_ENCRYPTED.encrypted_call>)
      * [`STORE_ENCRYPTED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.STORE_ENCRYPTED.pallet>)
      * [`STORE_ENCRYPTED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.STORE_ENCRYPTED.wallet>)
    * [`SUBMIT_ENCRYPTED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUBMIT_ENCRYPTED>)
      * [`SUBMIT_ENCRYPTED.ciphertext`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUBMIT_ENCRYPTED.ciphertext>)
      * [`SUBMIT_ENCRYPTED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUBMIT_ENCRYPTED.pallet>)
      * [`SUBMIT_ENCRYPTED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUBMIT_ENCRYPTED.wallet>)
    * [`SUDO`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUDO>)
      * [`SUDO.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUDO.call>)
      * [`SUDO.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUDO.pallet>)
      * [`SUDO.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUDO.wallet>)
    * [`SWAP_AUTHORITIES`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_AUTHORITIES>)
      * [`SWAP_AUTHORITIES.new_authorities`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_AUTHORITIES.new_authorities>)
      * [`SWAP_AUTHORITIES.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_AUTHORITIES.pallet>)
      * [`SWAP_AUTHORITIES.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_AUTHORITIES.wallet>)
    * [`SWAP_COLDKEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY>)
      * [`SWAP_COLDKEY.new_coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY.new_coldkey>)
      * [`SWAP_COLDKEY.old_coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY.old_coldkey>)
      * [`SWAP_COLDKEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY.pallet>)
      * [`SWAP_COLDKEY.swap_cost`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY.swap_cost>)
      * [`SWAP_COLDKEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY.wallet>)
    * [`SWAP_COLDKEY_ANNOUNCED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY_ANNOUNCED>)
      * [`SWAP_COLDKEY_ANNOUNCED.new_coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY_ANNOUNCED.new_coldkey>)
      * [`SWAP_COLDKEY_ANNOUNCED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY_ANNOUNCED.pallet>)
      * [`SWAP_COLDKEY_ANNOUNCED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY_ANNOUNCED.wallet>)
    * [`SWAP_HOTKEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY>)
      * [`SWAP_HOTKEY.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY.hotkey>)
      * [`SWAP_HOTKEY.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY.netuid>)
      * [`SWAP_HOTKEY.new_hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY.new_hotkey>)
      * [`SWAP_HOTKEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY.pallet>)
      * [`SWAP_HOTKEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY.wallet>)
    * [`SWAP_HOTKEY_V2`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2>)
      * [`SWAP_HOTKEY_V2.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.hotkey>)
      * [`SWAP_HOTKEY_V2.keep_stake`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.keep_stake>)
      * [`SWAP_HOTKEY_V2.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.netuid>)
      * [`SWAP_HOTKEY_V2.new_hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.new_hotkey>)
      * [`SWAP_HOTKEY_V2.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.pallet>)
      * [`SWAP_HOTKEY_V2.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.wallet>)
    * [`SWAP_STAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE>)
      * [`SWAP_STAKE.alpha_amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.alpha_amount>)
      * [`SWAP_STAKE.destination_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.destination_netuid>)
      * [`SWAP_STAKE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.hotkey>)
      * [`SWAP_STAKE.origin_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.origin_netuid>)
      * [`SWAP_STAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.pallet>)
      * [`SWAP_STAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.wallet>)
    * [`SWAP_STAKE_LIMIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT>)
      * [`SWAP_STAKE_LIMIT.allow_partial`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.allow_partial>)
      * [`SWAP_STAKE_LIMIT.alpha_amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.alpha_amount>)
      * [`SWAP_STAKE_LIMIT.destination_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.destination_netuid>)
      * [`SWAP_STAKE_LIMIT.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.hotkey>)
      * [`SWAP_STAKE_LIMIT.limit_price`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.limit_price>)
      * [`SWAP_STAKE_LIMIT.origin_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.origin_netuid>)
      * [`SWAP_STAKE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.pallet>)
      * [`SWAP_STAKE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.wallet>)
    * [`TERMINATE_LEASE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE>)
      * [`TERMINATE_LEASE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE.hotkey>)
      * [`TERMINATE_LEASE.lease_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE.lease_id>)
      * [`TERMINATE_LEASE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE.pallet>)
      * [`TERMINATE_LEASE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE.wallet>)
    * [`TOGGLE_USER_LIQUIDITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY>)
      * [`TOGGLE_USER_LIQUIDITY.enable`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY.enable>)
      * [`TOGGLE_USER_LIQUIDITY.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY.netuid>)
      * [`TOGGLE_USER_LIQUIDITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY.pallet>)
      * [`TOGGLE_USER_LIQUIDITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY.wallet>)
    * [`TRANSACT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSACT>)
      * [`TRANSACT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSACT.pallet>)
      * [`TRANSACT.transaction`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSACT.transaction>)
      * [`TRANSACT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSACT.wallet>)
    * [`TRANSFER_ALL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL>)
      * [`TRANSFER_ALL.dest`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL.dest>)
      * [`TRANSFER_ALL.keep_alive`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL.keep_alive>)
      * [`TRANSFER_ALL.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL.pallet>)
      * [`TRANSFER_ALL.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL.wallet>)
    * [`TRANSFER_ALLOW_DEATH`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH>)
      * [`TRANSFER_ALLOW_DEATH.dest`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH.dest>)
      * [`TRANSFER_ALLOW_DEATH.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH.pallet>)
      * [`TRANSFER_ALLOW_DEATH.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH.value>)
      * [`TRANSFER_ALLOW_DEATH.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH.wallet>)
    * [`TRANSFER_KEEP_ALIVE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE>)
      * [`TRANSFER_KEEP_ALIVE.dest`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE.dest>)
      * [`TRANSFER_KEEP_ALIVE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE.pallet>)
      * [`TRANSFER_KEEP_ALIVE.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE.value>)
      * [`TRANSFER_KEEP_ALIVE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE.wallet>)
    * [`TRANSFER_STAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE>)
      * [`TRANSFER_STAKE.alpha_amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.alpha_amount>)
      * [`TRANSFER_STAKE.destination_coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.destination_coldkey>)
      * [`TRANSFER_STAKE.destination_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.destination_netuid>)
      * [`TRANSFER_STAKE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.hotkey>)
      * [`TRANSFER_STAKE.origin_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.origin_netuid>)
      * [`TRANSFER_STAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.pallet>)
      * [`TRANSFER_STAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.wallet>)
    * [`TRY_ASSOCIATE_HOTKEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRY_ASSOCIATE_HOTKEY>)
      * [`TRY_ASSOCIATE_HOTKEY.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRY_ASSOCIATE_HOTKEY.hotkey>)
      * [`TRY_ASSOCIATE_HOTKEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRY_ASSOCIATE_HOTKEY.pallet>)
      * [`TRY_ASSOCIATE_HOTKEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRY_ASSOCIATE_HOTKEY.wallet>)
    * [`UNNOTE_PREIMAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNNOTE_PREIMAGE>)
      * [`UNNOTE_PREIMAGE.hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNNOTE_PREIMAGE.hash>)
      * [`UNNOTE_PREIMAGE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNNOTE_PREIMAGE.pallet>)
      * [`UNNOTE_PREIMAGE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNNOTE_PREIMAGE.wallet>)
    * [`UNREQUEST_PREIMAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNREQUEST_PREIMAGE>)
      * [`UNREQUEST_PREIMAGE.hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNREQUEST_PREIMAGE.hash>)
      * [`UNREQUEST_PREIMAGE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNREQUEST_PREIMAGE.pallet>)
      * [`UNREQUEST_PREIMAGE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNREQUEST_PREIMAGE.wallet>)
    * [`UNSTAKE_ALL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL>)
      * [`UNSTAKE_ALL.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL.hotkey>)
      * [`UNSTAKE_ALL.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL.pallet>)
      * [`UNSTAKE_ALL.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL.wallet>)
    * [`UNSTAKE_ALL_ALPHA`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL_ALPHA>)
      * [`UNSTAKE_ALL_ALPHA.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL_ALPHA.hotkey>)
      * [`UNSTAKE_ALL_ALPHA.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL_ALPHA.pallet>)
      * [`UNSTAKE_ALL_ALPHA.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL_ALPHA.wallet>)
    * [`UPDATE_CAP`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP>)
      * [`UPDATE_CAP.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP.crowdloan_id>)
      * [`UPDATE_CAP.new_cap`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP.new_cap>)
      * [`UPDATE_CAP.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP.pallet>)
      * [`UPDATE_CAP.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP.wallet>)
    * [`UPDATE_END`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END>)
      * [`UPDATE_END.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END.crowdloan_id>)
      * [`UPDATE_END.new_end`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END.new_end>)
      * [`UPDATE_END.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END.pallet>)
      * [`UPDATE_END.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END.wallet>)
    * [`UPDATE_MIN_CONTRIBUTION`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION>)
      * [`UPDATE_MIN_CONTRIBUTION.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION.crowdloan_id>)
      * [`UPDATE_MIN_CONTRIBUTION.new_min_contribution`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION.new_min_contribution>)
      * [`UPDATE_MIN_CONTRIBUTION.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION.pallet>)
      * [`UPDATE_MIN_CONTRIBUTION.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION.wallet>)
    * [`UPDATE_SYMBOL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL>)
      * [`UPDATE_SYMBOL.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL.netuid>)
      * [`UPDATE_SYMBOL.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL.pallet>)
      * [`UPDATE_SYMBOL.symbol`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL.symbol>)
      * [`UPDATE_SYMBOL.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL.wallet>)
    * [`UPGRADE_ACCOUNTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPGRADE_ACCOUNTS>)
      * [`UPGRADE_ACCOUNTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPGRADE_ACCOUNTS.pallet>)
      * [`UPGRADE_ACCOUNTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPGRADE_ACCOUNTS.wallet>)
      * [`UPGRADE_ACCOUNTS.who`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPGRADE_ACCOUNTS.who>)
    * [`UPLOAD_CODE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE>)
      * [`UPLOAD_CODE.code`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE.code>)
      * [`UPLOAD_CODE.determinism`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE.determinism>)
      * [`UPLOAD_CODE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE.pallet>)
      * [`UPLOAD_CODE.storage_deposit_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE.storage_deposit_limit>)
      * [`UPLOAD_CODE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE.wallet>)
    * [`WITHDRAW`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW>)
      * [`WITHDRAW.address`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW.address>)
      * [`WITHDRAW.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW.pallet>)
      * [`WITHDRAW.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW.value>)
      * [`WITHDRAW.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW.wallet>)
    * [`WITHDRAW`](<#id17>)
      * [`WITHDRAW.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW.crowdloan_id>)
      * [`WITHDRAW.pallet`](<#id18>)
      * [`WITHDRAW.wallet`](<#id19>)
    * [`WITH_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT>)
      * [`WITH_WEIGHT.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT.call>)
      * [`WITH_WEIGHT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT.pallet>)
      * [`WITH_WEIGHT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT.wallet>)
      * [`WITH_WEIGHT.weight`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT.weight>)
    * [`WRITE_PULSE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE>)
      * [`WRITE_PULSE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE.pallet>)
      * [`WRITE_PULSE.pulses_payload`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE.pulses_payload>)
      * [`WRITE_PULSE.signature`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE.signature>)
      * [`WRITE_PULSE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE.wallet>)



# bittensor.extras.dev_framework.calls.non_sudo_calls[#](<#module-bittensor.extras.dev_framework.calls.non_sudo_calls> "Link to this heading")

This file is auto-generated. Do not edit manually.

For developers: \- Use the function recreate_calls_subpackage() to regenerate this file. \- The command lists are built dynamically from the current Subtensor metadata (Subtensor.substrate.metadata). \- Each command is represented as a namedtuple with fields:

>   * System arguments: wallet, pallet (and sudo for sudo calls).
> 
>   * Additional arguments: taken from the extrinsic definition (with type hints for reference).
> 
> 


  * These namedtuples are intended as convenient templates for building commands in tests and end-to-end scenarios.




Note

Any manual changes will be overwritten the next time the generator is run. Subtensor spec version: 397

## Classes[#](<#classes> "Link to this heading")

[`ADD_LIQUIDITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY> "bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY") |   
---|---  
[`ADD_PROXY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY> "bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY") |   
[`ADD_STAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE> "bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE") |   
[`ADD_STAKE_BURN`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN> "bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN") |   
[`ADD_STAKE_LIMIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT> "bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT") |   
[`ANNOUNCE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE> "bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE") |   
[`ANNOUNCE_COLDKEY_SWAP`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_COLDKEY_SWAP> "bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_COLDKEY_SWAP") |   
[`ANNOUNCE_NEXT_KEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_NEXT_KEY> "bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_NEXT_KEY") |   
[`APPLY_AUTHORIZED_UPGRADE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPLY_AUTHORIZED_UPGRADE> "bittensor.extras.dev_framework.calls.non_sudo_calls.APPLY_AUTHORIZED_UPGRADE") |   
[`APPROVE_AS_MULTI`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI> "bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI") |   
[`ASSOCIATE_EVM_KEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY> "bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY") |   
[`AS_DERIVATIVE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE> "bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE") |   
[`AS_MULTI`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI> "bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI") |   
[`AS_MULTI_THRESHOLD_1`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1> "bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1") |   
[`AUTHORIZE_UPGRADE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE> "bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE") |   
[`AUTHORIZE_UPGRADE_WITHOUT_CHECKS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE_WITHOUT_CHECKS> "bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE_WITHOUT_CHECKS") |   
[`BATCH`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH> "bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH") |   
[`BATCH_ALL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_ALL> "bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_ALL") |   
[`BATCH_COMMIT_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS> "bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS") |   
[`BATCH_REVEAL_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS> "bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS") |   
[`BATCH_SET_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS> "bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS") |   
[`BURN`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN> "bittensor.extras.dev_framework.calls.non_sudo_calls.BURN") |   
[`BURNED_REGISTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER> "bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER") |   
[`BURN_ALPHA`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA> "bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA") |   
[`CALL`](<#id0> "bittensor.extras.dev_framework.calls.non_sudo_calls.CALL") |   
[`CALL`](<#id0> "bittensor.extras.dev_framework.calls.non_sudo_calls.CALL") |   
[`CALL_OLD_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT> "bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT") |   
[`CANCEL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL> "bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL") |   
[`CANCEL_AS_MULTI`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI> "bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI") |   
[`CANCEL_NAMED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_NAMED> "bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_NAMED") |   
[`CANCEL_RETRY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY> "bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY") |   
[`CANCEL_RETRY_NAMED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY_NAMED> "bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY_NAMED") |   
[`CLAIM_ROOT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLAIM_ROOT> "bittensor.extras.dev_framework.calls.non_sudo_calls.CLAIM_ROOT") |   
[`CLEAR_COLDKEY_SWAP_ANNOUNCEMENT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_COLDKEY_SWAP_ANNOUNCEMENT> "bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_COLDKEY_SWAP_ANNOUNCEMENT") |   
[`CLEAR_IDENTITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_IDENTITY> "bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_IDENTITY") |   
[`COMMIT_CRV3_MECHANISM_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS> "bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS") |   
[`COMMIT_MECHANISM_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS> "bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS") |   
[`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS> "bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS") |   
[`COMMIT_TIMELOCKED_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS> "bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS") |   
[`COMMIT_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS> "bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS") |   
[`CONTRIBUTE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE> "bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE") |   
[`CREATE`](<#id5> "bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE") |   
[`CREATE`](<#id5> "bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE") |   
[`CREATE2`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2> "bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2") |   
[`CREATE_PURE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE> "bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE") |   
[`DECREASE_TAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE> "bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE") |   
[`DISABLE_LP`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_LP> "bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_LP") |   
[`DISABLE_VOTING_POWER_TRACKING`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_VOTING_POWER_TRACKING> "bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_VOTING_POWER_TRACKING") |   
[`DISABLE_WHITELIST`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_WHITELIST> "bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_WHITELIST") |   
[`DISPATCH_AS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS> "bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS") |   
[`DISPATCH_AS_FALLIBLE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE> "bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE") |   
[`DISPUTE_COLDKEY_SWAP`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPUTE_COLDKEY_SWAP> "bittensor.extras.dev_framework.calls.non_sudo_calls.DISPUTE_COLDKEY_SWAP") |   
[`DISSOLVE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE> "bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE") |   
[`DISSOLVE_NETWORK`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK> "bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK") |   
[`ENABLE_VOTING_POWER_TRACKING`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENABLE_VOTING_POWER_TRACKING> "bittensor.extras.dev_framework.calls.non_sudo_calls.ENABLE_VOTING_POWER_TRACKING") |   
[`ENSURE_UPDATED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENSURE_UPDATED> "bittensor.extras.dev_framework.calls.non_sudo_calls.ENSURE_UPDATED") |   
[`ENTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENTER> "bittensor.extras.dev_framework.calls.non_sudo_calls.ENTER") |   
[`EXTEND`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.EXTEND> "bittensor.extras.dev_framework.calls.non_sudo_calls.EXTEND") |   
[`FAUCET`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET> "bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET") |   
[`FINALIZE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FINALIZE> "bittensor.extras.dev_framework.calls.non_sudo_calls.FINALIZE") |   
[`FORCE_ADJUST_TOTAL_ISSUANCE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE> "bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE") |   
[`FORCE_BATCH`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_BATCH> "bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_BATCH") |   
[`FORCE_ENTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ENTER> "bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ENTER") |   
[`FORCE_EXIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXIT> "bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXIT") |   
[`FORCE_EXTEND`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXTEND> "bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXTEND") |   
[`FORCE_RELEASE_DEPOSIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT> "bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT") |   
[`FORCE_SET_BALANCE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE> "bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE") |   
[`FORCE_SLASH_DEPOSIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT> "bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT") |   
[`FORCE_TRANSFER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER> "bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER") |   
[`FORCE_UNRESERVE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE> "bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE") |   
[`IF_ELSE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE> "bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE") |   
[`INCREASE_TAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE> "bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE") |   
[`INSTANTIATE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE> "bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE") |   
[`INSTANTIATE_OLD_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT> "bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT") |   
[`INSTANTIATE_WITH_CODE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE> "bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE") |   
[`INSTANTIATE_WITH_CODE_OLD_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT> "bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT") |   
[`KILL_PREFIX`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX> "bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX") |   
[`KILL_PURE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE> "bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE") |   
[`KILL_STORAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_STORAGE> "bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_STORAGE") |   
[`MIGRATE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MIGRATE> "bittensor.extras.dev_framework.calls.non_sudo_calls.MIGRATE") |   
[`MODIFY_POSITION`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION> "bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION") |   
[`MOVE_STAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE> "bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE") |   
[`NOTE_PREIMAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE") |   
[`NOTE_STALLED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED> "bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED") |   
[`POKE_DEPOSIT`](<#id8> "bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT") |   
[`POKE_DEPOSIT`](<#id8> "bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT") |   
[`PROXY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY> "bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY") |   
[`PROXY_ANNOUNCED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED> "bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED") |   
[`RECYCLE_ALPHA`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA> "bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA") |   
[`REFUND`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REFUND> "bittensor.extras.dev_framework.calls.non_sudo_calls.REFUND") |   
[`REGISTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER> "bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER") |   
[`REGISTER_LEASED_NETWORK`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK> "bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK") |   
[`REGISTER_LIMIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT> "bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT") |   
[`REGISTER_NETWORK`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK> "bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK") |   
[`REGISTER_NETWORK_WITH_IDENTITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY> "bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY") |   
[`REJECT_ANNOUNCEMENT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT> "bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT") |   
[`RELEASE_DEPOSIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT> "bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT") |   
[`REMARK`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK> "bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK") |   
[`REMARK_WITH_EVENT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK_WITH_EVENT> "bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK_WITH_EVENT") |   
[`REMOVE_ANNOUNCEMENT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT> "bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT") |   
[`REMOVE_CODE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_CODE> "bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_CODE") |   
[`REMOVE_KEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_KEY> "bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_KEY") |   
[`REMOVE_LIQUIDITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY> "bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY") |   
[`REMOVE_PROXIES`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXIES> "bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXIES") |   
[`REMOVE_PROXY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY> "bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY") |   
[`REMOVE_STAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE> "bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE") |   
[`REMOVE_STAKE_FULL_LIMIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT> "bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT") |   
[`REMOVE_STAKE_LIMIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT> "bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT") |   
[`REPORT_EQUIVOCATION`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION> "bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION") |   
[`REPORT_EQUIVOCATION_UNSIGNED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED> "bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED") |   
[`REQUEST_PREIMAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REQUEST_PREIMAGE> "bittensor.extras.dev_framework.calls.non_sudo_calls.REQUEST_PREIMAGE") |   
[`RESET_COLDKEY_SWAP`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RESET_COLDKEY_SWAP> "bittensor.extras.dev_framework.calls.non_sudo_calls.RESET_COLDKEY_SWAP") |   
[`REVEAL_MECHANISM_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS> "bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS") |   
[`REVEAL_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS> "bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS") |   
[`ROOT_DISSOLVE_NETWORK`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_DISSOLVE_NETWORK> "bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_DISSOLVE_NETWORK") |   
[`ROOT_REGISTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_REGISTER> "bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_REGISTER") |   
[`SCHEDULE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE> "bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE") |   
[`SCHEDULE_AFTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER> "bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER") |   
[`SCHEDULE_GRANDPA_CHANGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE> "bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE") |   
[`SCHEDULE_NAMED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED> "bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED") |   
[`SCHEDULE_NAMED_AFTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER> "bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER") |   
[`SCHEDULE_SWAP_COLDKEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_SWAP_COLDKEY> "bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_SWAP_COLDKEY") |   
[`SERVE_AXON`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON> "bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON") |   
[`SERVE_AXON_TLS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS> "bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS") |   
[`SERVE_PROMETHEUS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS> "bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS") |   
[`SET`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET") |   
[`SET_AUTO_PARENT_DELEGATION_ENABLED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED") |   
[`SET_BASE_FEE_PER_GAS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BASE_FEE_PER_GAS> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BASE_FEE_PER_GAS") |   
[`SET_BEACON_CONFIG`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG") |   
[`SET_CHILDKEY_TAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE") |   
[`SET_CHILDREN`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN") |   
[`SET_CODE`](<#id11> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE") |   
[`SET_CODE`](<#id11> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE") |   
[`SET_CODE_WITHOUT_CHECKS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE_WITHOUT_CHECKS> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE_WITHOUT_CHECKS") |   
[`SET_COLDKEY_AUTO_STAKE_HOTKEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY") |   
[`SET_COMMITMENT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT") |   
[`SET_ELASTICITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ELASTICITY> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ELASTICITY") |   
[`SET_FEE_RATE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE") |   
[`SET_HEAP_PAGES`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_HEAP_PAGES> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_HEAP_PAGES") |   
[`SET_IDENTITY`](<#id14> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY") |   
[`SET_IDENTITY`](<#id14> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY") |   
[`SET_KEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_KEY> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_KEY") |   
[`SET_MAX_EXTRINSIC_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_EXTRINSIC_WEIGHT> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_EXTRINSIC_WEIGHT") |   
[`SET_MAX_PENDING_EXTRINSICS_NUMBER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_PENDING_EXTRINSICS_NUMBER> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_PENDING_EXTRINSICS_NUMBER") |   
[`SET_MAX_SPACE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_SPACE> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_SPACE") |   
[`SET_MECHANISM_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS") |   
[`SET_OLDEST_STORED_ROUND`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_OLDEST_STORED_ROUND> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_OLDEST_STORED_ROUND") |   
[`SET_ON_INITIALIZE_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ON_INITIALIZE_WEIGHT> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ON_INITIALIZE_WEIGHT") |   
[`SET_PENDING_CHILDKEY_COOLDOWN`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_PENDING_CHILDKEY_COOLDOWN> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_PENDING_CHILDKEY_COOLDOWN") |   
[`SET_REAL_PAYS_FEE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE") |   
[`SET_RETRY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY") |   
[`SET_RETRY_NAMED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED") |   
[`SET_ROOT_CLAIM_TYPE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ROOT_CLAIM_TYPE> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ROOT_CLAIM_TYPE") |   
[`SET_STORAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORAGE> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORAGE") |   
[`SET_STORED_EXTRINSIC_LIFETIME`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORED_EXTRINSIC_LIFETIME> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORED_EXTRINSIC_LIFETIME") |   
[`SET_SUBNET_IDENTITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY") |   
[`SET_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS") |   
[`SET_WHITELIST`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WHITELIST> "bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WHITELIST") |   
[`START_CALL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.START_CALL> "bittensor.extras.dev_framework.calls.non_sudo_calls.START_CALL") |   
[`STORE_ENCRYPTED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.STORE_ENCRYPTED> "bittensor.extras.dev_framework.calls.non_sudo_calls.STORE_ENCRYPTED") |   
[`SUBMIT_ENCRYPTED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUBMIT_ENCRYPTED> "bittensor.extras.dev_framework.calls.non_sudo_calls.SUBMIT_ENCRYPTED") |   
[`SUDO`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUDO> "bittensor.extras.dev_framework.calls.non_sudo_calls.SUDO") |   
[`SWAP_AUTHORITIES`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_AUTHORITIES> "bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_AUTHORITIES") |   
[`SWAP_COLDKEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY> "bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY") |   
[`SWAP_COLDKEY_ANNOUNCED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY_ANNOUNCED> "bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY_ANNOUNCED") |   
[`SWAP_HOTKEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY> "bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY") |   
[`SWAP_HOTKEY_V2`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2> "bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2") |   
[`SWAP_STAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE> "bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE") |   
[`SWAP_STAKE_LIMIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT> "bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT") |   
[`TERMINATE_LEASE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE> "bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE") |   
[`TOGGLE_USER_LIQUIDITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY> "bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY") |   
[`TRANSACT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSACT> "bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSACT") |   
[`TRANSFER_ALL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL> "bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL") |   
[`TRANSFER_ALLOW_DEATH`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH> "bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH") |   
[`TRANSFER_KEEP_ALIVE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE> "bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE") |   
[`TRANSFER_STAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE> "bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE") |   
[`TRY_ASSOCIATE_HOTKEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRY_ASSOCIATE_HOTKEY> "bittensor.extras.dev_framework.calls.non_sudo_calls.TRY_ASSOCIATE_HOTKEY") |   
[`UNNOTE_PREIMAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNNOTE_PREIMAGE> "bittensor.extras.dev_framework.calls.non_sudo_calls.UNNOTE_PREIMAGE") |   
[`UNREQUEST_PREIMAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNREQUEST_PREIMAGE> "bittensor.extras.dev_framework.calls.non_sudo_calls.UNREQUEST_PREIMAGE") |   
[`UNSTAKE_ALL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL> "bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL") |   
[`UNSTAKE_ALL_ALPHA`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL_ALPHA> "bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL_ALPHA") |   
[`UPDATE_CAP`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP> "bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP") |   
[`UPDATE_END`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END> "bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END") |   
[`UPDATE_MIN_CONTRIBUTION`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION> "bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION") |   
[`UPDATE_SYMBOL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL> "bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL") |   
[`UPGRADE_ACCOUNTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPGRADE_ACCOUNTS> "bittensor.extras.dev_framework.calls.non_sudo_calls.UPGRADE_ACCOUNTS") |   
[`UPLOAD_CODE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE> "bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE") |   
[`WITHDRAW`](<#id17> "bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW") |   
[`WITHDRAW`](<#id17> "bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW") |   
[`WITH_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT> "bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT") |   
[`WRITE_PULSE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE> "bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE") |   
  
## Module Contents[#](<#module-contents> "Link to this heading")

class bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.hotkey> "Link to this definition")
    

liquidity[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.liquidity> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.pallet> "Link to this definition")
    

tick_high[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.tick_high> "Link to this definition")
    

tick_low[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.tick_low> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

delay[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY.delay> "Link to this definition")
    

delegate[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY.delegate> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY.pallet> "Link to this definition")
    

proxy_type[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY.proxy_type> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

amount_staked[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE.amount_staked> "Link to this definition")
    

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE.hotkey> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

amount[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.amount> "Link to this definition")
    

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.hotkey> "Link to this definition")
    

limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.limit> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

allow_partial[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.allow_partial> "Link to this definition")
    

amount_staked[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.amount_staked> "Link to this definition")
    

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.hotkey> "Link to this definition")
    

limit_price[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.limit_price> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call_hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE.call_hash> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE.pallet> "Link to this definition")
    

real[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE.real> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_COLDKEY_SWAP[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_COLDKEY_SWAP> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

new_coldkey_hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_COLDKEY_SWAP.new_coldkey_hash> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_COLDKEY_SWAP.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_COLDKEY_SWAP.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_NEXT_KEY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_NEXT_KEY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

enc_key[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_NEXT_KEY.enc_key> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_NEXT_KEY.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_NEXT_KEY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.APPLY_AUTHORIZED_UPGRADE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPLY_AUTHORIZED_UPGRADE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

code[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPLY_AUTHORIZED_UPGRADE.code> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPLY_AUTHORIZED_UPGRADE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPLY_AUTHORIZED_UPGRADE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call_hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.call_hash> "Link to this definition")
    

max_weight[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.max_weight> "Link to this definition")
    

maybe_timepoint[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.maybe_timepoint> "Link to this definition")
    

other_signatories[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.other_signatories> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.pallet> "Link to this definition")
    

threshold[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.threshold> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

block_number[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.block_number> "Link to this definition")
    

evm_key[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.evm_key> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.pallet> "Link to this definition")
    

signature[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.signature> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE.call> "Link to this definition")
    

index[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE.index> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.call> "Link to this definition")
    

max_weight[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.max_weight> "Link to this definition")
    

maybe_timepoint[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.maybe_timepoint> "Link to this definition")
    

other_signatories[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.other_signatories> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.pallet> "Link to this definition")
    

threshold[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.threshold> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1.call> "Link to this definition")
    

other_signatories[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1.other_signatories> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

code_hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE.code_hash> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE_WITHOUT_CHECKS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE_WITHOUT_CHECKS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

code_hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE_WITHOUT_CHECKS.code_hash> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE_WITHOUT_CHECKS.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE_WITHOUT_CHECKS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

calls[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH.calls> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_ALL[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_ALL> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

calls[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_ALL.calls> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_ALL.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_ALL.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

commit_hashes[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS.commit_hashes> "Link to this definition")
    

netuids[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS.netuids> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.pallet> "Link to this definition")
    

salts_list[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.salts_list> "Link to this definition")
    

uids_list[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.uids_list> "Link to this definition")
    

values_list[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.values_list> "Link to this definition")
    

version_keys[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.version_keys> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuids[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS.netuids> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS.pallet> "Link to this definition")
    

version_keys[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS.version_keys> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS.wallet> "Link to this definition")
    

weights[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS.weights> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.BURN[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

keep_alive[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN.keep_alive> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN.pallet> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER.hotkey> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

amount[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA.amount> "Link to this definition")
    

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA.hotkey> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CALL[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

data[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.data> "Link to this definition")
    

dest[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.dest> "Link to this definition")
    

gas_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.gas_limit> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.pallet> "Link to this definition")
    

storage_deposit_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.storage_deposit_limit> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CALL[#](<#id0> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

access_list[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.access_list> "Link to this definition")
    

authorization_list[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.authorization_list> "Link to this definition")
    

gas_limit[#](<#id1> "Link to this definition")
    

input[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.input> "Link to this definition")
    

max_fee_per_gas[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.max_fee_per_gas> "Link to this definition")
    

max_priority_fee_per_gas[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.max_priority_fee_per_gas> "Link to this definition")
    

nonce[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.nonce> "Link to this definition")
    

pallet[#](<#id2> "Link to this definition")
    

source[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.source> "Link to this definition")
    

target[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.target> "Link to this definition")
    

value[#](<#id3> "Link to this definition")
    

wallet[#](<#id4> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

data[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.data> "Link to this definition")
    

dest[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.dest> "Link to this definition")
    

gas_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.gas_limit> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.pallet> "Link to this definition")
    

storage_deposit_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.storage_deposit_limit> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

index[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL.index> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL.wallet> "Link to this definition")
    

when[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL.when> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call_hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.call_hash> "Link to this definition")
    

other_signatories[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.other_signatories> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.pallet> "Link to this definition")
    

threshold[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.threshold> "Link to this definition")
    

timepoint[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.timepoint> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_NAMED[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_NAMED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_NAMED.id> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_NAMED.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_NAMED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY.pallet> "Link to this definition")
    

task[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY.task> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY_NAMED[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY_NAMED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY_NAMED.id> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY_NAMED.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY_NAMED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CLAIM_ROOT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLAIM_ROOT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLAIM_ROOT.pallet> "Link to this definition")
    

subnets[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLAIM_ROOT.subnets> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLAIM_ROOT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_COLDKEY_SWAP_ANNOUNCEMENT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_COLDKEY_SWAP_ANNOUNCEMENT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_COLDKEY_SWAP_ANNOUNCEMENT.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_COLDKEY_SWAP_ANNOUNCEMENT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_IDENTITY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_IDENTITY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

identified[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_IDENTITY.identified> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_IDENTITY.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_IDENTITY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

commit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.commit> "Link to this definition")
    

mecid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.mecid> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.pallet> "Link to this definition")
    

reveal_round[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.reveal_round> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

commit_hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS.commit_hash> "Link to this definition")
    

mecid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS.mecid> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

commit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.commit> "Link to this definition")
    

commit_reveal_version[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.commit_reveal_version> "Link to this definition")
    

mecid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.mecid> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.pallet> "Link to this definition")
    

reveal_round[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.reveal_round> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

commit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.commit> "Link to this definition")
    

commit_reveal_version[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.commit_reveal_version> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.pallet> "Link to this definition")
    

reveal_round[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.reveal_round> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

commit_hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS.commit_hash> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

amount[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE.amount> "Link to this definition")
    

crowdloan_id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE.crowdloan_id> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.call> "Link to this definition")
    

cap[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.cap> "Link to this definition")
    

deposit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.deposit> "Link to this definition")
    

end[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.end> "Link to this definition")
    

min_contribution[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.min_contribution> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.pallet> "Link to this definition")
    

target_address[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.target_address> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE[#](<#id5> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

access_list[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.access_list> "Link to this definition")
    

authorization_list[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.authorization_list> "Link to this definition")
    

gas_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.gas_limit> "Link to this definition")
    

init[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.init> "Link to this definition")
    

max_fee_per_gas[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.max_fee_per_gas> "Link to this definition")
    

max_priority_fee_per_gas[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.max_priority_fee_per_gas> "Link to this definition")
    

nonce[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.nonce> "Link to this definition")
    

pallet[#](<#id6> "Link to this definition")
    

source[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.source> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.value> "Link to this definition")
    

wallet[#](<#id7> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

access_list[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.access_list> "Link to this definition")
    

authorization_list[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.authorization_list> "Link to this definition")
    

gas_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.gas_limit> "Link to this definition")
    

init[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.init> "Link to this definition")
    

max_fee_per_gas[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.max_fee_per_gas> "Link to this definition")
    

max_priority_fee_per_gas[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.max_priority_fee_per_gas> "Link to this definition")
    

nonce[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.nonce> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.pallet> "Link to this definition")
    

salt[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.salt> "Link to this definition")
    

source[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.source> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

delay[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE.delay> "Link to this definition")
    

index[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE.index> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE.pallet> "Link to this definition")
    

proxy_type[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE.proxy_type> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE.hotkey> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE.pallet> "Link to this definition")
    

take[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE.take> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_LP[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_LP> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_LP.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_LP.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_VOTING_POWER_TRACKING[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_VOTING_POWER_TRACKING> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_VOTING_POWER_TRACKING.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_VOTING_POWER_TRACKING.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_VOTING_POWER_TRACKING.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_WHITELIST[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_WHITELIST> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

disabled[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_WHITELIST.disabled> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_WHITELIST.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_WHITELIST.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

as_origin[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS.as_origin> "Link to this definition")
    

call[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS.call> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

as_origin[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE.as_origin> "Link to this definition")
    

call[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE.call> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.DISPUTE_COLDKEY_SWAP[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPUTE_COLDKEY_SWAP> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPUTE_COLDKEY_SWAP.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPUTE_COLDKEY_SWAP.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

crowdloan_id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE.crowdloan_id> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

coldkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK.coldkey> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.ENABLE_VOTING_POWER_TRACKING[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENABLE_VOTING_POWER_TRACKING> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENABLE_VOTING_POWER_TRACKING.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENABLE_VOTING_POWER_TRACKING.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENABLE_VOTING_POWER_TRACKING.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.ENSURE_UPDATED[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENSURE_UPDATED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hashes[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENSURE_UPDATED.hashes> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENSURE_UPDATED.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENSURE_UPDATED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.ENTER[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENTER> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENTER.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENTER.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.EXTEND[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.EXTEND> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.EXTEND.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.EXTEND.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

block_number[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET.block_number> "Link to this definition")
    

nonce[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET.nonce> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET.wallet> "Link to this definition")
    

work[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET.work> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.FINALIZE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FINALIZE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

crowdloan_id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FINALIZE.crowdloan_id> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FINALIZE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FINALIZE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

delta[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE.delta> "Link to this definition")
    

direction[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE.direction> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_BATCH[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_BATCH> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

calls[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_BATCH.calls> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_BATCH.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_BATCH.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ENTER[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ENTER> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ENTER.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ENTER.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXIT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXIT.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXTEND[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXTEND> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXTEND.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXTEND.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

account[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT.account> "Link to this definition")
    

block[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT.block> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

new_free[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE.new_free> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE.wallet> "Link to this definition")
    

who[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE.who> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

account[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT.account> "Link to this definition")
    

block[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT.block> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

dest[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER.dest> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER.pallet> "Link to this definition")
    

source[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER.source> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

amount[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE.amount> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE.wallet> "Link to this definition")
    

who[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE.who> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

fallback[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE.fallback> "Link to this definition")
    

main[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE.main> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE.hotkey> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE.pallet> "Link to this definition")
    

take[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE.take> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

code_hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.code_hash> "Link to this definition")
    

data[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.data> "Link to this definition")
    

gas_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.gas_limit> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.pallet> "Link to this definition")
    

salt[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.salt> "Link to this definition")
    

storage_deposit_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.storage_deposit_limit> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

code_hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.code_hash> "Link to this definition")
    

data[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.data> "Link to this definition")
    

gas_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.gas_limit> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.pallet> "Link to this definition")
    

salt[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.salt> "Link to this definition")
    

storage_deposit_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.storage_deposit_limit> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

code[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.code> "Link to this definition")
    

data[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.data> "Link to this definition")
    

gas_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.gas_limit> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.pallet> "Link to this definition")
    

salt[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.salt> "Link to this definition")
    

storage_deposit_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.storage_deposit_limit> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

code[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.code> "Link to this definition")
    

data[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.data> "Link to this definition")
    

gas_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.gas_limit> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.pallet> "Link to this definition")
    

salt[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.salt> "Link to this definition")
    

storage_deposit_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.storage_deposit_limit> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX.pallet> "Link to this definition")
    

prefix[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX.prefix> "Link to this definition")
    

subkeys[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX.subkeys> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

ext_index[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.ext_index> "Link to this definition")
    

height[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.height> "Link to this definition")
    

index[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.index> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.pallet> "Link to this definition")
    

proxy_type[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.proxy_type> "Link to this definition")
    

spawner[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.spawner> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_STORAGE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_STORAGE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

keys[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_STORAGE.keys> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_STORAGE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_STORAGE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.MIGRATE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MIGRATE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MIGRATE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MIGRATE.wallet> "Link to this definition")
    

weight_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MIGRATE.weight_limit> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.hotkey> "Link to this definition")
    

liquidity_delta[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.liquidity_delta> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.pallet> "Link to this definition")
    

position_id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.position_id> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

alpha_amount[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.alpha_amount> "Link to this definition")
    

destination_hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.destination_hotkey> "Link to this definition")
    

destination_netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.destination_netuid> "Link to this definition")
    

origin_hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.origin_hotkey> "Link to this definition")
    

origin_netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.origin_netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

bytes[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

best_finalized_block_number[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED.best_finalized_block_number> "Link to this definition")
    

delay[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED.delay> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call_hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT.call_hash> "Link to this definition")
    

other_signatories[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT.other_signatories> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT.pallet> "Link to this definition")
    

threshold[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT.threshold> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT[#](<#id8> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#id9> "Link to this definition")
    

wallet[#](<#id10> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY.call> "Link to this definition")
    

force_proxy_type[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY.force_proxy_type> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY.pallet> "Link to this definition")
    

real[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY.real> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.call> "Link to this definition")
    

delegate[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.delegate> "Link to this definition")
    

force_proxy_type[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.force_proxy_type> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.pallet> "Link to this definition")
    

real[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.real> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

amount[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA.amount> "Link to this definition")
    

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA.hotkey> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REFUND[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REFUND> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

crowdloan_id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REFUND.crowdloan_id> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REFUND.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REFUND.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

block_number[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.block_number> "Link to this definition")
    

coldkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.coldkey> "Link to this definition")
    

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.hotkey> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.netuid> "Link to this definition")
    

nonce[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.nonce> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.wallet> "Link to this definition")
    

work[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.work> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

emissions_share[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK.emissions_share> "Link to this definition")
    

end_block[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK.end_block> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT.hotkey> "Link to this definition")
    

limit_price[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT.limit_price> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK.hotkey> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY.hotkey> "Link to this definition")
    

identity[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY.identity> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call_hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT.call_hash> "Link to this definition")
    

delegate[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT.delegate> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

account[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT.account> "Link to this definition")
    

block[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT.block> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK.pallet> "Link to this definition")
    

remark[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK.remark> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK_WITH_EVENT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK_WITH_EVENT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK_WITH_EVENT.pallet> "Link to this definition")
    

remark[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK_WITH_EVENT.remark> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK_WITH_EVENT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call_hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT.call_hash> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT.pallet> "Link to this definition")
    

real[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT.real> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_CODE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_CODE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

code_hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_CODE.code_hash> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_CODE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_CODE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_KEY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_KEY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_KEY.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_KEY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY.hotkey> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY.pallet> "Link to this definition")
    

position_id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY.position_id> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXIES[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXIES> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXIES.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXIES.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

delay[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY.delay> "Link to this definition")
    

delegate[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY.delegate> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY.pallet> "Link to this definition")
    

proxy_type[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY.proxy_type> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

amount_unstaked[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE.amount_unstaked> "Link to this definition")
    

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE.hotkey> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT.hotkey> "Link to this definition")
    

limit_price[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT.limit_price> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

allow_partial[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.allow_partial> "Link to this definition")
    

amount_unstaked[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.amount_unstaked> "Link to this definition")
    

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.hotkey> "Link to this definition")
    

limit_price[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.limit_price> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

equivocation_proof[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION.equivocation_proof> "Link to this definition")
    

key_owner_proof[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION.key_owner_proof> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

equivocation_proof[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED.equivocation_proof> "Link to this definition")
    

key_owner_proof[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED.key_owner_proof> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REQUEST_PREIMAGE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REQUEST_PREIMAGE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REQUEST_PREIMAGE.hash> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REQUEST_PREIMAGE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REQUEST_PREIMAGE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.RESET_COLDKEY_SWAP[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RESET_COLDKEY_SWAP> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

coldkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RESET_COLDKEY_SWAP.coldkey> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RESET_COLDKEY_SWAP.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RESET_COLDKEY_SWAP.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

mecid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.mecid> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.pallet> "Link to this definition")
    

salt[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.salt> "Link to this definition")
    

uids[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.uids> "Link to this definition")
    

values[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.values> "Link to this definition")
    

version_key[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.version_key> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.pallet> "Link to this definition")
    

salt[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.salt> "Link to this definition")
    

uids[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.uids> "Link to this definition")
    

values[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.values> "Link to this definition")
    

version_key[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.version_key> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_DISSOLVE_NETWORK[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_DISSOLVE_NETWORK> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_DISSOLVE_NETWORK.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_DISSOLVE_NETWORK.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_DISSOLVE_NETWORK.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_REGISTER[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_REGISTER> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_REGISTER.hotkey> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_REGISTER.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_REGISTER.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.call> "Link to this definition")
    

maybe_periodic[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.maybe_periodic> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.pallet> "Link to this definition")
    

priority[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.priority> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.wallet> "Link to this definition")
    

when[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.when> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

after[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.after> "Link to this definition")
    

call[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.call> "Link to this definition")
    

maybe_periodic[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.maybe_periodic> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.pallet> "Link to this definition")
    

priority[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.priority> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

forced[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE.forced> "Link to this definition")
    

in_blocks[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE.in_blocks> "Link to this definition")
    

next_authorities[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE.next_authorities> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.call> "Link to this definition")
    

id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.id> "Link to this definition")
    

maybe_periodic[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.maybe_periodic> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.pallet> "Link to this definition")
    

priority[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.priority> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.wallet> "Link to this definition")
    

when[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.when> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

after[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.after> "Link to this definition")
    

call[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.call> "Link to this definition")
    

id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.id> "Link to this definition")
    

maybe_periodic[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.maybe_periodic> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.pallet> "Link to this definition")
    

priority[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.priority> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_SWAP_COLDKEY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_SWAP_COLDKEY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

new_coldkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_SWAP_COLDKEY.new_coldkey> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_SWAP_COLDKEY.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_SWAP_COLDKEY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

ip[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.ip> "Link to this definition")
    

ip_type[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.ip_type> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.pallet> "Link to this definition")
    

placeholder1[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.placeholder1> "Link to this definition")
    

placeholder2[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.placeholder2> "Link to this definition")
    

port[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.port> "Link to this definition")
    

protocol[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.protocol> "Link to this definition")
    

version[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.version> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

certificate[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.certificate> "Link to this definition")
    

ip[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.ip> "Link to this definition")
    

ip_type[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.ip_type> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.pallet> "Link to this definition")
    

placeholder1[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.placeholder1> "Link to this definition")
    

placeholder2[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.placeholder2> "Link to this definition")
    

port[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.port> "Link to this definition")
    

protocol[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.protocol> "Link to this definition")
    

version[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.version> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

ip[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.ip> "Link to this definition")
    

ip_type[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.ip_type> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.pallet> "Link to this definition")
    

port[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.port> "Link to this definition")
    

version[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.version> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

now[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET.now> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

enabled[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED.enabled> "Link to this definition")
    

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED.hotkey> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BASE_FEE_PER_GAS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BASE_FEE_PER_GAS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

fee[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BASE_FEE_PER_GAS.fee> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BASE_FEE_PER_GAS.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BASE_FEE_PER_GAS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

config_payload[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG.config_payload> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG.pallet> "Link to this definition")
    

signature[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG.signature> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE.hotkey> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE.pallet> "Link to this definition")
    

take[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE.take> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

children[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN.children> "Link to this definition")
    

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN.hotkey> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

code[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE.code> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE[#](<#id11> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

code_hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE.code_hash> "Link to this definition")
    

dest[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE.dest> "Link to this definition")
    

pallet[#](<#id12> "Link to this definition")
    

wallet[#](<#id13> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE_WITHOUT_CHECKS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE_WITHOUT_CHECKS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

code[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE_WITHOUT_CHECKS.code> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE_WITHOUT_CHECKS.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE_WITHOUT_CHECKS.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY.hotkey> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

info[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT.info> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ELASTICITY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ELASTICITY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

elasticity[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ELASTICITY.elasticity> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ELASTICITY.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ELASTICITY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE.pallet> "Link to this definition")
    

rate[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE.rate> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_HEAP_PAGES[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_HEAP_PAGES> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pages[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_HEAP_PAGES.pages> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_HEAP_PAGES.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_HEAP_PAGES.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

identified[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.identified> "Link to this definition")
    

info[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.info> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY[#](<#id14> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

additional[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.additional> "Link to this definition")
    

description[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.description> "Link to this definition")
    

discord[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.discord> "Link to this definition")
    

github_repo[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.github_repo> "Link to this definition")
    

image[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.image> "Link to this definition")
    

name[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.name> "Link to this definition")
    

pallet[#](<#id15> "Link to this definition")
    

url[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.url> "Link to this definition")
    

wallet[#](<#id16> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_KEY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_KEY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

new[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_KEY.new> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_KEY.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_KEY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_EXTRINSIC_WEIGHT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_EXTRINSIC_WEIGHT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_EXTRINSIC_WEIGHT.pallet> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_EXTRINSIC_WEIGHT.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_EXTRINSIC_WEIGHT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_PENDING_EXTRINSICS_NUMBER[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_PENDING_EXTRINSICS_NUMBER> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_PENDING_EXTRINSICS_NUMBER.pallet> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_PENDING_EXTRINSICS_NUMBER.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_PENDING_EXTRINSICS_NUMBER.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_SPACE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_SPACE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

new_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_SPACE.new_limit> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_SPACE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_SPACE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

dests[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.dests> "Link to this definition")
    

mecid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.mecid> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.pallet> "Link to this definition")
    

version_key[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.version_key> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.wallet> "Link to this definition")
    

weights[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.weights> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_OLDEST_STORED_ROUND[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_OLDEST_STORED_ROUND> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

oldest_round[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_OLDEST_STORED_ROUND.oldest_round> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_OLDEST_STORED_ROUND.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_OLDEST_STORED_ROUND.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ON_INITIALIZE_WEIGHT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ON_INITIALIZE_WEIGHT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ON_INITIALIZE_WEIGHT.pallet> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ON_INITIALIZE_WEIGHT.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ON_INITIALIZE_WEIGHT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_PENDING_CHILDKEY_COOLDOWN[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_PENDING_CHILDKEY_COOLDOWN> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

cooldown[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_PENDING_CHILDKEY_COOLDOWN.cooldown> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_PENDING_CHILDKEY_COOLDOWN.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_PENDING_CHILDKEY_COOLDOWN.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

delegate[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE.delegate> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE.pallet> "Link to this definition")
    

pays_fee[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE.pays_fee> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY.pallet> "Link to this definition")
    

period[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY.period> "Link to this definition")
    

retries[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY.retries> "Link to this definition")
    

task[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY.task> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED.id> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED.pallet> "Link to this definition")
    

period[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED.period> "Link to this definition")
    

retries[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED.retries> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ROOT_CLAIM_TYPE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ROOT_CLAIM_TYPE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

new_root_claim_type[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ROOT_CLAIM_TYPE.new_root_claim_type> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ROOT_CLAIM_TYPE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ROOT_CLAIM_TYPE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORAGE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORAGE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

items[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORAGE.items> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORAGE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORAGE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORED_EXTRINSIC_LIFETIME[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORED_EXTRINSIC_LIFETIME> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORED_EXTRINSIC_LIFETIME.pallet> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORED_EXTRINSIC_LIFETIME.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORED_EXTRINSIC_LIFETIME.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

additional[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.additional> "Link to this definition")
    

description[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.description> "Link to this definition")
    

discord[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.discord> "Link to this definition")
    

github_repo[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.github_repo> "Link to this definition")
    

logo_url[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.logo_url> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.pallet> "Link to this definition")
    

subnet_contact[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.subnet_contact> "Link to this definition")
    

subnet_name[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.subnet_name> "Link to this definition")
    

subnet_url[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.subnet_url> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

dests[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.dests> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.pallet> "Link to this definition")
    

version_key[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.version_key> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.wallet> "Link to this definition")
    

weights[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.weights> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WHITELIST[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WHITELIST> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

new[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WHITELIST.new> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WHITELIST.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WHITELIST.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.START_CALL[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.START_CALL> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.START_CALL.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.START_CALL.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.START_CALL.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.STORE_ENCRYPTED[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.STORE_ENCRYPTED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

encrypted_call[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.STORE_ENCRYPTED.encrypted_call> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.STORE_ENCRYPTED.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.STORE_ENCRYPTED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SUBMIT_ENCRYPTED[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUBMIT_ENCRYPTED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

ciphertext[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUBMIT_ENCRYPTED.ciphertext> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUBMIT_ENCRYPTED.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUBMIT_ENCRYPTED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SUDO[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUDO> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUDO.call> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUDO.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUDO.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_AUTHORITIES[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_AUTHORITIES> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

new_authorities[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_AUTHORITIES.new_authorities> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_AUTHORITIES.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_AUTHORITIES.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

new_coldkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY.new_coldkey> "Link to this definition")
    

old_coldkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY.old_coldkey> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY.pallet> "Link to this definition")
    

swap_cost[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY.swap_cost> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY_ANNOUNCED[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY_ANNOUNCED> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

new_coldkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY_ANNOUNCED.new_coldkey> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY_ANNOUNCED.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY_ANNOUNCED.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY.hotkey> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY.netuid> "Link to this definition")
    

new_hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY.new_hotkey> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.hotkey> "Link to this definition")
    

keep_stake[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.keep_stake> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.netuid> "Link to this definition")
    

new_hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.new_hotkey> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

alpha_amount[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.alpha_amount> "Link to this definition")
    

destination_netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.destination_netuid> "Link to this definition")
    

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.hotkey> "Link to this definition")
    

origin_netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.origin_netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

allow_partial[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.allow_partial> "Link to this definition")
    

alpha_amount[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.alpha_amount> "Link to this definition")
    

destination_netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.destination_netuid> "Link to this definition")
    

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.hotkey> "Link to this definition")
    

limit_price[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.limit_price> "Link to this definition")
    

origin_netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.origin_netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE.hotkey> "Link to this definition")
    

lease_id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE.lease_id> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

enable[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY.enable> "Link to this definition")
    

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSACT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSACT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSACT.pallet> "Link to this definition")
    

transaction[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSACT.transaction> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSACT.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

dest[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL.dest> "Link to this definition")
    

keep_alive[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL.keep_alive> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

dest[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH.dest> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH.pallet> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

dest[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE.dest> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE.pallet> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

alpha_amount[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.alpha_amount> "Link to this definition")
    

destination_coldkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.destination_coldkey> "Link to this definition")
    

destination_netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.destination_netuid> "Link to this definition")
    

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.hotkey> "Link to this definition")
    

origin_netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.origin_netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.TRY_ASSOCIATE_HOTKEY[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRY_ASSOCIATE_HOTKEY> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRY_ASSOCIATE_HOTKEY.hotkey> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRY_ASSOCIATE_HOTKEY.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRY_ASSOCIATE_HOTKEY.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.UNNOTE_PREIMAGE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNNOTE_PREIMAGE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNNOTE_PREIMAGE.hash> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNNOTE_PREIMAGE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNNOTE_PREIMAGE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.UNREQUEST_PREIMAGE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNREQUEST_PREIMAGE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hash[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNREQUEST_PREIMAGE.hash> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNREQUEST_PREIMAGE.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNREQUEST_PREIMAGE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL.hotkey> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL_ALPHA[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL_ALPHA> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

hotkey[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL_ALPHA.hotkey> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL_ALPHA.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL_ALPHA.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

crowdloan_id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP.crowdloan_id> "Link to this definition")
    

new_cap[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP.new_cap> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

crowdloan_id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END.crowdloan_id> "Link to this definition")
    

new_end[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END.new_end> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

crowdloan_id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION.crowdloan_id> "Link to this definition")
    

new_min_contribution[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION.new_min_contribution> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

netuid[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL.netuid> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL.pallet> "Link to this definition")
    

symbol[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL.symbol> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.UPGRADE_ACCOUNTS[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPGRADE_ACCOUNTS> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPGRADE_ACCOUNTS.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPGRADE_ACCOUNTS.wallet> "Link to this definition")
    

who[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPGRADE_ACCOUNTS.who> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

code[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE.code> "Link to this definition")
    

determinism[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE.determinism> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE.pallet> "Link to this definition")
    

storage_deposit_limit[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE.storage_deposit_limit> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

address[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW.address> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW.pallet> "Link to this definition")
    

value[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW.value> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW.wallet> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW[#](<#id17> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

crowdloan_id[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW.crowdloan_id> "Link to this definition")
    

pallet[#](<#id18> "Link to this definition")
    

wallet[#](<#id19> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

call[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT.call> "Link to this definition")
    

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT.pallet> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT.wallet> "Link to this definition")
    

weight[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT.weight> "Link to this definition")
    

class bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE> "Link to this definition")
    

Bases: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple> "\(in Python v3.14\)")

pallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE.pallet> "Link to this definition")
    

pulses_payload[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE.pulses_payload> "Link to this definition")
    

signature[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE.signature> "Link to this definition")
    

wallet[#](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE.wallet> "Link to this definition")
    

[ __ previous bittensor.extras.dev_framework.calls ](<../index.html> "previous page") [ next bittensor.extras.dev_framework.calls.pallets __](<../pallets/index.html> "next page")

__Contents

  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`ADD_LIQUIDITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY>)
      * [`ADD_LIQUIDITY.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.hotkey>)
      * [`ADD_LIQUIDITY.liquidity`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.liquidity>)
      * [`ADD_LIQUIDITY.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.netuid>)
      * [`ADD_LIQUIDITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.pallet>)
      * [`ADD_LIQUIDITY.tick_high`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.tick_high>)
      * [`ADD_LIQUIDITY.tick_low`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.tick_low>)
      * [`ADD_LIQUIDITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_LIQUIDITY.wallet>)
    * [`ADD_PROXY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY>)
      * [`ADD_PROXY.delay`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY.delay>)
      * [`ADD_PROXY.delegate`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY.delegate>)
      * [`ADD_PROXY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY.pallet>)
      * [`ADD_PROXY.proxy_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY.proxy_type>)
      * [`ADD_PROXY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_PROXY.wallet>)
    * [`ADD_STAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE>)
      * [`ADD_STAKE.amount_staked`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE.amount_staked>)
      * [`ADD_STAKE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE.hotkey>)
      * [`ADD_STAKE.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE.netuid>)
      * [`ADD_STAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE.pallet>)
      * [`ADD_STAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE.wallet>)
    * [`ADD_STAKE_BURN`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN>)
      * [`ADD_STAKE_BURN.amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.amount>)
      * [`ADD_STAKE_BURN.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.hotkey>)
      * [`ADD_STAKE_BURN.limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.limit>)
      * [`ADD_STAKE_BURN.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.netuid>)
      * [`ADD_STAKE_BURN.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.pallet>)
      * [`ADD_STAKE_BURN.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_BURN.wallet>)
    * [`ADD_STAKE_LIMIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT>)
      * [`ADD_STAKE_LIMIT.allow_partial`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.allow_partial>)
      * [`ADD_STAKE_LIMIT.amount_staked`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.amount_staked>)
      * [`ADD_STAKE_LIMIT.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.hotkey>)
      * [`ADD_STAKE_LIMIT.limit_price`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.limit_price>)
      * [`ADD_STAKE_LIMIT.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.netuid>)
      * [`ADD_STAKE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.pallet>)
      * [`ADD_STAKE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ADD_STAKE_LIMIT.wallet>)
    * [`ANNOUNCE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE>)
      * [`ANNOUNCE.call_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE.call_hash>)
      * [`ANNOUNCE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE.pallet>)
      * [`ANNOUNCE.real`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE.real>)
      * [`ANNOUNCE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE.wallet>)
    * [`ANNOUNCE_COLDKEY_SWAP`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_COLDKEY_SWAP>)
      * [`ANNOUNCE_COLDKEY_SWAP.new_coldkey_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_COLDKEY_SWAP.new_coldkey_hash>)
      * [`ANNOUNCE_COLDKEY_SWAP.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_COLDKEY_SWAP.pallet>)
      * [`ANNOUNCE_COLDKEY_SWAP.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_COLDKEY_SWAP.wallet>)
    * [`ANNOUNCE_NEXT_KEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_NEXT_KEY>)
      * [`ANNOUNCE_NEXT_KEY.enc_key`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_NEXT_KEY.enc_key>)
      * [`ANNOUNCE_NEXT_KEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_NEXT_KEY.pallet>)
      * [`ANNOUNCE_NEXT_KEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ANNOUNCE_NEXT_KEY.wallet>)
    * [`APPLY_AUTHORIZED_UPGRADE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPLY_AUTHORIZED_UPGRADE>)
      * [`APPLY_AUTHORIZED_UPGRADE.code`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPLY_AUTHORIZED_UPGRADE.code>)
      * [`APPLY_AUTHORIZED_UPGRADE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPLY_AUTHORIZED_UPGRADE.pallet>)
      * [`APPLY_AUTHORIZED_UPGRADE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPLY_AUTHORIZED_UPGRADE.wallet>)
    * [`APPROVE_AS_MULTI`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI>)
      * [`APPROVE_AS_MULTI.call_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.call_hash>)
      * [`APPROVE_AS_MULTI.max_weight`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.max_weight>)
      * [`APPROVE_AS_MULTI.maybe_timepoint`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.maybe_timepoint>)
      * [`APPROVE_AS_MULTI.other_signatories`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.other_signatories>)
      * [`APPROVE_AS_MULTI.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.pallet>)
      * [`APPROVE_AS_MULTI.threshold`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.threshold>)
      * [`APPROVE_AS_MULTI.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.APPROVE_AS_MULTI.wallet>)
    * [`ASSOCIATE_EVM_KEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY>)
      * [`ASSOCIATE_EVM_KEY.block_number`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.block_number>)
      * [`ASSOCIATE_EVM_KEY.evm_key`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.evm_key>)
      * [`ASSOCIATE_EVM_KEY.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.netuid>)
      * [`ASSOCIATE_EVM_KEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.pallet>)
      * [`ASSOCIATE_EVM_KEY.signature`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.signature>)
      * [`ASSOCIATE_EVM_KEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ASSOCIATE_EVM_KEY.wallet>)
    * [`AS_DERIVATIVE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE>)
      * [`AS_DERIVATIVE.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE.call>)
      * [`AS_DERIVATIVE.index`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE.index>)
      * [`AS_DERIVATIVE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE.pallet>)
      * [`AS_DERIVATIVE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_DERIVATIVE.wallet>)
    * [`AS_MULTI`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI>)
      * [`AS_MULTI.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.call>)
      * [`AS_MULTI.max_weight`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.max_weight>)
      * [`AS_MULTI.maybe_timepoint`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.maybe_timepoint>)
      * [`AS_MULTI.other_signatories`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.other_signatories>)
      * [`AS_MULTI.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.pallet>)
      * [`AS_MULTI.threshold`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.threshold>)
      * [`AS_MULTI.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI.wallet>)
    * [`AS_MULTI_THRESHOLD_1`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1>)
      * [`AS_MULTI_THRESHOLD_1.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1.call>)
      * [`AS_MULTI_THRESHOLD_1.other_signatories`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1.other_signatories>)
      * [`AS_MULTI_THRESHOLD_1.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1.pallet>)
      * [`AS_MULTI_THRESHOLD_1.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AS_MULTI_THRESHOLD_1.wallet>)
    * [`AUTHORIZE_UPGRADE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE>)
      * [`AUTHORIZE_UPGRADE.code_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE.code_hash>)
      * [`AUTHORIZE_UPGRADE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE.pallet>)
      * [`AUTHORIZE_UPGRADE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE.wallet>)
    * [`AUTHORIZE_UPGRADE_WITHOUT_CHECKS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE_WITHOUT_CHECKS>)
      * [`AUTHORIZE_UPGRADE_WITHOUT_CHECKS.code_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE_WITHOUT_CHECKS.code_hash>)
      * [`AUTHORIZE_UPGRADE_WITHOUT_CHECKS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE_WITHOUT_CHECKS.pallet>)
      * [`AUTHORIZE_UPGRADE_WITHOUT_CHECKS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.AUTHORIZE_UPGRADE_WITHOUT_CHECKS.wallet>)
    * [`BATCH`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH>)
      * [`BATCH.calls`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH.calls>)
      * [`BATCH.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH.pallet>)
      * [`BATCH.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH.wallet>)
    * [`BATCH_ALL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_ALL>)
      * [`BATCH_ALL.calls`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_ALL.calls>)
      * [`BATCH_ALL.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_ALL.pallet>)
      * [`BATCH_ALL.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_ALL.wallet>)
    * [`BATCH_COMMIT_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS>)
      * [`BATCH_COMMIT_WEIGHTS.commit_hashes`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS.commit_hashes>)
      * [`BATCH_COMMIT_WEIGHTS.netuids`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS.netuids>)
      * [`BATCH_COMMIT_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS.pallet>)
      * [`BATCH_COMMIT_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_COMMIT_WEIGHTS.wallet>)
    * [`BATCH_REVEAL_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS>)
      * [`BATCH_REVEAL_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.netuid>)
      * [`BATCH_REVEAL_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.pallet>)
      * [`BATCH_REVEAL_WEIGHTS.salts_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.salts_list>)
      * [`BATCH_REVEAL_WEIGHTS.uids_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.uids_list>)
      * [`BATCH_REVEAL_WEIGHTS.values_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.values_list>)
      * [`BATCH_REVEAL_WEIGHTS.version_keys`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.version_keys>)
      * [`BATCH_REVEAL_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_REVEAL_WEIGHTS.wallet>)
    * [`BATCH_SET_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS>)
      * [`BATCH_SET_WEIGHTS.netuids`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS.netuids>)
      * [`BATCH_SET_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS.pallet>)
      * [`BATCH_SET_WEIGHTS.version_keys`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS.version_keys>)
      * [`BATCH_SET_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS.wallet>)
      * [`BATCH_SET_WEIGHTS.weights`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BATCH_SET_WEIGHTS.weights>)
    * [`BURN`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN>)
      * [`BURN.keep_alive`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN.keep_alive>)
      * [`BURN.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN.pallet>)
      * [`BURN.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN.value>)
      * [`BURN.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN.wallet>)
    * [`BURNED_REGISTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER>)
      * [`BURNED_REGISTER.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER.hotkey>)
      * [`BURNED_REGISTER.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER.netuid>)
      * [`BURNED_REGISTER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER.pallet>)
      * [`BURNED_REGISTER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURNED_REGISTER.wallet>)
    * [`BURN_ALPHA`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA>)
      * [`BURN_ALPHA.amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA.amount>)
      * [`BURN_ALPHA.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA.hotkey>)
      * [`BURN_ALPHA.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA.netuid>)
      * [`BURN_ALPHA.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA.pallet>)
      * [`BURN_ALPHA.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.BURN_ALPHA.wallet>)
    * [`CALL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL>)
      * [`CALL.data`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.data>)
      * [`CALL.dest`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.dest>)
      * [`CALL.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.gas_limit>)
      * [`CALL.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.pallet>)
      * [`CALL.storage_deposit_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.storage_deposit_limit>)
      * [`CALL.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.value>)
      * [`CALL.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.wallet>)
    * [`CALL`](<#id0>)
      * [`CALL.access_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.access_list>)
      * [`CALL.authorization_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.authorization_list>)
      * [`CALL.gas_limit`](<#id1>)
      * [`CALL.input`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.input>)
      * [`CALL.max_fee_per_gas`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.max_fee_per_gas>)
      * [`CALL.max_priority_fee_per_gas`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.max_priority_fee_per_gas>)
      * [`CALL.nonce`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.nonce>)
      * [`CALL.pallet`](<#id2>)
      * [`CALL.source`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.source>)
      * [`CALL.target`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL.target>)
      * [`CALL.value`](<#id3>)
      * [`CALL.wallet`](<#id4>)
    * [`CALL_OLD_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT>)
      * [`CALL_OLD_WEIGHT.data`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.data>)
      * [`CALL_OLD_WEIGHT.dest`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.dest>)
      * [`CALL_OLD_WEIGHT.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.gas_limit>)
      * [`CALL_OLD_WEIGHT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.pallet>)
      * [`CALL_OLD_WEIGHT.storage_deposit_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.storage_deposit_limit>)
      * [`CALL_OLD_WEIGHT.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.value>)
      * [`CALL_OLD_WEIGHT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CALL_OLD_WEIGHT.wallet>)
    * [`CANCEL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL>)
      * [`CANCEL.index`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL.index>)
      * [`CANCEL.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL.pallet>)
      * [`CANCEL.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL.wallet>)
      * [`CANCEL.when`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL.when>)
    * [`CANCEL_AS_MULTI`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI>)
      * [`CANCEL_AS_MULTI.call_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.call_hash>)
      * [`CANCEL_AS_MULTI.other_signatories`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.other_signatories>)
      * [`CANCEL_AS_MULTI.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.pallet>)
      * [`CANCEL_AS_MULTI.threshold`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.threshold>)
      * [`CANCEL_AS_MULTI.timepoint`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.timepoint>)
      * [`CANCEL_AS_MULTI.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_AS_MULTI.wallet>)
    * [`CANCEL_NAMED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_NAMED>)
      * [`CANCEL_NAMED.id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_NAMED.id>)
      * [`CANCEL_NAMED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_NAMED.pallet>)
      * [`CANCEL_NAMED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_NAMED.wallet>)
    * [`CANCEL_RETRY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY>)
      * [`CANCEL_RETRY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY.pallet>)
      * [`CANCEL_RETRY.task`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY.task>)
      * [`CANCEL_RETRY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY.wallet>)
    * [`CANCEL_RETRY_NAMED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY_NAMED>)
      * [`CANCEL_RETRY_NAMED.id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY_NAMED.id>)
      * [`CANCEL_RETRY_NAMED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY_NAMED.pallet>)
      * [`CANCEL_RETRY_NAMED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CANCEL_RETRY_NAMED.wallet>)
    * [`CLAIM_ROOT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLAIM_ROOT>)
      * [`CLAIM_ROOT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLAIM_ROOT.pallet>)
      * [`CLAIM_ROOT.subnets`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLAIM_ROOT.subnets>)
      * [`CLAIM_ROOT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLAIM_ROOT.wallet>)
    * [`CLEAR_COLDKEY_SWAP_ANNOUNCEMENT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_COLDKEY_SWAP_ANNOUNCEMENT>)
      * [`CLEAR_COLDKEY_SWAP_ANNOUNCEMENT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_COLDKEY_SWAP_ANNOUNCEMENT.pallet>)
      * [`CLEAR_COLDKEY_SWAP_ANNOUNCEMENT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_COLDKEY_SWAP_ANNOUNCEMENT.wallet>)
    * [`CLEAR_IDENTITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_IDENTITY>)
      * [`CLEAR_IDENTITY.identified`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_IDENTITY.identified>)
      * [`CLEAR_IDENTITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_IDENTITY.pallet>)
      * [`CLEAR_IDENTITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CLEAR_IDENTITY.wallet>)
    * [`COMMIT_CRV3_MECHANISM_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS>)
      * [`COMMIT_CRV3_MECHANISM_WEIGHTS.commit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.commit>)
      * [`COMMIT_CRV3_MECHANISM_WEIGHTS.mecid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.mecid>)
      * [`COMMIT_CRV3_MECHANISM_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.netuid>)
      * [`COMMIT_CRV3_MECHANISM_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.pallet>)
      * [`COMMIT_CRV3_MECHANISM_WEIGHTS.reveal_round`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.reveal_round>)
      * [`COMMIT_CRV3_MECHANISM_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_CRV3_MECHANISM_WEIGHTS.wallet>)
    * [`COMMIT_MECHANISM_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS>)
      * [`COMMIT_MECHANISM_WEIGHTS.commit_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS.commit_hash>)
      * [`COMMIT_MECHANISM_WEIGHTS.mecid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS.mecid>)
      * [`COMMIT_MECHANISM_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS.netuid>)
      * [`COMMIT_MECHANISM_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS.pallet>)
      * [`COMMIT_MECHANISM_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_MECHANISM_WEIGHTS.wallet>)
    * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS>)
      * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.commit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.commit>)
      * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.commit_reveal_version`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.commit_reveal_version>)
      * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.mecid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.mecid>)
      * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.netuid>)
      * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.pallet>)
      * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.reveal_round`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.reveal_round>)
      * [`COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_MECHANISM_WEIGHTS.wallet>)
    * [`COMMIT_TIMELOCKED_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS>)
      * [`COMMIT_TIMELOCKED_WEIGHTS.commit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.commit>)
      * [`COMMIT_TIMELOCKED_WEIGHTS.commit_reveal_version`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.commit_reveal_version>)
      * [`COMMIT_TIMELOCKED_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.netuid>)
      * [`COMMIT_TIMELOCKED_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.pallet>)
      * [`COMMIT_TIMELOCKED_WEIGHTS.reveal_round`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.reveal_round>)
      * [`COMMIT_TIMELOCKED_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_TIMELOCKED_WEIGHTS.wallet>)
    * [`COMMIT_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS>)
      * [`COMMIT_WEIGHTS.commit_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS.commit_hash>)
      * [`COMMIT_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS.netuid>)
      * [`COMMIT_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS.pallet>)
      * [`COMMIT_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.COMMIT_WEIGHTS.wallet>)
    * [`CONTRIBUTE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE>)
      * [`CONTRIBUTE.amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE.amount>)
      * [`CONTRIBUTE.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE.crowdloan_id>)
      * [`CONTRIBUTE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE.pallet>)
      * [`CONTRIBUTE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CONTRIBUTE.wallet>)
    * [`CREATE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE>)
      * [`CREATE.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.call>)
      * [`CREATE.cap`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.cap>)
      * [`CREATE.deposit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.deposit>)
      * [`CREATE.end`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.end>)
      * [`CREATE.min_contribution`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.min_contribution>)
      * [`CREATE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.pallet>)
      * [`CREATE.target_address`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.target_address>)
      * [`CREATE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.wallet>)
    * [`CREATE`](<#id5>)
      * [`CREATE.access_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.access_list>)
      * [`CREATE.authorization_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.authorization_list>)
      * [`CREATE.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.gas_limit>)
      * [`CREATE.init`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.init>)
      * [`CREATE.max_fee_per_gas`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.max_fee_per_gas>)
      * [`CREATE.max_priority_fee_per_gas`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.max_priority_fee_per_gas>)
      * [`CREATE.nonce`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.nonce>)
      * [`CREATE.pallet`](<#id6>)
      * [`CREATE.source`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.source>)
      * [`CREATE.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE.value>)
      * [`CREATE.wallet`](<#id7>)
    * [`CREATE2`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2>)
      * [`CREATE2.access_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.access_list>)
      * [`CREATE2.authorization_list`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.authorization_list>)
      * [`CREATE2.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.gas_limit>)
      * [`CREATE2.init`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.init>)
      * [`CREATE2.max_fee_per_gas`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.max_fee_per_gas>)
      * [`CREATE2.max_priority_fee_per_gas`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.max_priority_fee_per_gas>)
      * [`CREATE2.nonce`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.nonce>)
      * [`CREATE2.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.pallet>)
      * [`CREATE2.salt`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.salt>)
      * [`CREATE2.source`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.source>)
      * [`CREATE2.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.value>)
      * [`CREATE2.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE2.wallet>)
    * [`CREATE_PURE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE>)
      * [`CREATE_PURE.delay`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE.delay>)
      * [`CREATE_PURE.index`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE.index>)
      * [`CREATE_PURE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE.pallet>)
      * [`CREATE_PURE.proxy_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE.proxy_type>)
      * [`CREATE_PURE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.CREATE_PURE.wallet>)
    * [`DECREASE_TAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE>)
      * [`DECREASE_TAKE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE.hotkey>)
      * [`DECREASE_TAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE.pallet>)
      * [`DECREASE_TAKE.take`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE.take>)
      * [`DECREASE_TAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DECREASE_TAKE.wallet>)
    * [`DISABLE_LP`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_LP>)
      * [`DISABLE_LP.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_LP.pallet>)
      * [`DISABLE_LP.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_LP.wallet>)
    * [`DISABLE_VOTING_POWER_TRACKING`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_VOTING_POWER_TRACKING>)
      * [`DISABLE_VOTING_POWER_TRACKING.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_VOTING_POWER_TRACKING.netuid>)
      * [`DISABLE_VOTING_POWER_TRACKING.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_VOTING_POWER_TRACKING.pallet>)
      * [`DISABLE_VOTING_POWER_TRACKING.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_VOTING_POWER_TRACKING.wallet>)
    * [`DISABLE_WHITELIST`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_WHITELIST>)
      * [`DISABLE_WHITELIST.disabled`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_WHITELIST.disabled>)
      * [`DISABLE_WHITELIST.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_WHITELIST.pallet>)
      * [`DISABLE_WHITELIST.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISABLE_WHITELIST.wallet>)
    * [`DISPATCH_AS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS>)
      * [`DISPATCH_AS.as_origin`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS.as_origin>)
      * [`DISPATCH_AS.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS.call>)
      * [`DISPATCH_AS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS.pallet>)
      * [`DISPATCH_AS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS.wallet>)
    * [`DISPATCH_AS_FALLIBLE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE>)
      * [`DISPATCH_AS_FALLIBLE.as_origin`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE.as_origin>)
      * [`DISPATCH_AS_FALLIBLE.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE.call>)
      * [`DISPATCH_AS_FALLIBLE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE.pallet>)
      * [`DISPATCH_AS_FALLIBLE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPATCH_AS_FALLIBLE.wallet>)
    * [`DISPUTE_COLDKEY_SWAP`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPUTE_COLDKEY_SWAP>)
      * [`DISPUTE_COLDKEY_SWAP.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPUTE_COLDKEY_SWAP.pallet>)
      * [`DISPUTE_COLDKEY_SWAP.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISPUTE_COLDKEY_SWAP.wallet>)
    * [`DISSOLVE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE>)
      * [`DISSOLVE.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE.crowdloan_id>)
      * [`DISSOLVE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE.pallet>)
      * [`DISSOLVE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE.wallet>)
    * [`DISSOLVE_NETWORK`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK>)
      * [`DISSOLVE_NETWORK.coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK.coldkey>)
      * [`DISSOLVE_NETWORK.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK.netuid>)
      * [`DISSOLVE_NETWORK.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK.pallet>)
      * [`DISSOLVE_NETWORK.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.DISSOLVE_NETWORK.wallet>)
    * [`ENABLE_VOTING_POWER_TRACKING`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENABLE_VOTING_POWER_TRACKING>)
      * [`ENABLE_VOTING_POWER_TRACKING.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENABLE_VOTING_POWER_TRACKING.netuid>)
      * [`ENABLE_VOTING_POWER_TRACKING.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENABLE_VOTING_POWER_TRACKING.pallet>)
      * [`ENABLE_VOTING_POWER_TRACKING.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENABLE_VOTING_POWER_TRACKING.wallet>)
    * [`ENSURE_UPDATED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENSURE_UPDATED>)
      * [`ENSURE_UPDATED.hashes`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENSURE_UPDATED.hashes>)
      * [`ENSURE_UPDATED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENSURE_UPDATED.pallet>)
      * [`ENSURE_UPDATED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENSURE_UPDATED.wallet>)
    * [`ENTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENTER>)
      * [`ENTER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENTER.pallet>)
      * [`ENTER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ENTER.wallet>)
    * [`EXTEND`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.EXTEND>)
      * [`EXTEND.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.EXTEND.pallet>)
      * [`EXTEND.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.EXTEND.wallet>)
    * [`FAUCET`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET>)
      * [`FAUCET.block_number`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET.block_number>)
      * [`FAUCET.nonce`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET.nonce>)
      * [`FAUCET.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET.pallet>)
      * [`FAUCET.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET.wallet>)
      * [`FAUCET.work`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FAUCET.work>)
    * [`FINALIZE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FINALIZE>)
      * [`FINALIZE.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FINALIZE.crowdloan_id>)
      * [`FINALIZE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FINALIZE.pallet>)
      * [`FINALIZE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FINALIZE.wallet>)
    * [`FORCE_ADJUST_TOTAL_ISSUANCE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE>)
      * [`FORCE_ADJUST_TOTAL_ISSUANCE.delta`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE.delta>)
      * [`FORCE_ADJUST_TOTAL_ISSUANCE.direction`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE.direction>)
      * [`FORCE_ADJUST_TOTAL_ISSUANCE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE.pallet>)
      * [`FORCE_ADJUST_TOTAL_ISSUANCE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ADJUST_TOTAL_ISSUANCE.wallet>)
    * [`FORCE_BATCH`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_BATCH>)
      * [`FORCE_BATCH.calls`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_BATCH.calls>)
      * [`FORCE_BATCH.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_BATCH.pallet>)
      * [`FORCE_BATCH.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_BATCH.wallet>)
    * [`FORCE_ENTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ENTER>)
      * [`FORCE_ENTER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ENTER.pallet>)
      * [`FORCE_ENTER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_ENTER.wallet>)
    * [`FORCE_EXIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXIT>)
      * [`FORCE_EXIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXIT.pallet>)
      * [`FORCE_EXIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXIT.wallet>)
    * [`FORCE_EXTEND`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXTEND>)
      * [`FORCE_EXTEND.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXTEND.pallet>)
      * [`FORCE_EXTEND.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_EXTEND.wallet>)
    * [`FORCE_RELEASE_DEPOSIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT>)
      * [`FORCE_RELEASE_DEPOSIT.account`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT.account>)
      * [`FORCE_RELEASE_DEPOSIT.block`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT.block>)
      * [`FORCE_RELEASE_DEPOSIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT.pallet>)
      * [`FORCE_RELEASE_DEPOSIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_RELEASE_DEPOSIT.wallet>)
    * [`FORCE_SET_BALANCE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE>)
      * [`FORCE_SET_BALANCE.new_free`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE.new_free>)
      * [`FORCE_SET_BALANCE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE.pallet>)
      * [`FORCE_SET_BALANCE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE.wallet>)
      * [`FORCE_SET_BALANCE.who`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SET_BALANCE.who>)
    * [`FORCE_SLASH_DEPOSIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT>)
      * [`FORCE_SLASH_DEPOSIT.account`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT.account>)
      * [`FORCE_SLASH_DEPOSIT.block`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT.block>)
      * [`FORCE_SLASH_DEPOSIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT.pallet>)
      * [`FORCE_SLASH_DEPOSIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_SLASH_DEPOSIT.wallet>)
    * [`FORCE_TRANSFER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER>)
      * [`FORCE_TRANSFER.dest`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER.dest>)
      * [`FORCE_TRANSFER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER.pallet>)
      * [`FORCE_TRANSFER.source`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER.source>)
      * [`FORCE_TRANSFER.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER.value>)
      * [`FORCE_TRANSFER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_TRANSFER.wallet>)
    * [`FORCE_UNRESERVE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE>)
      * [`FORCE_UNRESERVE.amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE.amount>)
      * [`FORCE_UNRESERVE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE.pallet>)
      * [`FORCE_UNRESERVE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE.wallet>)
      * [`FORCE_UNRESERVE.who`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.FORCE_UNRESERVE.who>)
    * [`IF_ELSE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE>)
      * [`IF_ELSE.fallback`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE.fallback>)
      * [`IF_ELSE.main`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE.main>)
      * [`IF_ELSE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE.pallet>)
      * [`IF_ELSE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.IF_ELSE.wallet>)
    * [`INCREASE_TAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE>)
      * [`INCREASE_TAKE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE.hotkey>)
      * [`INCREASE_TAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE.pallet>)
      * [`INCREASE_TAKE.take`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE.take>)
      * [`INCREASE_TAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INCREASE_TAKE.wallet>)
    * [`INSTANTIATE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE>)
      * [`INSTANTIATE.code_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.code_hash>)
      * [`INSTANTIATE.data`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.data>)
      * [`INSTANTIATE.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.gas_limit>)
      * [`INSTANTIATE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.pallet>)
      * [`INSTANTIATE.salt`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.salt>)
      * [`INSTANTIATE.storage_deposit_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.storage_deposit_limit>)
      * [`INSTANTIATE.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.value>)
      * [`INSTANTIATE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE.wallet>)
    * [`INSTANTIATE_OLD_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT>)
      * [`INSTANTIATE_OLD_WEIGHT.code_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.code_hash>)
      * [`INSTANTIATE_OLD_WEIGHT.data`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.data>)
      * [`INSTANTIATE_OLD_WEIGHT.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.gas_limit>)
      * [`INSTANTIATE_OLD_WEIGHT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.pallet>)
      * [`INSTANTIATE_OLD_WEIGHT.salt`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.salt>)
      * [`INSTANTIATE_OLD_WEIGHT.storage_deposit_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.storage_deposit_limit>)
      * [`INSTANTIATE_OLD_WEIGHT.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.value>)
      * [`INSTANTIATE_OLD_WEIGHT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_OLD_WEIGHT.wallet>)
    * [`INSTANTIATE_WITH_CODE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE>)
      * [`INSTANTIATE_WITH_CODE.code`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.code>)
      * [`INSTANTIATE_WITH_CODE.data`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.data>)
      * [`INSTANTIATE_WITH_CODE.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.gas_limit>)
      * [`INSTANTIATE_WITH_CODE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.pallet>)
      * [`INSTANTIATE_WITH_CODE.salt`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.salt>)
      * [`INSTANTIATE_WITH_CODE.storage_deposit_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.storage_deposit_limit>)
      * [`INSTANTIATE_WITH_CODE.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.value>)
      * [`INSTANTIATE_WITH_CODE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE.wallet>)
    * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.code`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.code>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.data`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.data>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.gas_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.gas_limit>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.pallet>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.salt`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.salt>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.storage_deposit_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.storage_deposit_limit>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.value>)
      * [`INSTANTIATE_WITH_CODE_OLD_WEIGHT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.INSTANTIATE_WITH_CODE_OLD_WEIGHT.wallet>)
    * [`KILL_PREFIX`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX>)
      * [`KILL_PREFIX.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX.pallet>)
      * [`KILL_PREFIX.prefix`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX.prefix>)
      * [`KILL_PREFIX.subkeys`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX.subkeys>)
      * [`KILL_PREFIX.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PREFIX.wallet>)
    * [`KILL_PURE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE>)
      * [`KILL_PURE.ext_index`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.ext_index>)
      * [`KILL_PURE.height`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.height>)
      * [`KILL_PURE.index`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.index>)
      * [`KILL_PURE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.pallet>)
      * [`KILL_PURE.proxy_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.proxy_type>)
      * [`KILL_PURE.spawner`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.spawner>)
      * [`KILL_PURE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_PURE.wallet>)
    * [`KILL_STORAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_STORAGE>)
      * [`KILL_STORAGE.keys`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_STORAGE.keys>)
      * [`KILL_STORAGE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_STORAGE.pallet>)
      * [`KILL_STORAGE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.KILL_STORAGE.wallet>)
    * [`MIGRATE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MIGRATE>)
      * [`MIGRATE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MIGRATE.pallet>)
      * [`MIGRATE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MIGRATE.wallet>)
      * [`MIGRATE.weight_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MIGRATE.weight_limit>)
    * [`MODIFY_POSITION`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION>)
      * [`MODIFY_POSITION.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.hotkey>)
      * [`MODIFY_POSITION.liquidity_delta`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.liquidity_delta>)
      * [`MODIFY_POSITION.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.netuid>)
      * [`MODIFY_POSITION.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.pallet>)
      * [`MODIFY_POSITION.position_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.position_id>)
      * [`MODIFY_POSITION.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MODIFY_POSITION.wallet>)
    * [`MOVE_STAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE>)
      * [`MOVE_STAKE.alpha_amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.alpha_amount>)
      * [`MOVE_STAKE.destination_hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.destination_hotkey>)
      * [`MOVE_STAKE.destination_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.destination_netuid>)
      * [`MOVE_STAKE.origin_hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.origin_hotkey>)
      * [`MOVE_STAKE.origin_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.origin_netuid>)
      * [`MOVE_STAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.pallet>)
      * [`MOVE_STAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.MOVE_STAKE.wallet>)
    * [`NOTE_PREIMAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE>)
      * [`NOTE_PREIMAGE.bytes`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.bytes>)
      * [`NOTE_PREIMAGE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.pallet>)
      * [`NOTE_PREIMAGE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_PREIMAGE.wallet>)
    * [`NOTE_STALLED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED>)
      * [`NOTE_STALLED.best_finalized_block_number`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED.best_finalized_block_number>)
      * [`NOTE_STALLED.delay`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED.delay>)
      * [`NOTE_STALLED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED.pallet>)
      * [`NOTE_STALLED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.NOTE_STALLED.wallet>)
    * [`POKE_DEPOSIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT>)
      * [`POKE_DEPOSIT.call_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT.call_hash>)
      * [`POKE_DEPOSIT.other_signatories`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT.other_signatories>)
      * [`POKE_DEPOSIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT.pallet>)
      * [`POKE_DEPOSIT.threshold`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT.threshold>)
      * [`POKE_DEPOSIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.POKE_DEPOSIT.wallet>)
    * [`POKE_DEPOSIT`](<#id8>)
      * [`POKE_DEPOSIT.pallet`](<#id9>)
      * [`POKE_DEPOSIT.wallet`](<#id10>)
    * [`PROXY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY>)
      * [`PROXY.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY.call>)
      * [`PROXY.force_proxy_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY.force_proxy_type>)
      * [`PROXY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY.pallet>)
      * [`PROXY.real`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY.real>)
      * [`PROXY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY.wallet>)
    * [`PROXY_ANNOUNCED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED>)
      * [`PROXY_ANNOUNCED.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.call>)
      * [`PROXY_ANNOUNCED.delegate`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.delegate>)
      * [`PROXY_ANNOUNCED.force_proxy_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.force_proxy_type>)
      * [`PROXY_ANNOUNCED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.pallet>)
      * [`PROXY_ANNOUNCED.real`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.real>)
      * [`PROXY_ANNOUNCED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.PROXY_ANNOUNCED.wallet>)
    * [`RECYCLE_ALPHA`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA>)
      * [`RECYCLE_ALPHA.amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA.amount>)
      * [`RECYCLE_ALPHA.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA.hotkey>)
      * [`RECYCLE_ALPHA.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA.netuid>)
      * [`RECYCLE_ALPHA.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA.pallet>)
      * [`RECYCLE_ALPHA.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RECYCLE_ALPHA.wallet>)
    * [`REFUND`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REFUND>)
      * [`REFUND.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REFUND.crowdloan_id>)
      * [`REFUND.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REFUND.pallet>)
      * [`REFUND.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REFUND.wallet>)
    * [`REGISTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER>)
      * [`REGISTER.block_number`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.block_number>)
      * [`REGISTER.coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.coldkey>)
      * [`REGISTER.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.hotkey>)
      * [`REGISTER.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.netuid>)
      * [`REGISTER.nonce`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.nonce>)
      * [`REGISTER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.pallet>)
      * [`REGISTER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.wallet>)
      * [`REGISTER.work`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER.work>)
    * [`REGISTER_LEASED_NETWORK`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK>)
      * [`REGISTER_LEASED_NETWORK.emissions_share`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK.emissions_share>)
      * [`REGISTER_LEASED_NETWORK.end_block`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK.end_block>)
      * [`REGISTER_LEASED_NETWORK.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK.pallet>)
      * [`REGISTER_LEASED_NETWORK.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LEASED_NETWORK.wallet>)
    * [`REGISTER_LIMIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT>)
      * [`REGISTER_LIMIT.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT.hotkey>)
      * [`REGISTER_LIMIT.limit_price`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT.limit_price>)
      * [`REGISTER_LIMIT.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT.netuid>)
      * [`REGISTER_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT.pallet>)
      * [`REGISTER_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_LIMIT.wallet>)
    * [`REGISTER_NETWORK`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK>)
      * [`REGISTER_NETWORK.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK.hotkey>)
      * [`REGISTER_NETWORK.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK.pallet>)
      * [`REGISTER_NETWORK.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK.wallet>)
    * [`REGISTER_NETWORK_WITH_IDENTITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY>)
      * [`REGISTER_NETWORK_WITH_IDENTITY.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY.hotkey>)
      * [`REGISTER_NETWORK_WITH_IDENTITY.identity`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY.identity>)
      * [`REGISTER_NETWORK_WITH_IDENTITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY.pallet>)
      * [`REGISTER_NETWORK_WITH_IDENTITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REGISTER_NETWORK_WITH_IDENTITY.wallet>)
    * [`REJECT_ANNOUNCEMENT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT>)
      * [`REJECT_ANNOUNCEMENT.call_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT.call_hash>)
      * [`REJECT_ANNOUNCEMENT.delegate`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT.delegate>)
      * [`REJECT_ANNOUNCEMENT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT.pallet>)
      * [`REJECT_ANNOUNCEMENT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REJECT_ANNOUNCEMENT.wallet>)
    * [`RELEASE_DEPOSIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT>)
      * [`RELEASE_DEPOSIT.account`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT.account>)
      * [`RELEASE_DEPOSIT.block`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT.block>)
      * [`RELEASE_DEPOSIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT.pallet>)
      * [`RELEASE_DEPOSIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RELEASE_DEPOSIT.wallet>)
    * [`REMARK`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK>)
      * [`REMARK.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK.pallet>)
      * [`REMARK.remark`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK.remark>)
      * [`REMARK.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK.wallet>)
    * [`REMARK_WITH_EVENT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK_WITH_EVENT>)
      * [`REMARK_WITH_EVENT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK_WITH_EVENT.pallet>)
      * [`REMARK_WITH_EVENT.remark`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK_WITH_EVENT.remark>)
      * [`REMARK_WITH_EVENT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMARK_WITH_EVENT.wallet>)
    * [`REMOVE_ANNOUNCEMENT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT>)
      * [`REMOVE_ANNOUNCEMENT.call_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT.call_hash>)
      * [`REMOVE_ANNOUNCEMENT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT.pallet>)
      * [`REMOVE_ANNOUNCEMENT.real`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT.real>)
      * [`REMOVE_ANNOUNCEMENT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_ANNOUNCEMENT.wallet>)
    * [`REMOVE_CODE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_CODE>)
      * [`REMOVE_CODE.code_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_CODE.code_hash>)
      * [`REMOVE_CODE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_CODE.pallet>)
      * [`REMOVE_CODE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_CODE.wallet>)
    * [`REMOVE_KEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_KEY>)
      * [`REMOVE_KEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_KEY.pallet>)
      * [`REMOVE_KEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_KEY.wallet>)
    * [`REMOVE_LIQUIDITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY>)
      * [`REMOVE_LIQUIDITY.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY.hotkey>)
      * [`REMOVE_LIQUIDITY.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY.netuid>)
      * [`REMOVE_LIQUIDITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY.pallet>)
      * [`REMOVE_LIQUIDITY.position_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY.position_id>)
      * [`REMOVE_LIQUIDITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_LIQUIDITY.wallet>)
    * [`REMOVE_PROXIES`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXIES>)
      * [`REMOVE_PROXIES.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXIES.pallet>)
      * [`REMOVE_PROXIES.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXIES.wallet>)
    * [`REMOVE_PROXY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY>)
      * [`REMOVE_PROXY.delay`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY.delay>)
      * [`REMOVE_PROXY.delegate`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY.delegate>)
      * [`REMOVE_PROXY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY.pallet>)
      * [`REMOVE_PROXY.proxy_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY.proxy_type>)
      * [`REMOVE_PROXY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_PROXY.wallet>)
    * [`REMOVE_STAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE>)
      * [`REMOVE_STAKE.amount_unstaked`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE.amount_unstaked>)
      * [`REMOVE_STAKE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE.hotkey>)
      * [`REMOVE_STAKE.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE.netuid>)
      * [`REMOVE_STAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE.pallet>)
      * [`REMOVE_STAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE.wallet>)
    * [`REMOVE_STAKE_FULL_LIMIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT>)
      * [`REMOVE_STAKE_FULL_LIMIT.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT.hotkey>)
      * [`REMOVE_STAKE_FULL_LIMIT.limit_price`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT.limit_price>)
      * [`REMOVE_STAKE_FULL_LIMIT.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT.netuid>)
      * [`REMOVE_STAKE_FULL_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT.pallet>)
      * [`REMOVE_STAKE_FULL_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_FULL_LIMIT.wallet>)
    * [`REMOVE_STAKE_LIMIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT>)
      * [`REMOVE_STAKE_LIMIT.allow_partial`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.allow_partial>)
      * [`REMOVE_STAKE_LIMIT.amount_unstaked`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.amount_unstaked>)
      * [`REMOVE_STAKE_LIMIT.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.hotkey>)
      * [`REMOVE_STAKE_LIMIT.limit_price`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.limit_price>)
      * [`REMOVE_STAKE_LIMIT.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.netuid>)
      * [`REMOVE_STAKE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.pallet>)
      * [`REMOVE_STAKE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REMOVE_STAKE_LIMIT.wallet>)
    * [`REPORT_EQUIVOCATION`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION>)
      * [`REPORT_EQUIVOCATION.equivocation_proof`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION.equivocation_proof>)
      * [`REPORT_EQUIVOCATION.key_owner_proof`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION.key_owner_proof>)
      * [`REPORT_EQUIVOCATION.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION.pallet>)
      * [`REPORT_EQUIVOCATION.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION.wallet>)
    * [`REPORT_EQUIVOCATION_UNSIGNED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED>)
      * [`REPORT_EQUIVOCATION_UNSIGNED.equivocation_proof`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED.equivocation_proof>)
      * [`REPORT_EQUIVOCATION_UNSIGNED.key_owner_proof`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED.key_owner_proof>)
      * [`REPORT_EQUIVOCATION_UNSIGNED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED.pallet>)
      * [`REPORT_EQUIVOCATION_UNSIGNED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REPORT_EQUIVOCATION_UNSIGNED.wallet>)
    * [`REQUEST_PREIMAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REQUEST_PREIMAGE>)
      * [`REQUEST_PREIMAGE.hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REQUEST_PREIMAGE.hash>)
      * [`REQUEST_PREIMAGE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REQUEST_PREIMAGE.pallet>)
      * [`REQUEST_PREIMAGE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REQUEST_PREIMAGE.wallet>)
    * [`RESET_COLDKEY_SWAP`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RESET_COLDKEY_SWAP>)
      * [`RESET_COLDKEY_SWAP.coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RESET_COLDKEY_SWAP.coldkey>)
      * [`RESET_COLDKEY_SWAP.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RESET_COLDKEY_SWAP.pallet>)
      * [`RESET_COLDKEY_SWAP.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.RESET_COLDKEY_SWAP.wallet>)
    * [`REVEAL_MECHANISM_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS>)
      * [`REVEAL_MECHANISM_WEIGHTS.mecid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.mecid>)
      * [`REVEAL_MECHANISM_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.netuid>)
      * [`REVEAL_MECHANISM_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.pallet>)
      * [`REVEAL_MECHANISM_WEIGHTS.salt`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.salt>)
      * [`REVEAL_MECHANISM_WEIGHTS.uids`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.uids>)
      * [`REVEAL_MECHANISM_WEIGHTS.values`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.values>)
      * [`REVEAL_MECHANISM_WEIGHTS.version_key`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.version_key>)
      * [`REVEAL_MECHANISM_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_MECHANISM_WEIGHTS.wallet>)
    * [`REVEAL_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS>)
      * [`REVEAL_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.netuid>)
      * [`REVEAL_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.pallet>)
      * [`REVEAL_WEIGHTS.salt`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.salt>)
      * [`REVEAL_WEIGHTS.uids`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.uids>)
      * [`REVEAL_WEIGHTS.values`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.values>)
      * [`REVEAL_WEIGHTS.version_key`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.version_key>)
      * [`REVEAL_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.REVEAL_WEIGHTS.wallet>)
    * [`ROOT_DISSOLVE_NETWORK`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_DISSOLVE_NETWORK>)
      * [`ROOT_DISSOLVE_NETWORK.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_DISSOLVE_NETWORK.netuid>)
      * [`ROOT_DISSOLVE_NETWORK.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_DISSOLVE_NETWORK.pallet>)
      * [`ROOT_DISSOLVE_NETWORK.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_DISSOLVE_NETWORK.wallet>)
    * [`ROOT_REGISTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_REGISTER>)
      * [`ROOT_REGISTER.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_REGISTER.hotkey>)
      * [`ROOT_REGISTER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_REGISTER.pallet>)
      * [`ROOT_REGISTER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.ROOT_REGISTER.wallet>)
    * [`SCHEDULE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE>)
      * [`SCHEDULE.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.call>)
      * [`SCHEDULE.maybe_periodic`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.maybe_periodic>)
      * [`SCHEDULE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.pallet>)
      * [`SCHEDULE.priority`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.priority>)
      * [`SCHEDULE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.wallet>)
      * [`SCHEDULE.when`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE.when>)
    * [`SCHEDULE_AFTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER>)
      * [`SCHEDULE_AFTER.after`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.after>)
      * [`SCHEDULE_AFTER.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.call>)
      * [`SCHEDULE_AFTER.maybe_periodic`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.maybe_periodic>)
      * [`SCHEDULE_AFTER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.pallet>)
      * [`SCHEDULE_AFTER.priority`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.priority>)
      * [`SCHEDULE_AFTER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_AFTER.wallet>)
    * [`SCHEDULE_GRANDPA_CHANGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE>)
      * [`SCHEDULE_GRANDPA_CHANGE.forced`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE.forced>)
      * [`SCHEDULE_GRANDPA_CHANGE.in_blocks`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE.in_blocks>)
      * [`SCHEDULE_GRANDPA_CHANGE.next_authorities`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE.next_authorities>)
      * [`SCHEDULE_GRANDPA_CHANGE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE.pallet>)
      * [`SCHEDULE_GRANDPA_CHANGE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_GRANDPA_CHANGE.wallet>)
    * [`SCHEDULE_NAMED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED>)
      * [`SCHEDULE_NAMED.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.call>)
      * [`SCHEDULE_NAMED.id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.id>)
      * [`SCHEDULE_NAMED.maybe_periodic`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.maybe_periodic>)
      * [`SCHEDULE_NAMED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.pallet>)
      * [`SCHEDULE_NAMED.priority`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.priority>)
      * [`SCHEDULE_NAMED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.wallet>)
      * [`SCHEDULE_NAMED.when`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED.when>)
    * [`SCHEDULE_NAMED_AFTER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER>)
      * [`SCHEDULE_NAMED_AFTER.after`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.after>)
      * [`SCHEDULE_NAMED_AFTER.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.call>)
      * [`SCHEDULE_NAMED_AFTER.id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.id>)
      * [`SCHEDULE_NAMED_AFTER.maybe_periodic`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.maybe_periodic>)
      * [`SCHEDULE_NAMED_AFTER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.pallet>)
      * [`SCHEDULE_NAMED_AFTER.priority`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.priority>)
      * [`SCHEDULE_NAMED_AFTER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_NAMED_AFTER.wallet>)
    * [`SCHEDULE_SWAP_COLDKEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_SWAP_COLDKEY>)
      * [`SCHEDULE_SWAP_COLDKEY.new_coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_SWAP_COLDKEY.new_coldkey>)
      * [`SCHEDULE_SWAP_COLDKEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_SWAP_COLDKEY.pallet>)
      * [`SCHEDULE_SWAP_COLDKEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SCHEDULE_SWAP_COLDKEY.wallet>)
    * [`SERVE_AXON`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON>)
      * [`SERVE_AXON.ip`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.ip>)
      * [`SERVE_AXON.ip_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.ip_type>)
      * [`SERVE_AXON.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.netuid>)
      * [`SERVE_AXON.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.pallet>)
      * [`SERVE_AXON.placeholder1`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.placeholder1>)
      * [`SERVE_AXON.placeholder2`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.placeholder2>)
      * [`SERVE_AXON.port`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.port>)
      * [`SERVE_AXON.protocol`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.protocol>)
      * [`SERVE_AXON.version`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.version>)
      * [`SERVE_AXON.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON.wallet>)
    * [`SERVE_AXON_TLS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS>)
      * [`SERVE_AXON_TLS.certificate`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.certificate>)
      * [`SERVE_AXON_TLS.ip`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.ip>)
      * [`SERVE_AXON_TLS.ip_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.ip_type>)
      * [`SERVE_AXON_TLS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.netuid>)
      * [`SERVE_AXON_TLS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.pallet>)
      * [`SERVE_AXON_TLS.placeholder1`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.placeholder1>)
      * [`SERVE_AXON_TLS.placeholder2`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.placeholder2>)
      * [`SERVE_AXON_TLS.port`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.port>)
      * [`SERVE_AXON_TLS.protocol`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.protocol>)
      * [`SERVE_AXON_TLS.version`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.version>)
      * [`SERVE_AXON_TLS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_AXON_TLS.wallet>)
    * [`SERVE_PROMETHEUS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS>)
      * [`SERVE_PROMETHEUS.ip`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.ip>)
      * [`SERVE_PROMETHEUS.ip_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.ip_type>)
      * [`SERVE_PROMETHEUS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.netuid>)
      * [`SERVE_PROMETHEUS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.pallet>)
      * [`SERVE_PROMETHEUS.port`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.port>)
      * [`SERVE_PROMETHEUS.version`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.version>)
      * [`SERVE_PROMETHEUS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SERVE_PROMETHEUS.wallet>)
    * [`SET`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET>)
      * [`SET.now`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET.now>)
      * [`SET.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET.pallet>)
      * [`SET.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET.wallet>)
    * [`SET_AUTO_PARENT_DELEGATION_ENABLED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED>)
      * [`SET_AUTO_PARENT_DELEGATION_ENABLED.enabled`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED.enabled>)
      * [`SET_AUTO_PARENT_DELEGATION_ENABLED.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED.hotkey>)
      * [`SET_AUTO_PARENT_DELEGATION_ENABLED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED.pallet>)
      * [`SET_AUTO_PARENT_DELEGATION_ENABLED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_AUTO_PARENT_DELEGATION_ENABLED.wallet>)
    * [`SET_BASE_FEE_PER_GAS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BASE_FEE_PER_GAS>)
      * [`SET_BASE_FEE_PER_GAS.fee`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BASE_FEE_PER_GAS.fee>)
      * [`SET_BASE_FEE_PER_GAS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BASE_FEE_PER_GAS.pallet>)
      * [`SET_BASE_FEE_PER_GAS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BASE_FEE_PER_GAS.wallet>)
    * [`SET_BEACON_CONFIG`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG>)
      * [`SET_BEACON_CONFIG.config_payload`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG.config_payload>)
      * [`SET_BEACON_CONFIG.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG.pallet>)
      * [`SET_BEACON_CONFIG.signature`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG.signature>)
      * [`SET_BEACON_CONFIG.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_BEACON_CONFIG.wallet>)
    * [`SET_CHILDKEY_TAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE>)
      * [`SET_CHILDKEY_TAKE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE.hotkey>)
      * [`SET_CHILDKEY_TAKE.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE.netuid>)
      * [`SET_CHILDKEY_TAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE.pallet>)
      * [`SET_CHILDKEY_TAKE.take`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE.take>)
      * [`SET_CHILDKEY_TAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDKEY_TAKE.wallet>)
    * [`SET_CHILDREN`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN>)
      * [`SET_CHILDREN.children`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN.children>)
      * [`SET_CHILDREN.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN.hotkey>)
      * [`SET_CHILDREN.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN.netuid>)
      * [`SET_CHILDREN.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN.pallet>)
      * [`SET_CHILDREN.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CHILDREN.wallet>)
    * [`SET_CODE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE>)
      * [`SET_CODE.code`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE.code>)
      * [`SET_CODE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE.pallet>)
      * [`SET_CODE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE.wallet>)
    * [`SET_CODE`](<#id11>)
      * [`SET_CODE.code_hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE.code_hash>)
      * [`SET_CODE.dest`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE.dest>)
      * [`SET_CODE.pallet`](<#id12>)
      * [`SET_CODE.wallet`](<#id13>)
    * [`SET_CODE_WITHOUT_CHECKS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE_WITHOUT_CHECKS>)
      * [`SET_CODE_WITHOUT_CHECKS.code`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE_WITHOUT_CHECKS.code>)
      * [`SET_CODE_WITHOUT_CHECKS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE_WITHOUT_CHECKS.pallet>)
      * [`SET_CODE_WITHOUT_CHECKS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_CODE_WITHOUT_CHECKS.wallet>)
    * [`SET_COLDKEY_AUTO_STAKE_HOTKEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY>)
      * [`SET_COLDKEY_AUTO_STAKE_HOTKEY.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY.hotkey>)
      * [`SET_COLDKEY_AUTO_STAKE_HOTKEY.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY.netuid>)
      * [`SET_COLDKEY_AUTO_STAKE_HOTKEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY.pallet>)
      * [`SET_COLDKEY_AUTO_STAKE_HOTKEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COLDKEY_AUTO_STAKE_HOTKEY.wallet>)
    * [`SET_COMMITMENT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT>)
      * [`SET_COMMITMENT.info`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT.info>)
      * [`SET_COMMITMENT.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT.netuid>)
      * [`SET_COMMITMENT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT.pallet>)
      * [`SET_COMMITMENT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_COMMITMENT.wallet>)
    * [`SET_ELASTICITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ELASTICITY>)
      * [`SET_ELASTICITY.elasticity`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ELASTICITY.elasticity>)
      * [`SET_ELASTICITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ELASTICITY.pallet>)
      * [`SET_ELASTICITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ELASTICITY.wallet>)
    * [`SET_FEE_RATE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE>)
      * [`SET_FEE_RATE.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE.netuid>)
      * [`SET_FEE_RATE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE.pallet>)
      * [`SET_FEE_RATE.rate`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE.rate>)
      * [`SET_FEE_RATE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_FEE_RATE.wallet>)
    * [`SET_HEAP_PAGES`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_HEAP_PAGES>)
      * [`SET_HEAP_PAGES.pages`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_HEAP_PAGES.pages>)
      * [`SET_HEAP_PAGES.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_HEAP_PAGES.pallet>)
      * [`SET_HEAP_PAGES.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_HEAP_PAGES.wallet>)
    * [`SET_IDENTITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY>)
      * [`SET_IDENTITY.identified`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.identified>)
      * [`SET_IDENTITY.info`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.info>)
      * [`SET_IDENTITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.pallet>)
      * [`SET_IDENTITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.wallet>)
    * [`SET_IDENTITY`](<#id14>)
      * [`SET_IDENTITY.additional`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.additional>)
      * [`SET_IDENTITY.description`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.description>)
      * [`SET_IDENTITY.discord`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.discord>)
      * [`SET_IDENTITY.github_repo`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.github_repo>)
      * [`SET_IDENTITY.image`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.image>)
      * [`SET_IDENTITY.name`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.name>)
      * [`SET_IDENTITY.pallet`](<#id15>)
      * [`SET_IDENTITY.url`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_IDENTITY.url>)
      * [`SET_IDENTITY.wallet`](<#id16>)
    * [`SET_KEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_KEY>)
      * [`SET_KEY.new`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_KEY.new>)
      * [`SET_KEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_KEY.pallet>)
      * [`SET_KEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_KEY.wallet>)
    * [`SET_MAX_EXTRINSIC_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_EXTRINSIC_WEIGHT>)
      * [`SET_MAX_EXTRINSIC_WEIGHT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_EXTRINSIC_WEIGHT.pallet>)
      * [`SET_MAX_EXTRINSIC_WEIGHT.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_EXTRINSIC_WEIGHT.value>)
      * [`SET_MAX_EXTRINSIC_WEIGHT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_EXTRINSIC_WEIGHT.wallet>)
    * [`SET_MAX_PENDING_EXTRINSICS_NUMBER`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_PENDING_EXTRINSICS_NUMBER>)
      * [`SET_MAX_PENDING_EXTRINSICS_NUMBER.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_PENDING_EXTRINSICS_NUMBER.pallet>)
      * [`SET_MAX_PENDING_EXTRINSICS_NUMBER.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_PENDING_EXTRINSICS_NUMBER.value>)
      * [`SET_MAX_PENDING_EXTRINSICS_NUMBER.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_PENDING_EXTRINSICS_NUMBER.wallet>)
    * [`SET_MAX_SPACE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_SPACE>)
      * [`SET_MAX_SPACE.new_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_SPACE.new_limit>)
      * [`SET_MAX_SPACE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_SPACE.pallet>)
      * [`SET_MAX_SPACE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MAX_SPACE.wallet>)
    * [`SET_MECHANISM_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS>)
      * [`SET_MECHANISM_WEIGHTS.dests`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.dests>)
      * [`SET_MECHANISM_WEIGHTS.mecid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.mecid>)
      * [`SET_MECHANISM_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.netuid>)
      * [`SET_MECHANISM_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.pallet>)
      * [`SET_MECHANISM_WEIGHTS.version_key`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.version_key>)
      * [`SET_MECHANISM_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.wallet>)
      * [`SET_MECHANISM_WEIGHTS.weights`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_MECHANISM_WEIGHTS.weights>)
    * [`SET_OLDEST_STORED_ROUND`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_OLDEST_STORED_ROUND>)
      * [`SET_OLDEST_STORED_ROUND.oldest_round`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_OLDEST_STORED_ROUND.oldest_round>)
      * [`SET_OLDEST_STORED_ROUND.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_OLDEST_STORED_ROUND.pallet>)
      * [`SET_OLDEST_STORED_ROUND.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_OLDEST_STORED_ROUND.wallet>)
    * [`SET_ON_INITIALIZE_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ON_INITIALIZE_WEIGHT>)
      * [`SET_ON_INITIALIZE_WEIGHT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ON_INITIALIZE_WEIGHT.pallet>)
      * [`SET_ON_INITIALIZE_WEIGHT.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ON_INITIALIZE_WEIGHT.value>)
      * [`SET_ON_INITIALIZE_WEIGHT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ON_INITIALIZE_WEIGHT.wallet>)
    * [`SET_PENDING_CHILDKEY_COOLDOWN`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_PENDING_CHILDKEY_COOLDOWN>)
      * [`SET_PENDING_CHILDKEY_COOLDOWN.cooldown`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_PENDING_CHILDKEY_COOLDOWN.cooldown>)
      * [`SET_PENDING_CHILDKEY_COOLDOWN.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_PENDING_CHILDKEY_COOLDOWN.pallet>)
      * [`SET_PENDING_CHILDKEY_COOLDOWN.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_PENDING_CHILDKEY_COOLDOWN.wallet>)
    * [`SET_REAL_PAYS_FEE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE>)
      * [`SET_REAL_PAYS_FEE.delegate`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE.delegate>)
      * [`SET_REAL_PAYS_FEE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE.pallet>)
      * [`SET_REAL_PAYS_FEE.pays_fee`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE.pays_fee>)
      * [`SET_REAL_PAYS_FEE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_REAL_PAYS_FEE.wallet>)
    * [`SET_RETRY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY>)
      * [`SET_RETRY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY.pallet>)
      * [`SET_RETRY.period`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY.period>)
      * [`SET_RETRY.retries`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY.retries>)
      * [`SET_RETRY.task`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY.task>)
      * [`SET_RETRY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY.wallet>)
    * [`SET_RETRY_NAMED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED>)
      * [`SET_RETRY_NAMED.id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED.id>)
      * [`SET_RETRY_NAMED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED.pallet>)
      * [`SET_RETRY_NAMED.period`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED.period>)
      * [`SET_RETRY_NAMED.retries`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED.retries>)
      * [`SET_RETRY_NAMED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_RETRY_NAMED.wallet>)
    * [`SET_ROOT_CLAIM_TYPE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ROOT_CLAIM_TYPE>)
      * [`SET_ROOT_CLAIM_TYPE.new_root_claim_type`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ROOT_CLAIM_TYPE.new_root_claim_type>)
      * [`SET_ROOT_CLAIM_TYPE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ROOT_CLAIM_TYPE.pallet>)
      * [`SET_ROOT_CLAIM_TYPE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_ROOT_CLAIM_TYPE.wallet>)
    * [`SET_STORAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORAGE>)
      * [`SET_STORAGE.items`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORAGE.items>)
      * [`SET_STORAGE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORAGE.pallet>)
      * [`SET_STORAGE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORAGE.wallet>)
    * [`SET_STORED_EXTRINSIC_LIFETIME`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORED_EXTRINSIC_LIFETIME>)
      * [`SET_STORED_EXTRINSIC_LIFETIME.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORED_EXTRINSIC_LIFETIME.pallet>)
      * [`SET_STORED_EXTRINSIC_LIFETIME.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORED_EXTRINSIC_LIFETIME.value>)
      * [`SET_STORED_EXTRINSIC_LIFETIME.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_STORED_EXTRINSIC_LIFETIME.wallet>)
    * [`SET_SUBNET_IDENTITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY>)
      * [`SET_SUBNET_IDENTITY.additional`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.additional>)
      * [`SET_SUBNET_IDENTITY.description`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.description>)
      * [`SET_SUBNET_IDENTITY.discord`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.discord>)
      * [`SET_SUBNET_IDENTITY.github_repo`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.github_repo>)
      * [`SET_SUBNET_IDENTITY.logo_url`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.logo_url>)
      * [`SET_SUBNET_IDENTITY.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.netuid>)
      * [`SET_SUBNET_IDENTITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.pallet>)
      * [`SET_SUBNET_IDENTITY.subnet_contact`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.subnet_contact>)
      * [`SET_SUBNET_IDENTITY.subnet_name`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.subnet_name>)
      * [`SET_SUBNET_IDENTITY.subnet_url`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.subnet_url>)
      * [`SET_SUBNET_IDENTITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_SUBNET_IDENTITY.wallet>)
    * [`SET_WEIGHTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS>)
      * [`SET_WEIGHTS.dests`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.dests>)
      * [`SET_WEIGHTS.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.netuid>)
      * [`SET_WEIGHTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.pallet>)
      * [`SET_WEIGHTS.version_key`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.version_key>)
      * [`SET_WEIGHTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.wallet>)
      * [`SET_WEIGHTS.weights`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WEIGHTS.weights>)
    * [`SET_WHITELIST`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WHITELIST>)
      * [`SET_WHITELIST.new`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WHITELIST.new>)
      * [`SET_WHITELIST.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WHITELIST.pallet>)
      * [`SET_WHITELIST.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SET_WHITELIST.wallet>)
    * [`START_CALL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.START_CALL>)
      * [`START_CALL.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.START_CALL.netuid>)
      * [`START_CALL.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.START_CALL.pallet>)
      * [`START_CALL.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.START_CALL.wallet>)
    * [`STORE_ENCRYPTED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.STORE_ENCRYPTED>)
      * [`STORE_ENCRYPTED.encrypted_call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.STORE_ENCRYPTED.encrypted_call>)
      * [`STORE_ENCRYPTED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.STORE_ENCRYPTED.pallet>)
      * [`STORE_ENCRYPTED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.STORE_ENCRYPTED.wallet>)
    * [`SUBMIT_ENCRYPTED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUBMIT_ENCRYPTED>)
      * [`SUBMIT_ENCRYPTED.ciphertext`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUBMIT_ENCRYPTED.ciphertext>)
      * [`SUBMIT_ENCRYPTED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUBMIT_ENCRYPTED.pallet>)
      * [`SUBMIT_ENCRYPTED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUBMIT_ENCRYPTED.wallet>)
    * [`SUDO`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUDO>)
      * [`SUDO.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUDO.call>)
      * [`SUDO.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUDO.pallet>)
      * [`SUDO.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SUDO.wallet>)
    * [`SWAP_AUTHORITIES`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_AUTHORITIES>)
      * [`SWAP_AUTHORITIES.new_authorities`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_AUTHORITIES.new_authorities>)
      * [`SWAP_AUTHORITIES.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_AUTHORITIES.pallet>)
      * [`SWAP_AUTHORITIES.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_AUTHORITIES.wallet>)
    * [`SWAP_COLDKEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY>)
      * [`SWAP_COLDKEY.new_coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY.new_coldkey>)
      * [`SWAP_COLDKEY.old_coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY.old_coldkey>)
      * [`SWAP_COLDKEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY.pallet>)
      * [`SWAP_COLDKEY.swap_cost`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY.swap_cost>)
      * [`SWAP_COLDKEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY.wallet>)
    * [`SWAP_COLDKEY_ANNOUNCED`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY_ANNOUNCED>)
      * [`SWAP_COLDKEY_ANNOUNCED.new_coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY_ANNOUNCED.new_coldkey>)
      * [`SWAP_COLDKEY_ANNOUNCED.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY_ANNOUNCED.pallet>)
      * [`SWAP_COLDKEY_ANNOUNCED.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_COLDKEY_ANNOUNCED.wallet>)
    * [`SWAP_HOTKEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY>)
      * [`SWAP_HOTKEY.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY.hotkey>)
      * [`SWAP_HOTKEY.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY.netuid>)
      * [`SWAP_HOTKEY.new_hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY.new_hotkey>)
      * [`SWAP_HOTKEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY.pallet>)
      * [`SWAP_HOTKEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY.wallet>)
    * [`SWAP_HOTKEY_V2`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2>)
      * [`SWAP_HOTKEY_V2.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.hotkey>)
      * [`SWAP_HOTKEY_V2.keep_stake`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.keep_stake>)
      * [`SWAP_HOTKEY_V2.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.netuid>)
      * [`SWAP_HOTKEY_V2.new_hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.new_hotkey>)
      * [`SWAP_HOTKEY_V2.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.pallet>)
      * [`SWAP_HOTKEY_V2.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_HOTKEY_V2.wallet>)
    * [`SWAP_STAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE>)
      * [`SWAP_STAKE.alpha_amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.alpha_amount>)
      * [`SWAP_STAKE.destination_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.destination_netuid>)
      * [`SWAP_STAKE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.hotkey>)
      * [`SWAP_STAKE.origin_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.origin_netuid>)
      * [`SWAP_STAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.pallet>)
      * [`SWAP_STAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE.wallet>)
    * [`SWAP_STAKE_LIMIT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT>)
      * [`SWAP_STAKE_LIMIT.allow_partial`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.allow_partial>)
      * [`SWAP_STAKE_LIMIT.alpha_amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.alpha_amount>)
      * [`SWAP_STAKE_LIMIT.destination_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.destination_netuid>)
      * [`SWAP_STAKE_LIMIT.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.hotkey>)
      * [`SWAP_STAKE_LIMIT.limit_price`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.limit_price>)
      * [`SWAP_STAKE_LIMIT.origin_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.origin_netuid>)
      * [`SWAP_STAKE_LIMIT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.pallet>)
      * [`SWAP_STAKE_LIMIT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.SWAP_STAKE_LIMIT.wallet>)
    * [`TERMINATE_LEASE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE>)
      * [`TERMINATE_LEASE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE.hotkey>)
      * [`TERMINATE_LEASE.lease_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE.lease_id>)
      * [`TERMINATE_LEASE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE.pallet>)
      * [`TERMINATE_LEASE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TERMINATE_LEASE.wallet>)
    * [`TOGGLE_USER_LIQUIDITY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY>)
      * [`TOGGLE_USER_LIQUIDITY.enable`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY.enable>)
      * [`TOGGLE_USER_LIQUIDITY.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY.netuid>)
      * [`TOGGLE_USER_LIQUIDITY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY.pallet>)
      * [`TOGGLE_USER_LIQUIDITY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TOGGLE_USER_LIQUIDITY.wallet>)
    * [`TRANSACT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSACT>)
      * [`TRANSACT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSACT.pallet>)
      * [`TRANSACT.transaction`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSACT.transaction>)
      * [`TRANSACT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSACT.wallet>)
    * [`TRANSFER_ALL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL>)
      * [`TRANSFER_ALL.dest`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL.dest>)
      * [`TRANSFER_ALL.keep_alive`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL.keep_alive>)
      * [`TRANSFER_ALL.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL.pallet>)
      * [`TRANSFER_ALL.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALL.wallet>)
    * [`TRANSFER_ALLOW_DEATH`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH>)
      * [`TRANSFER_ALLOW_DEATH.dest`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH.dest>)
      * [`TRANSFER_ALLOW_DEATH.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH.pallet>)
      * [`TRANSFER_ALLOW_DEATH.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH.value>)
      * [`TRANSFER_ALLOW_DEATH.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_ALLOW_DEATH.wallet>)
    * [`TRANSFER_KEEP_ALIVE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE>)
      * [`TRANSFER_KEEP_ALIVE.dest`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE.dest>)
      * [`TRANSFER_KEEP_ALIVE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE.pallet>)
      * [`TRANSFER_KEEP_ALIVE.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE.value>)
      * [`TRANSFER_KEEP_ALIVE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_KEEP_ALIVE.wallet>)
    * [`TRANSFER_STAKE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE>)
      * [`TRANSFER_STAKE.alpha_amount`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.alpha_amount>)
      * [`TRANSFER_STAKE.destination_coldkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.destination_coldkey>)
      * [`TRANSFER_STAKE.destination_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.destination_netuid>)
      * [`TRANSFER_STAKE.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.hotkey>)
      * [`TRANSFER_STAKE.origin_netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.origin_netuid>)
      * [`TRANSFER_STAKE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.pallet>)
      * [`TRANSFER_STAKE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRANSFER_STAKE.wallet>)
    * [`TRY_ASSOCIATE_HOTKEY`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRY_ASSOCIATE_HOTKEY>)
      * [`TRY_ASSOCIATE_HOTKEY.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRY_ASSOCIATE_HOTKEY.hotkey>)
      * [`TRY_ASSOCIATE_HOTKEY.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRY_ASSOCIATE_HOTKEY.pallet>)
      * [`TRY_ASSOCIATE_HOTKEY.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.TRY_ASSOCIATE_HOTKEY.wallet>)
    * [`UNNOTE_PREIMAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNNOTE_PREIMAGE>)
      * [`UNNOTE_PREIMAGE.hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNNOTE_PREIMAGE.hash>)
      * [`UNNOTE_PREIMAGE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNNOTE_PREIMAGE.pallet>)
      * [`UNNOTE_PREIMAGE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNNOTE_PREIMAGE.wallet>)
    * [`UNREQUEST_PREIMAGE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNREQUEST_PREIMAGE>)
      * [`UNREQUEST_PREIMAGE.hash`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNREQUEST_PREIMAGE.hash>)
      * [`UNREQUEST_PREIMAGE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNREQUEST_PREIMAGE.pallet>)
      * [`UNREQUEST_PREIMAGE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNREQUEST_PREIMAGE.wallet>)
    * [`UNSTAKE_ALL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL>)
      * [`UNSTAKE_ALL.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL.hotkey>)
      * [`UNSTAKE_ALL.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL.pallet>)
      * [`UNSTAKE_ALL.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL.wallet>)
    * [`UNSTAKE_ALL_ALPHA`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL_ALPHA>)
      * [`UNSTAKE_ALL_ALPHA.hotkey`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL_ALPHA.hotkey>)
      * [`UNSTAKE_ALL_ALPHA.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL_ALPHA.pallet>)
      * [`UNSTAKE_ALL_ALPHA.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UNSTAKE_ALL_ALPHA.wallet>)
    * [`UPDATE_CAP`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP>)
      * [`UPDATE_CAP.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP.crowdloan_id>)
      * [`UPDATE_CAP.new_cap`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP.new_cap>)
      * [`UPDATE_CAP.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP.pallet>)
      * [`UPDATE_CAP.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_CAP.wallet>)
    * [`UPDATE_END`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END>)
      * [`UPDATE_END.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END.crowdloan_id>)
      * [`UPDATE_END.new_end`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END.new_end>)
      * [`UPDATE_END.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END.pallet>)
      * [`UPDATE_END.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_END.wallet>)
    * [`UPDATE_MIN_CONTRIBUTION`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION>)
      * [`UPDATE_MIN_CONTRIBUTION.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION.crowdloan_id>)
      * [`UPDATE_MIN_CONTRIBUTION.new_min_contribution`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION.new_min_contribution>)
      * [`UPDATE_MIN_CONTRIBUTION.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION.pallet>)
      * [`UPDATE_MIN_CONTRIBUTION.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_MIN_CONTRIBUTION.wallet>)
    * [`UPDATE_SYMBOL`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL>)
      * [`UPDATE_SYMBOL.netuid`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL.netuid>)
      * [`UPDATE_SYMBOL.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL.pallet>)
      * [`UPDATE_SYMBOL.symbol`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL.symbol>)
      * [`UPDATE_SYMBOL.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPDATE_SYMBOL.wallet>)
    * [`UPGRADE_ACCOUNTS`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPGRADE_ACCOUNTS>)
      * [`UPGRADE_ACCOUNTS.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPGRADE_ACCOUNTS.pallet>)
      * [`UPGRADE_ACCOUNTS.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPGRADE_ACCOUNTS.wallet>)
      * [`UPGRADE_ACCOUNTS.who`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPGRADE_ACCOUNTS.who>)
    * [`UPLOAD_CODE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE>)
      * [`UPLOAD_CODE.code`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE.code>)
      * [`UPLOAD_CODE.determinism`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE.determinism>)
      * [`UPLOAD_CODE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE.pallet>)
      * [`UPLOAD_CODE.storage_deposit_limit`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE.storage_deposit_limit>)
      * [`UPLOAD_CODE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.UPLOAD_CODE.wallet>)
    * [`WITHDRAW`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW>)
      * [`WITHDRAW.address`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW.address>)
      * [`WITHDRAW.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW.pallet>)
      * [`WITHDRAW.value`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW.value>)
      * [`WITHDRAW.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW.wallet>)
    * [`WITHDRAW`](<#id17>)
      * [`WITHDRAW.crowdloan_id`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITHDRAW.crowdloan_id>)
      * [`WITHDRAW.pallet`](<#id18>)
      * [`WITHDRAW.wallet`](<#id19>)
    * [`WITH_WEIGHT`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT>)
      * [`WITH_WEIGHT.call`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT.call>)
      * [`WITH_WEIGHT.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT.pallet>)
      * [`WITH_WEIGHT.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT.wallet>)
      * [`WITH_WEIGHT.weight`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WITH_WEIGHT.weight>)
    * [`WRITE_PULSE`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE>)
      * [`WRITE_PULSE.pallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE.pallet>)
      * [`WRITE_PULSE.pulses_payload`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE.pulses_payload>)
      * [`WRITE_PULSE.signature`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE.signature>)
      * [`WRITE_PULSE.wallet`](<#bittensor.extras.dev_framework.calls.non_sudo_calls.WRITE_PULSE.wallet>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.