import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from unittest.mock import patch
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.asyncio
async def test_review_endpoint_invalid_repo(mocker):
    mocker.patch(
        "app.services.github_service.fetch_repository_files",
        side_effect=Exception("Invalid repository URL"),
    )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/review",
            json={
                "assignment_description": "Create a simple Python program.",
                "github_repo_url": "https://github.com/test/invalid_repo",
                "candidate_level": "Junior",
            },
        )

    assert response.status_code == 500


@pytest.mark.asyncio
async def test_review_endpoint_openai_error(mocker):

    mocker.patch(
        "app.services.github_service.fetch_repository_files",
        return_value=[
            {"name": "main.py", "path": "main.py", "content": "print('Hello, World!')"}
        ],
    )

    mocker.patch(
        "app.services.openai_service.analyze_code",
        side_effect=Exception("OpenAI API error"),
    )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/review",
            json={
                "assignment_description": "Create a simple Python program.",
                "github_repo_url": "https://github.com/test/repo",
                "candidate_level": "Junior",
            },
        )

    assert response.status_code == 500
