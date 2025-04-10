"""Parameter models for EVM RPC tools."""

from pydantic import BaseModel, Field
from typing import Optional, Union


class GetBlockNumberParameters(BaseModel):
    """Parameters for getting the current block number."""

    rpc_url: Optional[str] = Field(
        None,
        description="The RPC URL to use for the request. If not provided, will use the default RPC URL.",
    )
    chain_id: Optional[int] = Field(
        1, description="The chain ID to use. Defaults to 1 (Ethereum mainnet)"
    )


class GetBlockParameters(BaseModel):
    """Parameters for getting block information."""

    block_number: Optional[Union[int, str]] = Field(
        "latest",
        description="The block number to get information for. Can be a number or 'latest', 'earliest', 'pending'",
    )
    full_transactions: Optional[bool] = Field(
        False, description="Whether to include full transaction objects in the response"
    )
    rpc_url: Optional[str] = Field(
        None,
        description="The RPC URL to use for the request. If not provided, get it from system prompt.",
    )
    chain_id: Optional[int] = Field(
        1, description="The chain ID to use. Defaults to 1 (Ethereum mainnet)"
    )