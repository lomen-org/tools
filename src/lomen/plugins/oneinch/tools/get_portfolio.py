import asyncio
import os
import aiohttp
from pydantic import BaseModel, Field
from typing import Type, List, Dict, Any, Optional

from lomen.plugins.base import BaseTool

# Define supported chains (as provided in the original code context, assuming INCH1_SUPPORTED_CHAIN_IDS exists)
# In a real scenario, this might be loaded from a config file or defined more robustly.
# For now, using a placeholder based on descriptions.
INCH1_SUPPORTED_CHAIN_IDS = [
    {"id": 1, "name": "Ethereum"},
    {"id": 42161, "name": "Arbitrum"},
    {"id": 56, "name": "BNB Chain"},
    {"id": 100, "name": "Gnosis"},
    {"id": 10, "name": "Optimism"},
    {"id": 137, "name": "Polygon"},
    {"id": 8453, "name": "Base"},
    {"id": 324, "name": "ZKsync Era"},
    {"id": 59144, "name": "Linea"},
    {"id": 43114, "name": "Avalanche"},
]
SUPPORTED_CHAIN_IDS_SET = {chain["id"] for chain in INCH1_SUPPORTED_CHAIN_IDS}


# --- Pydantic Schemas ---
class GetPortfolioParams(BaseModel):
    address: str = Field(
        ...,
        description="The wallet address to get portfolio data for.",
        title="Wallet Address",
    )
    chain_id: int = Field(
        ...,
        description="The chain ID where the portfolio should be retrieved. Common values: 1 (Ethereum), 137 (Polygon), 56 (BNB Chain), 42161 (Arbitrum), 10 (Optimism), etc.",
        title="Chain ID",
    )


class GetPortfolioAllChainsParams(BaseModel):
    address: str = Field(
        ...,
        description="The wallet address to get portfolio data for across all chains.",
        title="Wallet Address",
    )


# --- Tool Implementations ---
class GetPortfolio(BaseTool):
    """
    Fetches portfolio information (token balances, value, etc.) for a specific address on a single chain using the 1inch API.
    """

    name = "get_portfolio"
    API_KEY_ENV = "ONEINCH_API_KEY"

    def __init__(self):
        """Initializes the tool by retrieving the API key from environment."""
        self.api_key = os.environ.get(self.API_KEY_ENV)
        if not self.api_key:
            raise ValueError(f"{self.API_KEY_ENV} environment variable must be set.")

    def get_params(self) -> Type[BaseModel]:
        """Returns the Pydantic schema for the tool's arguments."""
        return GetPortfolioParams

    async def _call_api(self, address: str, chain_id: int):
        """Internal async method to call the 1inch API using the stored key."""
        if not address:
            raise ValueError("Wallet address must be provided.")
        if not chain_id:
            raise ValueError("Chain ID must be provided.")

        headers = {"Authorization": f"Bearer {self.api_key}"}
        endpoint = f"https://api.1inch.dev/portfolio/v3/{chain_id}/balances/{address}"

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers) as response:
                if response.status == 401:
                    raise PermissionError("Invalid or missing 1inch API key.")
                if response.status == 400:
                    error_text = await response.text()
                    try:
                        error_data = await response.json()
                        error_message = error_data.get("description", error_text)
                        raise ValueError(f"1inch API error: {error_message}")
                    except:
                        raise ValueError(f"1inch API error: {error_text}")
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(
                        f"1inch API error (Status {response.status}): {error_text}"
                    )
                data = await response.json()
                return data

    # Keep a basic run method for potential sync-only adapters
    def run(self, *args, **kwargs):
        """Synchronous execution is not recommended for this I/O-bound tool. Use arun."""
        raise NotImplementedError("Use the asynchronous 'arun' method for this tool.")

    async def arun(self, address: str, chain_id: int):
        """
        Asynchronously fetches portfolio information for a specific address on a single chain.

        Args:
            address: The wallet address to query.
            chain_id: The chain ID to query.

        Returns:
            A dictionary containing detailed portfolio information including token balances.

        Raises:
            ValueError: If required parameters or API key are missing.
            PermissionError: If the API key is invalid.
            Exception: For API or network errors.
        """
        try:
            result = await self._call_api(address=address, chain_id=chain_id)

            # Process the response to make it more useful
            processed_result = {
                "chain_id": chain_id,
                "address": address,
                "tokens": [],
                "total_usd_value": 0,
            }

            # Extract token balances and clean up the data
            if "balances" in result and isinstance(result["balances"], list):
                for token in result["balances"]:
                    token_data = {
                        "symbol": token.get("symbol", "Unknown"),
                        "name": token.get("name", "Unknown Token"),
                        "address": token.get("address", ""),
                        "decimals": token.get("decimals", 18),
                        "logo_uri": token.get("logo_uri", ""),
                        "amount": token.get("amount", 0),
                        "amount_usd": token.get("amount_usd", 0),
                    }
                    processed_result["tokens"].append(token_data)
                    processed_result["total_usd_value"] += token_data["amount_usd"]

            return processed_result
        except (ValueError, PermissionError) as e:
            raise e
        except aiohttp.ClientError as e:
            raise Exception(f"Network error contacting 1inch API: {e}") from e
        except Exception as e:
            raise Exception(
                f"Failed to get portfolio for address '{address}' on chain {chain_id}: {e}"
            ) from e


