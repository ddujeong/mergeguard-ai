import requests


def parse_pr_url(pr_url: str):

    parts = pr_url.strip("/").split("/")

    owner = parts[3]
    repo = parts[4]
    pr_number = parts[6]

    return owner, repo, pr_number


def get_pr_info(pr_url: str):

    owner, repo, pr_number = parse_pr_url(pr_url)

    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"

    response = requests.get(api_url)

    response.raise_for_status()

    data = response.json()

    return {
        "title": data["title"],
        "state": data["state"],
        "author": data["user"]["login"],
        "base_branch": data["base"]["ref"],
        "head_branch": data["head"]["ref"],
        "changed_files": data["changed_files"],
        "commits": data["commits"]
    }