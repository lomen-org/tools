import pytest
import aiohttp
from unittest.mock import patch, MagicMock, AsyncMock

from lomen.plugins.oneinch.tools.get_profit_and_loss import (
    GetProfitAndLoss,
    GetProfitAndLossParams,
)

# Use @pytest.mark.asyncio for specific async tests

# Dummy API Key for testing
DUMMY_API_KEY = "test-api-key"


@pytest.fixture
def tool():
    """Fixture to create an instance of the tool."""
    return GetProfitAndLoss(api_key=DUMMY_API_KEY)


@pytest.mark.asyncio
async def test_get_pnl_success_no_timerange(tool, mocker):
    """Test successful PnL fetch with default timerange."""
    address = "0xTestAddress"
    chain_id = 1
    expected_pnl = {"total_gain_usd": "123.45", "total_roi_percent": "15.5"}
    mock_response_data = {"result": expected_pnl}

    # Mock API response
    mock_resp = AsyncMock()
    mock_resp.status = 200
    mock_resp.json = AsyncMock(return_value=mock_response_data)
    mock_resp.__aexit__ = AsyncMock(return_value=None)
    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    result = await tool.arun(address=address, chain_id=chain_id)  # No timerange

    assert result == expected_pnl
    # Check URL called (without timerange)
    aiohttp.ClientSession.get.assert_called_once_with(
        f"https://api.1inch.dev/portfolio/portfolio/v4/general/profit_and_loss?addresses={address}&chain_id={chain_id}",
        headers={"Authorization": f"Bearer {DUMMY_API_KEY}"},
    )


@pytest.mark.asyncio
async def test_get_pnl_success_with_timerange(tool, mocker):
    """Test successful PnL fetch with a specific timerange."""
    address = "0xTestAddress"
    chain_id = 137
    timerange = "1month"
    expected_pnl = {"total_gain_usd": "50.00", "total_roi_percent": "5.0"}
    mock_response_data = {"result": expected_pnl}

    # Mock API response
    mock_resp = AsyncMock()
    mock_resp.status = 200
    mock_resp.json = AsyncMock(return_value=mock_response_data)
    mock_resp.__aexit__ = AsyncMock(return_value=None)
    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    result = await tool.arun(address=address, chain_id=chain_id, timerange=timerange)

    assert result == expected_pnl
    # Check URL called (with timerange)
    aiohttp.ClientSession.get.assert_called_once_with(
        f"https://api.1inch.dev/portfolio/portfolio/v4/general/profit_and_loss?addresses={address}&chain_id={chain_id}&timerange={timerange}",
        headers={"Authorization": f"Bearer {DUMMY_API_KEY}"},
    )


@pytest.mark.asyncio
async def test_get_pnl_not_found_404(tool, mocker):
    """Test PnL fetch when API returns 404 (e.g., inactive address)."""
    address = "0xInactiveAddress"
    chain_id = 1
    mock_status = 404

    # Mock API response
    mock_resp = AsyncMock()
    mock_resp.status = mock_status
    mock_resp.text = AsyncMock(return_value="Not Found")
    mock_resp.__aexit__ = AsyncMock(return_value=None)
    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    with pytest.raises(ValueError) as excinfo:
        await tool.arun(address=address, chain_id=chain_id)

    assert f"Could not calculate PnL for address '{address}'" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_pnl_api_error(tool, mocker):
    """Test PnL fetch with a generic API error."""
    address = "0xTestAddress"
    chain_id = 1
    mock_status = 500
    mock_error_text = "Server Error"

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


def test_get_pnl_params(tool):
    """Test get_params for GetProfitAndLoss."""
    assert tool.get_params() == GetProfitAndLossParams
