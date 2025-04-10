"""Get block tool for EVM RPC plugin."""

from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field

from ...base import BaseTool
from ..utils import get_web3


class GetBlockTool(BaseTool):
    """Tool to fetch block information from an EVM blockchain.

    This tool retrieves detailed information about a specific block from an
    Ethereum or other EVM-compatible blockchain. It can get the latest block
    or a specific block by number.

    The tool provides details such as:
    - Block hash
    - Timestamp
    - Miner address
    - Gas used/limit
    - List of transactions (can be full transaction objects or just hashes)
    - Parent hash
    - Other block metadata

    Use this tool when you need to:
    - Analyze specific blocks for transactions
    - Get block timestamps for time-based analysis
    - Verify block details or transaction inclusion
    - Track blockchain metrics over time

    - **Ethereum Mainnet**
    - Chain ID: 1
    - RPC URL: https://ethereum-rpc.publicnode.com

    - **BNB Smart Chain**
    - Chain ID: 56
    - RPC URL: https://bsc-rpc.publicnode.com

    - **Polygon**
    - Chain ID: 137
    - RPC URL: https://polygon-rpc.com

    - **Avalanche**
    - Chain ID: 43114
    - RPC URL: https://api.avax.network/ext/bc/C/rpc

    - **Arbitrum One**
    - Chain ID: 42161
    - RPC URL: https://arb1.arbitrum.io/rpc

    - **Optimism**
    - Chain ID: 10
    - RPC URL: https://mainnet.optimism.io

    - **Gnosis Chain**
    - Chain ID: 100
    - RPC URL: https://rpc.gnosischain.com

    - **Cronos**
    - Chain ID: 25
    - RPC URL: https://mainnet.cronoslabs.com/v1/02594d9ef6c0f4403a5374c3977725d62ffc4841113598314dfa58f8c88638ba

    - **zkSync Era**
    - Chain ID: 324
    - RPC URL: https://mainnet.era.zksync.io

    - **Base**
    - Chain ID: 8453
    - RPC URL: https://mainnet.base.org

    - **Linea**
    - Chain ID: 59144
    - RPC URL: https://linea-mainnet.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161

    - **Mantle**
    - Chain ID: 5000
    - RPC URL: https://rpc.mantle.xyz

    - **Scroll**
    - Chain ID: 53431
    - RPC URL: https://rpc.scroll.io

    - **Celo**

    - Chain ID: 42220
    - RPC URL: https://forno.celo.org
    """

    name = "evm_get_block"

    class Params(BaseModel):
        """Parameters for getting block information."""

        block_number: Optional[Union[int, str]] = Field(
            "latest",
            description="The block number to get information for. Can be a number or 'latest', 'earliest', 'pending'",
        )
        full_transactions: Optional[bool] = Field(
            False,
            description="Whether to include full transaction objects in the response",
        )
        rpc_url: str = Field(
            None,
            description="The RPC URL to use for the request. If not provided, get it from system prompt.",
        )
        chain_id: int = Field(
            1, description="The chain ID to use. Defaults to 1 (Ethereum mainnet)"
        )

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
            rpc_url = params.rpc_url
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
