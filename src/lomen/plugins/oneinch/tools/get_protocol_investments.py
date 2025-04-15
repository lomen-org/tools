import asyncio
import os
import aiohttp
from pydantic import BaseModel, Field
from typing import Type, List, Dict, Any, Optional

from lomen.plugins.base import BaseTool


# --- Pydantic Schema ---
class GetProtocolInvestmentsParams(BaseModel):
    address: str = Field(
        ...,
        description="The wallet address to check for protocol investments.",
        title="Wallet Address",
    )
    chain_id: int = Field(
        ...,
        description="The chain ID (e.g., 1 for Ethereum, 137 for Polygon) to analyze.",
        title="Chain ID",
    )


# --- Tool Implementation ---
class GetProtocolInvestments(BaseTool):
    """
    Fetches information about a wallet's investments in various DeFi protocols (e.g., Aave, Uniswap) using the 1inch API.
    """

    API_KEY_ENV = "ONEINCH_API_KEY"

    @property
    def name(self) -> str:
        """Name of the tool."""
        return "get_protocol_investments"

    @property
    def description(self) -> str:
        """Description of what the tool does."""
        return "Fetches information about a wallet's investments in various DeFi protocols (e.g., Aave, Uniswap) on a blockchain."

    def __init__(self):
        """Initializes the tool by retrieving the API key from environment."""
        self.api_key = os.environ.get(self.API_KEY_ENV)
        if not self.api_key:
            raise ValueError(f"{self.API_KEY_ENV} environment variable must be set.")

    def get_params(self) -> Type[BaseModel]:
        """Returns the Pydantic schema for the tool's arguments."""
        return GetProtocolInvestmentsParams

    async def _call_api(self, address: str, chain_id: int):
        """Internal async method to call the 1inch API using the stored key."""
        if not address:
            raise ValueError("Wallet address must be provided.")
        if not chain_id:
            raise ValueError("Chain ID must be provided.")

        headers = {"Authorization": f"Bearer {self.api_key}"}
        endpoint = f"https://api.1inch.dev/portfolio/v3/{chain_id}/protocols/{address}"

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

    def run(self, *args, **kwargs):
        """Synchronous execution is not recommended for this I/O-bound tool. Use arun."""
        raise NotImplementedError("Use the asynchronous 'arun' method for this tool.")

    async def arun(self, address: str, chain_id: int):
        """
        Asynchronously retrieves protocol investment information for a wallet on a specific chain.

        Args:
            address: The wallet address to analyze.
            chain_id: The chain ID to analyze.

        Returns:
            A dictionary containing protocol investment information for the wallet.

        Raises:
            ValueError: If required parameters or API key are missing.
            PermissionError: If the API key is invalid.
            Exception: For API or network errors.
        """
        try:
            result = await self._call_api(address=address, chain_id=chain_id)

            # Process and enrich the response
            processed_result = {
                "address": address,
                "chain_id": chain_id,
                "protocols": [],
                "total_invested_usd": 0,
                "protocol_count": 0,
            }

            # Extract protocol investment data
            if result and isinstance(result, list):
                for protocol in result:
                    protocol_data = {
                        "name": protocol.get("name", "Unknown Protocol"),
                        "adapter_id": protocol.get("adapter_id", ""),
                        "logo_uri": protocol.get("logo_uri", ""),
                        "positions": protocol.get("positions", []),
                        "total_value_usd": 0,
                    }

                    # Calculate total value in this protocol
                    for position in protocol_data["positions"]:
                        position_value = position.get("value_usd", 0)
                        protocol_data["total_value_usd"] += position_value

                    processed_result["protocols"].append(protocol_data)
                    processed_result["total_invested_usd"] += protocol_data[
                        "total_value_usd"
                    ]

                processed_result["protocol_count"] = len(processed_result["protocols"])

            return processed_result
        except (ValueError, PermissionError) as e:
            raise e
        except aiohttp.ClientError as e:
            raise Exception(f"Network error contacting 1inch API: {e}") from e
        except Exception as e:
            raise Exception(
                f"Failed to get protocol investments for address '{address}' on chain {chain_id}: {e}"
            ) from e
