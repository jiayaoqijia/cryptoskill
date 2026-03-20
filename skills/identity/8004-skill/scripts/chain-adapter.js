#!/usr/bin/env node

/**
 * Multi-Chain Adapter for ERC-8004
 * Supports TRON (TRC-8004) and EVM chains (BSC, Ethereum, etc.)
 */

const TronWebModule = require('tronweb');
const TronWeb = TronWebModule.TronWeb || TronWebModule;
const { ethers } = require('ethers');

/**
 * Create chain client based on chain type
 */
async function createClient(chainConfig, privateKey = null) {
  const chainType = chainConfig.type;
  
  if (!chainType) {
    throw new Error('Chain type not specified in configuration');
  }
  
  if (chainType === 'tron') {
    return createTronClient(chainConfig, privateKey);
  } else if (chainType === 'evm') {
    return createEvmClient(chainConfig, privateKey);
  } else {
    throw new Error(`Unsupported chain type: ${chainType}`);
  }
}

/**
 * Create TRON client
 */
function createTronClient(networkConfig, privateKey = null) {
  const tronWeb = new TronWeb({
    fullHost: networkConfig.fullNode,
    privateKey: privateKey || undefined
  });
  
  // For read-only operations without private key, set a dummy address
  if (!privateKey) {
    // Use a valid TRON address for read-only calls (TRON Foundation address)
    tronWeb.defaultAddress = {
      hex: '410000000000000000000000000000000000000000',
      base58: 'T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb'
    };
  }
  
  return {
    type: 'tron',
    client: tronWeb,
    
    getAddress: () => {
      if (!privateKey) {
        throw new Error('Private key required for this operation');
      }
      return tronWeb.defaultAddress.base58;
    },
    
    getContract: async (abi, address) => {
      // TRON ABI is already in array format
      return await tronWeb.contract(abi, address);
    },
    
    callMethod: async (contract, method, ...args) => {
      // For read-only calls, TronWeb needs the from address
      const options = {
        from: tronWeb.defaultAddress.base58
      };
      return await contract[method](...args).call(options);
    },
    
    sendTransaction: async (contract, method, options, ...args) => {
      if (!privateKey) {
        throw new Error('Private key required for transactions');
      }
      const tx = await contract[method](...args).send({
        feeLimit: options.feeLimit || 1000000000,
        callValue: options.value || 0
      });
      return tx;
    },
    
    formatAddress: (address) => {
      if (address.startsWith('0x')) {
        return tronWeb.address.fromHex(address);
      }
      return address;
    },
    
    toHex: (str) => tronWeb.toHex(str),
    
    sha3: (str) => tronWeb.sha3(str)
  };
}

/**
 * Create EVM client (BSC, Ethereum, etc.)
 */
function createEvmClient(networkConfig, privateKey = null) {
  const provider = new ethers.JsonRpcProvider(networkConfig.rpc);
  let wallet = null;
  
  if (privateKey) {
    // Ensure private key has "0x" prefix for ethers.js
    let formattedKey = privateKey.trim();
    if (!formattedKey.startsWith('0x')) {
      formattedKey = '0x' + formattedKey;
    }
    wallet = new ethers.Wallet(formattedKey, provider);
  }
  
  return {
    type: 'evm',
    client: wallet || provider,
    provider: provider,
    wallet: wallet,
    
    getAddress: () => {
      if (!wallet) throw new Error('Wallet not initialized');
      return wallet.address;
    },
    
    getContract: async (abi, address) => {
      // For EVM chains, ABI is already in correct format
      const iface = new ethers.Interface(abi);
      if (wallet) {
        return new ethers.Contract(address, iface, wallet);
      } else {
        return new ethers.Contract(address, iface, provider);
      }
    },
    
    callMethod: async (contract, method, ...args) => {
      return await contract[method](...args);
    },
    
    sendTransaction: async (contract, method, options, ...args) => {
      const txOptions = {};
      if (options.value) {
        txOptions.value = ethers.parseEther(options.value.toString());
      }
      
      const tx = await contract[method](...args, txOptions);
      const receipt = await tx.wait();
      return receipt.hash;
    },
    
    formatAddress: (address) => {
      return ethers.getAddress(address);
    },
    
    toHex: (str) => ethers.hexlify(ethers.toUtf8Bytes(str)),
    
    sha3: (str) => ethers.keccak256(ethers.toUtf8Bytes(str))
  };
}

/**
 * Convert TRON ABI to EVM ABI format
 */
function convertAbiToEvm(tronAbi) {
  function convertType(item) {
    const evmItem = {
      type: item.type,
      name: item.name,
      stateMutability: item.stateMutability
    };
    
    if (item.inputs) {
      evmItem.inputs = item.inputs.map(input => {
        const evmInput = {
          name: input.name,
          type: input.type
        };
        // Preserve components for tuple types
        if (input.components) {
          evmInput.components = input.components.map(comp => ({
            name: comp.name || comp.metadataKey || '',
            type: comp.type
          }));
        }
        return evmInput;
      });
    }
    
    if (item.outputs) {
      evmItem.outputs = item.outputs.map(output => {
        const evmOutput = {
          name: output.name || '',
          type: output.type
        };
        // Preserve components for tuple types
        if (output.components) {
          evmOutput.components = output.components.map(comp => ({
            name: comp.name || '',
            type: comp.type
          }));
        }
        return evmOutput;
      });
    }
    
    return evmItem;
  }
  
  return tronAbi.map(convertType);
}

module.exports = {
  createClient,
  createTronClient,
  createEvmClient,
  convertAbiToEvm
};
