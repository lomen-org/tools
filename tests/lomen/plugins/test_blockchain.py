import pytest
import aiohttp
import os
from unittest.mock import AsyncMock, patch

from lomen.plugins.evm_rpc import GetBlock, GetBlockNumber


@pytest.mark.asyncio
async def test_get_block():
    """Test GetBlock tool."""
    tool = GetBlock()
    rpc_url = "https://eth.llamarpc.com"
    chain_id = 1
    block_number = 123456

    mock_response = {
        "jsonrpc": "2.0",
        "id": 1,
        "result": {
            "number": "0x1e240",
            "hash": "0x...",
            "parentHash": "0x...",
            "transactions": [],
        },
    }

    async with aiohttp.ClientSession() as session:
        with patch.object(session, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value.__aenter__.return_value.json = AsyncMock(
                return_value=mock_response
            )
            with patch("aiohttp.ClientSession", return_value=session):
                result = await tool.arun(
                    rpc_url=rpc_url,
                    chain_id=chain_id,
                    block_number=block_number
                )
                assert isinstance(result, dict)


@pytest.mark.asyncio
async def test_get_block_number():
    """Test GetBlockNumber tool."""
    tool = GetBlockNumber()
    rpc_url = "https://eth.llamarpc.com"
    chain_id = 1

    mock_response = {"jsonrpc": "2.0", "id": 1, "result": "0x1234"}

    async with aiohttp.ClientSession() as session:
        with patch.object(session, "post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value.__aenter__.return_value.json = AsyncMock(
                return_value=mock_response
            )
            with patch("aiohttp.ClientSession", return_value=session):
                result = await tool.arun(
                    rpc_url=rpc_url,
                    chain_id=chain_id
                )
                assert isinstance(result, dict)