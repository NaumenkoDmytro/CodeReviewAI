import httpx

async def fetch_repository_files(repo_url: str):

    api_url = f"https://api.github.com/repos/{repo_url}/contents"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        response.raise_for_status()
        return response.json() 
