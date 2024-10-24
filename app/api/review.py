from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.github_service import fetch_repository_files
from app.services.openai_service import analyze_code


router = APIRouter()


class ReviewRequest(BaseModel):
    assignment_description: str
    github_repo_url: str
    candidate_level: str


@router.post("/review")
async def review_code(request: ReviewRequest):
    try:
        repo_files_content, repo_file_structure = await fetch_repository_files(
            request.github_repo_url
        )

        review_result = await analyze_code(
            repo_files_content, request.assignment_description, request.candidate_level
        )
        return f"{repo_file_structure}\n\n\nReview Result:\n{review_result}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
