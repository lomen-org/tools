"""Get block number tool for EVM RPC plugin."""

from typing import Any, Dict

from ...base import BaseTool
from ..parameters import GetBlockNumberParameters
from ..utils import get_web3, DEFAULT_RPC_URL


class GetBlockNumberTool(BaseTool):
    """Tool to fetch the current block number from an EVM blockchain."""

    name = "evm_get_block_number"

    class Params(GetBlockNumberParameters):
        """Parameters for the GetBlockNumberTool."""
        pass

    @classmethod
    def execute(cls, params: Params, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Fetch the current block number from the specified EVM blockchain.

        Args:
            params: Tool parameters including rpc_url and chain_id
            credentials: Dictionary of credentials (not used for this tool)

        Returns:
            Dictionary containing the block number
        """
        try:
            # Get a Web3 instance for the specified RPC URL and chain ID
            rpc_url = params.rpc_url or credentials.get("RPC_URL", DEFAULT_RPC_URL)
            web3 = get_web3(rpc_url, params.chain_id)
            
            # Get the current block number
            block_number = web3.eth.block_number
            
            return {
                "block_number": block_number,
            }
        except Exception as e:
            raise Exception(f"Failed to get block number: {str(e)}")