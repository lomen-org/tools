"""Utility functions for EVM RPC tools."""

from web3 import Web3

# Default RPC URL to use if not provided
DEFAULT_RPC_URL = "https://eth.llamarpc.com"

# Web3 instance cache to avoid creating new instances for every request
_web3_instances = {}


def get_web3(rpc_url: str = None, chain_id: int = None) -> Web3:
    """Get or create a Web3 instance for the given RPC URL and chain ID.
    
    Args:
        rpc_url: RPC URL to connect to. Defaults to DEFAULT_RPC_URL.
        chain_id: Expected chain ID. Defaults to 1 (Ethereum mainnet).
        
    Returns:
        Web3 instance connected to the specified RPC URL.
        
    Raises:
        Exception: If the chain ID from the node doesn't match the expected chain ID.
    """
    rpc_url = rpc_url or DEFAULT_RPC_URL
    chain_id = chain_id or 1  # Default to Ethereum mainnet

    cache_key = f"{rpc_url}:{chain_id}"
    if cache_key not in _web3_instances:
        web3 = Web3(Web3.HTTPProvider(rpc_url))
        # Verify chain ID if specified
        if chain_id is not None:
            chain_id_from_node = web3.eth.chain_id
            if chain_id_from_node != chain_id:
                raise Exception(
                    f"Chain ID mismatch. Expected {chain_id}, got {chain_id_from_node}"
                )
        _web3_instances[cache_key] = web3
    return _web3_instances[cache_key]