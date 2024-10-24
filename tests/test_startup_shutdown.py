import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_startup_event():

    with patch("app.main.logger") as logger_mock:

        await app.router.startup()

        logger_mock.info.assert_any_call("FastAPI application is starting up.")


@pytest.mark.asyncio
async def test_shutdown_event():

    with patch("app.main.logger") as logger_mock:

        await app.router.shutdown()

        logger_mock.info.assert_any_call("FastAPI application is shutting down.")
