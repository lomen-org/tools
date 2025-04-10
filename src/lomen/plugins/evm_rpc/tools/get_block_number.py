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
