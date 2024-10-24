from openai import OpenAI
from fastapi import HTTPException
from app.utils.cache import get_cached_data, set_cached_data, generate_cache_key
from app.settings import OPENAI_API_KEY
from app.settings import logger


async def analyze_code(
    repo_files: str, assignment_description: str, candidate_level: str
) -> str:
    """
    Asynchronous function to analyze code from a GitHub repository using OpenAI's API based on a specified assignment and developer level.

    This function checks the cache for a previously stored analysis result. If found, the cached analysis is returned.
    If no cached data exists, it sends a request to the OpenAI API to perform a code review based on the provided coding assignment,
    candidate's level, and the code from the repository. The analysis includes downsides/comments, a rating, and a conclusion.
    The result is then cached for future use.

    Parameters:
    repo_files (str): A string containing the code from all files in the GitHub repository.
    assignment_description (str): A description of the coding task/assignment that is being reviewed.
    candidate_level (str): The experience level of the candidate (e.g., junior, mid-level, senior).

    Returns:
    str: The analysis result provided by the OpenAI API, including downsides/comments, a rating, and a conclusion.
    """
    client = OpenAI(api_key=OPENAI_API_KEY)
    cache_key = generate_cache_key(
        "openai_analysis", assignment_description, candidate_level
    )

    cached_analysis = await get_cached_data(cache_key)
    if cached_analysis:
        logger.info("Cache hit for OpenAI analysis")
        return cached_analysis

    logger.info("Sending code analysis request to OpenAI API")
    prompt = f"""
    You are reviewing a coding assignment for a {candidate_level} level developer. 
    The task is as follows: {assignment_description}. Here is the code from all files in project repository:
    {repo_files}
    You must return the review result in the following format: Downsides/Comments, Rating, Conclusion.
    Description of each part of the format:
    Downsides/Comments - You need to provide Downsides, Comments, for each file that you've analyzed.
    Rating - Based on Downsides/Comments you need to provide developer rating in range 1 to 5. Make sure that you took into account the developer level.
    Conclusion - Based on the information you analyzed develop a text where you need to clarify point to improve and current problems in the project and code.
    Your answer must include all parts of the format it's very imporatant.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
    except Exception as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise HTTPException(status_code=500, detail="Error with OpenAI API")
    analysis_result = response.choices[0].message.content
    logger.info("Successfully received response from OpenAI API")

    await set_cached_data(cache_key, analysis_result)
    return analysis_result
