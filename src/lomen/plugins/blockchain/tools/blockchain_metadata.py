import json
import os

from pydantic import BaseModel, Field

from lomen.plugins.base import BaseTool


class GetBlockchainMetadataParams(BaseModel):
    chain_id: int = Field(..., description="The chain ID for the blockchain")


class GetBlockchainMetadata(BaseTool):
    """
    Retrieve metadata for the specified blockchain network.
    """

    name = "get_blockchain_metadata"

    def get_params(self):
        return GetBlockchainMetadataParams

    def run(self, chain_id: int):
        """
        Retrieve metadata for the specified blockchain network.

        Supported chains and its IDs are:
        - Ethereum Mainnet: 1
        - Goerli Testnet: 5
        - Optimism: 10
        - Sepolia Testnet: 11155111
        - BNB Smart Chain: 56
        - BNB Smart Chain Testnet: 97
        - Polygon: 137
        - Polygon Mumbai Testnet: 80001
        - Arbitrum One: 42161
        - Arbitrum Goerli Testnet: 421613
        - Avalanche C-Chain: 43114
        - Gnosis Chain: 100
        - Cronos Mainnet: 25
        - zkSync Era: 324
        - Base: 8453
        - Linea: 59144
        - Mantle: 5000
        - Scroll: 534352
        - Celo: 42220

        Args:
            params: Parameters including chain_id
            credentials: Not used for this tool

        Returns:
            Dictionary containing chain metadata (name, rpc, explorer, etc.)

        Raises:
            Exception: If the chain is not found
        """
        try:
            print("Executing blockchain_metadata tool with chain_id:", chain_id)
            # Read chains data from JSON file
            chains_file = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "chains.json"
            )
            with open(chains_file, "r") as f:
                chains = json.load(f)

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
