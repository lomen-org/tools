import asyncio
import os
import aiohttp
from pydantic import BaseModel, Field
from typing import Type, Optional, Literal

from lomen.plugins.base import BaseTool

# Define supported timeranges
Timerange = Literal["1day", "1week", "1month", "1year", "3years"]


# --- Pydantic Schema ---
class GetProfitAndLossParams(BaseModel):
    address: str = Field(
        ...,
        description="The wallet address (e.g., 0x...) to get profit and loss for.",
    )
    chain_id: int = Field(..., description="The chain ID to get profit and loss for.")
    timerange: Optional[Timerange] = Field(
        None,
        description="Optional time range for PnL calculation (1day, 1week, 1month, 1year, 3years). Defaults to API's default if not provided.",
    )


# --- Tool Implementation ---
class GetProfitAndLoss(BaseTool):
    """
    Fetches the profit and loss (PnL) overview for a specific wallet address on a specific chain using the 1inch API.
    An optional time range can be specified.
    """

    name = "get_profit_and_loss"

    def __init__(self, api_key: str):
        """Initializes the tool with the 1inch API key."""
        if not api_key:
            raise ValueError("API key must be provided to GetProfitAndLoss tool.")
        self.api_key = api_key

    def get_params(self) -> Type[BaseModel]:
        """Returns the Pydantic schema for the tool's arguments."""
        return GetProfitAndLossParams

    async def _call_api(
        self, address: str, chain_id: int, timerange: Optional[str] = None
    ):
        """Internal async method to call the 1inch API using the stored key."""
        if not address:
            raise ValueError("Wallet address must be provided.")
        if not chain_id:
            raise ValueError("Chain ID must be provided.")
        # API key checked in __init__

        headers = {"Authorization": f"Bearer {self.api_key}"}
        endpoint = f"https://api.1inch.dev/portfolio/portfolio/v4/general/profit_and_loss?addresses={address}&chain_id={chain_id}"
        if timerange:
            endpoint += f"&timerange={timerange}"

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers) as response:
                if response.status == 401:
                    raise PermissionError("Invalid or missing 1inch API key.")
                # Handle potential 404 if address/chain combo is invalid for PnL
                if response.status == 404:
                    raise ValueError(
                        f"Could not calculate PnL for address '{address}' on chain {chain_id}. Check if the address is active or the chain is supported by 1inch PnL."
                    )
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(
                        f"1inch API error (Status {response.status}): {error_text}"
                    )
                data = await response.json()
                # API returns {"result": {...}}
                return data.get("result", data)

    # Keep a basic run method for potential sync-only adapters
    def run(self, *args, **kwargs):
        """Synchronous execution is not recommended for this I/O-bound tool. Use arun."""
        raise NotImplementedError("Use the asynchronous 'arun' method for this tool.")

    async def arun(
        self, address: str, chain_id: int, timerange: Optional[Timerange] = None
    ):
        """
        Asynchronously fetches the profit and loss data.

        Args:
            address: The wallet address.
            chain_id: The chain ID.
            timerange: Optional time range ('1day', '1week', '1month', '1year', '3years').

        Returns:
            A dictionary containing profit and loss data.

        Raises:
            ValueError: If required parameters or API key are missing, or address/chain invalid for PnL.
            PermissionError: If the API key is invalid.
            Exception: For API or network errors.
        """
        # API key is now accessed via self.api_key
        try:
            # Directly await the internal async method
            result = await self._call_api(
                address=address, chain_id=chain_id, timerange=timerange
            )
            return result
        except (ValueError, PermissionError) as e:
            raise e
        except aiohttp.ClientError as e:
            raise Exception(f"Network error contacting 1inch API: {e}") from e
        except Exception as e:
            raise Exception(
                f"Failed to get PnL for address '{address}' on chain {chain_id}: {e}"
            ) from e
