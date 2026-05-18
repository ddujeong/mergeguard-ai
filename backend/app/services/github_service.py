import requests
from app.core.config import GITHUB_TOKEN
import base64

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def parse_pr_url(pr_url: str):
    parts = pr_url.strip("/").split("/")

    owner = parts[3]
    repo = parts[4]
    pr_number = parts[6]

    return owner, repo, pr_number

def get_file_source(owner: str, repo: str, path: str, ref: str):

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"

    response = requests.get(
        url,
        headers=headers,
        params={
            "ref": ref
        }
    )

    if response.status_code != 200:
        return ""

    data = response.json()

    content = data.get("content")

    if not content:
        return ""

    return base64.b64decode(
        content
    ).decode("utf-8")

def get_pr_info(pr_url: str):
    owner, repo, pr_number = parse_pr_url(pr_url)

    pr_api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    files_api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    pr_response = requests.get(pr_api_url, headers=headers)
    pr_response.raise_for_status()

    files_response = requests.get(files_api_url, headers=headers)
    files_response.raise_for_status()

    pr_data = pr_response.json()
    head_sha = pr_data["head"]["sha"]
    files_data = files_response.json()

    files = []
    total_additions = 0
    total_deletions = 0

    for file in files_data:
        additions = file.get("additions", 0)
        deletions = file.get("deletions", 0)
        filename = file.get("filename")

        total_additions += additions
        total_deletions += deletions
        source_code = ""

        if filename and filename.endswith(".java"):
            source_code = get_file_source(
                owner,
                repo,
                filename,
                head_sha
            )
        files.append({
            "filename": file.get("filename"),
            "status": file.get("status"),
            "additions": additions,
            "deletions": deletions,
            "changes": file.get("changes", 0),
            "patch": file.get("patch", ""),
            "source_code": source_code
        })

    return {
        "repository": f"{owner}/{repo}",
        "pr_number": int(pr_number),
        "title": pr_data["title"],
        "state": pr_data["state"],
        "author": pr_data["user"]["login"],
        "base_branch": pr_data["base"]["ref"],
        "head_branch": pr_data["head"]["ref"],
        "changed_files": pr_data["changed_files"],
        "commits": pr_data["commits"],
        "total_additions": total_additions,
        "total_deletions": total_deletions,
        "files": files
    }
def get_open_pull_requests(owner: str, repo: str):

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=open"

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    return response.json()


def get_pull_request_files(owner: str, repo: str, pr_number: int):

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    response = requests.get(url, headers=headers)

    response.raise_for_status()

    return response.json()