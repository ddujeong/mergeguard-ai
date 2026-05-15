import requests


def parse_pr_url(pr_url: str):
    parts = pr_url.strip("/").split("/")

    owner = parts[3]
    repo = parts[4]
    pr_number = parts[6]

    return owner, repo, pr_number


def get_pr_info(pr_url: str):
    owner, repo, pr_number = parse_pr_url(pr_url)

    pr_api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    files_api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    pr_response = requests.get(pr_api_url)
    pr_response.raise_for_status()

    files_response = requests.get(files_api_url)
    files_response.raise_for_status()

    pr_data = pr_response.json()
    files_data = files_response.json()

    files = []
    total_additions = 0
    total_deletions = 0

    for file in files_data:
        additions = file.get("additions", 0)
        deletions = file.get("deletions", 0)

        total_additions += additions
        total_deletions += deletions

        files.append({
            "filename": file.get("filename"),
            "status": file.get("status"),
            "additions": additions,
            "deletions": deletions,
            "changes": file.get("changes", 0),
            "patch": file.get("patch", "")
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

    response = requests.get(url)

    response.raise_for_status()

    return response.json()


def get_pull_request_files(owner: str, repo: str, pr_number: int):

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    response = requests.get(url)

    response.raise_for_status()

    return response.json()