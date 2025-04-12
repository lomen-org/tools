"""Get block tool for EVM RPC plugin."""

from pydantic import BaseModel, Field
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

from lomen.plugins.base import BaseTool


class GetBlockParams(BaseModel):
    rpc_url: str = Field(..., description="The RPC URL for the blockchain")
    chain_id: int = Field(..., description="The chain ID for the blockchain")
    block_number: int = Field(..., description="The block number to fetch")
    full_transactions: bool = Field(
        ..., description="Whether to include full transactions"
    )
    is_poa: bool = Field(..., description="Whether the chain is a POA chain")


class GetBlock(BaseTool):
    """
    Fetch block information from the specified EVM blockchain.
    """

    name = "get_block"

    def run(
        self,
        rpc_url: str,
        chain_id: int,
        block_number: int,
        full_transactions: bool = False,
        is_poa: bool = False,
    ):
        """
        Fetch block information from the specified EVM blockchain.

        Args:
            params: Tool parameters including block_number, full_transactions, rpc_url,
            and chain_id
            credentials: Dictionary of credentials (not used for this tool)

        Returns:
            Dictionary containing block information
        """
        try:
            # Get a Web3 instance for the specified RPC URL and chain ID
            rpc_url = rpc_url
            web3 = Web3(Web3.HTTPProvider(rpc_url))

            if is_poa:
                web3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

            # Get block information
            block = web3.eth.get_block(
                block_number, full_transactions=full_transactions
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

    def get_params(self):
        return GetBlockParams
