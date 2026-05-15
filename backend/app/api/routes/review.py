from fastapi import APIRouter
from app.services.github_service import get_pr_info

router = APIRouter(prefix="/api/v1/reviews", tags=["reviews"])


@router.post("/analyze")
def analyze_pr(payload: dict):

    pr_url = payload.get("pr_url")

    result = get_pr_info(pr_url)

    return {
        "success": True,
        "data": result
    }