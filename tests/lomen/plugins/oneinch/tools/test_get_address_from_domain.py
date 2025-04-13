import pytest
import aiohttp
from unittest.mock import patch, MagicMock, AsyncMock

from lomen.plugins.oneinch.tools.get_address_from_domain import (
    GetAddressFromDomain,
    GetDomainFromAddressParams,
)

# Use @pytest.mark.asyncio for specific async tests

# Dummy API Key for testing
DUMMY_API_KEY = "test-api-key"


@pytest.fixture
def tool():
    """Fixture to create an instance of the tool."""
    return GetAddressFromDomain(api_key=DUMMY_API_KEY)


@pytest.mark.asyncio
async def test_get_address_from_domain_success(tool, mocker):
    """Test successful domain resolution."""
    domain_to_resolve = "vitalik.eth"
    expected_address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    mock_response_data = {"result": expected_address}

    # Mock the aiohttp response
    mock_resp = AsyncMock()
    mock_resp.status = 200
    mock_resp.json = AsyncMock(return_value=mock_response_data)
    # Mock the context manager exit
    mock_resp.__aexit__ = AsyncMock(return_value=None)

    # Mock the session.get call to return the mock response
    mock_session_get = AsyncMock(return_value=mock_resp)
    # Mock the session context manager enter
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)

    # Patch aiohttp.ClientSession directly
    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    # Call the tool's arun method
    result = await tool.arun(domain=domain_to_resolve)

    # Assertions
    assert result == expected_address
    # Check if aiohttp.ClientSession.get was called correctly (optional but good)
    aiohttp.ClientSession.get.assert_called_once_with(
        f"https://api.1inch.dev/domains/v2.0/lookup?name={domain_to_resolve}",
        headers={"Authorization": f"Bearer {DUMMY_API_KEY}"},
    )


@pytest.mark.asyncio
async def test_get_address_from_domain_not_found(tool, mocker):
    """Test domain resolution when the domain is not found (e.g., API returns non-200)."""
    domain_to_resolve = "nonexistentdomain.eth"
    mock_status = 404
    mock_error_text = "Not Found"

    # Mock the aiohttp response for 404
    mock_resp = AsyncMock()
    mock_resp.status = mock_status
    mock_resp.text = AsyncMock(return_value=mock_error_text)
    mock_resp.__aexit__ = AsyncMock(return_value=None)

    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)

    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    # Expect an exception
    with pytest.raises(Exception) as excinfo:
        await tool.arun(domain=domain_to_resolve)

    # Assertions on the exception
    assert f"1inch API error (Status {mock_status})" in str(excinfo.value)
    assert mock_error_text in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_address_from_domain_invalid_key(tool, mocker):
    """Test domain resolution with an invalid API key (401)."""
    domain_to_resolve = "vitalik.eth"
    mock_status = 401

    # Mock the aiohttp response for 401
    mock_resp = AsyncMock()
    mock_resp.status = mock_status
    mock_resp.__aexit__ = AsyncMock(return_value=None)  # No text needed for 401 check

    mock_session_get = AsyncMock(return_value=mock_resp)
    mock_session_get.__aenter__ = AsyncMock(return_value=mock_resp)

    mocker.patch("aiohttp.ClientSession.get", return_value=mock_session_get)

    # Expect a PermissionError
    with pytest.raises(PermissionError) as excinfo:
        await tool.arun(domain=domain_to_resolve)

    assert "Invalid or missing 1inch API key" in str(excinfo.value)


@pytest.mark.asyncio
async def test_get_address_from_domain_no_domain(tool):
    """Test calling the tool without providing a domain."""
    with pytest.raises(ValueError) as excinfo:
        # Need to simulate calling _call_api directly or trigger arun's internal call check
        # Since arun calls _call_api which checks, we call arun
        await tool.arun(domain="")  # Pass empty string to trigger validation

    assert "Domain name must be provided" in str(excinfo.value)


def test_get_params(tool):
    """Test that get_params returns the correct Pydantic model."""
    assert tool.get_params() == GetDomainFromAddressParams
