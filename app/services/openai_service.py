import openai

openai.api_key = "YOUR_OPENAI_API_KEY"

async def analyze_code(repo_files, assignment_description, candidate_level):
    prompt = f"""
    You are reviewing a coding assignment for a {candidate_level} level developer. 
    The task is as follows: {assignment_description}. Here is the code:
    {repo_files}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1500
    )
    return response.choices[0].message["content"]
