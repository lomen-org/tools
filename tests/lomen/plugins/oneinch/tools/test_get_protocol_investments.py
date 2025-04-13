import pytest
import aiohttp
from unittest.mock import patch, MagicMock, AsyncMock

from lomen.plugins.oneinch.tools.get_protocol_investments import (
    GetProtocolInvestments,
    GetProtocolInvestmentsParams,
)

# Use @pytest.mark.asyncio for specific async tests

# Dummy API Key for testing
DUMMY_API_KEY = "test-api-key"


@pytest.fixture
def tool():
    """Fixture to create an instance of the tool."""
    return GetProtocolInvestments(api_key=DUMMY_API_KEY)


@pytest.mark.asyncio
async def test_get_protocol_investments_success(tool, mocker):
    """Test successful fetch of protocol investments."""
    address = "0xTestAddress"
    chain_id = 1
    expected_investments = [
        {"protocol": "Aave", "value_usd": "500.50"},
        {"protocol": "Compound", "value_usd": "1000.00"},
    ]
    mock_response_data = {"result": expected_investments}

    # Mock API response
    mock_resp = AsyncMock()
    mock_resp.status = 200
    mock_resp.json = AsyncMock(return_value=mock_response_data)
    mock_resp.__aexit__ = AsyncMock(return_value=None)
    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    result = await tool.arun(address=address, chain_id=chain_id)

    assert result == expected_investments
    aiohttp.ClientSession.get.assert_called_once()


@pytest.mark.asyncio
async def test_get_protocol_investments_none_found_404(tool, mocker):
    """Test fetch when API returns 404 (no investments found)."""
    address = "0xNewAddress"
    chain_id = 137
    mock_status = 404

    # Mock API response
    mock_resp = AsyncMock()
    mock_resp.status = mock_status
    mock_resp.text = AsyncMock(return_value="Not Found")  # Text might not be checked
    mock_resp.__aexit__ = AsyncMock(return_value=None)
    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    # The tool should return an empty list on 404 for this endpoint
    result = await tool.arun(address=address, chain_id=chain_id)

    assert result == []
    aiohttp.ClientSession.get.assert_called_once()


@pytest.mark.asyncio
async def test_get_protocol_investments_api_error(tool, mocker):
    """Test fetch with a generic API error."""
    address = "0xTestAddress"
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
        await tool.arun(address=address, chain_id=chain_id)

    assert f"1inch API error (Status {mock_status})" in str(excinfo.value)


def test_get_protocol_investments_params(tool):
    """Test get_params for GetProtocolInvestments."""
    assert tool.get_params() == GetProtocolInvestmentsParams
