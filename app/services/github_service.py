import httpx
from fastapi import HTTPException
from app.utils.cache import get_cached_data, set_cached_data, generate_cache_key
from app.settings import GITHUB_API_TOKEN
from app.settings import logger


async def fetch_repository_files(repo_url: str):
    cache_key = generate_cache_key("github_repo", repo_url)

    cached_data = await get_cached_data(cache_key)
    if cached_data:
        logger.info(f"Cache hit for GitHub repository: {repo_url}")
        datalist = cached_data.split("||||")
        return datalist[0], datalist[1]
    logger.info(f"Fetching repository files from GitHub: {repo_url}")

    try:
        owner, repo = repo_url.split("/")[-2:]
    except ValueError:
        logger.error(f"Invalid repository URL format: {repo_url}")
        raise HTTPException(status_code=400, detail="Invalid repository URL format.")

    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    headers = {
        "Authorization": f"token {GITHUB_API_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(api_url, headers=headers)
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            logger.error(f"GitHub API returned an error: {str(e)}")
            raise HTTPException(
                status_code=response.status_code, detail=response.json()
            )

        repo_data = response.json()
        logger.info(f"Repository files successfully fetched: {repo_url}")
        file_urls = await fetch_all_files(client, repo_data, headers)
        content_from_files = ""
        for file in file_urls:
            file_content = await fetch_file_content(
                client, file["download_url"], headers
            )
            content_from_files += (
                f"Filename: {file['path']}, content from this file: {file_content}"
            )

        formatted_files = "Files found in the repository:\n"
        formatted_files += "\n".join(
            [f"• {file_path['path']}" for file_path in file_urls]
        )

        await set_cached_data(
            cache_key, content_from_files + "||||" + formatted_files, 60
        )
        return content_from_files, formatted_files


async def fetch_all_files(client, contents, headers, file_list=[]):
    for item in contents:
        if item["type"] == "file":
            file_list.append(
                {"path": item["path"], "download_url": item["download_url"]}
            )
        elif item["type"] == "dir":
            dir_url = item["url"]
            dir_response = await client.get(dir_url, headers=headers)

            if dir_response.status_code != 200:
                logger.error(f"GitHub API returned an error: {dir_response.json()}")
                raise HTTPException(
                    status_code=dir_response.status_code, detail=dir_response.json()
                )

            sub_contents = dir_response.json()
            await fetch_all_files(client, sub_contents, headers, file_list)

    return file_list


async def fetch_file_content(client, file_url, headers):
    file_response = await client.get(file_url, headers=headers)
    if file_response.status_code != 200:
        logger.error(f"GitHub API returned an error: {file_response.json()}")
        raise HTTPException(
            status_code=file_response.status_code, detail=file_response.json()
        )

    return file_response.text
