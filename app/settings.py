from dotenv import load_dotenv
import os
from app.logging_config import configure_logger


load_dotenv()

logger = configure_logger()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")
REDIS_URL = "redis://redis"
