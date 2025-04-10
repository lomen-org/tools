"""Get block number tool for EVM RPC plugin."""

from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from ...base import BaseTool
from ..utils import get_web3


class GetBlockNumberTool(BaseTool):
    """Tool to fetch the current block number from an EVM blockchain.

    These are the supported chains and it's RPC and chainId.
    Whenever you are using a chain, you can use the RPC URL and chainId to connect to the chain.
    Do not just use chainId, but use the RPC URL as well.
    """

    name = "evm_get_block_number"

    class Params(BaseModel):
        """Parameters for getting the current block number."""

        rpc_url: str = Field(
            None,
            description="The RPC URL to use for the request. If not provided, will use the default RPC URL.",
        )
        chain_id: int = Field(
            1, description="The chain ID to use. Defaults to 1 (Ethereum mainnet)"
        )

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
            rpc_url = params.rpc_url
            web3 = get_web3(rpc_url, params.chain_id)

            # Get the current block number
            block_number = web3.eth.block_number

            return {
                "block_number": block_number,
            }
        except Exception as e:
            raise Exception(f"Failed to get block number: {str(e)}")
