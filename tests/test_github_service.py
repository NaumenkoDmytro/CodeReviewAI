import pytest
from httpx import HTTPStatusError
from unittest.mock import patch
from app.services.github_service import fetch_repository_files


@pytest.mark.asyncio
@patch("httpx.AsyncClient.get")
async def test_fetch_repository_files_error(mock_get):
    mock_get.side_effect = HTTPStatusError(
        "Error fetching data", request=None, response=None
    )

    with pytest.raises(Exception):
        await fetch_repository_files("https://github.com/test/repo")
