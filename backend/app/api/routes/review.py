from fastapi import APIRouter

from app.services.github_service import get_pr_info
from app.services.risk_analyzer import analyze_risk
from app.services.llm_review_service import generate_code_review

router = APIRouter(prefix="/api/v1/reviews", tags=["reviews"])


@router.post("/analyze")
def analyze_pr(payload: dict):

    pr_url = payload.get("pr_url")

    pr_info = get_pr_info(pr_url)

    risk_result = analyze_risk(pr_info)

    llm_review = generate_code_review(pr_info, risk_result)

    return {
        "success": True,
        "data": {
            **pr_info,
            "risk_analysis": risk_result,
            "llm_review": llm_review
        }
    }