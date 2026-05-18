import requests
import os

DISCORD_WEBHOOK_URL = os.getenv(
    "DISCORD_WEBHOOK_URL"
)

FRONTEND_URL = os.getenv(
    "FRONTEND_URL"
)

def send_discord_alert(result):

    if not DISCORD_WEBHOOK_URL:
        return

    risk = result["risk_analysis"]
    ripple = result["ripple_effect"]

    pr_url = result.get("pr_url", "")

    dashboard_url = (
        f"{FRONTEND_URL}?prUrl={pr_url}"
        if FRONTEND_URL and pr_url
        else ""
    )

    message = f"""
🚨 MergeGuard AI 분석 결과

📦 Repository
{result['repository']}

🔀 PR #{result.get('pr_number')}

⚠️ Risk Score
{risk['risk_score']}

🌊 Ripple Effect
{ripple['level']}

📄 Changed Files
{result['changed_files']}

🧩 Commits
{result['commits']}

🔗 GitHub PR
{pr_url}

🔗 MergeGuard Dashboard
{dashboard_url}
"""

    try:
        requests.post(
            DISCORD_WEBHOOK_URL,
            json={
                "content": message
            },
            timeout=5
        )
    except Exception as e:
        print("Discord alert failed:", e)