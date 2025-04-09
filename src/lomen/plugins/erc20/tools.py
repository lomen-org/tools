"""Tools for the ERC20 plugin."""

from typing import Any, Dict

from pydantic import BaseModel
from web3 import Web3


class BlockNumberTool:
    """Tool to fetch the current block number from an Ethereum node."""

    name = "erc20_block_number"

    class Params(BaseModel):
        """Parameters for the BlockNumberTool."""

        pass

    @classmethod
    def execute(cls, params: Params, credentials: Dict[str, Any]) -> int:
        """
        Fetch the current block number from the blockchain.

        Args:
            params: Tool parameters (none required for this tool)
            credentials: Dict containing RPC_URL

        Returns:
            Current block number as an integer
        """
        rpc_url = credentials["RPC_URL"]
        w3 = Web3(Web3.HTTPProvider(rpc_url))

        if not w3.is_connected():
            raise ConnectionError(f"Could not connect to node at {rpc_url}")

        return w3.eth.block_number
