import requests

from app.core.config import GITHUB_TOKEN


headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}


def analyze_impact(
    repository: str,
    changed_methods: list
):

    impacted_methods = {}

    owner, repo = repository.split("/")

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/contents"
    )

    response = requests.get(
        url,
        headers=headers
    )

    if response.status_code != 200:
        return {}

    impacted_methods = {
        method: []
        for method in changed_methods
    }

    return impacted_methods