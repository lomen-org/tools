"""Blockchain metadata tool for retrieving chain information."""

import json
import os
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field

from ...base import BaseTool


class BlockchainMetadataTool(BaseTool):
    """Tool to retrieve metadata for blockchain networks.

    This tool returns metadata for a specified blockchain network by chain ID, including:
    - Chain name
    - RPC URL endpoint
    - Block explorer URL
    - Native currency
    - Whether it's a testnet or mainnet

    You can use this tool whenever you need information about a specific blockchain
    without having to hardcode RPC URLs or explorer links in other tools.

    The following chains are supported:

    Mainnets:
    - 1: Ethereum Mainnet (ETH)
    - 10: Optimism (ETH)
    - 25: Cronos Mainnet (CRO)
    - 56: BNB Smart Chain (BNB)
    - 100: Gnosis Chain (xDAI)
    - 137: Polygon (MATIC)
    - 324: zkSync Era (ETH)
    - 5000: Mantle (MNT)
    - 8453: Base (ETH)
    - 42161: Arbitrum One (ETH)
    - 42220: Celo (CELO)
    - 43114: Avalanche C-Chain (AVAX)
    - 59144: Linea (ETH)
    - 534352: Scroll (ETH)

    Testnets:
    - 5: Goerli Testnet (ETH)
    - 97: BNB Smart Chain Testnet (BNB)
    - 11155111: Sepolia Testnet (ETH)
    - 80001: Polygon Mumbai Testnet (MATIC)
    - 421613: Arbitrum Goerli Testnet (ETH)

    Example:
      Input: {"chain_id": 1}
      Output: {
        "name": "Ethereum Mainnet",
        "rpc": "https://ethereum-rpc.publicnode.com",
        "explorer": "https://etherscan.io",
        "currency": "ETH",
        "is_testnet": false,
        "chain_id": 1
      }
    """

    name = "blockchain_metadata"

    class Params(BaseModel):
        """Parameters for getting blockchain metadata."""

        chain_id: Union[int, str] = Field(
            ...,
            description="The chain ID of the blockchain network to get metadata for.",
        )

    @classmethod
    def execute(cls, params: Params, credentials: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve metadata for the specified blockchain network.

        Args:
            params: Parameters including chain_id
            credentials: Not used for this tool

        Returns:
            Dictionary containing chain metadata (name, rpc, explorer, etc.)

        Raises:
            Exception: If the chain is not found
        """
        try:
            print("Executing blockchain_metadata tool with chain_id:", params.chain_id)
            # Read chains data from JSON file
            chains_file = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "chains.json"
            )
            with open(chains_file, "r") as f:
                chains = json.load(f)

            # Convert chain_id to string if it's an int or ensure it's a string otherwise
            chain_id = params.chain_id
            chain_id_str = str(chain_id)

            # Find chain by ID
            if chain_id_str in chains:
                result = chains[chain_id_str].copy()
                # Add chain_id to result (as int if possible)
                try:
                    result["chain_id"] = int(chain_id_str)
                except ValueError:
                    result["chain_id"] = chain_id_str
                return result
            else:
                raise Exception(f"Chain ID {chain_id} not found or not supported")

        except FileNotFoundError:
            raise Exception("Chains data file not found")
        except json.JSONDecodeError:
            raise Exception("Invalid chains data file format")
        except Exception as e:
            raise Exception(f"Failed to get blockchain metadata: {str(e)}")
