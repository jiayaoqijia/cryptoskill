# bittensor.core.settings &#8212; Bittensor SDK Docs  documentation

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
        * [bittensor.core.settings](<#>)
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
  * [ __ Show source ](<https://github.com/opentensor/btcli/blob/main/autoapi/bittensor/core/settings/index.rst?plain=1> "Show source")
  * [ __ Open issue ](<https://github.com/opentensor/btcli/issues/new?title=Issue%20on%20page%20%2Fautoapi/bittensor/core/settings/index.html&body=Your%20issue%20content%20here.> "Open an issue")



__

  * [ __ .rst ](<../../../../_sources/autoapi/bittensor/core/settings/index.rst> "Download source file")
  * __ .pdf



__ ______ __

# bittensor.core.settings

##  Contents 

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`ARCHIVE_ENTRYPOINT`](<#bittensor.core.settings.ARCHIVE_ENTRYPOINT>)
    * [`BLOCKTIME`](<#bittensor.core.settings.BLOCKTIME>)
    * [`DEFAULTS`](<#bittensor.core.settings.DEFAULTS>)
      * [`DEFAULTS.axon`](<#bittensor.core.settings.DEFAULTS.axon>)
        * [`DEFAULTS.axon.external_ip`](<#bittensor.core.settings.DEFAULTS.axon.external_ip>)
        * [`DEFAULTS.axon.external_port`](<#bittensor.core.settings.DEFAULTS.axon.external_port>)
        * [`DEFAULTS.axon.ip`](<#bittensor.core.settings.DEFAULTS.axon.ip>)
        * [`DEFAULTS.axon.max_workers`](<#bittensor.core.settings.DEFAULTS.axon.max_workers>)
        * [`DEFAULTS.axon.port`](<#bittensor.core.settings.DEFAULTS.axon.port>)
      * [`DEFAULTS.config`](<#bittensor.core.settings.DEFAULTS.config>)
      * [`DEFAULTS.logging`](<#bittensor.core.settings.DEFAULTS.logging>)
        * [`DEFAULTS.logging.debug`](<#bittensor.core.settings.DEFAULTS.logging.debug>)
        * [`DEFAULTS.logging.enable_third_party_loggers`](<#bittensor.core.settings.DEFAULTS.logging.enable_third_party_loggers>)
        * [`DEFAULTS.logging.info`](<#bittensor.core.settings.DEFAULTS.logging.info>)
        * [`DEFAULTS.logging.logging_dir`](<#bittensor.core.settings.DEFAULTS.logging.logging_dir>)
        * [`DEFAULTS.logging.record_log`](<#bittensor.core.settings.DEFAULTS.logging.record_log>)
        * [`DEFAULTS.logging.trace`](<#bittensor.core.settings.DEFAULTS.logging.trace>)
      * [`DEFAULTS.no_version_checking`](<#bittensor.core.settings.DEFAULTS.no_version_checking>)
      * [`DEFAULTS.priority`](<#bittensor.core.settings.DEFAULTS.priority>)
        * [`DEFAULTS.priority.max_workers`](<#bittensor.core.settings.DEFAULTS.priority.max_workers>)
        * [`DEFAULTS.priority.maxsize`](<#bittensor.core.settings.DEFAULTS.priority.maxsize>)
      * [`DEFAULTS.strict`](<#bittensor.core.settings.DEFAULTS.strict>)
      * [`DEFAULTS.subtensor`](<#bittensor.core.settings.DEFAULTS.subtensor>)
        * [`DEFAULTS.subtensor.chain_endpoint`](<#bittensor.core.settings.DEFAULTS.subtensor.chain_endpoint>)
        * [`DEFAULTS.subtensor.network`](<#bittensor.core.settings.DEFAULTS.subtensor.network>)
      * [`DEFAULTS.wallet`](<#bittensor.core.settings.DEFAULTS.wallet>)
        * [`DEFAULTS.wallet.hotkey`](<#bittensor.core.settings.DEFAULTS.wallet.hotkey>)
        * [`DEFAULTS.wallet.name`](<#bittensor.core.settings.DEFAULTS.wallet.name>)
        * [`DEFAULTS.wallet.path`](<#bittensor.core.settings.DEFAULTS.wallet.path>)
    * [`DEFAULT_ENDPOINT`](<#bittensor.core.settings.DEFAULT_ENDPOINT>)
    * [`DEFAULT_MEV_PROTECTION`](<#bittensor.core.settings.DEFAULT_MEV_PROTECTION>)
    * [`DEFAULT_NETWORK`](<#bittensor.core.settings.DEFAULT_NETWORK>)
    * [`DEFAULT_PERIOD`](<#bittensor.core.settings.DEFAULT_PERIOD>)
    * [`FINNEY_ENTRYPOINT`](<#bittensor.core.settings.FINNEY_ENTRYPOINT>)
    * [`FINNEY_TEST_ENTRYPOINT`](<#bittensor.core.settings.FINNEY_TEST_ENTRYPOINT>)
    * [`HOME_DIR`](<#bittensor.core.settings.HOME_DIR>)
    * [`LATENT_LITE_ENTRYPOINT`](<#bittensor.core.settings.LATENT_LITE_ENTRYPOINT>)
    * [`LOCAL_ENTRYPOINT`](<#bittensor.core.settings.LOCAL_ENTRYPOINT>)
    * [`MAX_MEV_SHIELD_PERIOD`](<#bittensor.core.settings.MAX_MEV_SHIELD_PERIOD>)
    * [`MINERS_DIR`](<#bittensor.core.settings.MINERS_DIR>)
    * [`MLKEM768_PUBLIC_KEY_SIZE`](<#bittensor.core.settings.MLKEM768_PUBLIC_KEY_SIZE>)
    * [`NETWORKS`](<#bittensor.core.settings.NETWORKS>)
    * [`NETWORK_EXPLORER_MAP`](<#bittensor.core.settings.NETWORK_EXPLORER_MAP>)
    * [`NETWORK_MAP`](<#bittensor.core.settings.NETWORK_MAP>)
    * [`PIPADDRESS`](<#bittensor.core.settings.PIPADDRESS>)
    * [`RAO_SYMBOL`](<#bittensor.core.settings.RAO_SYMBOL>)
    * [`READ_ONLY`](<#bittensor.core.settings.READ_ONLY>)
    * [`REVERSE_NETWORK_MAP`](<#bittensor.core.settings.REVERSE_NETWORK_MAP>)
    * [`ROOT_TAO_STAKE_WEIGHT`](<#bittensor.core.settings.ROOT_TAO_STAKE_WEIGHT>)
    * [`SS58_ADDRESS_LENGTH`](<#bittensor.core.settings.SS58_ADDRESS_LENGTH>)
    * [`TAO_APP_BLOCK_EXPLORER`](<#bittensor.core.settings.TAO_APP_BLOCK_EXPLORER>)
    * [`TAO_SYMBOL`](<#bittensor.core.settings.TAO_SYMBOL>)
    * [`TYPE_REGISTRY`](<#bittensor.core.settings.TYPE_REGISTRY>)
    * [`USER_BITTENSOR_DIR`](<#bittensor.core.settings.USER_BITTENSOR_DIR>)
    * [`WALLETS_DIR`](<#bittensor.core.settings.WALLETS_DIR>)
    * [`version_as_int`](<#bittensor.core.settings.version_as_int>)



# bittensor.core.settings[#](<#module-bittensor.core.settings> "Link to this heading")

## Attributes[#](<#attributes> "Link to this heading")

[`ARCHIVE_ENTRYPOINT`](<#bittensor.core.settings.ARCHIVE_ENTRYPOINT> "bittensor.core.settings.ARCHIVE_ENTRYPOINT") |   
---|---  
[`BLOCKTIME`](<#bittensor.core.settings.BLOCKTIME> "bittensor.core.settings.BLOCKTIME") |   
[`DEFAULT_ENDPOINT`](<#bittensor.core.settings.DEFAULT_ENDPOINT> "bittensor.core.settings.DEFAULT_ENDPOINT") |   
[`DEFAULT_MEV_PROTECTION`](<#bittensor.core.settings.DEFAULT_MEV_PROTECTION> "bittensor.core.settings.DEFAULT_MEV_PROTECTION") |   
[`DEFAULT_NETWORK`](<#bittensor.core.settings.DEFAULT_NETWORK> "bittensor.core.settings.DEFAULT_NETWORK") |   
[`DEFAULT_PERIOD`](<#bittensor.core.settings.DEFAULT_PERIOD> "bittensor.core.settings.DEFAULT_PERIOD") |   
[`FINNEY_ENTRYPOINT`](<#bittensor.core.settings.FINNEY_ENTRYPOINT> "bittensor.core.settings.FINNEY_ENTRYPOINT") |   
[`FINNEY_TEST_ENTRYPOINT`](<#bittensor.core.settings.FINNEY_TEST_ENTRYPOINT> "bittensor.core.settings.FINNEY_TEST_ENTRYPOINT") |   
[`HOME_DIR`](<#bittensor.core.settings.HOME_DIR> "bittensor.core.settings.HOME_DIR") |   
[`LATENT_LITE_ENTRYPOINT`](<#bittensor.core.settings.LATENT_LITE_ENTRYPOINT> "bittensor.core.settings.LATENT_LITE_ENTRYPOINT") |   
[`LOCAL_ENTRYPOINT`](<#bittensor.core.settings.LOCAL_ENTRYPOINT> "bittensor.core.settings.LOCAL_ENTRYPOINT") |   
[`MAX_MEV_SHIELD_PERIOD`](<#bittensor.core.settings.MAX_MEV_SHIELD_PERIOD> "bittensor.core.settings.MAX_MEV_SHIELD_PERIOD") |   
[`MINERS_DIR`](<#bittensor.core.settings.MINERS_DIR> "bittensor.core.settings.MINERS_DIR") |   
[`MLKEM768_PUBLIC_KEY_SIZE`](<#bittensor.core.settings.MLKEM768_PUBLIC_KEY_SIZE> "bittensor.core.settings.MLKEM768_PUBLIC_KEY_SIZE") |   
[`NETWORKS`](<#bittensor.core.settings.NETWORKS> "bittensor.core.settings.NETWORKS") |   
[`NETWORK_EXPLORER_MAP`](<#bittensor.core.settings.NETWORK_EXPLORER_MAP> "bittensor.core.settings.NETWORK_EXPLORER_MAP") |   
[`NETWORK_MAP`](<#bittensor.core.settings.NETWORK_MAP> "bittensor.core.settings.NETWORK_MAP") |   
[`PIPADDRESS`](<#bittensor.core.settings.PIPADDRESS> "bittensor.core.settings.PIPADDRESS") |   
[`RAO_SYMBOL`](<#bittensor.core.settings.RAO_SYMBOL> "bittensor.core.settings.RAO_SYMBOL") |   
[`READ_ONLY`](<#bittensor.core.settings.READ_ONLY> "bittensor.core.settings.READ_ONLY") |   
[`REVERSE_NETWORK_MAP`](<#bittensor.core.settings.REVERSE_NETWORK_MAP> "bittensor.core.settings.REVERSE_NETWORK_MAP") |   
[`ROOT_TAO_STAKE_WEIGHT`](<#bittensor.core.settings.ROOT_TAO_STAKE_WEIGHT> "bittensor.core.settings.ROOT_TAO_STAKE_WEIGHT") |   
[`SS58_ADDRESS_LENGTH`](<#bittensor.core.settings.SS58_ADDRESS_LENGTH> "bittensor.core.settings.SS58_ADDRESS_LENGTH") |   
[`TAO_APP_BLOCK_EXPLORER`](<#bittensor.core.settings.TAO_APP_BLOCK_EXPLORER> "bittensor.core.settings.TAO_APP_BLOCK_EXPLORER") |   
[`TAO_SYMBOL`](<#bittensor.core.settings.TAO_SYMBOL> "bittensor.core.settings.TAO_SYMBOL") |   
[`TYPE_REGISTRY`](<#bittensor.core.settings.TYPE_REGISTRY> "bittensor.core.settings.TYPE_REGISTRY") |   
[`USER_BITTENSOR_DIR`](<#bittensor.core.settings.USER_BITTENSOR_DIR> "bittensor.core.settings.USER_BITTENSOR_DIR") |   
[`WALLETS_DIR`](<#bittensor.core.settings.WALLETS_DIR> "bittensor.core.settings.WALLETS_DIR") |   
[`version_as_int`](<#bittensor.core.settings.version_as_int> "bittensor.core.settings.version_as_int") |   
  
## Classes[#](<#classes> "Link to this heading")

[`DEFAULTS`](<#bittensor.core.settings.DEFAULTS> "bittensor.core.settings.DEFAULTS") |   
---|---  
  
## Module Contents[#](<#module-contents> "Link to this heading")

bittensor.core.settings.ARCHIVE_ENTRYPOINT = 'wss://archive.chain.opentensor.ai:443'[#](<#bittensor.core.settings.ARCHIVE_ENTRYPOINT> "Link to this definition")
    

bittensor.core.settings.BLOCKTIME = 12[#](<#bittensor.core.settings.BLOCKTIME> "Link to this definition")
    

class bittensor.core.settings.DEFAULTS[#](<#bittensor.core.settings.DEFAULTS> "Link to this definition")
    

class axon[#](<#bittensor.core.settings.DEFAULTS.axon> "Link to this definition")
    

external_ip[#](<#bittensor.core.settings.DEFAULTS.axon.external_ip> "Link to this definition")
    

external_port[#](<#bittensor.core.settings.DEFAULTS.axon.external_port> "Link to this definition")
    

ip[#](<#bittensor.core.settings.DEFAULTS.axon.ip> "Link to this definition")
    

max_workers[#](<#bittensor.core.settings.DEFAULTS.axon.max_workers> "Link to this definition")
    

port[#](<#bittensor.core.settings.DEFAULTS.axon.port> "Link to this definition")
    

config = False[#](<#bittensor.core.settings.DEFAULTS.config> "Link to this definition")
    

class logging[#](<#bittensor.core.settings.DEFAULTS.logging> "Link to this definition")
    

debug[#](<#bittensor.core.settings.DEFAULTS.logging.debug> "Link to this definition")
    

enable_third_party_loggers[#](<#bittensor.core.settings.DEFAULTS.logging.enable_third_party_loggers> "Link to this definition")
    

info[#](<#bittensor.core.settings.DEFAULTS.logging.info> "Link to this definition")
    

logging_dir = None[#](<#bittensor.core.settings.DEFAULTS.logging.logging_dir> "Link to this definition")
    

record_log[#](<#bittensor.core.settings.DEFAULTS.logging.record_log> "Link to this definition")
    

trace[#](<#bittensor.core.settings.DEFAULTS.logging.trace> "Link to this definition")
    

no_version_checking = False[#](<#bittensor.core.settings.DEFAULTS.no_version_checking> "Link to this definition")
    

class priority[#](<#bittensor.core.settings.DEFAULTS.priority> "Link to this definition")
    

max_workers[#](<#bittensor.core.settings.DEFAULTS.priority.max_workers> "Link to this definition")
    

maxsize[#](<#bittensor.core.settings.DEFAULTS.priority.maxsize> "Link to this definition")
    

strict = False[#](<#bittensor.core.settings.DEFAULTS.strict> "Link to this definition")
    

class subtensor[#](<#bittensor.core.settings.DEFAULTS.subtensor> "Link to this definition")
    

chain_endpoint[#](<#bittensor.core.settings.DEFAULTS.subtensor.chain_endpoint> "Link to this definition")
    

network[#](<#bittensor.core.settings.DEFAULTS.subtensor.network> "Link to this definition")
    

class wallet[#](<#bittensor.core.settings.DEFAULTS.wallet> "Link to this definition")
    

hotkey[#](<#bittensor.core.settings.DEFAULTS.wallet.hotkey> "Link to this definition")
    

name[#](<#bittensor.core.settings.DEFAULTS.wallet.name> "Link to this definition")
    

path[#](<#bittensor.core.settings.DEFAULTS.wallet.path> "Link to this definition")
    

bittensor.core.settings.DEFAULT_ENDPOINT = 'wss://entrypoint-finney.opentensor.ai:443'[#](<#bittensor.core.settings.DEFAULT_ENDPOINT> "Link to this definition")
    

bittensor.core.settings.DEFAULT_MEV_PROTECTION[#](<#bittensor.core.settings.DEFAULT_MEV_PROTECTION> "Link to this definition")
    

bittensor.core.settings.DEFAULT_NETWORK = 'finney'[#](<#bittensor.core.settings.DEFAULT_NETWORK> "Link to this definition")
    

bittensor.core.settings.DEFAULT_PERIOD = 128[#](<#bittensor.core.settings.DEFAULT_PERIOD> "Link to this definition")
    

bittensor.core.settings.FINNEY_ENTRYPOINT = 'wss://entrypoint-finney.opentensor.ai:443'[#](<#bittensor.core.settings.FINNEY_ENTRYPOINT> "Link to this definition")
    

bittensor.core.settings.FINNEY_TEST_ENTRYPOINT = 'wss://test.finney.opentensor.ai:443'[#](<#bittensor.core.settings.FINNEY_TEST_ENTRYPOINT> "Link to this definition")
    

bittensor.core.settings.HOME_DIR[#](<#bittensor.core.settings.HOME_DIR> "Link to this definition")
    

bittensor.core.settings.LATENT_LITE_ENTRYPOINT = 'wss://lite.sub.latent.to:443'[#](<#bittensor.core.settings.LATENT_LITE_ENTRYPOINT> "Link to this definition")
    

bittensor.core.settings.LOCAL_ENTRYPOINT[#](<#bittensor.core.settings.LOCAL_ENTRYPOINT> "Link to this definition")
    

bittensor.core.settings.MAX_MEV_SHIELD_PERIOD = 8[#](<#bittensor.core.settings.MAX_MEV_SHIELD_PERIOD> "Link to this definition")
    

bittensor.core.settings.MINERS_DIR[#](<#bittensor.core.settings.MINERS_DIR> "Link to this definition")
    

bittensor.core.settings.MLKEM768_PUBLIC_KEY_SIZE = 1184[#](<#bittensor.core.settings.MLKEM768_PUBLIC_KEY_SIZE> "Link to this definition")
    

bittensor.core.settings.NETWORKS = ['finney', 'test', 'archive', 'local', 'latent-lite'][#](<#bittensor.core.settings.NETWORKS> "Link to this definition")
    

bittensor.core.settings.NETWORK_EXPLORER_MAP[#](<#bittensor.core.settings.NETWORK_EXPLORER_MAP> "Link to this definition")
    

bittensor.core.settings.NETWORK_MAP[#](<#bittensor.core.settings.NETWORK_MAP> "Link to this definition")
    

bittensor.core.settings.PIPADDRESS = 'https://pypi.org/pypi/bittensor/json'[#](<#bittensor.core.settings.PIPADDRESS> "Link to this definition")
    

bittensor.core.settings.RAO_SYMBOL: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.settings.RAO_SYMBOL> "Link to this definition")
    

bittensor.core.settings.READ_ONLY[#](<#bittensor.core.settings.READ_ONLY> "Link to this definition")
    

bittensor.core.settings.REVERSE_NETWORK_MAP[#](<#bittensor.core.settings.REVERSE_NETWORK_MAP> "Link to this definition")
    

bittensor.core.settings.ROOT_TAO_STAKE_WEIGHT = 0.18[#](<#bittensor.core.settings.ROOT_TAO_STAKE_WEIGHT> "Link to this definition")
    

bittensor.core.settings.SS58_ADDRESS_LENGTH = 48[#](<#bittensor.core.settings.SS58_ADDRESS_LENGTH> "Link to this definition")
    

bittensor.core.settings.TAO_APP_BLOCK_EXPLORER = 'https://www.tao.app/block/'[#](<#bittensor.core.settings.TAO_APP_BLOCK_EXPLORER> "Link to this definition")
    

bittensor.core.settings.TAO_SYMBOL: [str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)")[#](<#bittensor.core.settings.TAO_SYMBOL> "Link to this definition")
    

bittensor.core.settings.TYPE_REGISTRY: [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")[[str](<https://docs.python.org/3/library/stdtypes.html#str> "\(in Python v3.14\)"), [dict](<https://docs.python.org/3/library/stdtypes.html#dict> "\(in Python v3.14\)")][#](<#bittensor.core.settings.TYPE_REGISTRY> "Link to this definition")
    

bittensor.core.settings.USER_BITTENSOR_DIR[#](<#bittensor.core.settings.USER_BITTENSOR_DIR> "Link to this definition")
    

bittensor.core.settings.WALLETS_DIR[#](<#bittensor.core.settings.WALLETS_DIR> "Link to this definition")
    

bittensor.core.settings.version_as_int: [int](<https://docs.python.org/3/library/functions.html#int> "\(in Python v3.14\)")[#](<#bittensor.core.settings.version_as_int> "Link to this definition")
    

[ __ previous bittensor.core.metagraph ](<../metagraph/index.html> "previous page") [ next bittensor.core.stream __](<../stream/index.html> "next page")

__Contents

  * [Attributes](<#attributes>)
  * [Classes](<#classes>)
  * [Module Contents](<#module-contents>)
    * [`ARCHIVE_ENTRYPOINT`](<#bittensor.core.settings.ARCHIVE_ENTRYPOINT>)
    * [`BLOCKTIME`](<#bittensor.core.settings.BLOCKTIME>)
    * [`DEFAULTS`](<#bittensor.core.settings.DEFAULTS>)
      * [`DEFAULTS.axon`](<#bittensor.core.settings.DEFAULTS.axon>)
        * [`DEFAULTS.axon.external_ip`](<#bittensor.core.settings.DEFAULTS.axon.external_ip>)
        * [`DEFAULTS.axon.external_port`](<#bittensor.core.settings.DEFAULTS.axon.external_port>)
        * [`DEFAULTS.axon.ip`](<#bittensor.core.settings.DEFAULTS.axon.ip>)
        * [`DEFAULTS.axon.max_workers`](<#bittensor.core.settings.DEFAULTS.axon.max_workers>)
        * [`DEFAULTS.axon.port`](<#bittensor.core.settings.DEFAULTS.axon.port>)
      * [`DEFAULTS.config`](<#bittensor.core.settings.DEFAULTS.config>)
      * [`DEFAULTS.logging`](<#bittensor.core.settings.DEFAULTS.logging>)
        * [`DEFAULTS.logging.debug`](<#bittensor.core.settings.DEFAULTS.logging.debug>)
        * [`DEFAULTS.logging.enable_third_party_loggers`](<#bittensor.core.settings.DEFAULTS.logging.enable_third_party_loggers>)
        * [`DEFAULTS.logging.info`](<#bittensor.core.settings.DEFAULTS.logging.info>)
        * [`DEFAULTS.logging.logging_dir`](<#bittensor.core.settings.DEFAULTS.logging.logging_dir>)
        * [`DEFAULTS.logging.record_log`](<#bittensor.core.settings.DEFAULTS.logging.record_log>)
        * [`DEFAULTS.logging.trace`](<#bittensor.core.settings.DEFAULTS.logging.trace>)
      * [`DEFAULTS.no_version_checking`](<#bittensor.core.settings.DEFAULTS.no_version_checking>)
      * [`DEFAULTS.priority`](<#bittensor.core.settings.DEFAULTS.priority>)
        * [`DEFAULTS.priority.max_workers`](<#bittensor.core.settings.DEFAULTS.priority.max_workers>)
        * [`DEFAULTS.priority.maxsize`](<#bittensor.core.settings.DEFAULTS.priority.maxsize>)
      * [`DEFAULTS.strict`](<#bittensor.core.settings.DEFAULTS.strict>)
      * [`DEFAULTS.subtensor`](<#bittensor.core.settings.DEFAULTS.subtensor>)
        * [`DEFAULTS.subtensor.chain_endpoint`](<#bittensor.core.settings.DEFAULTS.subtensor.chain_endpoint>)
        * [`DEFAULTS.subtensor.network`](<#bittensor.core.settings.DEFAULTS.subtensor.network>)
      * [`DEFAULTS.wallet`](<#bittensor.core.settings.DEFAULTS.wallet>)
        * [`DEFAULTS.wallet.hotkey`](<#bittensor.core.settings.DEFAULTS.wallet.hotkey>)
        * [`DEFAULTS.wallet.name`](<#bittensor.core.settings.DEFAULTS.wallet.name>)
        * [`DEFAULTS.wallet.path`](<#bittensor.core.settings.DEFAULTS.wallet.path>)
    * [`DEFAULT_ENDPOINT`](<#bittensor.core.settings.DEFAULT_ENDPOINT>)
    * [`DEFAULT_MEV_PROTECTION`](<#bittensor.core.settings.DEFAULT_MEV_PROTECTION>)
    * [`DEFAULT_NETWORK`](<#bittensor.core.settings.DEFAULT_NETWORK>)
    * [`DEFAULT_PERIOD`](<#bittensor.core.settings.DEFAULT_PERIOD>)
    * [`FINNEY_ENTRYPOINT`](<#bittensor.core.settings.FINNEY_ENTRYPOINT>)
    * [`FINNEY_TEST_ENTRYPOINT`](<#bittensor.core.settings.FINNEY_TEST_ENTRYPOINT>)
    * [`HOME_DIR`](<#bittensor.core.settings.HOME_DIR>)
    * [`LATENT_LITE_ENTRYPOINT`](<#bittensor.core.settings.LATENT_LITE_ENTRYPOINT>)
    * [`LOCAL_ENTRYPOINT`](<#bittensor.core.settings.LOCAL_ENTRYPOINT>)
    * [`MAX_MEV_SHIELD_PERIOD`](<#bittensor.core.settings.MAX_MEV_SHIELD_PERIOD>)
    * [`MINERS_DIR`](<#bittensor.core.settings.MINERS_DIR>)
    * [`MLKEM768_PUBLIC_KEY_SIZE`](<#bittensor.core.settings.MLKEM768_PUBLIC_KEY_SIZE>)
    * [`NETWORKS`](<#bittensor.core.settings.NETWORKS>)
    * [`NETWORK_EXPLORER_MAP`](<#bittensor.core.settings.NETWORK_EXPLORER_MAP>)
    * [`NETWORK_MAP`](<#bittensor.core.settings.NETWORK_MAP>)
    * [`PIPADDRESS`](<#bittensor.core.settings.PIPADDRESS>)
    * [`RAO_SYMBOL`](<#bittensor.core.settings.RAO_SYMBOL>)
    * [`READ_ONLY`](<#bittensor.core.settings.READ_ONLY>)
    * [`REVERSE_NETWORK_MAP`](<#bittensor.core.settings.REVERSE_NETWORK_MAP>)
    * [`ROOT_TAO_STAKE_WEIGHT`](<#bittensor.core.settings.ROOT_TAO_STAKE_WEIGHT>)
    * [`SS58_ADDRESS_LENGTH`](<#bittensor.core.settings.SS58_ADDRESS_LENGTH>)
    * [`TAO_APP_BLOCK_EXPLORER`](<#bittensor.core.settings.TAO_APP_BLOCK_EXPLORER>)
    * [`TAO_SYMBOL`](<#bittensor.core.settings.TAO_SYMBOL>)
    * [`TYPE_REGISTRY`](<#bittensor.core.settings.TYPE_REGISTRY>)
    * [`USER_BITTENSOR_DIR`](<#bittensor.core.settings.USER_BITTENSOR_DIR>)
    * [`WALLETS_DIR`](<#bittensor.core.settings.WALLETS_DIR>)
    * [`version_as_int`](<#bittensor.core.settings.version_as_int>)



By Opentensor Foundation 

© Copyright 2025, Opentensor Foundation.