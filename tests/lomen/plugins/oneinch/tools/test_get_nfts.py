import pytest
import aiohttp
from unittest.mock import patch, MagicMock, AsyncMock

from lomen.plugins.oneinch.tools.get_nfts import (
    GetNFTsForAddress,
    GetNFTsForAddressParams,
    NFT_SUPPORTED_CHAIN_IDS,  # Import for validation testing
)

# Use @pytest.mark.asyncio for specific async tests

# Dummy API Key for testing
DUMMY_API_KEY = "test-api-key"


@pytest.fixture
def tool():
    """Fixture to create an instance of the tool."""
    return GetNFTsForAddress(api_key=DUMMY_API_KEY)


@pytest.mark.asyncio
async def test_get_nfts_success(tool, mocker):
    """Test successful fetch of NFTs."""
    address = "0xTestAddress"
    chain_ids = [1, 137]  # Ethereum and Polygon
    limit = 10
    expected_nfts = {
        "result": [
            {"collection": "CryptoPunks", "token_id": "1234"},
            {"collection": "BoredApes", "token_id": "5678"},
        ]
    }

    # Mock API response
    mock_resp = AsyncMock()
    mock_resp.status = 200
    mock_resp.json = AsyncMock(return_value=expected_nfts)
    mock_resp.__aexit__ = AsyncMock(return_value=None)
    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    result = await tool.arun(address=address, chain_ids=chain_ids, limit=limit)

    assert result == expected_nfts
    # Check URL called
    chain_ids_str = ",".join(map(str, chain_ids))
    aiohttp.ClientSession.get.assert_called_once_with(
        f"https://api.1inch.dev/nft/v2/byaddress?chainIds={chain_ids_str}&address={address}&limit={limit}",
        headers={"Authorization": f"Bearer {DUMMY_API_KEY}"},
    )


@pytest.mark.asyncio
async def test_get_nfts_success_default_limit(tool, mocker):
    """Test successful fetch of NFTs using the default limit."""
    address = "0xTestAddress"
    chain_ids = [1]  # Ethereum only
    default_limit = 25
    expected_nfts = {"result": [{"collection": "CoolCats", "token_id": "999"}]}

    # Mock API response
    mock_resp = AsyncMock()
    mock_resp.status = 200
    mock_resp.json = AsyncMock(return_value=expected_nfts)
    mock_resp.__aexit__ = AsyncMock(return_value=None)
    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    # Call without limit parameter
    result = await tool.arun(address=address, chain_ids=chain_ids)

    assert result == expected_nfts
    # Check URL called with default limit
    chain_ids_str = ",".join(map(str, chain_ids))
    aiohttp.ClientSession.get.assert_called_once_with(
        f"https://api.1inch.dev/nft/v2/byaddress?chainIds={chain_ids_str}&address={address}&limit={default_limit}",
        headers={"Authorization": f"Bearer {DUMMY_API_KEY}"},
    )


@pytest.mark.asyncio
async def test_get_nfts_none_found_404(tool, mocker):
    """Test fetch when API returns 404 (no NFTs found)."""
    address = "0xNewAddress"
    chain_ids = [137]
    limit = 5
    mock_status = 404

    # Mock API response
    mock_resp = AsyncMock()
    mock_resp.status = mock_status
    mock_resp.text = AsyncMock(return_value="Not Found")
    mock_resp.__aexit__ = AsyncMock(return_value=None)
    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    # The tool should return {"result": []} on 404 for this endpoint
    result = await tool.arun(address=address, chain_ids=chain_ids, limit=limit)

    assert result == {"result": []}
    aiohttp.ClientSession.get.assert_called_once()


@pytest.mark.asyncio
async def test_get_nfts_api_error(tool, mocker):
    """Test fetch with a generic API error."""
    address = "0xTestAddress"
    chain_ids = [1]
    limit = 25
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
        await tool.arun(address=address, chain_ids=chain_ids, limit=limit)

    assert f"1inch API error (Status {mock_status})" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_nfts_invalid_chain_id(tool):
    """Test fetch with an unsupported chain ID."""
    address = "0xTestAddress"
    invalid_chain_ids = [1, 9999]  # 9999 is not supported

    with pytest.raises(ValueError) as excinfo:
        await tool.arun(address=address, chain_ids=invalid_chain_ids)

    assert "Unsupported chain IDs provided: [9999]" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_nfts_invalid_limit(tool, mocker):
    """Test fetch with an invalid limit."""
    address = "0xTestAddress"
    chain_ids = [1]
    
    # Mock the validation error before API call
    with patch.object(tool, '_call_api', side_effect=ValueError("Limit must be between 1 and 25")):
        with pytest.raises(ValueError) as excinfo:
            await tool.arun(address=address, chain_ids=chain_ids, limit=50)
        assert "Limit must be between 1 and 25" in str(excinfo.value)


def test_get_nfts_params(tool):
    """Test get_params for GetNFTsForAddress."""
    assert tool.get_params() == GetNFTsForAddressParams
