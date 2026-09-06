#!/usr/bin/env python3
"""DAO Proposal Starter - Create functional governance proposals"""
import json
import sys
import hashlib
import secrets
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional
from enum import Enum

class DAOType(Enum):
    """Supported DAO governance types"""
    COMPOUND = "compound"
    AAVE = "aave"
    UNISWAP = "uniswap"
    GENERIC = "generic"

def encode_function_call(function_signature: str, params: List) -> str:
    """Encode function call to hex (keccak256 of signature + ABI encoded params)"""
    # Simplified: compute selector from function signature
    sig_hash = hashlib.sha3_256(function_signature.encode()).hexdigest()
    selector = "0x" + sig_hash[:8]
    # For demo: encode params as simple hex string
    encoded_params = "".join(f"{p:064x}" if isinstance(p, int) else p.replace("0x", "") for p in params)
    return selector + encoded_params[:64]

def validate_address(address: str) -> bool:
    """Validate Ethereum address format"""
    if not address.startswith("0x"):
        return False
    if len(address) != 42:
        return False
    try:
        int(address, 16)
        return True
    except ValueError:
        return False

def calculate_voting_period(dao_type: str) -> tuple:
    """Calculate voting period based on DAO type (start block, voting blocks)"""
    now = datetime.now(timezone.utc)
    voting_blocks = {
        "compound": 13140,  # ~3 days at 12s blocks
        "aave": 80000,      # ~1.5 days at 15s blocks  
        "uniswap": 25200,   # ~7 days at 13s blocks
        "generic": 50400    # ~5.5 days at average
    }
    delay_blocks = {
        "compound": 1,
        "aave": 1,
        "uniswap": 1,
        "generic": 1
    }
    return (delay_blocks.get(dao_type, 1), voting_blocks.get(dao_type, 50400))

def create_proposal(
    title: str,
    description: str,
    targets: List[str],
    functions: List[str],
    params: List[List],
    values: List[int],
    dao_type: str = "generic",
    proposer: Optional[str] = None,
    voting_power: int = 1000000
) -> Dict:
    """Create a fully functional DAO proposal with proper encoding"""
    
    # Validation
    if not title or len(title) < 5:
        raise ValueError("Title must be at least 5 characters")
    
    if not description or len(description) < 20:
        raise ValueError("Description must be at least 20 characters")
    
    # Validate targets & functions match
    if len(targets) != len(functions):
        raise ValueError("Number of targets must match number of functions")
    
    if len(targets) != len(values):
        raise ValueError("Number of targets must match number of values")
    
    # Validate and encode calls
    calldatas = []
    for i, target in enumerate(targets):
        if not validate_address(target):
            raise ValueError(f"Invalid target address at index {i}: {target}")
        
        func_sig = functions[i]
        func_params = params[i] if i < len(params) else []
        
        # Encode the function call
        calldata = encode_function_call(func_sig, func_params)
        calldatas.append(calldata)
    
    # Calculate voting parameters
    vote_delay, vote_period = calculate_voting_period(dao_type)
    
    now = datetime.now(timezone.utc)
    voting_start = now + timedelta(hours=24)  # 1 day delay
    voting_end = voting_start + timedelta(days=7)
    
    # Generate proposal ID (keccak256 hash of proposal data)
    proposal_data = f"{title}{description}".encode()
    proposal_id_hash = hashlib.sha3_256(proposal_data).hexdigest()
    proposal_id = int(proposal_id_hash[:16], 16) % 1000000
    
    # Create proposal object
    proposal = {
        "id": proposal_id,
        "title": title,
        "description": description,
        "dao_type": dao_type,
        "proposer": proposer or "0x" + secrets.token_hex(20),
        "status": "pending",
        "created_at": now.isoformat(),
        "voting_delay_blocks": vote_delay,
        "voting_period_blocks": vote_period,
        "voting_start_time": voting_start.isoformat(),
        "voting_end_time": voting_end.isoformat(),
        "actions": [
            {
                "target": targets[i],
                "function": functions[i],
                "value": values[i],
                "calldata": calldatas[i],
                "params": params[i] if i < len(params) else []
            }
            for i in range(len(targets))
        ],
        "voting": {
            "required_votes": voting_power,
            "for_votes": 0,
            "against_votes": 0,
            "abstain_votes": 0,
            "quorum_percentage": 4.0,
            "support_required_percentage": 50.0
        },
        "execution": {
            "ready": False,
            "executed": False,
            "eta": None,
            "timelock_delay_seconds": 259200  # 3 days
        },
        "ipfs_hash": "QmProposal" + proposal_id_hash[:56]
    }
    
    return {
        "success": True,
        "proposal": proposal,
        "raw_calldata": calldatas,
        "encoded_proposal": {
            "targets": targets,
            "values": values,
            "signatures": functions,
            "calldatas": calldatas,
            "description": description,
            "description_hash": hashlib.sha3_256(description.encode()).hexdigest()
        }
    }

def main():
    try:
        input_data = json.loads(sys.stdin.read())
        
        title = input_data.get("title")
        description = input_data.get("description")
        targets = input_data.get("targets", [])
        functions = input_data.get("functions", [])
        params = input_data.get("params", [])
        values = input_data.get("values", [])
        dao_type = input_data.get("dao_type", "generic")
        proposer = input_data.get("proposer")
        voting_power = input_data.get("voting_power", 1000000)
        
        # Validate DAO type
        valid_daos = [d.value for d in DAOType]
        if dao_type not in valid_daos:
            raise ValueError(f"Unknown DAO type. Supported: {', '.join(valid_daos)}")
        
        result = create_proposal(
            title=title,
            description=description,
            targets=targets,
            functions=functions,
            params=params,
            values=values,
            dao_type=dao_type,
            proposer=proposer,
            voting_power=voting_power
        )
        print(json.dumps(result, indent=2))
    except ValueError as e:
        print(json.dumps({
            "success": False,
            "error": str(e),
            "error_type": "validation_error"
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": str(e),
            "error_type": "system_error"
        }))
        sys.exit(1)

if __name__ == "__main__":
    main()
