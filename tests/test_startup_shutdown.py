import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

@pytest.mark.asyncio
async def test_startup_event():
    # Patch the logger
    with patch("app.main.logger") as logger_mock:
        # Manually fire the startup event
        await app.router.startup()

        # Ensure the startup message is logged
        logger_mock.info.assert_any_call("FastAPI application is starting up.")

@pytest.mark.asyncio
async def test_shutdown_event():
    # Patch the logger
    with patch("app.main.logger") as logger_mock:
        # Manually fire the shutdown event
        await app.router.shutdown()

        # Ensure the shutdown message is logged
        logger_mock.info.assert_any_call("FastAPI application is shutting down.")

