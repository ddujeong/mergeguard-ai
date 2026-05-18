def analyze_complexity(pr_info, risk_analysis):

    changed_files = pr_info.get("changed_files", 0)

    files = pr_info.get("files", [])

    additions = sum(file.get("additions", 0) for file in files)

    deletions = sum(file.get("deletions", 0) for file in files)

    risk_score = risk_analysis.get("risk_score", 0)

    complexity_score = 0

    complexity_score += changed_files * 5

    complexity_score += min(additions // 20, 30)

    complexity_score += min(deletions // 20, 20)

    complexity_score += risk_score // 2

    complexity_score = min(complexity_score, 100)

    if complexity_score >= 70:
        level = "HIGH"
    elif complexity_score >= 40:
        level = "MEDIUM"
    else:
        level = "LOW"

    return {
        "complexity_level": level,
        "complexity_score": complexity_score,
        "total_additions": additions,
        "total_deletions": deletions,
    }