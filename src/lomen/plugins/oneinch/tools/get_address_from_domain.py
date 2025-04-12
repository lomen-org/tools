import asyncio
import os
import aiohttp
from pydantic import BaseModel, Field
from typing import Type

from lomen.plugins.base import BaseTool


# --- Pydantic Schema ---
class GetDomainFromAddressParams(BaseModel):
    domain: str = Field(
        ...,
        description='The domain name to resolve (e.g., "vitalik.eth", "0x1234.lens"). Supported TLDs include .eth, .lens, .bnb, .base, .polygon, .avalanche, .optimism, .gnosis, .linea, .zksync, .arb, etc.',
        title="Domain Name",
    )


# --- Tool Implementation ---
class GetAddressFromDomain(BaseTool):
    """
    Resolves a blockchain domain name (like ENS, Lens) to its associated wallet address using the 1inch API.
    """

    name = "get_address_from_domain"

    def get_params(self) -> Type[BaseModel]:
        """Returns the Pydantic schema for the tool's arguments."""
        return GetDomainFromAddressParams

    async def _call_api(self, domain: str, api_key: str):
        """Internal async method to call the 1inch API."""
        if not domain:
            raise ValueError("Domain name must be provided.")
        if not api_key:
            raise ValueError(
                "1inch API key not found. Set the ONEINCH_API_KEY environment variable."
            )

        headers = {"Authorization": f"Bearer {api_key}"}
        endpoint = f"https://api.1inch.dev/domains/v2.0/lookup?name={domain}"

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
                # Assuming the API returns {"result": "0x..."} or similar on success
                return data.get(
                    "result", data
                )  # Return result field or full data if 'result' not present

    # Keep a basic run method for potential sync-only adapters, though MCP will use arun
    def run(self, *args, **kwargs):
        """Synchronous execution is not recommended for this I/O-bound tool. Use arun."""
        raise NotImplementedError("Use the asynchronous 'arun' method for this tool.")

    async def arun(self, domain: str):
        """
        Asynchronously executes the domain resolution.

        Args:
            domain: The domain name to resolve.

        Returns:
            The resolved wallet address or related information from the API.

        Raises:
            ValueError: If the domain name or API key is missing.
            PermissionError: If the API key is invalid.
            Exception: For other API or network errors.
        """
        api_key = os.getenv("ONEINCH_API_KEY")
        try:
            # Directly await the internal async method
            result = await self._call_api(domain=domain, api_key=api_key)
            return result
        except (ValueError, PermissionError) as e:
            # Re-raise specific errors
            raise e
        except aiohttp.ClientError as e:
            raise Exception(f"Network error contacting 1inch API: {e}") from e
        except Exception as e:
            # Catch other potential errors during async execution or API interaction
            raise Exception(f"Failed to resolve domain '{domain}': {e}") from e
