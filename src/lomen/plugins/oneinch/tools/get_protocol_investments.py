import asyncio
import os
import aiohttp
from pydantic import BaseModel, Field
from typing import Type

from lomen.plugins.base import BaseTool


# --- Pydantic Schema ---
class GetProtocolInvestmentsParams(BaseModel):
    address: str = Field(
        ...,
        description="The wallet address (e.g., 0x...) to get DeFi protocol investments for.",
    )
    chain_id: int = Field(
        ..., description="The chain ID to check for protocol investments."
    )


# --- Tool Implementation ---
class GetProtocolInvestments(BaseTool):
    """
    Fetches the current value of DeFi protocol investments for a specific wallet address on a specific chain using the 1inch API.
    """

    name = "get_protocol_investments"

    def __init__(self, api_key: str):
        """Initializes the tool with the 1inch API key."""
        if not api_key:
            raise ValueError("API key must be provided to GetProtocolInvestments tool.")
        self.api_key = api_key

    def get_params(self) -> Type[BaseModel]:
        """Returns the Pydantic schema for the tool's arguments."""
        return GetProtocolInvestmentsParams

    async def _call_api(self, address: str, chain_id: int):
        """Internal async method to call the 1inch API using the stored key."""
        if not address:
            raise ValueError("Wallet address must be provided.")
        if not chain_id:
            raise ValueError("Chain ID must be provided.")
        # API key checked in __init__

        headers = {"Authorization": f"Bearer {self.api_key}"}
        endpoint = f"https://api.1inch.dev/portfolio/portfolio/v4/overview/protocols/current_value?addresses={address}&chain_id={chain_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers) as response:
                if response.status == 401:
                    raise PermissionError("Invalid or missing 1inch API key.")
                # Handle 404 if address/chain has no investments or is invalid
                if response.status == 404:
                    return (
                        []
                    )  # Return empty list if no investments found or invalid address/chain for this endpoint
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(
                        f"1inch API error (Status {response.status}): {error_text}"
                    )
                data = await response.json()
                # API returns {"result": [...]}
                return data.get("result", [])  # Return result or empty list

    # Keep a basic run method for potential sync-only adapters
    def run(self, *args, **kwargs):
        """Synchronous execution is not recommended for this I/O-bound tool. Use arun."""
        raise NotImplementedError("Use the asynchronous 'arun' method for this tool.")

    async def arun(self, address: str, chain_id: int):
        """
        Asynchronously fetches DeFi protocol investments.

        Args:
            address: The wallet address.
            chain_id: The chain ID.

        Returns:
            A list containing details of DeFi protocol investments, or an empty list if none found.

        Raises:
            ValueError: If required parameters or API key are missing.
            PermissionError: If the API key is invalid.
            Exception: For API or network errors.
        """
        # API key is now accessed via self.api_key
        try:
            # Directly await the internal async method
            result = await self._call_api(address=address, chain_id=chain_id)
            return result
        except (ValueError, PermissionError) as e:
            raise e
        except aiohttp.ClientError as e:
            raise Exception(f"Network error contacting 1inch API: {e}") from e
        except Exception as e:
            raise Exception(
                f"Failed to get protocol investments for address '{address}' on chain {chain_id}: {e}"
            ) from e
