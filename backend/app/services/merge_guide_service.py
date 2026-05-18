import json

import google.generativeai as genai

from app.core.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

primary_model = genai.GenerativeModel(
    "gemini-3-flash-preview"
)

fallback_model = genai.GenerativeModel(
    "gemini-3.1-flash-lite"
)


def generate_merge_guide(pr_info, risk_analysis, conflict_analysis):

    prompt = f"""
당신은 Git 협업 전문가입니다.

다음 PR 정보를 기반으로
안전한 merge 전략을 제안하세요.

현재 위험도:
- level: {risk_analysis['risk_level']}
- score: {risk_analysis['risk_score']}

충돌 PR 수:
- {conflict_analysis['conflict_count']}

위험 파일:
{risk_analysis['risky_files']}

감지 키워드:
{risk_analysis['detected_keywords']}

반드시 한국어로 작성하세요.
반드시 아래 JSON 형식으로만 응답하세요.

{{
  "merge_strategy": [
    "...",
    "...",
    "..."
  ]
}}
"""

    try:

        response = primary_model.generate_content(prompt)

    except Exception:

        print("2.5-flash quota 초과 → fallback 사용")

        response = fallback_model.generate_content(prompt)

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:

        parsed = json.loads(text)

    except Exception:

        parsed = {
            "merge_strategy": [
                text
            ]
        }

    return parsed