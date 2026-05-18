def calculate_ast_risk(method_risks: list):

    score = 0

    for item in method_risks:

        level = item["risk_level"]

        if level == "HIGH":
            score += 15

        elif level == "MEDIUM":
            score += 5

    if score > 40:
        score = 40

    return {
        "ast_risk_score": score
    }