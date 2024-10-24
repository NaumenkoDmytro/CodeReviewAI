import httpx
from fastapi import HTTPException
from app.utils.cache import get_cached_data, set_cached_data, generate_cache_key
from app.settings import GITHUB_API_TOKEN
from app.settings import logger


async def fetch_repository_files(repo_url: str) -> tuple:
    """
    Asynchronous function to fetch files from a GitHub repository by its URL.

    This function checks the cache for stored repository data.
    If cached data is found, it retrieves and returns them.
    If no cached data exists, it sends a request to the GitHub API to fetch the repository's file list,
    then it retrieves the content of these files. After fetching the data, it caches the result.

    Parameters:
    repo_url (str): The URL of the GitHub repository in the format "https://github.com/owner/repo".

    Returns:
    tuple: The first part is the content of all the files from the repository,
           the second part is a formatted list of the files with their names.
    """
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


async def fetch_all_files(
    client: httpx.AsyncClient, contents: list, headers: dict, file_list=[]
) -> list:
    """
    Asynchronous recursive function to retrieve all files from a GitHub repository, including those in subdirectories.

    This function iterates through the repository's contents. If an item is a file, it adds the file's path and download URL
    to the `file_list`. If the item is a directory, it recursively fetches the contents of the directory and continues
    processing them until all files have been found.

    Parameters:
    client (httpx.AsyncClient): The HTTP client used to make requests to the GitHub API.
    contents (list): The list of items (files and directories) from the GitHub repository.
    headers (dict): HTTP headers including authorization and content type for the GitHub API request.
    file_list (list, optional): A list that accumulates file paths and download URLs. Defaults to an empty list.

    Returns:
    list: A list of dictionaries containing file paths and download URLs for all files in the repository.
    """
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


async def fetch_file_content(
    client: httpx.AsyncClient, file_url: str, headers: dict
) -> str:
    """
    Asynchronous function to fetch the content of a file from a GitHub repository using its download URL.

    This function sends a request to the provided file's download URL and retrieves its content.
    If the request fails, it logs the error and raises an HTTPException.

    Parameters:
    client (httpx.AsyncClient): The HTTP client used to make the request to the file's URL.
    file_url (str): The download URL of the file from the GitHub repository.
    headers (dict): HTTP headers, including authorization and content type for the GitHub API request.

    Returns:
    str: The textual content of the file.
    """
    file_response = await client.get(file_url, headers=headers)
    if file_response.status_code != 200:
        logger.error(f"GitHub API returned an error: {file_response.json()}")
        raise HTTPException(
            status_code=file_response.status_code, detail=file_response.json()
        )

    return file_response.text
