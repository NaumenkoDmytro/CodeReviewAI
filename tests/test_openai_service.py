import pytest
from unittest.mock import patch
from app.services.openai_service import analyze_code

@pytest.mark.asyncio
@patch("openai.ChatCompletion.create")
async def test_analyze_code_error(mock_create):
    # Simulate an API error
    mock_create.side_effect = Exception("OpenAI API error")
    
    with pytest.raises(Exception):
        await analyze_code([], "Create a simple Python program", "Junior")



