import asyncio
import os
import json
import aiohttp
from pydantic import BaseModel, Field
from typing import Type, Optional

from lomen.plugins.base import BaseTool


# --- Pydantic Schemas ---
class GetTokenInfoBySymbolParams(BaseModel):
    symbol: str = Field(..., description="The token symbol (e.g., 'USDC', 'ETH').")
    chain_id: int = Field(..., description="The chain ID where the token exists.")


class GetTokenInfoByAddressParams(BaseModel):
    token_address: str = Field(..., description="The contract address of the token.")
    chain_id: int = Field(..., description="The chain ID where the token exists.")


# --- Tool Implementations ---
class GetTokenInfoBySymbol(BaseTool):
    """
    Fetches information (name, decimals, address, logo, market cap) for a token by its symbol on a specific chain using the 1inch API.
    It first checks a local cache (`src/lomen/plugins/tokens/{chain_id}.json`) before querying the API.
    """

    name = "get_token_info_by_symbol"

    def get_params(self) -> Type[BaseModel]:
        """Returns the Pydantic schema for the tool's arguments."""
        return GetTokenInfoBySymbolParams

    def _check_local_cache(self, symbol: str, chain_id: int) -> Optional[dict]:
        """Checks the local JSON cache for the token."""
        # Adjusted path relative to the 'src' directory
        tokens_file_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(__file__))
            ),  # Moves up three levels from tools/ -> oneinch/ -> plugins/
            "tokens",
            f"{chain_id}.json",
        )
        if os.path.exists(tokens_file_path):
            try:
                with open(tokens_file_path, "r") as f:
                    tokens_data = json.load(f)
                # Search case-insensitively
                for token_info in tokens_data.values():
                    if token_info.get("symbol", "").upper() == symbol.upper():
                        return token_info
            except (json.JSONDecodeError, IOError) as e:
                # Log or handle error reading local file if necessary, but proceed to API
                print(
                    f"Warning: Error reading local token file {tokens_file_path}: {e}"
                )
        return None

    async def _call_api(self, symbol: str, chain_id: int, api_key: str):
        """Internal async method to call the 1inch API."""
        if not symbol:
            raise ValueError("Token symbol must be provided.")
        if not chain_id:
            raise ValueError("Chain ID must be provided.")
        if not api_key:
            raise ValueError(
                "1inch API key not found. Set the ONEINCH_API_KEY environment variable."
            )

        headers = {"Authorization": f"Bearer {api_key}"}
        # Parameters from original code
        only_positive_rating = True
        country = "US"
        endpoint = f"https://api.1inch.dev/token/v1.2/{chain_id}/search?query={symbol}&only_positive_rating={only_positive_rating}&limit=1&country={country}"

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
                if not data:
                    raise ValueError(
                        f"Token symbol '{symbol}' not found on chain {chain_id} via 1inch API."
                    )
                # API returns a list, take the first element
                return data[0]

    # Keep a basic run method for potential sync-only adapters
    def run(self, *args, **kwargs):
        """Synchronous execution is not recommended for this I/O-bound tool. Use arun."""
        raise NotImplementedError("Use the asynchronous 'arun' method for this tool.")

    async def arun(self, symbol: str, chain_id: int):
        """
        Asynchronously fetches token information by symbol.

        Args:
            symbol: The token symbol.
            chain_id: The chain ID.

        Returns:
            A dictionary containing token information.

        Raises:
            ValueError: If required parameters or API key are missing, or token not found.
            PermissionError: If the API key is invalid.
            Exception: For API, network, or file errors.
        """
        # 1. Check local cache first
        cached_token = self._check_local_cache(symbol=symbol, chain_id=chain_id)
        if cached_token:
            print(f"Found token '{symbol}' on chain {chain_id} in local cache.")
            return cached_token

        # 2. If not in cache, call API
        print(
            f"Token '{symbol}' not in cache for chain {chain_id}, querying 1inch API..."
        )
        api_key = os.getenv("ONEINCH_API_KEY")
        try:
            # Directly await the internal async method
            result = await self._call_api(
                symbol=symbol, chain_id=chain_id, api_key=api_key
            )
            return result
        except (ValueError, PermissionError) as e:
            raise e
        except aiohttp.ClientError as e:
            raise Exception(f"Network error contacting 1inch API: {e}") from e
        except Exception as e:
            raise Exception(
                f"Failed to get token info for symbol '{symbol}' on chain {chain_id}: {e}"
            ) from e


class GetTokenInfoByAddress(BaseTool):
    """
    Fetches information (symbol, name, decimals, logo, market cap) for a token by its contract address on a specific chain using the 1inch API.
    """

    name = "get_token_info_by_address"

    def get_params(self) -> Type[BaseModel]:
        """Returns the Pydantic schema for the tool's arguments."""
        return GetTokenInfoByAddressParams

    async def _call_api(self, token_address: str, chain_id: int, api_key: str):
        """Internal async method to call the 1inch API."""
        if not token_address:
            raise ValueError("Token address must be provided.")
        if not chain_id:
            raise ValueError("Chain ID must be provided.")
        if not api_key:
            raise ValueError(
                "1inch API key not found. Set the ONEINCH_API_KEY environment variable."
            )

        headers = {"Authorization": f"Bearer {api_key}"}
        endpoint = f"https://api.1inch.dev/token/v1.2/{chain_id}/custom/{token_address}"

        async with aiohttp.ClientSession() as session:
            async with session.get(endpoint, headers=headers) as response:
                if response.status == 401:
                    raise PermissionError("Invalid or missing 1inch API key.")
                if response.status != 200:
                    error_text = await response.text()
                    # Check for specific 404 for better error message
                    if response.status == 404:
                        raise ValueError(
                            f"Token address '{token_address}' not found on chain {chain_id} via 1inch API."
                        )
                    raise Exception(
                        f"1inch API error (Status {response.status}): {error_text}"
                    )
                data = await response.json()
                return data

    # Keep a basic run method for potential sync-only adapters
    def run(self, *args, **kwargs):
        """Synchronous execution is not recommended for this I/O-bound tool. Use arun."""
        raise NotImplementedError("Use the asynchronous 'arun' method for this tool.")

    async def arun(self, token_address: str, chain_id: int):
        """
        Asynchronously fetches token information by address.

        Args:
            token_address: The token contract address.
            chain_id: The chain ID.

        Returns:
            A dictionary containing token information.

        Raises:
            ValueError: If required parameters or API key are missing, or token not found.
            PermissionError: If the API key is invalid.
            Exception: For API or network errors.
        """
        api_key = os.getenv("ONEINCH_API_KEY")
        try:
            # Directly await the internal async method
            result = await self._call_api(
                token_address=token_address, chain_id=chain_id, api_key=api_key
            )
            return result
        except (ValueError, PermissionError) as e:
            raise e
        except aiohttp.ClientError as e:
            raise Exception(f"Network error contacting 1inch API: {e}") from e
        except Exception as e:
            raise Exception(
                f"Failed to get token info for address '{token_address}' on chain {chain_id}: {e}"
            ) from e
