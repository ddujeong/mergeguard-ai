RISK_KEYWORDS = [
    "auth", "login", "jwt", "security", "token",
    "config", "env", "setting",
    "database", "migration", "schema",
    "axios", "api", "client",
]

COMMON_RISK_FILES = [
    "package.json",
    "requirements.txt",
    ".env",
    "next.config",
    "dockerfile",
    "docker-compose",
]


def analyze_risk(pr_info: dict) -> dict:
    files = pr_info.get("files", [])

    risk_score = 0
    detected_keywords = set()
    risk_reasons = []
    risky_files = []

    changed_file_count = len(files)
    total_additions = pr_info.get("total_additions", 0)
    total_deletions = pr_info.get("total_deletions", 0)

    if changed_file_count >= 10:
        risk_score += 30
        risk_reasons.append("변경 파일 수가 많아 충돌 가능성이 높습니다.")

    if total_additions + total_deletions >= 300:
        risk_score += 25
        risk_reasons.append("변경 라인 수가 많아 리뷰 범위가 큽니다.")

    for file in files:
        filename = file.get("filename", "").lower()
        patch = file.get("patch", "").lower()

        matched = False

        for keyword in RISK_KEYWORDS:
            if keyword in filename or keyword in patch:
                matched = True
                detected_keywords.add(keyword.upper())
                break

        for common_file in COMMON_RISK_FILES:
            if common_file in filename:
                matched = True
                break

        if matched:
            risky_files.append(file.get("filename"))
            risk_score += 15

    if risky_files:
        risk_reasons.append("인증, 설정, API, 의존성 등 공통 영향 범위가 큰 파일이 수정되었습니다.")
    if risky_files and risk_score < 35:
        risk_score = 35
    risk_score = min(risk_score, 100)

    if risk_score >= 70:
        risk_level = "HIGH"
    elif risk_score >= 35:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    if not risk_reasons:
        risk_reasons.append("현재 diff 기준으로 큰 협업 위험 요소는 발견되지 않았습니다.")

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "risk_reasons": risk_reasons,
        "risky_files": list(set(risky_files)),
        "detected_keywords": list(detected_keywords),
    }