from openai import OpenAI
from app.utils.cache import get_cached_data, set_cached_data, generate_cache_key
from app.settings import OPENAI_API_KEY


async def analyze_code(repo_files, assignment_description, candidate_level):
    client = OpenAI(api_key=OPENAI_API_KEY)
    # Generate a unique cache key for the OpenAI request based on inputs
    cache_key = generate_cache_key("openai_analysis", assignment_description, candidate_level)

    # Check if the result is already cached
    cached_analysis = await get_cached_data(cache_key)
    if cached_analysis:
        return cached_analysis

    # Craft the OpenAI prompt
    prompt = f"""
    You are reviewing a coding assignment for a {candidate_level} level developer. 
    The task is as follows: {assignment_description}. Here is the code from all files in project repository:
    {repo_files}
    Return the review result in the following format: Downsides/Comments, Rating, Conclusion.
    Description of each part of the review:
    Downsides/Comments - You need to provide Downsides, Comments, for each file that you've analyzed.
    Rating - Based on Downsides/Comments you need to provide developer rating in range 1 to 5. Make sure that you took into account the developer level.
    Conclusion - Based on the information you analyzed develop a text where you need to clarify point to improve and current problems in the project and code.
    """

    # Make the OpenAI API call
    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
    )
    analysis_result = response.choices[0].message.content

    # Cache the result of the analysis
    await set_cached_data(cache_key, analysis_result)
    return analysis_result
