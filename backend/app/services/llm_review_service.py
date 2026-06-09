import json
import re
import google.generativeai as genai

from app.core.config import GEMINI_API_KEY
from app.llm.architecture_review_prompt import build_architecture_review_prompt

genai.configure(api_key=GEMINI_API_KEY)

primary_model = genai.GenerativeModel(
    "gemini-3-flash-preview"
)

fallback_model = genai.GenerativeModel(
    "gemini-3.1-flash-lite"
)


def generate_code_review(pr_info: dict, risk_analysis: dict):

    files = pr_info.get("files", [])

    diff_text = ""

    for file in files[:3]:

        diff_text += f"\n\nFILE: {file['filename']}\n"

        patch = file.get("patch", "")

        diff_text += patch[:3000]

    prompt = f"""
당신은 시니어 코드 리뷰어입니다.

다음 GitHub PR diff를 분석하여:

1. 잠재적인 버그 가능성
2. 협업 충돌 가능성
3. 리팩토링 포인트
4. 테스트 필요 여부

를 리뷰해주세요.

현재 위험도:
- level: {risk_analysis['risk_level']}
- score: {risk_analysis['risk_score']}

반드시 한국어로 작성하세요.

반드시 아래 JSON 형식만 반환하세요.

{{
  "summary": "...",
  "issues": [
    "...",
    "..."
  ],
  "suggestions": [
    "...",
    "..."
  ]
}}

PR Diff:
{diff_text}
"""

    try:
        response = primary_model.generate_content(prompt)

    except Exception:
        print("2.5-flash 호출 실패 → fallback 사용")
        response = fallback_model.generate_content(prompt)

    text = response.text.strip()

    text = re.sub(r"^```json", "", text)
    text = re.sub(r"^```", "", text)
    text = re.sub(r"```$", "", text)
    text = text.strip()

    try:
        parsed = json.loads(text)
    except Exception:
        parsed = {
            "summary": text,
            "issues": [],
            "suggestions": []
        }

    return parsed

def generate_architecture_review(
        repo_context,
        pr_context,
        ripple_context
):

    prompt = build_architecture_review_prompt(
        repo_context,
        pr_context,
        ripple_context
    )

    try:
        response = primary_model.generate_content(prompt)

    except Exception:
        print("architecture review primary 호출 실패 → fallback 사용")
        response = fallback_model.generate_content(prompt)

    return response.text