import httpx
from fastapi import HTTPException
from app.utils.cache import get_cached_data, set_cached_data, generate_cache_key
import os

GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")

async def fetch_repository_files(repo_url: str):
    # Generate a unique cache key for the repository
    cache_key = generate_cache_key("github_repo", repo_url)

    # Check if the result is already cached
    cached_data = await get_cached_data(cache_key)
    if cached_data:
        return cached_data

    try:
        owner, repo = repo_url.split('/')[-2:]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid repository URL format.")

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    headers = {
        "Authorization": f"token {GITHUB_API_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        # Cache the response data before returning it
        repo_data = response.json()
        await set_cached_data(cache_key, repo_data)
        return repo_data
