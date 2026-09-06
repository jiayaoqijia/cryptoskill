#!/usr/bin/env python3
"""
Smart Contract Deployer - Compile and deploy Solidity contracts.

Author: SpoonOS Contributor
Version: 1.0.0
"""

import os
import json
import sys
import subprocess
from typing import Optional, List, Any

# Ensure dependencies are installed
def install_dependencies():
    required = ["web3", "py-solc-x"]
    for package in required:
        try:
            __import__(package.replace("-", "_").split(".")[0])
        except ImportError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            except Exception as e:
                print(f"Error installing {package}: {e}")
                sys.exit(1)

install_dependencies()

from web3 import Web3
from solcx import compile_source, compile_files, install_solc

# Attempt to import BaseTool, handle running standalone for testing
try:
    from spoon_ai.tools.base import BaseTool
except ImportError:
    from pydantic import BaseModel, Field
    class BaseTool(BaseModel):
        name: str
        description: str
        parameters: dict
        async def execute(self, **kwargs): pass

from pydantic import Field

class ContractDeployerTool(BaseTool):
    name: str = "deploy_contract"
    description: str = "Compiles and deploys a Solidity smart contract to an EVM chain."
    parameters: dict = Field(default={
        "type": "object",
        "properties": {
            "source_code": {
                "type": "string",
                "description": "Solidity source code"
            },
            "file_path": {
                "type": "string",
                "description": "Path to .sol file"
            },
            "contract_name": {
                "type": "string",
                "description": "Name of the contract to deploy"
            },
            "rpc_url": {
                "type": "string",
                "description": "RPC URL for the blockchain"
            },
            "private_key": {
                "type": "string",
                "description": "Private key for signing transaction"
            },
            "constructor_args": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Arguments for the constructor"
            },
            "solc_version": {
                "type": "string",
                "description": "Solidity compiler version",
                "default": "0.8.19"
            }
        },
        "required": ["contract_name"]
    })

    async def execute(self, contract_name: str, source_code: str = None, file_path: str = None, rpc_url: str = None, private_key: str = None, constructor_args: List[Any] = None, solc_version: str = "0.8.19") -> str:
        """
        Compiles and deploys the contract.
        """
        if not source_code and not file_path:
            return "Error: Either 'source_code' or 'file_path' must be provided."

        # Install compiler
        try:
            install_solc(solc_version)
        except Exception as e:
             return f"Error installing solc version {solc_version}: {str(e)}"

        # Compile
        try:
            if source_code:
                compiled_sol = compile_source(source_code, solc_version=solc_version)
            else:
                compiled_sol = compile_files([file_path], solc_version=solc_version)
            
            contract_id = None
            # Find the contract interface
            for key in compiled_sol.keys():
                if f":{contract_name}" in key:
                    contract_id = key
                    break
            
            if not contract_id:
                # Fallback: check if the key IS the contract name (compile_source behavior sometimes)
                if contract_name in compiled_sol:
                    contract_id = contract_name
                else: 
                     # Try to find just by name match at end
                     for key in compiled_sol:
                         if key.endswith(contract_name):
                             contract_id = key
                             break
            
            if not contract_id:
                return f"Error: Contract '{contract_name}' not found in compilation output. Available: {list(compiled_sol.keys())}"

            contract_interface = compiled_sol[contract_id]
            abi = contract_interface['abi']
            bytecode = contract_interface['bin']

        except Exception as e:
            return f"Error during compilation: {str(e)}"

        # If no RPC Provided, just return the bytecode/ABI (dry-run mode)
        rpc_url = rpc_url or os.environ.get("WEB3_RPC_URL")
        if not rpc_url:
            return json.dumps({
                "message": "Compilation successful (Dry Run - No RPC)",
                "abi": abi,
                "bytecode_preview": bytecode[:64] + "..."
            }, indent=2)

        private_key = private_key or os.environ.get("PRIVATE_KEY")
        if not private_key:
             return "Error: Private key required for deployment."

        # Deploy
        try:
            w3 = Web3(Web3.HTTPProvider(rpc_url))
            if not w3.is_connected():
                return f"Error: Could not connect to RPC URL: {rpc_url}"

            account = w3.eth.account.from_key(private_key)
            Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
            
            # Build transaction
            construct_txn = Contract.constructor(*(constructor_args or [])).build_transaction({
                'from': account.address,
                'nonce': w3.eth.get_transaction_count(account.address),
            })

            # Sign and send
            signed = w3.eth.account.sign_transaction(construct_txn, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
            
            # Wait for receipt
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

            return json.dumps({
                "message": "Deployment successful",
                "contract_address": tx_receipt.contractAddress,
                "transaction_hash": tx_hash.hex(),
                "abi": abi
            }, indent=2)

        except Exception as e:
            return f"Error during deployment: {str(e)}"

if __name__ == "__main__":
    import asyncio
    
    async def main():
        tool = ContractDeployerTool()
        print("Contract Deployer Tool Standalone Mode")
        # Example dry run
        src = "pragma solidity ^0.8.0; contract Test { uint public x; }"
        print("Compiling test contract...")
        res = await tool.execute(contract_name="Test", source_code=src)
        print(res)

    asyncio.run(main())
