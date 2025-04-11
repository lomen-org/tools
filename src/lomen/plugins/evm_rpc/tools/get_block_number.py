"""Get block number tool for EVM RPC plugin."""

from web3 import Web3


def get_block_number(rpc_url, chain_id):
    """
    Fetch the current block number from the specified EVM blockchain.

    Args:
        rpc_url: The RPC URL for the blockchain
        chain_id: The chain ID for the blockchain

    Returns:
        Dictionary containing the block number
    """
    try:
        # Get a Web3 instance for the specified RPC URL and chain ID
        web3 = Web3(Web3.HTTPProvider(rpc_url))

        # Get the current block number
        block_number = web3.eth.block_number

        return {
            "block_number": block_number,
        }
    except Exception as e:
        raise Exception(f"Failed to get block number: {str(e)}")
