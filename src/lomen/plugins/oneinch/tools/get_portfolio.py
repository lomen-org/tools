import asyncio
import os
import aiohttp
from pydantic import BaseModel, Field
from typing import Type, List

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
        description="The wallet address (e.g., 0x...) to get the portfolio for.",
    )
    chain_id: int = Field(
        ...,
        description=f"The chain ID. Supported: {', '.join(str(c['id']) for c in INCH1_SUPPORTED_CHAIN_IDS)}.",
    )


class GetPortfolioForAllChainsParams(BaseModel):
    address: str = Field(
        ...,
        description="The wallet address (e.g., 0x...) to get the portfolio for across all supported chains.",
    )


# --- Tool Implementations ---
class GetPortfolio(BaseTool):
    """
    Fetches the ERC20 token portfolio overview for a specific wallet address on a single supported chain using the 1inch API.
    Supported chains: Ethereum (1), Arbitrum (42161), BNB Chain (56), Gnosis (100), Optimism (10), Polygon (137), Base (8453), ZKsync Era (324), Linea (59144), Avalanche (43114).
    """

    name = "get_portfolio"

    def get_params(self) -> Type[BaseModel]:
        """Returns the Pydantic schema for the tool's arguments."""
        return GetPortfolioParams

    async def _call_api(self, address: str, chain_id: int, api_key: str):
        """Internal async method to call the 1inch API."""
        if not address:
            raise ValueError("Wallet address must be provided.")
        if not chain_id:
            raise ValueError("Chain ID must be provided.")
        if chain_id not in SUPPORTED_CHAIN_IDS_SET:
            supported_ids = ", ".join(str(c["id"]) for c in INCH1_SUPPORTED_CHAIN_IDS)
            raise ValueError(
                f"Chain ID {chain_id} is not supported by this tool. Supported IDs: {supported_ids}"
            )
        if not api_key:
            raise ValueError(
                "1inch API key not found. Set the ONEINCH_API_KEY environment variable."
            )

        headers = {"Authorization": f"Bearer {api_key}"}
        endpoint = f"https://api.1inch.dev/portfolio/portfolio/v4/overview/erc20/details?addresses={address}&chain_id={chain_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers) as response:
                if response.status == 401:
                    raise PermissionError("Invalid or missing 1inch API key.")
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(
                        f"1inch API error (Status {response.status}): {error_text}"
                    )
                data = await response.json()
                # API returns {"result": [...]}
                return data.get("result", data)

    # Keep a basic run method for potential sync-only adapters
    def run(self, *args, **kwargs):
        """Synchronous execution is not recommended for this I/O-bound tool. Use arun."""
        raise NotImplementedError("Use the asynchronous 'arun' method for this tool.")

    async def arun(self, address: str, chain_id: int):
        """
        Asynchronously fetches the portfolio for a single chain.

        Args:
            address: The wallet address.
            chain_id: The supported chain ID.

        Returns:
            A list containing portfolio details for the specified chain.

        Raises:
            ValueError: If required parameters, API key are missing, or chain ID is unsupported.
            PermissionError: If the API key is invalid.
            Exception: For API or network errors.
        """
        api_key = os.getenv("ONEINCH_API_KEY")
        try:
            # Directly await the internal async method
            result = await self._call_api(
                address=address, chain_id=chain_id, api_key=api_key
            )
            return result
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
    Fetches the ERC20 token portfolio overview for a specific wallet address across all supported chains sequentially using the 1inch API.
    Use this only when explicitly asked for all chains, as it makes multiple API calls.
    Supported chains: Ethereum (1), Arbitrum (42161), BNB Chain (56), Gnosis (100), Optimism (10), Polygon (137), Base (8453), ZKsync Era (324), Linea (59144), Avalanche (43114).
    """

    name = "get_portfolio_all_chains"

    def get_params(self) -> Type[BaseModel]:
        """Returns the Pydantic schema for the tool's arguments."""
        return GetPortfolioForAllChainsParams

    async def _call_individual_chain(
        self, session, address: str, chain: dict, api_key: str
    ) -> dict:
        """Calls the API for a single chain."""
        endpoint = f"https://api.1inch.dev/portfolio/portfolio/v4/overview/erc20/details?addresses={address}&chain_id={chain['id']}"
        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            async with session.get(endpoint, headers=headers) as response:
                if response.status == 401:
                    # Don't retry on auth errors
                    return {
                        "chain_name": chain["name"],
                        "chain_id": chain["id"],
                        "error": "Invalid or missing 1inch API key.",
                    }
                if response.status != 200:
                    error_text = await response.text()
                    return {
                        "chain_name": chain["name"],
                        "chain_id": chain["id"],
                        "error": f"API Error (Status {response.status}): {error_text}",
                    }
                data = await response.json()
                return {
                    "chain_name": chain["name"],
                    "chain_id": chain["id"],
                    "portfolio": data.get(
                        "result", []
                    ),  # Default to empty list if 'result' is missing
                }
        except aiohttp.ClientError as e:
            return {
                "chain_name": chain["name"],
                "chain_id": chain["id"],
                "error": f"Network Error: {e}",
            }
        except Exception as e:
            return {
                "chain_name": chain["name"],
                "chain_id": chain["id"],
                "error": f"Unexpected Error: {e}",
            }

    async def _call_all_apis(self, address: str, api_key: str):
        """Internal async method to call the 1inch API for all supported chains."""
        if not address:
            raise ValueError("Wallet address must be provided.")
        if not api_key:
            raise ValueError(
                "1inch API key not found. Set the ONEINCH_API_KEY environment variable."
            )

        results = []
        async with aiohttp.ClientSession() as session:
            tasks = []
            for chain in INCH1_SUPPORTED_CHAIN_IDS:
                # Create task for each chain
                tasks.append(
                    self._call_individual_chain(session, address, chain, api_key)
                )
                # Introduce delay between starting tasks to avoid rate limiting
                await asyncio.sleep(
                    1.1
                )  # Slightly more than 1s as per original code's implication

            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks)

        return results

    # Keep a basic run method for potential sync-only adapters
    def run(self, *args, **kwargs):
        """Synchronous execution is not recommended for this I/O-bound tool. Use arun."""
        raise NotImplementedError("Use the asynchronous 'arun' method for this tool.")

    async def arun(self, address: str):
        """
        Asynchronously fetches the portfolio across all supported chains.

        Args:
            address: The wallet address.

        Returns:
            A list of dictionaries, each containing the chain name, ID, and portfolio data (or an error message) for that chain.

        Raises:
            ValueError: If the address or API key is missing.
            Exception: For errors during the process.
        """
        api_key = os.getenv("ONEINCH_API_KEY")
        try:
            # Directly await the internal async method
            result = await self._call_all_apis(address=address, api_key=api_key)
            return result
        except (
            ValueError,
            PermissionError,
        ) as e:  # PermissionError might be raised by _call_api if hit early
            raise e
        except Exception as e:
            # Catch other potential errors during async execution
            raise Exception(
                f"Failed to get portfolio for address '{address}' across all chains: {e}"
            ) from e
