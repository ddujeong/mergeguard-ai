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
from app.indexing.repo_indexer import index_repository
from app.analysis.repo_context_builder import build_repo_context
from app.analysis.pr_context_builder import build_pr_context
from app.services.llm_review_service import generate_architecture_review
from app.schemas.repo_index_request import RepoIndexRequest
from sqlalchemy.orm import Session
from fastapi import Depends
from app.repository.models import Repository

from app.repository.db import get_db

router = APIRouter(prefix="/api/v1/reviews", tags=["reviews"])


@router.post("/analyze")
def analyze_pr(payload: dict, db: Session = Depends(get_db)):

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
    
    repo_name = pr_info["repository"]
    
    repository_entity = db.query(
        Repository
    ).filter(
        Repository.name == repo_name
    ).first()
    
    repo_context = {}

    if repository_entity:

        repo_context = build_repo_context(
            repository_id=repository_entity.id,
            db=db
        )

    pr_context = build_pr_context(
        pr_info["files"]
    )

    architecture_review = (
        generate_architecture_review(
            repo_context,
            pr_context
        )
    )
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
        "architecture_review": architecture_review,
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

@router.post("/github/webhook")
def github_webhook(payload: dict):

    action = payload.get("action")

    if action not in ["opened", "synchronize", "reopened"]:
        return {
            "success": True,
            "message": "ignored event"
        }

    pull_request = payload.get("pull_request")

    if not pull_request:
        return {
            "success": False,
            "message": "pull_request payload missing"
        }

    pr_url = pull_request.get("html_url")

    if not pr_url:
        return {
            "success": False,
            "message": "pr_url missing"
        }

    return analyze_pr({
        "pr_url": pr_url
    })


@router.post("/repositories/index")
def index_repo(
        request: RepoIndexRequest,
        db: Session = Depends(get_db)
):

    return index_repository(
        request.owner,
        request.repo,
        db
    )
    
@router.get("/repositories/{repository_id}/context")
def get_repo_context(
        repository_id: int,
        db: Session = Depends(get_db)
):

    return build_repo_context(
        repository_id,
        db
    )