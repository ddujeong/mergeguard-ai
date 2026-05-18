def generate_merge_strategy(
    risk_analysis: dict,
    conflict_analysis: dict
):

    risk_score = risk_analysis.get("risk_score", 0)

    keywords = risk_analysis.get(
        "detected_keywords",
        []
    )

    conflict_count = conflict_analysis.get(
        "conflict_count",
        0
    )

    recommended_strategy = "SQUASH_AND_MERGE"

    requires_rebase = False

    requires_manual_review = False

    requires_team_sync = False

    recommended_order = []

    if conflict_count >= 1:

        recommended_strategy = "REBASE_AND_MERGE"

        requires_rebase = True

        recommended_order.append(
            "충돌 PR 우선 merge 확인"
        )

    if risk_score >= 70:

        requires_manual_review = True

    if "AUTH" in keywords:

        requires_team_sync = True

        recommended_order.append(
            "인증 관련 기능 테스트 수행"
        )

    if "DB" in keywords:

        recommended_order.append(
            "DB 마이그레이션 순서 확인"
        )

    return {
        "recommended_strategy": recommended_strategy,
        "requires_rebase": requires_rebase,
        "requires_manual_review": requires_manual_review,
        "requires_team_sync": requires_team_sync,
        "risk_priority": keywords,
        "recommended_order": recommended_order
    }