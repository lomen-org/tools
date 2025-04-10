"""Get block tool for EVM RPC plugin."""

from typing import Any, Dict

from ...base import BaseTool
from ..parameters import GetBlockParameters
from ..utils import get_web3, DEFAULT_RPC_URL


class GetBlockTool(BaseTool):
    """Tool to fetch block information from an EVM blockchain."""

    name = "evm_get_block"

    class Params(GetBlockParameters):
        """Parameters for the GetBlockTool."""
        pass

    @classmethod
    def execute(cls, params: Params, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch block information from the specified EVM blockchain.

        Args:
            params: Tool parameters including block_number, full_transactions, rpc_url, and chain_id
            credentials: Dictionary of credentials (not used for this tool)

        Returns:
            Dictionary containing block information
        """
        try:
            # Get a Web3 instance for the specified RPC URL and chain ID
            rpc_url = params.rpc_url or credentials.get("RPC_URL", DEFAULT_RPC_URL)
            web3 = get_web3(rpc_url, params.chain_id)
            
            # Get block information
            block = web3.eth.get_block(
                params.block_number, full_transactions=params.full_transactions
            )
            
            # Convert block attributes to dict and handle any Web3.py specific types
            block_dict = dict(block)
            for key, value in block_dict.items():
                if isinstance(value, (bytes, bytearray)):
                    block_dict[key] = value.hex()
                elif (
                    isinstance(value, list)
                    and value
                    and isinstance(value[0], (bytes, bytearray))
                ):
                    block_dict[key] = [
                        item.hex() if isinstance(item, (bytes, bytearray)) else item
                        for item in value
                    ]
            
            return block_dict
        except Exception as e:
            raise Exception(f"Failed to get block: {str(e)}")