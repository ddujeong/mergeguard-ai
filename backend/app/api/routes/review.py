from fastapi import APIRouter

from app.services.github_service import get_pr_info
from app.services.risk_analyzer import analyze_risk
from app.services.llm_review_service import generate_code_review
from app.services.conflict_analyzer import analyze_conflicts
from app.services.merge_guide_service import generate_merge_guide
from app.services.complexity_analyzer import analyze_complexity
from app.schemas.diff_request import DiffAnalyzeRequest
from app.services.diff_parser import parse_diff_text

router = APIRouter(prefix="/api/v1/reviews", tags=["reviews"])


@router.post("/analyze")
def analyze_pr(payload: dict):

    pr_url = payload.get("pr_url")

    pr_info = get_pr_info(pr_url)

    risk_result = analyze_risk(pr_info)

    llm_review = generate_code_review(pr_info, risk_result)

    conflict_result = analyze_conflicts(
        pr_url,
        pr_info["files"]
    )
    merge_guide = generate_merge_guide(
        pr_info,
        risk_result,
        conflict_result
)
    complexity_result = analyze_complexity(
    pr_info,
    risk_result
)
    return {
        "success": True,
        "data": {
            **pr_info,
            "risk_analysis": risk_result,
            "conflict_analysis": conflict_result,
            "llm_review": llm_review,
            "merge_guide": merge_guide,
            "complexity_analysis": complexity_result
        }
    }
@router.post("/analyze-diff")
def analyze_diff(request: DiffAnalyzeRequest):

    files = parse_diff_text(request.diff_text)

    pr_info = {
        "repository": "LOCAL_DIFF",
        "author": "local-user",
        "changed_files": len(files),
        "commits": 1,
        "files": files
    }

    risk_result = analyze_risk(pr_info)

    complexity_result = analyze_complexity(
        pr_info,
        risk_result
    )

    llm_review = generate_code_review(
        pr_info,
        risk_result
    )

    merge_guide = generate_merge_guide(
        pr_info,
        risk_result,
        {
            "conflict_count": 0,
            "conflict_prs": []
        }
    )

    return {
        "success": True,
        "data": {
            **pr_info,
            "risk_analysis": risk_result,
            "complexity_analysis": complexity_result,
            "llm_review": llm_review,
            "merge_guide": merge_guide,
            "conflict_analysis": {
                "conflict_count": 0,
                "conflict_prs": []
            }
        }
    }