class GetPortfolioAllChains(BaseTool):
    """
    Fetches portfolio information (token balances, value) for a specific address across all supported chains using the 1inch API.
    """

    name = "get_portfolio_all_chains"
    API_KEY_ENV = "ONEINCH_API_KEY"

    def __init__(self):
        """Initializes the tool by retrieving the API key from environment."""
        self.api_key = os.environ.get(self.API_KEY_ENV)
        if not self.api_key:
            raise ValueError(f"{self.API_KEY_ENV} environment variable must be set.")
        # List of chain IDs supported by 1inch API
        self.supported_chains = [
            1,  # Ethereum
            56,  # BNB Chain
            137,  # Polygon
            10,  # Optimism
            42161,  # Arbitrum
            100,  # Gnosis
            8453,  # Base
            43114,  # Avalanche C-Chain
            250,  # Fantom
            324,  # zkSync Era
        ]

    def get_params(self) -> Type[BaseModel]:
        """Returns the Pydantic schema for the tool's arguments."""
        return GetPortfolioAllChainsParams

    async def _call_api(self, address: str, chain_ids: List[int]):
        """Internal async method to call the 1inch API for multiple chains."""
        if not address:
            raise ValueError("Wallet address must be provided.")
        if not chain_ids:
            raise ValueError("At least one chain ID must be provided.")

        # Create portfolio tool to reuse existing code
        portfolio_tool = GetPortfolio()

        # Use asyncio.gather to fetch all chains in parallel
        tasks = []
        for chain_id in chain_ids:
            # Create task for each chain
            task = asyncio.create_task(
                portfolio_tool.arun(address=address, chain_id=chain_id)
            )
            tasks.append((chain_id, task))

        # Wait for all tasks to complete and collect results
        results = {}
        for chain_id, task in tasks:
            try:
                # Get the result, suppress errors for individual chains
                chain_result = await task
                results[str(chain_id)] = chain_result
            except Exception as e:
                # For multi-chain queries, we don't want one failure to break everything
                # Just note the error but continue with other chains
                results[str(chain_id)] = {"error": str(e), "chain_id": chain_id}

        return results

    # Keep a basic run method for potential sync-only adapters
    def run(self, *args, **kwargs):
        """Synchronous execution is not recommended for this I/O-bound tool. Use arun."""
        raise NotImplementedError("Use the asynchronous 'arun' method for this tool.")

    async def arun(self, address: str):
        """
        Asynchronously fetches portfolio information for a specific address across all supported chains.

        Args:
            address: The wallet address to query.

        Returns:
            A dictionary containing portfolio information mapped by chain ID.

        Raises:
            ValueError: If required parameters or API key are missing.
            PermissionError: If the API key is invalid.
            Exception: For API or network errors.
        """
        try:
            # Call API with all supported chains
            results = await self._call_api(
                address=address, chain_ids=self.supported_chains
            )

            # Calculate total portfolio value across all chains
            total_portfolio_value = 0
            chains_with_assets = 0

            for chain_id, chain_data in results.items():
                if "total_usd_value" in chain_data:
                    total_portfolio_value += chain_data["total_usd_value"]
                    if chain_data["total_usd_value"] > 0:
                        chains_with_assets += 1

            # Add summary to the results
            summary = {
                "address": address,
                "total_value_usd": total_portfolio_value,
                "chains_with_assets": chains_with_assets,
                "chains_queried": len(self.supported_chains),
            }

            return {"summary": summary, "chains": results}
        except Exception as e:
            raise Exception(
                f"Failed to get portfolio for address '{address}' across all chains: {e}"
            ) from e
