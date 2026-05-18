from fastapi import APIRouter

from app.services.github_service import get_pr_info
from app.services.risk_analyzer import analyze_risk
from app.services.llm_review_service import generate_code_review
from app.services.conflict_analyzer import analyze_conflicts
from app.services.complexity_analyzer import analyze_complexity
from app.schemas.diff_request import DiffAnalyzeRequest
from app.services.diff_parser import parse_diff_text
from app.services.merge_strategy_service import generate_merge_strategy
from app.services.ast_analyzer import analyze_changed_structure
from app.services.ast_risk_analyzer import calculate_ast_risk
from app.services.impact_chain_analyzer import (
    build_deep_call_chains,
    calculate_ripple_effect
)
from app.services.discord_service import send_discord_alert

router = APIRouter(prefix="/api/v1/reviews", tags=["reviews"])


@router.post("/analyze")
def analyze_pr(payload: dict):

    pr_url = payload.get("pr_url")

    pr_info = get_pr_info(pr_url)

    risk_result = analyze_risk(pr_info)

    conflict_result = analyze_conflicts(
        pr_url,
        pr_info["files"]
    )
    complexity_result = analyze_complexity(
        pr_info,
        risk_result
    )
    
    ast_result = analyze_changed_structure(
        pr_info["files"]
    )
    deep_impact_chains = build_deep_call_chains(
        ast_result["call_relations"]
    )
    ripple_effect = calculate_ripple_effect(
        deep_impact_chains
    )
    ast_risk = calculate_ast_risk(
        ast_result.get("method_risks", [])
    )

    risk_result["risk_score"] = min(
        risk_result["risk_score"] + ast_risk["ast_risk_score"],
        100
    )
    llm_review = generate_code_review(pr_info, risk_result)
    
    merge_guide = generate_merge_strategy(
        risk_result,
        conflict_result
    )
    result_data = {
        **pr_info,
        "risk_analysis": risk_result,
        "conflict_analysis": conflict_result,
        "llm_review": llm_review,
        "merge_guide": merge_guide,
        "complexity_analysis": complexity_result,
        "ast_analysis": ast_result,
        "ast_risk_analysis": ast_risk,
        "deep_impact_analysis": deep_impact_chains,
        "ripple_effect": ripple_effect,
        "pr_url": pr_url
    }
    send_discord_alert(result_data)
    return {
        "success": True,
        "data": result_data
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
    ast_result = analyze_changed_structure(files)
    
    deep_impact_chains = build_deep_call_chains(
        ast_result["call_relations"]
    )
    ripple_effect = calculate_ripple_effect(
        deep_impact_chains
    )
    
    ast_risk = calculate_ast_risk(
        ast_result.get("method_risks", [])
    )

    risk_result["risk_score"] = min(
        risk_result["risk_score"] + ast_risk["ast_risk_score"],
        100
    )
    llm_review = generate_code_review(
        pr_info,
        risk_result
    )

    merge_guide = generate_merge_strategy(
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
            "ast_analysis": ast_result,
            "llm_review": llm_review,
            "merge_guide": merge_guide,
            "conflict_analysis": {
                "conflict_count": 0,
                "conflict_prs": []
            },
            "ast_risk_analysis": ast_risk,
            "deep_impact_analysis": deep_impact_chains,
            "ripple_effect": ripple_effect
        }
    }