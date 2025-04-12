import asyncio
import os
import aiohttp
from pydantic import BaseModel, Field
from typing import Type, Optional, List

from lomen.plugins.base import BaseTool

# Define supported chains for NFTs based on original description
NFT_SUPPORTED_CHAIN_IDS = [1, 137, 42161, 43114, 100, 8217, 10, 8453]
NFT_SUPPORTED_CHAIN_IDS_STR = ", ".join(map(str, NFT_SUPPORTED_CHAIN_IDS))


# --- Pydantic Schema ---
class GetNFTsForAddressParams(BaseModel):
    address: str = Field(
        ..., description="The wallet address (e.g., 0x...) to get NFTs for."
    )
    # Store chain_ids as a list of integers for easier validation
    chain_ids: List[int] = Field(
        ...,
        description=f"A list of chain IDs to search for NFTs. Supported: {NFT_SUPPORTED_CHAIN_IDS_STR}.",
    )
    limit: Optional[int] = Field(
        25, description="Maximum number of NFTs to return (default 25, max 25)."
    )


# --- Tool Implementation ---
class GetNFTsForAddress(BaseTool):
    """
    Fetches NFTs owned by a specific wallet address across one or more supported chains using the 1inch API.
    Supported chains: Ethereum (1), Polygon (137), Arbitrum (42161), Avalanche (43114), Gnosis (100), Klaytn (8217), Optimism (10), Base (8453).
    """

    name = "get_nfts_for_address"

    def get_params(self) -> Type[BaseModel]:
        """Returns the Pydantic schema for the tool's arguments."""
        return GetNFTsForAddressParams

    async def _call_api(
        self, address: str, chain_ids: List[int], limit: int, api_key: str
    ):
        """Internal async method to call the 1inch API."""
        if not address:
            raise ValueError("Wallet address must be provided.")
        if not chain_ids:
            raise ValueError("At least one Chain ID must be provided.")
        # Validate chain IDs
        invalid_chains = [
            cid for cid in chain_ids if cid not in NFT_SUPPORTED_CHAIN_IDS
        ]
        if invalid_chains:
            raise ValueError(
                f"Unsupported chain IDs provided: {invalid_chains}. Supported: {NFT_SUPPORTED_CHAIN_IDS_STR}"
            )
        if not api_key:
            raise ValueError(
                "1inch API key not found. Set the ONEINCH_API_KEY environment variable."
            )
        if not 1 <= limit <= 25:
            raise ValueError("Limit must be between 1 and 25.")

        headers = {"Authorization": f"Bearer {api_key}"}
        # Convert list of ints back to comma-separated string for API
        chain_ids_str = ",".join(map(str, chain_ids))
        endpoint = f"https://api.1inch.dev/nft/v2/byaddress?chainIds={chain_ids_str}&address={address}&limit={limit}"

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers) as response:
                if response.status == 401:
                    raise PermissionError("Invalid or missing 1inch API key.")
                # Handle 404 - likely means no NFTs found for the address/chain combo
                if response.status == 404:
                    return {"result": []}  # Return empty result list
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(
                        f"1inch API error (Status {response.status}): {error_text}"
                    )
                data = await response.json()
                # API returns {"result": [...]}
                return data  # Return the full response which includes 'result'

    # Keep a basic run method for potential sync-only adapters
    def run(self, *args, **kwargs):
        """Synchronous execution is not recommended for this I/O-bound tool. Use arun."""
        raise NotImplementedError("Use the asynchronous 'arun' method for this tool.")

    async def arun(self, address: str, chain_ids: List[int], limit: Optional[int] = 25):
        """
        Asynchronously fetches NFTs for the given address and chains.

        Args:
            address: The wallet address.
            chain_ids: A list of supported chain IDs.
            limit: Maximum number of NFTs to return (1-25, default 25).

        Returns:
            A dictionary containing the list of NFTs found (usually under the 'result' key).

        Raises:
            ValueError: If required parameters, API key are missing, or inputs are invalid.
            PermissionError: If the API key is invalid.
            Exception: For API or network errors.
        """
        # Ensure limit is within bounds even if default is used
        actual_limit = max(1, min(limit or 25, 25))

        api_key = os.getenv("ONEINCH_API_KEY")
        try:
            # Directly await the internal async method
            result = await self._call_api(
                address=address,
                chain_ids=chain_ids,
                limit=actual_limit,
                api_key=api_key,
            )
            return result
        except (ValueError, PermissionError) as e:
            raise e
        except aiohttp.ClientError as e:
            raise Exception(f"Network error contacting 1inch API: {e}") from e
        except Exception as e:
            raise Exception(
                f"Failed to get NFTs for address '{address}' on chains {chain_ids}: {e}"
            ) from e
