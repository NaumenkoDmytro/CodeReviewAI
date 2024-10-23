import openai
from app.utils.cache import get_cached_data, set_cached_data, generate_cache_key

openai.api_key = "YOUR_OPENAI_API_KEY"

async def analyze_code(repo_files, assignment_description, candidate_level):
    # Generate a unique cache key for the OpenAI request based on inputs
    cache_key = generate_cache_key("openai_analysis", assignment_description, candidate_level)

    # Check if the result is already cached
    cached_analysis = await get_cached_data(cache_key)
    if cached_analysis:
        return cached_analysis

    # Craft the OpenAI prompt
    prompt = f"""
    You are reviewing a coding assignment for a {candidate_level} level developer. 
    The task is as follows: {assignment_description}. Here is the code:
    {repo_files}
    """

    # Make the OpenAI API call
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500
    )
    analysis_result = response.choices[0].message["content"]

    # Cache the result of the analysis
    await set_cached_data(cache_key, analysis_result)
    return analysis_result