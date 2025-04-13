import pytest
import json
import aiohttp
import os
from unittest.mock import patch, MagicMock, AsyncMock, mock_open

from lomen.plugins.oneinch.tools.get_token_info import (
    GetTokenInfoBySymbol,
    GetTokenInfoBySymbolParams,
    GetTokenInfoByAddress,
    GetTokenInfoByAddressParams,
)

# Use @pytest.mark.asyncio for specific async tests

# Dummy API Key for testing
DUMMY_API_KEY = "test-api-key"


# --- Fixtures ---
@pytest.fixture
def tool_by_symbol():
    """Fixture for GetTokenInfoBySymbol tool."""
    return GetTokenInfoBySymbol(api_key=DUMMY_API_KEY)


@pytest.fixture
def tool_by_address():
    """Fixture for GetTokenInfoByAddress tool."""
    return GetTokenInfoByAddress(api_key=DUMMY_API_KEY)


# --- Tests for GetTokenInfoBySymbol ---


@pytest.mark.asyncio
async def test_get_token_info_by_symbol_api_success(tool_by_symbol, mocker):
    """Test successful token info fetch by symbol via API."""
    symbol = "USDC"
    chain_id = 1
    expected_data = {
        "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "symbol": "USDC",
        "name": "USD Coin",
        "decimals": 6,
        "logoUrl": "https://...",
        "eip2612": True,
        "rating": {"positive": 100, "negative": 0},
        "marketCap": 30000000000,
    }

    # Mock os.path.exists to return False (cache miss)
    mocker.patch("os.path.exists", return_value=False)

    # Mock API response
    mock_resp = AsyncMock()
    mock_resp.status = 200
    mock_resp.json = AsyncMock(return_value=[expected_data])  # API returns a list
    mock_resp.__aexit__ = AsyncMock(return_value=None)
    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    result = await tool_by_symbol.arun(symbol=symbol, chain_id=chain_id)

    assert result == expected_data
    os.path.exists.assert_called_once()  # Check cache was checked
    aiohttp.ClientSession.get.assert_called_once()  # Check API was called


@pytest.mark.asyncio
async def test_get_token_info_by_symbol_cache_hit(tool_by_symbol, mocker):
    """Test successful token info fetch by symbol from local cache."""
    symbol = "WETH"
    chain_id = 1
    cached_data = {
        "address": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
        "symbol": "WETH",
        "name": "Wrapped Ether",
        "decimals": 18,
        "logoUrl": "https://...",
    }
    # Mock file content
    mock_file_content = json.dumps(
        {"some_other_token": {}, cached_data["address"]: cached_data}
    )
    mock_read_data = mock_file_content

    # Mock os.path.exists to return True (cache hit)
    mocker.patch("os.path.exists", return_value=True)
    # Mock open to simulate reading the file
    mocker.patch("builtins.open", mock_open(read_data=mock_read_data))
    # Mock aiohttp just in case, although it shouldn't be called
    mock_api_get = mocker.patch("aiohttp.ClientSession.get")

    result = await tool_by_symbol.arun(symbol=symbol, chain_id=chain_id)

    assert result == cached_data
    os.path.exists.assert_called_once()
    open.assert_called_once()  # Check file was opened
    mock_api_get.assert_not_called()  # Ensure API was NOT called


@pytest.mark.asyncio
async def test_get_token_info_by_symbol_api_not_found(tool_by_symbol, mocker):
    """Test token info fetch by symbol when API returns empty list."""
    symbol = "NOSUCHTOKEN"
    chain_id = 1

    mocker.patch("os.path.exists", return_value=False)  # Cache miss

    # Mock API response (empty list)
    mock_resp = AsyncMock()
    mock_resp.status = 200
    mock_resp.json = AsyncMock(return_value=[])  # Empty list signifies not found
    mock_resp.__aexit__ = AsyncMock(return_value=None)
    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    with pytest.raises(ValueError) as excinfo:
        await tool_by_symbol.arun(symbol=symbol, chain_id=chain_id)

    assert f"Token symbol '{symbol}' not found" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_token_info_by_symbol_api_error(tool_by_symbol, mocker):
    """Test token info fetch by symbol with API error."""
    symbol = "USDC"
    chain_id = 1
    mock_status = 500
    mock_error_text = "Internal Server Error"

    mocker.patch("os.path.exists", return_value=False)  # Cache miss

    # Mock API response
    mock_resp = AsyncMock()
    mock_resp.status = mock_status
    mock_resp.text = AsyncMock(return_value=mock_error_text)
    mock_resp.__aexit__ = AsyncMock(return_value=None)
    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    with pytest.raises(Exception) as excinfo:
        await tool_by_symbol.arun(symbol=symbol, chain_id=chain_id)

    assert f"1inch API error (Status {mock_status})" in str(excinfo.value)


def test_get_token_info_by_symbol_params(tool_by_symbol):
    """Test get_params for GetTokenInfoBySymbol."""
    assert tool_by_symbol.get_params() == GetTokenInfoBySymbolParams


# --- Tests for GetTokenInfoByAddress ---


@pytest.mark.asyncio
async def test_get_token_info_by_address_success(tool_by_address, mocker):
    """Test successful token info fetch by address."""
    token_address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    chain_id = 1
    expected_data = {
        "address": token_address,
        "symbol": "USDC",
        "name": "USD Coin",
        "decimals": 6,
        "logoUrl": "https://...",
    }

    # Mock API response
    mock_resp = AsyncMock()
    mock_resp.status = 200
    mock_resp.json = AsyncMock(return_value=expected_data)
    mock_resp.__aexit__ = AsyncMock(return_value=None)
    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    result = await tool_by_address.arun(token_address=token_address, chain_id=chain_id)

    assert result == expected_data
    aiohttp.ClientSession.get.assert_called_once()


@pytest.mark.asyncio
async def test_get_token_info_by_address_not_found(tool_by_address, mocker):
    """Test token info fetch by address when API returns 404."""
    token_address = "0xInvalidAddress"
    chain_id = 1
    mock_status = 404

    # Mock API response
    mock_resp = AsyncMock()
    mock_resp.status = mock_status
    mock_resp.text = AsyncMock(
        return_value="Not Found"
    )  # Text might not be checked by code
    mock_resp.__aexit__ = AsyncMock(return_value=None)
    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    with pytest.raises(ValueError) as excinfo:
        await tool_by_address.arun(token_address=token_address, chain_id=chain_id)

    assert f"Token address '{token_address}' not found" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_token_info_by_address_api_error(tool_by_address, mocker):
    """Test token info fetch by address with API error."""
    token_address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
    chain_id = 1
    mock_status = 503
    mock_error_text = "Service Unavailable"

    # Mock API response
    mock_resp = AsyncMock()
    mock_resp.status = mock_status
    mock_resp.text = AsyncMock(return_value=mock_error_text)
    mock_resp.__aexit__ = AsyncMock(return_value=None)
    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    with pytest.raises(Exception) as excinfo:
        await tool_by_address.arun(token_address=token_address, chain_id=chain_id)

    assert f"1inch API error (Status {mock_status})" in str(excinfo.value)


def test_get_token_info_by_address_params(tool_by_address):
    """Test get_params for GetTokenInfoByAddress."""
    assert tool_by_address.get_params() == GetTokenInfoByAddressParams
